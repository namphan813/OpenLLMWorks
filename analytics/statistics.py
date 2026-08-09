"""
OpenLLMBench Statistics Engine

Purpose:
Transforms validated benchmark database records into aggregate
statistics for command-line tools, reports, websites, and APIs.

Version:
0.7.0-dev1
"""

from collections import Counter
from statistics import mean
from typing import Any


STATISTICS_MODULE_VERSION = "0.7.0-dev1"


# ------------------------------------------------------------
# SAFE VALUE HELPERS
# ------------------------------------------------------------

def get_nested(
    data: dict,
    *keys: str,
    default: Any = None,
) -> Any:
    """
    Safely retrieve a value from nested dictionaries.

    Example:
        get_nested(
            record,
            "hardware",
            "gpu",
            "model",
        )
    """

    current: Any = data

    for key in keys:
        if not isinstance(current, dict):
            return default

        if key not in current:
            return default

        current = current[key]

    return current


def clean_text(
    value: Any,
    fallback: str = "Unknown",
) -> str:
    """
    Return a cleaned text value or a fallback label.
    """

    if not isinstance(value, str):
        return fallback

    cleaned = value.strip()

    return cleaned if cleaned else fallback


def valid_number(
    value: Any,
) -> bool:
    """
    Return True when a value is a usable number.

    Boolean values are rejected even though Python treats them
    as integers.
    """

    return (
        isinstance(value, (int, float))
        and not isinstance(value, bool)
    )


# ------------------------------------------------------------
# VENDOR DETECTION
# ------------------------------------------------------------

def detect_cpu_vendor(
    cpu_model: str,
) -> str:
    """
    Infer the CPU vendor from its model name.
    """

    normalized = cpu_model.lower()

    if "intel" in normalized:
        return "Intel"

    if (
        "amd" in normalized
        or "ryzen" in normalized
        or "threadripper" in normalized
        or "epyc" in normalized
    ):
        return "AMD"

    if (
        "apple" in normalized
        or normalized.startswith("m1")
        or normalized.startswith("m2")
        or normalized.startswith("m3")
        or normalized.startswith("m4")
        or normalized.startswith("m5")
    ):
        return "Apple"

    return "Unknown"


def normalize_gpu_vendor(
    vendor: Any,
    gpu_model: Any,
) -> str:
    """
    Normalize the GPU vendor.

    The database vendor field is preferred. The model name is
    used as a fallback when the vendor field is missing.
    """

    vendor_text = clean_text(
        vendor,
        fallback="",
    )

    if vendor_text:
        normalized = vendor_text.lower()

        if "nvidia" in normalized:
            return "NVIDIA"

        if "amd" in normalized:
            return "AMD"

        if "intel" in normalized:
            return "Intel"

        if "apple" in normalized:
            return "Apple"

        return vendor_text

    model_text = clean_text(
        gpu_model,
        fallback="",
    ).lower()

    if "nvidia" in model_text:
        return "NVIDIA"

    if (
        "radeon" in model_text
        or "amd" in model_text
    ):
        return "AMD"

    if (
        "intel" in model_text
        or "arc" in model_text
        or "uhd" in model_text
        or "iris" in model_text
    ):
        return "Intel"

    if "apple" in model_text:
        return "Apple"

    return "Unknown"


# ------------------------------------------------------------
# COUNTER HELPERS
# ------------------------------------------------------------

def counter_to_dict(
    counter: Counter,
) -> dict[str, int]:
    """
    Convert a Counter into a consistently sorted dictionary.

    Results are ordered by:

    1. Highest count
    2. Alphabetical label
    """

    sorted_items = sorted(
        counter.items(),
        key=lambda item: (
            -item[1],
            item[0].lower(),
        ),
    )

    return {
        label: count
        for label, count in sorted_items
    }


def calculate_percentages(
    counts: dict[str, int],
    total: int,
) -> dict[str, float]:
    """
    Calculate percentage share for each count.
    """

    if total <= 0:
        return {
            label: 0.0
            for label in counts
        }

    return {
        label: round(
            count / total * 100,
            2,
        )
        for label, count in counts.items()
    }


# ------------------------------------------------------------
# RECORD EXTRACTION
# ------------------------------------------------------------

def extract_result_rows(
    database: dict,
) -> list[dict]:
    """
    Convert database result records into flattened analytics rows.

    This creates a reusable analytics-friendly representation
    without modifying the original database records.
    """

    database_results = database.get(
        "results",
        [],
    )

    if not isinstance(database_results, list):
        return []

    rows: list[dict] = []

    for record in database_results:
        if not isinstance(record, dict):
            continue

        gpu_model = clean_text(
            get_nested(
                record,
                "hardware",
                "gpu",
                "model",
            )
        )

        gpu_vendor = normalize_gpu_vendor(
            vendor=get_nested(
                record,
                "hardware",
                "gpu",
                "vendor",
            ),
            gpu_model=gpu_model,
        )

        cpu_model = clean_text(
            get_nested(
                record,
                "hardware",
                "cpu",
                "model",
            )
        )

        normalized_os_name = clean_text(
            get_nested(
                record,
                "hardware",
                "operating_system",
                "normalized",
                "name",
            )
        )

        normalized_os_release = clean_text(
            get_nested(
                record,
                "hardware",
                "operating_system",
                "normalized",
                "release",
            ),
            fallback="",
        )

        if normalized_os_release:
            operating_system = (
                f"{normalized_os_name} "
                f"{normalized_os_release}"
            )
        else:
            operating_system = normalized_os_name

        row = {
            "result_id": clean_text(
                record.get("result_id")
            ),
            "submission_name": clean_text(
                get_nested(
                    record,
                    "submission",
                    "submission_name",
                )
            ),
            "benchmark_status": clean_text(
                get_nested(
                    record,
                    "benchmark",
                    "status",
                )
            ),
            "backend": clean_text(
                get_nested(
                    record,
                    "benchmark",
                    "protocol",
                    "backend",
                )
            ),
            "gpu_vendor": gpu_vendor,
            "gpu_model": gpu_model,
            "gpu_type": clean_text(
                get_nested(
                    record,
                    "hardware",
                    "gpu",
                    "type",
                )
            ),
            "gpu_form_factor": clean_text(
                get_nested(
                    record,
                    "hardware",
                    "gpu",
                    "form_factor",
                )
            ),
            "vram_gib": get_nested(
                record,
                "hardware",
                "gpu",
                "vram",
                "capacity_gib",
            ),
            "cpu_vendor": detect_cpu_vendor(
                cpu_model
            ),
            "cpu_model": cpu_model,
            "memory_gb": get_nested(
                record,
                "hardware",
                "memory",
                "installed_capacity_gb",
            ),
            "operating_system": operating_system,
            "pp512": get_nested(
                record,
                "benchmark",
                "average",
                "pp512",
            ),
            "tg128": get_nested(
                record,
                "benchmark",
                "average",
                "tg128",
            ),
        }

        rows.append(row)

    return rows


# ------------------------------------------------------------
# PERFORMANCE STATISTICS
# ------------------------------------------------------------

def calculate_performance_statistics(
    rows: list[dict],
) -> dict:
    """
    Calculate overall benchmark performance statistics.
    """

    pp_values = [
        row["pp512"]
        for row in rows
        if valid_number(row.get("pp512"))
    ]

    tg_values = [
        row["tg128"]
        for row in rows
        if valid_number(row.get("tg128"))
    ]

    fastest_pp512 = None
    fastest_tg128 = None

    valid_pp_rows = [
        row
        for row in rows
        if valid_number(row.get("pp512"))
    ]

    valid_tg_rows = [
        row
        for row in rows
        if valid_number(row.get("tg128"))
    ]

    if valid_pp_rows:
        fastest_row = max(
            valid_pp_rows,
            key=lambda row: row["pp512"],
        )

        fastest_pp512 = {
            "result_id": fastest_row["result_id"],
            "submission_name": (
                fastest_row["submission_name"]
            ),
            "gpu_model": fastest_row["gpu_model"],
            "value": fastest_row["pp512"],
        }

    if valid_tg_rows:
        fastest_row = max(
            valid_tg_rows,
            key=lambda row: row["tg128"],
        )

        fastest_tg128 = {
            "result_id": fastest_row["result_id"],
            "submission_name": (
                fastest_row["submission_name"]
            ),
            "gpu_model": fastest_row["gpu_model"],
            "value": fastest_row["tg128"],
        }

    return {
        "average_pp512": (
            round(mean(pp_values), 2)
            if pp_values
            else None
        ),
        "average_tg128": (
            round(mean(tg_values), 2)
            if tg_values
            else None
        ),
        "fastest_pp512": fastest_pp512,
        "fastest_tg128": fastest_tg128,
    }


# ------------------------------------------------------------
# HARDWARE STATISTICS
# ------------------------------------------------------------

def calculate_hardware_statistics(
    rows: list[dict],
) -> dict:
    """
    Calculate hardware counts, distributions, and averages.
    """

    gpu_vendor_counter = Counter(
        row["gpu_vendor"]
        for row in rows
    )

    gpu_model_counter = Counter(
        row["gpu_model"]
        for row in rows
    )

    cpu_vendor_counter = Counter(
        row["cpu_vendor"]
        for row in rows
    )

    cpu_model_counter = Counter(
        row["cpu_model"]
        for row in rows
    )

    gpu_type_counter = Counter(
        row["gpu_type"]
        for row in rows
    )

    operating_system_counter = Counter(
        row["operating_system"]
        for row in rows
    )

    backend_counter = Counter(
        row["backend"]
        for row in rows
    )

    vram_values = [
        row["vram_gib"]
        for row in rows
        if valid_number(row.get("vram_gib"))
    ]

    memory_values = [
        row["memory_gb"]
        for row in rows
        if valid_number(row.get("memory_gb"))
    ]

    gpu_vendor_counts = counter_to_dict(
        gpu_vendor_counter
    )

    return {
        "gpu_vendor_counts": gpu_vendor_counts,
        "gpu_vendor_percentages": (
            calculate_percentages(
                counts=gpu_vendor_counts,
                total=len(rows),
            )
        ),
        "gpu_model_counts": counter_to_dict(
            gpu_model_counter
        ),
        "gpu_type_counts": counter_to_dict(
            gpu_type_counter
        ),
        "cpu_vendor_counts": counter_to_dict(
            cpu_vendor_counter
        ),
        "cpu_model_counts": counter_to_dict(
            cpu_model_counter
        ),
        "operating_system_counts": (
            counter_to_dict(
                operating_system_counter
            )
        ),
        "backend_counts": counter_to_dict(
            backend_counter
        ),
        "average_vram_gib": (
            round(mean(vram_values), 2)
            if vram_values
            else None
        ),
        "average_memory_gb": (
            round(mean(memory_values), 2)
            if memory_values
            else None
        ),
    }


# ------------------------------------------------------------
# SUBMISSION STATISTICS
# ------------------------------------------------------------

def calculate_submission_statistics(
    rows: list[dict],
    database: dict,
) -> dict:
    """
    Calculate benchmark status and import-history statistics.
    """

    status_counter = Counter(
        row["benchmark_status"]
        for row in rows
    )

    import_history = database.get(
        "import_history",
        [],
    )

    if not isinstance(import_history, list):
        import_history = []

    import_status_counter = Counter()

    for event in import_history:
        if not isinstance(event, dict):
            continue

        status = clean_text(
            event.get("status")
        )

        import_status_counter[status] += 1

    return {
        "benchmark_status_counts": (
            counter_to_dict(
                status_counter
            )
        ),
        "import_event_count": len(
            import_history
        ),
        "import_status_counts": (
            counter_to_dict(
                import_status_counter
            )
        ),
    }


# ------------------------------------------------------------
# COMPLETE STATISTICS REPORT
# ------------------------------------------------------------

def build_statistics(
    database: dict,
) -> dict:
    """
    Build the complete OpenLLMBench statistics report.

    The returned dictionary contains no terminal formatting and
    can be reused by command-line tools, websites, reports, or APIs.
    """

    rows = extract_result_rows(database)

    return {
        "statistics_version": (
            STATISTICS_MODULE_VERSION
        ),
        "database": {
            "project": clean_text(
                database.get("project"),
                fallback=(
                    "Open LLM Benchmark Database"
                ),
            ),
            "schema_version": clean_text(
                database.get("schema_version")
            ),
            "parser_version": clean_text(
                database.get("parser_version")
            ),
            "generated_at": clean_text(
                database.get("generated_at")
            ),
            "total_results": len(rows),
        },
        "submissions": (
            calculate_submission_statistics(
                rows=rows,
                database=database,
            )
        ),
        "hardware": (
            calculate_hardware_statistics(
                rows=rows
            )
        ),
        "performance": (
            calculate_performance_statistics(
                rows=rows
            )
        ),
    }