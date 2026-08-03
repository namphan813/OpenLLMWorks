"""
OpenLLMBench Database Validator

Purpose:
Validates the structure and internal consistency of the
persistent OpenLLMBench benchmark database.

Version:
0.6.0-dev4
"""

from pathlib import Path
from typing import Any
import json


VALIDATOR_VERSION = "0.6.0-dev4"
SUPPORTED_SCHEMA_VERSION = "0.6"

VALID_BENCHMARK_STATUSES = {
    "complete",
    "legacy_two_run",
    "incomplete",
    "invalid",
}


def load_json_file(file_path: Path) -> dict:
    """
    Load and decode one JSON file.

    Raises:
        FileNotFoundError:
            If the requested file does not exist.

        ValueError:
            If the file contains invalid JSON or its root
            is not a JSON object.
    """

    if not file_path.exists():
        raise FileNotFoundError(
            f"Database file does not exist: {file_path}"
        )

    try:
        data = json.loads(
            file_path.read_text(
                encoding="utf-8"
            )
        )

    except json.JSONDecodeError as error:
        raise ValueError(
            f"Database contains invalid JSON: {error}"
        ) from error

    if not isinstance(data, dict):
        raise ValueError(
            "Database root must be a JSON object."
        )

    return data


def add_error(
    errors: list[str],
    message: str,
) -> None:
    """
    Add one validation error.
    """

    errors.append(message)


def add_warning(
    warnings: list[str],
    message: str,
) -> None:
    """
    Add one non-fatal validation warning.
    """

    warnings.append(message)


def validate_database_header(
    database: dict,
    errors: list[str],
    warnings: list[str],
) -> None:
    """
    Validate database-level fields.
    """

    required_fields = {
        "project",
        "schema_version",
        "parser_version",
        "created_at",
        "generated_at",
        "result_count",
        "results",
        "import_history",
    }

    for field_name in sorted(required_fields):
        if field_name not in database:
            add_error(
                errors,
                f"Database is missing required field: "
                f"{field_name}"
            )

    schema_version = database.get(
        "schema_version"
    )

    if schema_version != SUPPORTED_SCHEMA_VERSION:
        add_error(
            errors,
            "Unsupported schema version: "
            f"{schema_version!r}. "
            f"Expected {SUPPORTED_SCHEMA_VERSION!r}."
        )

    results = database.get("results")

    if not isinstance(results, list):
        add_error(
            errors,
            "Database field 'results' must be a list."
        )

    import_history = database.get(
        "import_history"
    )

    if not isinstance(import_history, list):
        add_error(
            errors,
            "Database field 'import_history' must be a list."
        )

    result_count = database.get(
        "result_count"
    )

    if not isinstance(result_count, int):
        add_error(
            errors,
            "Database field 'result_count' must be an integer."
        )

    elif isinstance(results, list):
        actual_count = len(results)

        if result_count != actual_count:
            add_error(
                errors,
                "Database result_count does not match "
                f"the results list: stored={result_count}, "
                f"actual={actual_count}."
            )


def validate_result_record(
    record: Any,
    record_index: int,
    errors: list[str],
    warnings: list[str],
) -> str | None:
    """
    Validate one benchmark result record.

    Returns:
        The record's result ID when available.
    """

    label = f"Result record {record_index}"

    if not isinstance(record, dict):
        add_error(
            errors,
            f"{label} must be a JSON object."
        )
        return None

    required_sections = {
        "result_id",
        "submission",
        "hardware",
        "benchmark",
        "metadata",
    }

    for section_name in sorted(
        required_sections
    ):
        if section_name not in record:
            add_error(
                errors,
                f"{label} is missing required section: "
                f"{section_name}"
            )

    result_id = record.get("result_id")

    if not isinstance(result_id, str):
        add_error(
            errors,
            f"{label} has an invalid result_id."
        )
        result_id = None

    elif not result_id.startswith("result_"):
        add_warning(
            warnings,
            f"{label} result_id does not begin with "
            "'result_'."
        )

    submission = record.get("submission")

    if not isinstance(submission, dict):
        add_error(
            errors,
            f"{label} submission must be an object."
        )

    else:
        submission_name = submission.get(
            "submission_name"
        )

        if not isinstance(
            submission_name,
            str,
        ) or not submission_name.strip():
            add_error(
                errors,
                f"{label} has no valid submission_name."
            )

        runs_completed = submission.get(
            "runs_completed"
        )

        if not isinstance(
            runs_completed,
            int,
        ):
            add_error(
                errors,
                f"{label} runs_completed must be "
                "an integer."
            )

    hardware = record.get("hardware")

    if not isinstance(hardware, dict):
        add_error(
            errors,
            f"{label} hardware must be an object."
        )

    else:
        required_hardware_sections = {
            "system",
            "cpu",
            "memory",
            "gpu",
            "operating_system",
        }

        for section_name in sorted(
            required_hardware_sections
        ):
            if section_name not in hardware:
                add_error(
                    errors,
                    f"{label} hardware is missing: "
                    f"{section_name}"
                )

    benchmark = record.get("benchmark")

    if not isinstance(benchmark, dict):
        add_error(
            errors,
            f"{label} benchmark must be an object."
        )

    else:
        status = benchmark.get("status")

        if status not in VALID_BENCHMARK_STATUSES:
            add_error(
                errors,
                f"{label} has invalid benchmark "
                f"status: {status!r}"
            )

        protocol = benchmark.get("protocol")
        runs = benchmark.get("runs")
        average = benchmark.get("average")
        llama_cpp = benchmark.get(
            "llama_cpp"
        )

        if not isinstance(protocol, dict):
            add_error(
                errors,
                f"{label} protocol must be an object."
            )

        if not isinstance(llama_cpp, dict):
            add_error(
                errors,
                f"{label} llama_cpp must be an object."
            )

        if not isinstance(runs, list):
            add_error(
                errors,
                f"{label} runs must be a list."
            )

        else:
            if not runs:
                add_error(
                    errors,
                    f"{label} has no benchmark runs."
                )

            for run_index, run in enumerate(
                runs,
                start=1,
            ):
                if not isinstance(run, dict):
                    add_error(
                        errors,
                        f"{label} run {run_index} must "
                        "be an object."
                    )
                    continue

                for metric_name in (
                    "pp512",
                    "tg128",
                ):
                    metric_value = run.get(
                        metric_name
                    )

                    if not isinstance(
                        metric_value,
                        (int, float),
                    ):
                        add_error(
                            errors,
                            f"{label} run {run_index} "
                            f"has invalid {metric_name}."
                        )

                    elif metric_value <= 0:
                        add_warning(
                            warnings,
                            f"{label} run {run_index} "
                            f"has non-positive "
                            f"{metric_name}."
                        )

            if isinstance(submission, dict):
                runs_completed = submission.get(
                    "runs_completed"
                )

                if isinstance(
                    runs_completed,
                    int,
                ) and runs_completed != len(runs):
                    add_error(
                        errors,
                        f"{label} runs_completed does "
                        "not match benchmark runs: "
                        f"stored={runs_completed}, "
                        f"actual={len(runs)}."
                    )

        if not isinstance(average, dict):
            add_error(
                errors,
                f"{label} average must be an object."
            )

        else:
            for metric_name in (
                "pp512",
                "tg128",
            ):
                metric_value = average.get(
                    metric_name
                )

                if not isinstance(
                    metric_value,
                    (int, float),
                ):
                    add_error(
                        errors,
                        f"{label} average has invalid "
                        f"{metric_name}."
                    )

    metadata = record.get("metadata")

    if not isinstance(metadata, dict):
        add_error(
            errors,
            f"{label} metadata must be an object."
        )

    else:
        metadata_schema = metadata.get(
            "schema_version"
        )

        if metadata_schema != (
            SUPPORTED_SCHEMA_VERSION
        ):
            add_error(
                errors,
                f"{label} metadata schema version "
                f"is {metadata_schema!r}; expected "
                f"{SUPPORTED_SCHEMA_VERSION!r}."
            )

    return result_id


def validate_unique_result_ids(
    result_ids: list[str],
    errors: list[str],
) -> None:
    """
    Verify that no result ID appears more than once.
    """

    seen_ids: set[str] = set()
    duplicate_ids: set[str] = set()

    for result_id in result_ids:
        if result_id in seen_ids:
            duplicate_ids.add(result_id)

        seen_ids.add(result_id)

    for result_id in sorted(duplicate_ids):
        add_error(
            errors,
            "Duplicate result ID stored in database: "
            f"{result_id}"
        )


def validate_database(
    database: dict,
) -> dict:
    """
    Validate a complete OpenLLMBench database.

    Returns:
        A validation report containing:

        - valid
        - error_count
        - warning_count
        - errors
        - warnings
    """

    errors: list[str] = []
    warnings: list[str] = []

    validate_database_header(
        database=database,
        errors=errors,
        warnings=warnings,
    )

    result_ids: list[str] = []

    results = database.get("results")

    if isinstance(results, list):
        for record_index, record in enumerate(
            results,
            start=1,
        ):
            result_id = validate_result_record(
                record=record,
                record_index=record_index,
                errors=errors,
                warnings=warnings,
            )

            if result_id is not None:
                result_ids.append(result_id)

    validate_unique_result_ids(
        result_ids=result_ids,
        errors=errors,
    )

    return {
        "valid": len(errors) == 0,
        "error_count": len(errors),
        "warning_count": len(warnings),
        "errors": errors,
        "warnings": warnings,
    }


def validate_database_file(
    database_file: Path,
) -> dict:
    """
    Load and validate one database JSON file.
    """

    database = load_json_file(
        database_file
    )

    return validate_database(database)