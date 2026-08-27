# OpenLLMBench - Project Status

## Weekend 16 - Sprint 4 Complete

**Focus:** Standalone Runner, Managed Assets, and Contributor Bootstrap  
**Status:** Stable / Clean Checkpoint

---

## Current Objective

Move OpenLLMBench from a proven developer-operated benchmark workflow toward
a low-friction contributor experience without weakening benchmark
reproducibility, asset verification, raw-evidence preservation, or
maintainer-controlled ingestion.

The Windows NVIDIA Runner can now be packaged as a standalone executable and
can manage the frozen Benchmark Protocol v1.0 assets required to execute a
benchmark.

---

## Current Runner

**Runner:** OpenLLMBench Runner  
**Version:** `0.3.0-dev3`  
**Current platform:** Windows  
**Current accelerator:** NVIDIA  
**Benchmark Protocol:** v1.0

The Runner performs the contributor-side benchmark workflow:

```text
Start Runner
    |
    v
Detect NVIDIA Environment
    |
    v
Load Embedded Asset Manifest
    |
    v
Inspect Managed Protocol Assets
    |
    +--> Missing / Invalid Model
    |        |
    |        v
    |    Download Frozen Model
    |        |
    |        v
    |    Verify Size + SHA-256
    |
    +--> Missing / Invalid Runtime
             |
             v
         Download Frozen Upstream Sources
             |
             v
         Verify Size + SHA-256
             |
             v
         Assemble Managed Runtime
             |
             v
         Verify Required Runtime Files
    |
    v
Benchmark Readiness
    |
    v
Capture Hardware Evidence
    |
    v
Execute Three Benchmark Runs
    |
    v
Parse pp512 + tg128
    |
    v
Generate submission.json
    |
    v
Canonical Validation
    |
    v
Create Upload-Ready ZIP
```

The Runner remains intentionally isolated from the canonical OpenLLMBench
database.

---

## Standalone Windows Runner

OpenLLMBench now has a standalone Windows executable build path using
PyInstaller.

Build script:

```text
runner/build_runner.ps1
```

Build output:

```text
%TEMP%\OpenLLMBench-runner-build\
    dist\
        OpenLLMBench-Runner.exe
```

The standalone executable bundles:

- Python runtime
- OpenLLMBench Runner code
- OpenLLMBench parser/validation dependencies
- `runner/assets.json`

Large benchmark protocol assets are intentionally not embedded in the
executable.

The Runner acquires and verifies those assets separately.

This keeps the Runner executable independent from the multi-gigabyte benchmark
asset payload while preserving a frozen and verifiable protocol environment.

---

## Managed Protocol Storage

OpenLLMBench now maintains benchmark assets outside the repository under:

```text
%LOCALAPPDATA%\OpenLLMBench\
```

Current managed structure:

```text
%LOCALAPPDATA%\OpenLLMBench\
    artifacts\
    protocols\
        v1.0\
            models\
                Qwen3-4B-Q4_K_M.gguf

            runtime\
                llama-bench.exe
                llama-bench-impl.dll
                llama-common.dll
                llama.dll
                ggml.dll
                ggml-base.dll
                ggml-cuda.dll
                ...
```

Benchmark execution no longer depends on protocol assets being stored inside
the OpenLLMBench repository.

---

## Asset Manifest

Runner asset acquisition is controlled by:

```text
runner/assets.json
```

**Manifest schema:** `1.1`

The manifest defines the frozen assets required by Benchmark Protocol v1.0.

### Model

Current model:

```text
Qwen3-4B-Q4_K_M.gguf
```

Recorded model properties include:

- source URL
- filename
- size
- install path
- SHA-256

Current frozen model size:

```text
2,497,280,256 bytes
```

The Runner verifies the downloaded model before it is accepted into the
managed protocol environment.

### Runtime

The runtime is no longer distributed as a custom OpenLLMBench-hosted archive.

Instead, schema 1.1 defines frozen upstream runtime sources and the required
files that make up the canonical Windows NVIDIA runtime.

The Runner:

1. downloads each frozen upstream source
2. verifies source size and SHA-256
3. extracts the verified sources into staging
4. selects the required runtime files
5. assembles the managed runtime
6. validates the resulting runtime
7. atomically installs it into the managed protocol directory

This makes the runtime reproducible from verified upstream artifacts rather
than requiring OpenLLMBench to redistribute a large custom binary bundle.

---

## Windows NVIDIA Runtime

The canonical runtime is assembled from frozen upstream llama.cpp Windows CUDA
artifacts.

The assembled runtime contains the files required by the frozen benchmark
engine and its dependencies.

During Sprint 4 validation, the managed runtime contained:

```text
37 files
1,589.87 MiB
```

A comparison against freshly downloaded upstream archives confirmed that the
required runtime files matched their upstream counterparts.

The earlier custom runtime contained redundant CUDA 13 libraries in addition
to the CUDA 12 runtime.

Those CUDA 13 files are no longer part of the canonical assembled runtime.

---

## Retired Runtime Architecture

The earlier prototype runtime architecture used:

```text
openllmbench-runtime-windows-nvidia-v1.0.zip
```

That custom archive was approximately:

```text
994.7 MiB compressed
```

This architecture has been retired.

The following legacy manifest fields have been removed:

```text
archive_filename
archive_size_bytes
archive_sha256
```

The retired compatibility provisioning path:

```text
provision_runtime_from_archive()
```

has also been removed.

Repository searches confirmed that active references to the retired
single-archive runtime architecture are gone.

---

## Asset Provisioning

Asset-management logic is implemented in:

```text
runner/provisioning.py
```

Current responsibilities include:

- managed protocol path resolution
- asset manifest loading
- local asset inspection
- size validation
- SHA-256 validation
- verified file download
- upstream runtime-source acquisition
- staging and extraction
- required-file validation
- deterministic runtime assembly
- safe replacement of managed runtime assets
- cleanup of temporary staging data

The Runner wires these provisioning functions into startup and environment
verification.

---

## Contributor Bootstrap

The current Windows NVIDIA contributor flow no longer requires the contributor
to manually place the frozen model or llama.cpp runtime into the repository.

The intended flow is now:

```text
Contributor
    |
    v
OpenLLMBench-Runner.exe
    |
    v
Inspect Managed Protocol v1.0 Assets
    |
    +--> Assets Valid
    |        |
    |        v
    |    Continue
    |
    +--> Assets Missing / Invalid
             |
             v
         Acquire Frozen Assets
             |
             v
         Verify Assets
             |
             v
         Install Managed Protocol Assets
    |
    v
Run Benchmark
```

This substantially reduces the setup burden compared with the earlier
development Runner workflow.

---

## Standalone Packaging Validation

The standalone executable has been rebuilt with the asset manifest embedded
through PyInstaller.

The build process now:

- verifies `runner/run_benchmark.py` exists
- verifies `runner/assets.json` exists
- bundles `runner/assets.json` into the executable
- produces a one-file Windows console Runner

The standalone executable successfully launches and reaches the managed asset
verification and benchmark workflow.

A previous PATH-isolation test also confirmed that the standalone executable
can launch and perform environment verification without system Python being
available through `PATH`.

A pristine Windows machine remains an important pre-public-beta distribution
regression test.

---

## Sprint 4 Runtime Validation

The new managed-asset architecture was exercised using an NVIDIA Quadro T1000.

The Runner successfully:

- detected the NVIDIA environment
- loaded the asset manifest
- verified the managed model
- verified the managed runtime
- executed Benchmark Protocol v1.0
- completed all three benchmark runs
- parsed benchmark results
- generated `submission.json`
- passed canonical submission validation
- created the upload-ready submission ZIP

Observed performance during Sprint 4 testing included approximately:

```text
pp512 average: 130.38 t/s
tg128 average: 38.92 t/s
tg128 max:     41.32 t/s
```

An earlier run during the same runtime work produced:

```text
tg128 average: 40.40 t/s
tg128 max:     42.46 t/s
```

These measurements were observed during development validation and are not
being treated as new canonical leaderboard results unless submitted through
the normal OpenLLMBench submission workflow.

---

## Current Contributor Handoff

The proven contribution lifecycle is now:

```text
Contributor System
    |
    v
OpenLLMBench-Runner.exe
    |
    v
Managed Asset Verification / Provisioning
    |
    v
Environment Verification
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

Contributor execution and maintainer ingestion remain deliberately separated.

---

## Preserved Benchmark Guarantees

The standalone and managed-asset work does not change the core Benchmark
Protocol v1.0 guarantees.

OpenLLMBench continues to preserve:

- frozen benchmark protocol
- frozen benchmark model
- frozen benchmark engine/runtime
- SHA-256 asset verification
- three required benchmark runs
- raw benchmark evidence
- required hardware evidence
- canonical submission validation
- deterministic result identity
- maintainer-controlled provenance
- maintainer-controlled database ingestion
- separation between contributor systems and the canonical database

---

## Proven Historical Milestones

### Weekend 14

The first complete Runner-to-database lifecycle was demonstrated using
Bench-001 and an NVIDIA GeForce GTX 1050 2 GB.

That test proved:

```text
Runner
    -> Submission ZIP
    -> GitHub Issue
    -> Maintainer Validation
    -> Canonical Import
    -> Publisher
    -> Website
```

### Weekend 15

The Runner was hardened for contributor use.

Major work included:

- canonical submission-name hardening
- benchmark-readiness guidance
- improved failure reporting
- single-submission maintainer workflow
- contributor documentation
- GitHub Issue submission workflow
- Runner-first README guidance
- regression testing
- standalone executable groundwork

### Weekend 16 - Sprint 4

The Runner moved from standalone packaging groundwork to managed,
self-provisioning benchmark assets.

Major work included:

- standalone PyInstaller build
- managed protocol storage
- asset manifest schema 1.1
- verified model acquisition
- verified upstream runtime acquisition
- deterministic runtime assembly
- removal of the custom OpenLLMBench runtime archive
- packaged asset manifest
- end-to-end benchmark validation
- packaging and repository hardening

---

## Current Constraints

The current contributor-ready path is still intentionally narrow.

Current primary target:

```text
Windows + NVIDIA
```

Remaining constraints and validation needs include:

- pristine Windows machine testing
- public distribution location for the standalone Runner
- Windows trust / SmartScreen expectations
- contributor-facing installation and first-run documentation
- download failure and interrupted-download UX
- broader network-condition testing
- additional GPU regression testing
- final public-beta release/version strategy
- eventual support for additional accelerator vendors and platforms

These are distribution and contributor-experience concerns rather than
fundamental benchmark-pipeline blockers.

---

## Repository State

Sprint 4 implementation was completed and committed with a clean working tree.

Final Sprint 4 hardening included:

- removal of the retired single-archive runtime compatibility shim
- verification that legacy runtime-manifest references are gone
- verification of schema 1.1 integration
- embedding `runner/assets.json` in the standalone executable
- build-time manifest existence validation
- successful standalone Runner rebuild
- Python compile validation
- Git diff/whitespace validation
- clean-tree checkpoint

---

## Next

The next development phase should focus on turning the technically proven
standalone Runner into a public-beta-ready contributor package.

Priority areas include:

1. pristine Windows testing
2. distribution and release packaging
3. first-run contributor UX
4. download/provisioning failure recovery
5. contributor documentation
6. additional GPU regression coverage
7. public-beta release criteria
8. website integration and launch readiness

The benchmark execution, evidence, validation, submission, maintainer import,
publishing, and managed-asset foundations are now in place.
