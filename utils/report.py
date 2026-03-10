# utils/report.py
from fpdf import FPDF
import re
import textwrap


def clean_text(text):
    if not text:
        return ""
    # Remove non-ASCII characters to prevent PDF crashes
    text = re.sub(r"[^\x00-\x7F]+", " ", text)
    text = text.replace("\r", " ").replace("\t", " ")
    return text.strip()


def safe_multicell(pdf, text, line_height=8):
    if not text:
        return

    # Effective page width
    max_width = pdf.w - pdf.l_margin - pdf.r_margin

    for raw_line in text.split("\n"):
        line = raw_line.strip()
        if not line:
            pdf.ln(line_height)
            continue

        # Wrap text to avoid overflow
        wrapped = textwrap.wrap(line, width=90, break_long_words=True)
        for wline in wrapped:
            # Check if we need a page break
            if pdf.get_y() > pdf.h - 20:
                pdf.add_page()

            pdf.set_x(10)
            pdf.multi_cell(max_width, line_height, wline)


def generate_pdf(summary, topics, sentiments):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Helvetica", size=12)

    pdf.cell(0, 10, "NarrativeNexus - Analysis Report", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(4)

    # -------- Summary --------
    pdf.set_font("Helvetica", style="B", size=12)
    pdf.cell(0, 10, "Summary", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", size=11)

    safe_multicell(pdf, clean_text(summary))

    # -------- Topics --------
    pdf.ln(4)
    pdf.set_font("Helvetica", style="B", size=12)
    pdf.cell(0, 10, "Topics", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", size=11)

    for i, topic in enumerate(topics):
        topic_line = f"Topic {i + 1}: {', '.join(topic)}"
        safe_multicell(pdf, clean_text(topic_line))

    # -------- Sentiment --------
    pdf.ln(4)
    pdf.set_font("Helvetica", style="B", size=12)
    pdf.cell(0, 10, "Sentiment Analysis", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", size=11)

    for i, s in enumerate(sentiments):
        line = f"Document {i + 1}: {s['label']} (Score: {s['score']:.3f})"
        safe_multicell(pdf, clean_text(line))

    # Return bytes directly (Correct for fpdf2)
    return bytes(pdf.output())
