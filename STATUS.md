# OpenLLMBench — Project Status

Last Updated: August 9, 2026  
Current Development Phase: Weekend 11 — Discovery & Comparison  
Active Development Branch: `weekend-11-discovery-comparison`  
Repository State: Weekend 11 baseline established; canonical result identity reconciled; publisher and production build validated

---

## Project Overview

OpenLLMBench is an open-source benchmark database focused on measuring,
comparing, and preserving the performance history of local AI hardware.

The project has evolved from a collection of local benchmarking scripts into
an end-to-end data platform capable of accepting benchmark submissions,
validating and normalizing them, preserving them in a persistent database,
analyzing the resulting dataset, publishing structured data, and presenting
that information through an interactive website.

The long-term goal is to create a community-driven historical record of local
LLM hardware performance.

**Measure. Understand. Preserve.**

---

## Current System Architecture

OpenLLMBench has a functioning end-to-end data path:

```text
Benchmark Run
    |
    v
Raw Benchmark + Hardware Files
    |
    v
incoming/
    |
    v
Parser
    |
    v
Validation / Normalization
    |
    v
Canonical Result Identity
    |
    v
Duplicate Detection
    |
    v
Persistent Benchmark Database
    |
    v
Analytics / Statistics
    |
    v
Publisher
    |
    v
Generated JSON
    |
    v
Interactive Website