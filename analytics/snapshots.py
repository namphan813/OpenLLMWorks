"""
OpenLLMWorks Snapshot Engine

Purpose:
Builds a reusable current-state snapshot of the OpenLLMWorks
database for terminal reports, milestone infographics,
websites, and future monthly summaries.

Version:
0.7.0-dev1
"""

from typing import Any

from analytics.facts import build_interesting_facts
from analytics.leaderboards import build_leaderboards
from analytics.profiles import build_gpu_profiles
from analytics.statistics import build_statistics


SNAPSHOT_MODULE_VERSION = "0.7.0-dev1"


# ------------------------------------------------------------
# SAFE HELPERS
# ------------------------------------------------------------

def first_entry(
    values: dict,
) -> tuple[str, Any] | None:
    """
    Return the first item from an ordered dictionary.
    """

    if not values:
        return None

    key = next(iter(values))
    return key, values[key]


def format_leader(
    leader: dict | None,
) -> dict | None:
    """
    Return a compact representation of one leaderboard leader.
    """

    if not leader:
        return None

    return {
        "submission_name": leader.get(
            "submission_name"
        ),
        "gpu_model": leader.get(
            "gpu_model"
        ),
        "cpu_model": leader.get(
            "cpu_model"
        ),
        "value": leader.get("value"),
        "result_id": leader.get(
            "result_id"
        ),
    }


# ------------------------------------------------------------
# SNAPSHOT SECTIONS
# ------------------------------------------------------------

def build_database_snapshot(
    statistics_report: dict,
) -> dict:
    """
    Build database-level snapshot information.
    """

    database = statistics_report["database"]
    submissions = statistics_report[
        "submissions"
    ]

    import_statuses = submissions[
        "import_status_counts"
    ]

    return {
        "project": database["project"],
        "schema_version": database[
            "schema_version"
        ],
        "parser_version": database[
            "parser_version"
        ],
        "database_generated_at": database[
            "generated_at"
        ],
        "total_results": database[
            "total_results"
        ],
        "import_events": submissions[
            "import_event_count"
        ],
        "results_added": import_statuses.get(
            "added",
            0,
        ),
        "duplicates_detected": (
            import_statuses.get(
                "duplicate",
                0,
            )
        ),
    }


def build_community_snapshot(
    statistics_report: dict,
    gpu_profiles: dict,
) -> dict:
    """
    Build a compact summary of represented hardware.
    """

    hardware = statistics_report["hardware"]

    most_common_gpu = first_entry(
        hardware["gpu_model_counts"]
    )

    most_common_cpu = first_entry(
        hardware["cpu_model_counts"]
    )

    most_common_os = first_entry(
        hardware[
            "operating_system_counts"
        ]
    )

    return {
        "unique_gpu_models": len(
            hardware["gpu_model_counts"]
        ),
        "unique_cpu_models": len(
            hardware["cpu_model_counts"]
        ),
        "unique_operating_systems": len(
            hardware[
                "operating_system_counts"
            ]
        ),
        "gpu_profiles_available": len(
            gpu_profiles
        ),
        "most_common_gpu": (
            {
                "model": most_common_gpu[0],
                "count": most_common_gpu[1],
            }
            if most_common_gpu
            else None
        ),
        "most_common_cpu": (
            {
                "model": most_common_cpu[0],
                "count": most_common_cpu[1],
            }
            if most_common_cpu
            else None
        ),
        "most_common_operating_system": (
            {
                "name": most_common_os[0],
                "count": most_common_os[1],
            }
            if most_common_os
            else None
        ),
    }


def build_hardware_snapshot(
    statistics_report: dict,
    leaderboard_report: dict,
) -> dict:
    """
    Build hardware capacity and vendor information.
    """

    hardware = statistics_report["hardware"]
    leaders = leaderboard_report["leaders"]

    largest_vram = leaders.get(
        "largest_vram"
    )

    largest_memory = leaders.get(
        "largest_memory"
    )

    return {
        "gpu_vendor_counts": hardware[
            "gpu_vendor_counts"
        ],
        "cpu_vendor_counts": hardware[
            "cpu_vendor_counts"
        ],
        "average_vram_gib": hardware[
            "average_vram_gib"
        ],
        "average_memory_gb": hardware[
            "average_memory_gb"
        ],
        "largest_vram": (
            {
                "gpu_model": largest_vram[
                    "gpu_model"
                ],
                "capacity_gib": largest_vram[
                    "value"
                ],
                "submission_name": (
                    largest_vram[
                        "submission_name"
                    ]
                ),
            }
            if largest_vram
            else None
        ),
        "largest_system_memory": (
            {
                "submission_name": (
                    largest_memory[
                        "submission_name"
                    ]
                ),
                "gpu_model": largest_memory[
                    "gpu_model"
                ],
                "capacity_gb": largest_memory[
                    "value"
                ],
            }
            if largest_memory
            else None
        ),
    }


def build_performance_snapshot(
    statistics_report: dict,
    leaderboard_report: dict,
) -> dict:
    """
    Build current performance summary information.
    """

    performance = statistics_report[
        "performance"
    ]

    leaders = leaderboard_report["leaders"]

    return {
        "average_pp512": performance[
            "average_pp512"
        ],
        "average_tg128": performance[
            "average_tg128"
        ],
        "fastest_pp512": format_leader(
            leaders.get("fastest_pp512")
        ),
        "fastest_tg128": format_leader(
            leaders.get("fastest_tg128")
        ),
    }


# ------------------------------------------------------------
# COMPLETE SNAPSHOT
# ------------------------------------------------------------

def build_snapshot(
    database: dict,
    *,
    snapshot_name: str = (
        "OpenLLMWorks Weekend Snapshot"
    ),
) -> dict:
    """
    Build a complete current-state OpenLLMWorks snapshot.

    This version intentionally reports the present database state.
    Time-period comparisons will be added after submission and
    benchmark timestamps become part of the database schema.
    """

    statistics_report = build_statistics(
        database
    )

    leaderboard_report = build_leaderboards(
        database
    )

    gpu_profiles = build_gpu_profiles(
        database
    )

    facts_report = build_interesting_facts(
        database
    )

    return {
        "snapshot_version": (
            SNAPSHOT_MODULE_VERSION
        ),
        "snapshot_name": snapshot_name,
        "snapshot_type": "current_state",
        "time_comparison_available": False,
        "database": build_database_snapshot(
            statistics_report
        ),
        "community": build_community_snapshot(
            statistics_report,
            gpu_profiles,
        ),
        "hardware": build_hardware_snapshot(
            statistics_report,
            leaderboard_report,
        ),
        "performance": (
            build_performance_snapshot(
                statistics_report,
                leaderboard_report,
            )
        ),
        "interesting_facts": facts_report[
            "facts"
        ],
    }