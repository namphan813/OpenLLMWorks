# OpenLLMWorks Data Contract v1.0

## Purpose

This document defines the generated data consumed by the OpenLLMWorks website.

The website never computes statistics directly.

Instead, Python generates JSON files that become the single source of truth for the frontend.

---

# Data Flow

llama.cpp
↓
Benchmark Parser
↓
Benchmark Database
↓
Analytics Engine
↓
Generated JSON
↓
React Website

---

# Generated Files

database/generated/

    homepage.json
    hardware.json
    leaderboards.json
    snapshots.json
    trends.json

---

# homepage.json

Purpose:

Provides the data required for the homepage.

Contains:

- Summary statistics
- Featured community story
- Generation timestamp

Example

{
    "generatedAt": "...",

    "stats": {
        "benchmarkResults": 0,
        "gpuModels": 0,
        "cpuModels": 0,
        "importEvents": 0,
        "averageTg128": 0.0
    },

    "featuredStory": {
        "title": "...",
        "description": "...",
        "snapshot": "...",
        "badge": "Data Snapshot"
    }
}

---

# hardware.json

Purpose:

Complete list of hardware represented in the database.

Contains:

- GPU information
- CPU information
- System count
- Platform information

---

# leaderboards.json

Purpose:

Precomputed rankings.

Contains:

- Fastest GPUs
- Fastest CPUs
- Highest tg128
- Highest pp512

---

# snapshots.json

Purpose:

Historical database growth.

Contains:

- Total benchmarks
- Total hardware
- Total contributors
- Growth over time

---

# trends.json

Purpose:

Long-term analytics.

Contains:

- GPU vendor trends
- CPU vendor trends
- Model popularity
- Average performance over time

---

# Design Principles

• Website never calculates statistics.

• Python owns all analytics.

• JSON is the contract between backend and frontend.

• Every generated file can be regenerated at any time.

• Generated files should be deterministic.