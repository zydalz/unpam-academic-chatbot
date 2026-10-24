"""Gemini Service Integration for VIKA.

Provides streaming and batch generation using Google GenAI SDK (google-genai / google.generativeai)
with automatic fallback to available models and robust error handling.
"""

from __future__ import annotations

import logging
from typing import Generator, List, Optional, Tuple

from src.config import GEMINI_API_KEY, GEMINI_MODEL, MODEL_CANDIDATES
from src.knowledge_base import KnowledgeBase, SearchResult
from src.prompts import build_augmented_prompt, build_system_instruction

logger = logging.getLogger(__name__)


class GeminiService:
    """Wrapper around Google Gemini API with fallback capabilities."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        model_name: Optional[str] = None,
        knowledge_base: Optional[KnowledgeBase] = None,
    ) -> None:
        self.api_key = api_key or GEMINI_API_KEY
        self.model_name = model_name or GEMINI_MODEL
        self.kb = knowledge_base or KnowledgeBase()
        self._client = None
        self._init_client()

    def _init_client(self) -> None:
        """Initialize the Google GenAI SDK client."""
        if not self.api_key or self.api_key == "your_gemini_api_key_here":
            logger.warning("No valid Gemini API key configured.")
            self._client = None
            return

        try:
            # Preferred: google-genai (new SDK)
            from google import genai
            self._client = genai.Client(api_key=self.api_key)
            self._sdk_type = "new"
            logger.info("Initialized Google GenAI client (google-genai SDK).")
        except (ImportError, Exception) as e_new:
            try:
                # Fallback: google-generativeai (legacy SDK)
                import google.generativeai as legacy_genai
                legacy_genai.configure(api_key=self.api_key)
                self._client = legacy_genai
                self._sdk_type = "legacy"
                logger.info("Initialized Google GenAI client (legacy SDK).")
            except Exception as e_legacy:
                logger.error("Failed to initialize Gemini SDK: %s | %s", e_new, e_legacy)
                self._client = None
                self._sdk_type = "none"

    def is_configured(self) -> bool:
        """Check if a valid client is ready to use."""
        return self._client is not None and bool(self.api_key) and self.api_key != "your_gemini_api_key_here"

    def update_api_key(self, new_key: str) -> bool:
        """Update API key at runtime (e.g. from Streamlit settings page)."""
        self.api_key = new_key.strip()
        self._init_client()
        return self.is_configured()

    def answer_query_stream(
        self,
        query: str,
        style: str = "Kating Ramah",
        scope: str = "all",
        chat_history_summary: Optional[str] = None,
    ) -> Tuple[Generator[str, None, None], List[SearchResult]]:
        """Retrieve relevant context and stream the grounded answer.

        Returns:
            Tuple of (text_chunk_generator, list_of_search_results_for_citations)
        """
        # 1. Retrieve knowledge from KnowledgeBase
        search_results = self.kb.search(query=query, scope=scope, top_k=3)
        context_text = self.kb.format_context_for_prompt(search_results)

        # 2. Build system instruction and augmented prompt
        system_instruction = build_system_instruction(style=style, scope=scope)
        full_prompt = build_augmented_prompt(
            user_query=query,
            context_text=context_text,
            chat_history_summary=chat_history_summary,
        )

        # 3. Handle unconfigured API key gracefully
        if not self.is_configured():
            def unconfigured_stream() -> Generator[str, None, None]:
                yield (
                    "⚠️ **Kunci API Gemini Belum Dikonfigurasi**\n\n"
                    "Untuk berinteraksi langsung dengan AI, silakan masukkan **Gemini API Key** Anda "
                    "pada menu **Pengaturan (Settings)** di bilah navigasi atau simpan di file `.env` "
                    "(`GEMINI_API_KEY=...`).\n\n"
                    "*(Dapatkan API key secara gratis melalui [Google AI Studio](https://aistudio.google.com/)).*\n\n"
                    "---\n\n"
                    "Berikut adalah kutipan rujukan resmi yang berhasil ditemukan dalam sistem untuk pertanyaan Anda:\n\n"
                    + context_text
                )
            return unconfigured_stream(), search_results

        # 4. Stream response from Gemini
        def generator() -> Generator[str, None, None]:
            # Try current model and fallback models if needed
            model_attempts = [self.model_name] + [m for m in MODEL_CANDIDATES if m != self.model_name]
            last_error = None

            for m_name in model_attempts:
                try:
                    if self._sdk_type == "new":
                        from google.genai import types
                        response = self._client.models.generate_content_stream(
                            model=m_name,
                            contents=full_prompt,
                            config=types.GenerateContentConfig(
                                system_instruction=system_instruction,
                                temperature=0.3,
                            ),
                        )
                        for chunk in response:
                            if chunk.text:
                                yield chunk.text
                        return  # Successfully finished streaming

                    elif self._sdk_type == "legacy":
                        model = self._client.GenerativeModel(
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
                                yield chunk.text
                        return  # Successfully finished streaming

                except Exception as exc:
                    logger.warning("Model %s failed: %s. Trying next candidate...", m_name, exc)
                    last_error = exc
                    continue

            # If all model candidates failed
            yield (
                f"❌ **Terjadi kendala saat menghubungi layanan Gemini:**\n\n"
                f"`{str(last_error)}`\n\n"
                f"Pastikan koneksi internet aktif dan API Key memiliki kuota valid."
            )

        return generator(), search_results
