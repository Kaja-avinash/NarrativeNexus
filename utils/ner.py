import spacy
from spacy import displacy
import streamlit as st


# Load model (cached to prevent reloading)
@st.cache_resource
def load_spacy_model():
    return spacy.load("en_core_web_sm")


nlp = load_spacy_model()


def highlight_entities(text):
    """
    Returns HTML with highlighted entities (ORG, PERSON, GPE, etc.)
    """
    # Spacy has a limit of 1,000,000 characters. We truncate if needed.
    if len(text) > 1000000:
        text = text[:1000000]

    doc = nlp(text)

    # Generate HTML using Spacy's built-in visualizer
    html = displacy.render(doc, style="ent", page=True)
    return html
