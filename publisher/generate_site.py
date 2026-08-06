import json
from pathlib import Path
from datetime import datetime, UTC


ROOT = Path(__file__).resolve().parent.parent

OUTPUT_DIR = ROOT / "database" / "generated"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


homepage = {
    "contractVersion": "1.0",
    "generatedAt": datetime.now(UTC).isoformat(),

    "stats": {
        "benchmarkResults": 1,
        "gpuModels": 1,
        "cpuModels": 1,
        "importEvents": 4,
        "averageTg128": 31.69
    },

    "featuredStory": {
        "title": "The GTX 1650 is OpenLLMBench's first recorded GPU.",
        "description": "The current database contains one verified benchmark result establishing the first historical reference point.",
        "snapshot": "2026-08-02 14:17 UTC",
        "badge": "Data Snapshot"
    }
}


output_file = OUTPUT_DIR / "homepage.json"

with open(output_file, "w", encoding="utf-8") as file:
    json.dump(homepage, file, indent=4)

print()

print("OpenLLMBench Publisher")

print("-----------------------")

print()

print(f"Published: {output_file}")

print()

print("Done.")