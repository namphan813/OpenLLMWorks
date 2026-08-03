"""
OpenLLMBench Historical Snapshot Engine

Purpose:
Builds reusable monthly historical snapshots from timestamped
OpenLLMBench benchmark observations.

Version:
0.8.0-dev1
"""

from typing import Any

from analytics.trends import build_trend_report


HISTORICAL_SNAPSHOT_VERSION = "0.8.0-dev1"


# ------------------------------------------------------------
# SAFE HELPERS
# ------------------------------------------------------------

def valid_number(
    value: Any,
) -> bool:
    """
    Return True for usable integer or floating-point values.
    """

    return (
        isinstance(value, (int, float))
        and not isinstance(value, bool)
    )


def percentage_change(
    previous: Any,
    current: Any,
) -> float | None:
    """
    Calculate percentage change between two numeric values.

    Returns None when either value is unavailable or when the
    previous value is zero.
    """

    if not valid_number(previous):
        return None

    if not valid_number(current):
        return None

    if previous == 0:
        return None

    return round(
        ((current - previous) / previous) * 100,
        2,
    )


# ------------------------------------------------------------
# MONTHLY SNAPSHOT BUILDING
# ------------------------------------------------------------

def build_monthly_snapshot(
    month: dict,
    previous_month: dict | None = None,
) -> dict:
    """
    Convert one monthly trend bucket into a historical snapshot.
    """

    previous_pp512 = (
        previous_month.get("average_pp512")
        if previous_month
        else None
    )

    previous_tg128 = (
        previous_month.get("average_tg128")
        if previous_month
        else None
    )

    previous_results = (
        previous_month.get("result_count")
        if previous_month
        else None
    )

    return {
        "month": month["month"],
        "result_count": month["result_count"],
        "unique_gpu_models": (
            month["unique_gpu_models"]
        ),
        "unique_cpu_models": (
            month["unique_cpu_models"]
        ),
        "performance": {
            "average_pp512": (
                month["average_pp512"]
            ),
            "average_tg128": (
                month["average_tg128"]
            ),
            "fastest_pp512": (
                month["fastest_pp512"]
            ),
            "fastest_tg128": (
                month["fastest_tg128"]
            ),
        },
        "changes": {
            "result_count_change": (
                month["result_count"]
                - previous_results
                if previous_results is not None
                else None
            ),
            "result_count_percent_change": (
                percentage_change(
                    previous_results,
                    month["result_count"],
                )
            ),
            "average_pp512_percent_change": (
                percentage_change(
                    previous_pp512,
                    month["average_pp512"],
                )
            ),
            "average_tg128_percent_change": (
                percentage_change(
                    previous_tg128,
                    month["average_tg128"],
                )
            ),
        },
        "comparison_available": (
            previous_month is not None
        ),
        "previous_month": (
            previous_month["month"]
            if previous_month
            else None
        ),
    }


# ------------------------------------------------------------
# COMPLETE HISTORICAL REPORT
# ------------------------------------------------------------

def build_historical_snapshots(
    database: dict,
    *,
    start: str | None = None,
    end: str | None = None,
    gpu_model: str | None = None,
    gpu_vendor: str | None = None,
) -> dict:
    """
    Build monthly historical snapshots from the database.

    Optional filters are passed directly to the Trend Engine.
    """

    trend_report = build_trend_report(
        database,
        start=start,
        end=end,
        gpu_model=gpu_model,
        gpu_vendor=gpu_vendor,
    )

    monthly_data = trend_report["monthly"]

    snapshots: list[dict] = []

    for index, month in enumerate(
        monthly_data
    ):
        previous_month = (
            monthly_data[index - 1]
            if index > 0
            else None
        )

        snapshots.append(
            build_monthly_snapshot(
                month=month,
                previous_month=previous_month,
            )
        )

    return {
        "historical_snapshot_version": (
            HISTORICAL_SNAPSHOT_VERSION
        ),
        "snapshot_type": "monthly_history",
        "filters": trend_report["filters"],
        "database_result_count": (
            trend_report[
                "database_result_count"
            ]
        ),
        "timestamped_result_count": (
            trend_report[
                "timestamped_result_count"
            ]
        ),
        "snapshot_count": len(snapshots),
        "first_month": (
            snapshots[0]["month"]
            if snapshots
            else None
        ),
        "last_month": (
            snapshots[-1]["month"]
            if snapshots
            else None
        ),
        "snapshots": snapshots,
    }