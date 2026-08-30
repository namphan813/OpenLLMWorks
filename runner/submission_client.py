"""
OpenLLMWorks Direct Submission Client

Phase:
Weekend 17 - Direct Submission Pipeline

Purpose:
Provide contributor-facing disclosure and consent handling for
optional direct benchmark submission.

Direct submission is always opt-in.

The canonical OpenLLMWorks submission ZIP remains saved locally
regardless of whether the contributor chooses to upload it.

Network transport is intentionally not implemented in this phase.
"""

from __future__ import annotations

from pathlib import Path


def print_submission_disclosure(
    *,
    zip_path: Path,
    submission_name: str,
    gpu_name: str,
) -> None:
    """
    Show the contributor what benchmark package would be uploaded.
    """

    print()
    print("=" * 60)
    print("Submit Benchmark to OpenLLMWorks")
    print("=" * 60)
    print()

    print(
        "Your validated benchmark package is ready "
        "for optional submission."
    )
    print()

    print(
        f"Submission: {submission_name}"
    )

    print(
        f"GPU:        {gpu_name}"
    )

    print(
        f"Package:    {zip_path.name}"
    )

    print()
    print(
        "The package includes benchmark results and "
        "system information collected by the Runner:"
    )
    print()

    print("- CPU information")
    print("- Memory information")
    print("- Operating system information")
    print("- GPU and driver information")
    print("- Raw benchmark output")
    print("- OpenLLMWorks submission manifest")

    print()
    print(
        "Your validated ZIP will remain saved locally "
        "whether or not you upload it."
    )
    print()


def prompt_for_upload() -> bool:
    """
    Ask for explicit contributor consent before any upload.

    Ctrl+C and EOF are treated as declining the optional upload
    rather than interrupting the completed benchmark workflow.
    """

    while True:
        try:
            response = input(
                "Upload this benchmark to OpenLLMWorks? [Y/N]: "
            ).strip().lower()

        except (KeyboardInterrupt, EOFError):
            print()
            return False

        if response in {
            "y",
            "yes",
        }:
            return True

        if response in {
            "n",
            "no",
            "",
        }:
            return False

        print()
        print(
            "Please enter Y or N."
        )
        print()


def offer_direct_submission(
    *,
    zip_path: Path,
    submission_name: str,
    gpu_name: str,
) -> None:
    """
    Present the optional direct-submission workflow.

    Network transport will be added in a later implementation step.
    """

    print_submission_disclosure(
        zip_path=zip_path,
        submission_name=submission_name,
        gpu_name=gpu_name,
    )

    upload_requested = (
        prompt_for_upload()
    )

    if not upload_requested:
        print()
        print(
            "Direct submission skipped."
        )
        print(
            "You can submit the saved ZIP manually later."
        )
        print()

        return

    print()
    print(
        "[INFO] Direct submission transport is not "
        "connected in this development build."
    )
    print()
    print(
        "No files were uploaded."
    )
    print(
        "Your validated ZIP remains saved locally."
    )
    print()