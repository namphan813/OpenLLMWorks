"""
OpenLLMBench Hash Utilities

Purpose:
Provides reusable hashing functions used throughout
OpenLLMBench.

Version:
0.1.0
"""

from hashlib import sha256
from pathlib import Path


def sha256_file(
    file_path: Path,
) -> str:
    """
    Calculate the SHA-256 hash of a file.
    """

    digest = sha256()

    with file_path.open("rb") as file:

        while True:

            chunk = file.read(65536)

            if not chunk:
                break

            digest.update(chunk)

    return digest.hexdigest()