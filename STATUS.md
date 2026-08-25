# OpenLLMBench - Project Status

## Weekend 15 - Sprint 5 In Progress

**Focus:** Runner to Contributor Ready
**Status:** Stable / Final Cleanup and Checkpoint

---

## Weekend 15 Objective

Move the OpenLLMBench Runner from a proven development workflow toward a
safer, clearer contributor-facing system while preserving
maintainer-controlled ingestion.

---

## Completed Sprints

### Sprint 1 - Runner Hardening

- Hardened canonical `submission_name` validation.
- Restricted canonical submission names to letters, numbers, hyphens, and underscores.
- Added a 128-character submission-name limit.
- Added benchmark-readiness guidance before execution.
- Clarified that Benchmark Protocol v1.0 does not require a fixed cooldown period.
- Improved environment-verification failure guidance.
- Improved benchmark-process failure reporting while preserving raw output.
- Improved result-parsing failure guidance while preserving benchmark evidence.

### Sprint 2 - Maintainer Workflow

- Added a focused single-submission maintainer processing path.
- Added trusted maintainer-controlled provenance inputs.
- Added `scripts/process_submission.py`.
- Preserved deterministic result IDs and canonical duplicate detection.
- Documented the maintainer submission workflow.
- Kept contributor packages separate from maintainer-assigned trust metadata.

### Sprint 3 - Contributor UX and Documentation

- Updated contributor documentation around the Runner-first workflow.
- Documented current Runner setup requirements and limitations.
- Documented Runner output, validation, packaging, and failure states.
- Updated the GitHub benchmark-submission Issue workflow.
- Added Runner vs manual/advanced submission-method selection.
- Aligned the root README with the Runner-first contribution path.
- Preserved manual validation for troubleshooting and advanced workflows.
- Standardized contributor-facing validation examples on `python -m parser.validate`.
- Documented that a standalone contributor executable is planned but not yet available.

### Sprint 4 - Regression Testing

Performed a fresh current-build end-to-end smoke test using:

- NVIDIA Quadro T1000
- 4 GB VRAM
- Runner version `0.3.0-dev3`

The Runner successfully verified the environment and frozen assets, captured
all required hardware evidence, displayed readiness guidance, completed three
benchmark runs, parsed the results, generated `submission.json`, passed
canonical validation, and created an upload-ready ZIP.

| Run | pp512 | tg128 |
|---|---:|---:|
| 1 | 117.41 t/s | 35.41 t/s |
| 2 | 114.78 t/s | 32.13 t/s |
| 3 | 117.29 t/s | 29.98 t/s |
| **Average** | **116.49 t/s** | **32.51 t/s** |

The generated ZIP was extracted into a clean temporary directory and
independently validated with the canonical validator.

Independent validation confirmed:

- `submission.json` present
- manifest schema 1.0 valid
- hardware evidence 5/5 present
- benchmark runs 3/3 present
- validation passed

---

## Current Proven Contributor Handoff

```text
Contributor System
    |
    v
OpenLLMBench Runner
    |
    v
Environment and Asset Verification
    |
    v
Hardware Evidence Capture
    |
    v
Three Benchmark Runs
    |
    v
Result Parsing
    |
    v
submission.json
    |
    v
Canonical Validation
    |
    v
Upload-Ready ZIP
    |
    v
GitHub Benchmark Submission Issue
    |
    v
Maintainer Download / Extraction
    |
    v
Independent Canonical Validation
    |
    v
Controlled Maintainer Import
    |
    v
Canonical Database
    |
    v
Publisher
    |
    v
Website
```

The Runner remains intentionally isolated from the canonical database.

---

## Current Runner Constraints

The development Runner currently requires Windows, Python, the OpenLLMBench
repository or Runner source, the frozen Benchmark Protocol v1.0 model, the
frozen `llama-bench.exe` engine, and the expected benchmark directory
structure.

These are now the primary usability barriers between the proven workflow and
a low-friction public contributor experience.

---

## Sprint 5 - Cleanup / Checkpoint

Current landing work:

- repository health checks
- project-status reconciliation
- roadmap reconciliation
- stale README milestone cleanup
- final documentation consistency review
- final commit and clean-tree checkpoint

Repository health checks completed so far:

- working tree clean before checkpoint edits
- `git diff --check` clean
- `python -m compileall parser runner scripts` completed without errors

---

## Next

**Weekend 16 - Standalone Runner and Distribution**

Primary questions include executable packaging, dependency/bootstrap strategy,
frozen asset acquisition and verification, clean-Windows setup, fixed-path
assumptions, and console versus lightweight-GUI presentation.

The goal is to reduce contributor setup friction without weakening benchmark
reproducibility, raw-evidence preservation, or maintainer-controlled ingestion.

---

## Weekend 14 — Sprint 6 Complete

**Focus:** End-to-End Runner Validation
**Status:** Stable / Production-Style Workflow Proven

---

## Completed

- Performed the first fresh-GPU end-to-end OpenLLMBench Runner test
- Test hardware:
  - Bench-001
  - NVIDIA GeForce GTX 1050
  - 2 GB VRAM
  - Intel Core i5-8600K
  - 16 GB system memory
  - Windows 11 Pro 25H2
- Runner successfully:
  - detected the installed GPU
  - verified the benchmark model
  - verified llama-bench
  - captured hardware evidence
  - executed all three required benchmark runs
  - parsed pp512 and tg128
  - generated `submission.json`
  - passed canonical submission validation
  - created an upload-ready ZIP
- Submitted the Runner-generated ZIP through the GitHub Issues workflow
- Downloaded the submission on the maintainer/development system
- Independently validated the extracted submission using `parser.validate`
- Imported the submission using the single-submission maintainer workflow
- Applied GitHub Issue provenance and maintainer verification
- Added the result to the canonical database
- Republished generated website data
- Verified the GTX 1050 2GB appears correctly in the local hardware interface

---

## First End-to-End Runner Result

**GPU:** NVIDIA GeForce GTX 1050
**VRAM:** 2 GB

| Run | pp512 | tg128 |
|---|---:|---:|
| 1 | 123.09 t/s | 3.99 t/s |
| 2 | 126.70 t/s | 3.99 t/s |
| 3 | 125.62 t/s | 3.99 t/s |
| **Average** | **125.14 t/s** | **3.99 t/s** |

**Result ID:** `result_a64036c1c64f3997`

**Source:** GitHub Issue
**Verification:** Maintainer verified

Database result count after import: **9**

---

## Validated Workflow

The complete OpenLLMBench contribution lifecycle has now been demonstrated:

```text
Install GPU
    ↓
Run OpenLLMBench Runner
    ↓
Environment Verification
    ↓
Hardware Evidence Capture
    ↓
Three Benchmark Runs
    ↓
Result Parsing
    ↓
submission.json
    ↓
Canonical Validation
    ↓
Submission ZIP
    ↓
GitHub Issue
    ↓
Maintainer Download
    ↓
Independent Validation
    ↓
Canonical Database Import
    ↓
Publisher
    ↓
OpenLLMBench Website
```

This confirms that benchmark execution and submission packaging can occur on a separate benchmark system while database ingestion and publishing remain maintainer-controlled.

---

## Observations

- Runner successfully handled a 2 GB GPU despite the benchmark model being larger than available VRAM.
- The GTX 1050 produced substantially lower tg128 performance than higher-VRAM tested GPUs.
- The Runner required Python on the benchmark system.
- Git was not required for benchmark execution.
- OneDrive provided a convenient development deployment path between the maintainer and Bench-001 systems.
- The flat ZIP structure works correctly but is less convenient when manually extracting submissions in Windows.

---

## Next

Continue Runner validation using additional GPU generations and configurations.

Candidate next steps:

- Test additional GPUs on Bench-001
- Improve Runner contributor UX
- Evaluate friendlier ZIP extraction/package structure
- Improve dependency/bootstrap handling
- Reduce or eliminate the requirement for users to install Python
- Explore packaging the Runner as a standalone executable
- Continue toward the eventual one-click OpenLLMBench Runner experience

---

## Weekend 14 — Sprint 5 Complete

**Focus:** OpenLLMBench Runner v0
**Status:** Stable / Clean Checkpoint

---

## Completed

- Implemented the initial OpenLLMBench Runner
- Added automatic NVIDIA GPU and environment detection
- Added benchmark model verification using SHA-256
- Added llama-bench executable verification using SHA-256
- Added automatic benchmark workspace creation
- Added automatic hardware evidence collection:
  - CPU
  - System memory
  - System manufacturer and model
  - Windows version and build
  - NVIDIA GPU / driver information
- Added automatic execution of the OpenLLMBench Benchmark Protocol v1.0
- Runner executes three independent benchmark runs
- Added automatic parsing of:
  - pp512
  - tg128
  - llama.cpp commit
  - llama.cpp build
- Added benchmark result summary and averages
- Added automatic `submission.json` manifest generation
- Integrated the canonical OpenLLMBench submission validator
- Added automatic ZIP packaging after successful validation
- ZIP packages use the canonical flat submission structure
- Failed validation prevents ZIP creation
- Partial benchmark evidence is preserved when execution fails
- Runner does not modify the canonical OpenLLMBench database

---

## Runner Workflow

The current Runner pipeline is:

```text
Start Runner
    │
    ├── Detect NVIDIA GPU
    │
    ├── Verify benchmark model
    │      └── SHA-256
    │
    ├── Verify llama-bench.exe
    │      └── SHA-256
    │
    ├── Create benchmark workspace
    │
    ├── Capture hardware evidence
    │      ├── cpu.txt
    │      ├── memory.txt
    │      ├── system.txt
    │      ├── windows.txt
    │      └── nvidia-smi.txt
    │
    ├── Execute Benchmark Protocol v1.0
    │      ├── Run 1
    │      ├── Run 2
    │      └── Run 3
    │
    ├── Parse benchmark results
    │      ├── pp512
    │      ├── tg128
    │      ├── llama.cpp commit
    │      └── llama.cpp build
    │
    ├── Generate submission.json
    │
    ├── Run canonical submission validation
    │
    └── PASS
           │
           └── Create upload-ready ZIP
```

---

## Current Runner Output

A successful run produces:

```text
C:\AI-Benchmark\results\
    Runner-<GPU>-<timestamp>\
        benchmark-v1.0-p512-run1.txt
        benchmark-v1.0-p512-run2.txt
        benchmark-v1.0-p512-run3.txt
        cpu.txt
        memory.txt
        nvidia-smi.txt
        submission.json
        system.txt
        windows.txt

    Runner-<GPU>-<timestamp>.zip
```

The ZIP contains the canonical flat submission package ready for upload through the OpenLLMBench submission workflow.

---

## Current Architecture

```text
Benchmark System
      │
      ▼
OpenLLMBench Runner
      │
      ├── Environment Verification
      ├── Hardware Evidence
      ├── Benchmark Execution
      ├── Result Parsing
      ├── Manifest Generation
      ├── Canonical Validation
      └── ZIP Packaging
      │
      ▼
Submission Package
      │
      ▼
Maintainer Review / Import
      │
      ▼
Canonical Database
      │
      ▼
Publisher
      │
      ▼
Website
```

The Runner is intentionally isolated from the canonical database.

---

## Next

Continue validating the Runner against additional GPUs and benchmark systems.

Future Runner development may include:

- improved contributor-facing UX
- automatic dependency/bootstrap handling
- standalone executable packaging
- simplified upload workflow
- additional GPU vendor support
- eventual one-click benchmark and submission experience
