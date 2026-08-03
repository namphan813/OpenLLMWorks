"""
OpenLLMBench Hardware Profile Engine

Purpose:
Build reusable hardware profiles from the benchmark database.

Version:
0.7.0-dev1
"""

from collections import defaultdict

from analytics.statistics import (
    extract_result_rows,
    valid_number,
)


PROFILE_ENGINE_VERSION = "0.7.0-dev1"


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

        profiles[gpu_model] = {

            "submission_count": len(gpu_rows),

            "average_pp512": average(pp512_values),

            "average_tg128": average(tg128_values),

            "best_pp512": max(pp512_values)
            if pp512_values else None,

            "worst_pp512": min(pp512_values)
            if pp512_values else None,

            "average_memory_gb": average(memory_values),

            "average_vram_gib": average(vram_values),

            "operating_systems": operating_systems,

        }

    return profiles