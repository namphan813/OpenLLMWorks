# OpenLLMBench - Project Status

## Weekend 16 - Sprint 5 Complete

**Focus:** Standalone Runner Validation, Asset Recovery, and Contributor Failure Testing  
**Status:** Stable / Clean Checkpoint

---

## Current Objective

Move OpenLLMBench from a proven developer-operated benchmark workflow toward
a low-friction public-beta contributor experience without weakening benchmark
reproducibility, asset verification, raw-evidence preservation, or
maintainer-controlled ingestion.

The Windows NVIDIA Runner can now be packaged as a standalone executable,
manage the frozen Benchmark Protocol v1.0 assets required to execute a
benchmark, recover damaged managed assets, and complete the contributor
workflow from standalone execution to an upload-ready submission ZIP.

Sprint 5 validated this workflow from a controlled clean contributor state
outside the OpenLLMBench development environment.

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
    |    Acquire Frozen Model
    |        |
    |        +--> Reuse Verified Local Artifact
    |        |
    |        +--> Download Frozen Model
    |        |
    |        v
    |    Verify Size + SHA-256
    |
    +--> Missing / Invalid Runtime
             |
             v
         Acquire Frozen Upstream Sources
             |
             +--> Reuse Verified Local Artifacts
             |
             +--> Download Frozen Upstream Sources
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

OpenLLMBench has a standalone Windows executable build path using PyInstaller.

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

Sprint 5 confirmed that the standalone executable can be copied by itself to a
controlled contributor test location and complete the benchmark workflow
without requiring the OpenLLMBench repository.

---

## Managed Protocol Storage

OpenLLMBench maintains benchmark assets outside the repository under:

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
    results\
```

Benchmark execution no longer depends on protocol assets being stored inside
the OpenLLMBench repository.

The artifact cache also allows verified downloads to be reused when a managed
protocol asset must be repaired.

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

The Runner verifies the model before it is accepted into the managed protocol
environment.

Sprint 5 confirmed that an invalid managed model is rejected and can be
restored either from a verified local artifact or by reacquiring the frozen
model from its configured source.

### Runtime

The runtime is no longer distributed as a custom OpenLLMBench-hosted archive.

Instead, schema 1.1 defines frozen upstream runtime sources and the required
files that make up the canonical Windows NVIDIA runtime.

The Runner:

1. acquires each frozen upstream source
2. verifies source size and SHA-256
3. extracts verified sources into staging
4. selects the required runtime files
5. assembles the managed runtime
6. validates the resulting runtime
7. atomically installs it into the managed protocol directory

Verified local upstream artifacts may be reused rather than downloaded again.

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

Sprint 5 deliberately corrupted the managed:

```text
llama-bench.exe
```

The Runner successfully:

- detected the critical-file SHA-256 mismatch
- rejected the invalid managed runtime
- reused verified upstream source artifacts
- reconstructed the managed runtime
- verified the repaired benchmark engine
- passed environment verification
- returned to benchmark execution

This validated managed runtime recovery outside the normal happy path.

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
- verified local artifact reuse
- upstream runtime-source acquisition
- staging and extraction
- required-file validation
- deterministic runtime assembly
- safe replacement of managed runtime assets
- cleanup of temporary staging data

The Runner wires these provisioning functions into startup and environment
verification.

Sprint 5 exercised both normal provisioning and recovery paths.

---

## Contributor Bootstrap

The current Windows NVIDIA contributor flow does not require the contributor
to manually place the frozen model or llama.cpp runtime into the repository.

The intended flow is:

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

Sprint 5 validated this bootstrap flow from a controlled clean state with no
existing:

```text
%LOCALAPPDATA%\OpenLLMBench
```

managed environment.

The standalone Runner successfully created the managed environment, acquired
the required assets, verified them, executed Benchmark Protocol v1.0, and
created an upload-ready submission ZIP.

---

## Standalone Packaging Validation

The standalone executable is built with the asset manifest embedded through
PyInstaller.

The build process:

- verifies `runner/run_benchmark.py` exists
- verifies `runner/assets.json` exists
- bundles `runner/assets.json` into the executable
- produces a one-file Windows console Runner

A previous PATH-isolation test confirmed that the standalone executable can
launch and perform environment verification without system Python being
available through `PATH`.

Sprint 5 extended this validation by copying only the standalone executable
into a contributor-style test folder on Bench-001 and launching it normally
through Windows.

No OpenLLMBench repository files were placed beside the executable.

The Runner successfully provisioned its managed protocol environment and
completed the benchmark workflow.

Additional external-machine testing remains valuable before broad public
distribution, but the standalone clean-state contributor path has now been
demonstrated.

---

## Sprint 4 Runtime Validation

The managed-asset architecture was exercised during Sprint 4 using an NVIDIA
Quadro T1000.

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

## Sprint 5 Standalone and Recovery Validation

Sprint 5 exercised the standalone Windows NVIDIA Runner on Bench-001 using an
NVIDIA GeForce GTX 1050 2 GB.

The controlled test began with no existing managed OpenLLMBench environment.

Validation matrix:

```text
5.1   Clean-state first run              PASS
5.2   Existing asset reuse               PASS
5.3A  Corrupt managed model recovery     PASS
5.3B  Forced model re-download           PASS
5.3C  Managed runtime recovery           PASS
5.4A  User-aborted benchmark             PASS
5.4B  Offline provisioning failure       PASS
5.4C  Connectivity-restored recovery     PASS
5.5   Final healthy regression           PASS
```

### Clean-State First Run

The standalone executable was copied by itself into a contributor-style test
folder and launched normally through Windows.

The Runner successfully:

- created the managed OpenLLMBench environment
- acquired the frozen Benchmark Protocol v1.0 assets
- verified the model and runtime
- captured hardware evidence
- completed all three benchmark runs
- generated `submission.json`
- passed canonical validation
- created an upload-ready ZIP

### Existing Asset Reuse

A second launch confirmed that the Runner:

- detected the existing managed model
- verified the model SHA-256
- detected the existing managed runtime
- verified the runtime and benchmark engine
- skipped unnecessary reprovisioning
- returned directly to benchmark execution

### Managed Model Recovery

The managed model was deliberately corrupted while the verified artifact cache
remained intact.

The Runner:

- detected the SHA-256 mismatch
- rejected the invalid managed model
- reused the verified local artifact
- restored the managed model
- verified the repaired model
- returned to benchmark execution

### Forced Model Re-download

Both the managed model and cached model artifact were deliberately corrupted.

The Runner:

- rejected both invalid copies
- reacquired the frozen model
- verified the downloaded artifact
- installed the managed model
- verified the installed model
- returned to benchmark execution

### Managed Runtime Recovery

The managed `llama-bench.exe` was deliberately corrupted.

The Runner:

- detected the critical-file SHA-256 mismatch
- rejected the invalid managed runtime
- reused verified upstream source artifacts
- reconstructed the managed runtime
- verified the repaired benchmark engine
- passed environment verification
- returned to benchmark execution

### User-Aborted Benchmark

A benchmark was deliberately interrupted with:

```text
Ctrl+C
```

The interrupted workspace retained partial diagnostic/evidence data.

The interrupted run did not produce:

- a canonical `submission.json`
- an upload-ready submission ZIP

The incomplete run therefore could not masquerade as a valid Benchmark
Protocol v1.0 submission.

### Offline Provisioning Failure

The managed model and cached model artifact were invalidated while the test
machine was disconnected from the network.

The Runner could not complete required provisioning and terminated before
benchmark execution.

No valid submission ZIP was observed from the failed provisioning attempt.

This demonstrated fail-closed behavior when required verified assets could not
be obtained.

### Connectivity-Restored Recovery

Network connectivity was restored without manually repairing the invalid model
state.

The Runner:

- reacquired the frozen model
- restored the managed model
- completed all three benchmark runs
- generated the expected submission workspace
- generated the upload-ready ZIP

The completed workspace and ZIP each contained the expected nine submission
files.

This recovery run also served as the final healthy regression for Sprint 5.

No fundamental benchmark, validation, provisioning, or managed-asset
architecture failure was discovered during Sprint 5.

---

## Contributor UX Findings

Sprint 5 identified contributor-experience issues that do not weaken benchmark
integrity but should be addressed before public beta.

### UX-001 - Completion and Output Discoverability

When the standalone Runner is launched by double-clicking the executable, the
console closes immediately after successful completion.

The upload-ready ZIP is correctly written under:

```text
%LOCALAPPDATA%\OpenLLMBench\results
```

but the contributor may not have enough time to read the completion message or
discover the output location.

Desired improvement:

- keep the completion state visible
- clearly identify the generated submission ZIP
- clearly identify its filesystem location
- provide an obvious next step for submission

### UX-002 - Provisioning and Download Progress

Large asset downloads and some provisioning operations currently provide
limited visible progress.

During forced model reacquisition, external network activity confirmed that the
Runner was downloading the model, but the console did not provide enough
progress information for a contributor to distinguish active downloading from
a stalled process.

Desired improvement:

- distinguish local artifact reuse from network acquisition
- show when a large download has started
- provide useful download/provisioning progress
- clearly indicate verification and installation stages

### UX-003 - Graceful User Cancellation

`Ctrl+C` safely prevented an incomplete benchmark from becoming a valid
submission.

Contributor-facing cancellation messaging should still be improved.

Desired improvement:

- report that the benchmark was interrupted by the user
- state that no valid submission was created
- identify any retained partial diagnostic workspace
- tell the contributor that the benchmark can safely be run again

### UX-004 - Provisioning / Network Failure Visibility

When required provisioning was attempted without network connectivity, the
standalone console displayed output briefly and then closed.

The failure remained technically safe, but the contributor would have little
opportunity to understand what happened.

Desired improvement:

- keep fatal error output visible
- clearly identify network/download failure
- provide an actionable recovery message
- tell the contributor that rerunning after connectivity is restored is safe

These findings form the primary input for Weekend 16 Sprint 6.

---

## Current Contributor Handoff

The proven contribution lifecycle is:

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

The standalone, managed-asset, and recovery work does not change the core
Benchmark Protocol v1.0 guarantees.

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

Sprint 5 additionally demonstrated that corrupted or unavailable assets fail
closed rather than weakening these guarantees.

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

### Weekend 16 - Sprint 5

The standalone Runner and managed-asset architecture were exercised through
clean-state, corruption, recovery, interruption, offline, and restored-network
scenarios.

Major validation included:

- standalone clean-state contributor bootstrap
- persistent managed-asset reuse
- corrupt managed-model recovery
- forced model reacquisition
- corrupt runtime reconstruction
- safe user-aborted benchmark behavior
- offline provisioning fail-closed behavior
- automatic recovery after network restoration
- final successful end-to-end regression

Sprint 5 shifted the remaining public-beta concerns primarily toward
contributor UX, distribution, documentation, release readiness, and public
positioning rather than fundamental benchmark architecture.

---

## Current Constraints

The contributor-ready path remains intentionally narrow.

Current primary target:

```text
Windows + NVIDIA
```

Remaining public-beta work includes:

- contributor-facing completion and output UX
- download/provisioning progress visibility
- graceful interruption handling
- actionable network/download failure messaging
- public distribution location for the standalone Runner
- Windows trust / SmartScreen expectations
- contributor-facing installation and first-run documentation
- additional GPU regression coverage
- additional external-machine testing
- final public-beta release/version strategy
- website integration and launch readiness
- competitive landscape and naming/brand review
- eventual support for additional accelerator vendors and platforms

These are now primarily contributor-experience, distribution, positioning, and
release-readiness concerns rather than fundamental benchmark-pipeline blockers.

---

## Pre-Public-Beta Product Gate

Before broader external public-beta distribution, conduct a focused competitive
landscape and naming/brand review.

This work is intentionally parked as a pre-public-beta product gate and should
not interrupt current Runner engineering or contributor-UX work.

Goals:

- document adjacent OpenLLMBench or similarly named projects
- review potential naming and brand-confusion risks
- compare adjacent community local-LLM benchmark platforms
- document OpenLLMBench's differentiated position
- define public-beta messaging around:
  - standardized and frozen benchmark protocols
  - verified benchmark assets
  - standalone contributor Runner
  - validated evidence-backed submissions
  - historical consumer/workstation GPU performance data
  - Open Lab research and analysis
- make an explicit go / adjust / rename decision before broader public launch

The purpose of this review is not to change the technical direction of the
project unless evidence warrants it.

The goal is to ensure that OpenLLMBench enters public beta with a clear name,
clear differentiation, and clear public positioning rather than presenting
itself simply as another LLM benchmark website.

---

## Public-Beta Roadmap

Current planned sequence:

```text
Weekend 16
    Sprint 4 - Managed Assets                         COMPLETE
    Sprint 5 - Pristine / Recovery Validation        COMPLETE
    Sprint 6 - Contributor UX & Failure Recovery     NEXT
    Sprint 7 - Release / Distribution
    Sprint 8 - Public Contributor Documentation
        |
        v
    Pre-Public-Beta Product Gate
        - Competitive landscape review
        - Naming / brand review
        - Differentiation and positioning
        - Go / adjust / rename decision
        |
        v
    Beta Candidate

Weekend 17
    Small External Beta
    Sprint 9  - Beta Feedback / Runner Stabilization
    Sprint 10 - Website Launch Integration
    Sprint 11 - Launch Readiness
        |
        v
    OpenLLMBench Public Beta
```

This sequence is a planning framework rather than a frozen protocol
commitment.

Sprint boundaries may be adjusted as contributor testing reveals new
requirements.

---

## Repository State

Sprint 5 validation was completed with no required repository implementation
changes.

The development working tree was confirmed clean after Sprint 5 testing.

Sprint 5 destructive and recovery testing was performed against the standalone
Runner and its managed environment on Bench-001 rather than by modifying
repository code.

Current checkpoint:

```text
Weekend 16 - Sprint 5 Complete
Working tree clean
```

---

## Next

### Weekend 16 - Sprint 6

**Focus:** Contributor UX and Failure Recovery

Sprint 6 should convert the contributor-experience findings from Sprint 5 into
deliberate Runner behavior.

Primary targets:

1. successful completion UX
2. submission ZIP discoverability
3. download and provisioning progress visibility
4. graceful `Ctrl+C` handling
5. actionable provisioning/network failure messages
6. contributor-friendly pause/exit behavior
7. regression testing of the improved standalone executable

Sprint 6 should preserve the benchmark and provisioning architecture proven
during Sprints 4 and 5.

No Benchmark Protocol v1.0 changes are currently required.

After Sprint 6, the roadmap should continue toward:

1. release and distribution packaging
2. public contributor documentation
3. the pre-public-beta product/naming gate
4. small external beta testing
5. website launch integration
6. public-beta release readiness

The benchmark execution, managed assets, asset recovery, evidence, validation,
submission, maintainer import, publishing, and database foundations are now in
place.
