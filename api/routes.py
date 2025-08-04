# from fastapi import APIRouter, Depends
# from pydantic import BaseModel
# from typing import List
# import faiss
# import numpy as np

# from utils.auth import verify_token
# from utils.downloader import download_file_from_url
# from utils.parser import parse_file
# from utils.chunker import chunk_text
# from utils.embedder import get_embeddings_for_chunks
# from utils.file_store import save_faiss_index_and_metadata_to_db, load_faiss_index_and_metadata_from_db
# from utils.searcher import semantic_search_in_memory
# from utils.gemini_llm import answer_question
# from utils.utils import get_file_hash
# from utils.db_utils import init_db, get_document_by_hash

# router = APIRouter()
# init_db()

# class HackRxInput(BaseModel):
#     documents: str
#     questions: List[str]

# class HackRxResponse(BaseModel):
#     answers: List[str]

# @router.post("/run", response_model=HackRxResponse, dependencies=[Depends(verify_token)])
# def run_endpoint(payload: HackRxInput):
#     file_path = download_file_from_url(payload.documents)
#     doc_hash = get_file_hash(file_path)

#     doc_record = get_document_by_hash(doc_hash)
#     if doc_record and doc_record.get("faiss_index") and doc_record.get("metadata"):
#         index, chunks = load_faiss_index_and_metadata_from_db(doc_hash)
#     else:
#         # Pipeline: parse → chunk → embed → index → store
#         text = parse_file(file_path)
#         chunks = chunk_text(text)
#         embeddings = get_embeddings_for_chunks(chunks)

#         index = faiss.IndexFlatL2(len(embeddings[0]))
#         index.add(np.array(embeddings, dtype=np.float32))

#         # Save into database instead of files
#         save_faiss_index_and_metadata_to_db(doc_hash, payload.documents, index, chunks)

#     answers = []
#     for question in payload.questions:
#         top_chunks = semantic_search_in_memory(question, index, chunks)
#         answer = answer_question(question, top_chunks)
#         answers.append(answer)

#     return HackRxResponse(answers=answers)


# from fastapi import APIRouter, Depends
# from pydantic import BaseModel
# from typing import List
# import faiss
# import numpy as np
# import time  # ⏱ For timing

# from utils.auth import verify_token
# from utils.downloader import download_file_from_url
# from utils.parser import parse_file
# from utils.chunker import chunk_text
# from utils.embedder import get_embeddings_for_chunks
# from utils.file_store import save_faiss_index_and_metadata_to_db, load_faiss_index_and_metadata_from_db
# from utils.searcher import semantic_search_in_memory
# from utils.gemini_llm import answer_question
# from utils.utils import get_file_hash
# from utils.db_utils import init_db, get_document_by_hash

# router = APIRouter()
# init_db()

# class HackRxInput(BaseModel):
#     documents: str
#     questions: List[str]

# class HackRxResponse(BaseModel):
#     answers: List[str]

# @router.post("/run", response_model=HackRxResponse, dependencies=[Depends(verify_token)])
# def run_endpoint(payload: HackRxInput):
#     overall_start = time.time()

#     # ⏱ Download
#     t0 = time.time()
#     file_path = download_file_from_url(payload.documents)
#     print(f"📥 Downloaded file in {time.time() - t0:.2f} seconds")

#     # ⏱ Hashing
#     t0 = time.time()
#     doc_hash = get_file_hash(file_path)
#     print(f"🔑 Generated hash in {time.time() - t0:.2f} seconds")

#     # ⏱ Check cache
#     t0 = time.time()
#     doc_record = get_document_by_hash(doc_hash)
#     print(f"📦 Checked cache in {time.time() - t0:.2f} seconds")

#     if doc_record and doc_record.get("faiss_index") and doc_record.get("metadata"):
#         t0 = time.time()
#         index, chunks = load_faiss_index_and_metadata_from_db(doc_hash)
#         print(f"📚 Loaded FAISS index + metadata from DB in {time.time() - t0:.2f} seconds")
#     else:
#         # ⏱ Parse
#         t0 = time.time()
#         text = parse_file(file_path)
#         print(f"📄 Parsed document in {time.time() - t0:.2f} seconds")

#         # ⏱ Chunk
#         t0 = time.time()
#         chunks = chunk_text(text)
#         print(f"✂️ Chunked document in {time.time() - t0:.2f} seconds")

#         # ⏱ Embed
#         t0 = time.time()
#         embeddings = get_embeddings_for_chunks(chunks)
#         print(f"🧠 Embedded {len(chunks)} chunks in {time.time() - t0:.2f} seconds")

#         # ⏱ FAISS index
#         t0 = time.time()
#         index = faiss.IndexFlatL2(len(embeddings[0]))
#         index.add(np.array(embeddings, dtype=np.float32))
#         print(f"📊 Built FAISS index in {time.time() - t0:.2f} seconds")

#         # ⏱ Store
#         t0 = time.time()
#         save_faiss_index_and_metadata_to_db(doc_hash, payload.documents, index, chunks)
#         print(f"💾 Saved index + metadata to DB in {time.time() - t0:.2f} seconds")

#     # ⏱ QA loop
#     answers = []
#     for i, question in enumerate(payload.questions):
#         print(f"\n🔎 Question {i+1}: {question}")

#         t0 = time.time()
#         top_chunks = semantic_search_in_memory(question, index, chunks)
#         print(f"📌 Retrieved top chunks in {time.time() - t0:.2f} seconds")

#         t0 = time.time()
#         answer = answer_question(question, top_chunks)
#         print(f"📝 Generated answer in {time.time() - t0:.2f} seconds")

#         answers.append(answer)

#     print(f"\n⏱ Total time taken: {time.time() - overall_start:.2f} seconds")

#     return HackRxResponse(answers=answers)
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import List
import faiss
import numpy as np
import asyncio

from utils.auth import verify_token
from utils.downloader import download_file_from_url
from utils.parser import parse_file
from utils.chunker import chunk_text
from utils.embedder import get_embeddings_for_chunks
from utils.file_store import save_faiss_index_and_metadata_to_db, load_faiss_index_and_metadata_from_db
from utils.searcher import semantic_search_in_memory
from utils.gemini_llm import answer_question
from utils.utils import get_file_hash
from utils.db_utils import init_db, get_document_by_hash

router = APIRouter()
init_db()

class HackRxInput(BaseModel):
    documents: str
    questions: List[str]

class HackRxResponse(BaseModel):
    answers: List[str]

@router.post("/run", response_model=HackRxResponse, dependencies=[Depends(verify_token)])
async def run_endpoint(payload: HackRxInput):
    file_path = download_file_from_url(payload.documents)
    doc_hash = get_file_hash(file_path)
    doc_record = get_document_by_hash(doc_hash)

    if doc_record and doc_record.get("faiss_index") and doc_record.get("metadata"):
        index, chunks = load_faiss_index_and_metadata_from_db(doc_hash)
    else:
        text = parse_file(file_path)
        chunks = chunk_text(text)
        embeddings = get_embeddings_for_chunks(chunks)
        index = faiss.IndexFlatL2(len(embeddings[0]))
        index.add(np.array(embeddings, dtype=np.float32))
        save_faiss_index_and_metadata_to_db(doc_hash, payload.documents, index, chunks)

    async def process_question(question: str):
        top_chunks = semantic_search_in_memory(question, index, chunks)
        return await answer_question(question, top_chunks)

    tasks = [process_question(q) for q in payload.questions]
    answers = await asyncio.gather(*tasks)
    return HackRxResponse(answers=answers)
