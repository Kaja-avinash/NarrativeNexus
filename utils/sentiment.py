import streamlit as st
from transformers import pipeline


# CACHING: Load the model only once
@st.cache_resource
def load_sentiment_model():
    return pipeline("sentiment-analysis")


def get_sentiment(text):
    # Load cached model
    sentiment_model = load_sentiment_model()

    # Truncate to 512 tokens to prevent BERT crashes
    out = sentiment_model(text[:512])[0]
    return {"label": out["label"], "score": float(out["score"])}
