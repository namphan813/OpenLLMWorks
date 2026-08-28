"""
OpenLLMWorks Statistics

Purpose:
Command-line statistics viewer for the OpenLLMWorks
benchmark database.

Version:
0.7.0-dev2
"""

from pathlib import Path

from analytics.statistics import build_statistics
from parser.database import load_database
from parser.validator import validate_database_file


STATS_VERSION = "0.7.0-dev2"

PROJECT_FOLDER = Path(__file__).resolve().parent

DATABASE_FILE = (
    PROJECT_FOLDER
    / "database"
    / "benchmark_database.json"
)


def print_section(title: str) -> None:
    """Print one report section heading."""

    print()
    print("=" * 60)
    print(title)
    print("=" * 60)


def print_counter(
    title: str,
    counter: dict,
) -> None:
    """Print a labeled collection of counts."""

    print()
    print(title)

    if not counter:
        print("  None")
        return

    for label, count in counter.items():
        print(f"  {label:<25} {count}")


def format_metric(
    value: object,
) -> str:
    """Format a numeric metric safely."""

    if isinstance(value, (int, float)):
        return f"{value:.2f}"

    return "Unavailable"


def main() -> None:
    """Validate the database and print aggregate statistics."""

    print("OpenLLMWorks Statistics")
    print(f"Statistics Viewer v{STATS_VERSION}")

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
            parser_version=STATS_VERSION,
        )

    except ValueError as error:
        print()
        print(f"ERROR: {error}")
        return

    stats = build_statistics(database)

    database_stats = stats["database"]

    print_section("Database")

    print(
        f"Project:          "
        f"{database_stats['project']}"
    )

    print(
        f"Schema version:   "
        f"{database_stats['schema_version']}"
    )

    print(
        f"Parser version:   "
        f"{database_stats['parser_version']}"
    )

    print(
        f"Results:          "
        f"{database_stats['total_results']}"
    )

    hardware = stats["hardware"]

    print_section("GPU Vendors")

    gpu_counts = hardware[
        "gpu_vendor_counts"
    ]

    gpu_percentages = hardware[
        "gpu_vendor_percentages"
    ]

    if not gpu_counts:
        print("No GPU vendor data available.")

    else:
        for vendor, count in gpu_counts.items():
            percentage = gpu_percentages.get(
                vendor,
                0.0,
            )

            print(
                f"{vendor:<15}"
                f"{count:>5}"
                f" ({percentage:.2f}%)"
            )

    print_counter(
        "CPU Vendors",
        hardware["cpu_vendor_counts"],
    )

    print_counter(
        "Operating Systems",
        hardware[
            "operating_system_counts"
        ],
    )

    print_counter(
        "GPU Models",
        hardware["gpu_model_counts"],
    )

    print_counter(
        "Backends",
        hardware["backend_counts"],
    )

    print_section("Hardware Capacity")

    print(
        "Average VRAM:     "
        f"{format_metric(hardware['average_vram_gib'])} GiB"
    )

    print(
        "VRAM range:       "
        f"{format_metric(hardware['min_vram_gib'])} - "
        f"{format_metric(hardware['max_vram_gib'])} GiB"
    )

    print(
        "Average memory:   "
        f"{format_metric(hardware['average_memory_gb'])} GB"
    )

    print(
        "Memory range:     "
        f"{format_metric(hardware['min_memory_gb'])} - "
        f"{format_metric(hardware['max_memory_gb'])} GB"
    )

    performance = stats["performance"]

    print_section("Performance")

    print(
        "Average pp512:    "
        f"{format_metric(performance['average_pp512'])} "
        "tokens/sec"
    )

    print(
        "Median pp512:     "
        f"{format_metric(performance['median_pp512'])} "
        "tokens/sec"
    )

    print(
        "pp512 range:      "
        f"{format_metric(performance['min_pp512'])} - "
        f"{format_metric(performance['max_pp512'])} "
        "tokens/sec"
    )

    print()

    print(
        "Average tg128:    "
        f"{format_metric(performance['average_tg128'])} "
        "tokens/sec"
    )

    print(
        "Median tg128:     "
        f"{format_metric(performance['median_tg128'])} "
        "tokens/sec"
    )

    print(
        "tg128 range:      "
        f"{format_metric(performance['min_tg128'])} - "
        f"{format_metric(performance['max_tg128'])} "
        "tokens/sec"
    )

    fastest_pp512 = performance[
        "fastest_pp512"
    ]

    if fastest_pp512:
        print()
        print("Fastest pp512")
        print(
            f"  Submission: "
            f"{fastest_pp512['submission_name']}"
        )
        print(
            f"  GPU:        "
            f"{fastest_pp512['gpu_model']}"
        )
        print(
            f"  Result:     "
            f"{format_metric(fastest_pp512['value'])} "
            "tokens/sec"
        )

    fastest_tg128 = performance[
        "fastest_tg128"
    ]

    if fastest_tg128:
        print()
        print("Fastest tg128")
        print(
            f"  Submission: "
            f"{fastest_tg128['submission_name']}"
        )
        print(
            f"  GPU:        "
            f"{fastest_tg128['gpu_model']}"
        )
        print(
            f"  Result:     "
            f"{format_metric(fastest_tg128['value'])} "
            "tokens/sec"
        )

    submissions = stats["submissions"]

    print_section("Submission Status")

    print_counter(
        "Benchmark Status",
        submissions[
            "benchmark_status_counts"
        ],
    )

    print(
        "\nImport events: "
        f"{submissions['import_event_count']}"
    )

    print_counter(
        "Import Status",
        submissions[
            "import_status_counts"
        ],
    )


if __name__ == "__main__":
    main()