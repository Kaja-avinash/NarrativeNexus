import time
from pathlib import Path
import streamlit as st
import requests  # Needed for Lottie Animations
from streamlit_lottie import st_lottie  # Lottie Component

# ------------------ ⚠️ CRITICAL CONFIG MUST BE FIRST ⚠️ ------------------
st.set_page_config(page_title="NarrativeNexus Pro", layout="wide", page_icon="🧠")
# ------------------------------------------------------------------------

import pandas as pd
import streamlit.components.v1 as components

# --- Import Utils ---
from utils.file_utils import read_file
from utils.preprocessing import preprocess_text
from utils.topic_modeling import extract_topics, generate_pyldavis
from utils.summarizer import summarize
from utils.sentiment import get_sentiment
from utils.visualization import show_wordcloud, plot_similarity_heatmap, show_card
from utils.cosine_sim import compute_cosine_similarity
from utils.semantic_search import build_index, query
from utils.language import detect_language
from utils.translate import translate_to_english
from utils.report import generate_pdf
from utils.ner import highlight_entities
from utils.graph import generate_knowledge_graph
from utils.visualization import plot_3d_document_space


# ------------------ ANIMATION FUNCTIONS ------------------
def load_lottieurl(url: str):
    """Loads Lottie animation from a URL."""
    try:
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()
    except:
        return None


def typewriter_effect(text: str, speed: float = 0.01):
    """Generator function for the typewriter effect."""
    for word in text.split():
        yield word + " "
        time.sleep(speed)


# Load Assets
lottie_brain = load_lottieurl(
    "https://lottie.host/014c53c4-e698-4f51-b855-385036152b1b/zZ4aO6J2F8.json"
)
lottie_loading = load_lottieurl(
    "https://lottie.host/e2b604b3-d65d-424a-b50a-86717a6d8923/8H9y6Z55qj.json"
)

# ------------------ ULTRA-DYNAMIC 3D & SPECTRUM UI ENGINE ------------------
st.markdown(
    """
    <style>
    /* --- 1. THE DEEP NEBULA BACKGROUND --- */
    .stApp {
        background: linear-gradient(-45deg, #0f0c29, #302b63, #24243e);
        background-size: 400% 400%;
        animation: nebulaMove 15s ease infinite;
        overflow-x: hidden;
    }
    @keyframes nebulaMove {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    /* --- 2. SIDEBAR STYLING (NEW) --- */
    [data-testid="stSidebar"] {
        background-color: #0f0c29;
        background-image: linear-gradient(180deg, #0f0c29 0%, #1a1a40 100%);
        border-right: 1px solid rgba(162, 0, 255, 0.3); /* Neon Purple Border */
        box-shadow: 5px 0 15px rgba(0,0,0,0.3);
    }
    
    /* Navigation Radio Buttons - TRANSFORM INTO CARDS */
    .stRadio > div[role="radiogroup"] > label {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(162, 0, 255, 0.2);
        border-radius: 10px;
        padding: 12px 15px;
        margin-bottom: 8px;
        transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
        cursor: pointer;
    }
    
    /* Hover Effect for Nav Items */
    .stRadio > div[role="radiogroup"] > label:hover {
        background: rgba(162, 0, 255, 0.15);
        border-color: #00eaff; /* Cyan Glow on Hover */
        transform: translateX(8px); /* Slide to the right */
        box-shadow: 0 0 15px rgba(0, 234, 255, 0.2);
    }
    
    /* Text inside Nav Items */
    .stRadio > div[role="radiogroup"] > label p {
        font-family: 'Orbitron', sans-serif !important;
        font-size: 16px !important;
        color: #e0e0e0 !important;
        font-weight: 500;
        margin: 0;
    }

    /* Sidebar Titles */
    [data-testid="stSidebar"] h1, 
    [data-testid="stSidebar"] h2, 
    [data-testid="stSidebar"] h3 {
        font-family: 'Orbitron', sans-serif !important;
        color: #00eaff !important; /* Cyan Title */
        text-transform: uppercase;
        letter-spacing: 2px;
        text-shadow: 0 0 10px rgba(0, 234, 255, 0.5);
    }

    /* --- 3. THE 3D MOVING PARTICLES (Background Layer) --- */
    .circles {
        position: fixed;
        top: 0; left: 0; width: 100%; height: 100%;
        overflow: hidden;
        z-index: 0;
        pointer-events: none;
    }
    .circles li {
        position: absolute;
        display: block;
        list-style: none;
        width: 20px; height: 20px;
        background: rgba(255, 255, 255, 0.1);
        animation: animate 25s linear infinite;
        bottom: -150px;
        border-radius: 4px; /* Cube shape */
        box-shadow: 0 0 10px rgba(0, 255, 255, 0.5);
    }
    .circles li:nth-child(1){ left: 25%; width: 80px; height: 80px; animation-delay: 0s; }
    .circles li:nth-child(2){ left: 10%; width: 20px; height: 20px; animation-delay: 2s; animation-duration: 12s; }
    .circles li:nth-child(3){ left: 70%; width: 20px; height: 20px; animation-delay: 4s; }
    .circles li:nth-child(4){ left: 40%; width: 60px; height: 60px; animation-delay: 0s; animation-duration: 18s; }
    .circles li:nth-child(5){ left: 65%; width: 20px; height: 20px; animation-delay: 0s; }
    .circles li:nth-child(6){ left: 75%; width: 110px; height: 110px; animation-delay: 3s; }
    .circles li:nth-child(7){ left: 35%; width: 150px; height: 150px; animation-delay: 7s; }
    .circles li:nth-child(8){ left: 50%; width: 25px; height: 25px; animation-delay: 15s; animation-duration: 45s; }
    .circles li:nth-child(9){ left: 20%; width: 15px; height: 15px; animation-delay: 2s; animation-duration: 35s; }
    .circles li:nth-child(10){ left: 85%; width: 150px; height: 150px; animation-delay: 0s; animation-duration: 11s; }

    @keyframes animate {
        0%{ transform: translateY(0) rotate(0deg); opacity: 1; border-radius: 0; }
        100%{ transform: translateY(-1000px) rotate(720deg); opacity: 0; border-radius: 50%; }
    }

    /* --- 4. SPECTRUM TITLE (Rainbow Gradient) --- */
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@900&display=swap');
    
    @keyframes floatTitle {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-8px); }
    }
    
    .neon-title {
        font-family: 'Orbitron', sans-serif;
        text-align: center;
        font-size: 70px;
        font-weight: 900;
        background: linear-gradient(to right, #ff00cc, #3333ff, #00ccff, #00ff99);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0 0 40px rgba(255, 0, 204, 0.4);
        letter-spacing: 6px;
        margin-top: 10px;
        margin-bottom: 5px;
        animation: floatTitle 4s ease-in-out infinite;
        position: relative; z-index: 1;
    }

    .neon-subtitle {
        font-family: 'Orbitron', sans-serif;
        text-align: center;
        font-size: 18px;
        color: #00eaff;
        letter-spacing: 5px;
        text-transform: uppercase;
        margin-bottom: 40px;
        text-shadow: 0 0 15px rgba(0, 234, 255, 0.6);
        position: relative; z-index: 1;
    }

    /* --- 5. HOLOGRAPHIC CARDS --- */
    .glass-card {
        position: relative;
        background: rgba(18, 4, 40, 0.6);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 2px solid transparent;
        background-clip: padding-box;
        border-radius: 15px;
        padding: 25px;
        margin-bottom: 25px;
        color: white;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        z-index: 1;
    }
    
    /* Rainbow Border on Hover */
    .glass-card::after {
        content: "";
        position: absolute;
        top: -2px; bottom: -2px; left: -2px; right: -2px;
        background: linear-gradient(45deg, #ff00cc, #3333ff, #00ccff);
        z-index: -1;
        border-radius: 16px;
        opacity: 0.5;
    }
    .glass-card:hover {
        transform: translateY(-8px) scale(1.01);
        box-shadow: 0 20px 50px rgba(0,0,0,0.6), 0 0 30px rgba(255, 0, 204, 0.4);
    }
    .glass-card:hover::after { opacity: 1; }

    /* --- 6. BUTTONS & TABS --- */
    .stButton button {
        background: linear-gradient(90deg, #6a11cb 0%, #2575fc 100%);
        border: none;
        color: white;
        padding: 12px 28px;
        font-family: 'Orbitron', sans-serif;
        font-weight: bold;
        border-radius: 8px;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(106, 17, 203, 0.4);
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    .stButton button:hover {
        background: linear-gradient(90deg, #ff00cc 0%, #3333ff 100%);
        transform: translateY(-3px);
        box-shadow: 0 0 25px rgba(255, 0, 204, 0.6);
    }

    .stTabs [data-baseweb="tab"] {
        background-color: rgba(255,255,255,0.05);
        border-radius: 8px;
        color: #bbb;
        border: 1px solid rgba(255,255,255,0.1);
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #ff00cc, #333399);
        color: white;
        border: none;
        box-shadow: 0 0 15px rgba(255, 0, 204, 0.5);
    }
    
    .small-muted { color: #a0a0a0; font-size: 0.85em; margin-top: 5px; }

    /* FIX: Force Header Text to be White & Glowing */
    h3 {
        font-family: 'Orbitron', sans-serif;
        color: #ffffff !important;
        text-shadow: 0 0 10px rgba(0, 234, 255, 0.8);
        margin-top: 0;
        text-transform: uppercase;
        letter-spacing: 1px;
        background: none !important;
        -webkit-text-fill-color: white !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ------------------ INJECT PARTICLES (Hidden HTML) ------------------
st.markdown(
    """
    <ul class="circles">
        <li></li><li></li><li></li><li></li><li></li>
        <li></li><li></li><li></li><li></li><li></li>
    </ul>
    """,
    unsafe_allow_html=True,
)

# ------------------ SESSION STATE ------------------
session_defaults = {
    "raw_docs": [],
    "cleaned_docs": [],
    "summary": "",
    "topics_data": None,
    "sentiments": [],
    "history": [],
    "ner_html": "",
    "graph_html": "",
}

for key, val in session_defaults.items():
    if key not in st.session_state:
        st.session_state[key] = val

# ------------------ SIDEBAR WITH ANIMATION ------------------
with st.sidebar:
    # 🧠 THE BRAIN ANIMATION
    if lottie_brain:
        st_lottie(lottie_brain, height=200, key="brain")
    else:
        st.image("https://img.icons8.com/nolan/200/brain.png")  # Fallback

    # Styled Radio Button Navigation
    page = st.radio(
        "SYSTEM NAVIGATION",  # All caps for Sci-Fi look
        [
            "Upload",
            "Results Dashboard",
            "Semantic Search",
            "History",
        ],
    )

# ------------------ HEADER ------------------
st.markdown(
    """
    <div class="neon-title">NARRATIVENEXUS</div>
    <div class="neon-subtitle">DYNAMIC TEXT ANALYSIS PLATFORM</div>
    """,
    unsafe_allow_html=True,
)

# ----------------- Upload Directory ----------------
UPLOAD_DIR = Path("uploaded_files")
UPLOAD_DIR.mkdir(exist_ok=True)


def save_uploaded_file(uploaded_file):
    dest = UPLOAD_DIR / uploaded_file.name
    with open(dest, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return str(dest.resolve())


def clear_current_session():
    for key in session_defaults.keys():
        if isinstance(session_defaults[key], list):
            st.session_state[key] = []
        else:
            st.session_state[key] = session_defaults[key]


# ------------------ UPLOAD PAGE ------------------
if page == "Upload":
    # UPDATED: Slimmer Size + VIBRANT GRADIENT BACKGROUND
    st.markdown(
        """
        <div class='glass-card' style='
            text-align: center; 
            padding: 15px; 
            background: linear-gradient(90deg, #a200ff 0%, #00eaff 100%);
            border: none;
            box-shadow: 0 5px 15px rgba(162, 0, 255, 0.4);
        '>
            <h2 style='
                font-family: "Orbitron", sans-serif; 
                font-size: 28px; 
                font-weight: 700; 
                margin: 0; 
                color: #ffffff; 
                text-shadow: 0 2px 4px rgba(0,0,0,0.3);
                text-transform: uppercase;
                letter-spacing: 2px;
                line-height: 1.2;
            '>
                Dynamic Text Analysis
            </h2>
            <div style='
                color: rgba(255, 255, 255, 0.9); 
                font-size: 12px; 
                margin-top: 5px; 
                font-family: "Poppins", sans-serif;
                font-weight: 500;
            '>
                System accepts: PDF, DOCX, TXT, PPTX, CSV, Images (OCR), EPUB, RTF, HTML
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    files = st.file_uploader(
        "Initiate File Stream:",
        type=[
            "txt",
            "pdf",
            "docx",
            "doc",
            "csv",
            "xlsx",
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
        ],
        accept_multiple_files=True,
    )
    pasted_text = st.text_area(
        "Or Input Raw Data Stream (--- to separate):", height=150
    )
    topic_count = st.slider("Clustering Granularity (LDA)", 2, 8, 4)

    col1, col2 = st.columns([1, 1])

    # ... rest of the upload logic remains the same ...
    with col1:
        if st.button("🚀 EXECUTE ANALYSIS", type="primary"):
            docs = []
            saved_paths = []
            if files:
                for f in files:
                    try:
                        save_uploaded_file(f)
                        saved_paths.append(f.name)
                        content = read_file(f)
                        docs.append(content)
                    except Exception as e:
                        st.error(f"Error reading {f.name}: {e}")
            if pasted_text.strip():
                parts = [p.strip() for p in pasted_text.split("---") if p.strip()]
                docs.extend(parts)
                saved_paths.extend(["Pasted Text"] * len(parts))

            if not docs:
                st.warning("Please upload at least one document.")
            else:
                # 🎞️ SHOW LOADING ANIMATION WHILE PROCESSING
                with st.status("Initializing AI Subsystems...", expanded=True):
                    if lottie_loading:
                        st_lottie(lottie_loading, height=150, key="loading")

                    # SPEED OPTIMIZATION: Disabled translation
                    final_docs = docs

                    st.write("🧹 Normalizing Vector Space...")
                    cleaned = [preprocess_text(d) for d in final_docs]
                    full_text = " ".join(final_docs)
                    st.write("🤖 Engaging Neural Summarizers...")
                    summary = summarize(full_text)
                    sentiments = [get_sentiment(d) for d in final_docs]
                    st.write("💭 Mapping Latent Topics...")
                    topics = extract_topics(cleaned, n_topics=topic_count)
                    st.write("🕸️ Constructing Knowledge Graph...")
                    ner_html = highlight_entities(full_text[:5000])
                    graph_html = generate_knowledge_graph(full_text)

                    st.session_state.raw_docs = final_docs
                    st.session_state.cleaned_docs = cleaned
                    st.session_state.summary = summary
                    st.session_state.topics_data = topics
                    st.session_state.sentiments = sentiments
                    st.session_state.ner_html = ner_html
                    st.session_state.graph_html = graph_html

                    pdf_bytes = generate_pdf(summary, topics["topics"], sentiments)
                    st.session_state.history.append(
                        {
                            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                            "summary": summary,
                            "topics": topics["topics"],
                            "sentiments": sentiments,
                            "pdf": pdf_bytes,
                            "file_paths": saved_paths,
                        }
                    )
                st.success("Analysis Complete! Proceed to the **Results Dashboard**.")

    with col2:
        if st.button("TERMINATE SESSION"):
            clear_current_session()
            st.success("Session Purged.")
            st.rerun()

# ------------------ RESULTS DASHBOARD ------------------
elif page == "Results Dashboard":
    if not st.session_state.cleaned_docs:
        st.info("⚠️ Awaiting Data Input.")
    else:
        # MERGED TABS (Includes 3D Map)
        tabs = st.tabs(
            [
                "📋 Summary",
                "🕸️ Knowledge Graph",
                "🌌 3D Map",
                "🏷️ Entities (NER)",
                "😊 Sentiment",
                "💭 Topics (LDA)",
                "☁️ Word Cloud",
                "📐 Similarity",
                "📥 Export",
            ]
        )

        # 1. Summary WITH TYPEWRITER EFFECT
        with tabs[0]:
            st.markdown(
                "<div class='glass-card'><h3>Executive Summary</h3></div>",
                unsafe_allow_html=True,
            )
            # ⌨️ TYPEWRITER EFFECT HERE
            if st.session_state.summary:
                st.write_stream(typewriter_effect(st.session_state.summary))
            else:
                st.write("No summary available.")

            st.markdown(
                "<div class='glass-card'><h3>Data Stream Previews</h3></div>",
                unsafe_allow_html=True,
            )
            for i, d in enumerate(st.session_state.raw_docs):
                show_card(
                    f"Document {i + 1}", f"{len(d.split())} words", d[:300] + "..."
                )

        # 2. Knowledge Graph
        with tabs[1]:
            st.markdown(
                "<div class='glass-card'><h3>Entity Neural Network (Knowledge Graph)</h3></div>",
                unsafe_allow_html=True,
            )
            st.caption(
                "Visualizing relationships between People, Organizations, and Locations."
            )
            if st.session_state.graph_html:
                components.html(st.session_state.graph_html, height=600, scrolling=True)
            else:
                st.info("Insufficient entity density for graph construction.")

        # 3. 3D Map (UPDATED)
        with tabs[2]:
            st.markdown(
                "<div class='glass-card'><h3>3D Document Universe</h3></div>",
                unsafe_allow_html=True,
            )
            st.caption("Interactive 3D vector space. Double-click to reset view.")
            plot_3d_document_space(st.session_state.cleaned_docs)

        # 4. NER (FIXED: Using components.html)
        with tabs[3]:
            st.markdown(
                "<div class='glass-card'><h3>Named Entity Recognition</h3></div>",
                unsafe_allow_html=True,
            )
            st.caption("Highlighting key entities in the text.")
            if st.session_state.ner_html:
                components.html(st.session_state.ner_html, height=500, scrolling=True)
            else:
                st.info("No entities detected.")

        # 5. Sentiment
        with tabs[4]:
            st.markdown("### Sentiment Metrics")
            col1, col2 = st.columns([2, 1])
            with col1:
                df_sent = pd.DataFrame(st.session_state.sentiments)
                st.bar_chart(df_sent["score"])
            with col2:
                for i, s in enumerate(st.session_state.sentiments):
                    show_card(f"Doc {i + 1}", s["label"], f"{s['score']:.2f}")

        # 6. Topics
        with tabs[5]:
            st.subheader("LDA Topic Modeling")
            topics = st.session_state.topics_data["topics"]
            for i, t in enumerate(topics):
                st.markdown(f"**Topic {i + 1}:** {', '.join(t)}")

            if st.button("Generate Interactive Map"):
                html = generate_pyldavis(
                    st.session_state.topics_data["lda"],
                    st.session_state.topics_data["corpus"],
                    st.session_state.topics_data["dictionary"],
                )
                components.html(html, height=800, scrolling=True)

        # 7. Word Cloud & Keywords
        with tabs[6]:
            show_wordcloud(" ".join(st.session_state.cleaned_docs))
            st.markdown("---")
            from collections import Counter

            words = " ".join(st.session_state.cleaned_docs).split()
            freq = Counter(words).most_common(20)
            st.table(pd.DataFrame(freq, columns=["Keyword", "Count"]))

        # 8. Similarity
        with tabs[7]:
            df_sim, highest = compute_cosine_similarity(st.session_state.cleaned_docs)
            plot_similarity_heatmap(df_sim)
            st.info(f"Highest Correlation: {highest['pair']} ({highest['score']:.2f})")

        # 9. Export
        with tabs[8]:
            st.subheader("Export Report")
            pdf = generate_pdf(
                st.session_state.summary,
                st.session_state.topics_data["topics"],
                st.session_state.sentiments,
            )
            st.download_button(
                "Download Mission Report", pdf, "NarrativeNexus_Report.pdf"
            )

# ------------------ SEMANTIC SEARCH TAB ------------------
elif page == "Semantic Search":
    st.header("🔍 Neural Search")
    if not st.session_state.raw_docs:
        st.info("Upload documents first.")
    else:
        if st.button("Index Documents"):
            build_index(st.session_state.raw_docs)
            st.success("Index ready.")

        q = st.text_area("Query the Knowledge Base:")
        if st.button("Execute Search"):
            results = query(q)
            for r in results:
                show_card(
                    f"Confidence: {r['score']:.2f}",
                    "Match Segment",
                    r["doc"][:300] + "...",
                )

# ------------------ HISTORY ------------------
elif page == "History":
    st.header("🗂 Mission Logs")
    if not st.session_state.history:
        st.info("No past logs recorded.")
    else:
        for idx, rec in enumerate(reversed(st.session_state.history), 1):
            with st.expander(f"Log #{idx} — {rec['timestamp']}"):
                st.write("**Summary:** " + rec["summary"][:300] + "...")
                st.write(
                    "**Files:** " + ", ".join([str(p) for p in rec["file_paths"] if p])
                )
                if rec["pdf"]:
                    st.download_button(
                        "Download PDF", rec["pdf"], f"Analysis_{rec['timestamp']}.pdf"
                    )
