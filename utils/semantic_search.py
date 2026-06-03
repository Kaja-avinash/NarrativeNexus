from sentence_transformers import SentenceTransformer
from sklearn.neighbors import NearestNeighbors
import streamlit as st

model = None
embeddings = None
nn_index = None
docs_store = None


@st.cache_resource
def load_sentence_transformer():
    """Load model once and cache it"""
    return SentenceTransformer("all-MiniLM-L6-v2")


def build_index(docs):
    global model, embeddings, nn_index, docs_store
    docs_store = docs
    model = load_sentence_transformer()
    embeddings = model.encode(docs)
    nn_index = NearestNeighbors(metric="cosine").fit(embeddings)


def query(q, top_k=5):
    q_emb = model.encode([q])
    dist, idx = nn_index.kneighbors(q_emb, n_neighbors=top_k)
    results = []
    for d, i in zip(dist[0], idx[0]):
        results.append({"doc": docs_store[i], "score": float(1 - d)})
    return results
