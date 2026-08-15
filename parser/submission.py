"""
OpenLLMBench Submission Model

Purpose:
Represents benchmark submission directories, discovers
submissions placed in the incoming folder, performs
lightweight structural preflight validation, and reads
optional submission metadata manifests.

Version:
0.6.0-dev4
"""

from dataclasses import dataclass
from datetime import datetime
import json
from pathlib import Path
from typing import Any


SUBMISSION_MODULE_VERSION = "0.6.0-dev4"

SUBMISSION_MANIFEST_FILE = "submission.json"
SUPPORTED_MANIFEST_SCHEMA_VERSION = "1.0"

REQUIRED_HARDWARE_FILES = (
    "cpu.txt",
    "memory.txt",
    "system.txt",
    "windows.txt",
    "nvidia-smi.txt",
)


@dataclass(frozen=True)
class Submission:
    """Represents one benchmark submission directory."""

    source_path: Path
    submission_name: str

    @classmethod
    def from_path(cls, source_path: Path) -> "Submission":
        """
        Create a Submission from an existing directory.
        """

        source_path = source_path.resolve()

        if not source_path.exists():
            raise FileNotFoundError(
                f"Submission path does not exist: {source_path}"
            )

        if not source_path.is_dir():
            raise NotADirectoryError(
                f"Submission path is not a directory: {source_path}"
            )

        return cls(
            source_path=source_path,
            submission_name=source_path.name,
        )


@dataclass(frozen=True)
class SubmissionManifest:
    """
    Contributor-provided metadata for one submission.

    Hardware identity and benchmark measurements are
    intentionally excluded from the manifest because their
    authoritative values come from preserved evidence files.
    """

    schema_version: str
    submission_name: str
    submitted_at: str
    benchmark_timestamp: str


@dataclass(frozen=True)
class SubmissionPreflightResult:
    """
    Structural validation result for one submission package.

    Preflight validation checks the minimum package structure
    required before deeper parsing begins.

    Legacy submissions without submission.json remain valid.
    If submission.json is present, it must be valid.
    """

    valid: bool
    errors: tuple[str, ...]
    warnings: tuple[str, ...]
    benchmark_files: tuple[Path, ...]
    manifest: SubmissionManifest | None


def _validate_timestamp(
    value: Any,
    field_name: str,
) -> str:
    """
    Validate one ISO-8601 timestamp string.

    UTC timestamps ending in Z are supported.
    """

    if not isinstance(value, str) or not value.strip():
        raise ValueError(
            f"Manifest field '{field_name}' must be "
            "a non-empty timestamp string."
        )

    normalized_value = value.strip()

    try:
        datetime.fromisoformat(
            normalized_value.replace(
                "Z",
                "+00:00",
            )
        )

    except ValueError as error:
        raise ValueError(
            f"Manifest field '{field_name}' is not "
            f"a valid ISO-8601 timestamp: "
            f"{normalized_value}"
        ) from error

    return normalized_value


def load_submission_manifest(
    submission: Submission,
) -> SubmissionManifest | None:
    """
    Load and validate an optional submission.json manifest.

    Returns None when the manifest does not exist so historical
    submissions remain compatible with the current pipeline.

    Raises:
        ValueError:
            If submission.json exists but is malformed or
            contains invalid manifest fields.
    """

    manifest_path = (
        submission.source_path
        / SUBMISSION_MANIFEST_FILE
    )

    if not manifest_path.exists():
        return None

    if not manifest_path.is_file():
        raise ValueError(
            f"{SUBMISSION_MANIFEST_FILE} exists but "
            "is not a file."
        )

    try:
        manifest_data = json.loads(
            manifest_path.read_text(
                encoding="utf-8"
            )
        )

    except json.JSONDecodeError as error:
        raise ValueError(
            f"{SUBMISSION_MANIFEST_FILE} contains "
            f"invalid JSON: {error}"
        ) from error

    if not isinstance(manifest_data, dict):
        raise ValueError(
            f"{SUBMISSION_MANIFEST_FILE} root must "
            "be a JSON object."
        )

    schema_version = manifest_data.get(
        "schema_version"
    )

    if (
        not isinstance(schema_version, str)
        or schema_version
        != SUPPORTED_MANIFEST_SCHEMA_VERSION
    ):
        raise ValueError(
            "Unsupported submission manifest schema "
            f"version: {schema_version!r}. "
            "Expected "
            f"{SUPPORTED_MANIFEST_SCHEMA_VERSION!r}."
        )

    submission_name = manifest_data.get(
        "submission_name"
    )

    if (
        not isinstance(submission_name, str)
        or not submission_name.strip()
    ):
        raise ValueError(
            "Manifest field 'submission_name' must "
            "be a non-empty string."
        )

    submitted_at = _validate_timestamp(
        manifest_data.get("submitted_at"),
        "submitted_at",
    )

    benchmark_timestamp = _validate_timestamp(
        manifest_data.get(
            "benchmark_timestamp"
        ),
        "benchmark_timestamp",
    )

    return SubmissionManifest(
        schema_version=schema_version,
        submission_name=submission_name.strip(),
        submitted_at=submitted_at,
        benchmark_timestamp=benchmark_timestamp,
    )


def validate_submission_preflight(
    submission: Submission,
) -> SubmissionPreflightResult:
    """
    Validate the structure of one submission directory.

    Fatal errors:
    - Required hardware evidence file is missing.
    - No benchmark run files are present.
    - submission.json exists but is malformed or invalid.

    Warnings:
    - Fewer than three benchmark run files are present.
    - submission.json is absent and legacy folder-based
      submission identity will be used.
    """

    errors: list[str] = []
    warnings: list[str] = []

    for file_name in REQUIRED_HARDWARE_FILES:
        file_path = (
            submission.source_path
            / file_name
        )

        if not file_path.is_file():
            errors.append(
                f"Missing required file: {file_name}"
            )

    benchmark_files = tuple(
        sorted(
            submission.source_path.glob(
                "benchmark*-run*.txt"
            )
        )
    )

    if not benchmark_files:
        errors.append(
            "No benchmark run files were found."
        )

    elif len(benchmark_files) < 3:
        warnings.append(
            "Fewer than 3 benchmark run files were found "
            f"({len(benchmark_files)} present)."
        )

    manifest: SubmissionManifest | None = None
    manifest_path = (
        submission.source_path
        / SUBMISSION_MANIFEST_FILE
    )

    try:
        manifest = load_submission_manifest(
            submission
        )

    except ValueError as error:
        errors.append(str(error))

    if not manifest_path.exists():
        warnings.append(
            "submission.json was not found; "
            "legacy folder-based submission metadata "
            "will be used."
        )

    return SubmissionPreflightResult(
        valid=not errors,
        errors=tuple(errors),
        warnings=tuple(warnings),
        benchmark_files=benchmark_files,
        manifest=manifest,
    )


def discover_submissions(
    incoming_folder: Path,
) -> list[Submission]:
    """
    Find every submission directory inside the incoming folder.

    Files directly inside incoming are ignored. Only immediate
    child directories are treated as submissions.
    """

    incoming_folder = (
        incoming_folder.resolve()
    )

    if not incoming_folder.exists():
        incoming_folder.mkdir(
            parents=True,
            exist_ok=True,
        )

        return []

    if not incoming_folder.is_dir():
        raise NotADirectoryError(
            f"Incoming path is not a directory: "
            f"{incoming_folder}"
        )

    submission_folders = sorted(
        folder
        for folder in incoming_folder.iterdir()
        if folder.is_dir()
        and not folder.name.startswith(".")
        and folder.name != "__pycache__"
    )

    return [
        Submission.from_path(folder)
        for folder in submission_folders
    ]