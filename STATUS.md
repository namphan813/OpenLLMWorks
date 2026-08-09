# OpenLLMBench — Project Status

Last Updated: August 8, 2026  
Current Development Phase: Weekend 10 — Complete  
Active Development Branch: `weekend-10-hardware-data`  
Repository State: Weekend 10 implementation validated; working tree clean prior to documentation closeout

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

OpenLLMBench now has a functioning end-to-end data path:

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
```

The website consumes published data rather than reading directly from the
benchmark database, preserving a separation between collection, analytics,
publishing, and presentation.

---

## Current Data Pipeline

The benchmark pipeline currently supports:

- Raw benchmark result ingestion
- CPU identification
- Installed system memory detection
- System manufacturer and model detection
- Windows version normalization
- NVIDIA GPU identification through `nvidia-smi`
- GPU VRAM detection
- NVIDIA driver and CUDA UMD version capture
- Submission validation and normalization
- Duplicate detection
- Persistent benchmark storage
- Statistical aggregation
- GPU profile generation
- Website-oriented JSON publishing

Hardware metadata is captured with benchmark submissions so performance can be
evaluated in the context of the system that produced it.

---

## Hardware Data Model

Weekend 10 established hardware as a first-class part of OpenLLMBench.

Published GPU profiles currently include:

- GPU vendor
- GPU model
- GPU VRAM
- Benchmark submission count
- Average pp512
- Average tg128
- Best pp512
- Worst pp512
- Observed system memory configurations
- Observed operating systems
- Individual benchmark history
- CPU model for individual results
- System memory for individual results
- VRAM for individual results

Multiple submissions using the same GPU can be aggregated into a single
hardware profile while retaining the individual benchmark configurations
behind the aggregate values.

---

## Website Status

The public-facing website foundation is operational.

Current website functionality includes:

- Shared site layout and navigation
- Hardware Explorer
- GPU search
- GPU vendor filtering
- Performance sorting
- Individual GPU profile routes
- Aggregate GPU performance metrics
- Tested memory configurations
- Tested operating systems
- Individual benchmark history
- Interactive Best pp512 filtering
- Interactive Worst pp512 filtering
- Interactive memory filtering
- Interactive operating-system filtering
- Clear-filter behavior
- Responsive hardware result cards
- Shared footer and project navigation

Hardware profile pages now connect aggregate benchmark statistics back to the
individual configurations that produced those results.

---

## Published Data

The site publisher currently produces:

```text
database/generated/homepage.json
database/generated/hardware.json
database/generated/manifest.json
```

The publisher successfully loads the persistent benchmark database, builds
statistics, generates hardware profiles, and writes the website-facing data
artifacts.

The website then consumes these generated artifacts as its data source.

---

## Weekend 10 Validation

Weekend 10 completed an end-to-end validation pass.

Validated successfully:

- Publisher execution
- Persistent database loading
- Statistics generation
- Hardware profile generation
- Generated JSON output
- Hardware Explorer rendering
- GPU profile rendering
- GTX 1650 multi-submission aggregation
- Quadro T1000 single-submission profile
- Search, vendor, and sorting controls
- Best/Worst pp512 result filtering
- Memory configuration filtering
- Operating-system filtering
- Filter clearing
- Production Vite build
- Clean Git working state prior to documentation closeout

The production website build completed successfully with no build errors.

---

## Current Test Dataset

The current published hardware dataset includes multiple benchmark submissions
across two NVIDIA GPU variants:

- NVIDIA GeForce GTX 1650 — multiple benchmark configurations
- NVIDIA Quadro T1000 — single benchmark configuration

The GTX 1650 dataset currently demonstrates that OpenLLMBench can aggregate
results from different host configurations while preserving the individual
benchmark records underneath the GPU profile.

This dataset is intentionally small while the hardware data contract and
presentation layer are being validated.

---

## Known Follow-Up Items

The following items are not blockers for the current milestone:

- Publisher regeneration updates `generatedAt` timestamps even when benchmark
  data has not changed, causing generated files to appear modified in Git.
- Generic/custom-built systems may report non-descriptive firmware identity
  values such as `System manufacturer` and `System Product Name`.
- Additional GPU vendors and hardware families still need real-world validation.
- Larger datasets will be needed to validate Hardware Explorer behavior at
  community scale.
- Additional configuration metadata may be surfaced as the hardware schema
  matures.

These items should be handled incrementally rather than expanding the current
milestone.

---

## Current Project State

OpenLLMBench now has a working foundation connecting:

**benchmark execution → hardware capture → normalization → persistent storage →
analytics → publishing → interactive hardware exploration**

The core architecture is functioning, the hardware publishing contract is
operational, and the website can expose both aggregate GPU performance and the
individual benchmark configurations behind those statistics.

Weekend 10 establishes the foundation for expanding the hardware catalog,
improving comparison and discovery tools, and preparing OpenLLMBench for
eventual community-facing use.

---

## Next Development Phase

**Weekend 11**

Primary direction:

- Build on the completed hardware-data foundation
- Expand discovery and comparison capabilities
- Continue website/product refinement
- Validate the architecture against a larger and more diverse benchmark dataset
- Advance toward public/community readiness

Detailed scope and sprint sequencing remain governed by `ROADMAP.md`.