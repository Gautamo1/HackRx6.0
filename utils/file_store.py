# import os
# import json
# import faiss
# import numpy as np


# def save_faiss_index(index: faiss.Index, filepath: str):
#     faiss.write_index(index, filepath)


# def load_faiss_index(filepath: str) -> faiss.Index:
#     if not os.path.exists(filepath):
#         raise FileNotFoundError(f"FAISS index not found at {filepath}")
#     return faiss.read_index(filepath)


# def save_metadata(metadata: list, filepath: str):
#     with open(filepath, "w", encoding="utf-8") as f:
#         json.dump(metadata, f, indent=2, ensure_ascii=False)


# def load_metadata(filepath: str) -> list:
#     if not os.path.exists(filepath):
#         raise FileNotFoundError(f"Metadata JSON not found at {filepath}")
#     with open(filepath, "r", encoding="utf-8") as f:
#         return json.load(f)


import psycopg2
import pickle
import json
from utils.db_utils import get_connection


def save_faiss_index_and_metadata_to_db(doc_hash, source_url, index, metadata):
    """
    Stores both FAISS index (as BLOB) and metadata (as JSON) into PostgreSQL.
    """
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO documents (doc_hash, source_url, faiss_index, metadata)
        VALUES (%s, %s, %s, %s)
        ON CONFLICT (doc_hash) DO UPDATE
        SET source_url = EXCLUDED.source_url,
            faiss_index = EXCLUDED.faiss_index,
            metadata = EXCLUDED.metadata;
    """, (
        doc_hash,
        source_url,
        psycopg2.Binary(pickle.dumps(index)),
        json.dumps(metadata)
    ))
    conn.commit()
    cur.close()
    conn.close()


def load_faiss_index_and_metadata_from_db(doc_hash):
    """
    Retrieves FAISS index and metadata from PostgreSQL using doc_hash.
    """
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT faiss_index, metadata FROM documents WHERE doc_hash = %s;
    """, (doc_hash,))
    result = cur.fetchone()
    cur.close()
    conn.close()

    if result is None:
        raise ValueError(f"No document found with hash: {doc_hash}")

    index_blob, metadata_json = result
    index = pickle.loads(index_blob)
    metadata = metadata_json  # Already a list, no need to load again
    return index, metadata
