# utils/visualization.py
"""
Visualization utilities for NarrativeNexus AI.
Includes word clouds, similarity heatmaps, 3D document space,
topic visualizations, and UI component helpers.
"""
import streamlit as st
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from sklearn.decomposition import PCA
from sklearn.feature_extraction.text import TfidfVectorizer
from utils.config import (
    COLOR_BG, COLOR_PRIMARY, COLOR_SECONDARY,
    COLOR_SURFACE, COLOR_SURFACE_2, COLOR_TEXT, COLOR_MUTED
)


# ── Word Cloud ────────────────────────────────────────────────────────────────
def show_wordcloud(text: str, title: str = "Word Cloud") -> None:
    """Generate and display an enhanced word cloud."""
    if not text or len(text.strip()) < 10:
        st.info("Not enough text to generate word cloud.")
        return
    
    try:
        wordcloud = WordCloud(
            width=1200,
            height=500,
            background_color="#0B0618",
            colormap="cool",
            max_words=150,
            prefer_horizontal=0.9,
            relative_scaling=0.5,
            min_font_size=10,
            max_font_size=80,
            contour_width=0,
        ).generate(text)
        
        fig, ax = plt.subplots(figsize=(14, 6))
        ax.imshow(wordcloud, interpolation="bilinear")
        ax.axis("off")
        fig.patch.set_facecolor("#0B0618")
        ax.set_facecolor("#0B0618")
        plt.tight_layout(pad=0)
        st.pyplot(fig)
        plt.close(fig)
    except Exception as e:
        st.error(f"Word cloud error: {e}")


# ── Similarity Heatmap ────────────────────────────────────────────────────────
def plot_similarity_heatmap(df: pd.DataFrame) -> None:
    """Plot a styled document similarity heatmap."""
    if df.empty:
        st.info("No similarity data to display.")
        return
    
    fig = px.imshow(
        df,
        labels=dict(x="Document", y="Document", color="Similarity"),
        x=df.columns,
        y=df.columns,
        color_continuous_scale=[
            [0, "#0B0618"],
            [0.3, "#12082A"],
            [0.6, "#7B2BFF"],
            [0.8, "#00EAFF"],
            [1.0, "#ffffff"],
        ],
        text_auto=".2f",
        zmin=0,
        zmax=1,
        aspect="auto",
    )
    
    fig.update_traces(
        textfont=dict(size=12, color="white"),
        hovertemplate="<b>%{x}</b> vs <b>%{y}</b><br>Similarity: %{z:.3f}<extra></extra>",
    )
    
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color=COLOR_TEXT, family="Inter"),
        coloraxis_colorbar=dict(
            title="Similarity",
            tickfont=dict(color=COLOR_TEXT),
            titlefont=dict(color=COLOR_TEXT),
            bgcolor="rgba(18,8,42,0.8)",
            bordercolor=COLOR_PRIMARY,
            borderwidth=1,
        ),
        margin=dict(l=10, r=10, t=20, b=10),
        height=400,
    )
    st.plotly_chart(fig, use_container_width=True)


# ── 3D Document Space ─────────────────────────────────────────────────────────
def plot_3d_document_space(docs: list, labels: list = None) -> None:
    """
    Plot documents in 3D vector space using PCA reduction.
    Shows semantic proximity between documents.
    """
    if len(docs) < 2:
        st.info("ℹ️ Upload at least 2 documents to see the Document Space.")
        return
    
    tfidf = TfidfVectorizer(stop_words="english", max_features=1000)
    
    try:
        matrix = tfidf.fit_transform(docs)
    except ValueError:
        st.warning("Documents appear to be empty or contain only stopwords.")
        return
    
    # PCA reduction
    n_components = min(3, len(docs) - 1, matrix.shape[1])
    if n_components < 2:
        st.info("Not enough distinct content for 3D visualization.")
        return
    
    pca = PCA(n_components=n_components, random_state=42)
    
    try:
        coords = pca.fit_transform(matrix.toarray())
    except Exception:
        coords = np.random.rand(len(docs), 3)
    
    # Pad to 3D if needed
    while coords.shape[1] < 3:
        coords = np.hstack([coords, np.zeros((len(docs), 1))])
    
    # Add small jitter to separate overlapping points
    coords += np.random.normal(0, 0.02, coords.shape)
    
    doc_labels = labels or [f"Doc {i+1}" for i in range(len(docs))]
    snippets = [d[:120].replace("\n", " ") + "..." for d in docs]
    
    # Color gradient based on position
    colors = [f"hsl({int(240 + i * (120 / max(len(docs), 1)))}, 80%, 60%)" for i in range(len(docs))]
    
    df = pd.DataFrame({
        "x": coords[:, 0],
        "y": coords[:, 1],
        "z": coords[:, 2],
        "Document": doc_labels,
        "Snippet": snippets,
    })
    
    explained = pca.explained_variance_ratio_ if hasattr(pca, "explained_variance_ratio_") else [0, 0, 0]
    
    fig = px.scatter_3d(
        df,
        x="x", y="y", z="z",
        color="Document",
        hover_data={"Snippet": True, "x": False, "y": False, "z": False},
        opacity=0.95,
    )
    
    fig.update_traces(
        marker=dict(
            size=12,
            line=dict(width=2, color="rgba(255,255,255,0.8)"),
            symbol="circle",
        ),
        hovertemplate="<b>%{customdata[0]}</b><br>%{customdata[1]}<extra></extra>",
    )
    
    fig.update_layout(
        title=dict(
            text=f"3D Document Vector Space  (Variance explained: {sum(explained[:3])*100:.1f}%)",
            font=dict(color=COLOR_TEXT, size=14),
            x=0.5,
        ),
        scene=dict(
            xaxis=dict(backgroundcolor="#0B0618", gridcolor="#2D1B6E", showbackground=True,
                       title="PC1", titlefont=dict(color=COLOR_MUTED), tickfont=dict(color=COLOR_MUTED)),
            yaxis=dict(backgroundcolor="#0B0618", gridcolor="#2D1B6E", showbackground=True,
                       title="PC2", titlefont=dict(color=COLOR_MUTED), tickfont=dict(color=COLOR_MUTED)),
            zaxis=dict(backgroundcolor="#0B0618", gridcolor="#2D1B6E", showbackground=True,
                       title="PC3", titlefont=dict(color=COLOR_MUTED), tickfont=dict(color=COLOR_MUTED)),
            bgcolor="#0B0618",
        ),
        paper_bgcolor="#12082A",
        font=dict(color=COLOR_TEXT, family="Inter"),
        margin=dict(l=0, r=0, b=0, t=50),
        height=580,
        legend=dict(
            bgcolor="rgba(18,8,42,0.8)",
            bordercolor=COLOR_PRIMARY,
            borderwidth=1,
            font=dict(color=COLOR_TEXT),
        ),
    )
    
    st.plotly_chart(fig, use_container_width=True)


# ── Sentiment Bar Chart ───────────────────────────────────────────────────────
def plot_sentiment_chart(sentiments: list) -> None:
    """Plot enhanced sentiment analysis chart."""
    if not sentiments:
        return
    
    labels = [s["label"] for s in sentiments]
    scores = [s["score"] for s in sentiments]
    docs = [f"Doc {i+1}" for i in range(len(sentiments))]
    
    colors_map = {"POSITIVE": "#00FF88", "NEGATIVE": "#FF4455", "NEUTRAL": "#FFB830", "UNKNOWN": "#8B8BA0"}
    bar_colors = [colors_map.get(l, "#8B8BA0") for l in labels]
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=docs,
        y=scores,
        marker=dict(
            color=bar_colors,
            line=dict(color="rgba(255,255,255,0.2)", width=1),
            opacity=0.9,
        ),
        text=[f"{l}<br>{s:.1%}" for l, s in zip(labels, scores)],
        textposition="outside",
        textfont=dict(color=COLOR_TEXT, size=11),
        hovertemplate="<b>%{x}</b><br>Sentiment: %{text}<extra></extra>",
    ))
    
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color=COLOR_TEXT, family="Inter"),
        xaxis=dict(gridcolor="rgba(255,255,255,0.05)", title="Document"),
        yaxis=dict(gridcolor="rgba(255,255,255,0.05)", title="Confidence", tickformat=".0%"),
        margin=dict(l=10, r=10, t=20, b=10),
        height=350,
        showlegend=False,
    )
    
    st.plotly_chart(fig, use_container_width=True)


# ── Topic Radar Chart ─────────────────────────────────────────────────────────
def plot_topic_radar(topics: list) -> None:
    """Plot topic importance as a radar/polar chart."""
    if not topics:
        return
    
    topic_labels = [f"Topic {i+1}" for i in range(len(topics))]
    # Use number of unique words as a proxy for topic richness
    values = [len(set(t)) for t in topics]
    values_normalized = [v / max(values) if max(values) > 0 else 0 for v in values]
    
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=values_normalized + values_normalized[:1],
        theta=topic_labels + topic_labels[:1],
        fill="toself",
        fillcolor="rgba(123,43,255,0.2)",
        line=dict(color=COLOR_PRIMARY, width=2),
        marker=dict(color=COLOR_SECONDARY, size=8),
    ))
    
    fig.update_layout(
        polar=dict(
            bgcolor="rgba(18,8,42,0.6)",
            radialaxis=dict(visible=True, gridcolor="rgba(255,255,255,0.1)",
                           tickfont=dict(color=COLOR_MUTED), linecolor="rgba(255,255,255,0.1)"),
            angularaxis=dict(gridcolor="rgba(255,255,255,0.1)",
                            tickfont=dict(color=COLOR_TEXT)),
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color=COLOR_TEXT, family="Inter"),
        margin=dict(l=30, r=30, t=30, b=30),
        height=350,
        showlegend=False,
    )
    
    st.plotly_chart(fig, use_container_width=True)


# ── UI Components ─────────────────────────────────────────────────────────────
def show_card(title: str, subtitle: str, content: str) -> None:
    """Render a glassmorphism card."""
    st.markdown(
        f"""
        <div class="nn-card">
            <div class="nn-card-title">{title}</div>
            <div class="nn-card-subtitle">{subtitle}</div>
            <div class="nn-card-content">{content}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def show_kpi_card(value: str, label: str, icon: str, color: str = "#7B2BFF") -> None:
    """Render a KPI metric card."""
    st.markdown(
        f"""
        <div class="kpi-card" style="border-top: 3px solid {color};">
            <div class="kpi-icon">{icon}</div>
            <div class="kpi-value" style="color: {color};">{value}</div>
            <div class="kpi-label">{label}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def show_skeleton_loader(height: int = 120) -> None:
    """Display a loading skeleton placeholder."""
    st.markdown(
        f"""
        <div class="skeleton" style="height: {height}px; border-radius: 12px; margin-bottom: 16px;">
        </div>
        """,
        unsafe_allow_html=True,
    )


def show_badge(text: str, color: str = "#7B2BFF") -> str:
    """Return badge HTML."""
    return f'<span class="nn-badge" style="background: {color}20; border: 1px solid {color}; color: {color};">{text}</span>'


def show_step_progress(steps: list, current: int) -> None:
    """Show AI workflow progress steps."""
    steps_html = ""
    for i, step in enumerate(steps):
        if i < current:
            icon = "✓"
            cls = "step-done"
        elif i == current:
            icon = "⟳"
            cls = "step-active"
        else:
            icon = "○"
            cls = "step-pending"
        steps_html += f'<div class="workflow-step {cls}"><span class="step-icon">{icon}</span> {step}</div>'
    
    st.markdown(f'<div class="workflow-container">{steps_html}</div>', unsafe_allow_html=True)
