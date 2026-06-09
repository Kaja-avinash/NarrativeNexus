# utils/translate.py
"""
Translation module with graceful fallback.
Uses deep-translator (Google Translate API) instead of broken googletrans.
Falls back gracefully if translation is unavailable.
"""
import streamlit as st
from utils.config import FEATURE_TRANSLATION


@st.cache_resource(show_spinner=False)
def _check_translator_available() -> bool:
    """Check if translation is available."""
    try:
        from deep_translator import GoogleTranslator
        # Quick sanity check
        result = GoogleTranslator(source="auto", target="en").translate("hello")
        return bool(result)
    except Exception:
        return False


def translate_to_english(text: str, detected_lang: str = "auto") -> tuple[str, bool]:
    """
    Translate text to English.
    
    Returns:
        tuple: (translated_text, was_translated)
    """
    if not text or not text.strip():
        return text, False
    
    if detected_lang == "en":
        return text, False
    
    if not FEATURE_TRANSLATION:
        return text, False
    
    try:
        from deep_translator import GoogleTranslator
        # Split into chunks (Google Translate has 5000 char limit)
        max_chars = 4500
        if len(text) <= max_chars:
            translated = GoogleTranslator(source="auto", target="en").translate(text)
            return translated or text, True
        else:
            # Chunk and translate
            chunks = [text[i:i+max_chars] for i in range(0, len(text), max_chars)]
            translated_chunks = []
            for chunk in chunks[:5]:  # limit to 5 chunks for performance
                try:
                    t = GoogleTranslator(source="auto", target="en").translate(chunk)
                    translated_chunks.append(t or chunk)
                except Exception:
                    translated_chunks.append(chunk)
            return " ".join(translated_chunks), True
    except ImportError:
        return text, False
    except Exception as e:
        # Graceful fallback: return original text
        return text, False


def is_translation_available() -> bool:
    """Check if translation service is available."""
    try:
        from deep_translator import GoogleTranslator
        return True
    except ImportError:
        return False
