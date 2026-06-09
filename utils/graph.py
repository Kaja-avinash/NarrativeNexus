# utils/graph.py
"""
Knowledge Graph generation using spaCy NER + NetworkX + Pyvis.
Uses centralized model loader. Supports entity filtering, community detection,
multiple entity types, and HTML export.
"""
import networkx as nx
from pyvis.network import Network
import streamlit as st
import tempfile
import os
import json
from utils.models import load_spacy
from utils.config import ENTITY_TYPES, MAX_GRAPH_CHARS


def generate_knowledge_graph(
    text: str,
    entity_types: list = None,
    max_nodes: int = 100,
    physics: bool = True,
) -> str:
    """
    Generate an interactive knowledge graph from text.
    
    Args:
        text: Input text to analyze
        entity_types: List of entity types to include (default: PERSON, ORG, GPE)
        max_nodes: Maximum number of nodes in graph
        physics: Whether to enable physics simulation
    
    Returns:
        HTML string of the interactive graph
    """
    if entity_types is None:
        entity_types = ["ORG", "PERSON", "GPE"]
    
    nlp = load_spacy()
    if nlp is None:
        return "<div style='color:white;padding:20px;'>⚠️ Knowledge Graph unavailable — spaCy model not loaded.</div>"
    
    # Limit text size for performance
    text = text[:MAX_GRAPH_CHARS]
    
    try:
        doc = nlp(text)
    except Exception as e:
        return f"<div style='color:white;'>⚠️ Graph processing error: {e}</div>"
    
    G = nx.Graph()
    edge_weights = {}
    
    # Extract entities and build connections
    for sent in doc.sents:
        ents = [
            (e.text.strip(), e.label_)
            for e in sent.ents
            if e.label_ in entity_types and len(e.text.strip()) > 1
        ]
        
        # Deduplicate within sentence
        seen_in_sent = {}
        for text_ent, label in ents:
            if text_ent not in seen_in_sent:
                seen_in_sent[text_ent] = label
        ents = list(seen_in_sent.items())
        
        # Connect entities that co-occur in the same sentence
        if len(ents) > 1:
            for i in range(len(ents)):
                for j in range(i + 1, len(ents)):
                    source, src_label = ents[i]
                    target, tgt_label = ents[j]
                    
                    if source == target:
                        continue
                    
                    # Add nodes with type-specific styling
                    src_color = ENTITY_TYPES.get(src_label, {}).get("color", "#7B2BFF")
                    tgt_color = ENTITY_TYPES.get(tgt_label, {}).get("color", "#7B2BFF")
                    src_label_name = ENTITY_TYPES.get(src_label, {}).get("label", src_label)
                    tgt_label_name = ENTITY_TYPES.get(tgt_label, {}).get("label", tgt_label)
                    
                    G.add_node(source, title=f"{source} [{src_label_name}]", group=src_label, color=src_color)
                    G.add_node(target, title=f"{target} [{tgt_label_name}]", group=tgt_label, color=tgt_color)
                    
                    # Track edge weights
                    edge_key = tuple(sorted([source, target]))
                    edge_weights[edge_key] = edge_weights.get(edge_key, 0) + 1
    
    # Add weighted edges
    for (source, target), weight in edge_weights.items():
        G.add_edge(source, target, weight=weight, title=f"Co-occurs {weight}x")
    
    if len(G.nodes()) == 0:
        return "<div style='color:#E8E8F0;padding:30px;text-align:center;background:#12082A;border-radius:12px;'>ℹ️ No entities found. Try uploading documents with named people, organizations, or locations.</div>"
    
    # Prune to most connected nodes if graph is too large
    if len(G.nodes()) > max_nodes:
        top_nodes = sorted(G.degree(), key=lambda x: x[1], reverse=True)[:max_nodes]
        G = G.subgraph([n for n, d in top_nodes])
    
    # Community detection
    try:
        communities = list(nx.community.greedy_modularity_communities(G))
        for i, community in enumerate(communities):
            for node in community:
                if node in G.nodes():
                    G.nodes[node]["community"] = i
    except Exception:
        pass
    
    # Set node sizes based on degree centrality
    centrality = nx.degree_centrality(G)
    for node in G.nodes():
        degree_val = centrality.get(node, 0)
        G.nodes[node]["size"] = max(15, min(50, 15 + degree_val * 200))
    
    # Create Pyvis network
    net = Network(
        height="650px",
        width="100%",
        bgcolor="#0B0618",
        font_color="#E8E8F0",
        directed=False,
    )
    net.from_nx(G)
    
    # Configure physics
    if physics:
        net.set_options(json.dumps({
            "physics": {
                "enabled": True,
                "barnesHut": {
                    "gravitationalConstant": -8000,
                    "centralGravity": 0.3,
                    "springLength": 180,
                    "springConstant": 0.04,
                    "damping": 0.09,
                },
                "stabilization": {"iterations": 150}
            },
            "interaction": {
                "hover": True,
                "tooltipDelay": 100,
                "zoomView": True,
                "dragView": True,
            },
            "nodes": {
                "font": {"size": 13, "color": "#E8E8F0", "face": "Inter"},
                "borderWidth": 2,
                "borderWidthSelected": 4,
                "shadow": {"enabled": True, "color": "rgba(123,43,255,0.4)", "size": 10}
            },
            "edges": {
                "color": {"color": "rgba(255,255,255,0.15)", "highlight": "#00EAFF"},
                "smooth": {"type": "dynamic"},
                "width": 1,
                "shadow": False,
            }
        }))
    
    # Save to temp file and read HTML
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".html", mode="w") as tmp:
            net.save_graph(tmp.name)
            with open(tmp.name, "r", encoding="utf-8") as f:
                html = f.read()
        os.remove(tmp.name)
        return html
    except Exception as e:
        return f"<div style='color:white;'>⚠️ Graph render error: {e}</div>"


def get_graph_stats(text: str, entity_types: list = None) -> dict:
    """Return graph statistics without rendering."""
    if entity_types is None:
        entity_types = ["ORG", "PERSON", "GPE"]
    
    nlp = load_spacy()
    if nlp is None:
        return {"nodes": 0, "edges": 0, "entities": {}}
    
    doc = nlp(text[:MAX_GRAPH_CHARS])
    entity_counts = {}
    
    for ent in doc.ents:
        if ent.label_ in entity_types:
            label = ENTITY_TYPES.get(ent.label_, {}).get("label", ent.label_)
            entity_counts[label] = entity_counts.get(label, 0) + 1
    
    return {
        "total_entities": sum(entity_counts.values()),
        "entity_breakdown": entity_counts,
    }
