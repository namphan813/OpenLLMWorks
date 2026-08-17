from pathlib import Path
import json


def publish_homepage(
    output_directory: Path,
    generated_at: str,
    publisher_name: str,
    publisher_version: str,
    contract_version: str,
    statistics_report: dict,
):
    """
    Publish homepage.json using real OpenLLMBench analytics.
    """

    database_stats = statistics_report["database"]
    submission_stats = statistics_report["submissions"]
    hardware_stats = statistics_report["hardware"]
    performance_stats = statistics_report["performance"]

    gpu_model_counts = hardware_stats.get(
        "gpu_model_counts",
        {},
    )

    homepage = {
        "contractVersion": contract_version,
        "generatedAt": generated_at,
        "generator": {
            "name": publisher_name,
            "version": publisher_version,
        },
        "stats": {
            "benchmarkResults": (
                database_stats["total_results"]
            ),
            "gpuModels": len(
                gpu_model_counts
            ),
            "cpuModels": len(
                hardware_stats.get(
                    "cpu_model_counts",
                    {},
                )
            ),
            "importEvents": (
                submission_stats[
                    "import_event_count"
                ]
            ),
            "averagePp512": (
                performance_stats[
                    "average_pp512"
                ]
            ),
            "medianPp512": (
                performance_stats[
                    "median_pp512"
                ]
            ),
            "minPp512": (
                performance_stats[
                    "min_pp512"
                ]
            ),
            "maxPp512": (
                performance_stats[
                    "max_pp512"
                ]
            ),
            "averageTg128": (
                performance_stats[
                    "average_tg128"
                ]
            ),
            "medianTg128": (
                performance_stats[
                    "median_tg128"
                ]
            ),
            "minTg128": (
                performance_stats[
                    "min_tg128"
                ]
            ),
            "maxTg128": (
                performance_stats[
                    "max_tg128"
                ]
            ),
            "averageVramGib": (
                hardware_stats[
                    "average_vram_gib"
                ]
            ),
            "minVramGib": (
                hardware_stats[
                    "min_vram_gib"
                ]
            ),
            "maxVramGib": (
                hardware_stats[
                    "max_vram_gib"
                ]
            ),
            "averageMemoryGb": (
                hardware_stats[
                    "average_memory_gb"
                ]
            ),
            "minMemoryGb": (
                hardware_stats[
                    "min_memory_gb"
                ]
            ),
            "maxMemoryGb": (
                hardware_stats[
                    "max_memory_gb"
                ]
            ),
        },
        "featuredStory": {
            "title": (
                "The GTX 1650 is OpenLLMBench's "
                "first recorded GPU."
            ),
            "description": (
                "This benchmark established the first "
                "historical performance reference point "
                "in the OpenLLMBench database."
            ),
            "snapshot": "2026-08-02 14:17 UTC",
            "badge": "Data Snapshot",
        },
    }

    homepage_file = (
        output_directory
        / "homepage.json"
    )

    with homepage_file.open(
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(
            homepage,
            file,
            indent=4,
        )
        file.write("\n")

    return homepage_file