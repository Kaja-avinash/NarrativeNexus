import networkx as nx
from pyvis.network import Network
import spacy
import streamlit as st
import tempfile
import os


@st.cache_resource
def load_spacy_model():
    return spacy.load("en_core_web_sm")


nlp = load_spacy_model()


def generate_knowledge_graph(text):
    # Limit text size for performance
    doc = nlp(text[:200000])

    G = nx.Graph()

    # Extract entities and build connections
    for sent in doc.sents:
        # We focus on Organizations, People, and Locations
        ents = [e.text for e in sent.ents if e.label_ in ["ORG", "PERSON", "GPE"]]

        # If 2+ entities appear in the same sentence, assume they are related
        if len(ents) > 1:
            for i in range(len(ents) - 1):
                source = ents[i]
                target = ents[i + 1]

                # Add nodes
                G.add_node(source, title=source, group="Entity", color="#00eaff")
                G.add_node(target, title=target, group="Entity", color="#00eaff")

                # Add edge (connection)
                if G.has_edge(source, target):
                    G[source][target]["weight"] += 1
                else:
                    G.add_edge(source, target, weight=1)

    # Visualization settings
    net = Network(height="600px", width="100%", bgcolor="#1c0b2c", font_color="white")
    net.from_nx(G)

    # Physics for the cool "floating" effect
    net.repulsion(node_distance=150, spring_length=200)

    # Save to temporary HTML file
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as tmp:
            net.save_graph(tmp.name)
            with open(tmp.name, "r", encoding="utf-8") as f:
                html = f.read()
        os.remove(tmp.name)
        return html
    except Exception as e:
        return f"<div>Error generating graph: {e}</div>"
