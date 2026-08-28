"""
OpenLLMWorks Leaderboard Viewer

Purpose:
Validates the OpenLLMWorks database, builds leaderboard data,
and prints a clean command-line leaderboard report.

Version:
0.7.0-dev3
"""

from pathlib import Path
from typing import Any

from analytics.leaderboards import build_leaderboards
from parser.database import load_database
from parser.validator import validate_database_file


LEADERBOARD_VIEWER_VERSION = "0.7.0-dev3"
LEADERBOARD_LIMIT = 10

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
    """Print one leaderboard section heading."""

    print()
    print("=" * 68)
    print(title)
    print("=" * 68)


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


def print_performance_leaderboard(
    title: str,
    entries: list[dict],
    unit: str,
) -> None:
    """Print a ranked performance leaderboard."""

    print_section(title)

    if not entries:
        print("No leaderboard data available.")
        return

    for entry in entries:
        print(
            f"{entry['rank']:>2}. "
            f"{entry['gpu_model']}"
        )

        print(
            f"    Result:      "
            f"{format_number(entry['value'])} {unit}"
        )

        print(
            f"    Submission:  "
            f"{entry['submission_name']}"
        )

        print(
            f"    CPU:         "
            f"{entry['cpu_model']}"
        )

        print(
            f"    OS:          "
            f"{entry['operating_system']}"
        )

        print()


def print_capacity_leaderboard(
    title: str,
    entries: list[dict],
    unit: str,
) -> None:
    """Print a ranked hardware-capacity leaderboard."""

    print_section(title)

    if not entries:
        print("No leaderboard data available.")
        return

    for entry in entries:
        print(
            f"{entry['rank']:>2}. "
            f"{entry['submission_name']}"
        )

        print(
            f"    GPU:         "
            f"{entry['gpu_model']}"
        )

        print(
            f"    Capacity:    "
            f"{format_number(entry['value'])} {unit}"
        )

        print(
            f"    CPU:         "
            f"{entry['cpu_model']}"
        )

        print()


def print_popularity_leaderboard(
    title: str,
    entries: list[dict],
) -> None:
    """Print a ranked popularity leaderboard."""

    print_section(title)

    if not entries:
        print("No leaderboard data available.")
        return

    for entry in entries:
        submission_word = (
            "submission"
            if entry["count"] == 1
            else "submissions"
        )

        print(
            f"{entry['rank']:>2}. "
            f"{entry['label']}"
        )

        print(
            f"    {entry['count']} "
            f"{submission_word} "
            f"({entry['percentage']:.2f}%)"
        )

        print()


# ------------------------------------------------------------
# MAIN
# ------------------------------------------------------------

def main() -> None:
    """Validate the database and print all leaderboards."""

    print("OpenLLMWorks Leaderboards")
    print(
        f"Leaderboard Viewer "
        f"v{LEADERBOARD_VIEWER_VERSION}"
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
                LEADERBOARD_VIEWER_VERSION
            ),
        )

    except ValueError as error:
        print()
        print(f"ERROR: {error}")
        return

    leaderboards = build_leaderboards(
        database=database,
        limit=LEADERBOARD_LIMIT,
    )

    print()
    print(
        f"Database results: "
        f"{leaderboards['database_result_count']}"
    )

    performance = leaderboards[
        "performance"
    ]

    print_performance_leaderboard(
        title="Fastest pp512",
        entries=performance[
            "fastest_pp512"
        ],
        unit="tokens/sec",
    )

    print_performance_leaderboard(
        title="Fastest tg128",
        entries=performance[
            "fastest_tg128"
        ],
        unit="tokens/sec",
    )

    hardware_capacity = leaderboards[
        "hardware_capacity"
    ]

    print_capacity_leaderboard(
        title="Largest VRAM",
        entries=hardware_capacity[
            "largest_vram"
        ],
        unit="GiB",
    )

    print_capacity_leaderboard(
        title="Largest System Memory",
        entries=hardware_capacity[
            "largest_memory"
        ],
        unit="GB",
    )

    popularity = leaderboards[
        "popularity"
    ]

    print_popularity_leaderboard(
        title="Most Common GPUs",
        entries=popularity[
            "most_common_gpu"
        ],
    )

    print_popularity_leaderboard(
        title="Most Common CPUs",
        entries=popularity[
            "most_common_cpu"
        ],
    )

    print_section("Current Leaders")

    leaders = leaderboards["leaders"]

    fastest_pp512 = leaders[
        "fastest_pp512"
    ]

    fastest_tg128 = leaders[
        "fastest_tg128"
    ]

    largest_vram = leaders[
        "largest_vram"
    ]

    most_common_gpu = leaders[
        "most_common_gpu"
    ]

    if fastest_pp512:
        print(
            "Fastest pp512:  "
            f"{fastest_pp512['gpu_model']} "
            f"({format_number(fastest_pp512['value'])} "
            "tokens/sec)"
        )

    if fastest_tg128:
        print(
            "Fastest tg128:  "
            f"{fastest_tg128['gpu_model']} "
            f"({format_number(fastest_tg128['value'])} "
            "tokens/sec)"
        )

    if largest_vram:
        print(
            "Largest VRAM:   "
            f"{largest_vram['gpu_model']} "
            f"({format_number(largest_vram['value'])} GiB)"
        )

    if most_common_gpu:
        print(
            "Most common GPU: "
            f"{most_common_gpu['label']} "
            f"({most_common_gpu['count']} submission)"
        )


if __name__ == "__main__":
    main()