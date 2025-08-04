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


from typing import List

def chunk_text(text: str, max_words: int = 250, overlap: int = 20) -> List[str]:
    """
    Split text into overlapping chunks for embedding.

    Args:
        text (str): The full input text.
        max_words (int): Maximum words per chunk.
        overlap (int): Number of words to overlap between chunks.

    Returns:
        List[str]: List of chunked strings.
    """
    if max_words <= overlap:
        raise ValueError("max_words must be greater than overlap")

    words = text.split()
    step = max_words - overlap

    return [
        " ".join(words[i:i + max_words]).strip()
        for i in range(0, len(words), step)
    ]

