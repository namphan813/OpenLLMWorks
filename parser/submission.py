"""
OpenLLMBench Submission Model

Purpose:
Represents benchmark submission directories, discovers
submissions placed in the incoming folder, and performs
lightweight structural preflight validation.

Version:
0.6.0-dev3
"""

from dataclasses import dataclass
from pathlib import Path


SUBMISSION_MODULE_VERSION = "0.6.0-dev3"


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
class SubmissionPreflightResult:
    """
    Structural validation result for one submission package.

    Preflight validation is intentionally lightweight.

    It checks whether the submission contains the minimum
    expected files required before deeper parsing begins.
    """

    valid: bool
    errors: tuple[str, ...]
    warnings: tuple[str, ...]
    benchmark_files: tuple[Path, ...]


def validate_submission_preflight(
    submission: Submission,
) -> SubmissionPreflightResult:
    """
    Validate the structure of one submission directory.

    Preflight checks intentionally avoid parsing file contents.

    Fatal errors:
    - Required hardware evidence file is missing.
    - No benchmark run files are present.

    Warnings:
    - Fewer than three benchmark run files are present.
    """

    errors: list[str] = []
    warnings: list[str] = []

    for file_name in REQUIRED_HARDWARE_FILES:
        file_path = submission.source_path / file_name

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

    return SubmissionPreflightResult(
        valid=not errors,
        errors=tuple(errors),
        warnings=tuple(warnings),
        benchmark_files=benchmark_files,
    )


def discover_submissions(
    incoming_folder: Path,
) -> list[Submission]:
    """
    Find every submission directory inside the incoming folder.

    Files directly inside incoming are ignored. Only immediate
    child directories are treated as submissions.
    """

    incoming_folder = incoming_folder.resolve()

    if not incoming_folder.exists():
        incoming_folder.mkdir(
            parents=True,
            exist_ok=True,
        )

        return []

    if not incoming_folder.is_dir():
        raise NotADirectoryError(
            f"Incoming path is not a directory: {incoming_folder}"
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