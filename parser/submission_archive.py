"""
OpenLLMWorks Submission Archive Utilities

Provides shared inspection and safe extraction for OpenLLMWorks
benchmark submission ZIP archives.

This module handles archive safety only. It does not perform canonical
benchmark submission validation. Extracted submissions must still pass
the canonical parser.validate workflow before they are trusted.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path, PurePosixPath
import shutil
import stat
import zipfile


MAX_ARCHIVE_BYTES = 10 * 1024 * 1024
MAX_UNCOMPRESSED_BYTES = 25 * 1024 * 1024
MAX_FILE_COUNT = 100
SUBMISSION_MANIFEST_FILE = "submission.json"


class SubmissionArchiveError(Exception):
    """Raised when a submission archive is invalid or unsafe."""


@dataclass(frozen=True)
class SubmissionArchiveResult:
    """Result returned after safe submission archive extraction."""

    archive_path: Path
    extract_root: Path
    submission_dir: Path
    archive_size: int
    uncompressed_size: int
    entry_count: int


def _normalized_member_path(
    member: zipfile.ZipInfo,
) -> PurePosixPath:
    """Return a platform-neutral ZIP member path."""

    normalized_name = member.filename.replace("\\", "/")
    return PurePosixPath(normalized_name)


def _validate_member_path(
    member: zipfile.ZipInfo,
    extract_root: Path,
) -> None:
    """Validate one ZIP member before extraction."""

    member_path = _normalized_member_path(member)

    if member_path.is_absolute():
        raise SubmissionArchiveError(
            f"Unsafe absolute archive path: {member.filename}"
        )

    if ".." in member_path.parts:
        raise SubmissionArchiveError(
            f"Unsafe parent traversal path: {member.filename}"
        )

    if member_path.parts and ":" in member_path.parts[0]:
        raise SubmissionArchiveError(
            f"Unsafe drive-qualified path: {member.filename}"
        )

    unix_mode = member.external_attr >> 16

    if stat.S_ISLNK(unix_mode):
        raise SubmissionArchiveError(
            f"Symbolic links are not allowed: {member.filename}"
        )

    destination = (
        extract_root
        / Path(*member_path.parts)
    ).resolve()

    try:
        destination.relative_to(extract_root)
    except ValueError as error:
        raise SubmissionArchiveError(
            f"Archive path escapes extraction root: {member.filename}"
        ) from error


def _extract_member(
    archive: zipfile.ZipFile,
    member: zipfile.ZipInfo,
    extract_root: Path,
) -> None:
    """
    Extract one ZIP member using its normalized platform-neutral path.

    ZIP archives created on Windows may contain backslashes in member
    names. Those separators must be normalized explicitly so extraction
    produces the same directory structure on Windows and Linux.
    """

    member_path = _normalized_member_path(member)

    destination = (
        extract_root
        / Path(*member_path.parts)
    )

    if member.is_dir() or member.filename.endswith(("/", "\\")):
        destination.mkdir(
            parents=True,
            exist_ok=True,
        )
        return

    destination.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with archive.open(member, "r") as source:
        with destination.open("wb") as target:
            shutil.copyfileobj(
                source,
                target,
            )


def extract_submission_archive(
    archive_path: Path,
    extract_root: Path,
) -> SubmissionArchiveResult:
    """
    Safely inspect and extract one OpenLLMWorks submission ZIP.

    The archive must satisfy the OpenLLMWorks intake safety limits and
    contain exactly one submission.json file.

    Existing extraction directories are never overwritten.
    """

    archive_path = archive_path.expanduser().resolve()
    extract_root = extract_root.expanduser().resolve()

    if not archive_path.exists():
        raise SubmissionArchiveError(
            f"Submission ZIP was not found: {archive_path}"
        )

    if not archive_path.is_file():
        raise SubmissionArchiveError(
            f"Submission ZIP is not a file: {archive_path}"
        )

    archive_size = archive_path.stat().st_size

    if archive_size <= 0:
        raise SubmissionArchiveError(
            "Submission ZIP is empty."
        )

    if archive_size > MAX_ARCHIVE_BYTES:
        raise SubmissionArchiveError(
            "Submission ZIP exceeds "
            f"{MAX_ARCHIVE_BYTES} byte archive limit."
        )

    if extract_root.exists():
        raise SubmissionArchiveError(
            "Extraction destination already exists. "
            f"Nothing was overwritten: {extract_root}"
        )

    try:
        with zipfile.ZipFile(archive_path, "r") as archive:
            members = archive.infolist()

            if not members:
                raise SubmissionArchiveError(
                    "Submission ZIP contains no files."
                )

            if len(members) > MAX_FILE_COUNT:
                raise SubmissionArchiveError(
                    "Submission ZIP contains too many entries: "
                    f"{len(members)}."
                )

            total_uncompressed = sum(
                member.file_size
                for member in members
            )

            if total_uncompressed > MAX_UNCOMPRESSED_BYTES:
                raise SubmissionArchiveError(
                    "Submission ZIP exceeds the allowed "
                    "uncompressed size."
                )

            for member in members:
                _validate_member_path(
                    member,
                    extract_root,
                )

            extract_root.mkdir(
                parents=True,
                exist_ok=False,
            )

            for member in members:
                _extract_member(
                    archive,
                    member,
                    extract_root,
                )

    except zipfile.BadZipFile as error:
        if extract_root.exists():
            shutil.rmtree(
                extract_root,
                ignore_errors=True,
            )

        raise SubmissionArchiveError(
            "Submission file is not a valid ZIP archive."
        ) from error

    except Exception:
        if extract_root.exists():
            shutil.rmtree(
                extract_root,
                ignore_errors=True,
            )

        raise

    manifests = list(
        extract_root.rglob(
            SUBMISSION_MANIFEST_FILE
        )
    )

    if len(manifests) != 1:
        shutil.rmtree(
            extract_root,
            ignore_errors=True,
        )

        raise SubmissionArchiveError(
            "Expected exactly one submission.json after extraction; "
            f"found {len(manifests)}."
        )

    submission_dir = manifests[0].parent.resolve()

    return SubmissionArchiveResult(
        archive_path=archive_path,
        extract_root=extract_root,
        submission_dir=submission_dir,
        archive_size=archive_size,
        uncompressed_size=total_uncompressed,
        entry_count=len(members),
    )