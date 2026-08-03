"""
OpenLLMBench Hardware Profile Viewer

Version:
0.7.0-dev1
"""

from pathlib import Path

from parser.database import load_database
from analytics.profiles import build_gpu_profiles

DATABASE_FILE = Path("database/benchmark_database.json")
PARSER_VERSION = "0.7.0-dev1"


def print_profile(name: str, profile: dict) -> None:

    print("=" * 60)
    print("Hardware Profile")
    print("=" * 60)
    print()

    print(f"GPU: {name}")
    print()

    print("-" * 60)
    print("Community")
    print("-" * 60)

    print(f"Submissions: {profile['submission_count']}")

    operating_systems = profile["operating_systems"]

    if operating_systems:
        print("Operating Systems:")

        for operating_system in operating_systems:
            print(f"  • {operating_system}")

    print()

    print("-" * 60)
    print("Performance")
    print("-" * 60)

    print(f"Average pp512 : {profile['average_pp512']:.2f}")
    print(f"Average tg128 : {profile['average_tg128']:.2f}")
    print(f"Best pp512    : {profile['best_pp512']:.2f}")
    print(f"Worst pp512   : {profile['worst_pp512']:.2f}")

    print()

    print("-" * 60)
    print("Hardware")
    print("-" * 60)

    print(f"Average RAM   : {profile['average_memory_gb']:.2f} GB")
    print(f"Average VRAM  : {profile['average_vram_gib']:.2f} GiB")

    print()


def main():

    print("OpenLLMBench Hardware Profiles")
    print("Profile Viewer v0.7.0-dev1")
    print()

    database = load_database(
        DATABASE_FILE,
        PARSER_VERSION,
    )

    profiles = build_gpu_profiles(database)

    print(f"Profiles discovered: {len(profiles)}")
    print()

    for gpu_name in sorted(profiles):
        print_profile(
            gpu_name,
            profiles[gpu_name],
        )


if __name__ == "__main__":
    main()