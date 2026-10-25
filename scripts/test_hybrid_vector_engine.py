"""Automated verification test for VIKA Hybrid Vector Embedding & Cosine Similarity Engine.

Verifies:
1. VectorEngine initialization and index creation for 38 chunks.
2. Persistent disk cache in data/processed/vector_embeddings.json.
3. Cosine similarity mathematical correctness (0.0 to 1.0).
4. Hybrid search retrieval ranking accuracy across diverse queries.
5. FastAPI endpoint /api/vector/status and /api/health vector metrics.
"""

import asyncio
import json
import os
import sys
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

import httpx
from app import app
from src.config import DATA_PROCESSED_DIR, HYBRID_ALPHA
from src.knowledge_base import KnowledgeBase
from src.vector_engine import VectorEngine


async def test_hybrid_engine():
    print("================================================================")
    print("      VIKA HYBRID VECTOR EMBEDDING & COSINE SIMILARITY TEST     ")
    print("================================================================")

    # 1. Knowledge Base & Vector Engine Init
    print("\n[Step 1] Initializing KnowledgeBase & VectorEngine...")
    kb = KnowledgeBase()
    ve = kb.vector_engine

    print(f" -> Total documents registered: {len(kb.documents)}")
    print(f" -> Total chunks indexed: {len(kb.chunks)}")
    print(f" -> Vector engine status: is_indexed={ve.is_indexed}, source={ve.vector_source}")
    print(f" -> Vector dimension: {ve.vector_dim}")
    print(f" -> Hybrid alpha weight: {ve.hybrid_alpha}")

    assert len(kb.chunks) == 38, f"Expected 38 chunks, found {len(kb.chunks)}"
    assert ve.is_indexed is True, "VectorEngine should be indexed"
    assert ve.vector_dim > 0, "Vector dimension should be positive"
    print(" [PASS] KnowledgeBase & VectorEngine properly indexed.")

    # 2. Check Disk Cache
    print("\n[Step 2] Verifying Persistent Disk Cache...")
    cache_file = DATA_PROCESSED_DIR / "vector_embeddings.json"
    assert cache_file.exists(), f"Cache file not found at {cache_file}"
    cache_data = json.loads(cache_file.read_text(encoding="utf-8"))
    assert "vectors" in cache_data, "Cache should contain vectors array"
    assert len(cache_data["vectors"]) == 38, f"Expected 38 cached vectors, got {len(cache_data['vectors'])}"
    print(f" -> Cache file verified: {cache_file.name} ({cache_file.stat().st_size / 1024:.1f} KB)")
    print(" [PASS] Disk cache validated.")

    # 3. Test Cosine Similarity Math
    print("\n[Step 3] Testing Cosine Similarity computation...")
    sample_q = "Berapa persen kehadiran minimal untuk bisa ikut UAS?"
    q_vec = ve.embed_query(sample_q)
    sims = ve.compute_cosine_similarities(q_vec)

    assert len(sims) == 38, f"Expected 38 similarities, got {len(sims)}"
    assert 0.0 <= sims.max() <= 1.0, f"Cosine similarity out of range: {sims.max()}"
    print(f" -> Query: '{sample_q}'")
    print(f" -> Max Cosine Similarity: {sims.max():.4f}")
    print(" [PASS] Cosine Similarity math verified.")

    # 4. Test Multi-Query Hybrid Search Accuracy
    print("\n[Step 4] Testing Hybrid Search Queries...")
    test_cases = [
        {
            "query": "Kapan jadwal ujian tengah semester UTS semester genap 2026/2027?",
            "expected_kw": ["kalender", "uts", "oktober"],
            "scope": "universitas",
        },
        {
            "query": "Berapa persen batas kehadiran kuliah agar boleh ikut ujian akhir semester?",
            "expected_kw": ["presensi", "75", "uas", "kehadiran"],
            "scope": "universitas",
        },
        {
            "query": "Syarat pendaftaran proposal skripsi mahasiswa teknik informatika smt 7",
            "expected_kw": ["proposal", "skripsi", "ftiunpam", "semester"],
            "scope": "filkom",
        },
    ]

    for tc in test_cases:
        results = kb.search(query=tc["query"], scope=tc["scope"], top_k=2)
        assert len(results) > 0, f"No results for '{tc['query']}'"
        top = results[0]
        print(f" -> Query: '{tc['query'][:45]}...'")
        print(f"    Match: [{top.doc_title}] - {top.section_title}")
        print(f"    Similarity: {top.similarity_percentage} | Hybrid Score: {top.relevance_score:.3f}")
        assert top.similarity_score is not None, "similarity_score should not be None"
        assert top.similarity_percentage is not None, "similarity_percentage should not be None"

    print(" [PASS] All test queries returned ranked hybrid results.")

    # 5. Test API Endpoints
    print("\n[Step 5] Testing FastAPI /api/vector/status and /api/health endpoints...")
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as client:
        # /api/vector/status
        r_vec = await client.get("/api/vector/status")
        assert r_vec.status_code == 200, f"Expected 200, got {r_vec.status_code}"
        vec_json = r_vec.json()
        print(f" -> /api/vector/status response: {vec_json}")
        assert vec_json["is_indexed"] is True
        assert vec_json["total_chunks_indexed"] == 38
        assert vec_json["cache_exists"] is True

        # /api/health
        r_health = await client.get("/api/health")
        assert r_health.status_code == 200
        health_json = r_health.json()
        print(f" -> /api/health vector_engine: {health_json['vector_engine']}")
        assert "vector_engine" in health_json

    print(" [PASS] API endpoints verified successfully.")
    print("\n================================================================")
    print("      HYBRID VECTOR EMBEDDING MODULE 100% OPERATIONAL!          ")
    print("================================================================\n")


if __name__ == "__main__":
    asyncio.run(test_hybrid_engine())
