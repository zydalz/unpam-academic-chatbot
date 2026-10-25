"""Automated verification script for VIKA enhancements:
1. Anti-hallucination hyperparameters.
2. Multi-turn conversational memory.
3. Slowapi rate limiting middleware.
"""

import asyncio
import os
import sys
from pathlib import Path

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

import httpx
from app import app
from src.config import LLM_MAX_OUTPUT_TOKENS, LLM_TEMPERATURE, LLM_TOP_P


async def test_all():
    print("=== VIKA THREE ENHANCEMENTS VERIFICATION ===")

    # 1. Hyperparameters Check
    print(f"1. Hyperparameters in Config: Temp={LLM_TEMPERATURE}, TopP={LLM_TOP_P}, MaxTokens={LLM_MAX_OUTPUT_TOKENS}")
    assert LLM_TEMPERATURE == 0.2, "Expected temperature 0.2"
    assert LLM_TOP_P == 0.90, "Expected top_p 0.90"
    print("   -> Hyperparameter check: PASS")

    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as client:
        # 2. Multi-turn memory test
        print("2. Testing Multi-turn memory payload to /api/chat...")
        payload = {
            "query": "Berapa rincian biayanya?",
            "style": "Ringkas",
            "scope": "filkom",
            "provider": "gemini",
            "history_summary": "Mahasiswa: Kapan proposal skripsi 2026-1?\nVIKA: 24 - 25 September 2026.",
        }
        r = await client.post("/api/chat", json=payload)
        assert r.status_code == 200, f"Expected 200, got {r.status_code}"
        print(f"   -> Multi-turn chat status: {r.status_code} PASS")

        # 3. Rate limiter check on PIN verification
        print("3. Testing Rate Limiter on /api/settings/verify-pin (10/min limit)...")
        status_codes = []
        for i in range(12):
            resp = await client.post("/api/settings/verify-pin", json={"pin": "2026"})
            status_codes.append(resp.status_code)

        has_200 = 200 in status_codes
        has_429 = 429 in status_codes
        print(f"   -> Status codes over 12 rapid calls: {status_codes}")
        print(f"   -> Rate limiter active (200 OK then 429 Too Many Requests): {has_429}")
        assert has_429, "Rate limiter should have triggered 429"
        print("   -> Rate limiter check: PASS")

    print("\nALL THREE TASKS VERIFIED SUCCESSFULLY!")


if __name__ == "__main__":
    asyncio.run(test_all())
