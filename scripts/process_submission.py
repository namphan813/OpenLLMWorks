"""
OpenLLMBench Maintainer Submission Workflow

Purpose:
Process one extracted OpenLLMBench submission through the existing
canonical maintainer pipeline:

1. Validate the source submission.
2. Copy it into the repository incoming directory.
3. Import exactly that staged submission with trusted provenance.
4. Publish updated website data.

This script is intentionally a thin orchestrator. It does not
reimplement submission validation, benchmark parsing, database
ingestion, or publishing logic.
"""

from __future__ import annotations

import argparse
from pathlib import Path
import shutil
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]
INCOMING_DIR = ROOT / "incoming"


def build_argument_parser() -> argparse.ArgumentParser:
    """Build the maintainer workflow command-line interface."""

    parser = argparse.ArgumentParser(
        description=(
            "Validate, stage, import, and publish one "
            "OpenLLMBench submission."
        )
    )

    parser.add_argument(
        "submission_path",
        type=Path,
        help=(
            "Path to one extracted OpenLLMBench submission "
            "directory."
        ),
    )

    parser.add_argument(
        "--source-type",
        required=True,
        help="Trusted submission source type.",
    )

    parser.add_argument(
        "--contributor-id",
        required=True,
        help="Trusted contributor identifier.",
    )

    parser.add_argument(
        "--contributor-type",
        required=True,
        help="Trusted contributor type.",
    )

    parser.add_argument(
        "--verification-status",
        required=True,
        help="Maintainer-assigned verification status.",
    )

    return parser


def run_command(
    command: list[str],
    phase_name: str,
) -> bool:
    """
    Run one canonical OpenLLMBench CLI command.

    Returns True when the command exits successfully.
    """

    completed = subprocess.run(
        command,
        cwd=ROOT,
    )

    if completed.returncode != 0:
        print()
        print(
            f"[FAIL] {phase_name} exited with code "
            f"{completed.returncode}."
        )
        return False

    return True


def resolve_source_path(
    submission_path: Path,
) -> Path:
    """Resolve and verify the source submission directory."""

    source_path = submission_path.expanduser().resolve()

    if not source_path.exists():
        raise FileNotFoundError(
            "Submission path was not found: "
            f"{source_path}"
        )

    if not source_path.is_dir():
        raise NotADirectoryError(
            "Submission path is not a directory: "
            f"{source_path}"
        )

    return source_path


def stage_submission(
    source_path: Path,
) -> Path:
    """
    Copy one validated submission into incoming/.

    Existing destinations are never overwritten.
    """

    INCOMING_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    destination = (
        INCOMING_DIR
        / source_path.name
    )

    if destination.exists():
        raise FileExistsError(
            "Staging destination already exists. "
            "Nothing was overwritten: "
            f"{destination}"
        )

    shutil.copytree(
        source_path,
        destination,
    )

    return destination


def main() -> int:
    """Run the single-submission maintainer workflow."""

    parser = build_argument_parser()
    args = parser.parse_args()

    print()
    print("OpenLLMBench Maintainer Workflow")
    print("=" * 60)
    print()

    try:
        source_path = resolve_source_path(
            args.submission_path
        )
    except (
        FileNotFoundError,
        NotADirectoryError,
    ) as error:
        print(f"[FAIL] {error}")
        return 1

    print("Source submission:")
    print(source_path)
    print()

    print("[1/4] Validate submission")
    print("-" * 60)

    validation_command = [
        sys.executable,
        "-m",
        "parser.validate",
        str(source_path),
    ]

    if not run_command(
        validation_command,
        "Submission validation",
    ):
        print()
        print(
            "Workflow stopped before staging or database "
            "modification."
        )
        return 1

    print()
    print("[PASS] Submission validation")
    print()

    print("[2/4] Stage submission")
    print("-" * 60)

    try:
        staged_path = stage_submission(
            source_path
        )
    except (
        FileExistsError,
        OSError,
    ) as error:
        print(f"[FAIL] {error}")
        print()
        print(
            "Workflow stopped before database import."
        )
        return 1

    print(f"[PASS] Copied to {staged_path}")
    print()

    print("[3/4] Import submission")
    print("-" * 60)

    import_command = [
        sys.executable,
        "-m",
        "parser.parser",
        "--submission",
        staged_path.name,
        "--source-type",
        args.source_type,
        "--contributor-id",
        args.contributor_id,
        "--contributor-type",
        args.contributor_type,
        "--verification-status",
        args.verification_status,
    ]

    if not run_command(
        import_command,
        "Submission import",
    ):
        print()
        print(
            "Workflow stopped before publishing."
        )
        print(
            "The staged submission remains available at:"
        )
        print(staged_path)
        return 1

    print()
    print("[PASS] Submission import")
    print()

    print("[4/4] Publish website data")
    print("-" * 60)

    publish_command = [
        sys.executable,
        "-m",
        "publisher.generate_site",
    ]

    if not run_command(
        publish_command,
        "Website publishing",
    ):
        print()
        print(
            "The database import completed, but publishing "
            "did not complete successfully."
        )
        print(
            "Review the publisher output above before "
            "continuing."
        )
        return 1

    print()
    print("[PASS] Website publishing")
    print()
    print("=" * 60)
    print("Maintainer workflow completed successfully.")
    print("=" * 60)
    print()
    print("Staged submission:")
    print(staged_path)
    print()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
