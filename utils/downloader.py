# import os
# import requests
# from urllib.parse import urlparse

# TMP_DIR = "tmp"

# def download_file_from_url(url: str) -> str:
#     os.makedirs(TMP_DIR, exist_ok=True)

#     parsed_url = urlparse(url)
#     filename = os.path.basename(parsed_url.path)
#     file_path = os.path.join(TMP_DIR, filename)

#     response = requests.get(url)
#     if response.status_code != 200:
#         raise Exception(f"Failed to download file: {url} - Status: {response.status_code}")

#     with open(file_path, "wb") as f:
#         f.write(response.content)

#     return file_path


import os
import requests
from urllib.parse import urlparse

TMP_DIR = "tmp"

def download_file_from_url(url: str) -> str:
    os.makedirs(TMP_DIR, exist_ok=True)

    parsed_url = urlparse(url)
    filename = os.path.basename(parsed_url.path) or "downloaded_file"
    file_path = os.path.join(TMP_DIR, filename)

    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()
    except requests.RequestException as e:
        raise RuntimeError(f"Failed to download file from {url}") from e

    with open(file_path, "wb") as f:
        f.write(response.content)

    print(f"📥 File downloaded to {file_path}")
    return file_path
