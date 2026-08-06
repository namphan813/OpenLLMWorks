from datetime import UTC, datetime
from pathlib import Path
import json

from homepage import publish_homepage


ROOT = Path(__file__).resolve().parent.parent

OUTPUT_DIR = ROOT / "database" / "generated"

PUBLISHER_NAME = "OpenLLMBench Publisher"
PUBLISHER_VERSION = "0.1"
CONTRACT_VERSION = "1.0"


def write_json(output_file: Path, data: dict):
    with output_file.open("w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)
        file.write("\n")


def main():

    generated_at = datetime.now(UTC).isoformat()

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    homepage_file = publish_homepage(
        OUTPUT_DIR,
        generated_at,
        PUBLISHER_NAME,
        PUBLISHER_VERSION,
        CONTRACT_VERSION,
    )

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