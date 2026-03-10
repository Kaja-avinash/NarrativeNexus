# utils/file_utils.py
import pandas as pd
import json
from bs4 import BeautifulSoup
from docx import Document
import pdfplumber
from pptx import Presentation
import striprtf
from lxml import etree as ET
from PIL import Image
import pytesseract
import ebooklib
from ebooklib import epub
import tempfile
import os


# --- OCR HANDLER (Images) ---
def read_image(file):
    try:
        image = Image.open(file)
        # Ensure Tesseract is installed on the system!
        text = pytesseract.image_to_string(image)
        return text
    except Exception as e:
        return f"Image OCR Error (Check Tesseract installation): {e}"


# --- PDF HANDLER ---
def read_pdf(file):
    try:
        text = []
        with pdfplumber.open(file) as pdf:
            for page in pdf.pages:
                extracted = page.extract_text() or ""
                text.append(extracted)
        return "\n".join(text)
    except Exception as e:
        return f"PDF read error: {e}"


# --- DOCX HANDLER ---
def read_docx(file):
    try:
        doc = Document(file)
        return "\n".join([p.text for p in doc.paragraphs])
    except Exception as e:
        return f"DOCX read error: {e}"


# --- PPTX HANDLER ---
def read_pptx(file):
    try:
        text = []
        prs = Presentation(file)
        for slide in prs.slides:
            for shape in slide.shapes:
                if hasattr(shape, "text"):
                    text.append(shape.text)
        return "\n".join(text)
    except Exception as e:
        return f"PPTX read error: {e}"


# --- EPUB HANDLER (Fixed) ---
def read_epub(file):
    try:
        # EbookLib requires a file path, not a stream.
        # We create a temporary file to handle this safely.
        with tempfile.NamedTemporaryFile(delete=False, suffix=".epub") as tmp:
            tmp.write(file.getvalue())
            tmp_path = tmp.name

        book = epub.read_epub(tmp_path)
        chapters = []
        for item in book.get_items():
            if item.get_type() == ebooklib.ITEM_DOCUMENT:
                soup = BeautifulSoup(item.get_content(), "html.parser")
                chapters.append(soup.get_text())

        os.remove(tmp_path)  # Clean up
        return "\n".join(chapters)
    except Exception as e:
        return f"EPUB read error: {e}"


# --- TEXT/CSV/JSON/HTML (Standard) ---
def read_txt(file):
    try:
        return file.read().decode("utf-8", errors="ignore")
    except:
        return "Text decode error."


def read_csv(file):
    try:
        df = pd.read_csv(file)
        return "\n".join(df.astype(str).agg(" ".join, axis=1))
    except Exception as e:
        return f"CSV error: {e}"


def read_excel(file):
    try:
        df = pd.read_excel(file)
        return "\n".join(df.astype(str).agg(" ".join, axis=1))
    except Exception as e:
        return f"Excel error: {e}"


def read_json(file):
    try:
        data = json.load(file)
        return json.dumps(data, indent=2)
    except Exception as e:
        return f"JSON error: {e}"


def read_html(file):
    try:
        soup = BeautifulSoup(file.read(), "html.parser")
        return soup.get_text(separator="\n")
    except Exception as e:
        return f"HTML error: {e}"


def read_rtf(file):
    try:
        return striprtf.rtf_to_text(file.read().decode("utf-8", errors="ignore"))
    except Exception as e:
        return f"RTF error: {e}"


def read_xml(file):
    try:
        tree = ET.parse(file)
        root = tree.getroot()
        return ET.tostring(root, encoding="unicode", method="text")
    except Exception as e:
        return f"XML error: {e}"


# --- MASTER HANDLER ---
def read_file(file):
    name = file.name.lower()

    if name.endswith(".pdf"):
        return read_pdf(file)
    elif name.endswith((".docx", ".doc")):
        return read_docx(file)
    elif name.endswith((".pptx", ".ppt")):
        return read_pptx(file)
    elif name.endswith(".txt"):
        return read_txt(file)
    elif name.endswith(".csv"):
        return read_csv(file)
    elif name.endswith((".xlsx", ".xls")):
        return read_excel(file)
    elif name.endswith(".json"):
        return read_json(file)
    elif name.endswith((".html", ".htm")):
        return read_html(file)
    elif name.endswith(".rtf"):
        return read_rtf(file)
    elif name.endswith(".epub"):
        return read_epub(file)
    elif name.endswith(".xml"):
        return read_xml(file)
    # ADDED IMAGE SUPPORT
    elif name.endswith((".png", ".jpg", ".jpeg", ".tiff", ".bmp")):
        return read_image(file)
    else:
        return "Unsupported file format."
