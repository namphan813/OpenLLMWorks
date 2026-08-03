"""
OpenLLMBench Interesting Facts Viewer

Version:
0.7.0-dev1
"""

from pathlib import Path

from parser.database import load_database
from analytics.facts import build_interesting_facts

DATABASE_FILE = Path("database/benchmark_database.json")
PARSER_VERSION = "0.7.0-dev1"


def print_category(title: str):

    print()
    print("=" * 60)
    print(title)
    print("=" * 60)


def print_fact(fact: dict):

    print(f"• {fact['title']}")
    print(f"  {fact['description']}")
    print()


def main():

    print("OpenLLMBench Interesting Facts")
    print("Facts Viewer v0.7.0-dev1")
    print()

    database = load_database(
        DATABASE_FILE,
        PARSER_VERSION,
    )

    report = build_interesting_facts(database)

    print(f"Facts Generated: {report['fact_count']}")

    categories = report["categories"]

    print_category("Database")

    for fact in categories["database"]:
        print_fact(fact)

    print_category("Performance")

    for fact in categories["performance"]:
        print_fact(fact)

    print_category("Hardware")

    for fact in categories["hardware"]:
        print_fact(fact)


if __name__ == "__main__":
    main()