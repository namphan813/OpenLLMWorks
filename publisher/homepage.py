import json
from pathlib import Path


def publish_homepage(
    output_directory: Path,
    generated_at: str,
    publisher_name: str,
    publisher_version: str,
    contract_version: str,
):
    """
    Publish homepage.json.
    """

    homepage = {
        "contractVersion": contract_version,
        "generatedAt": generated_at,
        "generator": {
            "name": publisher_name,
            "version": publisher_version,
        },
        "stats": {
            "benchmarkResults": 1,
            "gpuModels": 1,
            "cpuModels": 1,
            "importEvents": 4,
            "averageTg128": 31.69,
        },
        "featuredStory": {
            "title": "The GTX 1650 is OpenLLMBench's first recorded GPU.",
            "description": (
                "The current database contains one verified benchmark result "
                "establishing the first historical reference point."
            ),
            "snapshot": "2026-08-02 14:17 UTC",
            "badge": "Data Snapshot",
        },
    }

    homepage_file = output_directory / "homepage.json"

    with homepage_file.open("w", encoding="utf-8") as file:
        json.dump(homepage, file, indent=4)
        file.write("\n")

    return homepage_file