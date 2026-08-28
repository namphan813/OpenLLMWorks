"""
OpenLLMWorks Result ID Reconciliation Utility

Purpose:
Recompute canonical result IDs using the current identity rules,
report collisions, and optionally repair the database safely.

Default behavior is dry-run only.

Use:
    python -m scripts.reconcile_result_ids

Apply:
    python -m scripts.reconcile_result_ids --apply
"""

from collections import defaultdict
from copy import deepcopy
from pathlib import Path
import argparse
import json

from parser.database import (
    generate_result_id,
    load_database,
    write_database,
)
from parser.timestamps import utc_timestamp


DATABASE_FILE = Path(
    "database/benchmark_database.json"
)

PARSER_VERSION = "0.6.0-dev3"

RECONCILIATION_VERSION = "0.1"


def build_canonical_groups(
    database: dict,
) -> dict[str, list[dict]]:
    """
    Group stored records by their current canonical result ID.
    """

    grouped = defaultdict(list)

    for record in database["results"]:
        canonical_result_id = generate_result_id(
            hardware=record["hardware"],
            benchmark=record["benchmark"],
        )

        grouped[canonical_result_id].append(
            record
        )

    return dict(grouped)


def describe_record(
    record: dict,
) -> str:
    """
    Build a concise human-readable result description.
    """

    submission = record.get(
        "submission",
        {},
    )

    hardware = record.get(
        "hardware",
        {},
    )

    gpu = hardware.get(
        "gpu",
        {},
    )

    benchmark = record.get(
        "benchmark",
        {},
    )

    average = benchmark.get(
        "average",
        {},
    )

    return (
        f"{record.get('result_id')} | "
        f"{submission.get('submission_name')} | "
        f"{gpu.get('model')} | "
        f"pp512={average.get('pp512')} | "
        f"tg128={average.get('tg128')}"
    )


def choose_survivor(
    records: list[dict],
) -> dict:
    """
    Choose one authoritative record from a collision group.

    Preference order:
    1. Earliest imported_at timestamp
    2. Earliest processed_at timestamp
    3. Lexicographically smallest existing result_id

    This preserves the oldest known database record whenever
    possible rather than preferring a later duplicate.
    """

    def sort_key(record: dict):
        metadata = record.get(
            "metadata",
            {},
        )

        imported_at = (
            metadata.get("imported_at")
            or ""
        )

        processed_at = (
            metadata.get("processed_at")
            or ""
        )

        result_id = (
            record.get("result_id")
            or ""
        )

        return (
            imported_at,
            processed_at,
            result_id,
        )

    return min(
        records,
        key=sort_key,
    )


def build_reconciled_database(
    database: dict,
    grouped: dict[str, list[dict]],
) -> tuple[dict, list[dict]]:
    """
    Build a reconciled database copy.

    Each canonical identity produces exactly one stored record.
    Duplicate records are removed from the results list, but a
    reconciliation history entry preserves what changed.
    """

    reconciled = deepcopy(
        database
    )

    reconciled_results = []

    collision_history = []

    for canonical_result_id in sorted(
        grouped
    ):
        records = grouped[
            canonical_result_id
        ]

        survivor = deepcopy(
            choose_survivor(records)
        )

        previous_survivor_id = survivor.get(
            "result_id"
        )

        duplicate_ids = sorted(
            record.get("result_id")
            for record in records
            if record is not None
            and record.get("result_id")
            != previous_survivor_id
        )

        survivor[
            "result_id"
        ] = canonical_result_id

        survivor.setdefault(
            "metadata",
            {},
        )

        survivor["metadata"][
            "last_updated"
        ] = utc_timestamp()

        survivor["metadata"][
            "canonical_result_id_version"
        ] = RECONCILIATION_VERSION

        reconciled_results.append(
            survivor
        )

        if (
            len(records) > 1
            or previous_survivor_id
            != canonical_result_id
        ):
            collision_history.append(
                {
                    "canonical_result_id": (
                        canonical_result_id
                    ),
                    "survivor_previous_result_id": (
                        previous_survivor_id
                    ),
                    "removed_duplicate_result_ids": (
                        duplicate_ids
                    ),
                    "records_collapsed": len(
                        records
                    ),
                }
            )

    reconciled[
        "results"
    ] = reconciled_results

    reconciled[
        "result_count"
    ] = len(
        reconciled_results
    )

    reconciled.setdefault(
        "migration_history",
        [],
    )

    reconciliation_timestamp = (
        utc_timestamp()
    )

    reconciled[
        "migration_history"
    ].append(
        {
            "type": (
                "result_id_reconciliation"
            ),
            "version": (
                RECONCILIATION_VERSION
            ),
            "reconciled_at": (
                reconciliation_timestamp
            ),
            "records_before": len(
                database["results"]
            ),
            "records_after": len(
                reconciled_results
            ),
            "collision_groups": len(
                [
                    records
                    for records
                    in grouped.values()
                    if len(records) > 1
                ]
            ),
            "duplicate_records_removed": (
                len(database["results"])
                - len(reconciled_results)
            ),
            "groups": (
                collision_history
            ),
        }
    )

    return (
        reconciled,
        collision_history,
    )


def print_report(
    database: dict,
    grouped: dict[str, list[dict]],
) -> None:
    """
    Print the canonical identity report.
    """

    stored_count = len(
        database["results"]
    )

    canonical_count = len(
        grouped
    )

    collision_groups = [
        records
        for records
        in grouped.values()
        if len(records) > 1
    ]

    collision_count = len(
        collision_groups
    )

    duplicate_records = sum(
        len(records) - 1
        for records
        in collision_groups
    )

    print(
        "OpenLLMWorks Result ID Reconciliation"
    )
    print("=" * 44)
    print()

    print(
        f"Stored records: {stored_count}"
    )

    print(
        "Canonical identities: "
        f"{canonical_count}"
    )

    print(
        "Identity collisions: "
        f"{collision_count}"
    )

    print(
        "Duplicate records represented "
        "by collisions: "
        f"{duplicate_records}"
    )

    print()
    print(
        "Canonical Identity Report"
    )
    print("-" * 44)

    for canonical_result_id in sorted(
        grouped
    ):
        records = grouped[
            canonical_result_id
        ]

        status = (
            "COLLISION"
            if len(records) > 1
            else "UNIQUE"
        )

        print()
        print(
            f"{canonical_result_id} "
            f"[{status}]"
        )

        for record in records:
            print(
                "  "
                + describe_record(
                    record
                )
            )


def apply_reconciliation(
    database: dict,
    grouped: dict[str, list[dict]],
) -> None:
    """
    Rewrite the database with canonical IDs and deduplicated
    results.
    """

    reconciled, collision_history = (
        build_reconciled_database(
            database=database,
            grouped=grouped,
        )
    )

    print()
    print(
        "Applying reconciliation..."
    )

    print(
        "Records before: "
        f"{len(database['results'])}"
    )

    print(
        "Records after: "
        f"{len(reconciled['results'])}"
    )

    print(
        "Duplicate records removed: "
        f"{len(database['results']) - len(reconciled['results'])}"
    )

    print(
        "Collision groups resolved: "
        f"{len(collision_history)}"
    )

    write_database(
        database=reconciled,
        database_file=DATABASE_FILE,
        parser_version=PARSER_VERSION,
    )

    print()
    print(
        "Database reconciliation complete."
    )

    print(
        f"Database written to: "
        f"{DATABASE_FILE.resolve()}"
    )


def parse_args():
    parser = argparse.ArgumentParser(
        description=(
            "Reconcile OpenLLMWorks "
            "deterministic result IDs."
        )
    )

    parser.add_argument(
        "--apply",
        action="store_true",
        help=(
            "Write the reconciled database. "
            "Without this flag, the tool "
            "performs a dry run only."
        ),
    )

    return parser.parse_args()


def main():
    args = parse_args()

    database = load_database(
        database_file=DATABASE_FILE,
        parser_version=PARSER_VERSION,
    )

    grouped = build_canonical_groups(
        database
    )

    print_report(
        database=database,
        grouped=grouped,
    )

    if not args.apply:
        print()
        print(
            "DRY RUN ONLY - database was not modified."
        )

        print(
            "Run with --apply to write "
            "the reconciled database."
        )

        return

    apply_reconciliation(
        database=database,
        grouped=grouped,
    )


if __name__ == "__main__":
    main()