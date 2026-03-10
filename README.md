# NarrativeNexus AI

### AI-Powered Text Intelligence & Document Analysis Platform

NarrativeNexus is an AI-driven text analytics platform designed to extract meaningful insights from textual data using Natural Language Processing (NLP). The system enables users to upload documents and analyze them through sentiment analysis, topic modeling, semantic search, and similarity detection via an interactive dashboard.

The platform transforms raw text into actionable intelligence using machine learning techniques and data visualization tools.

---

# Table of Contents

- Overview
- Features
- Project Structure
- Quick Start
- Usage
- AI & NLP Modules
- Technologies Used
- Deployment
- Dependencies
- Author
- License

---

# Overview

NarrativeNexus leverages advanced Natural Language Processing techniques to analyze and interpret textual data. The platform provides an intuitive interface where users can upload documents and gain insights through automated text analysis.

It integrates multiple NLP components including sentiment classification, topic discovery, semantic search, and similarity analysis. Results are visualized through charts, word clouds, and dashboards to improve interpretability.

The application is built using Python and Streamlit to provide an interactive and user-friendly environment.

---

# Features

• Document Upload and Processing
• Sentiment Analysis for Text Data
• Topic Modeling for Theme Extraction
• Semantic Search across Documents
• Word Cloud Visualization
• Document Similarity Detection
• Interactive Data Visualization Dashboard
• Export Analysis Reports as PDF

---

# Project Structure

```
NarrativeNexus
│
├── assets
│   └── custom.css
│
├── lib
│   ├── preprocessing.py
│   ├── sentiment.py
│   ├── topic_modeling.py
│   ├── semantic_search.py
│   ├── visualization.py
│   ├── language.py
│   └── report.py
│
├── uploaded_files
│
├── app.py
├── requirements.txt
└── README.md
```

---

# Quick Start

## Clone the Repository

git clone https://github.com/Kaja-avinash/NarrativeNexus.git

Navigate to the project directory

cd NarrativeNexus

---

## Create Virtual Environment

python -m venv venv

Activate virtual environment

Windows:

venv\Scripts\activate

Mac/Linux:

source venv/bin/activate

---

## Install Dependencies

pip install -r requirements.txt

---

## Run the Application

streamlit run app.py

Open the application in your browser

http://localhost:8501

---

# Usage

The application provides several modules for document analysis.

| Module              | Description                    |
| ------------------- | ------------------------------ |
| Upload Documents    | Upload text files for analysis |
| Sentiment Analysis  | Determine emotional tone       |
| Topic Modeling      | Discover hidden themes         |
| Word Cloud          | Visualize most frequent terms  |
| Semantic Search     | Search documents intelligently |
| Similarity Analysis | Identify related documents     |
| Export Report       | Download analysis results      |

---

# AI & NLP Modules

### Sentiment Analysis

Classifies textual content into:

• Positive
• Negative
• Neutral

This helps determine the overall emotional tone of the document.

---

### Topic Modeling

Topic modeling identifies hidden themes within documents using machine learning techniques such as:

• TF-IDF Vectorization
• Latent Dirichlet Allocation (LDA)

---

### Semantic Search

Semantic search allows intelligent searching of text documents by understanding contextual meaning rather than relying solely on keywords.

---

### Cosine Similarity

Cosine similarity is used to measure similarity between documents by comparing vector representations of text.

---

# Technologies Used

Python
Streamlit
Pandas
NumPy
Scikit-learn
NLTK
Matplotlib
WordCloud

---

# Deployment

The application can be deployed using:

• Streamlit Community Cloud
• AWS EC2
• Docker Containers

---

# Dependencies

Install required libraries using:

pip install -r requirements.txt

Main libraries used in this project include:

streamlit
pandas
numpy
scikit-learn
matplotlib
wordcloud
nltk

---

# Author

K. Avinash
B.Tech – Artificial Intelligence and Data Science
Vasireddy Venkatadri Institute of Technology

---

# License

Copyright (c) 2026 K. Avinash

All Rights Reserved.

This project and its source code are the intellectual property of K. Avinash.

No part of this project may be copied, modified, distributed, published, or used for commercial or non-commercial purposes without explicit written permission from the author.

Unauthorized use, reproduction, or distribution of this code is strictly prohibited.
