"""
OpenLLMWorks Leaderboard Publisher

Purpose:
Build the public leaderboard data contract consumed by the OpenLLMWorks
website and other public-facing tools.

The publisher does not calculate benchmark analytics from raw benchmark
records itself. It consumes reusable GPU profile rankings produced by the
analytics layer and transforms those rankings into a stable public JSON
structure.

Version:
0.2.1
"""

from datetime import datetime, timezone
import json
from pathlib import Path

from analytics.leaderboards import rank_gpu_profiles_by_metric
from analytics.profiles import build_gpu_profiles
from publisher.hardware import (
    build_variant_id,
    normalize_public_vram_gib,
)


LEADERBOARD_PUBLISHER_VERSION = "0.2.1"
LEADERBOARD_CONTRACT_VERSION = "1.0"


def utc_timestamp() -> str:
    """
    Return the current UTC timestamp in ISO 8601 format.
    """

    return datetime.now(timezone.utc).isoformat()


def build_public_entry(
    ranked_profile: dict,
) -> dict:
    """
    Convert one ranked GPU profile into the stable public
    leaderboard entry structure.
    """

    gpu_vendor = ranked_profile.get(
        "gpu_vendor",
        "Unknown",
    )

    gpu_model = ranked_profile.get(
        "gpu_model",
        "Unknown",
    )

    raw_vram_gib = ranked_profile.get(
        "vram_gib"
    )

    public_vram_gib = normalize_public_vram_gib(
        raw_vram_gib
    )

    form_factor = ranked_profile.get(
        "form_factor",
        "Unknown",
    )

    variant_id = build_variant_id(
        gpu_model=gpu_model,
        vram_gib=raw_vram_gib,
        form_factor=form_factor,
    )

    return {
        "rank": ranked_profile.get(
            "rank"
        ),
        "variantId": variant_id,
        "gpuVendor": gpu_vendor,
        "gpuModel": gpu_model,
        "gpuIdentity": {
            "vendor": gpu_vendor,
            "model": gpu_model,
            "vramGiB": public_vram_gib,
            "formFactor": form_factor,
        },
        "submissionCount": ranked_profile.get(
            "submission_count",
            0,
        ),
        "value": ranked_profile.get(
            "value"
        ),
        **(
            {"backend": ranked_profile["overall_backend"]}
            if ranked_profile.get("overall_backend")
            else {}
        ),
    }


def build_metric_leaderboard(
    gpu_profiles: dict,
    metric_key: str,
) -> dict:
    """
    Build one public leaderboard from reusable GPU profiles.

    Ranking is delegated to analytics.leaderboards so ranking
    behavior has one source of truth.
    """

    ranked_profiles = rank_gpu_profiles_by_metric(
        gpu_profiles,
        metric_key,
    )

    entries = [
        build_public_entry(
            ranked_profile
        )
        for ranked_profile in ranked_profiles
    ]

    values = [
        entry["value"]
        for entry in entries
        if isinstance(
            entry.get("value"),
            (int, float),
        )
        and not isinstance(
            entry.get("value"),
            bool,
        )
    ]

    return {
        "totalRanked": len(entries),
        "bestValue": (
            max(values)
            if values
            else None
        ),
        "worstValue": (
            min(values)
            if values
            else None
        ),
        "entries": entries,
    }


def build_backend_profiles(
    gpu_profiles: dict,
    backend: str,
) -> dict:
    """
    Create a backend-specific ranking view while preserving
    the physical GPU identity and variant ID.
    """

    backend_profiles = {}

    for profile_key, profile in gpu_profiles.items():
        stats = profile.get(
            "performance_by_backend", {}
        ).get(backend)

        if not stats:
            continue

        backend_profile = {
            **profile,
            "submission_count": stats["submission_count"],
            "average_pp512": stats["average_pp512"],
            "average_tg128": stats["average_tg128"],
            "best_pp512": stats["best_pp512"],
            "worst_pp512": stats["worst_pp512"],
        }

        backend_profiles[profile_key] = backend_profile

    return backend_profiles


def build_overall_profiles(
    gpu_profiles: dict,
) -> dict:
    """
    Select one representative backend per physical GPU.

    Prefer CUDA, then Vulkan. Never combine backend averages.
    """

    overall_profiles = {}

    for profile_key, profile in gpu_profiles.items():
        available = profile.get(
            "performance_by_backend", {}
        )

        backend = next(
            (
                candidate
                for candidate in ("CUDA", "Vulkan")
                if candidate in available
            ),
            None,
        )

        if backend is None:
            continue

        stats = available[backend]

        overall_profiles[profile_key] = {
            **profile,
            "submission_count": stats["submission_count"],
            "average_pp512": stats["average_pp512"],
            "average_tg128": stats["average_tg128"],
            "best_pp512": stats["best_pp512"],
            "worst_pp512": stats["worst_pp512"],
            "overall_backend": backend,
        }

    return overall_profiles


def build_legacy_profiles(
    gpu_profiles: dict,
) -> dict:
    """
    Exclude mixed-backend profiles from legacy rankings.

    Single-backend profiles retain their original performance
    statistics and existing leaderboard behavior.
    """

    return {
        key: profile
        for key, profile in gpu_profiles.items()
        if len(profile.get("performance_by_backend", {})) <= 1
    }


def build_leaderboards_payload(
    database: dict,
) -> dict:
    """
    Build the complete public leaderboard payload.
    """

    generated_at = utc_timestamp()

    gpu_profiles = build_gpu_profiles(
        database
    )

    legacy_profiles = build_legacy_profiles(
        gpu_profiles
    )

    pp512 = build_metric_leaderboard(
        legacy_profiles,
        "average_pp512",
    )

    tg128 = build_metric_leaderboard(
        legacy_profiles,
        "average_tg128",
    )

    overall_profiles = build_overall_profiles(
        gpu_profiles
    )

    overall_pp512 = build_metric_leaderboard(
        overall_profiles,
        "average_pp512",
    )

    overall_tg128 = build_metric_leaderboard(
        overall_profiles,
        "average_tg128",
    )

    # Attach the representative backend to each overall entry.
    # Ranking analytics does not retain custom profile metadata.
    backend_by_variant_id = {}

    for profile in overall_profiles.values():
        identity = profile["gpu_identity"]

        variant_id = build_variant_id(
            gpu_model=identity["model"],
            vram_gib=identity["vram_gib"],
            form_factor=identity["form_factor"],
        )
        backend_by_variant_id[variant_id] = profile[
            "overall_backend"
        ]

    for leaderboard in (overall_pp512, overall_tg128):
        for entry in leaderboard["entries"]:
            entry["backend"] = backend_by_variant_id[
                entry["variantId"]
            ]

    backends = sorted({
        backend
        for profile in gpu_profiles.values()
        for backend in profile.get(
            "performance_by_backend", {}
        )
    })

    leaderboards_by_backend = {}

    for backend in backends:
        backend_profiles = build_backend_profiles(
            gpu_profiles,
            backend,
        )

        backend_pp512 = build_metric_leaderboard(
            backend_profiles,
            "average_pp512",
        )

        backend_tg128 = build_metric_leaderboard(
            backend_profiles,
            "average_tg128",
        )

        # Explicitly identify the backend for every ranked entry.
        for leaderboard in (backend_pp512, backend_tg128):
            for entry in leaderboard["entries"]:
                entry["backend"] = backend

        leaderboards_by_backend[backend] = {
            "pp512": backend_pp512,
            "tg128": backend_tg128,
        }

    return {
        "contractVersion": (
            LEADERBOARD_CONTRACT_VERSION
        ),
        "generatedAt": generated_at,
        "generator": {
            "name": (
                "OpenLLMWorks Leaderboard Publisher"
            ),
            "version": (
                LEADERBOARD_PUBLISHER_VERSION
            ),
        },
        "summary": {
            "gpuVariants": len(
                gpu_profiles
            ),
            "pp512Ranked": pp512[
                "totalRanked"
            ],
            "tg128Ranked": tg128[
                "totalRanked"
            ],
        },
        "leaderboards": {
            "pp512": pp512,
            "tg128": tg128,
        },
        "leaderboardsOverall": {
            "pp512": overall_pp512,
            "tg128": overall_tg128,
        },
        "leaderboardsByBackend": leaderboards_by_backend,
    }


def publish_leaderboards(
    database: dict,
    output_directory: Path,
) -> Path:
    """
    Generate leaderboards.json in the supplied output directory.
    """

    output_directory.mkdir(
        parents=True,
        exist_ok=True,
    )

    payload = build_leaderboards_payload(
        database
    )

    leaderboard_file = (
        output_directory
        / "leaderboards.json"
    )

    with leaderboard_file.open(
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(
            payload,
            file,
            indent=4,
        )

        file.write("\n")

    return leaderboard_file