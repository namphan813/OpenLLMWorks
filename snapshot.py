"""
OpenLLMBench Snapshot Viewer

Purpose:
Validates the benchmark database, builds a current-state
OpenLLMBench snapshot, and prints a compact milestone report.

Version:
0.7.0-dev1
"""

from pathlib import Path
from typing import Any

from analytics.snapshots import build_snapshot
from parser.database import load_database
from parser.validator import validate_database_file


SNAPSHOT_VIEWER_VERSION = "0.7.0-dev1"

PROJECT_FOLDER = Path(__file__).resolve().parent

DATABASE_FILE = (
    PROJECT_FOLDER
    / "database"
    / "benchmark_database.json"
)


# ------------------------------------------------------------
# DISPLAY HELPERS
# ------------------------------------------------------------

def print_section(title: str) -> None:
    """Print one snapshot section heading."""

    print()
    print("=" * 64)
    print(title)
    print("=" * 64)


def format_number(
    value: Any,
    decimal_places: int = 2,
) -> str:
    """Format a numeric value safely."""

    if isinstance(value, bool):
        return "Unavailable"

    if isinstance(value, (int, float)):
        return f"{value:.{decimal_places}f}"

    return "Unavailable"


def format_count(
    value: Any,
) -> str:
    """Format an integer-style count safely."""

    if isinstance(value, bool):
        return "Unavailable"

    if isinstance(value, int):
        return str(value)

    return "Unavailable"


def print_counted_item(
    label: str,
    item: dict | None,
    name_key: str,
) -> None:
    """Print one most-common item and its count."""

    if not item:
        print(f"{label:<28} Unavailable")
        return

    print(
        f"{label:<28} "
        f"{item.get(name_key, 'Unknown')}"
    )

    print(
        f"{'':<28} "
        f"{format_count(item.get('count'))} result(s)"
    )


def print_leader(
    title: str,
    leader: dict | None,
    unit: str,
) -> None:
    """Print one performance leader."""

    print()
    print(title)

    if not leader:
        print("  No leader available.")
        return

    print(
        f"  GPU:         "
        f"{leader.get('gpu_model', 'Unknown')}"
    )

    print(
        f"  Submission:  "
        f"{leader.get('submission_name', 'Unknown')}"
    )

    print(
        f"  Result:      "
        f"{format_number(leader.get('value'))} {unit}"
    )


# ------------------------------------------------------------
# SNAPSHOT SECTIONS
# ------------------------------------------------------------

def print_database_snapshot(
    snapshot: dict,
) -> None:
    """Print database-level snapshot information."""

    database = snapshot["database"]

    print_section("Database")

    print(
        f"{'Project':<28} "
        f"{database['project']}"
    )

    print(
        f"{'Schema version':<28} "
        f"{database['schema_version']}"
    )

    print(
        f"{'Parser version':<28} "
        f"{database['parser_version']}"
    )

    print(
        f"{'Unique results':<28} "
        f"{database['total_results']}"
    )

    print(
        f"{'Import events':<28} "
        f"{database['import_events']}"
    )

    print(
        f"{'Results added':<28} "
        f"{database['results_added']}"
    )

    print(
        f"{'Duplicates detected':<28} "
        f"{database['duplicates_detected']}"
    )


def print_community_snapshot(
    snapshot: dict,
) -> None:
    """Print represented hardware and platform counts."""

    community = snapshot["community"]

    print_section("Community Snapshot")

    print(
        f"{'Unique GPU models':<28} "
        f"{community['unique_gpu_models']}"
    )

    print(
        f"{'Unique CPU models':<28} "
        f"{community['unique_cpu_models']}"
    )

    print(
        f"{'Unique operating systems':<28} "
        f"{community['unique_operating_systems']}"
    )

    print(
        f"{'GPU profiles available':<28} "
        f"{community['gpu_profiles_available']}"
    )

    print()

    print_counted_item(
        label="Most common GPU",
        item=community["most_common_gpu"],
        name_key="model",
    )

    print()

    print_counted_item(
        label="Most common CPU",
        item=community["most_common_cpu"],
        name_key="model",
    )

    print()

    print_counted_item(
        label="Most common OS",
        item=community[
            "most_common_operating_system"
        ],
        name_key="name",
    )


def print_hardware_snapshot(
    snapshot: dict,
) -> None:
    """Print hardware capacity and vendor information."""

    hardware = snapshot["hardware"]

    print_section("Hardware")

    print(
        f"{'Average VRAM':<28} "
        f"{format_number(hardware['average_vram_gib'])} GiB"
    )

    print(
        f"{'Average system memory':<28} "
        f"{format_number(hardware['average_memory_gb'])} GB"
    )

    largest_vram = hardware["largest_vram"]

    if largest_vram:
        print()
        print("Largest VRAM")

        print(
            f"  GPU:         "
            f"{largest_vram['gpu_model']}"
        )

        print(
            f"  Capacity:    "
            f"{format_number(largest_vram['capacity_gib'])} GiB"
        )

        print(
            f"  Submission:  "
            f"{largest_vram['submission_name']}"
        )

    largest_memory = hardware[
        "largest_system_memory"
    ]

    if largest_memory:
        print()
        print("Largest System Memory")

        print(
            f"  Submission:  "
            f"{largest_memory['submission_name']}"
        )

        print(
            f"  GPU:         "
            f"{largest_memory['gpu_model']}"
        )

        print(
            f"  Capacity:    "
            f"{format_number(largest_memory['capacity_gb'])} GB"
        )

    print()
    print("GPU Vendors")

    gpu_vendor_counts = hardware[
        "gpu_vendor_counts"
    ]

    if not gpu_vendor_counts:
        print("  None")
    else:
        for vendor, count in gpu_vendor_counts.items():
            print(
                f"  {vendor:<20} {count}"
            )

    print()
    print("CPU Vendors")

    cpu_vendor_counts = hardware[
        "cpu_vendor_counts"
    ]

    if not cpu_vendor_counts:
        print("  None")
    else:
        for vendor, count in cpu_vendor_counts.items():
            print(
                f"  {vendor:<20} {count}"
            )


def print_performance_snapshot(
    snapshot: dict,
) -> None:
    """Print current benchmark performance information."""

    performance = snapshot["performance"]

    print_section("Performance")

    print(
        f"{'Average pp512':<28} "
        f"{format_number(performance['average_pp512'])} "
        "tokens/sec"
    )

    print(
        f"{'Average tg128':<28} "
        f"{format_number(performance['average_tg128'])} "
        "tokens/sec"
    )

    print_leader(
        title="Fastest pp512",
        leader=performance["fastest_pp512"],
        unit="tokens/sec",
    )

    print_leader(
        title="Fastest tg128",
        leader=performance["fastest_tg128"],
        unit="tokens/sec",
    )


def print_selected_facts(
    snapshot: dict,
    limit: int = 5,
) -> None:
    """Print a small selection of generated facts."""

    facts = snapshot["interesting_facts"]

    print_section("Snapshot Highlights")

    if not facts:
        print("No interesting facts available.")
        return

    for fact in facts[:limit]:
        print(f"• {fact['title']}")
        print(f"  {fact['description']}")
        print()


# ------------------------------------------------------------
# MAIN
# ------------------------------------------------------------

def main() -> None:
    """Validate the database and print the current snapshot."""

    print("OpenLLMBench Weekend Snapshot")
    print(
        f"Snapshot Viewer "
        f"v{SNAPSHOT_VIEWER_VERSION}"
    )

    try:
        validation = validate_database_file(
            DATABASE_FILE
        )

    except (
        FileNotFoundError,
        ValueError,
    ) as error:
        print()
        print(f"ERROR: {error}")
        return

    if not validation["valid"]:
        print()
        print("Database validation failed.")

        for error in validation["errors"]:
            print(f"- {error}")

        return

    try:
        database = load_database(
            database_file=DATABASE_FILE,
            parser_version=(
                SNAPSHOT_VIEWER_VERSION
            ),
        )

    except ValueError as error:
        print()
        print(f"ERROR: {error}")
        return

    snapshot = build_snapshot(
        database=database,
        snapshot_name=(
            "OpenLLMBench Weekend 4 Snapshot"
        ),
    )

    print()
    print(snapshot["snapshot_name"])

    print(
        "Snapshot type: "
        f"{snapshot['snapshot_type']}"
    )

    print(
        "Time comparison available: "
        f"{snapshot['time_comparison_available']}"
    )

    print_database_snapshot(snapshot)
    print_community_snapshot(snapshot)
    print_hardware_snapshot(snapshot)
    print_performance_snapshot(snapshot)
    print_selected_facts(snapshot)


if __name__ == "__main__":
    main()