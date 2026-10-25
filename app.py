"""VIKA (Virtual Interactive Knowledge Assistant) - Main Application Server.

FastAPI Full-Stack Engine delivering 100% pixel-perfect UI fidelity to the
Showcase Board mockups with real-time SSE streaming, Dual-LLM orchestration
(Google Gemini 3.8 & Llama 3.3 via Groq), and UNPAM academic document retrieval.

Author: Abu Ziyad Al Katani (zydalz)
License: MIT License
"""

import json
import logging
import os
from pathlib import Path
from typing import Any, Dict, List, Optional

import uvicorn
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from slowapi import Limiter
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address

from src.config import (
    ADMIN_PIN,
    APP_FULL_NAME,
    APP_NAME,
    APP_TAGLINE,
    ROOT_DIR,
    SERVER_HOST,
    SERVER_PORT,
    STATIC_DIR,
)
from src.gemini_service import AIService
from src.knowledge_base import KnowledgeBase

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

# Initialize Rate Limiter
limiter = Limiter(key_func=get_remote_address, default_limits=["120/minute"])

# Initialize FastAPI application
app = FastAPI(
    title=f"{APP_NAME} - {APP_FULL_NAME}",
    description="Asisten Virtual Akademik Universitas Pamulang berbasis Gemini & Llama RAG",
    version="2.0.0",
)
app.state.limiter = limiter


@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request: Request, exc: RateLimitExceeded) -> JSONResponse:
    """Clean handler for rate limit exceedances avoiding private internal functions."""
    return JSONResponse(
        status_code=429,
        content={"detail": "Batas frekuensi permintaan terlampaui (Rate limit exceeded). Silakan tunggu beberapa saat."},
    )

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static Files Mount
if STATIC_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

# Shared Engine Singletons
knowledge_base = KnowledgeBase()
ai_service = AIService(knowledge_base=knowledge_base)


# -------------------------------------------------------------
# Request & Response Schemas
# -------------------------------------------------------------
class ChatRequest(BaseModel):
    query: str = Field(..., description="Pertanyaan mahasiswa")
    style: str = Field(default="Kasual", description="Gaya bahasa (Kasual, Formal, Ringkas)")
    scope: str = Field(default="universitas", description="Cakupan rujukan (universitas, filkom, all)")
    provider: str = Field(default="gemini", description="Penyedia model (gemini atau llama/groq)")
    gemini_key: Optional[str] = Field(default=None, description="Kunci API Gemini opsional dari peramban")
    groq_key: Optional[str] = Field(default=None, description="Kunci API Groq opsional dari peramban")
    history_summary: Optional[str] = Field(default=None, description="Ringkasan riwayat percakapan")


class VerifyPinRequest(BaseModel):
    pin: str = Field(..., description="PIN Admin Developer")


class KeysUpdateRequest(BaseModel):
    gemini_key: Optional[str] = Field(default=None, description="Kunci API Gemini baru")
    groq_key: Optional[str] = Field(default=None, description="Kunci API Groq baru")
    admin_pin: Optional[str] = Field(default=None, description="PIN Admin Developer untuk verifikasi otentikasi")


# -------------------------------------------------------------
# Web & API Endpoints
# -------------------------------------------------------------
@app.get("/")
async def serve_index() -> FileResponse:
    """Serve the primary Single Page Application interface."""
    index_file = STATIC_DIR / "index.html"
    if not index_file.exists():
        raise HTTPException(status_code=404, detail="Index HTML not found")
    return FileResponse(str(index_file))


@app.get("/api/health")
async def health_check() -> Dict[str, Any]:
    """Health check endpoint indicating AI engine readiness and vector status."""
    ve = knowledge_base.vector_engine
    return {
        "status": "online",
        "app_name": APP_NAME,
        "tagline": APP_TAGLINE,
        "gemini_configured": ai_service.is_gemini_configured(),
        "groq_configured": ai_service.is_groq_configured(),
        "total_documents": len(knowledge_base.documents),
        "total_chunks": len(knowledge_base.chunks),
        "vector_engine": {
            "is_indexed": ve.is_indexed,
            "vector_source": ve.vector_source,
            "vector_dimension": ve.vector_dim,
            "total_chunks_indexed": len(ve.chunk_ids),
            "hybrid_alpha": ve.hybrid_alpha,
        },
    }


@app.get("/api/vector/status")
async def get_vector_status() -> Dict[str, Any]:
    """Return status and diagnostic metrics of the Hybrid Vector Retrieval Engine."""
    ve = knowledge_base.vector_engine
    return {
        "is_indexed": ve.is_indexed,
        "vector_source": ve.vector_source,
        "embedding_model": ve.embedding_model,
        "vector_dimension": ve.vector_dim,
        "total_chunks_indexed": len(ve.chunk_ids),
        "hybrid_alpha": ve.hybrid_alpha,
        "cache_exists": (ROOT_DIR / "data" / "processed" / "vector_embeddings.json").exists(),
    }


@app.get("/api/settings/keys")
async def get_keys_status() -> Dict[str, Any]:
    """Return status and masked keys for display in settings UI."""
    def mask_key(k: str) -> str:
        if not k or len(k) < 8:
            return ""
        return k[:4] + "••••••••" + k[-4:]

    return {
        "gemini_configured": ai_service.is_gemini_configured(),
        "groq_configured": ai_service.is_groq_configured(),
        "gemini_masked": mask_key(ai_service.gemini_api_key),
        "groq_masked": mask_key(ai_service.groq_api_key),
    }


@app.post("/api/settings/verify-pin")
@limiter.limit("10/minute")
async def verify_admin_pin(request: Request, payload: VerifyPinRequest) -> Dict[str, Any]:
    """Verify developer admin PIN before granting access to API key management."""
    if payload.pin.strip() == str(ADMIN_PIN).strip():
        return {
            "success": True,
            "message": "Autentikasi Admin Developer berhasil.",
        }
    raise HTTPException(status_code=403, detail="PIN Admin tidak valid. Akses ditolak.")


@app.post("/api/settings/keys")
async def update_api_keys(payload: KeysUpdateRequest) -> Dict[str, Any]:
    """Save new API keys into memory and persist to .env file."""
    # Verify Admin PIN authorization
    if not payload.admin_pin or payload.admin_pin.strip() != str(ADMIN_PIN).strip():
        raise HTTPException(
            status_code=403,
            detail="Autentikasi gagal: PIN Admin Developer diperlukan untuk memperbarui kunci API.",
        )

    env_path = ROOT_DIR / ".env"
    env_lines = []
    if env_path.exists():
        env_lines = env_path.read_text(encoding="utf-8").splitlines()

    def update_or_append(lines: List[str], key: str, val: str) -> List[str]:
        found = False
        new_lines = []
        for line in lines:
            if line.startswith(f"{key}=") or line.startswith(f"{key} ="):
                new_lines.append(f"{key}={val}")
                found = True
            else:
                new_lines.append(line)
        if not found:
            new_lines.append(f"{key}={val}")
        return new_lines

    if payload.gemini_key is not None:
        val = payload.gemini_key.strip()
        ai_service.set_api_keys(gemini_key=val)
        env_lines = update_or_append(env_lines, "GEMINI_API_KEY", val)

    if payload.groq_key is not None:
        val = payload.groq_key.strip()
        ai_service.set_api_keys(groq_key=val)
        env_lines = update_or_append(env_lines, "GROQ_API_KEY", val)

    try:
        env_path.write_text("\n".join(env_lines) + "\n", encoding="utf-8")
    except Exception as e:
        logger.warning("Could not write to .env file: %s", e)

    return {
        "success": True,
        "message": "Kunci API berhasil disimpan dan diaktifkan.",
        "gemini_configured": ai_service.is_gemini_configured(),
        "groq_configured": ai_service.is_groq_configured(),
    }


@app.get("/api/documents")
async def list_documents() -> List[Dict[str, Any]]:
    """Return the official registered catalog of 5 UNPAM reference documents."""
    return [doc.model_dump() for doc in knowledge_base.get_document_catalog()]


@app.post("/api/chat")
@limiter.limit("20/minute")
async def chat_stream_endpoint(request: Request, chat_req: ChatRequest) -> StreamingResponse:
    """Server-Sent Events (SSE) streaming endpoint for grounded academic chat."""
    query = chat_req.query.strip()
    if not query:
        raise HTTPException(status_code=400, detail="Query cannot be empty")

    logger.info("Received query: '%s' | style=%s, scope=%s, provider=%s", query, chat_req.style, chat_req.scope, chat_req.provider)

    generator, search_results, meta_container = ai_service.answer_query_stream(
        query=query,
        style=chat_req.style,
        scope=chat_req.scope,
        provider=chat_req.provider,
        gemini_key=chat_req.gemini_key,
        groq_key=chat_req.groq_key,
        chat_history_summary=chat_req.history_summary,
    )

    async def event_publisher():
        # 1. Send initial metadata (citations, external_source, recommendations)
        yield f"data: {json.dumps({'type': 'meta', **meta_container})}\n\n"

        # 2. Stream answer tokens
        for token in generator:
            yield f"data: {json.dumps({'type': 'token', 'content': token})}\n\n"

        # 3. Send final meta update if recommendations were enriched from model output
        yield f"data: {json.dumps({'type': 'meta', 'recommendations': meta_container.get('recommendations', [])})}\n\n"

        # 4. End of stream signal
        yield "data: [DONE]\n\n"

    return StreamingResponse(
        event_publisher(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )


if __name__ == "__main__":
    logger.info("Starting VIKA Web Application Server on http://%s:%d", SERVER_HOST, SERVER_PORT)
    uvicorn.run("app:app", host=SERVER_HOST, port=SERVER_PORT, reload=True)
