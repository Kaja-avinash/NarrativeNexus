import streamlit as st
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import plotly.express as px
import pandas as pd
import numpy as np
from sklearn.decomposition import PCA
from sklearn.feature_extraction.text import TfidfVectorizer


def show_wordcloud(text):
    if not text:
        return

    # Generate Word Cloud
    try:
        wordcloud = WordCloud(
            width=800,
            height=400,
            background_color="#1c0b2c",
            colormap="cool",
            max_words=100,
        ).generate(text)

        # Display using Matplotlib
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.imshow(wordcloud, interpolation="bilinear")
        ax.axis("off")
        fig.patch.set_alpha(0)
        st.pyplot(fig)
    except Exception as e:
        st.error(f"Could not generate word cloud: {e}")


def plot_similarity_heatmap(df):
    if df.empty:
        return

    fig = px.imshow(
        df,
        labels=dict(x="Document", y="Document", color="Similarity"),
        x=df.columns,
        y=df.columns,
        color_continuous_scale="Viridis",
        text_auto=".2f",
    )

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font_color="white"
    )
    st.plotly_chart(fig, use_container_width=True)


def show_card(title, subtitle, content):
    st.markdown(
        f"""
    <div class="glass-card">
        <h4 style="color: #00eaff; margin-bottom: 5px;">{title}</h4>
        <div class="small-muted" style="margin-bottom: 10px;">{subtitle}</div>
        <div style="font-size: 0.95em; line-height: 1.5;">{content}</div>
    </div>
    """,
        unsafe_allow_html=True,
    )


def plot_3d_document_space(docs):
    """
    Robust 3D Plotting with Jitter and High-Contrast visibility.
    """
    if len(docs) < 3:
        st.info("ℹ️ Upload at least 3 documents to see the 3D Cluster Map.")
        return

    # 1. Vectorize
    tfidf = TfidfVectorizer(stop_words="english")
    try:
        matrix = tfidf.fit_transform(docs)
    except ValueError:
        st.warning("Documents likely empty or only contain stop words.")
        return

    # 2. PCA Reduction
    # We need at least 3 samples to span 3D space comfortably
    n_components = 3
    pca = PCA(n_components=n_components)

    # Padding logic: If we have < 3 features/samples, PCA might output fewer columns
    try:
        coords = pca.fit_transform(matrix.toarray())
    except Exception:
        # Fallback for edge cases
        coords = np.random.rand(len(docs), 3)

    # 3. JITTER: Add tiny noise to separate overlapping points
    # This ensures points don't stack on top of each other perfectly
    noise = np.random.normal(0, 0.05, coords.shape)
    if coords.shape[1] == 3:
        coords = coords + noise

    # 4. Prepare DataFrame
    data = {}
    # Safely handle cases where PCA returns fewer than 3 dims
    cols = coords.shape[1]
    data["x"] = coords[:, 0]
    data["y"] = coords[:, 1] if cols > 1 else np.zeros(len(docs))
    data["z"] = coords[:, 2] if cols > 2 else np.zeros(len(docs))

    df = pd.DataFrame(data)
    df["Document"] = [f"Doc {i + 1}" for i in range(len(docs))]
    # Truncate snippets for cleaner hover tooltips
    df["Snippet"] = [d[:100] + "..." for d in docs]

    # 5. Plot
    fig = px.scatter_3d(
        df,
        x="x",
        y="y",
        z="z",
        color="Document",
        hover_data=["Snippet"],
        opacity=1.0,  # Max opacity
        size_max=20,  # Larger dots
    )

    # 6. High-Contrast Styling
    fig.update_traces(
        marker=dict(size=15, line=dict(width=2, color="white"))
    )  # White outline makes them pop

    fig.update_layout(
        title="3D Document Cluster Map",
        scene=dict(
            # Brighter grid lines (#555 instead of #333) so the box is visible
            xaxis=dict(
                backgroundcolor="#0e0416",
                gridcolor="#555",
                showbackground=True,
                title="",
            ),
            yaxis=dict(
                backgroundcolor="#0e0416",
                gridcolor="#555",
                showbackground=True,
                title="",
            ),
            zaxis=dict(
                backgroundcolor="#0e0416",
                gridcolor="#555",
                showbackground=True,
                title="",
            ),
            bgcolor="#0e0416",
        ),
        paper_bgcolor="#1c0b2c",
        font_color="white",
        margin=dict(l=0, r=0, b=0, t=40),
        height=600,
        legend=dict(yanchor="top", y=0.9, xanchor="left", x=0.1),
    )

    st.plotly_chart(fig, use_container_width=True)
