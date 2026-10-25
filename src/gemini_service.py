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
        self.gemini_api_key = gemini_api_key or GEMINI_API_KEY
        self.groq_api_key = groq_api_key or GROQ_API_KEY
        self.gemini_model = GEMINI_MODEL
        self.groq_model = GROQ_MODEL
        self.kb = knowledge_base or KnowledgeBase()
        self.ext_search = ExternalSearchService(enabled=True)
        self._gemini_client = None
        self._init_gemini_client()

    def _init_gemini_client(self) -> None:
        """Initialize Google GenAI client."""
        if not self.gemini_api_key or self.gemini_api_key == "your_gemini_api_key_here":
            self._gemini_client = None
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
        chat_history_summary: Optional[str] = None,
    ) -> Tuple[Generator[str, None, None], List[SearchResult], Dict[str, Any]]:
        """Retrieve relevant context and stream the grounded answer.

        Returns:
            Tuple of:
            - text_chunk_generator (Generator yielding text strings)
            - list_of_search_results (List[SearchResult])
            - metadata_container (Dict holding citations, recommendations, provider used)
        """
        # 1. Retrieve knowledge from KnowledgeBase
        search_results = self.kb.search(query=query, scope=scope, top_k=3)
        context_text = self.kb.format_context_for_prompt(search_results)

        # 2. Check for external fallback if results are empty or query touches portal/bantuan
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
        if "skripsi" in q_low or "tugas akhir" in q_low:
            default_recs = ["Syarat Sidang UAPS", "Jalur Publikasi Jurnal", "Batas SKS Skripsi"]
        elif "uts" in q_low or "uas" in q_low or "jadwal" in q_low or "kalender" in q_low:
            default_recs = ["Batas Presensi 75%", "Jadwal Revisi KRS", "Prosedur Remedial"]
        elif "cuti" in q_low:
            default_recs = ["Maksimal 2 Semester Cuti", "Syarat Cuti ke Kaprodi", "Batas Masa Studi S1"]

        metadata_container["recommendations"] = default_recs

        # Provider routing
        if provider.lower() in ["llama", "groq"]:
            return self._stream_groq(full_prompt, system_instruction, metadata_container), search_results, metadata_container
        else:
            return self._stream_gemini(full_prompt, system_instruction, context_text, metadata_container), search_results, metadata_container

    def _stream_gemini(
        self,
        full_prompt: str,
        system_instruction: str,
        context_text: str,
        metadata_container: Dict[str, Any],
    ) -> Generator[str, None, None]:
        """Stream output from Google Gemini."""
        if not self.is_gemini_configured():
            yield (
                "Berikut adalah ringkasan kebijakan resmi yang berhasil ditemukan dari dokumen kampus:\n\n"
                + context_text + "\n\n"
                "*(Catatan: Masukkan GEMINI_API_KEY Anda di menu Pengaturan atau file `.env` untuk mengaktifkan pemrosesan narasi penuh model Gemini 3.8 Flash).*"
            )
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
                            temperature=0.3,
                        ),
                    )
                    for chunk in response:
                        if chunk.text:
                            full_accumulated += chunk.text
                            # Clean RECS tags on the fly so user doesn't see raw HTML tags
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
                        generation_config={"temperature": 0.3},
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

        yield f"❌ Terjadi kendala pada layanan Gemini: `{last_error}`. Silakan periksa kembali kuota API Key Anda."

    def _stream_groq(
        self,
        full_prompt: str,
        system_instruction: str,
        metadata_container: Dict[str, Any],
    ) -> Generator[str, None, None]:
        """Stream output from Groq API (Llama 3.3 70B)."""
        if not self.is_groq_configured():
            yield (
                "⚠️ **Kunci API Groq (Llama 3.3) Belum Dikonfigurasi**\n\n"
                "Untuk menggunakan model Llama 3.3 70B via Groq, masukkan **Groq API Key** Anda "
                "di halaman **Pengaturan** atau simpan di file `.env` (`GROQ_API_KEY=gsk_...`).\n\n"
                "*(Dapatkan API key secara gratis di [console.groq.com](https://console.groq.com)).*\n\n"
                "Kamu juga bisa beralih kembali ke **Google Gemini 3.8 Flash** di menu Pengaturan."
            )
            return

        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.groq_api_key.strip()}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": self.groq_model,
            "messages": [
                {"role": "system", "content": system_instruction},
                {"role": "user", "content": full_prompt},
            ],
            "temperature": 0.3,
            "stream": True,
        }

        full_accumulated = ""
        try:
            with httpx.Client(timeout=30.0) as client:
                with client.stream("POST", url, headers=headers, json=payload) as response:
                    if response.status_code != 200:
                        yield f"❌ Error Groq ({response.status_code}): {response.read().decode('utf-8')}"
                        return

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

        except Exception as exc:
            logger.error("Groq streaming error: %s", exc)
            yield f"❌ Terjadi kesalahan saat menghubungi API Groq (Llama 3.3): `{str(exc)}`"

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
