# utils/state.py
"""
Centralized session state management for NarrativeNexus AI.
Provides typed, versioned session state with activity tracking.
"""
import time
import streamlit as st
from typing import Any, Dict, List, Optional
from utils.config import SESSION_HISTORY_MAX


# ── Default State ─────────────────────────────────────────────────────────────
STATE_DEFAULTS: Dict[str, Any] = {
    # Document data
    "raw_docs": [],
    "cleaned_docs": [],
    "file_names": [],
    "file_sizes": [],
    "upload_timestamps": [],
    
    # Analysis results
    "summary": "",
    "topics_data": None,
    "sentiments": [],
    "ner_html": "",
    "graph_html": "",
    "detected_languages": [],
    "comparison_results": None,
    
    # Search
    "search_index_built": False,
    "search_history": [],
    "search_suggestions": [
        "What are the main themes?",
        "Who are the key people mentioned?",
        "What organizations are involved?",
        "What are the main conclusions?",
        "What problems are discussed?",
        "What solutions are proposed?",
        "What dates or events are mentioned?",
        "What is the overall sentiment?",
    ],
    
    # History
    "history": [],
    
    # Dashboard
    "total_docs_processed": 0,
    "total_searches": 0,
    "total_reports": 0,
    "total_topics_found": 0,
    "total_entities_found": 0,
    "total_languages_found": 0,
    "activity_log": [],
    
    # UI state
    "current_page": "🏠 Dashboard",
    "theme": "dark",
    "graph_filter_types": ["PERSON", "ORG", "GPE"],
    "onboarding_complete": False,
    "analysis_step": 0,
    "is_analyzing": False,
    "last_error": None,
    
    # Settings
    "settings": {
        "theme": "dark",
        "language": "en",
        "topic_count": 4,
        "show_animations": True,
        "export_format": "pdf",
        "max_summary_length": 150,
        "graph_entity_types": ["PERSON", "ORG", "GPE"],
        "semantic_top_k": 5,
    },
    
    # App version tracking
    "state_version": "2.0.0",
}


def init_state() -> None:
    """Initialize all session state defaults on first run."""
    for key, val in STATE_DEFAULTS.items():
        if key not in st.session_state:
            if isinstance(val, (dict, list)):
                import copy
                st.session_state[key] = copy.deepcopy(val)
            else:
                st.session_state[key] = val


def reset_analysis() -> None:
    """Reset only analysis-related state, preserving history and settings."""
    analysis_keys = [
        "raw_docs", "cleaned_docs", "file_names", "file_sizes",
        "upload_timestamps", "summary", "topics_data", "sentiments",
        "ner_html", "graph_html", "detected_languages", "comparison_results",
        "search_index_built", "analysis_step", "is_analyzing", "last_error",
    ]
    for key in analysis_keys:
        import copy
        st.session_state[key] = copy.deepcopy(STATE_DEFAULTS[key])


def log_activity(action: str, detail: str = "") -> None:
    """Add an entry to the activity log."""
    entry = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "action": action,
        "detail": detail,
        "ts_unix": time.time(),
    }
    if "activity_log" not in st.session_state:
        st.session_state.activity_log = []
    st.session_state.activity_log.insert(0, entry)
    # Keep max 100 activity entries
    if len(st.session_state.activity_log) > 100:
        st.session_state.activity_log = st.session_state.activity_log[:100]


def add_to_history(record: dict) -> None:
    """Add an analysis record to history."""
    if "history" not in st.session_state:
        st.session_state.history = []
    st.session_state.history.insert(0, record)
    if len(st.session_state.history) > SESSION_HISTORY_MAX:
        st.session_state.history = st.session_state.history[:SESSION_HISTORY_MAX]


def add_search_to_history(query: str, results: list) -> None:
    """Track search history."""
    if "search_history" not in st.session_state:
        st.session_state.search_history = []
    entry = {
        "query": query,
        "result_count": len(results),
        "timestamp": time.strftime("%H:%M:%S"),
    }
    # Avoid duplicate consecutive searches
    if not st.session_state.search_history or st.session_state.search_history[0]["query"] != query:
        st.session_state.search_history.insert(0, entry)
    if len(st.session_state.search_history) > 20:
        st.session_state.search_history = st.session_state.search_history[:20]
    # Update global stats
    st.session_state.total_searches += 1
    log_activity("Search", f'Query: "{query[:50]}"')


def increment_stat(stat_key: str, amount: int = 1) -> None:
    """Safely increment a global statistic."""
    current = st.session_state.get(stat_key, 0)
    st.session_state[stat_key] = current + amount


def get_stats() -> Dict[str, int]:
    """Return current dashboard statistics."""
    return {
        "docs": st.session_state.get("total_docs_processed", 0),
        "searches": st.session_state.get("total_searches", 0),
        "reports": st.session_state.get("total_reports", 0),
        "topics": st.session_state.get("total_topics_found", 0),
        "entities": st.session_state.get("total_entities_found", 0),
        "languages": st.session_state.get("total_languages_found", 0),
    }
