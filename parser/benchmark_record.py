"""
OpenLLMBench Benchmark Record Model

Purpose:
Defines the structured benchmark record produced from one parsed
OpenLLMBench submission.

Version:
0.6.0-dev2
"""

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class BenchmarkRecord:
    """
    Immutable representation of one processed benchmark submission.

    The record stores the complete schema-ready benchmark data while
    keeping JSON serialization outside the parser orchestration layer.
    """

    schema_version: str
    project: str
    protocol: dict[str, Any]
    submission: dict[str, Any]
    hardware: dict[str, Any]
    llama_cpp: dict[str, Any]
    runs: list[dict[str, Any]]
    average: dict[str, float]

    def to_dict(self) -> dict[str, Any]:
        """
        Return the benchmark record as a JSON-serializable dictionary.
        """

        return {
            "schema_version": self.schema_version,
            "project": self.project,
            "protocol": self.protocol,
            "submission": self.submission,
            "hardware": self.hardware,
            "llama_cpp": self.llama_cpp,
            "runs": self.runs,
            "average": self.average,
        }
