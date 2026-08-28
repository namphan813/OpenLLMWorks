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

``` text
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

-   Benchmark parser
-   Persistent benchmark database
-   Deterministic result IDs
-   Duplicate detection
-   Core statistics engine

### Outcome

OpenLLMWorks became capable of reliably collecting and storing benchmark
data.

------------------------------------------------------------------------

# ✅ Intelligence

**Status:** Complete

Transformed benchmark records into reusable insights.

### Highlights

-   Statistics
-   Leaderboards
-   Hardware Profiles
-   Interesting Facts
-   Snapshot Viewer
-   Trend Engine
-   Historical Snapshots

### Outcome

The project evolved from storing data to explaining it.

------------------------------------------------------------------------

# ✅ Evolution

**Status:** Complete

Prepared OpenLLMWorks for long-term growth and safe maintenance.

### Highlights

-   UTC timestamp normalization
-   Schema evolution
-   Migration framework
-   SHA-256 hashing
-   Verified backups
-   Utilities layer

### Outcome

The project gained the operational tools necessary to preserve data
integrity over time.

------------------------------------------------------------------------

# ✅ Identity

**Status:** Complete

Defined the philosophy, documentation, and engineering culture of
OpenLLMWorks.

### Highlights

-   README
-   Roadmap
-   Manifesto
-   Founding Story
-   Architecture Guide
-   Design Principles
-   Contributing Guide
-   AI Collaboration
-   Parking Lot

### Outcome

The project now documents not only *how* it works, but *why* it exists.

------------------------------------------------------------------------

# 🟡 Community

**Status:** Active

Current objective:

Prepare OpenLLMWorks for meaningful community use and contribution.

The public-facing experience now has a strong v1 foundation. The next
major dependency is making contribution and ingestion equally
trustworthy.

### Delivered Foundations

-   React website foundation
-   Data-driven homepage
-   Navigation
-   Hardware Explorer
-   GPU search
-   Vendor filtering
-   VRAM filtering
-   Performance sorting
-   GPU ranking context
-   Hardware profile pages
-   Multi-system GPU aggregation
-   Individual benchmark history
-   Tested configuration filtering
-   Driver and CUDA provenance
-   GPU comparison
-   Comparison evidence context
-   Connected discovery → profile → comparison user flows
-   Responsive desktop and mobile foundations
-   Leaderboards
-   Snapshot browsing
-   Documentation integration

### Current Goal

Move from a strong read/explore experience toward a trustworthy
contribution experience.

That means strengthening the path by which benchmark data enters
OpenLLMWorks before opening that path more broadly to the community.

### Outcome Target

A newcomer should eventually be able to:

1.  Understand what OpenLLMWorks measures.
2.  Explore real benchmark data.
3.  Understand the evidence behind published results.
4.  Run the benchmark protocol.
5.  Submit a result.
6.  Receive clear validation feedback.
7.  Contribute without risking the integrity of the historical dataset.

------------------------------------------------------------------------

# ⚪ Recommendations

**Status:** Planned

Turn benchmark data into actionable guidance.

### Planned Features

-   Recommendation Engine
-   Model Compatibility Explorer
-   Hardware Build Planner
-   Performance classifications
-   Community-backed hardware suggestions
-   Optional affiliate recommendations

### Goal

Help users answer the question:

> *"What can my computer actually run?"*

The recommendation layer should be built on sufficiently broad and
well-contextualized benchmark evidence rather than isolated benchmark
values.

------------------------------------------------------------------------

# ⚪ Platform

**Status:** Future

Expand OpenLLMWorks into a broader community platform.

### Planned Features

-   Public benchmark submission
-   Community accounts, if needed
-   Public API
-   Interactive dashboards
-   Community contributions
-   Submission moderation
-   Dataset export
-   Integration opportunities

### Goal

Allow the community to continuously grow and enrich the benchmark
database while preserving trust, reproducibility, and historical
accuracy.

------------------------------------------------------------------------

# ⚪ Research Platform

**Status:** Vision

Become a trusted historical archive of local AI performance.

### Potential Features

-   Long-term trend analysis
-   Research datasets
-   Academic exports
-   Historical performance reports
-   Hardware adoption studies
-   Driver and software evolution studies
-   LLM ecosystem evolution
-   Cross-generation hardware analysis

### Goal

Provide a lasting historical record of how local AI has evolved over
time.

------------------------------------------------------------------------

# Website Product Evolution

The website has progressed beyond its original role as a presentation
layer.

It is becoming the primary interface for exploring the OpenLLMWorks
dataset.

The current product journey is:

``` text
Discover Hardware
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

Future website development should preserve this connected user-flow
model.

Features should not merely exist.

Users should be able to discover how those features relate to one
another.

------------------------------------------------------------------------

# Hardware Discovery

**Status:** v1 Foundation Complete

### Delivered

-   GPU browsing
-   GPU search
-   Vendor filtering
-   VRAM filtering
-   Multiple sorting modes
-   Relative performance bars
-   Performance ranking
-   Benchmark-result counts
-   Stable GPU variant identity
-   Direct hardware-profile navigation
-   Comparison selection from Hardware Explorer

### Future Evolution

As the dataset grows:

-   Additional filter dimensions
-   More advanced sorting
-   Pagination or virtualization
-   Larger-catalog navigation
-   Saved or shareable filters
-   Better mobile discovery
-   Search refinements
-   Configuration-aware discovery

The v1 discovery foundation is complete.

The concept itself is not considered permanently finished.

------------------------------------------------------------------------

# Hardware Profiles

**Status:** v1 Foundation Complete

### Delivered

-   Aggregated GPU performance
-   pp512 ranking
-   tg128 ranking
-   Best and worst benchmark context
-   Benchmark history
-   Tested memory configurations
-   Operating systems
-   CPU context
-   VRAM context
-   Driver provenance
-   CUDA provenance
-   Configuration filtering
-   Direct comparison entry point

### Future Evolution

Potential additions include:

-   Additional software provenance
-   Benchmark protocol details
-   Model / quantization context
-   Driver-history views
-   Performance distribution
-   More detailed configuration filters
-   Historical change visualization
-   Shareable profile views

Hardware identity and benchmark environment should remain separate
concepts.

------------------------------------------------------------------------

# GPU Comparison

**Status:** v1 Foundation Complete

### Delivered

-   Direct GPU-vs-GPU comparison
-   pp512 comparison
-   tg128 comparison
-   Percentage performance difference
-   VRAM comparison
-   Benchmark-result counts
-   Tested memory comparison
-   Operating-system comparison
-   Evidence/sample context
-   Links back to GPU profiles
-   Discovery → comparison flow
-   Profile → comparison flow
-   URL-preserved comparison selection

### Interpretation Principle

Published comparison values describe the currently available benchmark
evidence.

They should not automatically be interpreted as controlled laboratory
head-to-head tests.

### Future Evolution

Potential additions include:

-   Shareable comparison URLs and richer metadata
-   Additional benchmark metrics
-   Configuration-matched comparisons
-   Driver-matched comparisons
-   Model-specific comparisons
-   Confidence or evidence scoring
-   Distribution-based comparison
-   Historical comparison
-   Multi-GPU comparison

Weekend 11 delivered the v1 comparison foundation earlier than
originally planned.

------------------------------------------------------------------------

# Benchmark Evidence & Provenance

**Status:** v1 Foundation Complete

OpenLLMWorks should preserve not only benchmark performance, but also
the environment that produced it.

### Current Context

Published benchmark results can preserve:

-   CPU
-   System memory
-   Operating system
-   GPU VRAM
-   GPU driver version
-   CUDA UMD version
-   NVIDIA SMI version

Not every historical submission contains every field.

Missing provenance remains unknown rather than being inferred.

### Principle

> **Unknown is better than invented.**

### Future Evolution

As the benchmark protocol evolves:

-   Capture additional backend information
-   Capture richer software-stack versions
-   Improve cross-platform provenance
-   Track benchmark protocol revisions
-   Preserve model and quantization context
-   Support software-version analysis
-   Explore performance changes across driver generations

------------------------------------------------------------------------

# Comparison Evidence

**Status:** v1 Foundation Complete

Benchmark averages should communicate the amount and diversity of
evidence behind them.

### Delivered

-   Benchmark-result counts
-   Tested memory-configuration counts
-   Tested operating-system counts
-   Single-result labeling
-   Limited-sample labeling
-   Growing-sample labeling
-   Comparison methodology/context messaging

### Future Evolution

The current labels are intentionally simple.

As the dataset grows, OpenLLMWorks may explore:

-   Evidence scores
-   Confidence indicators
-   Minimum sample thresholds
-   Configuration diversity
-   Statistical dispersion
-   Outlier visibility
-   Matched-system comparisons

Evidence presentation should remain understandable to ordinary visitors
and should not imply more statistical certainty than the dataset
supports.

------------------------------------------------------------------------

# Development Validation Model

OpenLLMWorks now uses two complementary forms of validation.

## Engineering Validation

Ask:

> **Does the feature work correctly?**

Examples:

-   Does the parser extract the correct value?
-   Does normalization preserve meaning?
-   Does duplicate detection behave correctly?
-   Does the publisher generate valid JSON?
-   Does the website consume the correct contract?
-   Does comparison math produce the correct result?

## User-Flow Validation

Ask:

> **Can someone understand how to use it?**

Examples:

-   Can someone discover hardware?
-   Can someone interpret a benchmark score?
-   Can someone move from discovery to a GPU profile?
-   Can someone initiate a comparison naturally?
-   Can someone understand the evidence behind an average?
-   Can someone return to deeper benchmark context?

Future website work should include both validation modes.

------------------------------------------------------------------------

# Weekend Sprint Roadmap

The weekend roadmap is a working implementation plan.

Sprint scope may move forward or backward as dependencies become
clearer.

Completing work earlier than planned does not require artificially
repeating that work in a later weekend.

------------------------------------------------------------------------

## ✅ Weekend 1--5 --- Core Foundation

**Status:** Complete

Established:

-   Benchmark execution
-   Parser
-   Persistent database
-   Analytics
-   Validation
-   Documentation
-   Governance

------------------------------------------------------------------------

## ✅ Weekend 6 --- Website Foundation

**Status:** Complete

Established:

-   React / Vite application
-   Navigation
-   Homepage
-   Design system
-   Component structure
-   Public repository workflow
-   Website vision

------------------------------------------------------------------------

## ✅ Weekend 7 --- Publisher & Data Integration

**Status:** Complete

Established:

-   Website data contracts
-   Publisher architecture
-   Generated homepage data
-   Manifest generation
-   Python → React data flow
-   Data-driven homepage

------------------------------------------------------------------------

## ✅ Weekend 8 --- Analytics Integration

**Status:** Complete

Established:

-   Real analytics powering the website
-   Leaderboards
-   Snapshot integration
-   Additional publisher outputs
-   Website analytics foundation

------------------------------------------------------------------------

## ✅ Weekend 9 --- Hardware Explorer & Multi-System Validation

**Status:** Complete

Established:

-   Hardware Explorer
-   Hardware profiles
-   Multi-system GPU aggregation
-   Benchmark history
-   Tested configurations
-   Responsive hardware experience
-   Real-world validation across multiple systems

------------------------------------------------------------------------

## ✅ Weekend 10 --- Hardware Data Architecture

**Status:** Complete

Established:

-   Richer hardware identity
-   Canonical GPU variant handling
-   Public hardware contract improvements
-   Hardware identity reconciliation
-   Publisher validation
-   Production-build validation

### Outcome

The hardware layer became stable enough to support richer discovery,
comparison, and future community data.

------------------------------------------------------------------------

## ✅ Weekend 11 --- Discovery & Comparison

**Status:** Complete

Weekend 11 expanded beyond its original scope.

### Delivered

-   Hardware search improvements
-   Vendor filtering
-   VRAM filtering
-   Expanded sorting
-   Relative performance visualization
-   GPU ranking context
-   Richer hardware profiles
-   Benchmark-history filtering
-   Driver and CUDA provenance
-   GPU comparison
-   Percentage performance differences
-   Tested-configuration comparison
-   Evidence/sample context
-   Discovery → comparison flow
-   Profile → comparison flow
-   Comparison-selection UX polish

### Outcome

OpenLLMWorks gained a connected hardware exploration experience.

Weekend 11 also delivered the v1 foundation of Browse / Filter / Compare
UX earlier than originally scheduled.

------------------------------------------------------------------------

## ✅ Weekend 12 --- Submission Pipeline Hardening

**Status:** Complete

### Objective

Make benchmark ingestion safer, clearer, and more contributor-ready
before opening the submission path more broadly.

### Delivered

-   Added lightweight structural submission preflight validation
-   Validate required hardware evidence before deeper parsing
-   Reject submissions containing no benchmark run files
-   Preserve legacy two-run submissions with explicit warnings
-   Added optional `submission.json` manifest support
-   Added manifest schema versioning
-   Validate contributor-provided submission identity
-   Validate ISO-8601 submission and benchmark timestamps
-   Reject malformed or structurally invalid manifests
-   Preserve compatibility with historical folder-based submissions
-   Propagate validated manifest metadata into normalized result records
-   Tolerate unknown manifest fields for forward compatibility
-   Added contributor-facing manifest documentation
-   Updated `example_submission/` with a working manifest example
-   Intentionally tested malformed and invalid submission cases

### Validation Coverage

Weekend 12 intentionally exercised:

-   Valid manifest
-   Unsupported schema version
-   Empty submission name
-   Incorrect submission-name type
-   Invalid submission timestamp
-   Invalid benchmark timestamp
-   Non-object JSON root
-   Malformed JSON
-   Unknown manifest fields
-   Missing required hardware evidence
-   Missing manifest / legacy submission
-   Historical two-run submission
-   Manifest metadata propagation

### Compatibility

`submission.json` remains optional.

Historical submissions without a manifest continue through the existing
folder-based workflow and receive a warning explaining that legacy
metadata is being used.

Raw benchmark and hardware evidence remain authoritative.
Contributor-provided manifest metadata does not replace measured
hardware or benchmark data.

### Outcome

OpenLLMWorks now has a stronger trust boundary at the beginning of the
submission pipeline.

Structurally invalid submissions can fail before deeper parsing, valid
contributors can provide explicit submission metadata, and historical
benchmark packages remain compatible with the current pipeline.

This establishes the ingestion foundation needed for the future
contributor workflow. ---

## ✅ Weekend 13 --- Leaderboards & Analytics Expansion

**Status:** Complete

### Objective

Build richer insight layers on top of the increasingly trustworthy
dataset.

Weekend 13 focused on deeper interpretation of benchmark evidence while
preserving clear boundaries between analytics, public data contracts,
and website presentation.

### Completed Sprints

-   Sprint 1 --- Analytics & Schema Compatibility
-   Sprint 2 --- Statistics Expansion
-   Sprint 3 --- GPU-Profile Leaderboards & Publishing
-   Sprint 4 --- Published Leaderboard Website Integration

### Outcome

Weekend 13 established a canonical analytics-to-presentation path.

``` text
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

## Weekend 14 --- Contributor Workflow & Runner Foundation

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

## Weekend 15 --- Runner to Contributor Ready

**Status:** Complete

### Objective

Harden the proven Runner workflow, formalize maintainer ingestion, align the
contributor experience, and regression-test the complete handoff boundary.

### Completed Sprints

- Sprint 1 --- Runner Hardening
- Sprint 2 --- Maintainer Workflow
- Sprint 3 --- Contributor UX & Documentation
- Sprint 4 --- Regression Testing
- Sprint 5 --- Cleanup & Checkpoint

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

The contribution path is technically complete. Distribution and setup
friction are now the primary contributor-facing barriers.

------------------------------------------------------------------------

## Weekend 16 --- Standalone Runner, Contributor UX & Product Identity

**Status:** Active - Sprints 4-6 and Product / Name Gate Complete

### Objective

Reduce the technical prerequisites between a new Windows contributor and a
successful OpenLLMWorks benchmark submission, while preserving the frozen
benchmark protocol, verified assets, raw evidence, and maintainer-controlled
trust boundary.

Weekend 16 expanded beyond the original standalone-packaging plan. The Runner
is now self-provisioning, recovery-tested, contributor-visible during long
operations, backward compatible with legacy managed assets, and operating
under the new OpenLLMWorks public identity.

### Completed Work

#### Sprint 4 --- Managed Assets

- Built the standalone Windows Runner with PyInstaller
- Embedded `runner/assets.json`
- Established managed protocol storage outside the repository
- Added verified frozen-model acquisition
- Added verified upstream llama.cpp runtime acquisition
- Added deterministic runtime assembly
- Retired the custom project-hosted runtime archive
- Preserved exact size and SHA-256 verification
- Completed end-to-end standalone benchmark validation

#### Sprint 5 --- Pristine / Recovery Validation

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

#### Sprint 6 --- Contributor UX & Failure Recovery

- Kept packaged completion and handled-failure states visible
- Improved upload-ready ZIP and workspace discoverability
- Added graceful `Ctrl+C` handling
- Added retained partial-workspace reporting
- Added safe-to-rerun guidance
- Added local artifact status visibility
- Added network-download visibility
- Added 10 percent download-progress milestones
- Preserved existing verification and integrity guarantees

#### Product / Name Gate --- Complete

The planned pre-public-beta product gate was pulled forward before release and
distribution.

Decision:

```text
Public ecosystem:       OpenLLMWorks
Contributor app:        OpenLLMWorks Runner
Canonical dataset:      Open LLM Benchmark Database
Frozen methodology:     OLBD Protocol v1.0
```

Completed:

- Competitive and naming review
- Public rebrand from OpenLLMBench to OpenLLMWorks
- GitHub repository rename
- Git remote update and verification
- `OpenLLMWorks.com` secured
- Project-layer rebrand
- Runner product rebrand
- Standalone artifact renamed to `OpenLLMWorks-Runner.exe`
- Backward-compatible legacy managed-asset reuse
- New benchmark results redirected to `%LOCALAPPDATA%\OpenLLMWorks\results`
- Bench-001 legacy-upgrade regression
- Clean repository checkpoint

Frozen historical provenance and the Open LLM Benchmark Database / OLBD
Protocol v1.0 technical identity are preserved where appropriate rather than
being cosmetically rewritten.

### Current Compatibility Boundary

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

### Current Proven Contributor Path

```text
Download / Copy OpenLLMWorks-Runner.exe
    |
    v
Launch
    |
    v
Verify / Provision Frozen Assets
    |
    v
Benchmark
    |
    v
Canonical Validation
    |
    v
Receive Upload-Ready Submission ZIP
```

Contributors do not need to understand Python, repository internals, or manual
benchmark setup.

### Next --- Sprint 7: Release / Distribution

Primary targets:

- Define public Runner distribution location
- Define beta artifact naming/version convention
- Define repeatable release-build and verification steps
- Document Windows trust / SmartScreen expectations
- Publish contributor-verifiable integrity information
- Test the distributed artifact from a contributor-style download location
- Reconcile rebrand-sensitive distribution documentation
- Regenerate public website/publisher outputs from canonical sources
- Perform a final residual old-name audit
- Perform release-candidate regression

Sprint 7 should not change OLBD Protocol v1.0 unless a release-blocking
technical issue is discovered.

### Then --- Sprint 8: Public Contributor Documentation

Focus on stranger-followable installation, first-run, benchmark, submission,
failure-recovery, and support guidance.

### Outcome Target

```text
OpenLLMWorks Runner
    |
    v
Repeatable Beta Distribution
    |
    v
Public Contributor Documentation
    |
    v
Beta Candidate
```

------------------------------------------------------------------------

## Future --- Website Polish, UX & SEO

**Status:** Planned

### Objective

Prepare the public website for a broader audience after contributor
distribution is simplified.

### Candidate Work

- Cross-page UX review
- Navigation refinement
- Empty states
- Error states
- Loading states
- Accessibility review
- Mobile polish
- Metadata
- Open Graph / social sharing
- Search-engine metadata
- Shareable hardware/comparison pages
- Performance review

------------------------------------------------------------------------

## Future --- Release Candidate & Testing

**Status:** Planned

### Objective

Stabilize the project for the initial public release.

### Candidate Work

- Feature freeze
- End-to-end regression testing
- Parser regression testing
- Submission failure testing
- Publisher validation
- Production website build
- Cross-browser testing
- Responsive testing
- Documentation review
- Broken-link review
- Dataset integrity verification
- Backup verification
- Release notes
- Final bug fixes

### Outcome Target

Produce an OpenLLMWorks public-beta release candidate that is stable enough for
public use.

------------------------------------------------------------------------

# Target Release

## OpenLLMWorks Public Beta

**Target:** Late September -- Early October 2026

The target remains directional rather than absolute.

Data integrity and contributor safety take priority over hitting a
specific calendar date.

### v1.0 Should Demonstrate

-   Reproducible benchmark ingestion
-   Persistent historical benchmark storage
-   Trustworthy hardware identity
-   Data-driven analytics
-   Hardware discovery
-   Hardware profiles
-   Benchmark evidence
-   GPU comparison
-   Contributor documentation
-   Safe submission workflow
-   Public website
-   Reproducible publisher/build process

------------------------------------------------------------------------

# Scope Pulled Forward by Weekend 11

Weekend 11 completed several capabilities earlier than expected.

### Delivered Early

-   Browse / Filter / Compare v1
-   Comparison selection UX
-   GPU ranking context
-   Comparison evidence context
-   Driver/CUDA provenance presentation
-   Connected hardware exploration user flows

These items should not be rebuilt simply because they appeared later in
the original schedule.

Instead, later sprints should extend and validate them.

------------------------------------------------------------------------

# Remaining Critical Path to v1.0

The current critical path is:

```text
Release / Distribution
    |
    v
Public Contributor Documentation
    |
    v
Beta Candidate
    |
    v
Small External Beta
    |
    v
Runner Stabilization
    |
    v
Website Launch Integration
    |
    v
Launch Readiness
    |
    v
OpenLLMWorks Public Beta
```

Standalone execution, managed provisioning, recovery behavior, contributor UX,
submission trust, maintainer ingestion, hardware discovery, comparison, and
the public naming decision are no longer primary blockers.

The largest remaining risks are distribution friction, Windows trust
expectations, stranger-followable documentation, external-machine validation,
and release integration.

------------------------------------------------------------------------

# Beyond Public Beta

After the initial public beta, development can expand toward:

-   Larger community datasets
-   Richer statistical analysis
-   Configuration-matched comparisons
-   Model compatibility
-   Recommendation systems
-   Hardware build guidance
-   Public API
-   Dataset exports
-   Research tooling
-   Hardware adoption trends
-   Driver and software evolution analysis
-   Long-term local AI performance history

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
