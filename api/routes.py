# from fastapi import APIRouter
# from pydantic import BaseModel
# from typing import List
# from utils.downloader import download_file_from_url
# from utils.parser import parse_file
# from utils.chunker import chunk_text
# from utils.embedder import get_embeddings_for_chunks
# from utils.file_store import save_faiss_index, save_metadata
# from utils.searcher import semantic_search
# from utils.gemini_llm import answer_question
# from utils.utils import get_file_hash
# import os
# import faiss
# import numpy as np

# router = APIRouter()


# # ---------------------------
# # /hackrx/run Endpoint
# # ---------------------------

# class HackRxInput(BaseModel):
#     documents: str
#     questions: List[str]

# class HackRxResponse(BaseModel):
#     answers: List[str]

# @router.post("/run", response_model=HackRxResponse)
# def run_endpoint(payload: HackRxInput):
#     file_path = download_file_from_url(payload.documents)
#     text = parse_file(file_path)
#     chunks = chunk_text(text)
#     embeddings = get_embeddings_for_chunks(chunks)

#     doc_hash = get_file_hash(file_path)
#     index_path = os.path.join("faiss_store", f"{doc_hash}.index.faiss")
#     json_path = os.path.join("faiss_store", f"{doc_hash}.chunks.json")

#     os.makedirs("faiss_store", exist_ok=True)
#     index = faiss.IndexFlatL2(len(embeddings[0]))
#     index.add(np.array(embeddings, dtype=np.float32))
#     save_faiss_index(index, index_path)
#     save_metadata(chunks, json_path)

#     answers = []
#     for question in payload.questions:
#         results = semantic_search(question, index_path, json_path)
#         answer = answer_question(question, results)
#         answers.append(answer)

#     return {"answers": answers}


# from fastapi import APIRouter
# from pydantic import BaseModel
# from typing import List
# import os
# import faiss
# import numpy as np

# from utils.downloader import download_file_from_url
# from utils.parser import parse_file
# from utils.chunker import chunk_text
# from utils.embedder import get_embeddings_for_chunks
# from utils.file_store import save_faiss_index, save_metadata, load_faiss_index, load_metadata
# from utils.searcher import semantic_search
# from utils.gemini_llm import answer_question
# from utils.utils import get_file_hash
# from utils.db_utils import init_db, get_document_by_hash, insert_document

# # Initialize the router
# router = APIRouter()
# init_db()  # Ensure database is ready

# # ----- Request and Response Schemas -----
# class HackRxInput(BaseModel):
#     documents: str  # URL
#     questions: List[str]

# class HackRxResponse(BaseModel):
#     answers: List[str]

# # ----- Main Endpoint -----
# @router.post("/run", response_model=HackRxResponse)
# def run_endpoint(payload: HackRxInput):
#     # Step 1: Download and hash the document
#     file_path = download_file_from_url(payload.documents)
#     doc_hash = get_file_hash(file_path)

#     # Step 2: Check if FAISS index already exists in DB
#     doc_record = get_document_by_hash(doc_hash)
#     if doc_record:
#         index_path = doc_record['faiss_index_path']
#         json_path = doc_record['metadata_path']
#     else:
#         # Step 3: Process new document
#         text = parse_file(file_path)
#         chunks = chunk_text(text)
#         embeddings = get_embeddings_for_chunks(chunks)

#         # Step 4: Store FAISS index + metadata
#         os.makedirs("faiss_store", exist_ok=True)
#         index_path = os.path.join("faiss_store", f"{doc_hash}.index.faiss")
#         json_path = os.path.join("faiss_store", f"{doc_hash}.chunks.json")

#         index = faiss.IndexFlatL2(len(embeddings[0]))
#         index.add(np.array(embeddings, dtype=np.float32))

#         save_faiss_index(index, index_path)
#         save_metadata(chunks, json_path)

#         insert_document(doc_hash, payload.documents, index_path, json_path)

#     # Step 5: Answer each question
#     answers = []
#     for question in payload.questions:
#         top_chunks = semantic_search(question, index_path, json_path)
#         answer = answer_question(question, top_chunks)
#         answers.append(answer)

#     return HackRxResponse(answers=answers)


from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import List
import faiss
import numpy as np

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
def run_endpoint(payload: HackRxInput):
    file_path = download_file_from_url(payload.documents)
    doc_hash = get_file_hash(file_path)

    doc_record = get_document_by_hash(doc_hash)
    if doc_record and doc_record.get("faiss_index") and doc_record.get("metadata"):
        index, chunks = load_faiss_index_and_metadata_from_db(doc_hash)
    else:
        # Pipeline: parse → chunk → embed → index → store
        text = parse_file(file_path)
        chunks = chunk_text(text)
        embeddings = get_embeddings_for_chunks(chunks)

        index = faiss.IndexFlatL2(len(embeddings[0]))
        index.add(np.array(embeddings, dtype=np.float32))

        # Save into database instead of files
        save_faiss_index_and_metadata_to_db(doc_hash, payload.documents, index, chunks)

    answers = []
    for question in payload.questions:
        top_chunks = semantic_search_in_memory(question, index, chunks)
        answer = answer_question(question, top_chunks)
        answers.append(answer)

    return HackRxResponse(answers=answers)
