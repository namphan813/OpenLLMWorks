"""
OpenLLMWorks Trend Analytics Engine

Purpose:
Builds time-aware benchmark observations and monthly trend
summaries from the OpenLLMWorks database.

Version:
0.8.0-dev1
"""

from collections import Counter, defaultdict
from datetime import datetime, timezone
from typing import Any

from parser.timestamps import normalize_timestamp


TREND_MODULE_VERSION = "0.8.0-dev1"


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


def average(
    values: list[float],
) -> float | None:
    """
    Return a rounded average when values are available.
    """

    if not values:
        return None

    return round(
        sum(values) / len(values),
        2,
    )


def normalize_optional_timestamp(
    value: Any,
) -> str | None:
    """
    Normalize a timestamp without failing the full trend report.

    Invalid or unavailable timestamps return None.
    """

    try:
        return normalize_timestamp(value)

    except ValueError:
        return None


def timestamp_to_datetime(
    timestamp: str,
) -> datetime:
    """
    Convert one normalized ISO timestamp to a UTC datetime.
    """

    parsed = datetime.fromisoformat(
        timestamp
    )

    return parsed.astimezone(
        timezone.utc
    )


def month_key(
    timestamp: str,
) -> str:
    """
    Return a YYYY-MM bucket for one normalized timestamp.
    """

    parsed = timestamp_to_datetime(
        timestamp
    )

    return parsed.strftime("%Y-%m")


# ------------------------------------------------------------
# TIMESTAMP SELECTION
# ------------------------------------------------------------

def choose_result_timestamp(
    record: dict,
) -> tuple[str | None, str | None]:
    """
    Select the best available timestamp for one result.

    Priority:

    1. benchmark_timestamp
    2. submitted_at
    3. imported_at
    4. processed_at

    Returns:
        (normalized_timestamp, source_name)
    """

    benchmark = record.get(
        "benchmark",
        {}
    )

    submission = record.get(
        "submission",
        {}
    )

    metadata = record.get(
        "metadata",
        {}
    )

    candidates = [
        (
            "benchmark_timestamp",
            benchmark.get(
                "benchmark_timestamp"
            ),
        ),
        (
            "submitted_at",
            submission.get(
                "submitted_at"
            ),
        ),
        (
            "imported_at",
            metadata.get(
                "imported_at"
            ),
        ),
        (
            "processed_at",
            metadata.get(
                "processed_at"
            ),
        ),
    ]

    for source_name, value in candidates:
        normalized = (
            normalize_optional_timestamp(
                value
            )
        )

        if normalized is not None:
            return normalized, source_name

    return None, None


# ------------------------------------------------------------
# OBSERVATION EXTRACTION
# ------------------------------------------------------------

def extract_trend_observations(
    database: dict,
) -> list[dict]:
    """
    Convert database results into timestamped trend observations.
    """

    observations: list[dict] = []

    results = database.get(
        "results",
        []
    )

    if not isinstance(results, list):
        raise ValueError(
            "Database results must be a list."
        )

    for record in results:
        if not isinstance(record, dict):
            continue

        timestamp, timestamp_source = (
            choose_result_timestamp(
                record
            )
        )

        if timestamp is None:
            continue

        hardware = record.get(
            "hardware",
            {}
        )

        benchmark = record.get(
            "benchmark",
            {}
        )

        submission = record.get(
            "submission",
            {}
        )

        averages = benchmark.get(
            "average",
            {}
        )

        protocol = benchmark.get(
            "protocol",
            {}
        )

        llama_cpp = benchmark.get(
            "llama_cpp",
            {}
        )

        observation = {
            "result_id": record.get(
                "result_id"
            ),
            "timestamp": timestamp,
            "timestamp_source": (
                timestamp_source
            ),
            "month": month_key(
                timestamp
            ),
            "submission_name": (
                submission.get(
                    "submission_name",
                    "Unknown",
                )
            ),
            "gpu_vendor": hardware.get(
                "gpu_vendor",
                "Unknown",
            ),
            "gpu_model": hardware.get(
                "gpu_model",
                "Unknown",
            ),
            "cpu_vendor": hardware.get(
                "cpu_vendor",
                "Unknown",
            ),
            "cpu_model": hardware.get(
                "cpu_model",
                "Unknown",
            ),
            "operating_system": (
                hardware.get(
                    "operating_system",
                    "Unknown",
                )
            ),
            "pp512": averages.get(
                "pp512"
            ),
            "tg128": averages.get(
                "tg128"
            ),
            "protocol_id": protocol.get(
                "id"
            ),
            "llama_cpp_commit": (
                llama_cpp.get(
                    "commit"
                )
            ),
            "llama_cpp_build": (
                llama_cpp.get(
                    "build"
                )
            ),
        }

        observations.append(
            observation
        )

    return sorted(
        observations,
        key=lambda item: (
            item["timestamp"],
            str(item.get("result_id")),
        ),
    )


# ------------------------------------------------------------
# DATE FILTERING
# ------------------------------------------------------------

def filter_observations(
    observations: list[dict],
    *,
    start: str | None = None,
    end: str | None = None,
    gpu_model: str | None = None,
    gpu_vendor: str | None = None,
) -> list[dict]:
    """
    Filter observations by date and optional GPU fields.

    Start and end are inclusive.
    """

    normalized_start = (
        normalize_optional_timestamp(
            start
        )
        if start is not None
        else None
    )

    normalized_end = (
        normalize_optional_timestamp(
            end
        )
        if end is not None
        else None
    )

    if (
        start is not None
        and normalized_start is None
    ):
        raise ValueError(
            f"Invalid start timestamp: {start!r}"
        )

    if (
        end is not None
        and normalized_end is None
    ):
        raise ValueError(
            f"Invalid end timestamp: {end!r}"
        )

    start_datetime = (
        timestamp_to_datetime(
            normalized_start
        )
        if normalized_start
        else None
    )

    end_datetime = (
        timestamp_to_datetime(
            normalized_end
        )
        if normalized_end
        else None
    )

    filtered: list[dict] = []

    for observation in observations:
        observation_datetime = (
            timestamp_to_datetime(
                observation["timestamp"]
            )
        )

        if (
            start_datetime is not None
            and observation_datetime
            < start_datetime
        ):
            continue

        if (
            end_datetime is not None
            and observation_datetime
            > end_datetime
        ):
            continue

        if (
            gpu_model is not None
            and observation.get(
                "gpu_model"
            )
            != gpu_model
        ):
            continue

        if (
            gpu_vendor is not None
            and observation.get(
                "gpu_vendor"
            )
            != gpu_vendor
        ):
            continue

        filtered.append(
            observation
        )

    return filtered


# ------------------------------------------------------------
# MONTHLY AGGREGATION
# ------------------------------------------------------------

def build_monthly_trends(
    observations: list[dict],
) -> list[dict]:
    """
    Aggregate timestamped observations into monthly buckets.
    """

    grouped: dict[
        str,
        list[dict],
    ] = defaultdict(list)

    for observation in observations:
        grouped[
            observation["month"]
        ].append(
            observation
        )

    monthly_trends: list[dict] = []

    for month in sorted(grouped):
        month_rows = grouped[month]

        pp512_values = [
            row["pp512"]
            for row in month_rows
            if valid_number(
                row.get("pp512")
            )
        ]

        tg128_values = [
            row["tg128"]
            for row in month_rows
            if valid_number(
                row.get("tg128")
            )
        ]

        gpu_models = {
            row.get(
                "gpu_model",
                "Unknown",
            )
            for row in month_rows
        }

        cpu_models = {
            row.get(
                "cpu_model",
                "Unknown",
            )
            for row in month_rows
        }

        monthly_trends.append(
            {
                "month": month,
                "result_count": len(
                    month_rows
                ),
                "unique_gpu_models": len(
                    gpu_models
                ),
                "unique_cpu_models": len(
                    cpu_models
                ),
                "average_pp512": average(
                    pp512_values
                ),
                "average_tg128": average(
                    tg128_values
                ),
                "fastest_pp512": (
                    max(pp512_values)
                    if pp512_values
                    else None
                ),
                "fastest_tg128": (
                    max(tg128_values)
                    if tg128_values
                    else None
                ),
            }
        )

    return monthly_trends


# ------------------------------------------------------------
# COMPLETE TREND REPORT
# ------------------------------------------------------------

def build_trend_report(
    database: dict,
    *,
    start: str | None = None,
    end: str | None = None,
    gpu_model: str | None = None,
    gpu_vendor: str | None = None,
) -> dict:
    """
    Build a complete time-aware trend report.
    """

    all_observations = (
        extract_trend_observations(
            database
        )
    )

    observations = filter_observations(
        all_observations,
        start=start,
        end=end,
        gpu_model=gpu_model,
        gpu_vendor=gpu_vendor,
    )

    timestamp_sources = Counter(
        observation[
            "timestamp_source"
        ]
        for observation in observations
    )

    months = build_monthly_trends(
        observations
    )

    first_timestamp = (
        observations[0]["timestamp"]
        if observations
        else None
    )

    last_timestamp = (
        observations[-1]["timestamp"]
        if observations
        else None
    )

    return {
        "trend_version": (
            TREND_MODULE_VERSION
        ),
        "filters": {
            "start": start,
            "end": end,
            "gpu_model": gpu_model,
            "gpu_vendor": gpu_vendor,
        },
        "database_result_count": len(
            database.get(
                "results",
                []
            )
        ),
        "timestamped_result_count": len(
            all_observations
        ),
        "filtered_result_count": len(
            observations
        ),
        "untimestamped_result_count": (
            len(
                database.get(
                    "results",
                    []
                )
            )
            - len(all_observations)
        ),
        "first_timestamp": (
            first_timestamp
        ),
        "last_timestamp": (
            last_timestamp
        ),
        "timestamp_source_counts": dict(
            timestamp_sources
        ),
        "monthly": months,
        "observations": observations,
    }