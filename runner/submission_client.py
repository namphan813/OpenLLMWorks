"""
OpenLLMWorks Direct Submission Client

Phase:
Weekend 17 - Direct Submission Pipeline

Purpose:
Provide contributor-facing disclosure, consent handling, and
optional HTTPS upload of validated benchmark submission packages.

Direct submission is always opt-in.

The canonical OpenLLMWorks submission ZIP remains saved locally
regardless of whether the contributor chooses to upload it or
whether the upload succeeds.
"""

from __future__ import annotations

import json
import socket
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any


SUBMISSION_API_URL = (
    "https://api.openllmworks.com/v1/submissions"
)

UPLOAD_TIMEOUT_SECONDS = 30


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


def parse_json_response(
    response_body: bytes,
) -> dict[str, Any] | None:
    """
    Decode a JSON API response.

    Invalid or unexpected JSON is treated as an unusable response
    rather than a benchmark failure.
    """

    try:
        decoded = response_body.decode(
            "utf-8"
        )

        parsed = json.loads(
            decoded
        )

    except (
        UnicodeDecodeError,
        json.JSONDecodeError,
    ):
        return None

    if not isinstance(
        parsed,
        dict,
    ):
        return None

    return parsed


def upload_submission(
    *,
    zip_path: Path,
) -> tuple[bool, str | None]:
    """
    Upload the canonical submission ZIP to OpenLLMWorks.

    Returns:

        (True, submission_id)

    on successful receipt, or:

        (False, None)

    when the upload fails.

    Upload failure never invalidates the completed benchmark.
    """

    if not zip_path.is_file():
        print()
        print(
            "[WARN] Direct submission could not start "
            "because the ZIP file was not found."
        )
        print()

        return (
            False,
            None,
        )

    try:
        zip_bytes = zip_path.read_bytes()

    except OSError as exc:
        print()
        print(
            "[WARN] Direct submission could not read "
            "the validated ZIP package."
        )
        print(
            f"[DETAIL] {exc}"
        )
        print()

        return (
            False,
            None,
        )

    if not zip_bytes:
        print()
        print(
            "[WARN] Direct submission could not start "
            "because the ZIP package is empty."
        )
        print()

        return (
            False,
            None,
        )

    request = urllib.request.Request(
        SUBMISSION_API_URL,
        data=zip_bytes,
        method="POST",
        headers={
            "Content-Type": "application/zip",
            "Content-Length": str(
                len(zip_bytes)
            ),
            "User-Agent": (
                "OpenLLMWorks-Runner"
            ),
        },
    )

    print()
    print(
        "[INFO] Uploading validated benchmark "
        "package..."
    )
    print()

    try:
        with urllib.request.urlopen(
            request,
            timeout=UPLOAD_TIMEOUT_SECONDS,
        ) as response:
            status_code = (
                response.status
            )

            response_body = (
                response.read()
            )

    except urllib.error.HTTPError as exc:
        response_body = (
            exc.read()
        )

        parsed = parse_json_response(
            response_body
        )

        print()
        print(
            "[WARN] OpenLLMWorks could not receive "
            "the benchmark submission."
        )

        if parsed is not None:
            message = parsed.get(
                "message"
            )

            if isinstance(
                message,
                str,
            ):
                print(
                    f"[DETAIL] {message}"
                )

        print(
            f"[DETAIL] HTTP {exc.code}"
        )
        print()

        return (
            False,
            None,
        )

    except (
        urllib.error.URLError,
        TimeoutError,
        socket.timeout,
    ) as exc:
        print()
        print(
            "[WARN] Direct submission could not "
            "reach OpenLLMWorks."
        )
        print(
            f"[DETAIL] {exc}"
        )
        print()

        return (
            False,
            None,
        )

    except OSError as exc:
        print()
        print(
            "[WARN] Direct submission encountered "
            "a network error."
        )
        print(
            f"[DETAIL] {exc}"
        )
        print()

        return (
            False,
            None,
        )

    if status_code != 201:
        print()
        print(
            "[WARN] OpenLLMWorks returned an "
            "unexpected submission response."
        )
        print(
            f"[DETAIL] HTTP {status_code}"
        )
        print()

        return (
            False,
            None,
        )

    parsed = parse_json_response(
        response_body
    )

    if parsed is None:
        print()
        print(
            "[WARN] OpenLLMWorks returned an "
            "unreadable submission response."
        )
        print()

        return (
            False,
            None,
        )

    status = parsed.get(
        "status"
    )

    submission_id = parsed.get(
        "submission_id"
    )

    if (
        status != "received"
        or not isinstance(
            submission_id,
            str,
        )
        or not submission_id
    ):
        print()
        print(
            "[WARN] OpenLLMWorks returned an "
            "unexpected submission response."
        )
        print()

        return (
            False,
            None,
        )

    return (
        True,
        submission_id,
    )


def offer_direct_submission(
    *,
    zip_path: Path,
    submission_name: str,
    gpu_name: str,
) -> None:
    """
    Present the optional direct-submission workflow.

    Benchmark success and upload success remain separate.
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

    upload_succeeded, submission_id = (
        upload_submission(
            zip_path=zip_path,
        )
    )

    if not upload_succeeded:
        print(
            "Your benchmark completed successfully."
        )
        print(
            "The validated ZIP remains saved locally."
        )
        print(
            "You can submit it manually later."
        )
        print()

        return

    print()
    print(
        "[OK] Benchmark received by OpenLLMWorks."
    )
    print()
    print(
        f"Submission ID: {submission_id}"
    )
    print()
    print(
        "Your local ZIP has been preserved."
    )
    print()