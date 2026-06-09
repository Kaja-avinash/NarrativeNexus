# utils/language.py
"""
Language detection using langdetect.
"""


def detect_language(text: str) -> str:
    """
    Detect the language of the input text.
    Returns ISO 639-1 language code (e.g., 'en', 'es', 'fr').
    Falls back to 'en' on failure.
    """
    if not text or len(text.strip()) < 20:
        return "en"
    
    try:
        from langdetect import detect
        lang = detect(text[:2000])  # Use first 2000 chars for speed
        return lang or "en"
    except Exception:
        return "en"


def get_language_name(code: str) -> str:
    """Convert ISO 639-1 code to language name."""
    mapping = {
        "en": "English", "es": "Spanish", "fr": "French",
        "de": "German", "it": "Italian", "pt": "Portuguese",
        "zh-cn": "Chinese (Simplified)", "zh-tw": "Chinese (Traditional)",
        "ja": "Japanese", "ar": "Arabic", "hi": "Hindi",
        "ru": "Russian", "ko": "Korean", "nl": "Dutch",
        "sv": "Swedish", "da": "Danish", "no": "Norwegian",
        "fi": "Finnish", "pl": "Polish", "tr": "Turkish",
        "vi": "Vietnamese", "th": "Thai", "id": "Indonesian",
    }
    return mapping.get(code, code.upper())
