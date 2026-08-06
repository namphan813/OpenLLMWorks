import json
from datetime import UTC, datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
OUTPUT_DIR = ROOT / "database" / "generated"

PUBLISHER_NAME = "OpenLLMBench Publisher"
PUBLISHER_VERSION = "0.1"
CONTRACT_VERSION = "1.0"


def write_json(output_file: Path, data: dict) -> None:
    """Write JSON data using UTF-8 and readable indentation."""
    with output_file.open("w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)

        # End generated files with a newline.
        file.write("\n")


def main() -> None:
    generated_at = datetime.now(UTC).isoformat()

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    homepage = {
        "contractVersion": CONTRACT_VERSION,
        "generatedAt": generated_at,
        "generator": {
            "name": PUBLISHER_NAME,
            "version": PUBLISHER_VERSION,
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

    homepage_file = OUTPUT_DIR / "homepage.json"
    write_json(homepage_file, homepage)

    manifest = {
        "publisher": {
            "name": PUBLISHER_NAME,
            "version": PUBLISHER_VERSION,
        },
        "generatedAt": generated_at,
        "files": [
            {
                "name": "homepage.json",
                "contractVersion": CONTRACT_VERSION,
            }
        ],
    }

    manifest_file = OUTPUT_DIR / "manifest.json"
    write_json(manifest_file, manifest)

    print()
    print(PUBLISHER_NAME)
    print("-----------------------")
    print()
    print(f"Published: {homepage_file}")
    print(f"Published: {manifest_file}")
    print()
    print("Publisher completed successfully.")


if __name__ == "__main__":
    main()