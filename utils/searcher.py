# import faiss
# import numpy as np
# import os
# import json
# from utils.embedder import get_embedding

# def load_faiss_index(index_path: str):
#     if not os.path.exists(index_path):
#         raise FileNotFoundError(f"FAISS index not found: {index_path}")
#     return faiss.read_index(index_path)

# def load_chunks_metadata(json_path: str) -> list:
#     if not os.path.exists(json_path):
#         raise FileNotFoundError(f"Metadata JSON not found: {json_path}")
#     with open(json_path, "r", encoding="utf-8") as f:
#         return json.load(f)

# def semantic_search(query: str, index_path: str, json_path: str, top_k: int = 5):
#     index = load_faiss_index(index_path)
#     chunks = load_chunks_metadata(json_path)
    
#     query_embedding = get_embedding(query).reshape(1, -1).astype("float32")

#     distances, indices = index.search(query_embedding, top_k)
    
#     results = []
#     for score, idx in zip(distances[0], indices[0]):
#         if idx < len(chunks):
#             results.append({
#                 "chunk": chunks[idx],
#                 "score": float(score)
#             })
    
#     return results


# import faiss
# import numpy as np
# from utils.embedder import get_embedding


# def semantic_search_in_memory(query: str, index: faiss.Index, chunks: list, top_k: int = 5):
#     """
#     Perform semantic search using an in-memory FAISS index and chunk metadata list.
    
#     Args:
#         query (str): The natural language query.
#         index (faiss.Index): In-memory FAISS index object.
#         chunks (list): List of chunk metadata (usually dicts with 'text' or 'content').
#         top_k (int): Number of top similar chunks to return.

#     Returns:
#         List[dict]: Each dict contains {chunk, score}.
#     """
#     query_embedding = get_embedding(query).reshape(1, -1).astype("float32")
#     distances, indices = index.search(query_embedding, top_k)

#     results = []
#     for score, idx in zip(distances[0], indices[0]):
#         if idx < len(chunks):
#             results.append({
#                 "chunk": chunks[idx],
#                 "score": float(score)
#             })

#     return results


import faiss
import numpy as np
from utils.embedder import get_embedding
from typing import List, Dict


def semantic_search_in_memory(query: str, index: faiss.Index, chunks: List[dict], top_k: int = 5) -> List[Dict]:
    """
    Perform semantic search using an in-memory FAISS index and list of chunk metadata.

    Args:
        query (str): Natural language query.
        index (faiss.Index): In-memory FAISS index built from chunk embeddings.
        chunks (List[dict]): List of chunk metadata (each containing 'text' or 'content').
        top_k (int): Number of top similar chunks to return.

    Returns:
        List[Dict]: Ranked list of relevant chunks and their FAISS similarity scores.
    """
    query_embedding = get_embedding(query).reshape(1, -1).astype("float32")
    distances, indices = index.search(query_embedding, top_k)

    results = []
    for score, idx in zip(distances[0], indices[0]):
        if idx < len(chunks):
            results.append({
                "chunk": chunks[idx],
                "score": float(score)
            })

    return results
