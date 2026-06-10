# utils/models.py
"""
Centralized model loader for NarrativeNexus AI.
All heavy ML models are loaded here with @st.cache_resource to prevent
duplicate loading, memory leaks, and slow startup.
"""

import streamlit as st
from utils.config import (
    SUMMARIZER_MODEL,
    SUMMARIZER_REVISION,
    SENTENCE_TRANSFORMER_MODEL,
    SPACY_MODEL,
)


@st.cache_resource(show_spinner=False)
def load_spacy() -> "spacy.Language":
    """Load spaCy NLP model (cached singleton)."""
    try:
        import spacy

        return spacy.load(SPACY_MODEL)
    except OSError:
        # Try to download if not found
        try:
            import subprocess, sys

            subprocess.run(
                [sys.executable, "-m", "spacy", "download", SPACY_MODEL],
                check=True,
                capture_output=True,
            )
            import spacy

            return spacy.load(SPACY_MODEL)
        except Exception as e:
            st.error(f"⚠️ spaCy model unavailable: {e}")
            return None


@st.cache_resource(show_spinner=False)
def load_summarizer():
    """Load summarization pipeline (cached singleton)."""
    try:
        from transformers import pipeline

        return pipeline(
            task="summarization",
            model=SUMMARIZER_MODEL,
            tokenizer=SUMMARIZER_MODEL,
        )

    except Exception:
        return None


@st.cache_resource(show_spinner=False)
def load_sentiment_model():
    """Load sentiment analysis pipeline (cached singleton)."""
    try:
        from transformers import pipeline

        return pipeline("sentiment-analysis")
    except Exception as e:
        st.warning(f"⚠️ Sentiment model unavailable: {e}")
        return None


@st.cache_resource(show_spinner=False)
def load_sentence_transformer():
    """Load sentence transformer model (cached singleton)."""
    try:
        from sentence_transformers import SentenceTransformer

        return SentenceTransformer(SENTENCE_TRANSFORMER_MODEL)
    except Exception as e:
        st.warning(f"⚠️ Sentence transformer unavailable: {e}")
        return None


def check_model_health() -> dict:
    """Check availability of all models. Returns dict of model statuses."""
    status = {}

    # spaCy
    try:
        import spacy

        spacy.load(SPACY_MODEL)
        status["spacy"] = True
    except Exception:
        status["spacy"] = False

    # Transformers
    try:
        from transformers import pipeline

        status["transformers"] = True
    except Exception:
        status["transformers"] = False

    # Sentence Transformers
    try:
        from sentence_transformers import SentenceTransformer

        status["sentence_transformers"] = True
    except Exception:
        status["sentence_transformers"] = False

    # Tesseract OCR
    try:
        import pytesseract

        pytesseract.get_tesseract_version()
        status["tesseract"] = True
    except Exception:
        status["tesseract"] = False

    # Translation
    try:
        from deep_translator import GoogleTranslator

        status["translation"] = True
    except Exception:
        status["translation"] = False

    return status
