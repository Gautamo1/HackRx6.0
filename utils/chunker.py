# def chunk_text(text: str, max_words: int = 100, overlap: int = 20) -> list:
#     words = text.split()
#     chunks = []

#     i = 0
#     while i < len(words):
#         chunk = words[i:i + max_words]
#         chunks.append(" ".join(chunk))
#         i += max_words - overlap  # Slide window with overlap

#     return chunks

# def chunk_text(text: str, max_words: int = 100, overlap: int = 20) -> list:
#     words = text.split()
#     step = max_words - overlap
#     return [
#         " ".join(words[i:i + max_words])
#         for i in range(0, len(words), step)
#     ]


import re
from typing import List

try:
    import nltk
    from nltk.tokenize import sent_tokenize

    try:
        nltk.data.find("tokenizers/punkt")
    except LookupError:
        nltk.download("punkt", quiet=True)
    try:
        nltk.data.find("tokenizers/punkt_tab")
    except LookupError:
        nltk.download("punkt_tab", quiet=True)
except Exception:
    sent_tokenize = None


def _split_sentences(text: str) -> List[str]:
    if sent_tokenize is not None:
        try:
            return [sentence.strip() for sentence in sent_tokenize(text) if sentence.strip()]
        except Exception:
            pass
    return [sentence.strip() for sentence in re.split(r"(?<=[.!?])\s+", text) if sentence.strip()]


def chunk_text(text: str, max_words: int = 250, overlap: int = 1) -> List[str]:
    """
    Split text into overlapping chunks for embedding.

    Args:
        text (str): The full input text.
        max_words (int): Maximum words per chunk.
        overlap (int): Number of trailing sentences to overlap between chunks.

    Returns:
        List[str]: List of chunked strings.
    """
    if max_words <= overlap:
        raise ValueError("max_words must be greater than overlap")

    if max_words <= 0 or overlap < 0:
        raise ValueError("max_words must be positive and overlap cannot be negative")

    sentences = _split_sentences(text)
    chunks = []
    current_sentences = []
    current_word_count = 0

    for sentence in sentences:
        sentence_word_count = len(sentence.split())
        if current_sentences and current_word_count + sentence_word_count > max_words:
            chunks.append(" ".join(current_sentences).strip())
            current_sentences = current_sentences[-overlap:] if overlap else []
            current_word_count = sum(len(item.split()) for item in current_sentences)

        current_sentences.append(sentence)
        current_word_count += sentence_word_count

    if current_sentences:
        chunks.append(" ".join(current_sentences).strip())

    return chunks

