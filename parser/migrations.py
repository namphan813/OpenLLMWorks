"""
OpenLLMBench Database Migration Engine

Purpose:
Upgrades older OpenLLMBench database structures to newer schema
versions without discarding existing benchmark records.

Version:
0.8.0-dev1
"""

from copy import deepcopy
from typing import Any

from parser.timestamps import (
    normalize_timestamp,
    utc_timestamp,
)


MIGRATION_MODULE_VERSION = "0.8.0-dev1"

SOURCE_SCHEMA_VERSION = "0.6"
TARGET_SCHEMA_VERSION = "0.7"


# ------------------------------------------------------------
# SAFE HELPERS
# ------------------------------------------------------------

def ensure_dict(
    parent: dict,
    key: str,
) -> dict:
    """
    Ensure that parent[key] exists as a dictionary.

    Returns the existing or newly created dictionary.
    """

    current = parent.get(key)

    if isinstance(current, dict):
        return current

    parent[key] = {}

    return parent[key]


def normalize_existing_timestamp(
    value: Any,
) -> str | None:
    """
    Normalize an existing timestamp when possible.

    Invalid or missing historical values return None rather than
    causing the migration to fail.
    """

    try:
        return normalize_timestamp(value)

    except ValueError:
        return None


# ------------------------------------------------------------
# RECORD MIGRATION
# ------------------------------------------------------------

def migrate_result_record_to_0_7(
    record: dict,
    *,
    migration_timestamp: str,
) -> dict:
    """
    Upgrade one schema 0.6 result record to schema 0.7.

    Historical benchmark and submission dates are not invented.
    When their true values are unavailable, they remain None.
    """

    migrated = deepcopy(record)

    submission = ensure_dict(
        migrated,
        "submission",
    )

    benchmark = ensure_dict(
        migrated,
        "benchmark",
    )

    metadata = ensure_dict(
        migrated,
        "metadata",
    )

    original_processed_at = (
        normalize_existing_timestamp(
            metadata.get("processed_at")
        )
    )

    # We cannot reconstruct the true submission time from old
    # schema records, so this remains unknown.
    submission.setdefault(
        "submitted_at",
        None,
    )

    # We also cannot safely infer when the benchmark was run.
    benchmark.setdefault(
        "benchmark_timestamp",
        None,
    )

    # processed_at is the best available historical approximation
    # for when this record entered the database.
    metadata.setdefault(
        "imported_at",
        original_processed_at
        or migration_timestamp,
    )

    metadata.setdefault(
        "last_updated",
        migration_timestamp,
    )

    metadata["schema_version"] = (
        TARGET_SCHEMA_VERSION
    )

    metadata["migrated_from_schema"] = (
        SOURCE_SCHEMA_VERSION
    )

    metadata["migration_module_version"] = (
        MIGRATION_MODULE_VERSION
    )

    metadata["migrated_at"] = (
        migration_timestamp
    )

    return migrated


# ------------------------------------------------------------
# DATABASE MIGRATION
# ------------------------------------------------------------

def migrate_database_0_6_to_0_7(
    database: dict,
) -> dict:
    """
    Upgrade a complete OpenLLMBench database from schema 0.6
    to schema 0.7.

    This function returns a migrated copy and does not modify the
    supplied database object.
    """

    if not isinstance(database, dict):
        raise ValueError(
            "Database root must be a dictionary."
        )

    current_schema = database.get(
        "schema_version"
    )

    if current_schema != SOURCE_SCHEMA_VERSION:
        raise ValueError(
            "Migration requires schema version "
            f"{SOURCE_SCHEMA_VERSION!r}; received "
            f"{current_schema!r}."
        )

    results = database.get("results")

    if not isinstance(results, list):
        raise ValueError(
            "Database must contain a results list."
        )

    migrated_database = deepcopy(database)
    migration_timestamp = utc_timestamp()

    migrated_results: list[dict] = []

    for index, record in enumerate(
        results,
        start=1,
    ):
        if not isinstance(record, dict):
            raise ValueError(
                f"Result record {index} must be "
                "a dictionary."
            )

        migrated_results.append(
            migrate_result_record_to_0_7(
                record,
                migration_timestamp=(
                    migration_timestamp
                ),
            )
        )

    migrated_database["results"] = (
        migrated_results
    )

    migrated_database["schema_version"] = (
        TARGET_SCHEMA_VERSION
    )

    migrated_database["generated_at"] = (
        migration_timestamp
    )

    migrated_database["result_count"] = len(
        migrated_results
    )

    migration_history = (
        migrated_database.setdefault(
            "migration_history",
            [],
        )
    )

    if not isinstance(migration_history, list):
        raise ValueError(
            "Database migration_history must "
            "be a list."
        )

    migration_history.append(
        {
            "from_schema": (
                SOURCE_SCHEMA_VERSION
            ),
            "to_schema": (
                TARGET_SCHEMA_VERSION
            ),
            "migrated_at": (
                migration_timestamp
            ),
            "migration_module_version": (
                MIGRATION_MODULE_VERSION
            ),
            "records_migrated": len(
                migrated_results
            ),
        }
    )

    return migrated_database


# ------------------------------------------------------------
# MIGRATION ROUTER
# ------------------------------------------------------------

def migrate_database(
    database: dict,
    *,
    target_schema: str = (
        TARGET_SCHEMA_VERSION
    ),
) -> dict:
    """
    Route a database through the required schema migration.

    Future schema migrations can be added here sequentially.
    """

    current_schema = database.get(
        "schema_version"
    )

    if current_schema == target_schema:
        return deepcopy(database)

    if (
        current_schema
        == SOURCE_SCHEMA_VERSION
        and target_schema
        == TARGET_SCHEMA_VERSION
    ):
        return migrate_database_0_6_to_0_7(
            database
        )

    raise ValueError(
        "No supported migration path from "
        f"{current_schema!r} to "
        f"{target_schema!r}."
    )