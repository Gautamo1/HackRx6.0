# import psycopg2
# from psycopg2.extras import RealDictCursor
# import os
# from dotenv import load_dotenv

# load_dotenv()

# DB_HOST = os.getenv("DB_HOST", "localhost")
# DB_PORT = os.getenv("DB_PORT", "5432")
# DB_NAME = os.getenv("DB_NAME", "Query")
# DB_USER = os.getenv("DB_USER", "postgres")
# DB_PASS = os.getenv("DB_PASS", "Gautam@802108")

# def get_connection():
#     return psycopg2.connect(
#         host=DB_HOST,
#         port=DB_PORT,
#         dbname=DB_NAME,
#         user=DB_USER,
#         password=DB_PASS
#     )

# def init_db():
#     conn = get_connection()
#     cur = conn.cursor()
#     cur.execute("""
#         CREATE TABLE IF NOT EXISTS documents (
#             doc_hash TEXT PRIMARY KEY,
#             source_url TEXT,
#             faiss_index_path TEXT,
#             metadata_path TEXT,
#             uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
#         );
#     """)
#     conn.commit()
#     cur.close()
#     conn.close()

# def insert_document(doc_hash, source_url, index_path, metadata_path):
#     conn = get_connection()
#     cur = conn.cursor()
#     cur.execute("""
#         INSERT INTO documents (doc_hash, source_url, faiss_index_path, metadata_path)
#         VALUES (%s, %s, %s, %s)
#         ON CONFLICT (doc_hash) DO NOTHING;
#     """, (doc_hash, source_url, index_path, metadata_path))
#     conn.commit()
#     cur.close()
#     conn.close()

# def get_document_by_hash(doc_hash):
#     conn = get_connection()
#     cur = conn.cursor(cursor_factory=RealDictCursor)
#     cur.execute("SELECT * FROM documents WHERE doc_hash = %s;", (doc_hash,))
#     result = cur.fetchone()
#     cur.close()
#     conn.close()
#     return result


# import psycopg2
# from psycopg2.extras import RealDictCursor
# import os
# from dotenv import load_dotenv

# load_dotenv()

# DB_HOST = os.getenv("DB_HOST", "localhost")
# DB_PORT = os.getenv("DB_PORT", "5432")
# DB_NAME = os.getenv("DB_NAME", "Query")
# DB_USER = os.getenv("DB_USER", "postgres")
# DB_PASS = os.getenv("DB_PASS", "Gautam@802108")  # Use env var or .env for production!

# def get_connection():
#     return psycopg2.connect(
#         host=DB_HOST,
#         port=DB_PORT,
#         dbname=DB_NAME,
#         user=DB_USER,
#         password=DB_PASS
#     )

# def init_db():
#     conn = get_connection()
#     cur = conn.cursor()
#     cur.execute("""
#         CREATE TABLE IF NOT EXISTS documents (
#             doc_hash TEXT PRIMARY KEY,
#             source_url TEXT,
#             faiss_index_path TEXT,
#             metadata_path TEXT,
#             uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
#         );
#     """)
#     conn.commit()
#     cur.close()
#     conn.close()

# def insert_document(doc_hash, source_url, index_path, metadata_path):
#     conn = get_connection()
#     cur = conn.cursor()
#     cur.execute("""
#         INSERT INTO documents (doc_hash, source_url, faiss_index_path, metadata_path)
#         VALUES (%s, %s, %s, %s)
#         ON CONFLICT (doc_hash) DO NOTHING;
#     """, (doc_hash, source_url, index_path, metadata_path))
#     conn.commit()
#     cur.close()
#     conn.close()

# def get_document_by_hash(doc_hash):
#     conn = get_connection()
#     cur = conn.cursor(cursor_factory=RealDictCursor)
#     cur.execute("SELECT * FROM documents WHERE doc_hash = %s;", (doc_hash,))
#     result = cur.fetchone()
#     cur.close()
#     conn.close()
#     return result


# import psycopg2
# from psycopg2.extras import RealDictCursor
# import os
# import pickle
# import json
# from dotenv import load_dotenv

# load_dotenv()

# DB_HOST = os.getenv("DB_HOST")
# DB_PORT = os.getenv("DB_PORT")
# DB_NAME = os.getenv("DB_NAME")
# DB_USER = os.getenv("DB_USER")
# DB_PASS = os.getenv("DB_PASS")

# def get_connection():
#     return psycopg2.connect(
#         host=DB_HOST,
#         port=DB_PORT,
#         dbname=DB_NAME,
#         user=DB_USER,
#         password=DB_PASS
#     )

# def init_db():
#     conn = get_connection()
#     cur = conn.cursor()
#     cur.execute("""
#         CREATE TABLE IF NOT EXISTS documents (
#             doc_hash TEXT PRIMARY KEY,
#             source_url TEXT,
#             faiss_index BYTEA,
#             metadata JSONB,
#             uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
#         );
#     """)
#     conn.commit()
#     cur.close()
#     conn.close()

# def insert_document(doc_hash, source_url, faiss_index_obj, metadata_obj):
#     conn = get_connection()
#     cur = conn.cursor()

#     # Serialize FAISS index and metadata
#     faiss_bytes = pickle.dumps(faiss_index_obj)
#     metadata_json = json.dumps(metadata_obj)

#     cur.execute("""
#         INSERT INTO documents (doc_hash, source_url, faiss_index, metadata)
#         VALUES (%s, %s, %s, %s)
#         ON CONFLICT (doc_hash) DO NOTHING;
#     """, (doc_hash, source_url, faiss_bytes, metadata_json))

#     conn.commit()
#     cur.close()
#     conn.close()

# def get_document_by_hash(doc_hash):
#     conn = get_connection()
#     cur = conn.cursor(cursor_factory=RealDictCursor)
#     cur.execute("SELECT * FROM documents WHERE doc_hash = %s;", (doc_hash,))
#     result = cur.fetchone()
#     cur.close()
#     conn.close()

#     if result:
#         result["faiss_index"] = pickle.loads(result["faiss_index"])
#     return result


import os
import psycopg2
import pickle
import json
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
from urllib.parse import urlparse

load_dotenv()

def get_connection():
    db_url = os.getenv("DATABASE_URL")
    if db_url:
        return psycopg2.connect(db_url)
    else:
        return psycopg2.connect(
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASS")
        )

def init_db():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS documents (
                    doc_hash TEXT PRIMARY KEY,
                    source_url TEXT,
                    faiss_index BYTEA,
                    metadata JSONB,
                    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)
            conn.commit()

def insert_document(doc_hash, source_url, faiss_index_obj, metadata_obj):
    faiss_bytes = pickle.dumps(faiss_index_obj)
    metadata_json = json.dumps(metadata_obj)

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO documents (doc_hash, source_url, faiss_index, metadata)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (doc_hash) DO NOTHING;
            """, (doc_hash, source_url, faiss_bytes, metadata_json))
            conn.commit()

def get_document_by_hash(doc_hash):
    with get_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("SELECT * FROM documents WHERE doc_hash = %s;", (doc_hash,))
            result = cur.fetchone()

    if result and result.get("faiss_index"):
        result["faiss_index"] = pickle.loads(result["faiss_index"])
    return result
