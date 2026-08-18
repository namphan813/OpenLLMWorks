"""
OpenLLMBench Submission Validation CLI

Provides a contributor-facing command for validating a benchmark
submission package before it is submitted or imported.

Usage:

    py -m parser.validate .\\example_submission
"""

from __future__ import annotations

import argparse
from pathlib import Path

from .submission import (
    SUBMISSION_MANIFEST_FILE,
    Submission,
    validate_submission_preflight,
)


def build_argument_parser() -> argparse.ArgumentParser:
    """Build the command-line argument parser."""

    parser = argparse.ArgumentParser(
        description=(
            "Validate an OpenLLMBench benchmark submission package."
        )
    )

    parser.add_argument(
        "submission_path",
        type=Path,
        help="Path to the benchmark submission directory.",
    )

    return parser


def print_preflight_result(
    submission: Submission,
) -> bool:
    """
    Validate one submission and print a contributor-friendly report.

    Returns True when structural validation passes.
    """

    result = validate_submission_preflight(submission)

    print()
    print("OpenLLMBench Submission Validation")
    print("=" * 34)
    print()
    print(f"Submission: {submission.submission_name}")
    print(f"Path: {submission.source_path}")
    print()

    manifest_path = (
        submission.source_path
        / SUBMISSION_MANIFEST_FILE
    )
    manifest_exists = manifest_path.exists()

    if result.manifest is not None:
        print("[OK] submission.json")
        print(
            "[OK] Manifest schema "
            f"{result.manifest.schema_version}"
        )
    elif manifest_exists:
        print("[FAIL] submission.json")
    else:
        print(
            "[WARN] submission.json not present "
            "(legacy submission)"
        )

    required_file_count = 5 - sum(
        1
        for error in result.errors
        if error.startswith("Missing required file:")
    )

    print(
        "[OK] Hardware evidence "
        f"({required_file_count}/5 required files present)"
        if required_file_count == 5
        else
        "[FAIL] Hardware evidence "
        f"({required_file_count}/5 required files present)"
    )

    benchmark_count = len(result.benchmark_files)

    if benchmark_count >= 3:
        print(
            f"[OK] Benchmark runs ({benchmark_count} found)"
        )
    elif benchmark_count > 0:
        print(
            f"[WARN] Benchmark runs ({benchmark_count} found; "
            "3 required for new submissions)"
        )
    else:
        print("[FAIL] Benchmark runs (none found)")

    if result.warnings:
        print()
        print("Warnings:")
        for warning in result.warnings:
            print(f"- {warning}")

    if result.errors:
        print()
        print("Errors:")
        for error in result.errors:
            print(f"- {error}")

    print()

    if result.valid:
        if result.warnings:
            print(
                "Validation PASSED with "
                f"{len(result.warnings)} warning(s)."
            )
        else:
            print("Validation PASSED.")

        return True

    print(
        "Validation FAILED with "
        f"{len(result.errors)} error(s)."
    )

    return False


def main() -> int:
    """Run the submission validation CLI."""

    parser = build_argument_parser()
    args = parser.parse_args()

    try:
        submission = Submission.from_path(
            args.submission_path
        )
    except (FileNotFoundError, NotADirectoryError) as error:
        print()
        print("OpenLLMBench Submission Validation")
        print("=" * 34)
        print()
        print(f"ERROR: {error}")
        return 1

    valid = print_preflight_result(submission)

    return 0 if valid else 1


if __name__ == "__main__":
    raise SystemExit(main())