# import os
# import json
# import re
# import google.generativeai as genai
# from dotenv import load_dotenv

# dotenv_path = 'C:/Users/kumar/OneDrive/Desktop/query_retrieval_system/.env'
# load_dotenv(dotenv_path=dotenv_path)

# api_key = os.getenv("GEMINI_API_KEY")
# if not api_key:
#     raise ValueError("GEMINI_API_KEY not found in .env file.")

# genai.configure(api_key=api_key)

# MODEL = "gemini-2.5-flash"

# def clean_and_parse_response(response_text: str) -> dict:
#     """Removes Markdown fences and parses the JSON safely."""
#     cleaned = re.sub(r"^```(?:json)?|```$", "", response_text.strip(), flags=re.MULTILINE)
#     try:
#         return json.loads(cleaned)
#     except json.JSONDecodeError as e:
#         return {
#             "error": f"Failed to parse Gemini response: {str(e)}",
#             "raw_response": response_text
#         }

# def answer_question(query: str, context_chunks: list) -> str:
#     # Use only top-3 relevant chunks to reduce latency
#     context = "\n".join(
#         (chunk.get("text") or chunk.get("content") or chunk.get("chunk") or "")
#         for chunk in context_chunks[:3]
#     )

#     prompt = f"""
# Based on the following context, answer the user's question briefly and factually.

# Return only the 20 word answer as plain text. Do NOT include markdown, rationale, or clauses.

# Context:
# {context}

# Question:
# {query}
# """

#     model = genai.GenerativeModel(MODEL)
#     response = model.generate_content(
#         prompt,
#         safety_settings={
#             "HARASSMENT": "BLOCK_NONE",
#             "HATE": "BLOCK_NONE",
#             "SEXUAL": "BLOCK_NONE",
#             "DANGEROUS": "BLOCK_NONE",
#         }
#     )

#     return response.text.strip()


# import os
# import json
# import re
# import google.generativeai as genai
# from dotenv import load_dotenv

# # Load environment variables
# dotenv_path = 'C:/Users/kumar/OneDrive/Desktop/query_retrieval_system/.env'
# load_dotenv(dotenv_path=dotenv_path)

# # Setup API key
# api_key = os.getenv("GEMINI_API_KEY")
# if not api_key:
#     raise ValueError("GEMINI_API_KEY not found in .env file.")

# genai.configure(api_key=api_key)

# MODEL = "gemini-2.5-flash"

# def clean_and_parse_response(response_text: str) -> dict:
#     """Cleans Markdown-style fences and tries to parse valid JSON."""
#     cleaned = re.sub(r"^```(?:json)?|```$", "", response_text.strip(), flags=re.MULTILINE)
#     try:
#         return json.loads(cleaned)
#     except json.JSONDecodeError as e:
#         return {
#             "error": f"Failed to parse Gemini response: {str(e)}",
#             "raw_response": response_text
#         }

# def answer_question(query: str, context_chunks: list) -> str:
#     """
#     Uses Gemini to answer a question using top-3 context chunks.
#     Returns a 20-word max plain text answer.
#     """
#     context = "\n".join(
#         chunk.get("text") or chunk.get("content") or chunk.get("chunk") or ""
#         for chunk in context_chunks[:3]
#     )

#     prompt = f"""
# Based on the following context, answer the user's question briefly and factually.

# Return only the 20 word answer as plain text. Do NOT include markdown, rationale, or clauses.

# Context:
# {context}

# Question:
# {query}
# """

#     model = genai.GenerativeModel(MODEL)
#     response = model.generate_content(
#         prompt,
#         safety_settings={  # Optional: bypasses strict filtering
#             "HARASSMENT": "BLOCK_NONE",
#             "HATE": "BLOCK_NONE",
#             "SEXUAL": "BLOCK_NONE",
#             "DANGEROUS": "BLOCK_NONE",
#         }
#     )

#     return response.text.strip()



import os
import json
import re
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
dotenv_path = 'C:/Users/kumar/OneDrive/Desktop/query_retrieval_system/.env'
load_dotenv(dotenv_path=dotenv_path)

# Setup API key
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY not found in .env file.")

genai.configure(api_key=api_key)


def clean_and_parse_response(response_text: str) -> dict:
    """Cleans Markdown-style fences and tries to parse valid JSON."""
    cleaned = re.sub(r"^```(?:json)?|```$", "", response_text.strip(), flags=re.MULTILINE)
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError as e:
        return {
            "error": f"Failed to parse Gemini response: {str(e)}",
            "raw_response": response_text
        }
    
async def answer_question(query: str, context_chunks: list) -> str:
    context = "\n".join(
        chunk.get("text") or chunk.get("content") or chunk.get("chunk") or ""
        for chunk in context_chunks[:3]
    )

    prompt = f"""
Answer the question using only the following context. Limit to 20 words. Do not explain.

Context:
{context}

Q: {query}
""".strip()
    
    MODEL = "gemini-2.5-flash"
    model = genai.GenerativeModel(MODEL)

    response = await model.generate_content_async(prompt)
    return response.text.strip()

