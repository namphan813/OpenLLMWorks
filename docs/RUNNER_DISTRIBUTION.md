# OpenLLMWorks Runner Distribution

## Purpose

This document defines the distribution architecture for the
contributor-facing **OpenLLMWorks Runner**.

The goal is to allow a contributor to run the benchmark and produce a
validated submission package without requiring knowledge of Python, Git,
repository internals, or command-line development workflows.

The distribution architecture must preserve the reproducibility and trust
requirements of the frozen **Open LLM Benchmark Database (OLBD) Protocol
v1.0**.

---

# Distribution Goals

The contributor experience should approach:

```text
Download OpenLLMWorks Runner
        |
        v
Launch Runner
        |
        v
Verify / Provision Benchmark Environment
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

The Runner must not receive authority to modify the canonical Open LLM
Benchmark Database.

---

# Application Packaging

The standalone Runner packages the Python application layer required for
benchmark execution.

This includes:

- `runner/run_benchmark.py`
- `runner/assets.json`
- `parser.submission`
- `parser.validate`
- required OpenLLMWorks internal modules
- required Python runtime and standard-library components

The contributor does not need to install Python separately.

The current Windows build uses PyInstaller and is produced by:

```text
runner/build_runner.ps1
```

Current standalone artifact:

```text
OpenLLMWorks-Runner.exe
```

The executable contains the application and validation layer but intentionally
does not contain the multi-gigabyte benchmark model or llama.cpp runtime.

---

# Benchmark Assets

Benchmark Protocol assets remain external to the Runner application package.

Current frozen OLBD Protocol v1.0 assets include:

```text
Qwen3-4B-Q4_K_M.gguf
llama.cpp Windows CUDA runtime
    |
    +-- llama-bench.exe
    +-- required runtime DLLs
```

These assets are part of the benchmark environment rather than the Runner
application itself.

They are managed independently from the packaged Runner.

The current asset manifest is:

```text
runner/assets.json
```

The manifest records the frozen source identity, expected size, expected
SHA-256, and installation information required by the Runner.

---

# Asset Verification

The Runner must verify frozen benchmark assets before benchmark execution.

Current OLBD Protocol v1.0 verification includes:

- expected model size and SHA-256
- expected frozen upstream runtime-source size and SHA-256
- required runtime-file presence
- critical `llama-bench.exe` identity verification

A missing or mismatched required asset must prevent benchmark execution until a
verified replacement can be provisioned.

The standalone distribution must not weaken these checks.

Unverified substitute assets must not silently enter Protocol v1.0.

---

# Current Architecture

The validated architecture separates the portable Runner executable from
persistent managed protocol assets and benchmark results.

```text
OpenLLMWorks-Runner.exe
        |
        v
%LOCALAPPDATA%
    |
    +-- OpenLLMWorks
    |       |
    |       +-- protocols\
    |       |       +-- v1.0\
    |       |               +-- models\
    |       |               +-- runtime\
    |       |
    |       +-- artifacts\
    |       |
    |       +-- results\
    |
    +-- OpenLLMBench\            legacy compatibility only
            |
            +-- protocols\
            +-- artifacts\
```

For a new installation, managed assets are stored under:

```text
%LOCALAPPDATA%\OpenLLMWorks\
```

For an existing installation, verified legacy assets may remain under:

```text
%LOCALAPPDATA%\OpenLLMBench\
```

The Runner may reuse those legacy verified assets in place.

New benchmark output always belongs to the current public product identity:

```text
%LOCALAPPDATA%\OpenLLMWorks\results\
```

This compatibility boundary avoids destructive migration, duplicate
multi-gigabyte model storage, and unnecessary redownloads.

---

# Managed Asset Bootstrap

The standalone Runner automatically prepares missing benchmark assets.

Current flow:

```text
Launch Runner
        |
        v
Load Frozen Asset Manifest
        |
        v
Inspect Managed Model
        |
        +-- Valid ------> Reuse
        |
        +-- Missing /
            Invalid
                |
                v
        Reuse Verified Local Artifact
                |
                +-- unavailable --> Download Frozen Model
                |
                v
        Verify Size + SHA-256
        |
        v
Inspect Managed Runtime
        |
        +-- Valid ------> Reuse
        |
        +-- Missing /
            Invalid
                |
                v
        Acquire Frozen Upstream Sources
                |
                +-- Reuse Verified Local Artifacts
                |
                +-- Download Frozen Sources
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
Environment Ready
        |
        v
Run Benchmark
```

Asset acquisition fails safely if:

- the download fails
- the asset is incomplete
- size verification fails
- SHA-256 verification fails
- the expected protocol asset is unavailable
- required runtime files cannot be assembled or verified

Downloads use temporary files and are verified before promotion into the
managed environment.

A failed, incomplete, or mismatched download must not replace an existing
verified asset.

Verified assets persist across Runner executions and Runner updates.

---

# Provisioning Visibility

Long-running provisioning operations must remain visible to contributors.

Current Runner behavior includes:

- local cache inspection messages
- verified-artifact reuse messages
- explicit network-download messages
- 10 percent download-progress milestones
- downloaded-artifact verification messages
- managed-asset provisioning status

These messages are contributor UX only.

They do not change the underlying integrity or verification requirements.

---

# External Requirements

Some requirements remain outside the OpenLLMWorks distribution.

Current expected platform requirements include:

- supported Windows environment
- compatible NVIDIA GPU
- functioning NVIDIA driver
- network access when required frozen assets are not already available locally
- sufficient storage for benchmark assets and results

Python and Git are not contributor requirements for the standalone Runner.

The initial public-beta target remains intentionally narrow:

```text
Windows + NVIDIA
```

Additional operating systems and accelerator vendors may be evaluated after
the initial public workflow is stable.

---

# Public Distribution Direction

The first public OpenLLMWorks Runner uses a **portable-first** distribution
model rather than requiring a traditional Windows installer.

The contributor should be able to:

```text
Download OpenLLMWorks-Runner.exe
        |
        v
Place It in a Convenient Folder
        |
        v
Launch It
```

Persistent protocol assets and results are managed separately under
`%LOCALAPPDATA%`.

The executable can therefore be replaced or updated without forcing verified
Protocol v1.0 assets to be downloaded again.

A traditional Windows installer may be evaluated later if it provides
meaningful usability or trust benefits.

The old development-only `C:\AI-Benchmark` layout is not a public contributor
requirement.

---

# Trust Boundary

The standalone Runner is responsible for:

- environment verification
- benchmark asset verification and provisioning
- hardware evidence capture
- benchmark execution
- result parsing
- `submission.json` generation
- canonical submission validation
- upload-ready ZIP creation

The standalone Runner is not responsible for:

- assigning trusted contributor provenance
- assigning maintainer verification
- modifying the canonical benchmark database
- publishing canonical website data

Those operations remain maintainer-controlled.

The intended lifecycle remains:

```text
Contributor
    |
    v
OpenLLMWorks Runner
    |
    v
Validated Submission ZIP
    |
    v
GitHub Benchmark Submission Issue
    |
    v
Maintainer Validation
    |
    v
Controlled Import
    |
    v
Open LLM Benchmark Database
    |
    v
Publisher
    |
    v
Website
```

---

# Current Architecture Decisions

## Decision 1 - Package the Application Layer

The OpenLLMWorks Runner, validator, required internal modules, asset manifest,
and Python runtime are packaged into the standalone application.

The contributor does not need a separate Python installation.

## Decision 2 - Keep Benchmark Assets External

The benchmark model and llama.cpp Windows CUDA runtime remain independently
managed frozen assets rather than being embedded directly into the Runner
executable.

Protocol assets remain subject to canonical verification before benchmark
execution.

## Decision 3 - Retire Development Paths as Public Requirements

Development-only repository and benchmark paths must not become contributor
requirements.

The public Runner manages its own persistent environment under
`%LOCALAPPDATA%`.

## Decision 4 - Portable-First Application

The first public OpenLLMWorks Runner is distributed as a standalone executable:

```text
OpenLLMWorks-Runner.exe
```

A traditional Windows installer is not required for the initial beta.

## Decision 5 - Verified Asset Bootstrap

The public Runner automatically acquires or reconstructs missing frozen
benchmark assets.

Downloaded artifacts must pass the canonical verification requirements before
being promoted into the managed environment.

Verified assets persist across Runner updates.

## Decision 6 - Split Canonical Asset Sources

The public Runner may use different authoritative distribution sources for
different frozen protocol assets.

The frozen benchmark model may be acquired from its pinned model distribution
source.

Frozen llama.cpp Windows runtime sources are acquired from the upstream
llama.cpp release assets defined by the protocol asset manifest.

Remote hosting platforms are distribution mechanisms only.

**OLBD Protocol v1.0 and the OpenLLMWorks asset manifest remain authoritative
for the expected asset identity, version, size, and hash.**

## Decision 7 - Protocol-Aware Managed Storage

Frozen benchmark assets are stored beneath a protocol-specific directory.

New-install layout:

```text
%LOCALAPPDATA%\OpenLLMWorks\
    protocols\
        v1.0\
            runtime\
                llama-bench.exe
                required runtime DLLs
            models\
                Qwen3-4B-Q4_K_M.gguf
    artifacts\
    results\
```

This keeps Protocol v1.0 assets isolated from future protocol revisions.

A future Protocol v1.1 or v2.0 may use different assets without overwriting or
invalidating the preserved v1.0 environment.

## Decision 8 - Preserve Legacy Managed Assets

Existing verified assets beneath:

```text
%LOCALAPPDATA%\OpenLLMBench\
```

may be reused in place for backward compatibility.

The Runner does not need to copy or move a multi-gigabyte verified environment
solely to change the directory name.

Managed-root resolution follows this compatibility model:

```text
If %LOCALAPPDATA%\OpenLLMWorks exists:
    use OpenLLMWorks managed assets

Else if %LOCALAPPDATA%\OpenLLMBench exists:
    reuse legacy managed assets in place

Else:
    create/use OpenLLMWorks
```

This is a compatibility mechanism, not a continuation of the retired public
brand.

## Decision 9 - New Results Belong to OpenLLMWorks

Benchmark results generated by the current Runner are written beneath:

```text
%LOCALAPPDATA%\OpenLLMWorks\results\
```

even when frozen protocol assets are being reused from the legacy
`%LOCALAPPDATA%\OpenLLMBench` environment.

This establishes a clean product boundary while retaining backward-compatible
asset reuse.

## Decision 10 - Preserve the Canonical Database Trust Boundary

The OpenLLMWorks public brand does not change the authority model of the
canonical dataset.

Contributor-side execution ends with a validated submission package.

Maintainer-side validation, provenance, import, and publication remain
separate controlled operations.

---

# Validated Recovery Behavior

Weekend 16 validation established the following standalone behavior:

```text
Clean-state first run              PASS
Existing asset reuse               PASS
Corrupt managed model recovery     PASS
Forced model re-download           PASS
Corrupt managed runtime recovery   PASS
User-aborted benchmark             PASS
Offline provisioning failure       PASS
Connectivity-restored recovery     PASS
Final healthy regression           PASS
```

The rebranded OpenLLMWorks Runner was also validated on Bench-001 against an
existing legacy managed environment.

That regression confirmed:

```text
OpenLLMWorks branding              PASS
Standalone EXE build               PASS
Legacy verified-asset reuse        PASS
No forced model redownload         PASS
No destructive asset migration     PASS
New OpenLLMWorks results path      PASS
Three benchmark runs               PASS
Canonical validation               PASS
Upload-ready ZIP creation          PASS
```

---

# Contributor Completion and Failure UX

Packaged execution currently:

- keeps successful completion visible
- displays workspace and ZIP locations
- handles `Ctrl+C` deliberately
- reports retained partial workspaces
- explains that rerunning is safe
- keeps handled provisioning failures visible before exit

Source/developer Python execution remains non-interactive.

These behaviors are part of the standalone contributor experience and should
be preserved by future release packaging.

---

# Resolved Decisions

The original Weekend 16 distribution design left several questions open.
Current status:

```text
Standalone executable technology          RESOLVED - PyInstaller
Frozen model acquisition                  RESOLVED - manifest-controlled
Frozen llama.cpp acquisition              RESOLVED - manifest-controlled upstream assets
Interrupted / failed provisioning         RESOLVED - fail closed; rerun safely
Clean-Windows bootstrap                    VALIDATED
Console presentation                       RESOLVED FOR BETA - console
Completed submission discoverability      RESOLVED
Portable vs installer                      RESOLVED FOR BETA - portable
Managed application-data location         RESOLVED
Legacy asset compatibility                 RESOLVED
New results location                       RESOLVED
```

Application self-update behavior remains intentionally deferred.

---

# Remaining Release / Distribution Decisions

The remaining work belongs primarily to **Weekend 16 Sprint 7 - Release /
Distribution** rather than to core Runner architecture.

Sprint 7 should resolve:

1. Public download/release location for `OpenLLMWorks-Runner.exe`.
2. Beta artifact naming and version convention.
3. Repeatable release-build procedure.
4. Release-artifact verification procedure.
5. Contributor-visible SHA-256 or equivalent integrity information for the
   distributed executable.
6. Windows SmartScreen / unsigned-executable expectations and documentation.
7. Contributor-style download-and-run regression.
8. Release notes and version metadata.
9. Rebrand-sensitive generated publisher/site output.
10. Final residual old-name audit.

A traditional installer and automatic application updates remain optional
future enhancements rather than public-beta blockers.

---

# Out of Scope

The current release/distribution architecture does not require:

- automatic canonical database ingestion
- automatic maintainer verification
- automatic GitHub submission
- a graphical Runner UI
- a traditional Windows installer
- automatic Runner self-update
- support for every operating system
- support for every accelerator vendor

These may be evaluated after the portable Windows NVIDIA beta path is proven
with external contributors.

---

# Current Direction

The current architecture is:

> Package the OpenLLMWorks Runner, validator, required internal modules, asset
> manifest, and Python runtime into a standalone portable application while
> keeping the benchmark model and llama.cpp runtime as independently managed,
> cryptographically verified frozen Protocol v1.0 assets.

The public Runner manages its own benchmark environment and removes the
contributor requirement for Python, Git, repository knowledge, and manual
development-path setup.

Existing verified legacy assets may be reused without migration, while new
benchmark results are written beneath the OpenLLMWorks product identity.

Benchmark reproducibility, frozen asset verification, raw evidence
preservation, canonical validation, and maintainer-controlled ingestion remain
non-negotiable architectural requirements.

---

# Status

**Weekend 16 - Distribution Architecture / Rebrand Reconciliation**

**Status:** Architecture Validated / Sprint 7 Release Work Next

The standalone Runner architecture has been proven through clean provisioning,
asset reuse, corruption recovery, interruption, offline failure, restored
connectivity, contributor UX validation, and the OpenLLMWorks legacy-upgrade
regression.

Current release artifact:

```text
OpenLLMWorks-Runner.exe
```

Current public project:

```text
OpenLLMWorks
```

Canonical technical dataset and frozen methodology:

```text
Open LLM Benchmark Database
OLBD Protocol v1.0
```

The next step is to turn the proven standalone artifact into a deliberate,
repeatable public-beta distribution workflow.
