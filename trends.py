"""
OpenLLMBench Trend Viewer

Purpose:
Loads the benchmark database and prints current monthly
time-aware analytics.

Version:
0.8.0-dev1
"""

from pathlib import Path
from typing import Any

from analytics.trends import (
    build_trend_report,
)
from parser.database import load_database


TREND_VIEWER_VERSION = "0.8.0-dev1"

PROJECT_FOLDER = Path(
    __file__
).resolve().parent

DATABASE_FILE = (
    PROJECT_FOLDER
    / "database"
    / "benchmark_database.json"
)


def format_number(
    value: Any,
) -> str:
    """
    Format a numeric trend value safely.
    """

    if (
        isinstance(value, (int, float))
        and not isinstance(value, bool)
    ):
        return f"{value:.2f}"

    return "Unavailable"


def print_section(
    title: str,
) -> None:
    """
    Print one viewer section heading.
    """

    print()
    print("=" * 64)
    print(title)
    print("=" * 64)


def print_monthly_trends(
    months: list[dict],
) -> None:
    """
    Print all monthly trend buckets.
    """

    print_section(
        "Monthly Trends"
    )

    if not months:
        print(
            "No timestamped benchmark "
            "results are available."
        )
        return

    for month in months:
        print(
            f"Month:              "
            f"{month['month']}"
        )

        print(
            f"Results:            "
            f"{month['result_count']}"
        )

        print(
            f"Unique GPUs:        "
            f"{month['unique_gpu_models']}"
        )

        print(
            f"Unique CPUs:        "
            f"{month['unique_cpu_models']}"
        )

        print(
            f"Average pp512:      "
            f"{format_number(month['average_pp512'])} "
            "tokens/sec"
        )

        print(
            f"Average tg128:      "
            f"{format_number(month['average_tg128'])} "
            "tokens/sec"
        )

        print(
            f"Fastest pp512:      "
            f"{format_number(month['fastest_pp512'])} "
            "tokens/sec"
        )

        print(
            f"Fastest tg128:      "
            f"{format_number(month['fastest_tg128'])} "
            "tokens/sec"
        )

        print()


def main() -> None:
    """
    Load the database and print the trend report.
    """

    print("OpenLLMBench Trends")
    print(
        f"Trend Viewer "
        f"v{TREND_VIEWER_VERSION}"
    )

    try:
        database = load_database(
            database_file=DATABASE_FILE,
            parser_version=(
                TREND_VIEWER_VERSION
            ),
        )

        report = build_trend_report(
            database
        )

    except (
        FileNotFoundError,
        ValueError,
    ) as error:
        print()
        print(f"ERROR: {error}")
        return

    print_section(
        "Trend Coverage"
    )

    print(
        "Database results:       "
        f"{report['database_result_count']}"
    )

    print(
        "Timestamped results:    "
        f"{report['timestamped_result_count']}"
    )

    print(
        "Untimestamped results:  "
        f"{report['untimestamped_result_count']}"
    )

    print(
        "First timestamp:        "
        f"{report['first_timestamp']}"
    )

    print(
        "Last timestamp:         "
        f"{report['last_timestamp']}"
    )

    print()
    print("Timestamp Sources")

    for source, count in (
        report[
            "timestamp_source_counts"
        ].items()
    ):
        print(
            f"  {source:<22} {count}"
        )

    print_monthly_trends(
        report["monthly"]
    )


if __name__ == "__main__":
    main()