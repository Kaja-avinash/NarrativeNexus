import streamlit as st
from utils.config import FEATURE_TRANSLATION


@st.cache_resource(show_spinner=False)
def _check_translator_available():
    try:
        from deep_translator import GoogleTranslator

        return True
    except Exception:
        return False


def translate_to_english(text, detected_lang="auto"):
    if not text or not text.strip():
        return text, False

    if detected_lang == "en":
        return text, False

    if not FEATURE_TRANSLATION:
        return text, False

    try:
        from deep_translator import GoogleTranslator

        translated = GoogleTranslator(source="auto", target="en").translate(text)

        return translated or text, True

    except Exception:
        return text, False


def is_translation_available():
    try:
        from deep_translator import GoogleTranslator

        return True
    except ImportError:
        return False
