"""
OpenLLMWorks Leaderboard Engine

Purpose:
Builds reusable performance and hardware leaderboards from
the OpenLLMWorks benchmark database.

Version:
0.7.0-dev3
"""

from collections import Counter
from typing import Any

from analytics.statistics import (
    extract_result_rows,
    valid_number,
)


LEADERBOARD_MODULE_VERSION = "0.7.0-dev3"


# ------------------------------------------------------------
# BASIC HELPERS
# ------------------------------------------------------------

def clean_label(
    value: Any,
    fallback: str = "Unknown",
) -> str:
    """
    Return a usable display label.
    """

    if not isinstance(value, str):
        return fallback

    cleaned = value.strip()

    return cleaned if cleaned else fallback


def build_result_entry(
    row: dict,
    metric_name: str,
) -> dict:
    """
    Build one standardized leaderboard result entry.
    """

    return {
        "result_id": row.get("result_id"),
        "submission_name": clean_label(
            row.get("submission_name")
        ),
        "gpu_vendor": clean_label(
            row.get("gpu_vendor")
        ),
        "gpu_model": clean_label(
            row.get("gpu_model")
        ),
        "cpu_vendor": clean_label(
            row.get("cpu_vendor")
        ),
        "cpu_model": clean_label(
            row.get("cpu_model")
        ),
        "operating_system": clean_label(
            row.get("operating_system")
        ),
        "metric": metric_name,
        "value": row.get(metric_name),
    }


# ------------------------------------------------------------
# PERFORMANCE LEADERBOARDS
# ------------------------------------------------------------

def rank_by_metric(
    rows: list[dict],
    metric_name: str,
    limit: int = 10,
) -> list[dict]:
    """
    Rank benchmark results by one numeric metric.

    Higher values rank first.
    """

    valid_rows = [
        row
        for row in rows
        if valid_number(
            row.get(metric_name)
        )
    ]

    ranked_rows = sorted(
        valid_rows,
        key=lambda row: (
            -row[metric_name],
            clean_label(
                row.get("gpu_model")
            ).lower(),
            clean_label(
                row.get("submission_name")
            ).lower(),
        ),
    )

    leaderboard: list[dict] = []

    for position, row in enumerate(
        ranked_rows[:limit],
        start=1,
    ):
        entry = build_result_entry(
            row=row,
            metric_name=metric_name,
        )

        entry["rank"] = position

        leaderboard.append(entry)

    return leaderboard


# ------------------------------------------------------------
# GPU PROFILE LEADERBOARDS
# ------------------------------------------------------------

def rank_gpu_profiles_by_metric(
    gpu_profiles: dict,
    metric_name: str,
) -> list[dict]:
    """
    Rank aggregated GPU profiles by one numeric performance metric.

    Unlike rank_by_metric(), which ranks individual benchmark
    results, this function ranks canonical GPU variants produced
    by analytics.profiles.build_gpu_profiles().

    Higher values rank first.
    """

    ranked_profiles: list[dict] = []

    for profile_key, profile in gpu_profiles.items():
        value = profile.get(
            metric_name
        )

        if not valid_number(value):
            continue

        gpu_identity = profile.get(
            "gpu_identity",
            {},
        )

        if not isinstance(
            gpu_identity,
            dict,
        ):
            gpu_identity = {}

        ranked_profiles.append(
            {
                "profile_key": profile_key,
                "gpu_vendor": clean_label(
                    gpu_identity.get(
                        "vendor",
                        profile.get(
                            "gpu_vendor"
                        ),
                    )
                ),
                "gpu_model": clean_label(
                    gpu_identity.get(
                        "model",
                        profile.get(
                            "gpu_model"
                        ),
                    )
                ),
                "vram_gib": (
                    gpu_identity.get(
                        "vram_gib"
                    )
                ),
                "form_factor": clean_label(
                    gpu_identity.get(
                        "form_factor",
                        profile.get(
                            "gpu_form_factor"
                        ),
                    )
                ),
                "submission_count": (
                    profile.get(
                        "submission_count",
                        0,
                    )
                ),
                "metric": metric_name,
                "value": value,
            }
        )

    ranked_profiles.sort(
        key=lambda entry: (
            -entry["value"],
            entry[
                "gpu_model"
            ].lower(),
            entry[
                "profile_key"
            ].lower(),
        )
    )

    for position, entry in enumerate(
        ranked_profiles,
        start=1,
    ):
        entry["rank"] = position

    return ranked_profiles


# ------------------------------------------------------------
# CAPACITY LEADERBOARDS
# ------------------------------------------------------------

def rank_by_capacity(
    rows: list[dict],
    metric_name: str,
    limit: int = 10,
) -> list[dict]:
    """
    Rank systems by a hardware capacity value.

    Supported examples:

    - vram_gib
    - memory_gb
    """

    valid_rows = [
        row
        for row in rows
        if valid_number(
            row.get(metric_name)
        )
    ]

    ranked_rows = sorted(
        valid_rows,
        key=lambda row: (
            -row[metric_name],
            clean_label(
                row.get("gpu_model")
            ).lower(),
            clean_label(
                row.get("submission_name")
            ).lower(),
        ),
    )

    leaderboard: list[dict] = []

    for position, row in enumerate(
        ranked_rows[:limit],
        start=1,
    ):
        entry = build_result_entry(
            row=row,
            metric_name=metric_name,
        )

        entry["rank"] = position

        leaderboard.append(entry)

    return leaderboard


# ------------------------------------------------------------
# POPULARITY LEADERBOARDS
# ------------------------------------------------------------

def rank_common_values(
    rows: list[dict],
    field_name: str,
    limit: int = 10,
) -> list[dict]:
    """
    Rank the most commonly occurring values for one field.
    """

    values = [
        clean_label(
            row.get(field_name)
        )
        for row in rows
    ]

    counter = Counter(values)

    sorted_items = sorted(
        counter.items(),
        key=lambda item: (
            -item[1],
            item[0].lower(),
        ),
    )

    total = len(values)

    leaderboard: list[dict] = []

    for position, (
        label,
        count,
    ) in enumerate(
        sorted_items[:limit],
        start=1,
    ):
        percentage = (
            round(
                count / total * 100,
                2,
            )
            if total > 0
            else 0.0
        )

        leaderboard.append(
            {
                "rank": position,
                "label": label,
                "count": count,
                "percentage": percentage,
            }
        )

    return leaderboard


# ------------------------------------------------------------
# LEADERBOARD SUMMARY
# ------------------------------------------------------------

def first_entry(
    leaderboard: list[dict],
) -> dict | None:
    """
    Return the first leaderboard entry when available.
    """

    if not leaderboard:
        return None

    return leaderboard[0]


def build_leaderboards(
    database: dict,
    limit: int = 10,
) -> dict:
    """
    Build the complete OpenLLMWorks leaderboard report.

    The returned data contains no terminal formatting and can
    later be reused by:

    - command-line tools
    - websites
    - reports
    - APIs
    - monthly snapshots
    """

    rows = extract_result_rows(
        database
    )

    fastest_pp512 = rank_by_metric(
        rows=rows,
        metric_name="pp512",
        limit=limit,
    )

    fastest_tg128 = rank_by_metric(
        rows=rows,
        metric_name="tg128",
        limit=limit,
    )

    largest_vram = rank_by_capacity(
        rows=rows,
        metric_name="vram_gib",
        limit=limit,
    )

    largest_memory = rank_by_capacity(
        rows=rows,
        metric_name="memory_gb",
        limit=limit,
    )

    most_common_gpu = rank_common_values(
        rows=rows,
        field_name="gpu_model",
        limit=limit,
    )

    most_common_cpu = rank_common_values(
        rows=rows,
        field_name="cpu_model",
        limit=limit,
    )

    return {
        "leaderboard_version": (
            LEADERBOARD_MODULE_VERSION
        ),
        "database_result_count": len(rows),
        "limit": limit,
        "performance": {
            "fastest_pp512": fastest_pp512,
            "fastest_tg128": fastest_tg128,
        },
        "hardware_capacity": {
            "largest_vram": largest_vram,
            "largest_memory": largest_memory,
        },
        "popularity": {
            "most_common_gpu": most_common_gpu,
            "most_common_cpu": most_common_cpu,
        },
        "leaders": {
            "fastest_pp512": first_entry(
                fastest_pp512
            ),
            "fastest_tg128": first_entry(
                fastest_tg128
            ),
            "largest_vram": first_entry(
                largest_vram
            ),
            "largest_memory": first_entry(
                largest_memory
            ),
            "most_common_gpu": first_entry(
                most_common_gpu
            ),
            "most_common_cpu": first_entry(
                most_common_cpu
            ),
        },
    }