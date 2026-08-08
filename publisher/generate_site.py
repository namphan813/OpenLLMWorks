from datetime import UTC, datetime
from pathlib import Path
import json
import sys


ROOT = Path(__file__).resolve().parent.parent

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


from analytics.statistics import build_statistics
from publisher.hardware import publish_hardware
from publisher.homepage import publish_homepage


DATABASE_FILE = ROOT / "database" / "benchmark_database.json"
OUTPUT_DIR = ROOT / "database" / "generated"

PUBLISHER_NAME = "OpenLLMBench Publisher"
PUBLISHER_VERSION = "0.1"
CONTRACT_VERSION = "1.0"


def load_json(input_file: Path) -> dict:
    with input_file.open(
        "r",
        encoding="utf-8",
    ) as file:
        return json.load(file)


def write_json(
    output_file: Path,
    data: dict,
) -> None:
    with output_file.open(
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(
            data,
            file,
            indent=4,
        )
        file.write("\n")


def main() -> None:
    generated_at = datetime.now(UTC).isoformat()

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    print()
    print(PUBLISHER_NAME)
    print("-----------------------")
    print()

    print(f"Loading database: {DATABASE_FILE}")

    database = load_json(
        DATABASE_FILE
    )

    print("Database loaded.")
    print()

    print("Building statistics...")

    statistics_report = build_statistics(
        database
    )

    print("Statistics built.")
    print()

    homepage_file = publish_homepage(
        OUTPUT_DIR,
        generated_at,
        PUBLISHER_NAME,
        PUBLISHER_VERSION,
        CONTRACT_VERSION,
        statistics_report,
    )

    hardware_file = publish_hardware(
        database=database,
        output_directory=OUTPUT_DIR,
    )

    manifest = {
        "publisher": {
            "name": PUBLISHER_NAME,
            "version": PUBLISHER_VERSION,
        },
        "generatedAt": generated_at,
        "source": {
            "database": "benchmark_database.json",
            "statisticsVersion": statistics_report.get(
                "statistics_version",
                "Unknown",
            ),
        },
        "files": [
            {
                "name": "homepage.json",
                "contractVersion": CONTRACT_VERSION,
            },
            {
                "name": "hardware.json",
                "contractVersion": CONTRACT_VERSION,
            },
        ],
    }

    manifest_file = OUTPUT_DIR / "manifest.json"

    write_json(
        manifest_file,
        manifest,
    )

    print(f"Published: {homepage_file}")
    print(f"Published: {hardware_file}")
    print(f"Published: {manifest_file}")
    print()
    print("Publisher completed successfully.")


if __name__ == "__main__":
    main()