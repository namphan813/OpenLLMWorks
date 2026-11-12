"""
OpenLLMWorks Hardware Profile Engine

Purpose:
Build reusable hardware profiles from the benchmark database.

Version:
0.7.0-dev4
"""

from collections import defaultdict

from analytics.statistics import (
    extract_result_rows,
    valid_number,
)


PROFILE_ENGINE_VERSION = "0.7.0-dev4"


def average(values):
    """Return the average of a list of numbers."""

    if not values:
        return None

    return sum(values) / len(values)


def build_gpu_profiles(database):
    """
    Build one profile for every distinct GPU variant.

    GPU variant identity currently consists of:
    - GPU vendor
    - GPU model
    - VRAM capacity
    - GPU form factor

    System memory, CPU, operating system, software provenance,
    and benchmark performance are test-configuration/result
    attributes and are intentionally excluded from GPU identity.
    """

    rows = extract_result_rows(database)

    grouped = defaultdict(list)

    for row in rows:
        gpu_vendor = row.get("gpu_vendor", "Unknown")
        gpu_model = row.get("gpu_model", "Unknown")
        vram_gib = row.get("vram_gib")
        gpu_form_factor = row.get(
            "gpu_form_factor",
            "Unknown",
        )

        identity_key = (
            gpu_vendor,
            gpu_model,
            vram_gib,
            gpu_form_factor,
        )

        grouped[identity_key].append(row)

    profiles = {}

    for identity_key, gpu_rows in grouped.items():
        (
            gpu_vendor,
            gpu_model,
            identity_vram_gib,
            gpu_form_factor,
        ) = identity_key

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

        # Preserve physical GPU identity while calculating
        # performance separately for each acceleration backend.
        backend_groups = defaultdict(list)

        for row in gpu_rows:
            backend = row.get("backend") or "CUDA"
            backend = str(backend).strip().casefold()

            if backend == "cuda":
                backend = "CUDA"
            elif backend == "vulkan":
                backend = "Vulkan"
            else:
                raise ValueError(
                    f"Unsupported benchmark backend: {backend!r}"
                )

            backend_groups[backend].append(row)

        performance_by_backend = {}

        for backend, backend_rows in sorted(backend_groups.items()):
            backend_pp512 = [
                row["pp512"]
                for row in backend_rows
                if valid_number(row.get("pp512"))
            ]

            backend_tg128 = [
                row["tg128"]
                for row in backend_rows
                if valid_number(row.get("tg128"))
            ]

            performance_by_backend[backend] = {
                "submission_count": len(backend_rows),
                "average_pp512": average(backend_pp512),
                "average_tg128": average(backend_tg128),
                "best_pp512": (
                    max(backend_pp512)
                    if backend_pp512
                    else None
                ),
                "worst_pp512": (
                    min(backend_pp512)
                    if backend_pp512
                    else None
                ),
            }

        benchmark_results = []

        for row in gpu_rows:
            benchmark_results.append(
                {
                    "backend": row.get("backend") or "CUDA",
                    "result_id": row.get(
                        "result_id",
                        "",
                    ),
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
                    "driver_version": row.get(
                        "driver_version",
                        "",
                    ),
                    "cuda_umd_version": row.get(
                        "cuda_umd_version",
                        "",
                    ),
                    "nvidia_smi_version": row.get(
                        "nvidia_smi_version",
                        "",
                    ),
                }
            )

        profile_key = (
            f"{gpu_vendor}|"
            f"{gpu_model}|"
            f"{identity_vram_gib}|"
            f"{gpu_form_factor}"
        )

        profiles[profile_key] = {
            "submission_count": len(gpu_rows),
            "performance_by_backend": performance_by_backend,

            "gpu_identity": {
                "vendor": gpu_vendor,
                "model": gpu_model,
                "vram_gib": identity_vram_gib,
                "form_factor": gpu_form_factor,
            },

            "gpu_vendor": gpu_vendor,

            "gpu_model": gpu_model,

            "gpu_form_factor": gpu_form_factor,

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