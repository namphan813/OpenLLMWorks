"""
OpenLLMBench Hardware Publisher

Purpose:
Build the public hardware data contract consumed by the OpenLLMBench
website Hardware Explorer.

The publisher does not calculate benchmark analytics itself.
It packages reusable GPU profile data produced by analytics/profiles.py
into a stable public JSON structure.

Version:
0.6
"""

from datetime import datetime, timezone
import json
from pathlib import Path
import re

from analytics.profiles import build_gpu_profiles


HARDWARE_PUBLISHER_VERSION = "0.6"
HARDWARE_CONTRACT_VERSION = "1.5"


def utc_timestamp() -> str:
    """
    Return the current UTC timestamp in ISO 8601 format.
    """

    return datetime.now(timezone.utc).isoformat()


def slugify(value: str) -> str:
    """
    Convert a value into a URL-safe slug component.
    """

    normalized = str(value).strip().lower()

    normalized = re.sub(
        r"[^a-z0-9]+",
        "-",
        normalized,
    )

    return normalized.strip("-")


def format_vram_slug(vram_gib) -> str | None:
    """
    Convert VRAM capacity into a compact slug component.

    Examples:
    4.0  -> 4gb
    12.0 -> 12gb
    1.5  -> 1-5gb
    """

    if vram_gib is None:
        return None

    try:
        numeric_vram = float(vram_gib)
    except (TypeError, ValueError):
        return None

    if numeric_vram.is_integer():
        value = str(int(numeric_vram))
    else:
        value = (
            f"{numeric_vram:g}"
            .replace(".", "-")
        )

    return f"{value}gb"


def build_variant_id(
    gpu_model: str,
    vram_gib,
    form_factor: str,
) -> str:
    """
    Build the stable public identifier for a GPU variant.

    Identity currently includes:
    - GPU model
    - VRAM capacity
    - form factor when known

    Unknown form factors are intentionally omitted from the public ID.
    """

    components = [
        slugify(gpu_model),
    ]

    vram_component = format_vram_slug(
        vram_gib
    )

    if vram_component:
        components.append(
            vram_component
        )

    normalized_form_factor = (
        str(form_factor or "")
        .strip()
    )

    if (
        normalized_form_factor
        and normalized_form_factor.lower()
        != "unknown"
    ):
        form_factor_component = slugify(
            normalized_form_factor
        )

        if form_factor_component:
            components.append(
                form_factor_component
            )

    return "-".join(
        component
        for component in components
        if component
    )


def build_hardware_payload(database: dict) -> dict:
    """
    Build the public Hardware Explorer payload.
    """

    generated_at = utc_timestamp()

    gpu_profiles = build_gpu_profiles(database)

    hardware = []

    for profile_key, profile in sorted(gpu_profiles.items()):
        gpu_identity = profile.get(
            "gpu_identity",
            {},
        )

        gpu_vendor = gpu_identity.get(
            "vendor",
            profile.get(
                "gpu_vendor",
                "Unknown",
            ),
        )

        gpu_model = gpu_identity.get(
            "model",
            profile.get(
                "gpu_model",
                "Unknown",
            ),
        )

        gpu_vram_gib = gpu_identity.get(
            "vram_gib"
        )

        gpu_form_factor = gpu_identity.get(
            "form_factor",
            profile.get(
                "gpu_form_factor",
                "Unknown",
            ),
        )

        variant_id = build_variant_id(
            gpu_model=gpu_model,
            vram_gib=gpu_vram_gib,
            form_factor=gpu_form_factor,
        )

        hardware.append(
            {
                "variantId": variant_id,

                "gpuVendor": gpu_vendor,
                "gpuModel": gpu_model,

                "gpuIdentity": {
                    "vendor": gpu_vendor,
                    "model": gpu_model,
                    "vramGib": gpu_vram_gib,
                    "formFactor": gpu_form_factor,
                },

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
                    "memoryConfigurationsGb": profile.get(
                        "memory_configurations_gb",
                        [],
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
            "gpuVariants": len(hardware),
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