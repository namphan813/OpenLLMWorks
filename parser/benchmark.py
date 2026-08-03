"""
OpenLLMBench Benchmark Parser

Purpose:
Provides functions for reading and parsing benchmark output files
generated under the OpenLLMBench Benchmark Protocol.

Version:
0.5.5
"""

from pathlib import Path
import re


BENCHMARK_MODULE_VERSION = "0.5.5"


# ------------------------------------------------------------
# FILE READING
# ------------------------------------------------------------

def read_text_file(file_path: Path) -> str:
    """
    Read a text file while handling common Windows encodings.

    Args:
        file_path:
            Path to the text file.

    Returns:
        The decoded text contents of the file.
    """

    raw_data = file_path.read_bytes()

    if raw_data.startswith((b"\xff\xfe", b"\xfe\xff")):
        return raw_data.decode("utf-16")

    if raw_data.startswith(b"\xef\xbb\xbf"):
        return raw_data.decode("utf-8-sig")

    try:
        return raw_data.decode("utf-8")

    except UnicodeDecodeError:
        return raw_data.decode(
            "cp1252",
            errors="replace",
        )


# ------------------------------------------------------------
# BENCHMARK PARSING
# ------------------------------------------------------------

def extract_result(file_path: Path) -> dict:
    """
    Extract benchmark metrics and llama.cpp version information.

    The function currently expects benchmark output containing:

    - pp512
    - tg128
    - llama.cpp commit and build information, when available

    Args:
        file_path:
            Path to one benchmark run file.

    Returns:
        A dictionary containing the parsed benchmark result.

    Raises:
        ValueError:
            If pp512 or tg128 cannot be found.
    """

    text = read_text_file(file_path)

    pp_match = re.search(
        r"pp512\s*\|\s*([0-9]+(?:\.[0-9]+)?)",
        text,
    )

    tg_match = re.search(
        r"tg128\s*\|\s*([0-9]+(?:\.[0-9]+)?)",
        text,
    )

    build_match = re.search(
        r"build:\s*([a-fA-F0-9]+)\s*\((\d+)\)",
        text,
    )

    if not pp_match:
        raise ValueError(
            f"Could not find a pp512 result in {file_path.name}"
        )

    if not tg_match:
        raise ValueError(
            f"Could not find a tg128 result in {file_path.name}"
        )

    return {
        "filename": file_path.name,
        "pp512": float(pp_match.group(1)),
        "tg128": float(tg_match.group(1)),
        "commit": (
            build_match.group(1)
            if build_match
            else None
        ),
        "build": (
            int(build_match.group(2))
            if build_match
            else None
        ),
    }


# ------------------------------------------------------------
# SUBMISSION STATUS
# ------------------------------------------------------------

def determine_status(
    valid_run_count: int,
    required_runs: int,
) -> str:
    """
    Determine the submission status from the number of valid runs.

    Args:
        valid_run_count:
            Number of successfully parsed benchmark runs.

        required_runs:
            Number of runs required by the benchmark protocol.

    Returns:
        One of:

        - complete
        - legacy_two_run
        - incomplete
        - invalid
    """

    if valid_run_count >= required_runs:
        return "complete"

    if valid_run_count == 2:
        return "legacy_two_run"

    if valid_run_count == 1:
        return "incomplete"

    return "invalid"


def print_status_message(
    status: str,
    valid_run_count: int,
    required_runs: int,
) -> None:
    """
    Print benchmark protocol status information.

    Args:
        status:
            Submission status returned by determine_status().

        valid_run_count:
            Number of successfully parsed benchmark runs.

        required_runs:
            Number of runs required by the benchmark protocol.
    """

    print(f"Runs completed: {valid_run_count}")
    print(f"Protocol runs required: {required_runs}")
    print(f"Submission status: {status}")

    messages = {
        "complete": (
            "Result meets the Benchmark Protocol v1.0 "
            "run-count requirement."
        ),
        "legacy_two_run": (
            "This is a legacy two-run result. Raw run files "
            "must be preserved and the result clearly labeled."
        ),
        "incomplete": (
            "This result is incomplete and should not be treated "
            "as an official comparable benchmark score."
        ),
        "invalid": (
            "This result is invalid because no valid benchmark "
            "runs were successfully parsed."
        ),
    }

    message = messages.get(
        status,
        "The submission returned an unknown status.",
    )

    print(message)