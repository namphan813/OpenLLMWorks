"""
OpenLLMBench Interesting Facts Engine

Purpose:
Transforms database statistics and leaderboard results into
short, reusable facts for terminal viewers, websites, reports,
and future monthly snapshots.

Version:
0.7.0-dev1
"""

from typing import Any

from analytics.leaderboards import build_leaderboards
from analytics.statistics import build_statistics


FACTS_MODULE_VERSION = "0.7.0-dev1"


# ------------------------------------------------------------
# SAFE HELPERS
# ------------------------------------------------------------

def format_number(
    value: Any,
    decimal_places: int = 2,
) -> str:
    """
    Format a numeric value for fact text.
    """

    if isinstance(value, bool):
        return "Unavailable"

    if isinstance(value, (int, float)):
        return f"{value:.{decimal_places}f}"

    return "Unavailable"


def pluralize(
    count: int,
    singular: str,
    plural: str | None = None,
) -> str:
    """
    Return the correct singular or plural label.
    """

    if count == 1:
        return singular

    return plural or f"{singular}s"


def first_counter_entry(
    counts: dict[str, int],
) -> tuple[str, int] | None:
    """
    Return the first item from an already-ranked count dictionary.
    """

    if not counts:
        return None

    label = next(iter(counts))
    return label, counts[label]


def add_fact(
    facts: list[dict],
    *,
    fact_id: str,
    category: str,
    title: str,
    value: Any,
    description: str,
) -> None:
    """
    Add one consistently structured fact.
    """

    facts.append(
        {
            "fact_id": fact_id,
            "category": category,
            "title": title,
            "value": value,
            "description": description,
        }
    )


# ------------------------------------------------------------
# FACT GENERATION
# ------------------------------------------------------------

def build_database_facts(
    statistics_report: dict,
) -> list[dict]:
    """
    Build facts describing database size and import activity.
    """

    facts: list[dict] = []

    database_stats = statistics_report["database"]
    submission_stats = statistics_report["submissions"]

    total_results = database_stats["total_results"]

    add_fact(
        facts,
        fact_id="database_total_results",
        category="database",
        title="Database Results",
        value=total_results,
        description=(
            f"OpenLLMBench currently contains "
            f"{total_results} unique "
            f"{pluralize(total_results, 'benchmark result')}."
        ),
    )

    import_count = submission_stats["import_event_count"]

    add_fact(
        facts,
        fact_id="database_import_events",
        category="database",
        title="Import Events",
        value=import_count,
        description=(
            f"The database has recorded "
            f"{import_count} "
            f"{pluralize(import_count, 'import event')}."
        ),
    )

    import_status_counts = submission_stats[
        "import_status_counts"
    ]

    duplicate_count = import_status_counts.get(
        "duplicate",
        0,
    )

    add_fact(
        facts,
        fact_id="duplicates_detected",
        category="database",
        title="Duplicates Detected",
        value=duplicate_count,
        description=(
            f"Duplicate protection has blocked "
            f"{duplicate_count} duplicate "
            f"{pluralize(duplicate_count, 'submission')}."
        ),
    )

    return facts


def build_performance_facts(
    statistics_report: dict,
    leaderboard_report: dict,
) -> list[dict]:
    """
    Build facts describing benchmark performance.
    """

    facts: list[dict] = []

    performance_stats = statistics_report[
        "performance"
    ]

    leaders = leaderboard_report["leaders"]

    average_pp512 = performance_stats[
        "average_pp512"
    ]

    add_fact(
        facts,
        fact_id="average_pp512",
        category="performance",
        title="Average Prompt Processing",
        value=average_pp512,
        description=(
            f"The database-wide average pp512 result is "
            f"{format_number(average_pp512)} tokens/sec."
        ),
    )

    average_tg128 = performance_stats[
        "average_tg128"
    ]

    add_fact(
        facts,
        fact_id="average_tg128",
        category="performance",
        title="Average Token Generation",
        value=average_tg128,
        description=(
            f"The database-wide average tg128 result is "
            f"{format_number(average_tg128)} tokens/sec."
        ),
    )

    fastest_pp512 = leaders.get(
        "fastest_pp512"
    )

    if fastest_pp512:
        add_fact(
            facts,
            fact_id="fastest_pp512",
            category="performance",
            title="Fastest Prompt Processing",
            value=fastest_pp512["value"],
            description=(
                f"{fastest_pp512['gpu_model']} currently leads "
                f"pp512 at "
                f"{format_number(fastest_pp512['value'])} "
                f"tokens/sec, submitted as "
                f"{fastest_pp512['submission_name']}."
            ),
        )

    fastest_tg128 = leaders.get(
        "fastest_tg128"
    )

    if fastest_tg128:
        add_fact(
            facts,
            fact_id="fastest_tg128",
            category="performance",
            title="Fastest Token Generation",
            value=fastest_tg128["value"],
            description=(
                f"{fastest_tg128['gpu_model']} currently leads "
                f"tg128 at "
                f"{format_number(fastest_tg128['value'])} "
                f"tokens/sec, submitted as "
                f"{fastest_tg128['submission_name']}."
            ),
        )

    return facts


def build_hardware_facts(
    statistics_report: dict,
    leaderboard_report: dict,
) -> list[dict]:
    """
    Build facts describing hardware represented in the database.
    """

    facts: list[dict] = []

    hardware_stats = statistics_report["hardware"]
    leaders = leaderboard_report["leaders"]

    most_common_gpu = leaders.get(
        "most_common_gpu"
    )

    if most_common_gpu:
        gpu_count = most_common_gpu["count"]

        add_fact(
            facts,
            fact_id="most_common_gpu",
            category="hardware",
            title="Most Common GPU",
            value=most_common_gpu["label"],
            description=(
                f"{most_common_gpu['label']} is currently the "
                f"most represented GPU with "
                f"{gpu_count} "
                f"{pluralize(gpu_count, 'submission')} "
                f"({most_common_gpu['percentage']:.2f}%)."
            ),
        )

    most_common_cpu = leaders.get(
        "most_common_cpu"
    )

    if most_common_cpu:
        cpu_count = most_common_cpu["count"]

        add_fact(
            facts,
            fact_id="most_common_cpu",
            category="hardware",
            title="Most Common CPU",
            value=most_common_cpu["label"],
            description=(
                f"{most_common_cpu['label']} is currently the "
                f"most represented CPU with "
                f"{cpu_count} "
                f"{pluralize(cpu_count, 'submission')} "
                f"({most_common_cpu['percentage']:.2f}%)."
            ),
        )

    most_common_os = first_counter_entry(
        hardware_stats[
            "operating_system_counts"
        ]
    )

    if most_common_os:
        os_name, os_count = most_common_os

        add_fact(
            facts,
            fact_id="most_common_operating_system",
            category="hardware",
            title="Most Common Operating System",
            value=os_name,
            description=(
                f"{os_name} is the most represented operating "
                f"system with "
                f"{os_count} "
                f"{pluralize(os_count, 'result')}."
            ),
        )

    largest_vram = leaders.get(
        "largest_vram"
    )

    if largest_vram:
        add_fact(
            facts,
            fact_id="largest_vram",
            category="hardware",
            title="Largest VRAM Capacity",
            value=largest_vram["value"],
            description=(
                f"{largest_vram['gpu_model']} currently has the "
                f"largest recorded VRAM capacity at "
                f"{format_number(largest_vram['value'])} GiB."
            ),
        )

    largest_memory = leaders.get(
        "largest_memory"
    )

    if largest_memory:
        add_fact(
            facts,
            fact_id="largest_system_memory",
            category="hardware",
            title="Largest System Memory",
            value=largest_memory["value"],
            description=(
                f"{largest_memory['submission_name']} currently "
                f"has the largest recorded system memory "
                f"capacity at "
                f"{format_number(largest_memory['value'])} GB."
            ),
        )

    average_vram = hardware_stats[
        "average_vram_gib"
    ]

    add_fact(
        facts,
        fact_id="average_vram",
        category="hardware",
        title="Average VRAM",
        value=average_vram,
        description=(
            f"The average recorded GPU has "
            f"{format_number(average_vram)} GiB of VRAM."
        ),
    )

    average_memory = hardware_stats[
        "average_memory_gb"
    ]

    add_fact(
        facts,
        fact_id="average_system_memory",
        category="hardware",
        title="Average System Memory",
        value=average_memory,
        description=(
            f"The average benchmark system has "
            f"{format_number(average_memory)} GB of memory."
        ),
    )

    return facts


# ------------------------------------------------------------
# COMPLETE FACT REPORT
# ------------------------------------------------------------

def build_interesting_facts(
    database: dict,
) -> dict:
    """
    Build the complete OpenLLMBench interesting-facts report.

    The returned structure contains no terminal or website
    formatting. It can later power:

    - facts.py
    - the website homepage
    - monthly snapshots
    - reports
    - APIs
    """

    statistics_report = build_statistics(
        database
    )

    leaderboard_report = build_leaderboards(
        database
    )

    database_facts = build_database_facts(
        statistics_report
    )

    performance_facts = build_performance_facts(
        statistics_report,
        leaderboard_report,
    )

    hardware_facts = build_hardware_facts(
        statistics_report,
        leaderboard_report,
    )

    all_facts = (
        database_facts
        + performance_facts
        + hardware_facts
    )

    return {
        "facts_version": FACTS_MODULE_VERSION,
        "database_result_count": statistics_report[
            "database"
        ]["total_results"],
        "fact_count": len(all_facts),
        "categories": {
            "database": database_facts,
            "performance": performance_facts,
            "hardware": hardware_facts,
        },
        "facts": all_facts,
    }