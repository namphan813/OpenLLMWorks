"""
OpenLLMWorks Parser Orchestrator

Purpose:
Discovers incoming benchmark submissions, parses each
submission, builds normalized benchmark records, detects
duplicates, and updates the persistent benchmark database.

Version:
0.6.0-dev5
"""

import argparse
from pathlib import Path
import statistics

from parser.benchmark import (
    determine_status,
    extract_result,
    print_status_message,
)
from parser.database import (
    add_result,
    build_result_record,
    load_database,
    write_database,
)
from parser.hardware import load_hardware_profile
from parser.submission import (
    Submission,
    discover_submissions,
    validate_submission_preflight,
)


PARSER_VERSION = "0.6.0-dev5"


# ------------------------------------------------------------
# PROJECT LOCATIONS
# ------------------------------------------------------------

PROJECT_FOLDER = Path(__file__).resolve().parent.parent
INCOMING_FOLDER = PROJECT_FOLDER / "incoming"
DATABASE_FOLDER = PROJECT_FOLDER / "database"

DATABASE_FILE = (
    DATABASE_FOLDER
    / "benchmark_database.json"
)


# ------------------------------------------------------------
# BENCHMARK PROTOCOL SETTINGS
# ------------------------------------------------------------

REQUIRED_RUNS = 3


# ------------------------------------------------------------
# PROVENANCE DEFAULTS
# ------------------------------------------------------------

DEFAULT_SOURCE_TYPE = "internal_seed"
DEFAULT_CONTRIBUTOR_ID = "founder_000001"
DEFAULT_CONTRIBUTOR_TYPE = "founder"
DEFAULT_VERIFICATION_STATUS = "internally_verified"


# ------------------------------------------------------------
# DISPLAY HARDWARE PROFILE
# ------------------------------------------------------------

def print_hardware_profile(
    hardware: dict,
) -> None:
    """
    Print a human-readable hardware summary.
    """

    system = hardware["system"]
    cpu = hardware["cpu"]
    memory = hardware["memory"]
    os_data = hardware["operating_system"]
    gpu = hardware["gpu"]

    print("Hardware Profile")
    print(
        f"System manufacturer: "
        f"{system['manufacturer']}"
    )
    print(
        f"System model: "
        f"{system['model']}"
    )

    if system["generic_firmware_identity"]:
        print(
            "Note: Generic motherboard firmware "
            "identity detected."
        )

    print(f"CPU: {cpu['model']}")

    print(
        f"CPU topology: "
        f"{cpu['physical_cores']} cores / "
        f"{cpu['logical_processors']} "
        "logical processors"
    )

    print(
        "Memory: "
        f"{memory['installed_capacity_gb']} GB "
        f"({memory['calculated_gib']:.2f} "
        "GiB reported)"
    )

    print(f"GPU: {gpu['model']}")

    print(
        f"VRAM: "
        f"{gpu['vram']['capacity_gib']} GiB"
    )

    print(
        "NVIDIA driver: "
        f"{gpu['software']['driver_version']}"
    )

    print(
        "CUDA UMD: "
        f"{gpu['software']['cuda_umd_version']}"
    )

    reported = os_data["reported"]
    normalized = os_data["normalized"]

    print(
        "Windows reported: "
        f"{reported['product_name']} "
        f"{reported['version']} "
        f"(build {reported['build']})"
    )

    normalized_description = (
        normalized["name"]
        or "Unknown Windows"
    )

    if normalized["release"]:
        normalized_description += (
            f" {normalized['release']}"
        )

    print(
        "Windows normalized: "
        f"{normalized_description}"
    )

    print(
        "OS recognition: "
        f"{normalized['recognition_status']}"
    )


# ------------------------------------------------------------
# PROCESS ONE SUBMISSION
# ------------------------------------------------------------

def process_submission(
    submission: Submission,
    *,
    source_type: str = DEFAULT_SOURCE_TYPE,
    contributor_id: str = DEFAULT_CONTRIBUTOR_ID,
    contributor_type: str = DEFAULT_CONTRIBUTOR_TYPE,
    verification_status: str = DEFAULT_VERIFICATION_STATUS,
) -> dict | None:
    """
    Parse one submission and return a normalized result record.

    Provenance is supplied by the trusted import workflow rather
    than by contributor-controlled submission metadata.

    Returns None when the submission cannot produce a valid
    benchmark record.
    """

    print("=" * 60)
    print(
        "Processing submission: "
        f"{submission.submission_name}"
    )
    print(
        f"Source: {submission.source_path}"
    )
    print("=" * 60)
    print()

    preflight = validate_submission_preflight(
        submission
    )

    for warning in preflight.warnings:
        print(f"WARNING: {warning}")

    if not preflight.valid:
        for error in preflight.errors:
            print(f"ERROR: {error}")

        print(
            "Submission skipped because it failed "
            "structural preflight validation."
        )

        return None

    print("Preflight: PASSED")
    print()

    if preflight.manifest is not None:
        effective_submission_name = (
            preflight.manifest.submission_name
        )
        submitted_at = (
            preflight.manifest.submitted_at
        )
        benchmark_timestamp = (
            preflight.manifest.benchmark_timestamp
        )

        print("Submission manifest: LOADED")
        print(
            "Manifest submission name: "
            f"{effective_submission_name}"
        )
        print(
            "Submitted at: "
            f"{submitted_at}"
        )
        print(
            "Benchmark timestamp: "
            f"{benchmark_timestamp}"
        )
        print()

    else:
        effective_submission_name = (
            submission.submission_name
        )
        submitted_at = None
        benchmark_timestamp = None

    try:
        hardware = load_hardware_profile(
            submission.source_path
        )

    except (
        FileNotFoundError,
        ValueError,
    ) as error:
        print(f"ERROR: {error}")
        print(
            "Submission skipped because its "
            "hardware profile could not be parsed."
        )
        return None

    print_hardware_profile(hardware)

    print()
    print("-" * 50)

    benchmark_files = sorted(
        submission.source_path.glob(
            "benchmark*-run*.txt"
        )
    )

    if not benchmark_files:
        print(
            "ERROR: No benchmark run files "
            "were found."
        )
        print(
            "Submission skipped: "
            f"{effective_submission_name}"
        )
        return None

    print(
        f"Found {len(benchmark_files)} "
        "benchmark file(s).\n"
    )

    results: list[dict] = []

    for file_path in benchmark_files:
        try:
            result = extract_result(file_path)
            results.append(result)

            print(file_path.name)

            print(
                f"  pp512: "
                f"{result['pp512']:.2f} "
                "tokens/sec"
            )

            print(
                f"  tg128: "
                f"{result['tg128']:.2f} "
                "tokens/sec"
            )

            if result["commit"] is not None:
                print(
                    f"  Commit: "
                    f"{result['commit']}"
                )

            if result["build"] is not None:
                print(
                    f"  Build: "
                    f"{result['build']}"
                )

            print()

        except ValueError as error:
            print(f"ERROR: {error}")
            print(
                "File excluded from the "
                "benchmark average.\n"
            )

    status = determine_status(
        valid_run_count=len(results),
        required_runs=REQUIRED_RUNS,
    )

    if not results:
        print_status_message(
            status=status,
            valid_run_count=0,
            required_runs=REQUIRED_RUNS,
        )

        print(
            "Submission skipped because no "
            "valid benchmark runs were parsed."
        )

        return None

    pp_average = statistics.mean(
        result["pp512"]
        for result in results
    )

    tg_average = statistics.mean(
        result["tg128"]
        for result in results
    )

    print("-" * 50)
    print("Official Average")

    print(
        f"pp512: "
        f"{pp_average:.2f} tokens/sec"
    )

    print(
        f"tg128: "
        f"{tg_average:.2f} tokens/sec"
    )

    print()
    print("-" * 50)
    print("Submission Validation")

    print_status_message(
        status=status,
        valid_run_count=len(results),
        required_runs=REQUIRED_RUNS,
    )

    return build_result_record(
        results=results,
        hardware=hardware,
        status=status,
        pp_average=pp_average,
        tg_average=tg_average,
        submission_name=effective_submission_name,
        submission_source=str(
            submission.source_path
        ),
        required_runs=REQUIRED_RUNS,
        parser_version=PARSER_VERSION,
        submitted_at=submitted_at,
        benchmark_timestamp=benchmark_timestamp,
        source_type=source_type,
        contributor_id=contributor_id,
        contributor_type=contributor_type,
        verification_status=verification_status,
    )


# ------------------------------------------------------------
# COMMAND-LINE INTERFACE
# ------------------------------------------------------------

def build_argument_parser() -> argparse.ArgumentParser:
    """
    Build the parser orchestrator command-line interface.
    """

    argument_parser = argparse.ArgumentParser(
        description=(
            "Process OpenLLMWorks submissions from the "
            "incoming directory and update the benchmark "
            "database."
        )
    )

    argument_parser.add_argument(
        "--submission",
        help=(
            "Process only the named submission directory "
            "inside incoming. If omitted, all discovered "
            "submissions are processed."
        ),
    )

    argument_parser.add_argument(
        "--source-type",
        default=DEFAULT_SOURCE_TYPE,
        help=(
            "Trusted submission source type. "
            f"Default: {DEFAULT_SOURCE_TYPE}"
        ),
    )

    argument_parser.add_argument(
        "--contributor-id",
        default=DEFAULT_CONTRIBUTOR_ID,
        help=(
            "Trusted contributor identifier. "
            f"Default: {DEFAULT_CONTRIBUTOR_ID}"
        ),
    )

    argument_parser.add_argument(
        "--contributor-type",
        default=DEFAULT_CONTRIBUTOR_TYPE,
        help=(
            "Trusted contributor type. "
            f"Default: {DEFAULT_CONTRIBUTOR_TYPE}"
        ),
    )

    argument_parser.add_argument(
        "--verification-status",
        default=DEFAULT_VERIFICATION_STATUS,
        help=(
            "Maintainer-assigned verification status. "
            f"Default: {DEFAULT_VERIFICATION_STATUS}"
        ),
    )

    return argument_parser


def resolve_submissions(
    submission_name: str | None,
) -> list[Submission]:
    """
    Resolve either one explicitly requested submission or all
    submissions currently present in the incoming directory.
    """

    if submission_name is None:
        return discover_submissions(
            INCOMING_FOLDER
        )

    requested_path = (
        INCOMING_FOLDER
        / submission_name
    )

    if not requested_path.exists():
        raise FileNotFoundError(
            "Requested submission was not found: "
            f"{requested_path}"
        )

    if not requested_path.is_dir():
        raise NotADirectoryError(
            "Requested submission is not a directory: "
            f"{requested_path}"
        )

    return [
        Submission.from_path(
            requested_path
        )
    ]


# ------------------------------------------------------------
# MAIN
# ------------------------------------------------------------

def main(
    args: argparse.Namespace,
) -> None:
    """
    Process selected incoming submissions and update the
    persistent benchmark database.
    """

    print("Open LLM Benchmark Database")
    print(
        f"Benchmark Parser v{PARSER_VERSION}"
    )
    print("-" * 60)

    try:
        submissions = resolve_submissions(
            args.submission
        )

    except (
        FileNotFoundError,
        NotADirectoryError,
    ) as error:
        print(f"ERROR: {error}")
        return

    print(
        f"Discovered {len(submissions)} "
        "submission(s):"
    )

    for submission in submissions:
        print(
            f"  - {submission.submission_name}"
        )

    print()

    if not submissions:
        print(
            "No submission folders were found "
            "inside:"
        )
        print(INCOMING_FOLDER)
        return

    print("Import Provenance")
    print(
        f"Source type: "
        f"{args.source_type}"
    )
    print(
        f"Contributor ID: "
        f"{args.contributor_id}"
    )
    print(
        f"Contributor type: "
        f"{args.contributor_type}"
    )
    print(
        "Verification status: "
        f"{args.verification_status}"
    )
    print()

    try:
        database = load_database(
            database_file=DATABASE_FILE,
            parser_version=PARSER_VERSION,
        )

    except ValueError as error:
        print(f"ERROR: {error}")
        print(
            "The benchmark database was not "
            "modified."
        )
        return

    added_count = 0
    duplicate_count = 0
    skipped_count = 0

    for submission in submissions:
        record = process_submission(
            submission,
            source_type=args.source_type,
            contributor_id=args.contributor_id,
            contributor_type=args.contributor_type,
            verification_status=(
                args.verification_status
            ),
        )

        if record is None:
            skipped_count += 1
            print()
            continue

        import_status, result_id = add_result(
            database=database,
            record=record,
        )

        print()
        print("-" * 50)
        print("Database Import")

        if import_status == "added":
            added_count += 1

            print("Status: ADDED")
            print(f"Result ID: {result_id}")

        elif import_status == "duplicate":
            duplicate_count += 1

            print("Status: DUPLICATE")
            print(
                "Existing result ID: "
                f"{result_id}"
            )

        print()

    write_database(
        database=database,
        database_file=DATABASE_FILE,
        parser_version=PARSER_VERSION,
    )

    print("=" * 60)
    print("Import Summary")
    print("=" * 60)
    print(
        f"Submissions discovered: "
        f"{len(submissions)}"
    )
    print(f"New results added: {added_count}")
    print(
        f"Duplicates detected: "
        f"{duplicate_count}"
    )
    print(f"Submissions skipped: {skipped_count}")
    print(
        f"Total database results: "
        f"{database['result_count']}"
    )
    print()
    print(
        "Database written to:"
    )
    print(DATABASE_FILE)


if __name__ == "__main__":
    argument_parser = build_argument_parser()
    arguments = argument_parser.parse_args()
    main(arguments)