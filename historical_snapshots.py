"""
OpenLLMWorks Historical Snapshot Viewer

Purpose:
Prints monthly OpenLLMWorks snapshot history and comparisons.

Version:
0.8.0-dev1
"""

from pathlib import Path
from typing import Any

from analytics.historical_snapshots import (
    build_historical_snapshots,
)
from parser.database import load_database


HISTORICAL_VIEWER_VERSION = "0.8.0-dev1"

PROJECT_FOLDER = Path(__file__).resolve().parent

DATABASE_FILE = (
    PROJECT_FOLDER
    / "database"
    / "benchmark_database.json"
)


# ------------------------------------------------------------
# DISPLAY HELPERS
# ------------------------------------------------------------

def print_section(
    title: str,
) -> None:
    """Print one report section."""

    print()
    print("=" * 64)
    print(title)
    print("=" * 64)


def format_number(
    value: Any,
) -> str:
    """Format a numeric value safely."""

    if (
        isinstance(value, (int, float))
        and not isinstance(value, bool)
    ):
        return f"{value:.2f}"

    return "Unavailable"


def format_change(
    value: Any,
    suffix: str = "%",
) -> str:
    """Format positive and negative change values."""

    if (
        not isinstance(value, (int, float))
        or isinstance(value, bool)
    ):
        return "No prior comparison"

    sign = "+" if value > 0 else ""

    return f"{sign}{value:.2f}{suffix}"


def print_snapshot(
    snapshot: dict,
) -> None:
    """Print one monthly historical snapshot."""

    print_section(
        f"Monthly Snapshot — {snapshot['month']}"
    )

    print(
        f"{'Results':<30}"
        f"{snapshot['result_count']}"
    )

    print(
        f"{'Unique GPU models':<30}"
        f"{snapshot['unique_gpu_models']}"
    )

    print(
        f"{'Unique CPU models':<30}"
        f"{snapshot['unique_cpu_models']}"
    )

    performance = snapshot["performance"]

    print()
    print("Performance")

    print(
        f"{'Average pp512':<30}"
        f"{format_number(performance['average_pp512'])} "
        "tokens/sec"
    )

    print(
        f"{'Average tg128':<30}"
        f"{format_number(performance['average_tg128'])} "
        "tokens/sec"
    )

    print(
        f"{'Fastest pp512':<30}"
        f"{format_number(performance['fastest_pp512'])} "
        "tokens/sec"
    )

    print(
        f"{'Fastest tg128':<30}"
        f"{format_number(performance['fastest_tg128'])} "
        "tokens/sec"
    )

    changes = snapshot["changes"]

    print()
    print("Change From Previous Month")

    print(
        f"{'Result count':<30}"
        f"{format_change(changes['result_count_change'], '')}"
    )

    print(
        f"{'Result growth':<30}"
        f"{format_change(changes['result_count_percent_change'])}"
    )

    print(
        f"{'Average pp512':<30}"
        f"{format_change(changes['average_pp512_percent_change'])}"
    )

    print(
        f"{'Average tg128':<30}"
        f"{format_change(changes['average_tg128_percent_change'])}"
    )


# ------------------------------------------------------------
# MAIN
# ------------------------------------------------------------

def main() -> None:
    """Load the database and print historical snapshots."""

    print("OpenLLMWorks Historical Snapshots")
    print(
        f"Historical Viewer "
        f"v{HISTORICAL_VIEWER_VERSION}"
    )

    try:
        database = load_database(
            database_file=DATABASE_FILE,
            parser_version=(
                HISTORICAL_VIEWER_VERSION
            ),
        )

        report = build_historical_snapshots(
            database
        )

    except (
        FileNotFoundError,
        ValueError,
    ) as error:
        print()
        print(f"ERROR: {error}")
        return

    print_section("Snapshot Coverage")

    print(
        f"{'Database results':<30}"
        f"{report['database_result_count']}"
    )

    print(
        f"{'Timestamped results':<30}"
        f"{report['timestamped_result_count']}"
    )

    print(
        f"{'Monthly snapshots':<30}"
        f"{report['snapshot_count']}"
    )

    print(
        f"{'First month':<30}"
        f"{report['first_month']}"
    )

    print(
        f"{'Last month':<30}"
        f"{report['last_month']}"
    )

    for snapshot in report["snapshots"]:
        print_snapshot(snapshot)


if __name__ == "__main__":
    main()