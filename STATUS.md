# OpenLLMWorks - Project Status

## Weekend 19 - AMD / Vulkan Expansion

**Focus:** Cross-vendor accelerator support, backend provenance, Runner architecture, and first AMD benchmark path
**Status:** Starting / Architecture Review

---

## Current Objective

OpenLLMWorks has completed the core Windows/NVIDIA contributor and publication
lifecycle.

The proven production path is:

```text
OpenLLMWorks Runner
    |
    v
OLBD Protocol v1.0 Benchmark
    |
    v
Canonical Local Validation
    |
    v
Canonical Submission ZIP
    |
    v
Explicit Contributor Consent
    |
    v
HTTPS Direct Submission
    |
    v
Private R2 Intake
    |
    v
Automatic Server-Side Validation
    |
    v
D1 Operational State
    |
    v
Authenticated Control Room
    |
    v
Maintainer Approval
    |
    v
Controlled Canonical Import
    |
    v
Publisher
    |
    v
Production Publication Verification
    |
    v
OpenLLMWorks.com
```

The next major engineering boundary is accelerator expansion.

Weekend 19 asks:

> **Can OpenLLMWorks extend its proven Windows/NVIDIA benchmark path to
> AMD/Vulkan while preserving Protocol v1.0's workload, validation, provenance,
> and reproducibility guarantees, and clearly recording backend differences?**

The immediate target is not broad AMD support.

The target is the smallest trustworthy path from an AMD GPU through the
existing OpenLLMWorks lifecycle.

---

## Public Product Identity

```text
OpenLLMWorks
    |
    +-- OpenLLMWorks Runner
    |
    +-- Open LLM Benchmark Database
    |       |
    |       +-- OLBD Protocol v1.0
    |
    +-- Hardware Results / Comparisons
    |
    +-- Methodology
    |
    +-- The Works
    |       |
    |       +-- Experiments
    |       +-- Findings
    |       +-- Research Notes
    |       +-- Work in Progress
    |
    +-- Community
```

Brand roles:

- **OpenLLMWorks** - public project and ecosystem
- **OpenLLMWorks Runner** - contributor benchmark application
- **Open LLM Benchmark Database** - canonical technical benchmark dataset
- **OLBD Protocol v1.0** - frozen benchmark methodology and provenance
- **The Works** - research and editorial layer built on validated evidence

Current public positioning:

```text
Open benchmarks for local AI hardware.
```

Mission:

```text
Building the historical record of local AI performance.
```

Production website:

```text
https://openllmworks.com
```

GitHub repository:

```text
https://github.com/namphan813/OpenLLMWorks
```

Submission API:

```text
https://api.openllmworks.com/v1/submissions
```

---

## Current Runner

**Runner:** OpenLLMWorks Runner
**Current public platform:** Windows
**Current public accelerator path:** NVIDIA
**Current backend:** CUDA
**Benchmark Protocol:** OLBD Protocol v1.0

Current proven contributor workflow:

```text
Start Runner
    |
    v
Detect NVIDIA Environment
    |
    v
Verify / Provision Frozen Assets
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
Canonical Local Validation
    |
    v
Create Canonical ZIP
    |
    v
Show Submission Disclosure
    |
    v
Upload to OpenLLMWorks? [Y/N]
    |
    +--> N --> Preserve ZIP / manual fallback
    |
    +--> Y
             |
             v
          HTTPS Upload
             |
             v
          Submission ID
```

The Runner remains isolated from the canonical Open LLM Benchmark Database.

Contributor systems do not receive canonical database write authority.

---

## Protocol v1.0

OLBD Protocol v1.0 remains frozen.

Current benchmark workload:

- Qwen3-4B-Q4_K_M
- llama.cpp build 10069
- llama.cpp commit `178a6c449`
- pp512 prompt-processing measurement
- tg128 token-generation measurement
- three required benchmark runs
- arithmetic averaging
- raw benchmark evidence
- hardware evidence
- canonical validation

Protocol v1.0 currently has a proven Windows/NVIDIA/CUDA implementation.

Weekend 19 must not silently redefine what Protocol v1.0 means merely to add
another accelerator vendor.

Backend expansion and protocol evolution are separate concerns unless technical
evidence demonstrates that they cannot remain separate.

---

## Submission and Publication Lifecycle

The production submission lifecycle is operational.

Production infrastructure includes:

- HTTPS direct submission
- private Cloudflare R2 intake
- safe archive inspection and extraction
- authoritative Python canonical validation
- GitHub Actions validation workflow
- Cloudflare D1 operational state
- submission event history
- authenticated Control Room
- deliberate maintainer approval
- controlled canonical import
- publisher regeneration
- production publication verification

The canonical benchmark database remains separate from operational D1 state.

```text
R2
= submission artifacts and evidence

D1
= operational/control-plane state

Open LLM Benchmark Database
= canonical historical benchmark record
```

---

## Control Room

The maintainer Control Room is operational and protected by Cloudflare Access.

Administrative surfaces include:

```text
openllmworks.com/admin*
api.openllmworks.com/v1/admin/*
```

The Control Room supports the maintainer publication lifecycle rather than
granting contributors direct canonical access.

Proven capabilities include:

- authenticated maintainer access
- production D1 visibility
- submission review
- lifecycle state visibility
- approval workflow
- controlled canonical import
- publication verification
- recovery of published submissions
- retry-safe publication verification

Canonical Result ID is used as a publication identity guardrail.

Publication verification does not rely solely on GPU name or other ambiguous
hardware labels.

---

## Website

OpenLLMWorks.com is the primary public interface for the benchmark dataset.

Current major public surfaces include:

- Homepage
- Hardware Explorer
- Hardware Profiles
- GPU Comparison
- Leaderboards
- Methodology
- The Works
- Runner / contributor entry points

The homepage includes live benchmark highlights generated from published
hardware data.

The public site consumes publisher-generated data rather than independently
reconstructing canonical benchmark truth.

---

## Methodology

The Methodology page documents how OpenLLMWorks measures local AI hardware.

It explains:

- Protocol v1.0
- frozen benchmark workload
- Qwen3-4B Q4_K_M
- llama.cpp runtime identity
- pp512
- tg128
- three-run methodology
- arithmetic averaging
- evidence and provenance
- limitations
- future protocol philosophy

Editorial principle:

> OpenLLMWorks benchmarks hardware running local AI. It does not benchmark
> model intelligence.

---

## The Works

The Works is now an active OpenLLMWorks research and editorial surface.

Positioning:

> **Experiments, findings, and notes from the OpenLLMWorks lab.**

Editorial principle:

> **The benchmark database tells us what happened. The Works explores what it
> means.**

Supported content types:

- Experiment
- Finding
- Research Note
- Work in Progress

The Works includes:

- reusable article framework
- article registry
- public/private visibility
- featured article support
- route-specific SEO metadata
- research backlog
- dynamic sitemap integration
- dedicated article not-found experience

The first published Research Note is:

```text
What do PP512 and TG128 actually mean?
```

It establishes the foundational explanation of the two Protocol v1.0
performance measurements without introducing unsupported performance tiers or
workload recommendations.

The first planned hardware experiment remains:

```text
How far back can modern local AI go?
```

Research conclusions should follow validated evidence rather than precede it.

---

## Search and Discovery Foundation

Current public discovery infrastructure includes:

- route-specific page titles
- meta descriptions
- canonical URLs
- Open Graph metadata
- Twitter metadata
- robots.txt
- dynamically generated sitemap
- Google Search Console domain verification
- GA4 baseline analytics

The sitemap is generated from:

- core public routes
- published hardware variants
- public Works articles

Private or unpublished Works entries are excluded.

---

## Current Dataset

The dataset currently spans multiple NVIDIA generations and both consumer and
workstation hardware.

Current coverage includes examples from:

- Maxwell
- Pascal
- Turing
- Ampere
- Ada

The dataset includes both controlled internal systems and external contributor
results.

Dataset breadth remains early.

The project should continue adding evidence without sacrificing provenance or
validation quality.

Cross-generation observations may motivate research questions, but architectural
or causal conclusions require appropriate controlled evidence.

---

## Preserved Benchmark Guarantees

Platform expansion must preserve the project's existing trust model.

OpenLLMWorks currently guarantees:

- frozen Protocol v1.0 workload
- frozen benchmark model
- identified benchmark runtime
- verified benchmark assets
- SHA-256 asset verification
- three required benchmark runs
- raw benchmark evidence
- required hardware evidence
- canonical submission validation
- deterministic result identity
- explicit contributor consent
- authoritative server-side validation
- maintainer-controlled approval
- controlled canonical ingestion
- publication verification
- historical provenance
- separation between contributor systems and canonical data

AMD/Vulkan support must extend these guarantees rather than bypass them.

---

## Weekend Sprint History

Detailed historical snapshots are preserved in:

```text
docs/STATUS_HISTORY.md
```

### Weekend 14 - Contributor Workflow & Runner Foundation

Proved the first complete:

```text
Runner
-> Submission ZIP
-> Maintainer Validation
-> Canonical Import
-> Publisher
-> Website
```

### Weekend 15 - Runner to Contributor Ready

Hardened Runner behavior, contributor guidance, maintainer ingestion, packaging,
and regression testing.

### Weekend 16 - Standalone Runner & Public Beta

Delivered:

- self-provisioning standalone Runner
- managed Protocol v1.0 assets
- recovery testing
- contributor UX
- OpenLLMWorks rebrand
- public GitHub repository
- public Runner release
- OpenLLMWorks.com
- GA4 baseline

### Weekend 17 - Direct Submission

Delivered:

```text
Runner
-> Canonical ZIP
-> Explicit Consent
-> HTTPS Submission
-> Private R2 Intake
-> Submission ID
```

Direct Submission reached production E2E PASS.

### Weekend 18 - Control Room & Publication Lifecycle

Delivered the operational and maintainer side of direct submission:

- safe server-side archive handling
- automatic canonical validation
- D1 operational state
- Control Room
- Cloudflare Access authentication
- submission review
- deliberate approval
- controlled canonical import
- publication verification
- Result-ID guardrails
- recovery workflow

The contributor-to-publication lifecycle is now proven.

### Inter-Sprint - Public Research & Discovery

Following Weekend 18, public-product work established:

- homepage refinement
- Benchmark Highlights
- Methodology
- The Works
- Works research backlog
- Works article registry
- dynamic sitemap
- route-specific SEO metadata
- first published Works Research Note

This work established the public explanation and research layer needed to make
the growing benchmark dataset more understandable.

---

## Weekend 19 - AMD / Vulkan Expansion

### Objective

Establish the first trustworthy non-NVIDIA accelerator path in OpenLLMWorks.

Initial target:

```text
AMD GPU
    |
    v
Vulkan-capable llama.cpp Runtime
    |
    v
OpenLLMWorks Runner
    |
    v
Protocol v1.0 Workload
    |
    v
Canonical Validation
    |
    v
Canonical Submission ZIP
    |
    v
Direct Submission
    |
    v
Control Room
    |
    v
Canonical Import
    |
    v
Publication
```

The first milestone is one valid AMD result, not comprehensive AMD support.

### Architecture Questions

Weekend 19 should determine:

1. where NVIDIA/CUDA assumptions currently exist in the Runner
2. how accelerator vendor and backend should be represented
3. whether current hardware evidence is sufficiently backend-neutral
4. what AMD/Vulkan evidence must be captured
5. how llama.cpp Vulkan runtime assets should be provisioned and verified
6. how runtime/backend selection should work
7. whether canonical validation currently assumes NVIDIA-specific evidence
8. whether the public hardware contract exposes sufficient backend provenance
9. whether CUDA and Vulkan results can share the same Protocol v1.0 result
   space without misleading users
10. what changes are implementation expansion versus protocol evolution

These questions should be answered from code and controlled testing rather than
assumption.

---

## Weekend 19 Guardrails

Do not change Protocol v1.0 merely to make AMD implementation easier.

Do not assume CUDA and Vulkan scores are directly comparable before validating
that interpretation.

Do not hide backend differences behind a generic GPU abstraction if those
differences matter to reproducibility.

Do not create an AMD-specific submission format.

Do not bypass the existing canonical validator or publication lifecycle.

Do not build broad multi-vendor abstractions before proving the smallest AMD
path.

Prefer:

```text
One AMD GPU
    |
    v
One Proven Vulkan Path
    |
    v
One Valid Submission
    |
    v
One Published Result
```

Then generalize from evidence.

---

## Current Constraints

Current public Runner support remains:

```text
Windows + NVIDIA + CUDA
```

Known expansion constraints include:

- AMD detection is not yet part of the public Runner
- Vulkan runtime provisioning is not yet part of the public Runner
- AMD hardware evidence requirements have not yet been defined
- backend provenance may require contract/schema review
- canonical validation may contain NVIDIA-specific assumptions
- public presentation currently reflects a predominantly NVIDIA dataset
- CUDA/Vulkan comparability has not yet been established
- Intel accelerator support remains future work
- dataset breadth remains early
- external contributor growth remains useful

These are now platform-expansion and evidence-quality concerns rather than
submission-lifecycle blockers.

---

## Immediate Next Steps

Weekend 19 should begin with architecture inspection rather than implementation.

```text
Audit Runner
    |
    v
Find NVIDIA / CUDA Assumptions
    |
    v
Audit Validator / Submission Contract
    |
    v
Define Backend Provenance Requirements
    |
    v
Define Smallest AMD / Vulkan Path
    |
    v
Implement
    |
    v
Bench Test
    |
    v
Canonical Validation
    |
    v
Production Lifecycle Test
```

The first coding change should follow the architecture audit.

---

## Current Checkpoint

```text
OpenLLMWorks brand                         ESTABLISHED
OpenLLMWorks.com                           LIVE
GitHub repository                          PUBLIC

OpenLLMWorks Runner                        PUBLIC BETA
Windows NVIDIA CUDA path                   PROVEN
Managed Protocol v1.0 assets               PROVEN
Canonical local validation                 PROVEN
Canonical submission ZIP                   PROVEN

Direct submission                          PRODUCTION PASS
Private R2 intake                          LIVE
Automatic server validation                LIVE
D1 operational state                       LIVE

Authenticated Control Room                 LIVE
Maintainer approval                        PROVEN
Controlled canonical import                PROVEN
Production publication verification        PROVEN
Published-submission recovery              PROVEN

External contributor validation            PROVEN
External result publication                PROVEN

Hardware Explorer                          LIVE
GPU Compare                                LIVE
Methodology                                LIVE
The Works                                  LIVE
First Works Research Note                  PUBLISHED
Dynamic sitemap                            LIVE
Search Console                             VERIFIED
GA4 baseline                               LIVE

Protocol v1.0                              FROZEN
Dataset growth                             ACTIVE / EARLY

AMD / Vulkan architecture                  NEXT
First AMD Runner benchmark                 UPCOMING
First validated AMD submission             UPCOMING
First published AMD result                 UPCOMING
Intel accelerator support                  FUTURE
```

Weekend 16 made OpenLLMWorks public.

Weekend 17 connected the Runner directly to OpenLLMWorks.

Weekend 18 completed the operational path from submission to controlled
publication.

The public research work established how OpenLLMWorks explains the evidence it
collects.

**Weekend 19 begins the move from a proven NVIDIA benchmark platform toward a
cross-vendor local AI hardware benchmark.**