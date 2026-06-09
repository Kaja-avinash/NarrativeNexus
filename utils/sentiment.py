# utils/sentiment.py
"""
Sentiment analysis using HuggingFace pipeline.
Uses centralized model loader with BERT truncation and graceful fallback.
"""
from utils.models import load_sentiment_model
from utils.config import SENTIMENT_MAX_CHARS


def get_sentiment(text: str) -> dict:
    """
    Analyze sentiment of text.
    
    Returns:
        dict with keys: label, score, confidence_pct
    """
    if not text or not text.strip():
        return {"label": "NEUTRAL", "score": 0.5, "confidence_pct": 50}
    
    sentiment_model = load_sentiment_model()
    
    if sentiment_model is None:
        # Simple heuristic fallback
        positive_words = ["good", "great", "excellent", "positive", "success", "win", "best", "happy"]
        negative_words = ["bad", "poor", "terrible", "negative", "fail", "worst", "sad", "loss"]
        lower = text.lower()
        pos_count = sum(1 for w in positive_words if w in lower)
        neg_count = sum(1 for w in negative_words if w in lower)
        if pos_count > neg_count:
            return {"label": "POSITIVE", "score": 0.7, "confidence_pct": 70}
        elif neg_count > pos_count:
            return {"label": "NEGATIVE", "score": 0.7, "confidence_pct": 70}
        else:
            return {"label": "NEUTRAL", "score": 0.5, "confidence_pct": 50}
    
    try:
        # Truncate to BERT's token limit (512 tokens ≈ ~512 chars)
        truncated = text[:SENTIMENT_MAX_CHARS]
        out = sentiment_model(truncated)[0]
        return {
            "label": out["label"],
            "score": float(out["score"]),
            "confidence_pct": round(float(out["score"]) * 100, 1),
        }
    except Exception:
        return {"label": "UNKNOWN", "score": 0.5, "confidence_pct": 50}


def get_sentiment_batch(texts: list) -> list:
    """Process multiple texts for sentiment at once."""
    return [get_sentiment(t) for t in texts]


def sentiment_to_emoji(label: str) -> str:
    """Convert sentiment label to emoji."""
    mapping = {
        "POSITIVE": "😊",
        "NEGATIVE": "😔",
        "NEUTRAL": "😐",
        "UNKNOWN": "❓",
    }
    return mapping.get(label.upper(), "❓")


def sentiment_to_color(label: str) -> str:
    """Convert sentiment label to color."""
    mapping = {
        "POSITIVE": "#00FF88",
        "NEGATIVE": "#FF4455",
        "NEUTRAL": "#FFB830",
        "UNKNOWN": "#8B8BA0",
    }
    return mapping.get(label.upper(), "#8B8BA0")
