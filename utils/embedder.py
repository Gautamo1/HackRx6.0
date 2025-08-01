import os
import google.generativeai as genai
import numpy as np
from dotenv import load_dotenv



dotenv_path = 'C:/Users/kumar/OneDrive/Desktop/query_retrieval_system/.env'
load_dotenv(dotenv_path=dotenv_path)

# Load the API key from the environment
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY not found in .env file.")

genai.configure(api_key=api_key)

EMBED_MODEL = "models/embedding-001"

def get_embedding(text: str) -> np.ndarray:
    response = genai.embed_content(
        model=EMBED_MODEL,
        content=text,
        task_type="retrieval_document"
    )
    return np.array(response["embedding"], dtype=np.float32)

def get_embeddings_for_chunks(chunks: list) -> list:
    return [get_embedding(chunk) for chunk in chunks]

