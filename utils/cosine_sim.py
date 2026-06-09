# utils/cosine_sim.py
"""
Cosine similarity computation between documents.
"""
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def compute_cosine_similarity(docs: list) -> tuple:
    """
    Compute pairwise cosine similarity between documents using TF-IDF.
    
    Returns:
        tuple: (similarity_dataframe, highest_pair_info)
    """
    if not docs or len(docs) < 2:
        return pd.DataFrame(), {"pair": None, "score": 0.0}
    
    try:
        labels = [f"Doc {i+1}" for i in range(len(docs))]
        
        vectorizer = TfidfVectorizer(
            stop_words="english",
            max_features=5000,
            ngram_range=(1, 2),
        )
        matrix = vectorizer.fit_transform(docs)
        sim_matrix = cosine_similarity(matrix)
        
        df = pd.DataFrame(sim_matrix, index=labels, columns=labels)
        
        # Find highest non-diagonal pair
        highest_score = 0.0
        highest_pair = ""
        for i in range(len(labels)):
            for j in range(i + 1, len(labels)):
                score = float(sim_matrix[i][j])
                if score > highest_score:
                    highest_score = score
                    highest_pair = f"{labels[i]} ↔ {labels[j]}"
        
        return df, {"pair": highest_pair, "score": highest_score}
    
    except Exception as e:
        return pd.DataFrame(), {"pair": None, "score": 0.0}
