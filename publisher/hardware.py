"""
OpenLLMBench Hardware Publisher

Purpose:
Build the public hardware data contract consumed by the OpenLLMBench
website Hardware Explorer.

The publisher does not calculate benchmark analytics itself.
It packages reusable GPU profile data produced by analytics/profiles.py
into a stable public JSON structure.

Version:
0.3
"""

from datetime import datetime, timezone
import json
from pathlib import Path

from analytics.profiles import build_gpu_profiles


HARDWARE_PUBLISHER_VERSION = "0.3"
HARDWARE_CONTRACT_VERSION = "1.2"


def utc_timestamp() -> str:
    """
    Return the current UTC timestamp in ISO 8601 format.
    """

    return datetime.now(timezone.utc).isoformat()


def build_hardware_payload(database: dict) -> dict:
    """
    Build the public Hardware Explorer payload.
    """

    generated_at = utc_timestamp()

    gpu_profiles = build_gpu_profiles(database)

    hardware = []

    for gpu_model, profile in sorted(gpu_profiles.items()):
        hardware.append(
            {
                "gpuVendor": profile.get(
                    "gpu_vendor",
                    "Unknown",
                ),
                "gpuModel": gpu_model,
                "submissionCount": profile.get(
                    "submission_count",
                    0,
                ),
                "performance": {
                    "averagePp512": profile.get(
                        "average_pp512"
                    ),
                    "averageTg128": profile.get(
                        "average_tg128"
                    ),
                    "bestPp512": profile.get(
                        "best_pp512"
                    ),
                    "worstPp512": profile.get(
                        "worst_pp512"
                    ),
                },
                "system": {
                    "averageMemoryGb": profile.get(
                        "average_memory_gb"
                    ),
                    "averageVramGib": profile.get(
                        "average_vram_gib"
                    ),
                    "operatingSystems": profile.get(
                        "operating_systems",
                        [],
                    ),
                },
                "benchmarkResults": [
                    {
                        "submissionName": result.get(
                            "submission_name",
                            "Unknown",
                        ),
                        "cpuModel": result.get(
                            "cpu_model",
                            "Unknown",
                        ),
                        "pp512": result.get(
                            "pp512"
                        ),
                        "tg128": result.get(
                            "tg128"
                        ),
                        "operatingSystem": result.get(
                            "operating_system",
                            "Unknown",
                        ),
                        "memoryGb": result.get(
                            "memory_gb"
                        ),
                        "vramGib": result.get(
                            "vram_gib"
                        ),
                    }
                    for result in profile.get(
                        "benchmark_results",
                        [],
                    )
                ],
            }
        )

    return {
        "contractVersion": HARDWARE_CONTRACT_VERSION,
        "generatedAt": generated_at,
        "generator": {
            "name": "OpenLLMBench Hardware Publisher",
            "version": HARDWARE_PUBLISHER_VERSION,
        },
        "summary": {
            "gpuModels": len(hardware),
            "benchmarkResults": sum(
                item["submissionCount"]
                for item in hardware
            ),
        },
        "hardware": hardware,
    }


def publish_hardware(
    database: dict,
    output_directory: Path,
) -> Path:
    """
    Generate hardware.json in the supplied output directory.
    """

    output_directory.mkdir(
        parents=True,
        exist_ok=True,
    )

    payload = build_hardware_payload(database)

    hardware_file = (
        output_directory
        / "hardware.json"
    )

    with hardware_file.open(
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(
            payload,
            file,
            indent=4,
        )

    return hardware_file