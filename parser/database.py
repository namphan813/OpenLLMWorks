"""
OpenLLMWorks Database Module

Purpose:
Builds normalized benchmark records, generates deterministic
result IDs, detects duplicates, maintains the persistent
database, and upgrades supported older database schemas.

Version:
0.8.0-dev5
"""

from copy import deepcopy
from hashlib import sha256
from pathlib import Path
import json

from parser.migrations import migrate_database
from parser.timestamps import (
    normalize_timestamp,
    utc_timestamp,
)


DATABASE_MODULE_VERSION = "0.8.0-dev5"
DATABASE_SCHEMA_VERSION = "0.7"

SUPPORTED_SOURCE_SCHEMAS = {
    "0.6",
    "0.7",
}


# ------------------------------------------------------------
# RESULT ID GENERATION
# ------------------------------------------------------------

def build_result_fingerprint(
    hardware: dict,
    benchmark: dict,
) -> dict:
    """
    Build stable data used to identify one benchmark result.

    Result identity is intentionally based only on fields that
    describe the benchmark measurement itself.

    Descriptive metadata that may evolve over time must not
    change the deterministic result ID. Examples of excluded
    fields include:

    - submission names and source paths
    - timestamps
    - parser/database/schema versions
    - system manufacturer and model
    - GPU form factor and driver model
    - NVIDIA driver and CUDA versions
    - submission provenance and verification metadata

    This allows OpenLLMWorks to enrich historical records without
    accidentally turning an existing benchmark measurement into
    a new result.
    """

    cpu = hardware.get(
        "cpu",
        {},
    )

    memory = hardware.get(
        "memory",
        {},
    )

    gpu = hardware.get(
        "gpu",
        {},
    )

    operating_system = hardware.get(
        "operating_system",
        {},
    )

    gpu_vram = gpu.get(
        "vram",
        {},
    )

    stable_hardware = {
        "cpu": {
            "model": cpu.get(
                "model"
            ),
        },
        "memory": {
            "installed_capacity_gb": (
                memory.get(
                    "installed_capacity_gb"
                )
            ),
        },
        "operating_system": {
            "platform": (
                operating_system.get(
                    "platform"
                )
            ),
            "normalized": (
                operating_system.get(
                    "normalized"
                )
            ),
        },
        "gpu": {
            "vendor": gpu.get(
                "vendor"
            ),
            "model": gpu.get(
                "model"
            ),
            "vram": {
                "capacity_gib": (
                    gpu_vram.get(
                        "capacity_gib"
                    )
                ),
            },
        },
    }

    run_measurements = [
        {
            "pp512": run["pp512"],
            "tg128": run["tg128"],
        }
        for run in benchmark["runs"]
    ]

    return {
        "hardware": stable_hardware,
        "protocol": benchmark["protocol"],
        "llama_cpp": benchmark["llama_cpp"],
        "runs": run_measurements,
        "average": benchmark["average"],
    }


def generate_result_id(
    hardware: dict,
    benchmark: dict,
) -> str:
    """
    Generate a deterministic result ID.

    Identical normalized benchmark measurements produce the
    same ID even when descriptive metadata evolves.
    """

    fingerprint = build_result_fingerprint(
        hardware=hardware,
        benchmark=benchmark,
    )

    canonical_json = json.dumps(
        fingerprint,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    )

    digest = sha256(
        canonical_json.encode("utf-8")
    ).hexdigest()

    return f"result_{digest[:16]}"


# ------------------------------------------------------------
# BENCHMARK RECORD CREATION
# ------------------------------------------------------------

def build_result_record(
    *,
    results: list[dict],
    hardware: dict,
    status: str,
    pp_average: float,
    tg_average: float,
    submission_name: str,
    submission_source: str,
    required_runs: int,
    parser_version: str,
    submitted_at: str | None = None,
    benchmark_timestamp: str | None = None,
    source_type: str = "internal_seed",
    contributor_id: str = "founder_000001",
    contributor_type: str = "founder",
    verification_status: str = "internally_verified",
) -> dict:
    """
    Build one complete schema 0.7 benchmark result record.

    submitted_at and benchmark_timestamp remain optional until
    the public submission workflow captures them directly.

    Provenance fields are supplied by the trusted import
    workflow. Defaults preserve compatibility with historical
    internal seed imports.
    """

    commits = sorted(
        {
            result["commit"]
            for result in results
            if result["commit"] is not None
        }
    )

    builds = sorted(
        {
            result["build"]
            for result in results
            if result["build"] is not None
        }
    )

    normalized_submitted_at = (
        normalize_timestamp(submitted_at)
    )

    normalized_benchmark_timestamp = (
        normalize_timestamp(
            benchmark_timestamp
        )
    )

    imported_at = utc_timestamp()

    benchmark = {
        "status": status,
        "benchmark_timestamp": (
            normalized_benchmark_timestamp
        ),
        "protocol": {
            "id": "OLBD-BP-1.0",
            "version": "1.0",
            "required_runs": required_runs,
            "prompt_tokens": 512,
            "generation_tokens": 128,
            "backend": "CUDA",
        },
        "llama_cpp": {
            "commit": (
                commits[0]
                if len(commits) == 1
                else None
            ),
            "build": (
                builds[0]
                if len(builds) == 1
                else None
            ),
            "all_detected_commits": commits,
            "all_detected_builds": builds,
            "consistent_across_runs": (
                len(commits) <= 1
                and len(builds) <= 1
            ),
        },
        "runs": [
            {
                "run_number": index,
                "filename": result["filename"],
                "pp512": result["pp512"],
                "tg128": result["tg128"],
            }
            for index, result in enumerate(
                results,
                start=1,
            )
        ],
        "average": {
            "pp512": round(pp_average, 2),
            "tg128": round(tg_average, 2),
        },
    }

    result_id = generate_result_id(
        hardware=hardware,
        benchmark=benchmark,
    )

    return {
        "result_id": result_id,
        "submission": {
            "submission_name": submission_name,
            "source_path": submission_source,
            "source_type": source_type,
            "contributor_id": contributor_id,
            "contributor_type": contributor_type,
            "verification_status": (
                verification_status
            ),
            "runs_completed": len(results),
            "submitted_at": (
                normalized_submitted_at
            ),
        },
        "hardware": hardware,
        "benchmark": benchmark,
        "metadata": {
            "parser_version": parser_version,
            "database_module_version": (
                DATABASE_MODULE_VERSION
            ),
            "schema_version": (
                DATABASE_SCHEMA_VERSION
            ),
            "processed_at": imported_at,
            "imported_at": imported_at,
            "last_updated": imported_at,
        },
    }


# ------------------------------------------------------------
# DATABASE CREATION
# ------------------------------------------------------------

def create_empty_database(
    parser_version: str,
) -> dict:
    """
    Create a new empty schema 0.7 database.
    """

    timestamp = utc_timestamp()

    return {
        "project": (
            "Open LLM Benchmark Database"
        ),
        "schema_version": (
            DATABASE_SCHEMA_VERSION
        ),
        "parser_version": parser_version,
        "created_at": timestamp,
        "generated_at": timestamp,
        "result_count": 0,
        "results": [],
        "import_history": [],
        "migration_history": [],
    }


# ------------------------------------------------------------
# DATABASE LOADING AND EVOLUTION
# ------------------------------------------------------------

def validate_loaded_database_root(
    database: object,
) -> dict:
    """
    Validate the minimum structure needed before migration.
    """

    if not isinstance(database, dict):
        raise ValueError(
            "Database root must be a JSON object."
        )

    if not isinstance(
        database.get("results"),
        list,
    ):
        raise ValueError(
            "Database must contain a results list."
        )

    return database


def upgrade_database_if_needed(
    database: dict,
) -> dict:
    """
    Return a schema 0.7 copy of a supported database.

    Schema 0.6 is migrated in memory. Schema 0.7 is copied
    without modification.
    """

    current_schema = database.get(
        "schema_version"
    )

    if current_schema not in (
        SUPPORTED_SOURCE_SCHEMAS
    ):
        raise ValueError(
            "Unsupported database schema: "
            f"{current_schema!r}. Supported schemas: "
            f"{sorted(SUPPORTED_SOURCE_SCHEMAS)}."
        )

    if current_schema == (
        DATABASE_SCHEMA_VERSION
    ):
        return deepcopy(database)

    return migrate_database(
        database,
        target_schema=(
            DATABASE_SCHEMA_VERSION
        ),
    )


def load_database(
    database_file: Path,
    parser_version: str,
) -> dict:
    """
    Load the database and automatically upgrade supported
    older schemas in memory.

    This function does not write the upgraded database to disk.
    A later call to write_database performs that action.
    """

    if not database_file.exists():
        return create_empty_database(
            parser_version=parser_version
        )

    try:
        raw_database = json.loads(
            database_file.read_text(
                encoding="utf-8"
            )
        )

    except json.JSONDecodeError as error:
        raise ValueError(
            f"Database JSON is invalid: {error}"
        ) from error

    database = validate_loaded_database_root(
        raw_database
    )

    upgraded_database = (
        upgrade_database_if_needed(
            database
        )
    )

    upgraded_database.setdefault(
        "import_history",
        [],
    )

    upgraded_database.setdefault(
        "migration_history",
        [],
    )

    upgraded_database.setdefault(
        "created_at",
        utc_timestamp(),
    )

    upgraded_database["parser_version"] = (
        parser_version
    )

    upgraded_database["result_count"] = len(
        upgraded_database["results"]
    )

    return upgraded_database


# ------------------------------------------------------------
# DUPLICATE DETECTION
# ------------------------------------------------------------

def find_result(
    database: dict,
    result_id: str,
) -> dict | None:
    """
    Find an existing result by deterministic result ID.
    """

    for result in database["results"]:
        if result.get("result_id") == result_id:
            return result

    return None


def add_result(
    database: dict,
    record: dict,
) -> tuple[str, str]:
    """
    Add a result unless it already exists.

    Returns:
        ("added", result_id)
        or
        ("duplicate", result_id)
    """

    result_id = record["result_id"]

    existing_record = find_result(
        database=database,
        result_id=result_id,
    )

    import_timestamp = utc_timestamp()

    import_event = {
        "processed_at": import_timestamp,
        "imported_at": import_timestamp,
        "result_id": result_id,
        "submission_name": record[
            "submission"
        ]["submission_name"],
    }

    if existing_record is not None:
        import_event["status"] = (
            "duplicate"
        )

        import_event["duplicate_of"] = (
            result_id
        )

        database["import_history"].append(
            import_event
        )

        return "duplicate", result_id

    database["results"].append(
        deepcopy(record)
    )

    import_event["status"] = "added"

    database["import_history"].append(
        import_event
    )

    database["result_count"] = len(
        database["results"]
    )

    return "added", result_id


# ------------------------------------------------------------
# DATABASE WRITING
# ------------------------------------------------------------

def write_database(
    database: dict,
    database_file: Path,
    parser_version: str,
) -> None:
    """
    Write the complete schema 0.7 database to disk.

    Database backups and destructive reconciliation are handled
    separately from normal database writing.
    """

    database_file.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    database["schema_version"] = (
        DATABASE_SCHEMA_VERSION
    )

    database["parser_version"] = (
        parser_version
    )

    database["generated_at"] = (
        utc_timestamp()
    )

    database["result_count"] = len(
        database["results"]
    )

    database.setdefault(
        "migration_history",
        [],
    )

    database["results"] = sorted(
        database["results"],
        key=lambda record: record[
            "result_id"
        ],
    )

    database_file.write_text(
        json.dumps(
            database,
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )