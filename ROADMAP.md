# OpenLLMWorks Roadmap

The roadmap describes the long-term evolution of OpenLLMWorks.

Each phase builds upon the previous one while remaining aligned with the
project's mission:

> **Measure. Understand. Preserve.**

OpenLLMWorks is intentionally built in phases.

Each phase establishes a stable foundation before introducing the next
major capability.

The goal is steady, sustainable progress rather than rapid feature
accumulation.

------------------------------------------------------------------------

# Project Evolution

```text
Foundation
    ↓
Intelligence
    ↓
Evolution
    ↓
Identity
    ↓
Community
    ↓
Recommendations
    ↓
Platform
    ↓
Research Platform
```

------------------------------------------------------------------------

# ✅ Foundation

**Status:** Complete

Established the technical foundation of OpenLLMWorks.

### Highlights

- Benchmark parser
- Persistent benchmark database
- Deterministic result IDs
- Duplicate detection
- Core statistics engine

### Outcome

OpenLLMWorks became capable of reliably collecting and storing benchmark
data.

------------------------------------------------------------------------

# ✅ Intelligence

**Status:** Complete

Transformed benchmark records into reusable insights.

### Highlights

- Statistics
- Leaderboards
- Hardware Profiles
- Interesting Facts
- Snapshot Viewer
- Trend Engine
- Historical Snapshots

### Outcome

The project evolved from storing data to explaining it.

------------------------------------------------------------------------

# ✅ Evolution

**Status:** Complete

Prepared OpenLLMWorks for long-term growth and safe maintenance.

### Highlights

- UTC timestamp normalization
- Schema evolution
- Migration framework
- SHA-256 hashing
- Verified backups
- Utilities layer

### Outcome

The project gained the operational tools necessary to preserve data
integrity over time.

------------------------------------------------------------------------

# ✅ Identity

**Status:** Complete

Defined the philosophy, documentation, engineering culture, and public
identity of OpenLLMWorks.

### Highlights

- README
- Roadmap
- Manifesto
- Founding Story
- Architecture Guide
- Design Principles
- Contributing Guide
- AI Collaboration
- Parking Lot
- OpenLLMWorks public identity
- Open LLM Benchmark Database technical identity
- OLBD Protocol v1.0 provenance
- OpenLLMWorks.com
- Public GitHub repository

### Outcome

The project now documents not only *how* it works and *why* it exists,
but also presents a stable public identity under which the benchmark,
dataset, Runner, website, future research, and community can grow.

------------------------------------------------------------------------

# 🟡 Community

**Status:** Active - Public Beta

Current objective:

Prove that people outside the development environment can successfully
discover, run, submit to, and understand OpenLLMWorks.

The public-facing read/explore experience and the Windows NVIDIA
contribution path are now operational.

The major dependency has shifted from building the contribution system
to validating it with real external contributors.

### Delivered Foundations

- React website foundation
- Data-driven homepage
- Public production website
- OpenLLMWorks.com
- Public Beta identity
- Navigation
- Hardware Explorer
- GPU search
- Vendor filtering
- VRAM filtering
- Performance sorting
- GPU ranking context
- Hardware profile pages
- Multi-system GPU aggregation
- Individual benchmark history
- Tested configuration filtering
- Driver and CUDA provenance
- GPU comparison
- Comparison evidence context
- Connected discovery → profile → comparison user flows
- Responsive desktop and mobile foundations
- Leaderboards
- Snapshot browsing
- Documentation integration
- Standalone OpenLLMWorks Runner
- Managed and verified Protocol v1.0 assets
- Automated hardware evidence capture
- Automated three-run benchmark execution
- Canonical submission validation
- Upload-ready submission ZIP
- GitHub benchmark-submission workflow
- Maintainer-controlled ingestion
- Public GitHub repository
- Public Runner beta release
- Public release artifact verification
- GA4 baseline collection

### Current Goal

Move from internally proven contributor readiness to externally proven
contributor usability.

The next major milestone is not another large feature.

It is the first successful benchmark submission from someone who did not
build or operate the OpenLLMWorks development environment.

### Outcome Target

A newcomer should be able to:

1. Understand what OpenLLMWorks measures.
2. Explore real benchmark data.
3. Understand the evidence behind published results.
4. Find and download the public Runner.
5. Run the benchmark protocol.
6. Understand first-run provisioning.
7. Locate the generated submission ZIP.
8. Submit the result through the public workflow.
9. Receive clear validation feedback.
10. Contribute without risking the integrity of the historical dataset.

------------------------------------------------------------------------

# ⚪ Recommendations

**Status:** Planned

Turn benchmark data into actionable guidance.

### Planned Features

- Recommendation Engine
- Model Compatibility Explorer
- Hardware Build Planner
- Performance classifications
- Community-backed hardware suggestions
- Optional affiliate recommendations

### Goal

Help users answer the question:

> *"What can my computer actually run?"*

The recommendation layer should be built on sufficiently broad and
well-contextualized benchmark evidence rather than isolated benchmark
values.

Commercial or affiliate relationships should remain separate from
benchmark methodology, rankings, and editorial judgment.

------------------------------------------------------------------------

# ⚪ Platform

**Status:** Future

Expand OpenLLMWorks into a broader community platform.

### Planned Features

- Broader public benchmark participation
- Community accounts, if needed
- Public API
- Interactive dashboards
- Community contributions
- Submission moderation
- Dataset export
- Integration opportunities
- Additional accelerator vendors
- Additional operating systems

### Goal

Allow the community to continuously grow and enrich the benchmark
database while preserving trust, reproducibility, and historical
accuracy.

------------------------------------------------------------------------

# ⚪ Research Platform

**Status:** Vision

Become a trusted historical archive of local AI performance.

### Potential Features

- Long-term trend analysis
- Research datasets
- Academic exports
- Historical performance reports
- Hardware adoption studies
- Driver and software evolution studies
- LLM ecosystem evolution
- Cross-generation hardware analysis
- Cross-vendor analysis
- Cross-protocol analysis
- Model-generation analysis
- The Works research/editorial publishing

### Goal

Provide a lasting historical record of how local AI has evolved over
time.

------------------------------------------------------------------------

# Website Product Evolution

The website has progressed beyond its original role as a presentation
layer.

It is now the primary public interface for discovering and exploring the
OpenLLMWorks dataset and an entry point into the contribution workflow.

The current product journey is:

```text
Discover OpenLLMWorks
    ↓
Explore Hardware
    ↓
Search / Filter / Sort
    ↓
Inspect GPU Profile
    ↓
Understand Benchmark Evidence
    ↓
Inspect Test Context
    ↓
Compare Hardware
    ↓
Return to Deeper Evidence
```

The contributor journey extends this model:

```text
Discover OpenLLMWorks
    ↓
Understand the Benchmark
    ↓
Run Your First Benchmark
    ↓
Download OpenLLMWorks Runner
    ↓
Run Protocol v1.0
    ↓
Receive Submission ZIP
    ↓
Submit Result
    ↓
Validated Result
    ↓
Canonical Database
    ↓
Website
```

Future website development should preserve these connected user-flow
models.

Features should not merely exist.

Users should be able to discover how those features relate to one
another.

------------------------------------------------------------------------

# Hardware Discovery

**Status:** v1 Foundation Complete

### Delivered

- GPU browsing
- GPU search
- Vendor filtering
- VRAM filtering
- Multiple sorting modes
- Relative performance bars
- Performance ranking
- Benchmark-result counts
- Stable GPU variant identity
- Direct hardware-profile navigation
- Comparison selection from Hardware Explorer

### Future Evolution

As the dataset grows:

- Additional filter dimensions
- More advanced sorting
- Pagination or virtualization
- Larger-catalog navigation
- Saved or shareable filters
- Better mobile discovery
- Search refinements
- Configuration-aware discovery
- Vendor-aware discovery as AMD and Intel coverage expands

The v1 discovery foundation is complete.

The concept itself is not considered permanently finished.

------------------------------------------------------------------------

# Hardware Profiles

**Status:** v1 Foundation Complete

### Delivered

- Aggregated GPU performance
- pp512 ranking
- tg128 ranking
- Best and worst benchmark context
- Benchmark history
- Tested memory configurations
- Operating systems
- CPU context
- VRAM context
- Driver provenance
- CUDA provenance
- Configuration filtering
- Direct comparison entry point

### Future Evolution

Potential additions include:

- Additional software provenance
- Benchmark protocol details
- Model / quantization context
- Driver-history views
- Performance distribution
- More detailed configuration filters
- Historical change visualization
- Shareable profile views
- Cross-vendor software-stack context

Hardware identity and benchmark environment should remain separate
concepts.

------------------------------------------------------------------------

# GPU Comparison

**Status:** v1 Foundation Complete

### Delivered

- Direct GPU-vs-GPU comparison
- pp512 comparison
- tg128 comparison
- Percentage performance difference
- VRAM comparison
- Benchmark-result counts
- Tested memory comparison
- Operating-system comparison
- Evidence/sample context
- Links back to GPU profiles
- Discovery → comparison flow
- Profile → comparison flow
- URL-preserved comparison selection

### Interpretation Principle

Published comparison values describe the currently available benchmark
evidence.

They should not automatically be interpreted as controlled laboratory
head-to-head tests.

### Future Evolution

Potential additions include:

- Shareable comparison URLs and richer metadata
- Additional benchmark metrics
- Configuration-matched comparisons
- Driver-matched comparisons
- Model-specific comparisons
- Confidence or evidence scoring
- Distribution-based comparison
- Historical comparison
- Multi-GPU comparison
- Cross-vendor comparison

Weekend 11 delivered the v1 comparison foundation earlier than
originally planned.

------------------------------------------------------------------------

# Benchmark Evidence & Provenance

**Status:** v1 Foundation Complete

OpenLLMWorks should preserve not only benchmark performance, but also
the environment that produced it.

### Current Context

Published benchmark results can preserve:

- CPU
- System memory
- Operating system
- GPU VRAM
- GPU driver version
- CUDA UMD version
- NVIDIA SMI version

Not every historical submission contains every field.

Missing provenance remains unknown rather than being inferred.

### Principle

> **Unknown is better than invented.**

### Future Evolution

As the benchmark protocol evolves:

- Capture additional backend information
- Capture richer software-stack versions
- Improve cross-platform provenance
- Track benchmark protocol revisions
- Preserve model and quantization context
- Support software-version analysis
- Explore performance changes across driver generations
- Preserve vendor-specific runtime provenance
- Support cross-vendor evidence without flattening meaningful differences

------------------------------------------------------------------------

# Comparison Evidence

**Status:** v1 Foundation Complete

Benchmark averages should communicate the amount and diversity of
evidence behind them.

### Delivered

- Benchmark-result counts
- Tested memory-configuration counts
- Tested operating-system counts
- Single-result labeling
- Limited-sample labeling
- Growing-sample labeling
- Comparison methodology/context messaging

### Future Evolution

The current labels are intentionally simple.

As the dataset grows, OpenLLMWorks may explore:

- Evidence scores
- Confidence indicators
- Minimum sample thresholds
- Configuration diversity
- Statistical dispersion
- Outlier visibility
- Matched-system comparisons

Evidence presentation should remain understandable to ordinary visitors
and should not imply more statistical certainty than the dataset
supports.

------------------------------------------------------------------------

# Development Validation Model

OpenLLMWorks uses complementary forms of validation.

## Engineering Validation

Ask:

> **Does the feature work correctly?**

Examples:

- Does the parser extract the correct value?
- Does normalization preserve meaning?
- Does duplicate detection behave correctly?
- Does the publisher generate valid JSON?
- Does the website consume the correct contract?
- Does comparison math produce the correct result?
- Does the Runner verify assets correctly?
- Does a submission pass canonical validation?

## User-Flow Validation

Ask:

> **Can someone understand how to use it?**

Examples:

- Can someone discover hardware?
- Can someone interpret a benchmark score?
- Can someone move from discovery to a GPU profile?
- Can someone initiate a comparison naturally?
- Can someone understand the evidence behind an average?
- Can someone find the Runner?
- Can someone understand first-run provisioning?
- Can someone locate the submission ZIP?
- Can someone submit a result without maintainer coaching?

## External Validation

Ask:

> **Can someone outside the project successfully use it?**

Examples:

- Can a first-time visitor understand OpenLLMWorks?
- Can an external contributor download the correct artifact?
- Can they navigate Windows trust warnings?
- Can they complete the benchmark without development tools?
- Can they understand failures and recovery guidance?
- Can their submission enter the canonical workflow without repair?

Public-beta development should include all three validation modes.

------------------------------------------------------------------------

# Weekend Sprint Roadmap

The weekend roadmap is a working implementation plan.

Sprint scope may move forward or backward as dependencies become
clearer.

Completing work earlier than planned does not require artificially
repeating that work in a later weekend.

------------------------------------------------------------------------

## ✅ Weekend 1-5 - Core Foundation

**Status:** Complete

Established:

- Benchmark execution
- Parser
- Persistent database
- Analytics
- Validation
- Documentation
- Governance

------------------------------------------------------------------------

## ✅ Weekend 6 - Website Foundation

**Status:** Complete

Established:

- React / Vite application
- Navigation
- Homepage
- Design system
- Component structure
- Public repository workflow
- Website vision

------------------------------------------------------------------------

## ✅ Weekend 7 - Publisher & Data Integration

**Status:** Complete

Established:

- Website data contracts
- Publisher architecture
- Generated homepage data
- Manifest generation
- Python → React data flow
- Data-driven homepage

------------------------------------------------------------------------

## ✅ Weekend 8 - Analytics Integration

**Status:** Complete

Established:

- Real benchmark analytics powering the website
- Leaderboards
- Snapshot integration
- Additional publisher outputs
- Website analytics foundation

------------------------------------------------------------------------

## ✅ Weekend 9 - Hardware Explorer & Multi-System Validation

**Status:** Complete

Established:

- Hardware Explorer
- Hardware profiles
- Multi-system GPU aggregation
- Benchmark history
- Tested configurations
- Responsive hardware experience
- Real-world validation across multiple systems

------------------------------------------------------------------------

## ✅ Weekend 10 - Hardware Data Architecture

**Status:** Complete

Established:

- Richer hardware identity
- Canonical GPU variant handling
- Public hardware contract improvements
- Hardware identity reconciliation
- Publisher validation
- Production-build validation

### Outcome

The hardware layer became stable enough to support richer discovery,
comparison, and future community data.

------------------------------------------------------------------------

## ✅ Weekend 11 - Discovery & Comparison

**Status:** Complete

Weekend 11 expanded beyond its original scope.

### Delivered

- Hardware search improvements
- Vendor filtering
- VRAM filtering
- Expanded sorting
- Relative performance visualization
- GPU ranking context
- Richer hardware profiles
- Benchmark-history filtering
- Driver and CUDA provenance
- GPU comparison
- Percentage performance differences
- Tested-configuration comparison
- Evidence/sample context
- Discovery → comparison flow
- Profile → comparison flow
- Comparison-selection UX polish

### Outcome

OpenLLMWorks gained a connected hardware exploration experience.

Weekend 11 also delivered the v1 foundation of Browse / Filter / Compare
UX earlier than originally scheduled.

------------------------------------------------------------------------

## ✅ Weekend 12 - Submission Pipeline Hardening

**Status:** Complete

### Objective

Make benchmark ingestion safer, clearer, and more contributor-ready
before opening the submission path more broadly.

### Delivered

- Added lightweight structural submission preflight validation
- Validate required hardware evidence before deeper parsing
- Reject submissions containing no benchmark run files
- Preserve legacy two-run submissions with explicit warnings
- Added optional `submission.json` manifest support
- Added manifest schema versioning
- Validate contributor-provided submission identity
- Validate ISO-8601 submission and benchmark timestamps
- Reject malformed or structurally invalid manifests
- Preserve compatibility with historical folder-based submissions
- Propagate validated manifest metadata into normalized result records
- Tolerate unknown manifest fields for forward compatibility
- Added contributor-facing manifest documentation
- Updated `example_submission/` with a working manifest example
- Intentionally tested malformed and invalid submission cases

### Validation Coverage

Weekend 12 intentionally exercised:

- Valid manifest
- Unsupported schema version
- Empty submission name
- Incorrect submission-name type
- Invalid submission timestamp
- Invalid benchmark timestamp
- Non-object JSON root
- Malformed JSON
- Unknown manifest fields
- Missing required hardware evidence
- Missing manifest / legacy submission
- Historical two-run submission
- Manifest metadata propagation

### Compatibility

`submission.json` remains optional.

Historical submissions without a manifest continue through the existing
folder-based workflow and receive a warning explaining that legacy
metadata is being used.

Raw benchmark and hardware evidence remain authoritative.
Contributor-provided manifest metadata does not replace measured
hardware or benchmark data.

### Outcome

OpenLLMWorks established a stronger trust boundary at the beginning of
the submission pipeline.

Structurally invalid submissions can fail before deeper parsing, valid
contributors can provide explicit submission metadata, and historical
benchmark packages remain compatible with the current pipeline.

------------------------------------------------------------------------

## ✅ Weekend 13 - Leaderboards & Analytics Expansion

**Status:** Complete

### Objective

Build richer insight layers on top of the increasingly trustworthy
dataset.

Weekend 13 focused on deeper interpretation of benchmark evidence while
preserving clear boundaries between analytics, public data contracts,
and website presentation.

### Completed Sprints

- Sprint 1 - Analytics & Schema Compatibility
- Sprint 2 - Statistics Expansion
- Sprint 3 - GPU-Profile Leaderboards & Publishing
- Sprint 4 - Published Leaderboard Website Integration

### Outcome

Weekend 13 established a canonical analytics-to-presentation path.

```text
Benchmark Database
        ↓
Canonical Analytics
        ↓
GPU Profiles
        ↓
GPU Rankings
        ↓
Leaderboard Publisher
        ↓
leaderboards.json
        ↓
        +----------------------+
        |                      |
        v                      v
Hardware Explorer       Hardware Profile
```

Python analytics owns ranking.

The publisher owns the public leaderboard contract.

React consumes that contract and owns presentation.

The website no longer independently reconstructs authoritative GPU
rankings.

------------------------------------------------------------------------

## ✅ Weekend 14 - Contributor Workflow & Runner Foundation

**Status:** Complete

### Objective

Make it practical for someone outside the project to contribute benchmark
results while preserving the canonical trust boundary.

### Delivered

- Contributor journey and onboarding documentation
- Contributor-facing canonical validator
- Clear validation warnings and failure states
- Initial OpenLLMWorks Runner
- NVIDIA environment detection
- Frozen model and `llama-bench.exe` SHA-256 verification
- Automatic hardware-evidence collection
- Automatic three-run Benchmark Protocol v1.0 execution
- pp512 and tg128 result parsing
- Automatic `submission.json` generation
- Canonical submission validation
- Upload-ready ZIP packaging
- GitHub Issue benchmark-submission workflow
- First fresh-GPU end-to-end Runner rehearsal using a GTX 1050 2 GB
- Maintainer download and independent validation
- Controlled canonical database import
- Publisher regeneration
- Website verification of the imported result

### Outcome

Weekend 14 proved the complete contribution lifecycle:

```text
Runner
    |
    v
Validated Submission ZIP
    |
    v
GitHub Issue
    |
    v
Maintainer Validation / Import
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

The benchmark system and maintainer system can remain separate, and the
Runner does not receive authority to modify the canonical database.

------------------------------------------------------------------------

## ✅ Weekend 15 - Runner to Contributor Ready

**Status:** Complete

### Objective

Harden the proven Runner workflow, formalize maintainer ingestion, align the
contributor experience, and regression-test the complete handoff boundary.

### Completed Sprints

- Sprint 1 - Runner Hardening
- Sprint 2 - Maintainer Workflow
- Sprint 3 - Contributor UX & Documentation
- Sprint 4 - Regression Testing
- Sprint 5 - Cleanup & Checkpoint

### Delivered

- Hardened canonical submission-name validation
- Added benchmark-readiness guidance
- Improved environment, execution, and parsing failure guidance
- Added focused single-submission maintainer processing
- Added maintainer-controlled provenance and verification inputs
- Documented the maintainer submission workflow
- Updated contributor documentation to a Runner-first model
- Updated the GitHub benchmark-submission Issue template
- Improved ZIP packaging so extraction recreates one validator-ready
  top-level submission directory
- Preserved manual and advanced validation workflows
- Performed a fresh current-build Quadro T1000 regression run
- Verified Runner version `0.3.0-dev3` end to end
- Extracted the generated ZIP into a clean temporary location
- Independently revalidated the extracted package successfully

### Outcome

```text
Contributor Runner
    |
    v
Upload-Ready ZIP
    |
    v
GitHub Submission
    |
    v
Independent Maintainer Validation
    |
    v
Controlled Import
```

The contribution path became technically complete.

Distribution and setup friction became the next contributor-facing
barriers.

------------------------------------------------------------------------

## ✅ Weekend 16 - Standalone Runner to Public Beta

**Status:** Complete

### Objective

Reduce the technical prerequisites between a new Windows contributor and a
successful OpenLLMWorks benchmark submission, establish the long-term public
identity, publish the project, and make the complete beta experience publicly
accessible.

Weekend 16 expanded substantially beyond the original standalone-packaging
plan.

The Runner became self-provisioning, recovery-tested, contributor-visible
during long operations, backward compatible with legacy managed assets, publicly
distributed, and connected to a live OpenLLMWorks website.

### Sprint 4 - Managed Assets

Delivered:

- Standalone Windows Runner with PyInstaller
- Embedded `runner/assets.json`
- Managed protocol storage outside the repository
- Verified frozen-model acquisition
- Verified upstream llama.cpp runtime acquisition
- Deterministic runtime assembly
- Retirement of the custom project-hosted runtime archive
- Exact size and SHA-256 verification
- End-to-end standalone benchmark validation

### Sprint 5 - Pristine / Recovery Validation

Validated on Bench-001:

- Clean-state first run
- Existing verified-asset reuse
- Corrupt managed-model recovery
- Forced model reacquisition
- Corrupt managed-runtime reconstruction
- User-aborted benchmark behavior
- Offline provisioning fail-closed behavior
- Connectivity-restored recovery
- Final healthy end-to-end regression

### Sprint 6 - Contributor UX & Failure Recovery

Delivered:

- Packaged completion visibility
- Handled-failure visibility
- Upload-ready ZIP and workspace discoverability
- Graceful `Ctrl+C` handling
- Retained partial-workspace reporting
- Safe-to-rerun guidance
- Local artifact status visibility
- Network-download visibility
- 10 percent download-progress milestones
- Preservation of existing verification and integrity guarantees

### Product / Name Gate

Decision:

```text
Public ecosystem:       OpenLLMWorks
Contributor app:        OpenLLMWorks Runner
Canonical dataset:      Open LLM Benchmark Database
Frozen methodology:     OLBD Protocol v1.0
```

Delivered:

- Competitive and naming review
- Public rebrand from OpenLLMBench to OpenLLMWorks
- GitHub repository rename
- Git remote update and verification
- `OpenLLMWorks.com` secured
- Project-layer rebrand
- Runner product rebrand
- Standalone artifact renamed to `OpenLLMWorks-Runner.exe`
- Backward-compatible legacy managed-asset reuse
- New benchmark results under `%LOCALAPPDATA%\OpenLLMWorks\results`
- Bench-001 legacy-upgrade regression

### Rebrand Reconciliation

Delivered:

- Current-facing documentation reconciliation
- Runner distribution documentation update
- Publisher regeneration
- Website regeneration
- Historical-reference classification
- Preservation of intentional legacy compatibility
- Final residual old-name audit

No unexplained current-facing OpenLLMBench branding remained.

### Sprint 7 - Release / Distribution / Public Launch

Delivered:

- Public repository readiness review
- GitHub repository made public
- Public Runner version convention
- OpenLLMWorks Runner `v0.3.0-beta.1`
- GitHub Release distribution
- Public release integrity information
- Public artifact download verification
- Contributor-facing beta release guidance
- Public website launch preparation
- Cloudflare production deployment
- OpenLLMWorks.com production domain
- HTTPS validation
- `www.openllmworks.com` availability
- Public navigation cleanup
- Public Beta identity
- Homepage → Runner release path
- Hardware and Compare stranger-style smoke test
- GA4 baseline collection
- GA4 Realtime verification

### Outcome

Weekend 16 crossed the Public Beta boundary.

```text
Internal Benchmark System
    ↓
Standalone Runner
    ↓
Self-Provisioning Runner
    ↓
Recovery-Tested Runner
    ↓
OpenLLMWorks Rebrand
    ↓
Public GitHub
    ↓
Public Runner Release
    ↓
OpenLLMWorks.com
    ↓
PUBLIC BETA
```

The next gate is external usage, not another internal launch prerequisite.

------------------------------------------------------------------------

# Current Compatibility Boundary

Existing verified assets may remain under:

```text
%LOCALAPPDATA%\OpenLLMBench\
```

New installations use:

```text
%LOCALAPPDATA%\OpenLLMWorks\
```

New benchmark output always belongs to:

```text
%LOCALAPPDATA%\OpenLLMWorks\results\
```

This allows existing contributors to reuse multi-gigabyte verified assets
without destructive migration, duplicate model storage, or forced redownloads.

------------------------------------------------------------------------

# Current Proven Contributor Path

The maintainer-tested public contribution path is:

```text
OpenLLMWorks.com
    ↓
OpenLLMWorks Runner
    ↓
Verify / Provision Frozen Assets
    ↓
Capture Hardware Evidence
    ↓
Run Three Benchmarks
    ↓
Canonical Validation
    ↓
Upload-Ready Submission ZIP
    ↓
GitHub Submission
    ↓
Maintainer Validation
    ↓
Canonical Import
    ↓
Publisher
    ↓
OpenLLMWorks.com
```

Contributors do not need to understand Python, repository internals, or manual
benchmark setup.

The path is technically proven internally.

External contributor usability is the next validation target.

------------------------------------------------------------------------

# 🚩 Public Beta Launch

**Status:** Live

OpenLLMWorks Public Beta launched during Weekend 16, ahead of the original
late-September / early-October planning target.

Current public state:

```text
OpenLLMWorks.com                         LIVE
www.openllmworks.com                     LIVE
HTTPS                                    PASS
GitHub repository                        PUBLIC
OpenLLMWorks Runner v0.3.0-beta.1       PUBLIC
Hardware Explorer                        LIVE
Hardware Profiles                        LIVE
GPU Compare                              LIVE
Public visitor smoke test                PASS
GA4 baseline collection                  LIVE
```

Public Beta is intentionally narrow.

Current primary contributor target:

```text
Windows + NVIDIA
```

The launch establishes public availability.

It does not imply that every planned accelerator, operating system, feature,
or community capability is complete.

------------------------------------------------------------------------

# Weekend 17 - External Beta & Stabilization

**Status:** Next

Weekend 17 should be driven primarily by evidence from external contributors
rather than speculative internal feature work.

## Sprint 1 - First External Contributor

### Objective

Prove that someone outside the OpenLLMWorks development environment can
complete the public contributor journey.

Preferred test:

```text
Discover OpenLLMWorks.com
    ↓
Understand Project
    ↓
Find Runner
    ↓
Download Public Release
    ↓
Navigate Windows Trust / SmartScreen
    ↓
Launch Runner
    ↓
Provision Assets
    ↓
Complete Three Runs
    ↓
Locate Submission ZIP
    ↓
Follow GitHub Submission Workflow
    ↓
Submit Result
    ↓
Maintainer Validation / Import
    ↓
Result Appears on Website
```

### Observe

- Project-purpose clarity
- Runner discoverability
- Download clarity
- SmartScreen friction
- Provisioning clarity
- Benchmark progress clarity
- ZIP discoverability
- Submission clarity
- Validation outcome
- Maintainer repair requirements

Avoid unnecessary coaching.

Confusion is useful beta evidence.

## Sprint 2 - Small External Beta

After the first external contribution succeeds or major blockers are fixed,
expand carefully to a small group of contributors.

Initial target:

```text
Approximately 3-5 external systems
```

The goal is not traffic volume.

The goal is diversity of real contributor behavior.

### Candidate Coverage

- Different NVIDIA generations
- Different Windows configurations
- Different driver versions
- Different levels of technical experience
- Clean first-run environments

## Sprint 3 - Feedback / Runner Stabilization

Prioritize fixes according to observed external friction.

Potential areas:

- Windows trust guidance
- First-run provisioning messaging
- Benchmark progress
- Error recovery
- Result discoverability
- Submission guidance
- Release documentation
- Hardware-detection edge cases

Do not change OLBD Protocol v1.0 to solve presentation or onboarding issues.

Protocol changes require benchmark-methodology justification.

## Sprint 4 - External Result Publication

Validate the full community loop:

```text
External Contributor
    ↓
Submission
    ↓
Maintainer Validation
    ↓
Canonical Import
    ↓
Publisher
    ↓
OpenLLMWorks.com
```

The first externally generated result appearing in the canonical database and
public website will represent an important project milestone.

------------------------------------------------------------------------

# Website Polish, UX & Discovery

**Status:** Ongoing after Public Beta

The website is now live, so polish work should be informed by actual visitor
behavior.

### Candidate Work

- Cross-page UX review
- Navigation refinement
- Empty states
- Error states
- Loading states
- Accessibility review
- Mobile polish
- Page titles
- Metadata
- Open Graph / social sharing
- Search-engine metadata
- Shareable hardware/comparison pages
- Performance review
- Broken-link monitoring
- Canonical `www` redirect
- Contributor-funnel clarity

The website should not enter a redesign loop merely because Public Beta has
launched.

Observed visitor and contributor friction should drive priorities.

------------------------------------------------------------------------

# Analytics Evolution

**Status:** Baseline Collection Active

GA4 baseline collection began with the Public Beta launch.

Current objective:

> **Collect the history now. Analyze it when it becomes useful.**

Initial production collection has been verified.

Future analytics may include:

- Runner release clicks
- GitHub visits
- Submit Results clicks
- Hardware-profile engagement
- Compare usage
- Contributor-funnel analysis
- Returning visitors
- Referral sources
- Popular GPU generations

Custom tracking should answer real product questions rather than accumulate
events without a decision-making purpose.

------------------------------------------------------------------------

# Dataset Growth

**Status:** Active / Early

The value of OpenLLMWorks increases as the dataset becomes broader while
remaining trustworthy.

Near-term growth should include both:

```text
Internal Controlled Runs
        +
External Community Runs
```

Internal testing remains useful for:

- Historical GPU coverage
- Regression validation
- Edge-case hardware
- Known controlled systems

External submissions add:

- Hardware diversity
- Software-stack diversity
- Real contributor behavior
- Independent evidence
- Community participation

Neither replaces the other.

------------------------------------------------------------------------

# Accelerator Expansion

**Status:** Planned

Windows + NVIDIA remains the first supported public path.

The next major accelerator family should be evaluated only after the NVIDIA
contributor path is externally validated.

Potential expansion:

```text
NVIDIA
    ↓
AMD
    ↓
Intel
```

This sequence is directional rather than permanently fixed.

## AMD

Potential AMD work includes:

- AMD GPU detection
- Vulkan viability
- ROCm viability where appropriate
- Backend selection
- AMD hardware evidence
- Radeon consumer cards
- Radeon Pro cards
- Cross-vendor result normalization
- Runner accelerator selection when multiple GPUs are installed

A unified contributor experience is desirable even if vendor-specific backend
logic remains modular internally.

## Intel

Future Intel investigation may include:

- Intel Arc
- Integrated Intel graphics where technically meaningful
- Backend support
- Hardware evidence
- Runtime distribution

Cross-vendor expansion must preserve reproducibility and clearly record backend
differences.

------------------------------------------------------------------------

# Model / Protocol Evolution

**Status:** Future

Qwen3-4B-Q4_K_M remains the Protocol v1.0 benchmark model.

Protocol v1.0 should remain frozen.

Future benchmark evolution may introduce additional protocol versions or model
tracks without rewriting historical v1.0 results.

Potential future questions include:

- Additional model families
- Different parameter sizes
- Different quantizations
- Prompt-processing workloads
- Generation workloads
- VRAM-constrained workloads
- CPU-specific workloads
- Cross-backend behavior

Historical comparability must remain explicit.

A future protocol should coexist with Protocol v1.0 rather than silently
changing what a v1.0 score means.

------------------------------------------------------------------------

# Recommendations Evolution

**Status:** Planned after dataset growth

Recommendation features become more useful as evidence broadens.

Potential capabilities:

- "What can my GPU run?"
- Model compatibility
- Expected performance ranges
- VRAM-aware guidance
- Budget hardware suggestions
- Upgrade comparisons
- Hardware build planning
- Used-hardware value analysis

Recommendations should distinguish:

```text
Measured Evidence
        vs
Derived Guidance
        vs
Commercial Recommendation
```

Benchmark rankings and methodology must remain independent from affiliate or
commercial relationships.

------------------------------------------------------------------------

# The Works - Research & Editorial

**Status:** Future

The Works is reserved as a future research/editorial layer within
OpenLLMWorks.

Potential topics include:

- Why OpenLLMWorks uses Qwen
- How Protocol v1.0 was designed
- What benchmark reproducibility means
- Historical GPU performance
- NVIDIA generation comparisons
- AMD versus NVIDIA local LLM behavior
- Driver-performance changes
- VRAM and model-fit analysis
- Used GPU value
- Benchmark methodology
- Dataset research

Editorial work should explain the evidence rather than obscure methodology.

The project should remain transparent about what is measured, how it is
measured, and where conclusions exceed the available evidence.

------------------------------------------------------------------------

# Public API & Dataset Access

**Status:** Future

As community and research use grows, OpenLLMWorks may expose more structured
access to its data.

Potential capabilities:

- Public API
- Downloadable datasets
- Versioned exports
- Research snapshots
- Citation guidance
- Machine-readable hardware profiles
- Historical leaderboard exports

Public data access must preserve provenance and make protocol/version context
clear.

------------------------------------------------------------------------

# Release Strategy

OpenLLMWorks should use incremental beta releases rather than waiting for a
fictional point where every planned feature is complete.

Current public release:

```text
OpenLLMWorks Runner v0.3.0-beta.1
```

Future beta releases should be justified by meaningful changes such as:

- Contributor-blocking bug fixes
- Important UX improvements
- Hardware compatibility fixes
- Distribution improvements
- Security or integrity fixes

Avoid unnecessary version churn during early external testing.

The public beta website and Runner may evolve independently where appropriate.

------------------------------------------------------------------------

# Public Beta Success Criteria

Public Beta success is no longer defined by simply launching the website.

The website is live.

The Runner is public.

The next success criteria are evidence-based.

OpenLLMWorks should demonstrate:

- External contributors can find the Runner
- External contributors can run it successfully
- External submissions pass validation
- Maintainer ingestion works without manual reconstruction
- External results can be published
- Contributor friction is observable and fixable
- Dataset breadth begins increasing
- Benchmark integrity remains intact
- Public visitors can understand the results
- The project can evolve without rewriting historical evidence

------------------------------------------------------------------------

# Current Critical Path

The old critical path was:

```text
Release / Distribution
    ↓
Contributor Documentation
    ↓
Beta Candidate
    ↓
Website Integration
    ↓
Launch Readiness
    ↓
Public Beta
```

That path is complete.

The current critical path is:

```text
PUBLIC BETA
    ↓
First External Contributor
    ↓
First External Result Published
    ↓
Small External Beta
    ↓
Observed Feedback
    ↓
Runner / Documentation Stabilization
    ↓
Dataset Growth
    ↓
Broader Community Participation
    ↓
Accelerator Expansion
```

The largest near-term risks are now:

- external contributor friction
- Windows trust expectations
- documentation clarity
- unknown external-machine edge cases
- early dataset breadth
- submission friction

Distribution, website launch, public naming, managed provisioning, submission
trust, maintainer ingestion, hardware discovery, and comparison are no longer
primary launch blockers.

------------------------------------------------------------------------

# Beyond Public Beta

After the initial external beta, development can expand toward:

- Larger community datasets
- Richer statistical analysis
- Configuration-matched comparisons
- AMD benchmarking
- Intel benchmarking
- Model compatibility
- Recommendation systems
- Hardware build guidance
- Public API
- Dataset exports
- Research tooling
- Hardware adoption trends
- Driver and software evolution analysis
- Long-term local AI performance history
- The Works editorial/research program

The roadmap should remain flexible.

OpenLLMWorks should grow in response to the quality and usefulness of
its dataset rather than accumulating features for their own sake.

------------------------------------------------------------------------

# Guiding Principle

Every new capability should strengthen at least one part of the mission:

> **Measure. Understand. Preserve.**

If a feature does not improve measurement, understanding, preservation,
or the community's ability to contribute trustworthy evidence, it should
not take priority over work that does.

------------------------------------------------------------------------

# Current Position

```text
Foundation                              COMPLETE
Intelligence                            COMPLETE
Evolution                               COMPLETE
Identity                                COMPLETE
Community                               ACTIVE
Standalone Runner                       COMPLETE
Managed Assets                          COMPLETE
Recovery Validation                     COMPLETE
OpenLLMWorks Rebrand                    COMPLETE
Public GitHub                           LIVE
Runner v0.3.0-beta.1                    LIVE
OpenLLMWorks.com                        LIVE
Public Beta                             LIVE
Analytics Baseline                      LIVE
First External Contributor              NEXT
Small External Beta                     UPCOMING
Dataset Growth                          ACTIVE / EARLY
AMD Expansion                           PLANNED
Recommendations                         PLANNED
Platform                                FUTURE
Research Platform                       VISION
```

The project has crossed the launch boundary.

The next phase is not about proving that OpenLLMWorks can be built.

It is about proving that OpenLLMWorks can be used.