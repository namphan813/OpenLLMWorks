# OpenLLMBench Runner Distribution

## Purpose

This document defines the distribution architecture for the
contributor-facing OpenLLMBench Runner.

The goal is to allow a contributor to run the OpenLLMBench benchmark and
produce a validated submission package without requiring knowledge of Python,
Git, repository internals, or command-line development workflows.

The distribution architecture must preserve the reproducibility and trust
requirements of the OpenLLMBench benchmark protocol.

---

# Distribution Goals

The contributor experience should eventually approach:

```text
Download OpenLLMBench Runner
        |
        v
Launch Runner
        |
        v
Verify / Prepare Benchmark Environment
        |
        v
Run Benchmark
        |
        v
Validate Submission
        |
        v
Receive Upload-Ready ZIP
```

The Runner must not receive authority to modify the canonical OpenLLMBench
database.

---

# Application Packaging

The standalone Runner should package the Python application layer required for
benchmark execution.

This includes:

- `runner/run_benchmark.py`
- `parser.submission`
- `parser.validate`
- required OpenLLMBench internal modules
- required Python standard-library/runtime components

The contributor should not need to install Python separately.

Current dependency inspection shows that the Runner and required validation
modules rely primarily on the Python standard library and OpenLLMBench
internal modules.

This makes standalone application packaging relatively self-contained.

---

# Benchmark Assets

The benchmark engine and model should remain external to the Runner
application package.

Required frozen Benchmark Protocol v1.0 assets currently include:

```text
llama-bench.exe
Qwen3-4B-Q4_K_M.gguf
```

These assets are part of the benchmark environment rather than the Runner
application itself.

They should therefore be managed independently from the packaged Runner.

---

# Asset Verification

The Runner must continue to verify frozen benchmark assets before benchmark
execution.

Current Benchmark Protocol v1.0 verification includes:

- expected model SHA-256
- expected `llama-bench.exe` SHA-256

A missing or mismatched required asset must prevent benchmark execution.

The standalone distribution must not weaken these checks.

Unverified substitute assets must not silently enter Benchmark Protocol v1.0.

---

# Proposed Architecture

The current conceptual distribution architecture is:

```text
OpenLLMBench
|
+-- OpenLLMBench-Runner.exe
|
+-- runtime
|   |
|   +-- llama-bench.exe
|
+-- models
|   |
|   +-- Qwen3-4B-Q4_K_M.gguf
|
+-- results
```

The final directory location and installation strategy remain undecided.

---

# Future Asset Bootstrap

A future contributor-facing Runner may automatically prepare missing benchmark
assets.

Conceptually:

```text
Launch Runner
        |
        v
Check Benchmark Model
        |
        +-- Missing --> Acquire Asset --> Verify SHA-256
        |
        v
Check Benchmark Engine
        |
        +-- Missing --> Acquire Asset --> Verify SHA-256
        |
        v
Environment Ready
        |
        v
Run Benchmark
```

Asset acquisition must fail safely if:

- the download fails;
- the asset is incomplete;
- SHA-256 verification fails;
- the expected protocol asset is unavailable.

A successfully downloaded asset must still pass canonical SHA-256 verification
before benchmark execution begins.

---

# External Requirements

Some requirements remain outside the OpenLLMBench distribution.

Current expected platform requirements include:

- supported Windows environment;
- compatible NVIDIA GPU;
- functioning NVIDIA driver;
- sufficient storage for benchmark assets and results.

Python and Git should not be contributor requirements for the standalone
Runner.

---

# Public Distribution Direction

The development Runner currently uses:

```text
C:\AI-Benchmark
```

as its benchmark root.

`C:\AI-Benchmark` remains the benchmark root for the current development
Runner, but it is not the target location for the public standalone Runner.

The public Runner should manage its own application data and benchmark assets
without requiring the contributor to manually reproduce a development-style
directory structure.

A likely Windows location is:

```text
%LOCALAPPDATA%\OpenLLMBench\
    runtime\
    models\
    results\
```

This location is a design candidate rather than a finalized public contract.

The final directory layout should be validated during standalone packaging and
clean-machine testing.

---

# Trust Boundary

The standalone Runner is responsible for:

- environment verification;
- benchmark asset verification;
- hardware evidence capture;
- benchmark execution;
- result parsing;
- manifest generation;
- canonical submission validation;
- submission packaging.

The standalone Runner is not responsible for:

- assigning trusted contributor provenance;
- assigning maintainer verification;
- modifying the canonical benchmark database;
- publishing canonical website data.

Those operations remain maintainer-controlled.

---

# Current Architecture Decisions

## Decision 1 - Package the Application Layer

The OpenLLMBench Runner, validator, required internal modules, and required
Python runtime should be packaged into the standalone application.

The contributor should not need a separate Python installation.

## Decision 2 - Keep Benchmark Assets External

The benchmark model and `llama-bench.exe` should remain independently managed
frozen assets rather than being embedded directly into the Runner executable.

Both assets remain subject to canonical SHA-256 verification before benchmark
execution.

## Decision 3 - Retire the Development Path as a Public Requirement

`C:\AI-Benchmark` should remain supported by the current development Runner,
but it should not become a requirement of the public standalone distribution.

The public Runner should manage its own working environment.

## Decision 4 - Portable-First Application

The first public OpenLLMBench Runner should use a portable-first
distribution model rather than requiring a traditional Windows installer.

The Runner executable may be downloaded and launched directly, while
persistent benchmark assets and results are managed separately under a
stable application-data location such as:

```text
%LOCALAPPDATA%\OpenLLMBench\
    runtime\
    models\
    results\
```

This allows the Runner executable to be replaced or updated without
requiring benchmark assets to be downloaded again.

A traditional Windows installer may be evaluated later if it provides
meaningful usability benefits after the standalone Runner workflow is proven.

## Decision 5 - Verified Asset Bootstrap

The public Runner should automatically acquire missing frozen benchmark
assets rather than requiring contributors to prepare them manually.

Assets must be downloaded into a temporary location and must pass the
canonical SHA-256 check before being promoted into the managed
OpenLLMBench asset cache.

A failed, incomplete, or mismatched download must not replace an existing
verified asset and must prevent benchmark execution.

Verified assets should persist across Runner updates so contributors do not
need to repeatedly download large protocol assets.

## Decision 6 - Split Canonical Asset Sources

The public Runner should use different canonical distribution sources for
the benchmark model and benchmark engine.

The frozen benchmark model should be acquired from a version-pinned
Hugging Face repository or equivalent large-model distribution source.

The frozen llama.cpp Windows benchmark package should be acquired from the
official llama.cpp GitHub Release associated with the protocol build.

Both downloads must still pass OpenLLMBench's canonical SHA-256 verification
before they are promoted into the managed asset cache.

The remote hosting platform is a distribution mechanism only.

OpenLLMBench remains the authority for the expected asset identity and hash.

## Decision 7 - Protocol-Aware Asset Cache

The public Runner should store frozen benchmark assets under a
protocol-specific cache rather than one shared unversioned directory.

A likely layout is:

```text
%LOCALAPPDATA%\OpenLLMBench\
    protocols\
        v1.0\
            runtime\
                llama-bench.exe
            models\
                Qwen3-4B-Q4_K_M.gguf
    results\
```

This keeps Benchmark Protocol v1.0 assets isolated from future protocol
revisions.

A later Benchmark Protocol v1.1 or v2.0 may use different benchmark assets
without overwriting or invalidating the preserved v1.0 environment.

Each protocol-specific asset remains subject to its own canonical SHA-256
verification before benchmark execution.

---

# Open Decisions

Weekend 16 must still resolve:

1. Standalone executable packaging technology.
2. Exact Hugging Face repository/revision for the frozen benchmark model.
3. Exact llama.cpp GitHub release/tag and Windows package for Protocol v1.0.
4. Resume/retry behavior for interrupted downloads.
5. Clean-Windows bootstrap behavior.
6. Console versus lightweight GUI presentation.
7. How contributors locate completed submission packages.
8. How application updates are distributed.
9. Whether a traditional installer should be added after the portable beta.

---

# Out of Scope for Sprint 1

Sprint 1 defines the distribution architecture.

It does not need to implement:

- executable packaging;
- automatic asset downloads;
- Runner self-updates;
- GUI development;
- automatic GitHub submission;
- automatic canonical database ingestion.

Those capabilities should be evaluated or implemented in later sprints after
the distribution architecture is established.

---

# Current Direction

The current Weekend 16 architecture direction is:

> Package the OpenLLMBench Runner, validator, required internal modules, and
> Python runtime into a standalone application while keeping the benchmark
> engine and benchmark model as independently managed frozen assets.

The public Runner should eventually manage its own benchmark environment and
remove the contributor requirement for Python, Git, repository knowledge, and
manual `C:\AI-Benchmark` setup.

Benchmark reproducibility, frozen asset verification, raw evidence
preservation, canonical validation, and maintainer-controlled ingestion remain
non-negotiable architectural requirements.

---

# Status

**Weekend 16 - Sprint 1: Distribution Architecture**

**Status:** In Progress

## Managed Runtime Validation

Weekend 16 Sprint 3 validated the standalone Runner against the
managed OpenLLMBench application directory.

The Runner no longer requires the development-only
`C:\AI-Benchmark` directory for normal benchmark execution.

The validated Windows application layout is:

```text
%LOCALAPPDATA%\OpenLLMBench\
├── protocols\
│   └── v1.0\
│       ├── models\
│       │   └── Qwen3-4B-Q4_K_M.gguf
│       └── runtime\
│           ├── llama-bench.exe
│           └── required runtime DLLs
└── results\