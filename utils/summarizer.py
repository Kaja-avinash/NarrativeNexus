# utils/summarizer.py
"""
Text summarization using HuggingFace DistilBART.
Uses centralized model loader. Includes chunking and graceful fallback.
"""
import streamlit as st
from utils.models import load_summarizer
from utils.config import (
    SUMMARIZER_MAX_LENGTH, SUMMARIZER_MIN_LENGTH,
    SUMMARY_CHUNK_WORDS, MIN_WORDS_FOR_SUMMARY
)


def chunk_text(text: str, max_words: int = SUMMARY_CHUNK_WORDS):
    """Split text into chunks for processing."""
    words = text.split()
    for i in range(0, len(words), max_words):
        yield " ".join(words[i: i + max_words])


def summarize(text: str, max_length: int = None, min_length: int = None) -> str:
    """
    Summarize text using DistilBART. Falls back to truncated excerpt if model unavailable.
    
    Args:
        text: Input text to summarize
        max_length: Max tokens in summary (defaults to config value)
        min_length: Min tokens in summary (defaults to config value)
    
    Returns:
        Summary string
    """
    max_length = max_length or SUMMARIZER_MAX_LENGTH
    min_length = min_length or SUMMARIZER_MIN_LENGTH
    
    text = text.strip()
    if not text:
        return "No text provided for summarization."
    
    words = text.split()
    if len(words) < MIN_WORDS_FOR_SUMMARY:
        return text
    
    summarize_model = load_summarizer()
    
    if summarize_model is None:
        # Fallback: extractive summary (first N words)
        return " ".join(words[:300]) + "..."
    
    summaries = []
    try:
        for chunk in chunk_text(text, max_words=SUMMARY_CHUNK_WORDS):
            if not chunk.strip():
                continue
            try:
                result = summarize_model(
                    chunk,
                    max_length=max_length,
                    min_length=min(min_length, max(1, len(chunk.split()) // 4)),
                    do_sample=False,
                    truncation=True,
                )
                if result and result[0].get("summary_text"):
                    summaries.append(result[0]["summary_text"])
            except Exception:
                # Fallback for this chunk
                summaries.append(" ".join(chunk.split()[:100]))
    except Exception as e:
        return " ".join(words[:300]) + f"... [Summary model error: {e}]"
    
    return " ".join(summaries) if summaries else " ".join(words[:300]) + "..."
