# OpenLLMWorks - Project Status

## Weekend 16 - Product / Name Gate Complete

**Focus:** Public identity, Runner rebrand, backward compatibility, and pre-release validation  
**Status:** Stable / Clean Checkpoint

---

## Current Objective

Move OpenLLMWorks from a proven developer-operated benchmark workflow toward
a low-friction public-beta contributor experience without weakening benchmark
reproducibility, asset verification, raw-evidence preservation, or
maintainer-controlled ingestion.

Weekend 16 established the standalone Windows NVIDIA Runner, validated clean
provisioning and recovery behavior, hardened contributor UX, and completed the
pre-public-beta product/name gate.

The public project is now **OpenLLMWorks**.

The existing frozen benchmark methodology and canonical dataset retain their
technical heritage as the **Open LLM Benchmark Database (OLBD)** and
**Protocol v1.0**. Historical provenance is not being rewritten merely to
match the new public brand.

The next engineering focus is release and distribution.

---

## Public Product Identity

Current public architecture:

```text
OpenLLMWorks
    |
    +-- OpenLLMWorks Runner
    |
    +-- Open LLM Benchmark Database
    |       |
    |       +-- Protocol v1.0
    |
    +-- Hardware Results / Leaderboards
    |
    +-- The Works
    |       |
    |       +-- Future research / editorial
    |
    +-- Community
```

Brand roles:

- **OpenLLMWorks** - public project and ecosystem
- **OpenLLMWorks Runner** - contributor benchmark application
- **Open LLM Benchmark Database** - canonical technical benchmark dataset
- **OLBD Protocol v1.0** - frozen benchmark methodology and provenance
- **The Works** - reserved future research/editorial identity

The public brand should not normally be shortened to "LLM Works" because that
name is already used by unrelated projects and companies.

Current positioning:

```text
Real hardware. Reproducible local AI benchmarks.
```

Primary domain:

```text
OpenLLMWorks.com
```

The domain was secured for a two-year registration period during Weekend 16.

GitHub repository:

```text
https://github.com/namphan813/OpenLLMWorks
```

The repository was renamed from `OpenLLMBench` and the local Git remote was
updated and verified.

---

## Product / Name Gate Decision

The pre-public-beta naming and competitive-landscape gate is complete.

The review found that the former `OpenLLMBench` identity carried avoidable
name-confusion risk with other benchmark projects.

Adjacent local-LLM benchmarking projects also reinforced the need for a public
identity that could differentiate the project while leaving room for future
research, editorial, tooling, and community work beyond a single benchmark.

Decision:

```text
Former public brand: OpenLLMBench
New public brand:    OpenLLMWorks
Technical dataset:   Open LLM Benchmark Database
Protocol:            OLBD Protocol v1.0
```

The rebrand intentionally preserves frozen technical history rather than
performing a blind global replacement of every historical OpenLLMBench or OLBD
reference.

Historical database provenance, frozen protocol identity, backups, and legacy
compatibility paths remain intact where changing them would reduce traceability
or backward compatibility.

---

## Current Runner

**Runner:** OpenLLMWorks Runner  
**Version:** `0.3.0-dev3`  
**Current platform:** Windows  
**Current accelerator:** NVIDIA  
**Benchmark Protocol:** OLBD Protocol v1.0

The Runner performs the contributor-side benchmark workflow:

```text
Start OpenLLMWorks Runner
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

The Runner remains intentionally isolated from the canonical Open LLM
Benchmark Database.

---

## Standalone Windows Runner

OpenLLMWorks has a standalone Windows executable build path using PyInstaller.

Build script:

```text
runner/build_runner.ps1
```

Current build output:

```text
%TEMP%\OpenLLMWorks-runner-build\
    dist\
        OpenLLMWorks-Runner.exe
```

The standalone executable bundles:

- Python runtime
- OpenLLMWorks Runner code
- parser/validation dependencies
- `runner/assets.json`

Large Benchmark Protocol assets are intentionally not embedded in the
executable.

The Runner acquires and verifies those assets separately.

This keeps the Runner executable independent from the multi-gigabyte benchmark
asset payload while preserving a frozen and verifiable protocol environment.

Weekend 16 confirmed that the standalone executable can be copied by itself to
a contributor-style location and complete the benchmark workflow without
requiring the development repository.

---

## Managed Protocol Storage and Rebrand Compatibility

The rebrand deliberately separates **legacy verified assets** from **new
OpenLLMWorks output**.

New installations use:

```text
%LOCALAPPDATA%\OpenLLMWorks\
```

Existing installations that already contain verified managed assets under:

```text
%LOCALAPPDATA%\OpenLLMBench\
```

may reuse those assets in place.

Managed-root resolution is intentionally backward compatible:

```text
If %LOCALAPPDATA%\OpenLLMWorks exists:
    use OpenLLMWorks managed assets

Else if %LOCALAPPDATA%\OpenLLMBench exists:
    reuse legacy OpenLLMBench managed assets in place

Else:
    create/use OpenLLMWorks
```

New benchmark results always belong to the current product identity:

```text
%LOCALAPPDATA%\OpenLLMWorks\results\
```

This avoids:

- forcing existing contributors to redownload the frozen model
- duplicating multi-gigabyte verified assets
- destructively moving a known-good managed environment
- continuing to place newly generated benchmark results under the retired brand

A previously provisioned machine may therefore legitimately contain:

```text
%LOCALAPPDATA%\OpenLLMBench\
    artifacts\
    protocols\
        v1.0\
            models\
            runtime\

%LOCALAPPDATA%\OpenLLMWorks\
    results\
```

The legacy directory is compatibility infrastructure, not the current public
product identity.

---

## Rebrand Regression - Bench-001

The new standalone `OpenLLMWorks-Runner.exe` was tested on Bench-001 against an
existing legacy OpenLLMBench managed environment.

Precondition:

```text
Test-Path %LOCALAPPDATA%\OpenLLMBench   True
Test-Path %LOCALAPPDATA%\OpenLLMWorks   False
```

The OpenLLMWorks Runner successfully reused the existing verified protocol
assets without forcing the multi-gigabyte model to be downloaded again.

During the first compatibility pass, new results were observed still being
written beneath the legacy managed root. This behavior matched the initial
implementation but was not desirable as a long-term brand boundary.

`RESULTS_ROOT` was therefore decoupled from the compatibility-managed asset
root.

The final behavior was validated as:

```text
Legacy verified assets:
%LOCALAPPDATA%\OpenLLMBench

New benchmark results:
%LOCALAPPDATA%\OpenLLMWorks\results
```

Final path state:

```text
Test-Path %LOCALAPPDATA%\OpenLLMBench   True
Test-Path %LOCALAPPDATA%\OpenLLMWorks   True
```

This is the expected PASS state for an upgraded legacy installation.

The regression confirmed:

```text
OpenLLMWorks Runner branding             PASS
Standalone EXE build                     PASS
Legacy managed-asset reuse               PASS
No forced model redownload               PASS
No destructive legacy migration          PASS
No duplicate model required              PASS
New OpenLLMWorks results path             PASS
Three benchmark runs                     PASS
Canonical validation                     PASS
Upload-ready ZIP creation                PASS
Bench-001 upgrade path                   PASS
```

---

## Asset Manifest

Runner asset acquisition is controlled by:

```text
runner/assets.json
```

**Manifest schema:** `1.1`

The manifest defines the frozen assets required by Protocol v1.0.

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

### Runtime

Schema 1.1 defines frozen upstream runtime sources and the required files that
make up the canonical Windows NVIDIA runtime.

The Runner:

1. acquires each frozen upstream source
2. verifies source size and SHA-256
3. extracts verified sources into staging
4. selects the required runtime files
5. assembles the managed runtime
6. validates the resulting runtime
7. atomically installs it into the managed protocol directory

Verified local upstream artifacts may be reused rather than downloaded again.

During Sprint 4 validation, the managed runtime contained:

```text
37 files
1,589.87 MiB
```

The earlier custom runtime archive architecture has been retired.

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
- contributor-visible artifact status
- 10 percent download-progress milestones
- verified local artifact reuse
- upstream runtime-source acquisition
- staging and extraction
- required-file validation
- deterministic runtime assembly
- safe replacement of managed runtime assets
- cleanup of temporary staging data

The existing integrity architecture remains unchanged:

- downloads use temporary `.part` files
- exact size and SHA-256 verification occurs before promotion
- invalid downloads are rejected
- failed partial downloads are cleaned up
- existing verified artifacts may be reused
- managed assets are independently verified before benchmark execution

---

## Sprint 5 - Standalone and Recovery Validation

Sprint 5 exercised the standalone Windows NVIDIA Runner on Bench-001 using an
NVIDIA GeForce GTX 1050 2 GB.

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

This demonstrated clean bootstrap, persistent verified-asset reuse, corruption
recovery, fail-closed offline behavior, safe cancellation, and automatic
recovery after connectivity restoration.

No fundamental benchmark, validation, provisioning, or managed-asset
architecture failure was discovered.

---

## Sprint 6 - Contributor UX and Failure Recovery

Sprint 6 addressed the contributor-experience findings identified during
Sprint 5 without changing Protocol v1.0 or weakening asset, submission, or
validation guarantees.

### Sprint 6A - Completion, Failure, and Cancellation UX

Standalone validation confirmed:

```text
6A-1  Successful completion             PASS
6A-2  Ctrl+C cancellation               PASS
6A-3  Provisioning failure visibility   PASS
```

Packaged execution now:

- keeps successful completion visible
- leaves workspace and ZIP paths visible
- handles `Ctrl+C` deliberately
- reports retained partial workspaces
- explains that rerunning is safe
- keeps handled failures visible before the console closes

Source/developer Python execution remains non-interactive.

### Sprint 6B - Provisioning Visibility

Validation confirmed:

```text
Existing cached artifact detection       PASS
Local artifact status visibility         PASS
Missing artifact visibility              PASS
Network download visibility              PASS
10% download progress milestones         PASS
Download completion                      PASS
Downloaded artifact verification         PASS
Managed model provisioning               PASS
Full Runner workflow regression          PASS
```

Resolved Sprint 5 UX findings:

```text
UX-001  Completion and output discoverability       RESOLVED
UX-002  Provisioning and download progress          RESOLVED
UX-003  Graceful user cancellation                  RESOLVED
UX-004  Provisioning / failure visibility           RESOLVED
```

---

## Current Contributor Handoff

The proven contribution lifecycle is:

```text
Contributor System
    |
    v
OpenLLMWorks-Runner.exe
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
Open LLM Benchmark Database
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

The standalone, managed-asset, recovery, UX, and rebrand work does not change
the core Protocol v1.0 guarantees.

OpenLLMWorks continues to preserve:

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

The rebrand also preserves historical technical provenance instead of
rewriting old canonical records for cosmetic consistency.

---

## Proven Historical Milestones

### Weekend 14

The first complete Runner-to-database lifecycle was demonstrated using
Bench-001 and an NVIDIA GeForce GTX 1050 2 GB.

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
- retirement of the custom runtime archive
- packaged asset manifest
- end-to-end benchmark validation
- packaging and repository hardening

### Weekend 16 - Sprint 5

The standalone Runner and managed-asset architecture were exercised through
clean-state, corruption, recovery, interruption, offline, and restored-network
scenarios.

### Weekend 16 - Sprint 6

The contributor-facing lifecycle was hardened around completion, failure,
cancellation, artifact visibility, and download progress.

### Weekend 16 - Product / Name Gate

The planned pre-public-beta product gate was pulled forward before release and
distribution so the project would not create public release artifacts under a
name already scheduled for reconsideration.

Major work included:

- competitive and naming review
- selection of **OpenLLMWorks** as the public project identity
- preservation of **Open LLM Benchmark Database / OLBD Protocol v1.0** as the
  technical dataset and frozen methodology identity
- GitHub repository rename to `OpenLLMWorks`
- local Git remote update and verification
- acquisition of `OpenLLMWorks.com`
- project-layer rebrand
- standalone Runner rebrand
- PyInstaller build identity change to `OpenLLMWorks-Runner.exe`
- backward-compatible managed-asset root resolution
- separation of new OpenLLMWorks results from legacy asset storage
- Bench-001 legacy-upgrade regression
- final clean working-tree checkpoint

This work changed relatively little benchmark logic but established the
long-term public identity and compatibility boundaries required before public
distribution.

---

## Current Constraints

The contributor-ready path remains intentionally narrow.

Current primary target:

```text
Windows + NVIDIA
```

Remaining public-beta work includes:

- public distribution location for the standalone Runner
- beta artifact naming/version convention
- Windows trust / SmartScreen expectations
- contributor-facing installation and first-run documentation
- additional GPU regression coverage
- additional external-machine testing
- website/source regeneration after the rebrand
- final residual old-name audit
- public-beta release/version strategy
- website integration and launch readiness
- eventual support for additional accelerator vendors and platforms

These are primarily distribution, documentation, external validation, and
release-readiness concerns rather than fundamental benchmark-pipeline blockers.

---

## Public-Beta Roadmap

Current planned sequence:

```text
Weekend 16
    Sprint 4 - Managed Assets                         COMPLETE
    Sprint 5 - Pristine / Recovery Validation        COMPLETE
    Sprint 6 - Contributor UX & Failure Recovery     COMPLETE
    Product / Name Gate                              COMPLETE
        - Competitive landscape review
        - Naming / brand review
        - OpenLLMWorks decision
        - GitHub / Runner rebrand
        - Domain secured
        - Compatibility regression
    Sprint 7 - Release / Distribution                NEXT
    Sprint 8 - Public Contributor Documentation
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
    OpenLLMWorks Public Beta
```

This sequence is a planning framework rather than a frozen protocol
commitment.

Sprint boundaries may be adjusted as contributor testing reveals new
requirements.

---

## Repository State

The public project-layer rename and Runner identity changes were completed in
clean checkpoints.

Relevant rebrand commits include:

```text
Rebrand project layer to OpenLLMWorks
Rebrand Runner product as OpenLLMWorks
Add legacy managed asset compatibility
Write new Runner results under OpenLLMWorks
```

The standalone executable was rebuilt as:

```text
OpenLLMWorks-Runner.exe
```

and exercised on Bench-001 through a real legacy-install compatibility path.

The development working tree was confirmed clean after the final results-root
change and regression.

Current checkpoint:

```text
Weekend 16 - Product / Name Gate Complete
OpenLLMWorks Runner regression PASS
Working tree clean
```

Generated publisher/site output and remaining rebrand-sensitive documentation
should be reconciled from their canonical sources rather than blindly edited.

Historical database provenance and frozen Protocol v1.0 identity should remain
intact where intentional.

---

## Next

### Weekend 16 - Sprint 7

**Focus:** Release / Distribution

Sprint 7 should convert the proven standalone Windows NVIDIA
`OpenLLMWorks-Runner.exe` into a deliberate beta-distribution artifact and
repeatable release workflow.

Primary targets:

1. define the public distribution location for the standalone Runner
2. define the beta Runner artifact naming/version convention
3. define repeatable release-build and release-verification steps
4. document expected Windows trust / SmartScreen behavior
5. verify the distributed artifact from a contributor-style download location
6. define integrity information contributors can use for the distributed EXE
7. preserve the clean separation between the Runner artifact and large managed
   Protocol v1.0 assets
8. reconcile rebrand-sensitive distribution documentation
9. regenerate website/publisher outputs from canonical sources where required
10. perform a final residual old-name audit
11. perform release-candidate regression before public contributor
    documentation work

Sprint 7 should not change Protocol v1.0 unless a release-blocking technical
issue is discovered.

After Sprint 7:

```text
Public Contributor Documentation
    |
    v
Beta Candidate
    |
    v
Small External Beta
    |
    v
Feedback / Stabilization
    |
    v
Website Launch Integration
    |
    v
OpenLLMWorks Public Beta
```

The benchmark execution, managed assets, asset recovery, contributor UX,
evidence, validation, submission, maintainer import, publishing, canonical
database, public identity, and legacy compatibility foundations are now in
place.
