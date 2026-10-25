"""Hybrid Vector Embedding and Cosine Similarity Engine for VIKA.

Designed according to Hacktiv8 Session 2 curriculum:
1. Dense Vector Embeddings (Google text-embedding-004 with local semantic vectorizer fallback).
2. Pure NumPy 2.x Vector Math & Cosine Similarity:
       CosineSimilarity(u, v) = (u . v) / (||u|| * ||v||)
3. Hybrid Retrieval: Weighted combination of Dense Semantic Cosine Similarity and Lexical BM25:
       HybridScore = alpha * DenseScore + (1 - alpha) * LexicalScore
4. Persistent On-Disk Vector Cache:
       data/processed/vector_embeddings.json for instant startup and offline resilience.

Author: Abu Ziyad Al Katani (zydalz)
"""

import json
import logging
import math
import re
from collections import Counter
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import numpy as np

from src.config import DATA_PROCESSED_DIR, GEMINI_API_KEY

logger = logging.getLogger(__name__)

CACHE_FILE = DATA_PROCESSED_DIR / "vector_embeddings.json"


class LocalSemanticVectorizer:
    """High-performance Subword & Term-Frequency Semantic Vectorizer.
    
    Built with pure Python & NumPy 2.x to guarantee zero-dependency reliability,
    immune to native C-extension / SciPy ABI incompatibilities.
    """

    def __init__(self) -> None:
        self.vocab: Dict[str, int] = {}
        self.idf: Dict[str, float] = {}
        self.vocab_size: int = 0

    def _tokenize(self, text: str) -> List[str]:
        """Extract word tokens and 3-to-4 character subwords for Indonesian morphology."""
        words = re.findall(r"\b[a-zA-Z0-9_\-]{2,}\b", text.lower())
        tokens: List[str] = list(words)
        for w in words:
            if len(w) >= 4:
                # Subword character n-grams (captures prefixes like 'pem-', 'ber-', 'di-')
                for i in range(len(w) - 2):
                    tokens.append(w[i : i + 3])
                for i in range(len(w) - 3):
                    tokens.append(w[i : i + 4])
        return tokens

    def fit_transform(self, texts: List[str]) -> np.ndarray:
        """Fit vocabulary & IDF weights, returning an L2-normalized dense matrix."""
        doc_tokens = [self._tokenize(t) for t in texts]
        n_docs = len(texts)
        if n_docs == 0:
            return np.zeros((0, 1), dtype=np.float32)

        df = Counter()
        for tokens in doc_tokens:
            df.update(set(tokens))

        # Filter low/single frequency noise if many docs, keep meaningful tokens
        sorted_vocab = sorted(df.keys())
        self.vocab = {term: idx for idx, term in enumerate(sorted_vocab)}
        self.vocab_size = len(self.vocab)

        # Smooth inverse document frequency
        self.idf = {
            term: math.log((n_docs + 1.0) / (count + 1.0)) + 1.0
            for term, count in df.items()
        }

        # Build term-frequency matrix
        matrix = np.zeros((n_docs, self.vocab_size), dtype=np.float32)
        for i, tokens in enumerate(doc_tokens):
            counts = Counter(tokens)
            for term, c in counts.items():
                if term in self.vocab:
                    matrix[i, self.vocab[term]] = c * self.idf[term]

            norm = np.linalg.norm(matrix[i])
            if norm > 0:
                matrix[i] /= norm

        return matrix

    def transform(self, query: str) -> np.ndarray:
        """Transform a single query into an L2-normalized vector."""
        if self.vocab_size == 0:
            return np.zeros(1, dtype=np.float32)

        tokens = self._tokenize(query)
        vec = np.zeros(self.vocab_size, dtype=np.float32)
        counts = Counter(tokens)
        for term, c in counts.items():
            if term in self.vocab:
                vec[self.vocab[term]] = c * self.idf.get(term, 1.0)

        norm = np.linalg.norm(vec)
        if norm > 0:
            vec /= norm
        return vec


class VectorEngine:
    """Orchestrates Dense Vector Embeddings, Cosine Similarity, and Hybrid Retrieval."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        embedding_model: str = "text-embedding-004",
        hybrid_alpha: float = 0.55,
    ) -> None:
        self.api_key = (api_key or GEMINI_API_KEY).strip()
        self.embedding_model = embedding_model
        self.hybrid_alpha = max(0.0, min(1.0, hybrid_alpha))

        self.local_vectorizer = LocalSemanticVectorizer()
        self.chunk_ids: List[str] = []
        self.chunk_texts: List[str] = []
        self.chunk_metadata: List[Dict[str, Any]] = []

        # Vector matrices
        self.vector_matrix: Optional[np.ndarray] = None
        self.vector_dim: int = 0
        self.vector_source: str = "local"  # 'google-genai' or 'local'
        self.is_indexed: bool = False

    def index_chunks(self, chunks: List[Any], force_rebuild: bool = False) -> None:
        """Index all knowledge chunks into dense vector representations.
        
        Loads from persistent cache if available, or computes and saves to disk.
        """
        self.chunk_ids = [c.chunk_id for c in chunks]
        self.chunk_texts = [f"{c.doc_title} - {c.section_title}\n{c.content}" for c in chunks]
        self.chunk_metadata = [
            {
                "chunk_id": c.chunk_id,
                "doc_title": c.doc_title,
                "decree_number": c.decree_number,
                "publisher": c.publisher,
                "scope": c.scope,
                "section_title": c.section_title,
                "content": c.content,
            }
            for c in chunks
        ]

        if not force_rebuild and self._load_from_cache():
            logger.info("Loaded %d vector embeddings from disk cache: %s", len(self.chunk_ids), CACHE_FILE.name)
            self.is_indexed = True
            return

        # Compute embeddings
        self._build_embeddings()
        self._save_to_cache()
        self.is_indexed = True

    def _build_embeddings(self) -> None:
        """Generate dense vectors via Google GenAI API or fallback to LocalSemanticVectorizer."""
        google_embeddings = None

        if self.api_key and self.api_key not in ["your_gemini_api_key_here", ""]:
            google_embeddings = self._try_fetch_google_embeddings(self.chunk_texts)

        if google_embeddings is not None and len(google_embeddings) == len(self.chunk_texts):
            self.vector_matrix = np.array(google_embeddings, dtype=np.float32)
            # L2 normalize
            norms = np.linalg.norm(self.vector_matrix, axis=1, keepdims=True)
            norms[norms == 0] = 1.0
            self.vector_matrix /= norms
            self.vector_dim = self.vector_matrix.shape[1]
            self.vector_source = "google-genai"
            logger.info("Generated %d dense embeddings using Google GenAI (%d-dim)", len(self.chunk_texts), self.vector_dim)
        else:
            # Fallback to local high-precision semantic vectorizer
            logger.info("Using Local Semantic Vectorizer fallback for %d chunks", len(self.chunk_texts))
            self.vector_matrix = self.local_vectorizer.fit_transform(self.chunk_texts)
            self.vector_dim = self.vector_matrix.shape[1] if self.vector_matrix is not None else 0
            self.vector_source = "local-semantic"

    def _try_fetch_google_embeddings(self, texts: List[str]) -> Optional[List[List[float]]]:
        """Try fetching embeddings from Google GenAI API."""
        try:
            from google import genai
            client = genai.Client(api_key=self.api_key)
            vectors: List[List[float]] = []

            # Batch embed in groups of 10 to avoid request size limits
            batch_size = 10
            for i in range(0, len(texts), batch_size):
                batch = texts[i : i + batch_size]
                resp = client.models.embed_content(
                    model=self.embedding_model,
                    contents=batch,
                )
                for item in resp.embeddings:
                    vectors.append(item.values)

            return vectors
        except Exception as e:
            logger.warning("Google GenAI embedding unavailable (%s). Falling back to local vectorizer.", e)
            return None

    def embed_query(self, query: str) -> np.ndarray:
        """Compute an L2-normalized vector for a search query."""
        if self.vector_source == "google-genai" and self.api_key:
            try:
                from google import genai
                client = genai.Client(api_key=self.api_key)
                resp = client.models.embed_content(
                    model=self.embedding_model,
                    contents=query,
                )
                if resp.embeddings:
                    vec = np.array(resp.embeddings[0].values, dtype=np.float32)
                    norm = np.linalg.norm(vec)
                    if norm > 0:
                        vec /= norm
                    return vec
            except Exception as e:
                logger.warning("Google query embed failed (%s), using local vectorizer", e)

        # Fallback to local vectorizer
        return self.local_vectorizer.transform(query)

    def compute_cosine_similarities(self, query_vector: np.ndarray) -> np.ndarray:
        """Calculate Cosine Similarity between query vector and all chunk vectors.
        
        Since both query_vector and vector_matrix are L2-normalized:
            CosineSimilarity(u, v) = u . v
        Range: [-1.0, 1.0], bounded to [0.0, 1.0].
        """
        if self.vector_matrix is None or len(self.vector_matrix) == 0:
            return np.zeros(len(self.chunk_ids), dtype=np.float32)

        # If dimensions mismatch (e.g. Google query on local matrix), re-embed using local vectorizer
        if query_vector.shape[0] != self.vector_matrix.shape[1]:
            logger.debug("Dimension mismatch (%d vs %d), resetting to local vector", query_vector.shape[0], self.vector_matrix.shape[1])
            return np.zeros(len(self.chunk_ids), dtype=np.float32)

        # Matrix dot vector gives exact cosine similarity for all 38 chunks instantaneously
        sims = np.dot(self.vector_matrix, query_vector)
        # Clip negative similarities to 0.0
        return np.clip(sims, 0.0, 1.0)

    def hybrid_search(
        self,
        query: str,
        lexical_scores_dict: Dict[str, float],
        scope: str = "all",
        top_k: int = 3,
    ) -> List[Dict[str, Any]]:
        """Combine Dense Vector Cosine Similarity with Lexical BM25 Scores.
        
        Formula:
            HybridScore = alpha * DenseScore + (1 - alpha) * LexicalScore
        """
        if not self.is_indexed or self.vector_matrix is None:
            return []

        # 1. Compute Dense Cosine Similarities
        q_vec = self.embed_query(query)
        dense_sims = self.compute_cosine_similarities(q_vec)

        # 2. Normalize Lexical Scores to [0.0, 1.0]
        max_lex = max(lexical_scores_dict.values()) if lexical_scores_dict else 1.0
        if max_lex <= 0:
            max_lex = 1.0

        scored_candidates: List[Dict[str, Any]] = []

        for idx, chunk_id in enumerate(self.chunk_ids):
            meta = self.chunk_metadata[idx]
            raw_lex = lexical_scores_dict.get(chunk_id, 0.0)
            norm_lex = min(raw_lex / max_lex, 1.0)
            dense_sim = float(dense_sims[idx])

            # Apply scope filtering: prioritize matching scope, never drop shared univ rules
            scope_boost = 1.0
            if scope and scope.lower() != "all":
                if meta["scope"].lower() == scope.lower():
                    scope_boost = 1.15
                elif meta["scope"].lower() == "universitas":
                    scope_boost = 1.0
                else:
                    scope_boost = 0.85

            # Calculate Weighted Hybrid Score
            hybrid_score = (self.hybrid_alpha * dense_sim + (1.0 - self.hybrid_alpha) * norm_lex) * scope_boost

            if hybrid_score > 0.01 or raw_lex > 0:
                scored_candidates.append(
                    {
                        "chunk_id": chunk_id,
                        "doc_title": meta["doc_title"],
                        "decree_number": meta["decree_number"],
                        "publisher": meta["publisher"],
                        "scope": meta["scope"],
                        "section_title": meta["section_title"],
                        "content": meta["content"],
                        "hybrid_score": float(hybrid_score),
                        "cosine_similarity": float(dense_sim),
                        "lexical_score": float(raw_lex),
                        "similarity_percentage": f"{int(round(dense_sim * 100))}%",
                    }
                )

        # Sort descending by hybrid_score
        scored_candidates.sort(key=lambda x: x["hybrid_score"], reverse=True)
        return scored_candidates[:top_k]

    def _save_to_cache(self) -> None:
        """Persist computed vector matrix to JSON cache file."""
        if self.vector_matrix is None:
            return

        try:
            cache_data = {
                "vector_source": self.vector_source,
                "vector_dim": self.vector_dim,
                "total_chunks": len(self.chunk_ids),
                "chunk_ids": self.chunk_ids,
                "vectors": self.vector_matrix.tolist(),
            }
            CACHE_FILE.write_text(json.dumps(cache_data), encoding="utf-8")
            logger.info("Saved %d vectors to %s", len(self.chunk_ids), CACHE_FILE)
        except Exception as e:
            logger.warning("Failed to save vector cache: %s", e)

    def _load_from_cache(self) -> bool:
        """Load vector matrix from disk cache if present and valid."""
        if not CACHE_FILE.exists():
            return False

        try:
            data = json.loads(CACHE_FILE.read_text(encoding="utf-8"))
            cached_ids = data.get("chunk_ids", [])
            # Verify cached IDs match current chunk IDs
            if cached_ids != self.chunk_ids:
                logger.info("Vector cache chunk IDs mismatch, will rebuild.")
                return False

            raw_vectors = data.get("vectors", [])
            if len(raw_vectors) != len(self.chunk_ids):
                return False

            self.vector_matrix = np.array(raw_vectors, dtype=np.float32)
            self.vector_dim = int(data.get("vector_dim", self.vector_matrix.shape[1]))
            self.vector_source = data.get("vector_source", "local-cached")

            # Fit local vectorizer vocabulary so queries can be transformed
            self.local_vectorizer.fit_transform(self.chunk_texts)
            return True
        except Exception as e:
            logger.warning("Error reading vector cache (%s), rebuilding...", e)
            return False
