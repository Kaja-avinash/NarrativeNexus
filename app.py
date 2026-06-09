"""
NarrativeNexus AI — Enterprise Document Intelligence Platform
Version 2.0.0 | Production Build

Transform Documents Into Intelligence
"""

import time
from pathlib import Path
import streamlit as st

# ── MUST BE FIRST ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="NarrativeNexus AI",
    layout="wide",
    page_icon="🧠",
    initial_sidebar_state="expanded",
    menu_items={
        "Get Help": "https://github.com/Kaja-avinash/NarrativeNexus",
        "Report a bug": "https://github.com/Kaja-avinash/NarrativeNexus/issues",
        "About": "NarrativeNexus AI v2.0 — Transform Documents Into Intelligence",
    },
)

# ── NLTK Downloads ────────────────────────────────────────────────────────────
import nltk
for corpus in ["punkt", "stopwords", "wordnet", "punkt_tab"]:
    try:
        nltk.download(corpus, quiet=True)
    except Exception:
        pass

import pandas as pd
import streamlit.components.v1 as components
import requests
import json
import io
from streamlit_lottie import st_lottie

# ── Import Utils ──────────────────────────────────────────────────────────────
_import_errors = []
try:
    from utils.config import *
    from utils.state import (
        init_state, reset_analysis, log_activity,
        add_to_history, add_search_to_history,
        increment_stat, get_stats,
    )
    from utils.file_utils import read_file, validate_file, sanitize_filename
    from utils.preprocessing import preprocess_text
    from utils.topic_modeling import extract_topics, generate_pyldavis
    from utils.summarizer import summarize
    from utils.sentiment import get_sentiment, sentiment_to_emoji, sentiment_to_color
    from utils.visualization import (
        show_wordcloud, plot_similarity_heatmap, show_card,
        show_kpi_card, show_skeleton_loader, show_step_progress,
        plot_3d_document_space, plot_sentiment_chart, plot_topic_radar, show_badge,
    )
    from utils.cosine_sim import compute_cosine_similarity
    from utils.semantic_search import build_index, query, is_index_ready, find_similar_documents
    from utils.language import detect_language
    from utils.translate import translate_to_english, is_translation_available
    from utils.report import generate_pdf, generate_csv, generate_json_report
    from utils.ner import highlight_entities, extract_entities
    from utils.graph import generate_knowledge_graph, get_graph_stats
except Exception as e:
    _import_errors.append(str(e))

# ── Initialize State ──────────────────────────────────────────────────────────
init_state()

# ── Upload Directory ──────────────────────────────────────────────────────────
UPLOAD_DIR = Path("uploaded_files")
UPLOAD_DIR.mkdir(exist_ok=True)


# ══════════════════════════════════════════════════════════════════════════════
# DESIGN SYSTEM — COMPLETE CSS ENGINE
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Orbitron:wght@700;900&display=swap" rel="stylesheet">

<style>
/* ═══════════════════════ CSS VARIABLES ════════════════════════════════════ */
:root {
    --nn-primary: #7B2BFF;
    --nn-secondary: #00EAFF;
    --nn-accent: #FF2BFF;
    --nn-bg: #0B0618;
    --nn-surface: #12082A;
    --nn-surface-2: #1A0F35;
    --nn-surface-3: #221545;
    --nn-border: rgba(123,43,255,0.25);
    --nn-border-glow: rgba(0,234,255,0.3);
    --nn-text: #E8E8F0;
    --nn-muted: #8B8BA0;
    --nn-success: #00FF88;
    --nn-warning: #FFB830;
    --nn-error: #FF4455;
    --nn-radius: 14px;
    --nn-radius-sm: 8px;
    --nn-shadow: 0 8px 32px rgba(0,0,0,0.5);
    --nn-glow-primary: 0 0 20px rgba(123,43,255,0.35);
    --nn-glow-secondary: 0 0 20px rgba(0,234,255,0.35);
    --nn-font: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    --nn-font-display: 'Orbitron', 'Inter', sans-serif;
    --nn-transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
}

/* ═══════════════════════ GLOBAL RESET ════════════════════════════════════ */
* { box-sizing: border-box; }

.stApp {
    background: var(--nn-bg);
    background-image:
        radial-gradient(ellipse 80% 50% at 50% -20%, rgba(123,43,255,0.15) 0%, transparent 60%),
        radial-gradient(ellipse 60% 40% at 80% 80%, rgba(0,234,255,0.08) 0%, transparent 50%);
    font-family: var(--nn-font);
    color: var(--nn-text);
    overflow-x: hidden;
}

/* ═══════════════════════ PARTICLES ════════════════════════════════════════ */
.nn-particles {
    position: fixed;
    top: 0; left: 0; width: 100%; height: 100%;
    overflow: hidden;
    z-index: 0;
    pointer-events: none;
}
.nn-particle {
    position: absolute;
    border-radius: 50%;
    opacity: 0.15;
    animation: particle-float linear infinite;
}
.nn-particle:nth-child(1)  { width:3px;height:3px;left:10%;background:var(--nn-secondary);animation-duration:18s;animation-delay:0s;top:100%; }
.nn-particle:nth-child(2)  { width:5px;height:5px;left:25%;background:var(--nn-primary);animation-duration:25s;animation-delay:3s;top:100%; }
.nn-particle:nth-child(3)  { width:2px;height:2px;left:50%;background:var(--nn-secondary);animation-duration:20s;animation-delay:6s;top:100%; }
.nn-particle:nth-child(4)  { width:4px;height:4px;left:75%;background:var(--nn-accent);animation-duration:15s;animation-delay:1s;top:100%; }
.nn-particle:nth-child(5)  { width:3px;height:3px;left:90%;background:var(--nn-primary);animation-duration:22s;animation-delay:8s;top:100%; }
.nn-particle:nth-child(6)  { width:6px;height:6px;left:35%;background:var(--nn-secondary);animation-duration:30s;animation-delay:4s;top:100%; }
.nn-particle:nth-child(7)  { width:2px;height:2px;left:60%;background:var(--nn-accent);animation-duration:16s;animation-delay:2s;top:100%; }
.nn-particle:nth-child(8)  { width:4px;height:4px;left:80%;background:var(--nn-primary);animation-duration:28s;animation-delay:9s;top:100%; }

@keyframes particle-float {
    0%   { transform: translateY(0) scale(1); opacity: 0; }
    5%   { opacity: 0.2; }
    95%  { opacity: 0.1; }
    100% { transform: translateY(-100vh) scale(0.5) rotate(360deg); opacity: 0; }
}

/* ═══════════════════════ SIDEBAR ══════════════════════════════════════════ */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0D0820 0%, var(--nn-surface) 100%) !important;
    border-right: 1px solid var(--nn-border) !important;
    box-shadow: 4px 0 24px rgba(0,0,0,0.4);
}
[data-testid="stSidebar"] > div { padding-top: 0 !important; }

/* ═══════════════════════ NAV ITEMS ════════════════════════════════════════ */
.nn-nav-item {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 12px 16px;
    margin: 3px 8px;
    border-radius: var(--nn-radius-sm);
    cursor: pointer;
    transition: var(--nn-transition);
    border: 1px solid transparent;
    font-family: var(--nn-font);
    font-size: 13px;
    font-weight: 500;
    color: var(--nn-muted);
    position: relative;
    overflow: hidden;
}
.nn-nav-item::before {
    content: '';
    position: absolute;
    left: 0; top: 0; width: 3px; height: 100%;
    background: var(--nn-primary);
    transform: scaleY(0);
    transition: transform 0.2s ease;
}
.nn-nav-item:hover {
    background: rgba(123,43,255,0.12);
    border-color: var(--nn-border);
    color: var(--nn-text);
    transform: translateX(4px);
}
.nn-nav-item.active {
    background: linear-gradient(135deg, rgba(123,43,255,0.2), rgba(0,234,255,0.08));
    border-color: var(--nn-border);
    color: var(--nn-text);
    font-weight: 600;
}
.nn-nav-item.active::before { transform: scaleY(1); }

/* ═══════════════════════ HEADER ═══════════════════════════════════════════ */
.nn-hero {
    text-align: center;
    padding: 40px 20px 30px;
    position: relative;
    z-index: 1;
}
.nn-logo {
    font-family: var(--nn-font-display);
    font-size: clamp(36px, 6vw, 62px);
    font-weight: 900;
    background: linear-gradient(135deg, var(--nn-primary) 0%, var(--nn-secondary) 50%, var(--nn-accent) 100%);
    background-size: 200% 200%;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    letter-spacing: 4px;
    animation: gradient-shift 5s ease infinite, float-title 4s ease-in-out infinite;
    margin: 0;
    line-height: 1.1;
}
.nn-tagline {
    font-family: var(--nn-font);
    font-size: clamp(12px, 2vw, 15px);
    color: var(--nn-secondary);
    letter-spacing: 4px;
    text-transform: uppercase;
    margin: 8px 0 0;
    opacity: 0.85;
    font-weight: 500;
}
@keyframes gradient-shift {
    0%, 100% { background-position: 0% 50%; }
    50%       { background-position: 100% 50%; }
}
@keyframes float-title {
    0%, 100% { transform: translateY(0); }
    50%       { transform: translateY(-6px); }
}

/* ═══════════════════════ GLASS CARDS ══════════════════════════════════════ */
.nn-card {
    background: rgba(18,8,42,0.7);
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    border: 1px solid var(--nn-border);
    border-radius: var(--nn-radius);
    padding: 22px 24px;
    margin-bottom: 18px;
    transition: var(--nn-transition);
    position: relative;
    overflow: hidden;
}
.nn-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0; height: 1px;
    background: linear-gradient(90deg, transparent, var(--nn-primary), var(--nn-secondary), transparent);
    opacity: 0;
    transition: opacity 0.3s ease;
}
.nn-card:hover {
    border-color: var(--nn-border-glow);
    transform: translateY(-2px);
    box-shadow: var(--nn-glow-primary);
}
.nn-card:hover::before { opacity: 1; }
.nn-card-title {
    font-family: var(--nn-font-display);
    font-size: 13px;
    font-weight: 700;
    color: var(--nn-secondary);
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 6px;
}
.nn-card-subtitle { color: var(--nn-muted); font-size: 12px; margin-bottom: 10px; }
.nn-card-content { color: var(--nn-text); font-size: 14px; line-height: 1.6; }

/* Gradient Card Variants */
.nn-card-primary { border-color: rgba(123,43,255,0.4); }
.nn-card-secondary { border-color: rgba(0,234,255,0.4); }
.nn-card-success { border-color: rgba(0,255,136,0.3); }

/* ═══════════════════════ KPI CARDS ════════════════════════════════════════ */
.kpi-card {
    background: rgba(18,8,42,0.8);
    backdrop-filter: blur(12px);
    border: 1px solid var(--nn-border);
    border-radius: var(--nn-radius);
    padding: 20px;
    text-align: center;
    transition: var(--nn-transition);
    position: relative;
    overflow: hidden;
}
.kpi-card::after {
    content: '';
    position: absolute;
    bottom: 0; left: 0; right: 0; height: 2px;
    background: linear-gradient(90deg, transparent, currentColor, transparent);
    opacity: 0.4;
}
.kpi-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 12px 40px rgba(0,0,0,0.4);
    border-color: var(--nn-border-glow);
}
.kpi-icon { font-size: 28px; margin-bottom: 8px; }
.kpi-value {
    font-family: var(--nn-font-display);
    font-size: 32px;
    font-weight: 900;
    margin-bottom: 4px;
    line-height: 1;
}
.kpi-label { color: var(--nn-muted); font-size: 12px; font-weight: 500; letter-spacing: 1px; text-transform: uppercase; }

/* ═══════════════════════ BUTTONS ══════════════════════════════════════════ */
.stButton > button {
    background: linear-gradient(135deg, var(--nn-primary), #5B1FBF) !important;
    border: 1px solid rgba(123,43,255,0.5) !important;
    color: white !important;
    font-family: var(--nn-font) !important;
    font-weight: 600 !important;
    font-size: 14px !important;
    letter-spacing: 0.5px !important;
    border-radius: var(--nn-radius-sm) !important;
    padding: 10px 22px !important;
    transition: var(--nn-transition) !important;
    box-shadow: 0 4px 12px rgba(123,43,255,0.3) !important;
}
.stButton > button:hover {
    background: linear-gradient(135deg, #9B4BFF, var(--nn-primary)) !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 24px rgba(123,43,255,0.5) !important;
}
.stButton > button[kind="secondary"] {
    background: rgba(255,255,255,0.05) !important;
    border: 1px solid var(--nn-border) !important;
    box-shadow: none !important;
}
.stButton > button[kind="secondary"]:hover {
    background: rgba(123,43,255,0.15) !important;
    border-color: var(--nn-border-glow) !important;
}

/* ═══════════════════════ INPUTS ═══════════════════════════════════════════ */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea,
.stSelectbox > div > div > div {
    background: rgba(18,8,42,0.8) !important;
    border: 1px solid var(--nn-border) !important;
    border-radius: var(--nn-radius-sm) !important;
    color: var(--nn-text) !important;
    font-family: var(--nn-font) !important;
    transition: var(--nn-transition) !important;
}
.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: var(--nn-primary) !important;
    box-shadow: 0 0 0 3px rgba(123,43,255,0.15) !important;
}

/* ═══════════════════════ TABS ═════════════════════════════════════════════ */
.stTabs [data-baseweb="tab-list"] {
    background: rgba(18,8,42,0.6) !important;
    border-radius: var(--nn-radius) !important;
    padding: 4px !important;
    border: 1px solid var(--nn-border) !important;
    gap: 4px !important;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    border-radius: var(--nn-radius-sm) !important;
    color: var(--nn-muted) !important;
    font-family: var(--nn-font) !important;
    font-size: 13px !important;
    font-weight: 500 !important;
    border: none !important;
    padding: 8px 14px !important;
    transition: var(--nn-transition) !important;
}
.stTabs [data-baseweb="tab"]:hover { color: var(--nn-text) !important; background: rgba(123,43,255,0.1) !important; }
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, rgba(123,43,255,0.3), rgba(0,234,255,0.15)) !important;
    color: var(--nn-text) !important;
    font-weight: 600 !important;
    box-shadow: 0 0 12px rgba(123,43,255,0.3) !important;
}

/* ═══════════════════════ PROGRESS BAR ═════════════════════════════════════ */
.stProgress > div > div > div {
    background: linear-gradient(90deg, var(--nn-primary), var(--nn-secondary)) !important;
    border-radius: 999px !important;
    box-shadow: 0 0 10px rgba(0,234,255,0.4) !important;
}
.stProgress > div > div {
    background: rgba(255,255,255,0.05) !important;
    border-radius: 999px !important;
    height: 6px !important;
}

/* ═══════════════════════ METRICS ══════════════════════════════════════════ */
[data-testid="stMetricValue"] {
    font-family: var(--nn-font-display) !important;
    font-size: 28px !important;
    color: var(--nn-secondary) !important;
    font-weight: 700 !important;
}
[data-testid="stMetricLabel"] { color: var(--nn-muted) !important; font-size: 12px !important; }
[data-testid="stMetricDelta"] { font-size: 12px !important; }

/* ═══════════════════════ EXPANDER ═════════════════════════════════════════ */
.streamlit-expanderHeader {
    background: rgba(18,8,42,0.8) !important;
    border: 1px solid var(--nn-border) !important;
    border-radius: var(--nn-radius-sm) !important;
    color: var(--nn-text) !important;
    font-family: var(--nn-font) !important;
}
.streamlit-expanderContent {
    background: rgba(11,6,24,0.8) !important;
    border: 1px solid var(--nn-border) !important;
    border-top: none !important;
}

/* ═══════════════════════ UPLOAD ZONE ══════════════════════════════════════ */
[data-testid="stFileUploader"] {
    border: 2px dashed var(--nn-border) !important;
    border-radius: var(--nn-radius) !important;
    background: rgba(18,8,42,0.5) !important;
    padding: 20px !important;
    transition: var(--nn-transition) !important;
}
[data-testid="stFileUploader"]:hover {
    border-color: var(--nn-primary) !important;
    background: rgba(123,43,255,0.08) !important;
}
[data-testid="stFileUploaderDropzone"] { background: transparent !important; }

/* ═══════════════════════ SLIDER ═══════════════════════════════════════════ */
.stSlider > div > div > div > div {
    background: linear-gradient(90deg, var(--nn-primary), var(--nn-secondary)) !important;
}

/* ═══════════════════════ BADGES ════════════════════════════════════════════ */
.nn-badge {
    display: inline-flex;
    align-items: center;
    padding: 3px 10px;
    border-radius: 999px;
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 0.5px;
    margin: 2px;
}

/* ═══════════════════════ WORKFLOW STEPS ════════════════════════════════════ */
.workflow-container {
    display: flex;
    flex-direction: column;
    gap: 10px;
    padding: 16px;
    background: rgba(18,8,42,0.6);
    border: 1px solid var(--nn-border);
    border-radius: var(--nn-radius);
}
.workflow-step {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 10px 14px;
    border-radius: var(--nn-radius-sm);
    font-size: 13px;
    font-weight: 500;
    transition: var(--nn-transition);
}
.workflow-step.step-done {
    background: rgba(0,255,136,0.08);
    border: 1px solid rgba(0,255,136,0.2);
    color: var(--nn-success);
}
.workflow-step.step-active {
    background: rgba(123,43,255,0.15);
    border: 1px solid var(--nn-border);
    color: var(--nn-secondary);
    animation: pulse-glow 1.5s ease-in-out infinite;
}
.workflow-step.step-pending {
    background: rgba(255,255,255,0.02);
    border: 1px solid rgba(255,255,255,0.05);
    color: var(--nn-muted);
}
.step-icon {
    width: 22px;
    height: 22px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 50%;
    font-size: 12px;
    font-weight: 700;
}
@keyframes pulse-glow {
    0%, 100% { box-shadow: 0 0 0 rgba(0,234,255,0); }
    50%       { box-shadow: 0 0 12px rgba(0,234,255,0.25); }
}

/* ═══════════════════════ SKELETON LOADER ═══════════════════════════════════ */
.skeleton {
    background: linear-gradient(90deg, rgba(255,255,255,0.03) 25%, rgba(255,255,255,0.07) 50%, rgba(255,255,255,0.03) 75%);
    background-size: 200% 100%;
    animation: skeleton-wave 1.8s ease-in-out infinite;
}
@keyframes skeleton-wave {
    0%   { background-position: 200% 0; }
    100% { background-position: -200% 0; }
}

/* ═══════════════════════ FILE CARD ═════════════════════════════════════════ */
.file-card {
    display: flex;
    align-items: center;
    gap: 14px;
    padding: 14px 16px;
    background: rgba(18,8,42,0.6);
    border: 1px solid var(--nn-border);
    border-radius: var(--nn-radius-sm);
    margin-bottom: 10px;
    transition: var(--nn-transition);
}
.file-card:hover {
    border-color: var(--nn-border-glow);
    background: rgba(123,43,255,0.08);
}
.file-icon { font-size: 24px; }
.file-info { flex: 1; min-width: 0; }
.file-name { font-weight: 600; font-size: 14px; color: var(--nn-text); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.file-meta { font-size: 12px; color: var(--nn-muted); margin-top: 2px; }

/* ═══════════════════════ SEARCH RESULT CARD ════════════════════════════════ */
.search-result {
    background: rgba(18,8,42,0.7);
    border: 1px solid var(--nn-border);
    border-radius: var(--nn-radius);
    padding: 18px 20px;
    margin-bottom: 14px;
    transition: var(--nn-transition);
    position: relative;
    overflow: hidden;
}
.search-result::before {
    content: '';
    position: absolute;
    left: 0; top: 0; bottom: 0; width: 3px;
    background: linear-gradient(180deg, var(--nn-primary), var(--nn-secondary));
}
.search-result:hover { border-color: var(--nn-border-glow); transform: translateX(4px); }
.search-score {
    font-family: var(--nn-font-display);
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 1px;
    color: var(--nn-secondary);
    text-transform: uppercase;
    margin-bottom: 8px;
}
.search-text { color: var(--nn-text); font-size: 14px; line-height: 1.65; }

/* ═══════════════════════ ACTIVITY LOG ══════════════════════════════════════ */
.activity-item {
    display: flex;
    gap: 12px;
    padding: 10px 0;
    border-bottom: 1px solid rgba(255,255,255,0.04);
    align-items: flex-start;
}
.activity-item:last-child { border-bottom: none; }
.activity-time { font-size: 11px; color: var(--nn-muted); white-space: nowrap; margin-top: 2px; }
.activity-text { font-size: 13px; color: var(--nn-text); line-height: 1.4; }
.activity-dot {
    width: 8px; height: 8px;
    border-radius: 50%;
    background: var(--nn-primary);
    margin-top: 5px;
    flex-shrink: 0;
    box-shadow: 0 0 6px rgba(123,43,255,0.6);
}

/* ═══════════════════════ SIDEBAR LOGO ══════════════════════════════════════ */
.sidebar-brand {
    padding: 20px 16px 16px;
    border-bottom: 1px solid var(--nn-border);
    margin-bottom: 8px;
}
.sidebar-brand-name {
    font-family: var(--nn-font-display);
    font-size: 16px;
    font-weight: 900;
    background: linear-gradient(135deg, var(--nn-primary), var(--nn-secondary));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    letter-spacing: 2px;
}
.sidebar-brand-version { font-size: 10px; color: var(--nn-muted); letter-spacing: 1px; margin-top: 2px; }
.sidebar-section-label {
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 2px;
    color: var(--nn-muted);
    text-transform: uppercase;
    padding: 12px 24px 4px;
    margin-top: 4px;
}

/* ═══════════════════════ COMPARISON TABLE ═══════════════════════════════════ */
.comparison-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 16px;
    margin-top: 16px;
}
.comparison-cell {
    background: rgba(18,8,42,0.7);
    border: 1px solid var(--nn-border);
    border-radius: var(--nn-radius);
    padding: 16px;
}
.comparison-cell-header {
    font-size: 11px;
    font-weight: 700;
    color: var(--nn-secondary);
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 10px;
}

/* ═══════════════════════ ONBOARDING ════════════════════════════════════════ */
.onboarding-step {
    display: flex;
    align-items: flex-start;
    gap: 16px;
    padding: 16px;
    margin-bottom: 12px;
    background: rgba(123,43,255,0.06);
    border: 1px solid rgba(123,43,255,0.2);
    border-radius: var(--nn-radius);
    transition: var(--nn-transition);
}
.onboarding-step:hover { background: rgba(123,43,255,0.12); }
.onboarding-num {
    width: 32px; height: 32px;
    border-radius: 50%;
    background: linear-gradient(135deg, var(--nn-primary), var(--nn-secondary));
    display: flex; align-items: center; justify-content: center;
    font-weight: 700; font-size: 14px; color: white;
    flex-shrink: 0;
}

/* ═══════════════════════ SETTINGS ══════════════════════════════════════════ */
.settings-section {
    background: rgba(18,8,42,0.6);
    border: 1px solid var(--nn-border);
    border-radius: var(--nn-radius);
    padding: 20px 24px;
    margin-bottom: 16px;
}
.settings-title {
    font-weight: 700;
    font-size: 14px;
    color: var(--nn-text);
    margin-bottom: 14px;
    padding-bottom: 10px;
    border-bottom: 1px solid var(--nn-border);
}

/* ═══════════════════════ DIVIDER ═══════════════════════════════════════════ */
.nn-divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, var(--nn-border), transparent);
    margin: 20px 0;
}

/* ═══════════════════════ RESPONSIVE ════════════════════════════════════════ */
@media (max-width: 768px) {
    .nn-logo { font-size: 28px; letter-spacing: 2px; }
    .kpi-value { font-size: 24px; }
    .nn-card { padding: 16px; }
}

/* ═══════════════════════ HIDE STREAMLIT DEFAULTS ═══════════════════════════ */
/*
 * IMPORTANT: Do NOT hide stHeader or collapsedControl.
 * stHeader contains the sidebar toggle button; hiding it locks users out
 * of the sidebar permanently after it is collapsed.
 *
 * Safe to hide: hamburger menu, footer, deploy button.
 * Must keep: stHeader frame, collapsedControl (sidebar toggle).
 */
#MainMenu { visibility: hidden; }
footer { visibility: hidden; }
.stDeployButton { display: none; }

/* Keep the header visible but make it transparent so it blends with our theme */
header[data-testid="stHeader"] {
    background: transparent !important;
    border-bottom: none !important;
}

/* Preserve the sidebar toggle button — NEVER hide this */
[data-testid="collapsedControl"] {
    display: flex !important;
    visibility: visible !important;
    opacity: 1 !important;
    color: var(--nn-text) !important;
}

/* Hide only the top-right Streamlit toolbar status/decoration (not the collapse button) */
[data-testid="stToolbar"] {
    display: none !important;
}

/* Ensure the sidebar itself is always accessible */
[data-testid="stSidebar"][aria-expanded="false"] {
    min-width: 0 !important;
    width: 0 !important;
}
[data-testid="stSidebarCollapsedControl"] {
    display: flex !important;
    visibility: visible !important;
    opacity: 1 !important;
}
</style>
""", unsafe_allow_html=True)


# ── Particles ─────────────────────────────────────────────────────────────────
st.markdown("""
<div class="nn-particles">
  <div class="nn-particle"></div><div class="nn-particle"></div>
  <div class="nn-particle"></div><div class="nn-particle"></div>
  <div class="nn-particle"></div><div class="nn-particle"></div>
  <div class="nn-particle"></div><div class="nn-particle"></div>
</div>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# LOTTIE LOADER
# ══════════════════════════════════════════════════════════════════════════════
@st.cache_data(ttl=3600, show_spinner=False)
def load_lottie(url: str):
    try:
        r = requests.get(url, timeout=5)
        if r.status_code == 200:
            return r.json()
    except Exception:
        pass
    return None


lottie_brain = load_lottie("https://lottie.host/014c53c4-e698-4f51-b855-385036152b1b/zZ4aO6J2F8.json")
lottie_loading = load_lottie("https://lottie.host/e2b604b3-d65d-424a-b50a-86717a6d8923/8H9y6Z55qj.json")
lottie_success = load_lottie("https://lottie.host/75db9ef1-1b9e-4fe5-9a47-fe3b8c38d527/MZihlPt0oL.json")


# ══════════════════════════════════════════════════════════════════════════════
# SIDEBAR NAVIGATION
# ══════════════════════════════════════════════════════════════════════════════
NAV_PAGES = [
    ("🏠", "Dashboard"),
    ("📄", "Documents"),
    ("🧠", "AI Analysis"),
    ("🔍", "Semantic Search"),
    ("🌐", "Knowledge Graph"),
    ("📊", "Visualizations"),
    ("📑", "Reports"),
    ("⚙", "Settings"),
]

with st.sidebar:
    # Brand
    st.markdown("""
    <div class="sidebar-brand">
        <div class="sidebar-brand-name">NARRATIVENEXUS</div>
        <div class="sidebar-brand-version">AI PLATFORM v2.0</div>
    </div>
    """, unsafe_allow_html=True)

    # Brain animation
    if lottie_brain:
        st_lottie(lottie_brain, height=140, key="sidebar_brain", speed=0.8)
    else:
        st.markdown('<div style="text-align:center;font-size:60px;padding:20px">🧠</div>', unsafe_allow_html=True)

    # Navigation
    st.markdown('<div class="sidebar-section-label">Navigation</div>', unsafe_allow_html=True)
    
    current = st.session_state.get("current_page", "Dashboard")
    for icon, name in NAV_PAGES:
        active_cls = "active" if current == name else ""
        # Has data indicator
        has_data = bool(st.session_state.get("cleaned_docs"))
        lock = "" if name in ["Dashboard", "Documents", "Settings"] or has_data else " 🔒"
        
        if st.button(
            f"{icon}  {name}{lock}",
            key=f"nav_{name}",
            use_container_width=True,
            type="secondary" if current != name else "primary",
        ):
            if lock and name not in ["Dashboard", "Documents", "Settings"]:
                st.warning("⚠️ Upload documents first!")
            else:
                st.session_state.current_page = name
                st.rerun()
    
    st.markdown('<div class="nn-divider"></div>', unsafe_allow_html=True)
    
    # Quick stats
    stats = get_stats()
    st.markdown('<div class="sidebar-section-label">Session Stats</div>', unsafe_allow_html=True)
    col_a, col_b = st.columns(2)
    with col_a:
        st.metric("Docs", stats["docs"])
        st.metric("Topics", stats["topics"])
    with col_b:
        st.metric("Searches", stats["searches"])
        st.metric("Reports", stats["reports"])
    
    st.markdown('<div class="nn-divider"></div>', unsafe_allow_html=True)
    
    # Model health
    if st.button("⚡ System Status", use_container_width=True, type="secondary"):
        try:
            from utils.models import check_model_health
            health = check_model_health()
            for model, ok in health.items():
                icon = "✅" if ok else "❌"
                st.markdown(f"{icon} **{model.replace('_', ' ').title()}**")
        except Exception as e:
            st.error(f"Health check failed: {e}")


# ══════════════════════════════════════════════════════════════════════════════
# GLOBAL HEADER
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="nn-hero">
    <h1 class="nn-logo">NARRATIVENEXUS</h1>
    <p class="nn-tagline">Transform Documents Into Intelligence</p>
</div>
""", unsafe_allow_html=True)

# Import errors warning (non-fatal)
if _import_errors:
    with st.expander("⚠️ Some modules loaded with warnings", expanded=False):
        for err in _import_errors:
            st.warning(err)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE ROUTER
# ══════════════════════════════════════════════════════════════════════════════
page = st.session_state.get("current_page", "Dashboard")


# ──────────────────────────────────────────────────────────────────────────────
# PAGE 1: DASHBOARD
# ──────────────────────────────────────────────────────────────────────────────
if page == "Dashboard":
    has_data = bool(st.session_state.get("cleaned_docs"))

    # Onboarding for new users
    if not st.session_state.get("onboarding_complete") and not has_data:
        st.markdown("""
        <div class="nn-card nn-card-primary" style="margin-bottom: 24px;">
            <div class="nn-card-title">👋 Welcome to NarrativeNexus AI</div>
            <div style="color: var(--nn-text); font-size: 14px; margin-bottom: 16px;">
                Your enterprise document intelligence platform. Here's how to get started:
            </div>
        </div>
        """, unsafe_allow_html=True)

        steps = [
            ("1", "Upload Documents", "Go to 📄 Documents and upload PDF, DOCX, PPTX, EPUB, CSV, Excel, Images, and more."),
            ("2", "Run AI Analysis", "Click Execute Analysis — AI will summarize, extract topics, entities, and build a knowledge graph."),
            ("3", "Explore Results", "Explore 🧠 AI Analysis, 🔍 Semantic Search, 🌐 Knowledge Graph, and 📊 Visualizations."),
            ("4", "Export Reports", "Generate professional PDF, CSV, or JSON reports in 📑 Reports."),
        ]
        for num, title, desc in steps:
            st.markdown(f"""
            <div class="onboarding-step">
                <div class="onboarding-num">{num}</div>
                <div>
                    <div style="font-weight: 600; color: var(--nn-text); margin-bottom: 4px;">{title}</div>
                    <div style="color: var(--nn-muted); font-size: 13px;">{desc}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        col_ob1, col_ob2 = st.columns([1, 3])
        with col_ob1:
            if st.button("🚀 Get Started", type="primary", use_container_width=True):
                st.session_state.onboarding_complete = True
                st.session_state.current_page = "Documents"
                st.rerun()
        with col_ob2:
            if st.button("Dismiss", type="secondary"):
                st.session_state.onboarding_complete = True
                st.rerun()

    # KPI Dashboard
    st.markdown("### 📊 Analytics Dashboard")
    stats = get_stats()

    kpi_data = [
        (str(stats["docs"]), "Documents Processed", "📄", "#7B2BFF"),
        (str(stats["topics"]), "Topics Extracted", "💭", "#00EAFF"),
        (str(stats["entities"]), "Entities Found", "🏷️", "#FF2BFF"),
        (str(stats["languages"]), "Languages Detected", "🌐", "#FFB830"),
        (str(stats["searches"]), "Search Queries", "🔍", "#00FF88"),
        (str(stats["reports"]), "Reports Generated", "📑", "#FF6B9D"),
    ]

    cols = st.columns(3)
    for i, (val, label, icon, color) in enumerate(kpi_data):
        with cols[i % 3]:
            show_kpi_card(val, label, icon, color)

    st.markdown('<div class="nn-divider"></div>', unsafe_allow_html=True)

    # Current Session Info + Activity Log
    col_main, col_activity = st.columns([2, 1])

    with col_main:
        if has_data:
            st.markdown("### 📂 Current Session")
            docs = st.session_state.raw_docs
            file_names = st.session_state.get("file_names", [])
            
            # File icons by type
            ext_icons = {
                ".pdf": "📄", ".docx": "📝", ".doc": "📝",
                ".pptx": "📊", ".xlsx": "📈", ".csv": "📋",
                ".epub": "📚", ".txt": "📃", ".json": "🔧",
                ".jpg": "🖼️", ".png": "🖼️", ".jpeg": "🖼️",
            }

            for i, (doc, fname) in enumerate(zip(docs, file_names)):
                ext = Path(fname).suffix.lower() if fname else ""
                icon = ext_icons.get(ext, "📄")
                words = len(doc.split())
                chars = len(doc)
                st.markdown(f"""
                <div class="file-card">
                    <div class="file-icon">{icon}</div>
                    <div class="file-info">
                        <div class="file-name">{fname or f"Document {i+1}"}</div>
                        <div class="file-meta">{words:,} words · {chars:,} characters</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

            # Quick action buttons
            st.markdown("#### Quick Actions")
            qcol1, qcol2, qcol3 = st.columns(3)
            with qcol1:
                if st.button("🧠 View Analysis", use_container_width=True):
                    st.session_state.current_page = "AI Analysis"
                    st.rerun()
            with qcol2:
                if st.button("🔍 Semantic Search", use_container_width=True):
                    st.session_state.current_page = "Semantic Search"
                    st.rerun()
            with qcol3:
                if st.button("📑 Export Report", use_container_width=True):
                    st.session_state.current_page = "Reports"
                    st.rerun()
        else:
            st.markdown("""
            <div class="nn-card" style="text-align: center; padding: 40px;">
                <div style="font-size: 48px; margin-bottom: 12px;">📭</div>
                <div style="color: var(--nn-muted); font-size: 14px;">No documents in current session.<br>Go to Documents to upload files.</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("📄 Upload Documents", type="primary"):
                st.session_state.current_page = "Documents"
                st.rerun()

    with col_activity:
        st.markdown("### 📋 Activity Log")
        activity = st.session_state.get("activity_log", [])
        if activity:
            activity_html = ""
            for item in activity[:15]:
                activity_html += f"""
                <div class="activity-item">
                    <div class="activity-dot"></div>
                    <div>
                        <div class="activity-text">{item['action']}</div>
                        {'<div class="activity-time">' + item.get('detail', '')[:40] + '</div>' if item.get('detail') else ''}
                        <div class="activity-time">{item['timestamp']}</div>
                    </div>
                </div>
                """
            st.markdown(f'<div class="nn-card">{activity_html}</div>', unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="nn-card" style="text-align: center; padding: 24px;">
                <div style="color: var(--nn-muted); font-size: 13px;">No activity yet.</div>
            </div>
            """, unsafe_allow_html=True)

    # History section
    if st.session_state.get("history"):
        st.markdown('<div class="nn-divider"></div>', unsafe_allow_html=True)
        st.markdown("### 🗂️ Analysis History")
        for idx, rec in enumerate(st.session_state.history[:5], 1):
            with st.expander(f"Session #{idx} — {rec.get('timestamp', 'Unknown')} — {len(rec.get('file_names', []))} documents"):
                files = rec.get("file_names", [])
                st.write("**Files:**", ", ".join(files) if files else "Pasted text")
                st.write("**Summary preview:**", rec.get("summary", "")[:300] + "...")
                
                dl_col1, dl_col2, dl_col3 = st.columns(3)
                if rec.get("pdf"):
                    with dl_col1:
                        st.download_button("📄 PDF", rec["pdf"],
                                           f"NarrativeNexus_{rec.get('timestamp','')}.pdf",
                                           key=f"hist_pdf_{idx}")
                if rec.get("csv"):
                    with dl_col2:
                        st.download_button("📋 CSV", rec["csv"],
                                           f"NarrativeNexus_{rec.get('timestamp','')}.csv",
                                           key=f"hist_csv_{idx}")
                if rec.get("json_report"):
                    with dl_col3:
                        st.download_button("🔧 JSON", rec["json_report"],
                                           f"NarrativeNexus_{rec.get('timestamp','')}.json",
                                           key=f"hist_json_{idx}")


# ──────────────────────────────────────────────────────────────────────────────
# PAGE 2: DOCUMENTS (Upload)
# ──────────────────────────────────────────────────────────────────────────────
elif page == "Documents":
    st.markdown("""
    <div class="nn-card nn-card-primary">
        <div class="nn-card-title">📄 Document Intelligence Hub</div>
        <div style="color: var(--nn-muted); font-size: 13px; margin-top: 4px;">
            Upload documents for AI-powered analysis. Supports 18+ file formats.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Format badges
    formats = ["PDF", "DOCX", "PPTX", "EPUB", "CSV", "Excel", "TXT", "JSON", "HTML", "RTF", "XML", "Markdown", "JPG/PNG (OCR)"]
    badge_html = " ".join([
        f'<span class="nn-badge" style="background: rgba(123,43,255,0.1); border: 1px solid rgba(123,43,255,0.3); color: #A89BFF;">{f}</span>'
        for f in formats
    ])
    st.markdown(f"<div style='margin-bottom: 16px;'>{badge_html}</div>", unsafe_allow_html=True)

    # Upload area
    uploaded_files = st.file_uploader(
        "Drag & drop files here or click to browse",
        type=SUPPORTED_FORMATS,
        accept_multiple_files=True,
        help=f"Maximum {MAX_FILE_SIZE_MB}MB per file. Up to {MAX_FILES} files.",
    )

    pasted_text = st.text_area(
        "Or paste text directly (use --- to separate multiple documents):",
        height=120,
        placeholder="Paste your text here...",
    )

    col_settings1, col_settings2 = st.columns(2)
    with col_settings1:
        topic_count = st.slider("Number of Topics (LDA)", MIN_TOPICS, MAX_TOPICS,
                                 st.session_state.settings.get("topic_count", DEFAULT_TOPIC_COUNT))
    with col_settings2:
        enable_translation = st.checkbox(
            "Auto-translate to English",
            value=False,
            help="Translate non-English documents before analysis. Requires internet connection.",
            disabled=not is_translation_available(),
        )
        if not is_translation_available():
            st.caption("⚠️ Translation service unavailable")

    # Action buttons
    col_run, col_clear = st.columns([2, 1])

    with col_run:
        run_analysis = st.button("🚀 Execute AI Analysis", type="primary", use_container_width=True)

    with col_clear:
        if st.button("🗑️ Clear Session", use_container_width=True, type="secondary"):
            reset_analysis()
            log_activity("Session cleared")
            st.success("Session cleared.")
            st.rerun()

    # Show currently uploaded files
    if st.session_state.get("raw_docs"):
        st.markdown('<div class="nn-divider"></div>', unsafe_allow_html=True)
        st.markdown("### 📂 Current Session Documents")
        for i, (doc, fname) in enumerate(zip(
            st.session_state.raw_docs,
            st.session_state.get("file_names", [f"Document {j+1}" for j in range(len(st.session_state.raw_docs))])
        )):
            ext = Path(fname).suffix.lower() if fname else ""
            ext_icons = {".pdf": "📄", ".docx": "📝", ".pptx": "📊", ".xlsx": "📈",
                         ".csv": "📋", ".epub": "📚", ".jpg": "🖼️", ".png": "🖼️"}
            icon = ext_icons.get(ext, "📄")
            with st.expander(f"{icon} {fname} — {len(doc.split()):,} words"):
                st.text(doc[:500] + ("..." if len(doc) > 500 else ""))

    # ── ANALYSIS EXECUTION ──────────────────────────────────────────────────
    if run_analysis:
        docs = []
        saved_names = []

        # Process uploaded files
        if uploaded_files:
            for f in uploaded_files[:MAX_FILES]:
                is_valid, err = validate_file(f)
                if not is_valid:
                    st.warning(f"⚠️ {f.name}: {err}")
                    continue
                try:
                    content = read_file(f)
                    if content and not content.startswith("["):
                        docs.append(content)
                        saved_names.append(sanitize_filename(f.name))
                        # Save file
                        dest = UPLOAD_DIR / sanitize_filename(f.name)
                        dest.write_bytes(f.getbuffer())
                    else:
                        st.warning(f"⚠️ {f.name}: {content}")
                        docs.append(content)
                        saved_names.append(sanitize_filename(f.name))
                except Exception as e:
                    st.error(f"❌ {f.name}: {e}")

        # Process pasted text
        if pasted_text.strip():
            parts = [p.strip() for p in pasted_text.split("---") if p.strip()]
            for i, part in enumerate(parts):
                docs.append(part)
                saved_names.append(f"Pasted Text {i+1}")

        if not docs:
            st.warning("⚠️ Please upload at least one document or paste some text.")
        else:
            st.session_state.settings["topic_count"] = topic_count

            # AI Workflow Progress
            WORKFLOW_STEPS = [
                "📁 Loading Documents",
                "🌐 Language Detection",
                "🧹 Text Preprocessing",
                "🤖 Generating Summary",
                "😊 Sentiment Analysis",
                "💭 Topic Modeling (LDA)",
                "🏷️ Named Entity Recognition",
                "🕸️ Building Knowledge Graph",
                "✅ Analysis Complete",
            ]

            progress_placeholder = st.empty()
            status_placeholder = st.empty()

            try:
                def update_progress(step_idx, message=""):
                    with progress_placeholder.container():
                        st.progress(step_idx / (len(WORKFLOW_STEPS) - 1))
                        show_step_progress(WORKFLOW_STEPS, step_idx)
                    if message:
                        status_placeholder.info(message)

                update_progress(0)

                # Language Detection
                detected_langs = []
                for doc in docs:
                    try:
                        lang = detect_language(doc[:1000])
                        detected_langs.append(lang)
                    except Exception:
                        detected_langs.append("en")

                update_progress(1, f"🌐 Detected languages: {', '.join(set(detected_langs))}")

                # Optional Translation
                final_docs = docs[:]
                if enable_translation and is_translation_available():
                    translated_docs = []
                    for doc, lang in zip(docs, detected_langs):
                        if lang != "en":
                            t_doc, was_translated = translate_to_english(doc, lang)
                            translated_docs.append(t_doc)
                        else:
                            translated_docs.append(doc)
                    final_docs = translated_docs

                # Preprocessing
                update_progress(2, "🧹 Preprocessing text...")
                cleaned = [preprocess_text(d) for d in final_docs]
                full_text = " ".join(final_docs)

                # Summarization
                update_progress(3, "🤖 Running neural summarizer...")
                summary = summarize(full_text)

                # Sentiment
                update_progress(4, "😊 Analyzing sentiment...")
                sentiments = [get_sentiment(d) for d in final_docs]

                # Topic Modeling
                update_progress(5, "💭 Extracting topics with LDA...")
                topics_data = extract_topics(cleaned, n_topics=topic_count)

                # NER
                update_progress(6, "🏷️ Recognizing entities...")
                ner_html = highlight_entities(full_text[:MAX_NER_CHARS])
                entities = extract_entities(full_text[:MAX_NER_CHARS])

                # Knowledge Graph
                update_progress(7, "🕸️ Constructing knowledge graph...")
                graph_entity_types = st.session_state.settings.get("graph_entity_types", ["PERSON", "ORG", "GPE"])
                graph_html = generate_knowledge_graph(full_text, entity_types=graph_entity_types)

                # Store in session
                st.session_state.raw_docs = final_docs
                st.session_state.cleaned_docs = cleaned
                st.session_state.file_names = saved_names
                st.session_state.summary = summary
                st.session_state.topics_data = topics_data
                st.session_state.sentiments = sentiments
                st.session_state.ner_html = ner_html
                st.session_state.graph_html = graph_html
                st.session_state.detected_languages = detected_langs
                st.session_state.search_index_built = False

                # Update stats
                increment_stat("total_docs_processed", len(docs))
                increment_stat("total_topics_found", topic_count)
                increment_stat("total_entities_found", len(entities))
                if detected_langs:
                    increment_stat("total_languages_found", len(set(detected_langs)))

                # Generate reports for history
                pdf_bytes = generate_pdf(
                    summary, topics_data["topics"], sentiments,
                    entities=entities, file_names=saved_names,
                )
                csv_content = generate_csv(topics_data["topics"], sentiments, entities)
                json_content = generate_json_report(
                    summary, topics_data["topics"], sentiments,
                    entities=entities, file_names=saved_names,
                )

                add_to_history({
                    "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                    "summary": summary,
                    "topics": topics_data["topics"],
                    "sentiments": sentiments,
                    "file_names": saved_names,
                    "pdf": pdf_bytes,
                    "csv": csv_content,
                    "json_report": json_content,
                })
                increment_stat("total_reports", 1)
                log_activity("Analysis complete", f"{len(docs)} docs processed")

                update_progress(8, "")
                progress_placeholder.empty()
                status_placeholder.empty()

                st.success("✅ Analysis complete! Navigate to 🧠 AI Analysis to explore results.")

                # Auto-navigate
                time.sleep(1.5)
                st.session_state.current_page = "AI Analysis"
                st.rerun()

            except Exception as e:
                progress_placeholder.empty()
                status_placeholder.empty()
                st.error(f"❌ Analysis failed: {e}")
                log_activity("Analysis failed", str(e)[:100])
                if DEBUG:
                    st.exception(e)


# ──────────────────────────────────────────────────────────────────────────────
# PAGE 3: AI ANALYSIS
# ──────────────────────────────────────────────────────────────────────────────
elif page == "AI Analysis":
    if not st.session_state.get("cleaned_docs"):
        st.markdown("""
        <div class="nn-card" style="text-align:center; padding:40px;">
            <div style="font-size:48px;">🧠</div>
            <h3 style="color: var(--nn-text);">No Analysis Available</h3>
            <div style="color: var(--nn-muted); margin-top: 8px;">Upload documents first to run AI analysis.</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("📄 Go to Documents", type="primary"):
            st.session_state.current_page = "Documents"
            st.rerun()
    else:
        tabs = st.tabs([
            "📋 Summary", "😊 Sentiment", "💭 Topics",
            "🏷️ Entities (NER)", "📐 Similarity", "🔄 Comparison",
        ])

        # TAB 1: Summary
        with tabs[0]:
            st.markdown("""
            <div class="nn-card nn-card-primary">
                <div class="nn-card-title">Executive Summary</div>
            </div>
            """, unsafe_allow_html=True)

            if st.session_state.summary:
                # Show summary with nice formatting
                st.markdown(f"""
                <div class="nn-card" style="padding: 28px;">
                    <div style="font-size: 15px; line-height: 1.8; color: var(--nn-text);">
                        {st.session_state.summary}
                    </div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.info("No summary generated.")

            # Document previews
            st.markdown("#### Document Previews")
            file_names = st.session_state.get("file_names", [])
            for i, doc in enumerate(st.session_state.raw_docs):
                fname = file_names[i] if i < len(file_names) else f"Document {i+1}"
                words = len(doc.split())
                lang = st.session_state.detected_languages[i] if i < len(st.session_state.detected_languages) else "en"
                with st.expander(f"📄 {fname} — {words:,} words · Language: {lang.upper()}"):
                    st.text_area("Content preview:", doc[:800] + ("..." if len(doc) > 800 else ""),
                                 height=150, key=f"preview_{i}", disabled=True)

        # TAB 2: Sentiment
        with tabs[1]:
            st.markdown("""
            <div class="nn-card nn-card-primary">
                <div class="nn-card-title">Sentiment Analysis</div>
                <div class="nn-card-subtitle">Emotional tone classification for each document</div>
            </div>
            """, unsafe_allow_html=True)

            sentiments = st.session_state.sentiments
            if sentiments:
                # Sentiment chart
                plot_sentiment_chart(sentiments)

                st.markdown("#### Per-Document Results")
                file_names = st.session_state.get("file_names", [])
                scols = st.columns(min(3, len(sentiments)))
                for i, s in enumerate(sentiments):
                    fname = file_names[i] if i < len(file_names) else f"Doc {i+1}"
                    emoji = sentiment_to_emoji(s["label"])
                    color = sentiment_to_color(s["label"])
                    with scols[i % len(scols)]:
                        st.markdown(f"""
                        <div class="kpi-card" style="border-top: 3px solid {color};">
                            <div class="kpi-icon">{emoji}</div>
                            <div class="kpi-value" style="color: {color}; font-size: 18px;">{s['label']}</div>
                            <div class="kpi-label">{fname[:20]}</div>
                            <div style="font-size: 12px; color: var(--nn-muted); margin-top: 6px;">{s.get('confidence_pct', s['score']*100):.1f}% confidence</div>
                        </div>
                        """, unsafe_allow_html=True)

        # TAB 3: Topics
        with tabs[2]:
            st.markdown("""
            <div class="nn-card nn-card-primary">
                <div class="nn-card-title">LDA Topic Modeling</div>
                <div class="nn-card-subtitle">Latent Dirichlet Allocation — discovered thematic clusters</div>
            </div>
            """, unsafe_allow_html=True)

            topics_data = st.session_state.topics_data
            if topics_data:
                topics = topics_data["topics"]

                # Topic radar chart
                col_radar, col_list = st.columns([1, 1])
                with col_radar:
                    plot_topic_radar(topics)
                with col_list:
                    for i, topic_words in enumerate(topics):
                        colors = ["#7B2BFF", "#00EAFF", "#FF2BFF", "#FFB830", "#00FF88", "#FF6B9D", "#A29BFE", "#74B9FF"]
                        color = colors[i % len(colors)]
                        words_html = " ".join([
                            f'<span class="nn-badge" style="background:{color}15;border:1px solid {color}40;color:{color};">{w}</span>'
                            for w in topic_words
                        ])
                        st.markdown(f"""
                        <div class="nn-card" style="padding: 16px; margin-bottom: 10px;">
                            <div style="font-size: 12px; font-weight: 700; color: {color}; margin-bottom: 8px; letter-spacing: 1px;">TOPIC {i+1}</div>
                            <div>{words_html}</div>
                        </div>
                        """, unsafe_allow_html=True)

                # Interactive LDA visualization
                if st.button("🗺️ Generate Interactive Topic Map", use_container_width=True):
                    with st.spinner("Generating pyLDAvis visualization..."):
                        try:
                            html_vis = generate_pyldavis(
                                topics_data["lda"],
                                topics_data["corpus"],
                                topics_data["dictionary"],
                            )
                            components.html(html_vis, height=820, scrolling=True)
                        except Exception as e:
                            st.error(f"Could not generate topic map: {e}")

        # TAB 4: Entities (NER)
        with tabs[3]:
            st.markdown("""
            <div class="nn-card nn-card-primary">
                <div class="nn-card-title">Named Entity Recognition</div>
                <div class="nn-card-subtitle">Persons, Organizations, Locations, Dates, and more</div>
            </div>
            """, unsafe_allow_html=True)

            if st.session_state.ner_html:
                components.html(st.session_state.ner_html, height=500, scrolling=True)

                # Entity breakdown
                entities = extract_entities(
                    " ".join(st.session_state.raw_docs)[:MAX_NER_CHARS]
                )
                if entities:
                    st.markdown("#### Entity Summary")
                    entity_by_type = {}
                    for e in entities:
                        label = e.get("description", e["label"])
                        entity_by_type.setdefault(label, []).append(e["text"])
                    
                    etype_cols = st.columns(min(4, len(entity_by_type)))
                    for i, (etype, ents) in enumerate(entity_by_type.items()):
                        with etype_cols[i % len(etype_cols)]:
                            st.metric(etype, len(ents))
                            with st.expander("Show all"):
                                st.write(", ".join(sorted(set(ents))[:20]))
            else:
                st.info("No entities detected. Try uploading documents with named people, organizations, or places.")

        # TAB 5: Similarity
        with tabs[4]:
            st.markdown("""
            <div class="nn-card nn-card-primary">
                <div class="nn-card-title">Document Similarity Matrix</div>
                <div class="nn-card-subtitle">Cosine similarity between all document pairs</div>
            </div>
            """, unsafe_allow_html=True)

            if len(st.session_state.cleaned_docs) >= 2:
                df_sim, highest = compute_cosine_similarity(st.session_state.cleaned_docs)
                plot_similarity_heatmap(df_sim)

                if highest and highest.get("pair"):
                    st.markdown(f"""
                    <div class="nn-card nn-card-success" style="margin-top: 16px;">
                        <div class="nn-card-title">🏆 Most Similar Pair</div>
                        <div style="font-size: 16px; color: var(--nn-text); margin-top: 6px;">
                            {highest['pair']} — <strong style="color: var(--nn-success);">{highest['score']:.1%}</strong> similarity
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("ℹ️ Upload at least 2 documents to see the similarity matrix.")

        # TAB 6: Multi-Document Comparison
        with tabs[5]:
            st.markdown("""
            <div class="nn-card nn-card-primary">
                <div class="nn-card-title">Multi-Document Comparison</div>
                <div class="nn-card-subtitle">Side-by-side comparison of key metrics</div>
            </div>
            """, unsafe_allow_html=True)

            docs = st.session_state.raw_docs
            file_names = st.session_state.get("file_names", [f"Doc {i+1}" for i in range(len(docs))])
            sentiments = st.session_state.sentiments
            detected_langs = st.session_state.get("detected_languages", ["en"] * len(docs))

            if len(docs) >= 2:
                # Comparison grid
                ncols = min(3, len(docs))
                cols = st.columns(ncols)
                
                for i, (doc, fname) in enumerate(zip(docs, file_names)):
                    with cols[i % ncols]:
                        words = len(doc.split())
                        chars = len(doc)
                        lang = detected_langs[i] if i < len(detected_langs) else "en"
                        sent = sentiments[i] if i < len(sentiments) else {"label": "N/A", "score": 0}
                        emoji = sentiment_to_emoji(sent["label"])
                        color = sentiment_to_color(sent["label"])
                        
                        st.markdown(f"""
                        <div class="comparison-cell">
                            <div class="comparison-cell-header">📄 {fname[:25]}</div>
                            <div style="display: flex; flex-direction: column; gap: 8px;">
                                <div style="display: flex; justify-content: space-between; font-size: 13px;">
                                    <span style="color: var(--nn-muted);">Words</span>
                                    <span style="color: var(--nn-text); font-weight: 600;">{words:,}</span>
                                </div>
                                <div style="display: flex; justify-content: space-between; font-size: 13px;">
                                    <span style="color: var(--nn-muted);">Characters</span>
                                    <span style="color: var(--nn-text); font-weight: 600;">{chars:,}</span>
                                </div>
                                <div style="display: flex; justify-content: space-between; font-size: 13px;">
                                    <span style="color: var(--nn-muted);">Language</span>
                                    <span style="color: var(--nn-text); font-weight: 600;">{lang.upper()}</span>
                                </div>
                                <div style="display: flex; justify-content: space-between; font-size: 13px;">
                                    <span style="color: var(--nn-muted);">Sentiment</span>
                                    <span style="color: {color}; font-weight: 600;">{emoji} {sent['label']}</span>
                                </div>
                                <div style="display: flex; justify-content: space-between; font-size: 13px;">
                                    <span style="color: var(--nn-muted);">Confidence</span>
                                    <span style="color: var(--nn-text); font-weight: 600;">{sent.get('confidence_pct', sent['score']*100):.1f}%</span>
                                </div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)

                # Semantic similarity between docs
                st.markdown("#### Semantic Similarity Pairs")
                with st.spinner("Computing semantic similarity..."):
                    try:
                        similar_pairs = find_similar_documents(docs, threshold=0.1)
                        if similar_pairs:
                            for i, j, score in similar_pairs[:10]:
                                fn_i = file_names[i] if i < len(file_names) else f"Doc {i+1}"
                                fn_j = file_names[j] if j < len(file_names) else f"Doc {j+1}"
                                bar_pct = int(score * 100)
                                color = "#00FF88" if score > 0.7 else "#FFB830" if score > 0.4 else "#FF4455"
                                st.markdown(f"""
                                <div class="nn-card" style="padding: 14px; margin-bottom: 8px;">
                                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                                        <span style="font-size: 13px; color: var(--nn-text);">{fn_i} ↔ {fn_j}</span>
                                        <span style="font-weight: 700; color: {color};">{score:.1%}</span>
                                    </div>
                                    <div style="background: rgba(255,255,255,0.05); border-radius: 4px; height: 4px;">
                                        <div style="background: {color}; width: {bar_pct}%; height: 4px; border-radius: 4px; transition: width 1s ease;"></div>
                                    </div>
                                </div>
                                """, unsafe_allow_html=True)
                        else:
                            st.info("No highly similar document pairs found.")
                    except Exception as e:
                        st.warning(f"Could not compute semantic similarity: {e}")
            else:
                st.info("ℹ️ Upload at least 2 documents to compare them.")


# ──────────────────────────────────────────────────────────────────────────────
# PAGE 4: SEMANTIC SEARCH
# ──────────────────────────────────────────────────────────────────────────────
elif page == "Semantic Search":
    st.markdown("""
    <div class="nn-card nn-card-secondary">
        <div class="nn-card-title">🔍 Neural Semantic Search</div>
        <div class="nn-card-subtitle">Search your documents by meaning, not just keywords</div>
    </div>
    """, unsafe_allow_html=True)

    if not st.session_state.get("raw_docs"):
        st.info("⚠️ Upload documents first to enable semantic search.")
        if st.button("📄 Go to Documents", type="primary"):
            st.session_state.current_page = "Documents"
            st.rerun()
    else:
        # Build index if not done
        if not st.session_state.get("search_index_built"):
            with st.spinner("🔄 Building semantic search index..."):
                success = build_index(st.session_state.raw_docs)
                if success:
                    st.session_state.search_index_built = True
                    st.success(f"✅ Index built — {len(st.session_state.raw_docs)} documents indexed.")
                else:
                    st.error("❌ Failed to build search index. Sentence transformer model unavailable.")

        # Suggested queries
        st.markdown("#### 💡 Suggested Queries")
        suggestions = st.session_state.get("search_suggestions", [])[:6]
        sug_cols = st.columns(3)
        for i, sug in enumerate(suggestions):
            with sug_cols[i % 3]:
                if st.button(f"  {sug}", key=f"sug_{i}", use_container_width=True, type="secondary"):
                    st.session_state["_pending_query"] = sug

        # Search input
        pending = st.session_state.pop("_pending_query", "")
        query_text = st.text_area(
            "Enter your search query:",
            value=pending,
            height=80,
            placeholder="e.g. What are the main risks discussed?",
        )

        top_k = st.slider("Number of results", 1, min(10, len(st.session_state.raw_docs)), SEMANTIC_TOP_K)

        if st.button("🔍 Execute Search", type="primary", use_container_width=True):
            if not query_text.strip():
                st.warning("Enter a search query.")
            elif not st.session_state.get("search_index_built"):
                st.error("Search index not ready. Please wait or re-upload documents.")
            else:
                with st.spinner("🔄 Searching..."):
                    results = query(query_text, top_k=top_k)
                    add_search_to_history(query_text, results)

                if results:
                    st.markdown(f"#### 📊 Found {len(results)} result{'s' if len(results) > 1 else ''}")
                    file_names = st.session_state.get("file_names", [])
                    
                    for r in results:
                        doc_idx = r.get("doc_index", 0)
                        fname = file_names[doc_idx] if doc_idx < len(file_names) else f"Document {doc_idx+1}"
                        rel_pct = r.get("relevance_pct", round(r["score"] * 100, 1))
                        
                        bar_color = "#00FF88" if rel_pct > 70 else "#FFB830" if rel_pct > 40 else "#FF4455"
                        bar_w = int(rel_pct)
                        
                        st.markdown(f"""
                        <div class="search-result">
                            <div class="search-score">
                                {fname} · {rel_pct}% relevance
                                <span style="float: right;">
                                    <span class="nn-badge" style="background: {bar_color}20; border: 1px solid {bar_color}40; color: {bar_color};">
                                        {rel_pct:.0f}%
                                    </span>
                                </span>
                            </div>
                            <div style="background: rgba(255,255,255,0.05); border-radius: 4px; height: 3px; margin-bottom: 12px;">
                                <div style="background: linear-gradient(90deg, var(--nn-primary), var(--nn-secondary)); width: {bar_w}%; height: 3px; border-radius: 4px;"></div>
                            </div>
                            <div class="search-text">{r["doc"][:400]}{'...' if len(r["doc"]) > 400 else ''}</div>
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.info("No relevant results found. Try rephrasing your query.")

        # Search History
        history = st.session_state.get("search_history", [])
        if history:
            st.markdown('<div class="nn-divider"></div>', unsafe_allow_html=True)
            st.markdown("#### 🕐 Recent Searches")
            for h in history[:10]:
                col_h1, col_h2 = st.columns([4, 1])
                with col_h1:
                    if st.button(f"🔍 {h['query']}", key=f"hist_{h['query'][:20]}", use_container_width=True, type="secondary"):
                        st.session_state["_pending_query"] = h["query"]
                        st.rerun()
                with col_h2:
                    st.caption(f"{h['result_count']} results · {h['timestamp']}")


# ──────────────────────────────────────────────────────────────────────────────
# PAGE 5: KNOWLEDGE GRAPH
# ──────────────────────────────────────────────────────────────────────────────
elif page == "Knowledge Graph":
    st.markdown("""
    <div class="nn-card nn-card-secondary">
        <div class="nn-card-title">🌐 Knowledge Graph</div>
        <div class="nn-card-subtitle">Entity relationship network — interactive visualization</div>
    </div>
    """, unsafe_allow_html=True)

    if not st.session_state.get("raw_docs"):
        st.info("⚠️ Upload documents first to generate the knowledge graph.")
    else:
        # Controls
        col_ctrl1, col_ctrl2, col_ctrl3 = st.columns(3)
        with col_ctrl1:
            entity_options = list(ENTITY_TYPES.keys())
            selected_types = st.multiselect(
                "Entity Types",
                entity_options,
                default=st.session_state.settings.get("graph_entity_types", ["PERSON", "ORG", "GPE"]),
                help="Filter which entity types appear in the graph",
            )
        with col_ctrl2:
            max_nodes = st.slider("Max Nodes", 20, 200, 100, step=10)
        with col_ctrl3:
            enable_physics = st.checkbox("Physics Simulation", value=True)

        regen_graph = st.button("🔄 Regenerate Graph", type="primary")

        if regen_graph or st.session_state.get("graph_html"):
            if regen_graph:
                with st.spinner("🕸️ Building knowledge graph..."):
                    full_text = " ".join(st.session_state.raw_docs)
                    st.session_state.graph_html = generate_knowledge_graph(
                        full_text,
                        entity_types=selected_types or ["PERSON", "ORG", "GPE"],
                        max_nodes=max_nodes,
                        physics=enable_physics,
                    )
                    st.session_state.settings["graph_entity_types"] = selected_types

            if st.session_state.graph_html:
                # Export controls
                exp_col1, exp_col2 = st.columns([3, 1])
                with exp_col2:
                    st.download_button(
                        "💾 Export HTML",
                        st.session_state.graph_html,
                        "knowledge_graph.html",
                        "text/html",
                        use_container_width=True,
                    )

                # Full-screen toggle
                height = st.slider("Graph Height (px)", 400, 900, 650, step=50)
                components.html(st.session_state.graph_html, height=height, scrolling=False)

                # Stats
                stats_col1, stats_col2, stats_col3 = st.columns(3)
                with stats_col1:
                    st.metric("Entity Types", len(selected_types or ["PERSON", "ORG", "GPE"]))
                with stats_col2:
                    word_count = len(" ".join(st.session_state.raw_docs).split())
                    st.metric("Text Analyzed", f"{word_count:,} words")
                with stats_col3:
                    st.metric("Max Nodes", max_nodes)
            else:
                st.info("No entity relationships found in the uploaded documents.")
        else:
            if st.button("🚀 Generate Knowledge Graph", type="primary", use_container_width=True):
                st.rerun()


# ──────────────────────────────────────────────────────────────────────────────
# PAGE 6: VISUALIZATIONS
# ──────────────────────────────────────────────────────────────────────────────
elif page == "Visualizations":
    st.markdown("""
    <div class="nn-card nn-card-primary">
        <div class="nn-card-title">📊 Data Visualizations</div>
        <div class="nn-card-subtitle">Visual intelligence from your documents</div>
    </div>
    """, unsafe_allow_html=True)

    if not st.session_state.get("cleaned_docs"):
        st.info("⚠️ Upload and analyze documents first to see visualizations.")
        if st.button("📄 Go to Documents", type="primary"):
            st.session_state.current_page = "Documents"
            st.rerun()
    else:
        viz_tabs = st.tabs(["☁️ Word Cloud", "🌌 3D Space", "📐 Heatmap", "🗺️ Topic Map"])

        # Word Cloud
        with viz_tabs[0]:
            st.markdown("""
            <div class="nn-card">
                <div class="nn-card-title">Word Frequency Cloud</div>
            </div>
            """, unsafe_allow_html=True)

            wc_col1, wc_col2 = st.columns([2, 1])
            with wc_col1:
                combined_text = " ".join(st.session_state.cleaned_docs)
                show_wordcloud(combined_text)

            with wc_col2:
                st.markdown("#### Top Keywords")
                from collections import Counter
                words = combined_text.split()
                freq = Counter(words).most_common(20)
                df_freq = pd.DataFrame(freq, columns=["Keyword", "Count"])
                df_freq["Count"] = df_freq["Count"].astype(int)
                st.dataframe(
                    df_freq.style.background_gradient(subset=["Count"], cmap="Purples"),
                    use_container_width=True,
                    height=350,
                )

        # 3D Space
        with viz_tabs[1]:
            st.markdown("""
            <div class="nn-card">
                <div class="nn-card-title">3D Document Vector Space</div>
                <div class="nn-card-subtitle">Semantic proximity visualization — drag to rotate</div>
            </div>
            """, unsafe_allow_html=True)
            plot_3d_document_space(
                st.session_state.cleaned_docs,
                labels=st.session_state.get("file_names"),
            )

        # Heatmap
        with viz_tabs[2]:
            st.markdown("""
            <div class="nn-card">
                <div class="nn-card-title">Document Similarity Heatmap</div>
            </div>
            """, unsafe_allow_html=True)
            if len(st.session_state.cleaned_docs) >= 2:
                df_sim, highest = compute_cosine_similarity(st.session_state.cleaned_docs)
                plot_similarity_heatmap(df_sim)
            else:
                st.info("Need at least 2 documents for similarity analysis.")

        # Topic Map
        with viz_tabs[3]:
            st.markdown("""
            <div class="nn-card">
                <div class="nn-card-title">Interactive Topic Map (pyLDAvis)</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("🗺️ Generate Interactive Topic Map", type="primary"):
                with st.spinner("Generating visualization..."):
                    try:
                        td = st.session_state.topics_data
                        html_vis = generate_pyldavis(td["lda"], td["corpus"], td["dictionary"])
                        components.html(html_vis, height=820, scrolling=True)
                    except Exception as e:
                        st.error(f"Topic map error: {e}")
            else:
                st.info("Click the button above to generate the interactive topic visualization.")


# ──────────────────────────────────────────────────────────────────────────────
# PAGE 7: REPORTS
# ──────────────────────────────────────────────────────────────────────────────
elif page == "Reports":
    st.markdown("""
    <div class="nn-card nn-card-primary">
        <div class="nn-card-title">📑 Report Center</div>
        <div class="nn-card-subtitle">Export your analysis in multiple formats</div>
    </div>
    """, unsafe_allow_html=True)

    if not st.session_state.get("cleaned_docs"):
        st.info("⚠️ No analysis data available. Upload and analyze documents first.")
        if st.button("📄 Go to Documents", type="primary"):
            st.session_state.current_page = "Documents"
            st.rerun()
    else:
        topics_data = st.session_state.topics_data
        sentiments = st.session_state.sentiments
        summary = st.session_state.summary
        file_names = st.session_state.get("file_names", [])
        entities = extract_entities(" ".join(st.session_state.raw_docs)[:MAX_NER_CHARS])

        # Export formats
        rep_col1, rep_col2, rep_col3 = st.columns(3)

        with rep_col1:
            st.markdown("""
            <div class="nn-card" style="text-align: center; padding: 28px;">
                <div style="font-size: 40px; margin-bottom: 10px;">📄</div>
                <div style="font-weight: 700; color: var(--nn-text); margin-bottom: 4px;">PDF Report</div>
                <div style="color: var(--nn-muted); font-size: 12px; margin-bottom: 16px;">
                    Full analysis with summary, topics, sentiment & entities
                </div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("📄 Generate PDF", type="primary", use_container_width=True):
                with st.spinner("Generating PDF..."):
                    try:
                        pdf_bytes = generate_pdf(
                            summary, topics_data["topics"], sentiments,
                            entities=entities, file_names=file_names,
                        )
                        increment_stat("total_reports")
                        log_activity("PDF exported")
                        st.download_button(
                            "⬇️ Download PDF",
                            pdf_bytes,
                            f"NarrativeNexus_{time.strftime('%Y%m%d_%H%M%S')}.pdf",
                            "application/pdf",
                            use_container_width=True,
                        )
                    except Exception as e:
                        st.error(f"PDF error: {e}")

        with rep_col2:
            st.markdown("""
            <div class="nn-card" style="text-align: center; padding: 28px;">
                <div style="font-size: 40px; margin-bottom: 10px;">📋</div>
                <div style="font-weight: 700; color: var(--nn-text); margin-bottom: 4px;">CSV Export</div>
                <div style="color: var(--nn-muted); font-size: 12px; margin-bottom: 16px;">
                    Structured data — sentiment scores, topics & entities
                </div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("📋 Generate CSV", type="primary", use_container_width=True):
                with st.spinner("Generating CSV..."):
                    try:
                        csv_content = generate_csv(topics_data["topics"], sentiments, entities)
                        increment_stat("total_reports")
                        log_activity("CSV exported")
                        st.download_button(
                            "⬇️ Download CSV",
                            csv_content,
                            f"NarrativeNexus_{time.strftime('%Y%m%d_%H%M%S')}.csv",
                            "text/csv",
                            use_container_width=True,
                        )
                    except Exception as e:
                        st.error(f"CSV error: {e}")

        with rep_col3:
            st.markdown("""
            <div class="nn-card" style="text-align: center; padding: 28px;">
                <div style="font-size: 40px; margin-bottom: 10px;">🔧</div>
                <div style="font-weight: 700; color: var(--nn-text); margin-bottom: 4px;">JSON Export</div>
                <div style="color: var(--nn-muted); font-size: 12px; margin-bottom: 16px;">
                    Machine-readable structured data for integrations
                </div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("🔧 Generate JSON", type="primary", use_container_width=True):
                with st.spinner("Generating JSON..."):
                    try:
                        json_content = generate_json_report(
                            summary, topics_data["topics"], sentiments,
                            entities=entities, file_names=file_names,
                        )
                        increment_stat("total_reports")
                        log_activity("JSON exported")
                        st.download_button(
                            "⬇️ Download JSON",
                            json_content,
                            f"NarrativeNexus_{time.strftime('%Y%m%d_%H%M%S')}.json",
                            "application/json",
                            use_container_width=True,
                        )
                    except Exception as e:
                        st.error(f"JSON error: {e}")

        # Report preview
        st.markdown('<div class="nn-divider"></div>', unsafe_allow_html=True)
        st.markdown("#### 📋 Analysis Preview")
        
        prev_tabs = st.tabs(["Summary", "Topics", "Sentiment", "Entities"])
        
        with prev_tabs[0]:
            st.markdown(f"""
            <div class="nn-card">
                <div style="font-size: 14px; line-height: 1.75; color: var(--nn-text);">{summary}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with prev_tabs[1]:
            for i, topic in enumerate(topics_data["topics"]):
                colors = ["#7B2BFF", "#00EAFF", "#FF2BFF", "#FFB830"]
                c = colors[i % len(colors)]
                words = ", ".join(topic)
                st.markdown(f"""
                <div class="nn-card" style="padding: 14px; margin-bottom: 8px; border-left: 3px solid {c};">
                    <strong style="color: {c};">Topic {i+1}:</strong>
                    <span style="color: var(--nn-text); margin-left: 8px;">{words}</span>
                </div>
                """, unsafe_allow_html=True)
        
        with prev_tabs[2]:
            df_sent = pd.DataFrame(sentiments)
            if not df_sent.empty:
                st.dataframe(df_sent.style.background_gradient(subset=["score"]), use_container_width=True)
        
        with prev_tabs[3]:
            if entities:
                df_ents = pd.DataFrame(entities)
                st.dataframe(df_ents, use_container_width=True)
            else:
                st.info("No entities to display.")


# ──────────────────────────────────────────────────────────────────────────────
# PAGE 8: SETTINGS
# ──────────────────────────────────────────────────────────────────────────────
elif page == "Settings":
    st.markdown("""
    <div class="nn-card nn-card-primary">
        <div class="nn-card-title">⚙ Settings</div>
        <div class="nn-card-subtitle">Configure NarrativeNexus AI to your preferences</div>
    </div>
    """, unsafe_allow_html=True)

    settings = st.session_state.settings

    # NLP Settings
    st.markdown('<div class="settings-section"><div class="settings-title">🧠 NLP Configuration</div>', unsafe_allow_html=True)
    col_s1, col_s2 = st.columns(2)
    with col_s1:
        new_topic_count = st.slider(
            "Default Topic Count",
            MIN_TOPICS, MAX_TOPICS,
            settings.get("topic_count", DEFAULT_TOPIC_COUNT),
        )
        settings["topic_count"] = new_topic_count
    with col_s2:
        new_top_k = st.slider(
            "Semantic Search Results",
            1, 10,
            settings.get("semantic_top_k", SEMANTIC_TOP_K),
        )
        settings["semantic_top_k"] = new_top_k
    st.markdown('</div>', unsafe_allow_html=True)

    # Graph Settings
    st.markdown('<div class="settings-section"><div class="settings-title">🌐 Knowledge Graph</div>', unsafe_allow_html=True)
    new_entity_types = st.multiselect(
        "Default Entity Types",
        list(ENTITY_TYPES.keys()),
        default=settings.get("graph_entity_types", ["PERSON", "ORG", "GPE"]),
        help="Select which entity types to include in the knowledge graph",
    )
    settings["graph_entity_types"] = new_entity_types
    st.markdown('</div>', unsafe_allow_html=True)

    # Visualization Settings
    st.markdown('<div class="settings-section"><div class="settings-title">📊 Visualization</div>', unsafe_allow_html=True)
    show_animations = st.checkbox(
        "Enable animations",
        value=settings.get("show_animations", True),
    )
    settings["show_animations"] = show_animations
    st.markdown('</div>', unsafe_allow_html=True)

    # Export Settings
    st.markdown('<div class="settings-section"><div class="settings-title">📑 Export</div>', unsafe_allow_html=True)
    export_format = st.radio(
        "Default export format",
        ["pdf", "csv", "json"],
        index=["pdf", "csv", "json"].index(settings.get("export_format", "pdf")),
        horizontal=True,
    )
    settings["export_format"] = export_format
    st.markdown('</div>', unsafe_allow_html=True)

    # System Info
    st.markdown('<div class="settings-section"><div class="settings-title">ℹ️ System Information</div>', unsafe_allow_html=True)
    sys_col1, sys_col2, sys_col3 = st.columns(3)
    with sys_col1:
        st.metric("App Version", APP_VERSION)
    with sys_col2:
        import platform
        st.metric("Python", platform.python_version())
    with sys_col3:
        import streamlit
        st.metric("Streamlit", streamlit.__version__)
    st.markdown('</div>', unsafe_allow_html=True)

    # Model Health
    if st.button("🔬 Run System Health Check", type="primary"):
        with st.spinner("Checking models..."):
            try:
                from utils.models import check_model_health
                health = check_model_health()
                hcol1, hcol2 = st.columns(2)
                items = list(health.items())
                for i, (model, ok) in enumerate(items):
                    with hcol1 if i % 2 == 0 else hcol2:
                        icon = "✅" if ok else "❌"
                        status = "Available" if ok else "Unavailable"
                        color = "#00FF88" if ok else "#FF4455"
                        st.markdown(f"""
                        <div class="nn-card" style="padding: 14px; margin-bottom: 8px; border-left: 3px solid {color};">
                            <strong>{icon} {model.replace('_', ' ').title()}</strong>
                            <span style="color: {color}; font-size: 12px; float: right;">{status}</span>
                        </div>
                        """, unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Health check failed: {e}")

    # Save
    if st.button("💾 Save Settings", type="primary"):
        st.session_state.settings = settings
        log_activity("Settings saved")
        st.success("✅ Settings saved successfully!")

    # Reset
    if st.button("🔄 Reset All Settings", type="secondary"):
        from utils.state import STATE_DEFAULTS
        import copy
        st.session_state.settings = copy.deepcopy(STATE_DEFAULTS["settings"])
        st.success("Settings reset to defaults.")
        st.rerun()
