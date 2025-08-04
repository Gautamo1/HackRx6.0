# import pdfplumber
# import docx

# def parse_pdf(path: str) -> str:
#     text = ""
#     with pdfplumber.open(path) as pdf:
#         for page in pdf.pages:
#             page_text = page.extract_text()
#             if page_text:
#                 text += page_text + "\n"
#     return text.strip()

# def parse_docx(path: str) -> str:
#     doc = docx.Document(path)
#     return "\n".join([para.text for para in doc.paragraphs if para.text.strip()])

# def parse_file(path: str) -> str:
#     if path.endswith(".pdf"):
#         return parse_pdf(path)
#     elif path.endswith(".docx"):
#         return parse_docx(path)
#     else:
#         raise ValueError("Unsupported file type. Only PDF and DOCX are supported.")


# import pdfplumber
# import docx

# def parse_pdf(path: str) -> str:
#     """Extract text from a PDF file using pdfplumber."""
#     text = ""
#     with pdfplumber.open(path) as pdf:
#         for page in pdf.pages:
#             page_text = page.extract_text()
#             if page_text:
#                 text += page_text + "\n"
#     return text.strip()

# def parse_docx(path: str) -> str:
#     """Extract text from a DOCX file using python-docx."""
#     doc = docx.Document(path)
#     return "\n".join(para.text.strip() for para in doc.paragraphs if para.text.strip())

# def parse_file(path: str) -> str:
#     """
#     Parse a file and return its text content.

#     Supported formats:
#     - PDF
#     - DOCX
#     """
#     if path.lower().endswith(".pdf"):
#         return parse_pdf(path)
#     elif path.lower().endswith(".docx"):
#         return parse_docx(path)
#     else:
#         raise ValueError(f"Unsupported file type: {path}. Only PDF and DOCX are supported.")


import os
import hashlib
import pdfplumber
import mammoth
from concurrent.futures import ThreadPoolExecutor

CACHE_DIR = "cache"
os.makedirs(CACHE_DIR, exist_ok=True)

def get_file_hash(path: str) -> str:
    """Compute SHA-256 hash of file for caching purposes."""
    sha256 = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(8192):
            sha256.update(chunk)
    return sha256.hexdigest()

def parse_pdf(path: str) -> str:
    """Extract text from a PDF file using pdfplumber with parallelism."""
    with pdfplumber.open(path) as pdf:
        def extract(page):
            if not page.chars:  # Skip empty pages
                return ""
            return page.extract_text() or ""
        
        with ThreadPoolExecutor() as executor:
            results = list(executor.map(extract, pdf.pages))
        
        return "\n".join(filter(None, results)).strip()

def parse_docx(path: str) -> str:
    """Extract text from a DOCX file using mammoth (fast & clean)."""
    with open(path, "rb") as docx_file:
        result = mammoth.extract_raw_text(docx_file)
    return result.value.strip()

def parse_file(path: str) -> str:
    """
    Parse a file and return its text content. Uses SHA-based caching.

    Supported formats:
    - PDF
    - DOCX
    """
    file_hash = get_file_hash(path)
    cache_path = os.path.join(CACHE_DIR, f"{file_hash}.txt")

    # Use cache if available
    if os.path.exists(cache_path):
        with open(cache_path, "r", encoding="utf-8") as f:
            return f.read()

    # Parse based on file type
    if path.lower().endswith(".pdf"):
        parsed_text = parse_pdf(path)
    elif path.lower().endswith(".docx"):
        parsed_text = parse_docx(path)
    else:
        raise ValueError(f"Unsupported file type: {path}. Only PDF and DOCX are supported.")

    # Save to cache
    with open(cache_path, "w", encoding="utf-8") as f:
        f.write(parsed_text)

    return parsed_text
