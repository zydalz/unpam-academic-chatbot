"""AI Orchestrator Service for VIKA.

Supports:
1. Google Gemini (Default / Recommended): gemini-3.8-flash / gemini-2.5-flash via Google GenAI SDK
2. Llama 3.3 (Groq API): llama-3.3-70b-versatile via standard streaming HTTP
3. Whitelisted external academic search fallback
4. Proactive recommendation chips extraction
"""

from __future__ import annotations

import json
import logging
import re
from typing import Any, Dict, Generator, List, Optional, Tuple

import httpx

from src.config import (
    GEMINI_API_KEY,
    GEMINI_MODEL,
    GROQ_API_KEY,
    GROQ_MODEL,
    GROQ_MODEL_CANDIDATES,
    LLM_MAX_OUTPUT_TOKENS,
    LLM_TEMPERATURE,
    LLM_TOP_K,
    LLM_TOP_P,
    MODEL_CANDIDATES,
)
from src.external_search import ExternalSearchService
from src.knowledge_base import KnowledgeBase, SearchResult
from src.prompts import build_augmented_prompt, build_system_instruction

logger = logging.getLogger(__name__)


class AIService:
    """Unified Multi-LLM provider for VIKA with Gemini & Llama 3.3 support."""

    def __init__(
        self,
        gemini_api_key: Optional[str] = None,
        groq_api_key: Optional[str] = None,
        knowledge_base: Optional[KnowledgeBase] = None,
    ) -> None:
        self.gemini_api_key = (gemini_api_key or GEMINI_API_KEY).strip()
        self.groq_api_key = (groq_api_key or GROQ_API_KEY).strip()
        self.gemini_model = GEMINI_MODEL
        self.groq_model = GROQ_MODEL
        self.temperature = LLM_TEMPERATURE
        self.top_p = LLM_TOP_P
        self.top_k = LLM_TOP_K
        self.max_output_tokens = LLM_MAX_OUTPUT_TOKENS
        self.kb = knowledge_base or KnowledgeBase()
        self.ext_search = ExternalSearchService(enabled=True)
        self._gemini_client = None
        self._gemini_sdk_type = "none"
        self._init_gemini_client()

    def set_api_keys(self, gemini_key: Optional[str] = None, groq_key: Optional[str] = None) -> None:
        """Update API keys dynamically at runtime."""
        if gemini_key is not None:
            self.gemini_api_key = gemini_key.strip()
            self._init_gemini_client()
        if groq_key is not None:
            self.groq_api_key = groq_key.strip()

    def _init_gemini_client(self) -> None:
        """Initialize Google GenAI client."""
        if not self.gemini_api_key or self.gemini_api_key in ["your_gemini_api_key_here", ""]:
            self._gemini_client = None
            self._gemini_sdk_type = "none"
            return

        try:
            from google import genai
            self._gemini_client = genai.Client(api_key=self.gemini_api_key)
            self._gemini_sdk_type = "new"
            logger.info("Initialized Google GenAI client (google-genai SDK).")
        except Exception as e_new:
            try:
                import google.generativeai as legacy_genai
                legacy_genai.configure(api_key=self.gemini_api_key)
                self._gemini_client = legacy_genai
                self._gemini_sdk_type = "legacy"
                logger.info("Initialized Google GenAI client (legacy SDK).")
            except Exception as e_legacy:
                logger.error("Failed to initialize Gemini SDK: %s | %s", e_new, e_legacy)
                self._gemini_client = None
                self._gemini_sdk_type = "none"

    def is_gemini_configured(self) -> bool:
        return self._gemini_client is not None and bool(self.gemini_api_key) and self.gemini_api_key != "your_gemini_api_key_here"

    def is_groq_configured(self) -> bool:
        return bool(self.groq_api_key) and self.groq_api_key != "your_groq_api_key_here"

    def answer_query_stream(
        self,
        query: str,
        style: str = "Kasual",
        scope: str = "all",
        provider: str = "gemini",
        gemini_key: Optional[str] = None,
        groq_key: Optional[str] = None,
        chat_history_summary: Optional[str] = None,
    ) -> Tuple[Generator[str, None, None], List[SearchResult], Dict[str, Any]]:
        """Retrieve relevant context and stream the grounded answer."""
        if gemini_key:
            self.set_api_keys(gemini_key=gemini_key)
        if groq_key:
            self.set_api_keys(groq_key=groq_key)

        # 1. Retrieve knowledge from KnowledgeBase
        search_results = self.kb.search(query=query, scope=scope, top_k=3)
        context_text = self.kb.format_context_for_prompt(search_results)

        # 2. Check for external fallback if needed
        external_context = ""
        ext_info = None
        if not search_results or any(k in query.lower() for k in ["bantuan", "sispema", "rekomendasi", "viktor", "portal"]):
            ext_info = self.ext_search.search_official_fallback(query)
            if ext_info:
                external_context = (
                    f"Rujukan Tambahan Portal Resmi:\n"
                    f"- Sumber: {ext_info['source_title']} ({ext_info['publisher']})\n"
                    f"- URL: {ext_info['source_url']}\n"
                    f"- Ringkasan Kebijakan: {ext_info['summary']}\n"
                )

        # 3. Build system instruction and augmented prompt
        system_instruction = build_system_instruction(style=style, scope=scope)
        full_prompt = build_augmented_prompt(
            user_query=query,
            context_text=context_text,
            chat_history_summary=chat_history_summary,
            external_context=external_context,
        )

        metadata_container: Dict[str, Any] = {
            "provider": provider,
            "citations": [
                {
                    "title": r.doc_title,
                    "decree": r.decree_number,
                    "publisher": r.publisher,
                    "section": r.section_title,
                }
                for r in search_results
            ],
            "external_source": ext_info,
            "recommendations": [],
        }

        # Dynamic default recommendations based on query keywords
        default_recs = ["Syarat Kehadiran UAS", "Prosedur Cuti Kuliah", "Panduan Tugas Akhir"]
        q_low = query.lower()
        if "skripsi" in q_low or "tugas akhir" in q_low or "sidang" in q_low:
            default_recs = ["Syarat Sidang UAPS", "Jalur Publikasi Jurnal", "Batas SKS Skripsi"]
        elif "uts" in q_low or "uas" in q_low or "jadwal" in q_low or "kalender" in q_low:
            default_recs = ["Batas Presensi 75%", "Jadwal Revisi KRS", "Prosedur Remedial"]
        elif "cuti" in q_low:
            default_recs = ["Maksimal 2 Semester Cuti", "Syarat Cuti ke Kaprodi", "Batas Masa Studi S1"]

        metadata_container["recommendations"] = default_recs

        # Provider routing
        if provider.lower() in ["llama", "groq"]:
            return self._stream_groq(full_prompt, system_instruction, metadata_container, search_results), search_results, metadata_container
        else:
            return self._stream_gemini(full_prompt, system_instruction, metadata_container, search_results), search_results, metadata_container

    def _stream_gemini(
        self,
        full_prompt: str,
        system_instruction: str,
        metadata_container: Dict[str, Any],
        search_results: List[SearchResult],
    ) -> Generator[str, None, None]:
        """Stream output from Google Gemini or render structured document fallback."""
        if not self.is_gemini_configured():
            yield from self._render_structured_fallback(search_results)
            return

        model_attempts = [self.gemini_model] + [m for m in MODEL_CANDIDATES if m != self.gemini_model]
        last_error = None

        full_accumulated = ""
        for m_name in model_attempts:
            try:
                if self._gemini_sdk_type == "new":
                    from google.genai import types
                    response = self._gemini_client.models.generate_content_stream(
                        model=m_name,
                        contents=full_prompt,
                        config=types.GenerateContentConfig(
                            system_instruction=system_instruction,
                            temperature=self.temperature,
                            top_p=self.top_p,
                            max_output_tokens=self.max_output_tokens,
                        ),
                    )
                    for chunk in response:
                        if chunk.text:
                            full_accumulated += chunk.text
                            clean_chunk = re.sub(r"<!--\s*RECS:.*?-->", "", chunk.text)
                            if clean_chunk:
                                yield clean_chunk
                    
                    self._extract_recs(full_accumulated, metadata_container)
                    return

                elif self._gemini_sdk_type == "legacy":
                    model = self._gemini_client.GenerativeModel(
                        model_name=m_name,
                        system_instruction=system_instruction,
                    )
                    response = model.generate_content(
                        full_prompt,
                        stream=True,
                        generation_config={
                            "temperature": self.temperature,
                            "top_p": self.top_p,
                            "max_output_tokens": self.max_output_tokens,
                        },
                    )
                    for chunk in response:
                        if chunk.text:
                            full_accumulated += chunk.text
                            clean_chunk = re.sub(r"<!--\s*RECS:.*?-->", "", chunk.text)
                            if clean_chunk:
                                yield clean_chunk

                    self._extract_recs(full_accumulated, metadata_container)
                    return

            except Exception as exc:
                logger.warning("Gemini model %s failed: %s. Trying next...", m_name, exc)
                last_error = exc
                continue

        # If call failed (e.g. quota limit), provide graceful structured answer from docs
        yield from self._render_structured_fallback(search_results, error_note=str(last_error))

    def _stream_groq(
        self,
        full_prompt: str,
        system_instruction: str,
        metadata_container: Dict[str, Any],
        search_results: List[SearchResult],
    ) -> Generator[str, None, None]:
        """Stream output from Groq API."""
        if not self.is_groq_configured():
            yield from self._render_structured_fallback(
                search_results,
                error_note="Kunci API Groq belum diisi. Masukkan di menu Pengaturan untuk mengaktifkan penalaran penuh Groq AI."
            )
            return

        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.groq_api_key.strip()}",
            "Content-Type": "application/json",
        }
        
        groq_attempts = [self.groq_model] + [m for m in GROQ_MODEL_CANDIDATES if m != self.groq_model]
        last_groq_error = None

        for gm in groq_attempts:
            payload = {
                "model": gm,
                "messages": [
                    {"role": "system", "content": system_instruction},
                    {"role": "user", "content": full_prompt},
                ],
                "temperature": self.temperature,
                "top_p": self.top_p,
                "max_tokens": self.max_output_tokens,
                "stream": True,
            }

            full_accumulated = ""
            try:
                with httpx.Client(timeout=30.0) as client:
                    with client.stream("POST", url, headers=headers, json=payload) as response:
                        if response.status_code != 200:
                            err_msg = response.read().decode('utf-8')
                            logger.warning("Groq model %s failed (%s): %s. Trying next candidate...", gm, response.status_code, err_msg)
                            last_groq_error = f"{response.status_code}: {err_msg}"
                            continue

                        for line in response.iter_lines():
                            if not line:
                                continue
                            if line.startswith("data: "):
                                data_str = line[6:].strip()
                                if data_str == "[DONE]":
                                    break
                                try:
                                    data_json = json.loads(data_str)
                                    delta = data_json["choices"][0]["delta"]
                                    content = delta.get("content", "")
                                    if content:
                                        full_accumulated += content
                                        clean_chunk = re.sub(r"<!--\s*RECS:.*?-->", "", content)
                                        if clean_chunk:
                                            yield clean_chunk
                                except Exception:
                                    continue

                self._extract_recs(full_accumulated, metadata_container)
                return

            except Exception as exc:
                logger.warning("Groq model %s connection error: %s. Trying next...", gm, exc)
                last_groq_error = str(exc)
                continue

        # If all candidates failed, fallback gracefully
        yield from self._render_structured_fallback(search_results, error_note=f"Groq: {last_groq_error}")

    def _render_structured_fallback(
        self,
        search_results: List[SearchResult],
        error_note: Optional[str] = None,
    ) -> Generator[str, None, None]:
        """Render a clean, human-readable structured response directly from documents."""
        if not search_results:
            yield "Mohon maaf, informasi mengenai hal tersebut belum tercantum dalam basis data resmi yang tersedia saat ini. Kamu bisa melakukan konfirmasi langsung ke loket atau sekretariat terkait di kampus."
            return

        top_doc = search_results[0]
        yield f"Berikut adalah ringkasan kebijakan resmi dari **{top_doc.doc_title}** ({top_doc.decree_number}):\n\n"

        # Format content cleanly (clean headings, strip raw markdown table pipes into lists)
        content = top_doc.content
        lines = [line.strip() for line in content.split("\n") if line.strip()]
        for line in lines:
            if line.startswith("## ") or line.startswith("### "):
                clean_title = re.sub(r"^#+\s*", "", line)
                yield f"\n### {clean_title}\n"
            elif "|" in line and not line.startswith("||"):
                # Table row -> clean bullet point
                parts = [p.strip() for p in line.split("|") if p.strip()]
                if len(parts) >= 2 and not all(c in "-:" for c in "".join(parts)):
                    yield f"- **{parts[0]}**: {parts[1]}\n"
            elif not line.startswith("||"):
                yield f"{line}\n"

        if error_note:
            yield f"\n*(Catatan Konfigurasi: {error_note})*\n"
        else:
            yield "\n*(💡 Tips: Kamu bisa memasukkan Kunci API Gemini atau Groq di menu Pengaturan agar VIKA dapat berinteraksi dengan penalaran AI penuh).*\n"

    def _extract_recs(self, text: str, metadata_container: Dict[str, Any]) -> None:
        """Extract recommendation chips from raw model output."""
        match = re.search(r"<!--\s*RECS:\s*(\[.*?\])\s*-->", text, re.DOTALL)
        if match:
            try:
                parsed = json.loads(match.group(1))
                if isinstance(parsed, list) and len(parsed) > 0:
                    metadata_container["recommendations"] = [str(p).strip() for p in parsed[:3]]
            except Exception:
                pass


# Backward compatibility alias
GeminiService = AIService
