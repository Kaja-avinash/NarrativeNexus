# utils/ner.py
"""
Named Entity Recognition using spaCy.
Uses centralized model loader to prevent duplicate loading.
"""
import spacy
from spacy import displacy
import streamlit as st
from utils.models import load_spacy
from utils.config import MAX_NER_CHARS


def highlight_entities(text: str) -> str:
    """
    Returns HTML with highlighted entities (ORG, PERSON, GPE, etc.)
    Uses displacy for rendering. Truncates to MAX_NER_CHARS for performance.
    """
    if not text or not text.strip():
        return "<div>No text provided for entity recognition.</div>"
    
    nlp = load_spacy()
    if nlp is None:
        return "<div>⚠️ NER model not available.</div>"
    
    # Truncate to limit
    if len(text) > MAX_NER_CHARS:
        text = text[:MAX_NER_CHARS]
    
    try:
        doc = nlp(text)
        
        # Custom colors matching design system
        colors = {
            "PERSON": "#FF6B9D",
            "ORG": "#00EAFF",
            "GPE": "#7B2BFF",
            "DATE": "#FFB830",
            "MONEY": "#00FF88",
            "PRODUCT": "#FF9F43",
            "EVENT": "#EE5A24",
            "NORP": "#A29BFE",
            "LOC": "#74B9FF",
            "FACILITY": "#FD79A8",
        }
        
        options = {"colors": colors}
        html = displacy.render(doc, style="ent", page=True, options=options)
        
        # Inject dark-theme CSS into the displacy HTML
        dark_css = """
        <style>
        body { 
            background: #0B0618 !important; 
            color: #E8E8F0 !important;
            font-family: 'Inter', sans-serif !important;
            padding: 20px !important;
        }
        .entities { 
            line-height: 2.5 !important; 
            direction: ltr !important;
            font-size: 14px !important;
        }
        mark.entity {
            border-radius: 4px !important;
            padding: 0.2em 0.4em !important;
            margin: 0 0.2em !important;
            font-weight: 600 !important;
            color: #0B0618 !important;
        }
        </style>
        """
        return dark_css + html
        
    except Exception as e:
        return f"<div>⚠️ NER Error: {e}</div>"


def extract_entities(text: str) -> list:
    """
    Returns a list of entity dicts: [{text, label, start, end}]
    Useful for programmatic processing.
    """
    if not text:
        return []
    
    nlp = load_spacy()
    if nlp is None:
        return []
    
    try:
        doc = nlp(text[:MAX_NER_CHARS])
        entities = []
        seen = set()
        for ent in doc.ents:
            key = (ent.text.strip(), ent.label_)
            if key not in seen:
                seen.add(key)
                entities.append({
                    "text": ent.text.strip(),
                    "label": ent.label_,
                    "description": spacy.explain(ent.label_) or ent.label_,
                })
        return entities
    except Exception:
        return []
