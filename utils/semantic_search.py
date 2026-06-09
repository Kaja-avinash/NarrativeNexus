# utils/semantic_search.py
"""
Semantic search using SentenceTransformers + NearestNeighbors.
Uses centralized model loader. Supports search history and suggested queries.
"""
import numpy as np
import streamlit as st
from utils.models import load_sentence_transformer
from utils.config import SEMANTIC_TOP_K

# Module-level state
_embeddings = None
_nn_index = None
_docs_store = None


def build_index(docs: list) -> bool:
    """
    Build semantic search index from document list.
    
    Returns:
        bool: True if index built successfully
    """
    global _embeddings, _nn_index, _docs_store
    
    if not docs:
        return False
    
    model = load_sentence_transformer()
    if model is None:
        return False
    
    try:
        from sklearn.neighbors import NearestNeighbors
        _docs_store = docs
        _embeddings = model.encode(docs, show_progress_bar=False, batch_size=32)
        _nn_index = NearestNeighbors(metric="cosine", algorithm="brute").fit(_embeddings)
        return True
    except Exception as e:
        return False


def query(q: str, top_k: int = None) -> list:
    """
    Query the semantic search index.
    
    Returns:
        list of dicts: [{doc, score, doc_index}]
    """
    global _embeddings, _nn_index, _docs_store
    
    top_k = top_k or SEMANTIC_TOP_K
    
    if _nn_index is None or _docs_store is None:
        return []
    
    model = load_sentence_transformer()
    if model is None:
        return []
    
    try:
        q_emb = model.encode([q], show_progress_bar=False)
        n_neighbors = min(top_k, len(_docs_store))
        dist, idx = _nn_index.kneighbors(q_emb, n_neighbors=n_neighbors)
        
        results = []
        for d, i in zip(dist[0], idx[0]):
            score = float(1 - d)
            if score > 0.05:  # Filter very low relevance
                results.append({
                    "doc": _docs_store[i],
                    "score": score,
                    "doc_index": int(i),
                    "relevance_pct": round(score * 100, 1),
                })
        
        return sorted(results, key=lambda x: x["score"], reverse=True)
    except Exception:
        return []


def is_index_ready() -> bool:
    """Check if the search index has been built."""
    return _nn_index is not None and _docs_store is not None


def get_document_count() -> int:
    """Return number of indexed documents."""
    return len(_docs_store) if _docs_store else 0


def find_similar_documents(docs: list, threshold: float = 0.5) -> list:
    """
    Find pairs of similar documents.
    Returns list of (doc_i, doc_j, score) tuples above threshold.
    """
    model = load_sentence_transformer()
    if model is None or len(docs) < 2:
        return []
    
    try:
        embeddings = model.encode(docs, show_progress_bar=False)
        from sklearn.metrics.pairwise import cosine_similarity
        sim_matrix = cosine_similarity(embeddings)
        
        pairs = []
        for i in range(len(docs)):
            for j in range(i + 1, len(docs)):
                score = float(sim_matrix[i][j])
                if score >= threshold:
                    pairs.append((i, j, score))
        
        return sorted(pairs, key=lambda x: x[2], reverse=True)
    except Exception:
        return []
