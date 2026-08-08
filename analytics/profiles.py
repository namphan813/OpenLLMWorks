"""
OpenLLMBench Hardware Profile Engine

Purpose:
Build reusable hardware profiles from the benchmark database.

Version:
0.7.0-dev3
"""

from collections import defaultdict

from analytics.statistics import (
    extract_result_rows,
    valid_number,
)


PROFILE_ENGINE_VERSION = "0.7.0-dev3"


def average(values):
    """Return the average of a list of numbers."""

    if not values:
        return None

    return sum(values) / len(values)


def build_gpu_profiles(database):
    """
    Build one profile for every GPU model.
    """

    rows = extract_result_rows(database)

    grouped = defaultdict(list)

    for row in rows:
        gpu = row.get("gpu_model", "Unknown")
        grouped[gpu].append(row)

    profiles = {}

    for gpu_model, gpu_rows in grouped.items():
        pp512_values = [
            row["pp512"]
            for row in gpu_rows
            if valid_number(row.get("pp512"))
        ]

        tg128_values = [
            row["tg128"]
            for row in gpu_rows
            if valid_number(row.get("tg128"))
        ]

        memory_values = [
            row["memory_gb"]
            for row in gpu_rows
            if valid_number(row.get("memory_gb"))
        ]

        memory_configurations = sorted(set(memory_values))

        vram_values = [
            row["vram_gib"]
            for row in gpu_rows
            if valid_number(row.get("vram_gib"))
        ]

        operating_systems = sorted(
            {
                row.get("operating_system")
                for row in gpu_rows
                if row.get("operating_system")
            }
        )

        gpu_vendors = sorted(
            {
                row.get("gpu_vendor")
                for row in gpu_rows
                if row.get("gpu_vendor")
            }
        )

        gpu_vendor = (
            gpu_vendors[0]
            if len(gpu_vendors) == 1
            else "Unknown"
        )

        benchmark_results = []

        for row in gpu_rows:
            benchmark_results.append(
                {
                    "submission_name": row.get(
                        "submission_name",
                        "Unknown",
                    ),
                    "cpu_model": row.get(
                        "cpu_model",
                        "Unknown",
                    ),
                    "pp512": row.get("pp512"),
                    "tg128": row.get("tg128"),
                    "operating_system": row.get(
                        "operating_system",
                        "Unknown",
                    ),
                    "memory_gb": row.get("memory_gb"),
                    "vram_gib": row.get("vram_gib"),
                }
            )

        profiles[gpu_model] = {
            "submission_count": len(gpu_rows),

            "gpu_vendor": gpu_vendor,

            "average_pp512": average(pp512_values),

            "average_tg128": average(tg128_values),

            "best_pp512": (
                max(pp512_values)
                if pp512_values
                else None
            ),

            "worst_pp512": (
                min(pp512_values)
                if pp512_values
                else None
            ),

            "average_memory_gb": average(memory_values),

            "memory_configurations_gb": memory_configurations,

            "average_vram_gib": average(vram_values),

            "operating_systems": operating_systems,

            "benchmark_results": benchmark_results,
        }

    return profiles