# NarrativeNexus AI v2.0

<div align="center">

![NarrativeNexus AI](https://img.shields.io/badge/NarrativeNexus-AI%20Platform-7B2BFF?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.11-blue?style=for-the-badge&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.32+-FF4B4B?style=for-the-badge&logo=streamlit)
![License](https://img.shields.io/badge/License-All%20Rights%20Reserved-red?style=for-the-badge)

**Transform Documents Into Intelligence**

*Enterprise-grade AI document analysis platform with 20+ NLP features*

</div>

---

## 🚀 Live Demo

**Deployed Application:** [https://narrativenexus-ai.onrender.com](https://narrativenexus-ai.onrender.com)

> ⚠️ First load may take 2-3 minutes as AI models initialize. Subsequent loads are fast.

---

## ✨ Features

### Document Processing
| Feature | Formats | Status |
|---------|---------|--------|
| PDF Extraction | `.pdf` | ✅ |
| DOCX Processing | `.docx`, `.doc` | ✅ |
| PowerPoint | `.pptx` | ✅ |
| EPUB Books | `.epub` | ✅ |
| Spreadsheets | `.csv`, `.xlsx` | ✅ |
| OCR (Images) | `.jpg`, `.png`, `.bmp`, `.tiff` | ✅ |
| Web/HTML | `.html`, `.htm` | ✅ |
| Data Formats | `.json`, `.xml`, `.rtf` | ✅ |
| Plain Text | `.txt`, `.md` | ✅ |

### AI & NLP Analysis
- 🤖 **Summarization** — DistilBART neural summarization
- 😊 **Sentiment Analysis** — DistilBERT-based classification
- 💭 **Topic Modeling** — LDA with interactive pyLDAvis visualization
- 🏷️ **Named Entity Recognition** — spaCy with 10+ entity types
- 🌐 **Knowledge Graph** — Entity relationship network with community detection
- 🔍 **Semantic Search** — SentenceTransformers + NearestNeighbors
- 📐 **Document Similarity** — TF-IDF cosine similarity heatmap
- 🌌 **3D Document Space** — PCA-based vector space visualization
- 🌍 **Language Detection** — 20+ languages
- 🔄 **Translation** — Auto-translate to English (graceful fallback)

### Enterprise UI
- 🏠 **Dashboard** — KPI cards, activity log, session history
- 📄 **Documents** — Drag-and-drop upload, file previews, AI workflow progress
- 🧠 **AI Analysis** — 6-tab results dashboard with multi-doc comparison
- 🔍 **Semantic Search** — Search history, suggested prompts, relevance indicators
- 🌐 **Knowledge Graph** — Entity filtering, physics controls, HTML export
- 📊 **Visualizations** — Word cloud, 3D space, heatmap, topic map
- 📑 **Reports** — PDF, CSV, JSON export with full analysis data
- ⚙ **Settings** — NLP config, graph settings, system health check

---

## 🏗️ Architecture

```
NarrativeNexus/
├── app.py                 # Main application (8-page enterprise UI)
├── requirements.txt       # Python dependencies
├── packages.txt           # System packages (Tesseract OCR)
├── runtime.txt            # Python version
├── Procfile               # Deployment startup command
├── render.yaml            # Render.com deployment config
├── .streamlit/
│   └── config.toml        # Streamlit production config
└── utils/
    ├── config.py          # Centralized configuration
    ├── state.py           # Session state management
    ├── models.py          # ML model loading (cached singletons)
    ├── file_utils.py      # File format handlers (18+ types)
    ├── preprocessing.py   # Text normalization + lemmatization
    ├── summarizer.py      # HuggingFace DistilBART summarization
    ├── sentiment.py       # Sentiment analysis + helpers
    ├── topic_modeling.py  # LDA topic modeling + pyLDAvis
    ├── ner.py             # Named Entity Recognition (spaCy)
    ├── graph.py           # Knowledge graph (NetworkX + Pyvis)
    ├── semantic_search.py # Semantic search (SentenceTransformers)
    ├── cosine_sim.py      # Document similarity
    ├── visualization.py   # Charts, word clouds, 3D plots, UI components
    ├── language.py        # Language detection
    ├── translate.py       # Translation (deep-translator)
    └── report.py          # PDF, CSV, JSON report generation
```

---

## 🛠️ Quick Start

### Prerequisites
- Python 3.11+
- Tesseract OCR (for image/scanned PDF support)

### Local Installation

```bash
# Clone the repository
git clone https://github.com/Kaja-avinash/NarrativeNexus.git
cd NarrativeNexus

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Mac/Linux

# Install dependencies
pip install -r requirements.txt

# Download NLP models
python -m spacy download en_core_web_sm
python -m nltk.downloader punkt stopwords wordnet punkt_tab

# Run the application
streamlit run app.py
```

Open: http://localhost:8501

### OCR Setup (Optional)

For image and scanned PDF support, install Tesseract:
- **Windows:** [Tesseract installer](https://github.com/UB-Mannheim/tesseract/wiki)
- **macOS:** `brew install tesseract`
- **Linux:** `sudo apt-get install tesseract-ocr`

---

## 🚀 Deployment

### Render.com (Recommended)

1. Fork this repository to your GitHub account
2. Go to [render.com](https://render.com) → New → Web Service
3. Connect your GitHub repo
4. Render will auto-detect `render.yaml` and configure the service
5. Click **Deploy**

Build command (auto-detected from render.yaml):
```bash
pip install -r requirements.txt && python -m spacy download en_core_web_sm && python -m nltk.downloader punkt stopwords wordnet
```

Start command:
```bash
streamlit run app.py --server.port $PORT --server.address 0.0.0.0 --server.headless true
```

### Streamlit Community Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Connect your GitHub repo
3. Set main file to `app.py`
4. Deploy

> Note: `packages.txt` handles Tesseract installation automatically on Streamlit Cloud.

---

## 🤖 AI Models Used

| Model | Purpose | Size |
|-------|---------|------|
| `sshleifer/distilbart-cnn-12-6` | Text summarization | ~307MB |
| `distilbert-base-uncased-finetuned-sst-2-english` | Sentiment analysis | ~268MB |
| `all-MiniLM-L6-v2` | Semantic search | ~80MB |
| `en_core_web_sm` (spaCy) | NER + Knowledge Graph | ~12MB |

---

## 🔧 Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `TOKENIZERS_PARALLELISM` | Disable HuggingFace warnings | `false` |
| `TRANSFORMERS_CACHE` | Model cache directory | System default |
| `HF_HOME` | HuggingFace home | System default |
| `DEBUG` | Enable debug mode | `false` |

---

## 📊 Performance

| Operation | Typical Time |
|-----------|-------------|
| App startup (cold) | 30-120 seconds |
| File upload + parsing | 1-5 seconds |
| AI analysis (5 docs) | 15-60 seconds |
| Semantic search | <2 seconds |
| Knowledge graph | 3-10 seconds |
| Report generation | 1-3 seconds |

---

## 👨‍💻 Author

**K. Avinash**  
B.Tech — Artificial Intelligence and Data Science  
Vasireddy Venkatadri Institute of Technology

---

## 📄 License

Copyright © 2026 K. Avinash. All Rights Reserved.

This project and its source code are the intellectual property of K. Avinash.
No part of this project may be copied, modified, distributed, or used without explicit written permission.
