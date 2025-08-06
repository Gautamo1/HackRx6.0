# from fastapi import APIRouter, Depends
# from pydantic import BaseModel
# from typing import List
# import faiss
# import numpy as np
# import asyncio

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
# async def run_endpoint(payload: HackRxInput):
#     file_path = download_file_from_url(payload.documents)
#     doc_hash = get_file_hash(file_path)
#     doc_record = get_document_by_hash(doc_hash)

#     if doc_record and doc_record.get("faiss_index") and doc_record.get("metadata"):
#         index, chunks = load_faiss_index_and_metadata_from_db(doc_hash)
#     else:
#         text = parse_file(file_path)
#         chunks = chunk_text(text)
#         embeddings = get_embeddings_for_chunks(chunks)
#         index = faiss.IndexFlatL2(len(embeddings[0]))
#         index.add(np.array(embeddings, dtype=np.float32))
#         save_faiss_index_and_metadata_to_db(doc_hash, payload.documents, index, chunks)

#     async def process_question(question: str):
#         top_chunks = semantic_search_in_memory(question, index, chunks)
#         return await answer_question(question, top_chunks)

#     tasks = [process_question(q) for q in payload.questions]
#     answers = await asyncio.gather(*tasks)
#     return HackRxResponse(answers=answers)


# from fastapi import APIRouter, Depends
# from pydantic import BaseModel
# from typing import List
# import faiss
# import numpy as np
# import asyncio
# import time

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

# # ⏱ Global lock and time tracking
# last_request_time = 0
# cooldown_lock = asyncio.Lock()
# COOLDOWN_SECONDS = 60  # ⏳ wait 60 seconds between full requests

# class HackRxInput(BaseModel):
#     documents: str
#     questions: List[str]

# class HackRxResponse(BaseModel):
#     answers: List[str]

# @router.post("/run", response_model=HackRxResponse, dependencies=[Depends(verify_token)])
# async def run_endpoint(payload: HackRxInput):
#     global last_request_time

#     # 👮‍♂️ Rate limit logic
#     async with cooldown_lock:
#         now = time.time()
#         elapsed = now - last_request_time
#         if elapsed < COOLDOWN_SECONDS:
#             wait_time = COOLDOWN_SECONDS - elapsed
#             print(f"Rate limit hit. Waiting for {wait_time:.2f} seconds...")
#             await asyncio.sleep(wait_time)
#         last_request_time = time.time()

#     # 📥 Download + Parse + Embed logic
#     file_path = download_file_from_url(payload.documents)
#     doc_hash = get_file_hash(file_path)
#     doc_record = get_document_by_hash(doc_hash)

#     if doc_record and doc_record.get("faiss_index") and doc_record.get("metadata"):
#         index, chunks = load_faiss_index_and_metadata_from_db(doc_hash)
#     else:
#         text = parse_file(file_path)
#         chunks = chunk_text(text)
#         embeddings = get_embeddings_for_chunks(chunks)
#         index = faiss.IndexFlatL2(len(embeddings[0]))
#         index.add(np.array(embeddings, dtype=np.float32))
#         save_faiss_index_and_metadata_to_db(doc_hash, payload.documents, index, chunks)

#     # 🤖 Answer questions concurrently
#     async def process_question(question: str):
#         top_chunks = semantic_search_in_memory(question, index, chunks)
#         return await answer_question(question, top_chunks)

#     tasks = [process_question(q) for q in payload.questions]
#     answers = await asyncio.gather(*tasks)

#     return HackRxResponse(answers=answers)


from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import List
import faiss
import numpy as np
import asyncio
import time
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

# ⏱ Global lock and rate-limiting state
last_request_time = 0
cooldown_lock = asyncio.Lock()
COOLDOWN_SECONDS = 30  # Change if needed

class HackRxInput(BaseModel):
    documents: str
    questions: List[str]

class HackRxResponse(BaseModel):
    answers: List[str]

@router.post("/run", response_model=HackRxResponse, dependencies=[Depends(verify_token)])
async def run_endpoint(payload: HackRxInput):
    global last_request_time

    # Record start of request
    request_start_time = time.time()

    # Lock and check cooldown
    async with cooldown_lock:
        now = time.time()
        elapsed = now - last_request_time

        if elapsed < COOLDOWN_SECONDS:
            wait_time = COOLDOWN_SECONDS - elapsed
            print(f"⏱️ Rate limit hit. Waiting {wait_time:.2f} seconds before starting...")
            await asyncio.sleep(wait_time)

        # Set the new last request time BEFORE processing starts
        last_request_time = time.time()

    # ✅ Start actual processing timer
    processing_start_time = time.time()

    # 📥 Download + Parse + Embed logic
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

    # 🤖 Answer questions concurrently
    async def process_question(question: str):
        top_chunks = semantic_search_in_memory(question, index, chunks)
        return await answer_question(question, top_chunks)

    tasks = [process_question(q) for q in payload.questions]
    answers = await asyncio.gather(*tasks)

    # ✅ End processing
    processing_end_time = time.time()
    total_processing_time = processing_end_time - processing_start_time

    # ⏳ Optional cooldown to fill remaining time
    remaining_wait = COOLDOWN_SECONDS - total_processing_time
    if remaining_wait > 0:
        print(f"⌛ Enforcing remaining cooldown of {remaining_wait:.2f} seconds...")
        await asyncio.sleep(remaining_wait)

    return HackRxResponse(answers=answers)
