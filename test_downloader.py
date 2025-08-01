import os
import psycopg2
import json
from dotenv import load_dotenv

# Load .env variables
load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")

def get_connection():
    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASS
    )

def list_documents():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT doc_hash, source_url, metadata FROM documents;")
    rows = cur.fetchall()
    cur.close()
    conn.close()

    for i, (doc_hash, source_url, metadata) in enumerate(rows):
        print(f"\n📄 Document {i+1}:")
        print(f"Doc Hash: {doc_hash}")
        print(f"Source URL: {source_url}")
        print(f"Chunks: {len(metadata)}")
        print("First Chunk Preview:", json.dumps(metadata[2], indent=2) if metadata else "No chunks stored.")

if __name__ == "__main__":
    list_documents()
