"""
OpenLLMBench Submission Model

Purpose:
Represents benchmark submission directories and discovers
submissions placed in the incoming folder.

Version:
0.6.0-dev2
"""

from dataclasses import dataclass
from pathlib import Path


SUBMISSION_MODULE_VERSION = "0.6.0-dev2"


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