"""
OpenLLMWorks Direct Submission Maintainer Workflow

Purpose:
Process one downloaded Direct Submission ZIP through the existing
OpenLLMWorks maintainer pipeline.

Workflow:

1. Safely inspect and extract the submission archive.
2. Run canonical submission validation.
3. Present the submission to the maintainer for approval.
4. Hand the extracted submission to process_submission.py.
5. Preserve the existing canonical stage/import/publish workflow.

This script is intentionally a thin orchestrator. Archive safety,
canonical validation, database ingestion, and website publishing remain
owned by their existing OpenLLMWorks components.
"""

from __future__ import annotations

import argparse
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

from parser.submission_archive import (
    SubmissionArchiveError,
    extract_submission_archive,
)


ROOT = Path(__file__).resolve().parents[1]
PROCESS_SUBMISSION_SCRIPT = ROOT / "scripts" / "process_submission.py"


def build_argument_parser() -> argparse.ArgumentParser:
    """Build the Direct Submission maintainer CLI."""

    parser = argparse.ArgumentParser(
        description=(
            "Safely extract, validate, approve, import, and publish "
            "one downloaded OpenLLMWorks Direct Submission ZIP."
        )
    )

    parser.add_argument(
        "archive_path",
        type=Path,
        help="Path to one downloaded Direct Submission ZIP.",
    )

    return parser


def run_command(
    command: list[str],
    phase_name: str,
) -> bool:
    """Run one OpenLLMWorks command and report failure."""

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


def confirm_import() -> bool:
    """Request explicit maintainer approval before database import."""

    print()
    print("Maintainer approval required.")
    print(
        "This submission has passed archive safety checks "
        "and canonical validation."
    )
    print(
        "Approving will stage the submission, import it into "
        "the canonical database, and regenerate website data."
    )
    print()

    try:
        response = input("Approve this submission for import? [y/N]: ")
    except (EOFError, KeyboardInterrupt):
        print()
        print("Import cancelled.")
        return False

    return response.strip().lower() in {
        "y",
        "yes",
    }


def main() -> int:
    """Run the Direct Submission maintainer workflow."""

    parser = build_argument_parser()
    args = parser.parse_args()

    archive_path = args.archive_path.expanduser().resolve()

    print()
    print("OpenLLMWorks Direct Submission Workflow")
    print("=" * 60)
    print()
    print("Archive:")
    print(archive_path)
    print()

    temp_root = Path(
        tempfile.mkdtemp(
            prefix="OpenLLMWorks-direct-submission-"
        )
    )

    extract_root = temp_root / "extracted"

    try:
        print("[1/3] Inspect and safely extract archive")
        print("-" * 60)

        try:
            result = extract_submission_archive(
                archive_path,
                extract_root,
            )
        except SubmissionArchiveError as error:
            print(f"[FAIL] {error}")
            return 1

        print(f"[OK] Archive size: {result.archive_size} bytes")
        print(
            "[OK] Uncompressed size: "
            f"{result.uncompressed_size} bytes"
        )
        print(f"[OK] Archive entries: {result.entry_count}")
        print()
        print("Submission directory:")
        print(result.submission_dir)
        print()

        print("[2/3] Run canonical submission validation")
        print("-" * 60)

        validation_command = [
            sys.executable,
            "-m",
            "parser.validate",
            str(result.submission_dir),
        ]

        if not run_command(
            validation_command,
            "Canonical submission validation",
        ):
            print()
            print(
                "Workflow stopped before maintainer approval "
                "or database modification."
            )
            return 1

        print()
        print("[PASS] Canonical submission validation")

        if not confirm_import():
            print()
            print(
                "No database or published website data "
                "was modified."
            )
            return 0

        print()
        print("[3/3] Run canonical maintainer workflow")
        print("-" * 60)

        maintainer_command = [
            sys.executable,
            str(PROCESS_SUBMISSION_SCRIPT),
            str(result.submission_dir),
            "--source-type",
            "direct_submission",
            "--contributor-id",
            "founder_000001",
            "--contributor-type",
            "founder",
            "--verification-status",
            "maintainer_verified",
        ]

        if not run_command(
            maintainer_command,
            "Maintainer submission workflow",
        ):
            return 1

        print()
        print("=" * 60)
        print(
            "Direct Submission workflow completed successfully."
        )
        print("=" * 60)
        print()

        return 0

    finally:
        shutil.rmtree(
            temp_root,
            ignore_errors=True,
        )


if __name__ == "__main__":
    raise SystemExit(main())