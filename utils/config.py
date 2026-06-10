# utils/config.py
"""
Centralized configuration for NarrativeNexus AI
All constants, limits, and feature flags live here.
"""

import os

# ── App Identity ─────────────────────────────────────────────────────────────
APP_NAME = "NarrativeNexus AI"
APP_VERSION = "2.0.0"
APP_TAGLINE = "Transform Documents Into Intelligence"

# ── Color Palette ─────────────────────────────────────────────────────────────
COLOR_PRIMARY = "#7B2BFF"
COLOR_SECONDARY = "#00EAFF"
COLOR_ACCENT = "#FF2BFF"
COLOR_BG = "#0B0618"
COLOR_SURFACE = "#12082A"
COLOR_SURFACE_2 = "#1A0F35"
COLOR_TEXT = "#E8E8F0"
COLOR_MUTED = "#8B8BA0"
COLOR_SUCCESS = "#00FF88"
COLOR_WARNING = "#FFB830"
COLOR_ERROR = "#FF4455"

# ── File Upload Limits ────────────────────────────────────────────────────────
MAX_FILE_SIZE_MB = 50
MAX_FILES = 20
UPLOAD_DIR = "uploaded_files"

SUPPORTED_FORMATS = [
    "txt",
    "pdf",
    "docx",
    "doc",
    "csv",
    "xlsx",
    "xls",
    "json",
    "html",
    "htm",
    "md",
    "rtf",
    "xml",
    "pptx",
    "epub",
    "jpg",
    "jpeg",
    "png",
    "bmp",
    "tiff",
]

# ── NLP Settings ─────────────────────────────────────────────────────────────
DEFAULT_TOPIC_COUNT = 4
MIN_TOPICS = 2
MAX_TOPICS = 8
MAX_NER_CHARS = 5000
MAX_GRAPH_CHARS = 200000
MIN_WORDS_FOR_SUMMARY = 40
SUMMARY_CHUNK_WORDS = 700
SUMMARIZER_MAX_LENGTH = 150
SUMMARIZER_MIN_LENGTH = 50
SENTIMENT_MAX_CHARS = 512
SEMANTIC_TOP_K = 5

# ── Supported Languages ───────────────────────────────────────────────────────
SUPPORTED_LANGUAGES = {
    "en": "English",
    "es": "Spanish",
    "fr": "French",
    "de": "German",
    "it": "Italian",
    "pt": "Portuguese",
    "zh-cn": "Chinese",
    "ja": "Japanese",
    "ar": "Arabic",
    "hi": "Hindi",
    "ru": "Russian",
    "ko": "Korean",
}

# ── Feature Flags ─────────────────────────────────────────────────────────────
FEATURE_TRANSLATION = True  # Gracefully degrades if model unavailable
FEATURE_OCR = True  # Gracefully degrades if tesseract not installed
FEATURE_3D_MAP = True
FEATURE_KNOWLEDGE_GRAPH = True
FEATURE_COMPARISON = True

# ── Cache Settings ────────────────────────────────────────────────────────────
MODEL_CACHE_TTL = 3600  # seconds
SESSION_HISTORY_MAX = 20  # max history items

# ── Entity Types for Graph ────────────────────────────────────────────────────
ENTITY_TYPES = {
    "PERSON": {"color": "#FF6B9D", "label": "Person"},
    "ORG": {"color": "#00EAFF", "label": "Organization"},
    "GPE": {"color": "#7B2BFF", "label": "Location"},
    "DATE": {"color": "#FFB830", "label": "Date"},
    "MONEY": {"color": "#00FF88", "label": "Money"},
    "PRODUCT": {"color": "#FF9F43", "label": "Product"},
    "EVENT": {"color": "#EE5A24", "label": "Event"},
    "NORP": {"color": "#A29BFE", "label": "Nationality"},
}

# ── Environment Detection ─────────────────────────────────────────────────────
IS_CLOUD = os.environ.get("RENDER", False) or os.environ.get("STREAMLIT_SHARING", False)
DEBUG = os.environ.get("DEBUG", "false").lower() == "true"

# ── Model IDs ────────────────────────────────────────────────────────────────
SUMMARIZER_MODEL = "sshleifer/distilbart-cnn-12-6"
SUMMARIZER_REVISION = None
SENTENCE_TRANSFORMER_MODEL = "all-MiniLM-L6-v2"
SPACY_MODEL = "en_core_web_sm"
