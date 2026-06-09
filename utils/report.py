# utils/report.py
"""
Multi-format report generation for NarrativeNexus AI.
Supports PDF, CSV, JSON export formats.
"""
from fpdf import FPDF
import re
import textwrap
import json
import csv
import io
import time
from utils.config import APP_NAME, APP_VERSION


def clean_text(text: str) -> str:
    """Remove non-ASCII characters to prevent PDF encoding issues."""
    if not text:
        return ""
    text = re.sub(r"[^\x00-\x7F]+", " ", text)
    text = text.replace("\r", " ").replace("\t", " ")
    return text.strip()


def safe_multicell(pdf: FPDF, text: str, line_height: int = 8) -> None:
    """Write text to PDF with automatic line wrapping and page breaks."""
    if not text:
        return
    max_width = pdf.w - pdf.l_margin - pdf.r_margin
    for raw_line in text.split("\n"):
        line = raw_line.strip()
        if not line:
            pdf.ln(line_height)
            continue
        wrapped = textwrap.wrap(line, width=90, break_long_words=True)
        for wline in wrapped:
            if pdf.get_y() > pdf.h - 20:
                pdf.add_page()
            pdf.set_x(10)
            pdf.multi_cell(max_width, line_height, wline)


def generate_pdf(
    summary: str,
    topics: list,
    sentiments: list,
    entities: list = None,
    file_names: list = None,
) -> bytes:
    """
    Generate a comprehensive PDF analysis report.
    
    Returns:
        bytes: PDF file content
    """
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    
    # ── Header ──────────────────────────────────────────────────────────────
    pdf.set_fill_color(11, 6, 24)  # Dark background
    pdf.set_font("Helvetica", style="B", size=20)
    pdf.cell(0, 15, f"{APP_NAME} — Analysis Report", new_x="LMARGIN", new_y="NEXT")
    
    pdf.set_font("Helvetica", size=10)
    pdf.set_text_color(128, 128, 160)
    pdf.cell(0, 8, f"Generated: {time.strftime('%Y-%m-%d %H:%M:%S')} | Version {APP_VERSION}",
             new_x="LMARGIN", new_y="NEXT")
    
    if file_names:
        pdf.cell(0, 8, f"Documents: {', '.join([clean_text(f) for f in file_names[:5]])}",
                 new_x="LMARGIN", new_y="NEXT")
    
    pdf.set_text_color(0, 0, 0)
    pdf.ln(6)
    
    # ── Summary ──────────────────────────────────────────────────────────────
    pdf.set_font("Helvetica", style="B", size=14)
    pdf.cell(0, 10, "Executive Summary", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(2)
    pdf.set_font("Helvetica", size=11)
    safe_multicell(pdf, clean_text(summary))
    pdf.ln(6)
    
    # ── Topics ───────────────────────────────────────────────────────────────
    pdf.set_font("Helvetica", style="B", size=14)
    pdf.cell(0, 10, "Discovered Topics", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(2)
    pdf.set_font("Helvetica", size=11)
    
    for i, topic in enumerate(topics):
        topic_line = f"Topic {i + 1}: {', '.join(topic)}"
        safe_multicell(pdf, clean_text(topic_line))
    pdf.ln(6)
    
    # ── Sentiment ─────────────────────────────────────────────────────────────
    pdf.set_font("Helvetica", style="B", size=14)
    pdf.cell(0, 10, "Sentiment Analysis", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(2)
    pdf.set_font("Helvetica", size=11)
    
    for i, s in enumerate(sentiments):
        line = f"Document {i + 1}: {s['label']} (Confidence: {s.get('confidence_pct', s['score']*100):.1f}%)"
        safe_multicell(pdf, clean_text(line))
    pdf.ln(6)
    
    # ── Named Entities ────────────────────────────────────────────────────────
    if entities:
        pdf.set_font("Helvetica", style="B", size=14)
        pdf.cell(0, 10, "Named Entities", new_x="LMARGIN", new_y="NEXT")
        pdf.ln(2)
        pdf.set_font("Helvetica", size=11)
        
        entity_by_type = {}
        for e in entities:
            label = e.get("description", e.get("label", "Unknown"))
            entity_by_type.setdefault(label, []).append(e["text"])
        
        for label, ents in entity_by_type.items():
            line = f"{label}: {', '.join(ents[:10])}"
            if len(ents) > 10:
                line += f" (+{len(ents)-10} more)"
            safe_multicell(pdf, clean_text(line))
    
    return bytes(pdf.output())


def generate_csv(topics: list, sentiments: list, entities: list = None) -> str:
    """
    Generate a CSV report of analysis results.
    
    Returns:
        str: CSV content
    """
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Sentiments section
    writer.writerow(["=== SENTIMENT ANALYSIS ==="])
    writer.writerow(["Document", "Label", "Score", "Confidence %"])
    for i, s in enumerate(sentiments):
        writer.writerow([
            f"Doc {i+1}",
            s["label"],
            f"{s['score']:.3f}",
            f"{s.get('confidence_pct', s['score']*100):.1f}%"
        ])
    
    writer.writerow([])
    
    # Topics section
    writer.writerow(["=== TOPIC MODELING ==="])
    writer.writerow(["Topic #", "Keywords"])
    for i, topic in enumerate(topics):
        writer.writerow([f"Topic {i+1}", ", ".join(topic)])
    
    # Entities section
    if entities:
        writer.writerow([])
        writer.writerow(["=== NAMED ENTITIES ==="])
        writer.writerow(["Entity", "Type", "Description"])
        for e in entities:
            writer.writerow([e["text"], e["label"], e.get("description", "")])
    
    return output.getvalue()


def generate_json_report(
    summary: str,
    topics: list,
    sentiments: list,
    entities: list = None,
    file_names: list = None,
) -> str:
    """
    Generate a JSON report of all analysis results.
    
    Returns:
        str: JSON content
    """
    report = {
        "metadata": {
            "app": APP_NAME,
            "version": APP_VERSION,
            "generated": time.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "documents": file_names or [],
        },
        "summary": summary,
        "topics": [
            {"topic_id": i + 1, "keywords": topic}
            for i, topic in enumerate(topics)
        ],
        "sentiments": [
            {
                "document": f"doc_{i+1}",
                "label": s["label"],
                "score": s["score"],
                "confidence_pct": s.get("confidence_pct", s["score"] * 100),
            }
            for i, s in enumerate(sentiments)
        ],
        "entities": entities or [],
    }
    return json.dumps(report, indent=2, ensure_ascii=False)
