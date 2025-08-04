# utils/clause_matcher.py

import numpy as np
import google.generativeai as genai
from sklearn.metrics.pairwise import cosine_similarity

MODEL = "models/embedding-001"

def get_text_embedding(text: str) -> list:
    model = genai.GenerativeModel(MODEL)
    return model.embed_text(text)["embedding"]

def extract_relevant_clauses(query: str, context_chunks: list, top_k: int = 5) -> list:
    # Step 1: Embed the query
    query_embedding = np.array(get_text_embedding(query)).reshape(1, -1)

    # Step 2: Prepare clause texts
    clause_texts = [
        chunk.get("text") or chunk.get("content") or chunk.get("page_content") or getattr(chunk, "page_content", "")
        for chunk in context_chunks
    ]

    # Step 3: Embed all clause texts
    clause_embeddings = np.array([
        get_text_embedding(text) for text in clause_texts
    ])

    # Step 4: Compute cosine similarity
    similarities = cosine_similarity(query_embedding, clause_embeddings)[0]

    # Step 5: Get top-k similar clauses
    top_indices = similarities.argsort()[-top_k:][::-1]
    top_clauses = [clause_texts[i] for i in top_indices]

    return top_clauses

