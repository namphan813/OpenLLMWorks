"""
OpenLLMBench Backup Utility

Purpose:
Creates verified backups of the benchmark database.

Version:
0.1.0
"""

from datetime import datetime, timezone
from pathlib import Path
from shutil import copy2
import time

from utilities.hashes import sha256_file


BACKUP_UTILITY_VERSION = "0.1.0"


def timestamp_filename() -> str:
    """
    Build a UTC timestamp suitable for filenames.
    """

    return datetime.now(
        timezone.utc
    ).strftime("%Y%m%d_%H%M%SZ")


def create_verified_backup(
    source_database: Path,
    backup_directory: Path,
) -> dict:
    """
    Create a verified backup.

    Returns a report dictionary describing the operation.
    """

    start = time.perf_counter()

    backup_directory.mkdir(
        parents=True,
        exist_ok=True,
    )

    backup_name = (
        f"{source_database.stem}_"
        f"{timestamp_filename()}"
        f"{source_database.suffix}"
    )

    backup_file = (
        backup_directory / backup_name
    )

    copy2(
        source_database,
        backup_file,
    )

    source_hash = sha256_file(
        source_database
    )

    backup_hash = sha256_file(
        backup_file
    )

    verified = (
        source_hash == backup_hash
    )

    duration = (
        time.perf_counter()
        - start
    )

    return {
        "success": verified,
        "backup_created": (
            backup_file.exists()
        ),
        "backup_verified": verified,
        "source_file": str(
            source_database
        ),
        "backup_file": str(
            backup_file
        ),
        "source_sha256": source_hash,
        "backup_sha256": backup_hash,
        "duration_seconds": round(
            duration,
            3,
        ),
        "utility_version": (
            BACKUP_UTILITY_VERSION
        ),
    }