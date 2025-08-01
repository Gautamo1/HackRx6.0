import hashlib

def get_file_hash(filepath: str) -> str:
    """Returns a SHA256 hash of the file content."""
    sha256 = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(8192):
            sha256.update(chunk)
    return sha256.hexdigest()
