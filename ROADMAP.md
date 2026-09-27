# OpenLLMWorks - Roadmap

## Mission

OpenLLMWorks exists to build an open, reproducible, and durable historical
record of local AI hardware performance.

The project is built around three ideas:

```text
Measure.
Understand.
Preserve.
```

**Measure** local AI hardware using standardized, reproducible workloads.

**Understand** what benchmark results mean through comparisons, research, and
evidence-based interpretation.

**Preserve** results, methodology, provenance, and historical hardware data so
performance can be understood over time.

---

## Product Direction

OpenLLMWorks is evolving through five connected stages:

```text
Measure
    |
    v
Expand
    |
    v
Explain
    |
    v
Translate
    |
    v
Apply
```

### Measure

Build a trustworthy benchmark foundation.

This includes:

- frozen benchmark workloads
- reproducible execution
- verified assets
- raw evidence
- canonical validation
- deterministic result identity
- controlled publication
- historical provenance

This foundation is operational.

### Expand

Increase the breadth of evidence.

This includes:

- more GPU generations
- more contributor systems
- AMD
- Intel
- workstation accelerators
- historical hardware
- eventually additional operating systems

This is the current major engineering phase.

### Explain

Help users understand what the measurements represent.

This includes:

- Methodology
- metric explainers
- The Works
- experiments
- findings
- research notes
- hardware-generation analysis

This phase has begun.

### Translate

Turn benchmark measurements into useful context without hiding the underlying
data.

Potential examples include:

- performance-per-dollar
- prompt-processing value
- token-generation value
- power efficiency
- generation comparisons
- architecture comparisons
- historical performance trends

This phase depends on sufficient validated data.

### Apply

Eventually help users use the evidence to make hardware decisions.

Potential examples include:

- workload-oriented hardware guidance
- strengths and tradeoffs
- accelerator selection
- dedicated local AI hardware configurations
- value-oriented comparisons

OpenLLMWorks should reach this stage through accumulated evidence rather than
premature recommendation logic.

---

# Current Position

OpenLLMWorks has crossed the initial public-product and production-operations
boundaries.

The project currently has:

```text
Public benchmark project                   LIVE
Public GitHub repository                   LIVE
OpenLLMWorks.com                           LIVE
Standalone Windows Runner                  LIVE / PUBLIC BETA

OLBD Protocol v1.0                         FROZEN
Windows + NVIDIA + CUDA path               PROVEN

Direct submission                          PROVEN
Authoritative server validation            PROVEN
Operational submission state               PROVEN
Authenticated Control Room                 PROVEN
Maintainer approval                        PROVEN
Controlled canonical import                PROVEN
Production publication verification        PROVEN
Publication recovery                       PROVEN

External contributor validation            PROVEN
External result publication                PROVEN

Hardware Explorer                          LIVE
GPU Compare                                LIVE
Leaderboards                               LIVE
Methodology                                LIVE
The Works                                  LIVE
Research Note publishing                   LIVE

Dataset growth                             ACTIVE / EARLY
AMD / Vulkan expansion                     CURRENT PHASE
Intel accelerator expansion                FUTURE
```

The core challenge is no longer proving that the benchmark can operate from
Runner execution through publication.

That lifecycle exists.

The next challenge is increasing the breadth and usefulness of the evidence
without weakening reproducibility or provenance.

---

# Architectural Principles

## 1. The Canonical Dataset Is the Historical Record

The Open LLM Benchmark Database is the canonical benchmark record.

Operational systems may support it, but they do not replace it.

```text
Contributor Systems
        |
        v
Submission Infrastructure
        |
        v
Operational State
        |
        v
Maintainer-Controlled Import
        |
        v
Canonical Database
        |
        v
Publisher
        |
        v
Public Website
```

Contributor systems must not receive direct canonical database write access.

---

## 2. Operational State and Canonical Data Remain Separate

Current infrastructure deliberately separates:

```text
R2
= submission artifacts and evidence

D1
= operational and control-plane state

Open LLM Benchmark Database
= canonical historical benchmark record
```

This separation should remain unless a future architecture provides a stronger
trust model.

---

## 3. Protocol Changes Require Methodology Reasons

OLBD Protocol v1.0 is frozen.

Do not change the benchmark protocol to solve:

- UI problems
- contributor onboarding
- transport problems
- website presentation
- submission automation
- accelerator-detection convenience
- backend implementation convenience

A future protocol version should exist only when benchmark methodology itself
needs to change.

---

## 4. Platform Expansion Is Not Automatically Protocol Evolution

Adding another accelerator vendor or execution backend does not automatically
require a new benchmark protocol.

However, backend differences must not be hidden if they materially affect:

- reproducibility
- workload behavior
- comparability
- evidence requirements
- result interpretation

Cross-vendor expansion must explicitly record enough provenance to understand
how a result was produced.

---

## 5. Evidence Comes Before Conclusions

The benchmark database records observations.

Research may investigate those observations.

OpenLLMWorks should not turn small datasets or unexplained performance
differences into architectural conclusions.

Preferred research flow:

```text
Validated Results
        |
        v
Observation
        |
        v
Research Question
        |
        v
Controlled Investigation
        |
        v
Finding
        |
        v
The Works
```

Unexpected results are useful when they create better questions.

---

# Completed Foundation

Detailed historical project state is preserved in:

```text
docs/STATUS_HISTORY.md
docs/ROADMAP_HISTORY.md
```

The live roadmap intentionally summarizes completed work rather than reproducing
the complete engineering history.

---

## Weekend 14 - Contributor Workflow and Runner Foundation

Weekend 14 proved the first complete benchmark lifecycle:

```text
Runner
    |
    v
Submission ZIP
    |
    v
Maintainer Validation
    |
    v
Canonical Import
    |
    v
Publisher
    |
    v
Website
```

This established that a benchmark produced outside the canonical database could
be validated, imported, and published without allowing contributor systems to
modify canonical data directly.

---

## Weekend 15 - Contributor Readiness

Weekend 15 hardened the benchmark workflow for use outside the development
environment.

Major themes included:

- Runner reliability
- canonical submission packaging
- contributor guidance
- benchmark-readiness messaging
- failure reporting
- maintainer import workflow
- regression testing
- standalone packaging groundwork

---

## Weekend 16 - Standalone Runner and Public Beta

Weekend 16 moved OpenLLMWorks from an internal benchmark project to a public
product.

Major milestones included:

- managed Protocol v1.0 assets
- verified asset provisioning
- clean-state execution
- corruption recovery
- interruption recovery
- offline failure handling
- contributor UX improvements
- standalone Windows executable
- OpenLLMWorks rebrand
- public GitHub repository
- public Runner beta
- OpenLLMWorks.com
- public website validation
- GA4 baseline analytics

Weekend 16 established the public benchmark surface.

---

## Weekend 17 - Direct Submission

Weekend 17 removed the manual GitHub handoff as a requirement for the primary
contributor path.

The architecture became:

```text
Runner
    |
    v
Canonical Validation
    |
    v
Canonical ZIP
    |
    v
Contributor Disclosure
    |
    v
Explicit Consent
    |
    v
HTTPS Submission
    |
    v
Private R2 Intake
    |
    v
Submission ID
```

Important principles established during this phase include:

- direct submission is opt-in
- the canonical ZIP remains the submission artifact
- upload failure does not invalidate a successful benchmark
- the local ZIP remains preserved
- receiving a package is not equivalent to accepting or publishing it
- contributor transport remains separated from canonical ingestion

Direct Submission reached an end-to-end production pass.

---

## Weekend 18 - Control Room and Publication Lifecycle

Weekend 18 completed the operational side of direct submission.

The production lifecycle expanded to:

```text
Contributor
    |
    v
Runner
    |
    v
Direct Submission
    |
    v
Private Intake
    |
    v
Authoritative Validation
    |
    v
Operational State
    |
    v
Authenticated Control Room
    |
    v
Maintainer Approval
    |
    v
Controlled Import
    |
    v
Publisher
    |
    v
Publication Verification
    |
    v
OpenLLMWorks.com
```

Major milestones included:

- safe submission archive handling
- authoritative server-side canonical validation
- GitHub Actions validation
- D1 operational state
- submission lifecycle history
- Control Room Admin API
- Control Room UI
- Cloudflare Access authentication
- maintainer review
- deliberate approval
- controlled canonical import
- publication verification
- canonical Result ID guardrails
- retry-safe verification
- published-submission recovery

The contributor-to-publication lifecycle is now operational.

---

# Public Product and Research Foundation

Following the production lifecycle work, OpenLLMWorks established a stronger
public explanation and research layer.

This work should be treated as product foundation rather than a separate
benchmark protocol phase.

---

## Homepage

The homepage now presents OpenLLMWorks around the positioning:

```text
Open benchmarks for local AI hardware.
```

Supporting idea:

```text
Real-world local AI performance across consumer and workstation hardware,
measured with a standardized and reproducible benchmark.
```

The homepage includes live Benchmark Highlights derived from published hardware
data.

---

## Methodology

The public Methodology surface explains:

- Protocol v1.0
- benchmark workload
- Qwen3-4B Q4_K_M
- llama.cpp runtime identity
- pp512
- tg128
- three-run methodology
- arithmetic averaging
- evidence
- provenance
- limitations
- future protocol philosophy

Core framing:

> OpenLLMWorks benchmarks hardware running local AI, not model intelligence.

---

## The Works

The Works is the research and editorial layer of OpenLLMWorks.

Positioning:

> Experiments, findings, and notes from the OpenLLMWorks lab.

Editorial principle:

> The benchmark database tells us what happened. The Works explores what it
> means.

Current content types:

- Experiment
- Finding
- Research Note
- Work in Progress

The publishing foundation includes:

- reusable article shell
- article registry
- visibility controls
- featured content
- route-specific metadata
- dynamic sitemap integration
- research backlog
- article-specific not-found experience

The first published Research Note explains:

```text
What do PP512 and TG128 actually mean?
```

The first planned hardware experiment asks:

```text
How far back can modern local AI go?
```

The Works should continue to grow from validated benchmark evidence.

---

# Current Phase - Weekend 19

## AMD / Vulkan Expansion

The highest-value engineering objective is now the first trustworthy
non-NVIDIA benchmark path.

Initial target hardware is an available AMD Radeon RX 560.

The objective is not comprehensive AMD support.

The objective is:

```text
One AMD GPU
    |
    v
One Proven Vulkan Backend
    |
    v
One Valid Benchmark
    |
    v
One Canonical Submission
    |
    v
One Production Publication
```

Once that path is proven, the implementation can be generalized.

---

## Weekend 19 Critical Path

```text
Architecture Audit
    |
    v
Identify NVIDIA / CUDA Assumptions
    |
    v
Define Backend Provenance
    |
    v
AMD Hardware Detection
    |
    v
Vulkan Runtime Provisioning
    |
    v
Runner Backend Selection
    |
    v
AMD Evidence Capture
    |
    v
Protocol v1.0 Benchmark
    |
    v
Canonical Validation
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

---

## Stage 1 - Architecture Audit

Before implementing AMD support, inspect the existing codebase for assumptions
about:

- NVIDIA hardware
- `nvidia-smi`
- CUDA
- CUDA-specific llama.cpp runtime assets
- GPU detection
- VRAM detection
- driver evidence
- submission schema
- canonical validation
- hardware normalization
- publisher output
- public hardware contract

The audit should identify which assumptions are:

```text
Runner-only
Validator-only
Publisher-only
Contract-level
Protocol-level
```

This distinction matters.

Implementation-specific assumptions should not be mistaken for protocol
requirements.

---

## Stage 2 - Backend Provenance

OpenLLMWorks needs to know how a benchmark was executed.

At minimum, cross-vendor work should determine whether canonical evidence needs
to represent:

- accelerator vendor
- accelerator model
- execution backend
- driver identity
- runtime identity
- backend-specific runtime version
- detected VRAM
- offload behavior
- backend initialization evidence

The exact schema should follow the architecture audit.

Do not add fields merely because they might someday be useful.

Record what is required for reproducibility and interpretation.

---

## Stage 3 - AMD Detection

The Runner needs a reliable AMD hardware detection path.

Initial implementation should focus on the available test system rather than
attempting to support every AMD configuration immediately.

Detection should produce sufficient evidence for:

- GPU identity
- VRAM
- driver/runtime environment
- selected backend

Detection failures should remain contributor-visible and diagnosable.

---

## Stage 4 - Vulkan Runtime

The Runner currently provisions a frozen benchmark environment for the proven
CUDA path.

AMD expansion should determine how a verified Vulkan-capable llama.cpp runtime
fits into the same managed-asset architecture.

Requirements should include:

- explicit runtime identity
- verified acquisition
- size/hash verification where appropriate
- deterministic provisioning
- corruption recovery
- contributor-visible status
- clear backend selection

The project should avoid silently substituting arbitrary locally installed
runtime binaries.

---

## Stage 5 - First AMD Benchmark

The first AMD test should answer a narrow question:

```text
Can the existing Protocol v1.0 workload execute successfully through the
OpenLLMWorks Runner using the Vulkan backend?
```

Success requires more than receiving benchmark numbers.

The test should preserve:

- three-run execution
- raw output
- hardware evidence
- runtime evidence
- pp512 parsing
- tg128 parsing
- canonical packaging
- deterministic identity
- validation

Unexpected performance is not itself a failure.

Missing provenance or non-reproducible execution is.

---

## Stage 6 - Canonical Validation

The existing validator should remain the source of truth for benchmark validity.

Weekend 19 should determine whether validation rules currently contain
NVIDIA-specific assumptions.

Any required changes should make validation backend-aware without creating a
second AMD submission format.

Preferred architecture:

```text
Canonical Submission Format
        |
        +-- NVIDIA / CUDA Evidence
        |
        +-- AMD / Vulkan Evidence
        |
        +-- Future Backend Evidence
```

rather than:

```text
NVIDIA Submission Format

AMD Submission Format

Intel Submission Format
```

One canonical model is preferable when the evidence supports it.

---

## Stage 7 - Production Lifecycle

A successful local AMD benchmark is not the final milestone.

The first AMD result should travel through the same production lifecycle as an
NVIDIA result:

```text
Runner
    |
    v
Canonical ZIP
    |
    v
Direct Submission
    |
    v
Server Validation
    |
    v
Control Room
    |
    v
Maintainer Approval
    |
    v
Controlled Import
    |
    v
Publisher
    |
    v
Publication Verification
    |
    v
OpenLLMWorks.com
```

This proves that accelerator expansion belongs to the existing OpenLLMWorks
system rather than a parallel experimental pipeline.

---

# Cross-Vendor Comparability

Cross-vendor support creates a new research question:

```text
What does it mean to compare results produced through different execution
backends?
```

OpenLLMWorks should not assume that CUDA and Vulkan are interchangeable merely
because they execute the same model and benchmark workload.

Potential variables include:

- backend implementation
- kernel behavior
- memory management
- offload behavior
- driver stack
- runtime compilation options
- architecture-specific optimizations

The immediate requirement is transparency.

Results should expose enough provenance that future research can investigate
backend effects.

If controlled testing demonstrates that additional normalization or protocol
separation is necessary, that decision should be evidence-driven.

---

# Dataset Growth

The benchmark becomes more useful as validated coverage increases.

Dataset growth should proceed along several dimensions.

---

## NVIDIA Coverage

Continue adding useful NVIDIA coverage when inexpensive or strategically
valuable hardware becomes available.

High-value gaps include examples such as:

- additional Maxwell
- additional Pascal
- additional Turing
- RTX 20-series
- historical workstation GPUs
- repeated models across different host systems

Dataset growth should not become a requirement to fill every SKU.

Coverage should serve useful comparisons and research questions.

---

## AMD Coverage

After the first AMD/Vulkan result is proven, expand deliberately.

Potential future AMD coverage includes:

- older Polaris hardware
- Radeon Pro hardware
- RDNA generations
- additional VRAM configurations
- multiple host systems

The first goal is backend proof.

Breadth comes afterward.

---

## Intel Coverage

Intel accelerator support remains a future platform-expansion track.

Potential hardware includes Intel Arc discrete GPUs.

Intel work should benefit from the backend abstraction and provenance lessons
learned during AMD expansion.

Do not build Intel support simultaneously with the first AMD implementation
unless shared architecture work clearly requires it.

---

## Contributor Growth

External contributors are essential to making OpenLLMWorks more than a private
hardware lab.

Contributor growth should focus on:

- clear Runner onboarding
- trustworthy binaries
- understandable consent
- recoverable failures
- visible submission identity
- predictable publication lifecycle
- useful recognition
- low-friction contribution

Observed contributor behavior should drive UX improvements.

Avoid speculative onboarding complexity.

---

# Research Roadmap

Research should grow alongside the dataset rather than ahead of it.

The internal research backlog is the bridge between benchmark observations and
public conclusions.

```text
Benchmark Results
        |
        v
Research Backlog
        |
        v
Experiment
        |
        v
Validated Finding
        |
        v
The Works
```

---

## Foundational Explainability

Near-term educational content should help users understand the benchmark itself.

Topics include:

- what pp512 measures
- what tg128 measures
- why both metrics matter
- how the benchmark workload is constructed
- why three runs are used
- what benchmark limitations mean
- what hardware evidence is collected

This content improves interpretation without requiring speculative hardware
recommendations.

---

## Hardware Research

As coverage grows, useful investigations may include:

- historical GPU viability
- Pascal vs Turing behavior
- prompt processing versus generation behavior
- VRAM constraints
- architecture transitions
- workstation versus consumer hardware
- host-system effects
- backend effects
- cross-vendor behavior

Research should distinguish:

```text
Observation
Hypothesis
Controlled Evidence
Finding
```

Do not collapse those stages.

---

## Content Engine

A future Content Engine may assist with drafting research and data-driven
articles.

Principle:

```text
OpenLLMWorks supplies validated facts.
AI may assist with narrative.
Human approval controls publication.
```

The Content Engine should not become an autonomous source of benchmark claims.

Potential future capabilities include:

- structured article drafts
- benchmark-data references
- trend summaries
- research backlog assistance
- SEO metadata generation
- publication preparation

This is not a Weekend 19 priority.

---

# Translation Roadmap

Once dataset breadth is sufficient, OpenLLMWorks can translate benchmark
measurements into additional useful dimensions.

These should generally be derived from canonical benchmark results rather than
stored as competing benchmark truth.

---

## Performance per Dollar

Potential future analytics include:

```text
pp512 per dollar
tg128 per dollar
```

Prompt-processing value and token-generation value should remain separate.

A single combined value score risks hiding meaningful workload differences.

Initial pricing may be manually curated.

Later pricing integrations may be considered if reliable sources become
available.

Price data must remain distinguishable from canonical benchmark measurements
because prices change over time.

---

## Power and Efficiency

Potential future analysis includes:

```text
pp512 per watt
tg128 per watt
```

However, the evidence source matters.

Manufacturer TDP or board-power specifications must not be presented as
measured benchmark power consumption.

OpenLLMWorks should distinguish clearly between:

```text
Specified Power
Estimated Power
Measured Power
```

True measured efficiency requires appropriate measurement methodology.

---

## Historical Trends

The dataset may eventually support questions such as:

- how local AI performance changed across GPU generations
- how much generation speed improved over time
- how prompt-processing behavior changed
- how VRAM capacity evolved
- when older hardware stopped being practical for particular workloads
- how workstation hardware compares with consumer equivalents

Historical analysis is a core long-term opportunity because OpenLLMWorks
preserves benchmark provenance rather than only current rankings.

---

# Application Roadmap

OpenLLMWorks may eventually help users apply benchmark evidence to hardware
choices.

This should remain downstream of measurement and interpretation.

---

## Strengths and Tradeoffs

Future hardware pages may explain observed characteristics such as:

- stronger prompt processing
- stronger token generation
- VRAM capacity
- efficiency
- value
- historical significance

These descriptions should be evidence-based.

Avoid reducing hardware to generic:

```text
Good
Bad
Best
Worst
```

Different benchmark dimensions may favor different hardware.

---

## Workload Guidance

Future guidance may connect measured behavior to practical local AI use cases.

This requires validation.

Do not infer workload suitability solely from one benchmark metric without
evidence that the interpretation is useful.

Potential future research may investigate:

- interactive chat
- long-prompt processing
- batch processing
- coding workloads
- summarization
- agentic workloads
- dedicated inference systems

Guidance should follow research.

---

## Dedicated Accelerator Systems

OpenLLMWorks may investigate systems where a discrete GPU is dedicated to local
AI while display duties remain on integrated or secondary graphics.

Potential research questions include:

- dedicated accelerator behavior
- host-resource requirements
- power characteristics
- compact inference systems
- low-profile accelerators
- workstation cards
- external accelerator configurations

These are useful experimental tracks, not requirements for the core benchmark.

---

# Public Product Roadmap

The public site should continue improving, but website polish should not displace
high-value benchmark expansion.

---

## Hardware Explorer and Comparison

Potential improvements include:

- richer filtering
- backend visibility
- vendor filtering
- architecture filtering
- clearer metric explanations
- historical context
- contributor recognition
- research links

Features should be driven by dataset breadth and actual user needs.

---

## Benchmark Highlights

Benchmark Highlights should continue to derive from published canonical data.

Future highlights may include:

- generation comparisons
- vendor comparisons
- historical hardware
- efficiency
- value

Avoid editorializing rankings before the underlying metric is clearly defined.

---

## The Works Integration

Hardware and research should become increasingly connected.

Potential relationships include:

```text
Hardware Result
    |
    +--> Related Experiment
    |
    +--> Related Finding
    |
    +--> Methodology Explanation
```

and:

```text
The Works Article
    |
    +--> Referenced Hardware
    |
    +--> Referenced Results
    |
    +--> Live Benchmark Data
```

The long-term goal is a research layer that remains connected to canonical data
rather than copying benchmark values into static prose unnecessarily.

---

## Search and Discovery

Current foundations include:

- route-specific metadata
- canonical URLs
- Open Graph metadata
- robots.txt
- dynamic sitemap
- Search Console
- GA4

Future SEO work should primarily follow useful public content and dataset growth.

Do not create large quantities of low-value generated pages merely to increase
indexed URL count.

---

# Commerce and Sustainability

OpenLLMWorks may eventually support revenue-generating features.

Measurement integrity must remain separate from commercial relationships.

Potential models include:

- advertising
- affiliate hardware links
- retailer integrations
- sponsorships
- partnerships
- data/API products
- research partnerships

Commercial relationships must not alter benchmark results, validation rules, or
editorial conclusions.

A useful separation is:

```text
Measurement
    |
    v
Canonical Evidence
    |
    v
Interpretation
    |
    v
Optional Commerce
```

not:

```text
Commerce
    |
    v
Benchmark Conclusion
```

Trust in the benchmark is more valuable than short-term monetization.

---

# Future Protocol Evolution

Protocol v1.0 should remain frozen while it continues serving its intended
historical role.

Future benchmark needs may eventually justify a new protocol.

Possible reasons include:

- materially different model workloads
- new context-length requirements
- new inference patterns
- new benchmark metrics
- major runtime changes
- methodology improvements
- hardware classes that cannot be represented responsibly under v1.0

A future protocol should coexist with historical Protocol v1.0 results.

Do not rewrite historical results into a new methodology.

Preferred model:

```text
Protocol v1.0
    |
    +-- Historical Results
    |
    +-- Continued Compatible Results

Protocol v2.0
    |
    +-- New Workload
    |
    +-- New Results
```

Cross-protocol comparisons should clearly identify methodological differences.

---

# Additional Platform Expansion

AMD/Vulkan is the immediate expansion track, but it is not the endpoint.

Future platform work may include:

- Intel Arc
- additional accelerator APIs
- Linux
- additional Windows backends
- Apple Silicon
- integrated GPUs
- NPUs or dedicated AI accelerators

Each platform should earn support through a reproducible implementation and
clear evidence model.

Avoid claiming universal accelerator support before each path is actually
validated.

---

# Maintainer and Operational Improvements

The production lifecycle is proven, but operational improvements remain useful.

Potential future work includes:

- richer submission detail
- clearer validation failure reporting
- contributor-facing submission status
- duplicate handling improvements
- operational metrics
- audit visibility
- safer batch operations
- contributor recognition
- administrative quality-of-life improvements

These improvements should be incremental.

The Control Room should remain an operational tool, not become a separate
product that consumes engineering attention without improving benchmark
operations.

---

# Near-Term Priority Order

The current priority order is:

```text
1. Preserve Protocol v1.0 stability

2. Audit NVIDIA / CUDA assumptions

3. Define backend provenance requirements

4. Prove AMD / Vulkan Runner execution

5. Validate the first AMD canonical submission

6. Publish the first AMD result through the production lifecycle

7. Generalize the cross-vendor Runner architecture

8. Expand AMD coverage

9. Continue strategically useful NVIDIA dataset growth

10. Grow external contributor participation

11. Publish evidence-driven research through The Works

12. Begin translation layers as dataset breadth supports them
```

Intel and additional platforms follow the architectural lessons from AMD rather
than competing with the first cross-vendor implementation.

---

# Weekend 19 Acceptance Gate

Weekend 19 should be considered successful when OpenLLMWorks can demonstrate a
trustworthy AMD/Vulkan path without weakening Protocol v1.0 guarantees.

Ideal acceptance path:

```text
AMD Test System
    |
    v
OpenLLMWorks Runner
    |
    v
AMD Detection
    |
    v
Verified Vulkan Runtime
    |
    v
Protocol v1.0 Workload
    |
    v
Three Benchmark Runs
    |
    v
Raw Evidence
    |
    v
Canonical Validation
    |
    v
Canonical ZIP
    |
    v
Direct Submission
    |
    v
Server Validation
    |
    v
Control Room Approval
    |
    v
Canonical Import
    |
    v
Publisher
    |
    v
Publication Verification
    |
    v
OpenLLMWorks.com
```

The milestone is:

```text
FIRST VALIDATED AND PUBLISHED AMD / VULKAN RESULT
```

If Weekend 19 instead reveals that backend differences require additional
methodology or contract work, documenting that evidence is also a valid outcome.

Do not force publication merely to satisfy the sprint label.

---

# Beyond Weekend 19

After the first AMD path is proven:

```text
First AMD Result
    |
    v
Cross-Vendor Architecture Hardening
    |
    v
Additional AMD Results
    |
    v
Cross-Backend Research
    |
    v
Dataset Growth
    |
    v
Intel Expansion
```

In parallel:

```text
Dataset Growth
    |
    v
Research Backlog
    |
    v
The Works
    |
    v
Interpretation
    |
    v
Value / Efficiency / Historical Analytics
    |
    v
Evidence-Based Hardware Guidance
```

These tracks reinforce one another.

More validated hardware creates better research.

Better research makes benchmark data more understandable.

Better interpretation makes the dataset more useful.

Greater usefulness attracts contributors and creates more data.

---

# Long-Term Product Shape

The long-term OpenLLMWorks ecosystem may look like:

```text
                    OpenLLMWorks
                         |
        +----------------+----------------+
        |                |                |
        v                v                v
      Measure          Explain          Apply
        |                |                |
        v                v                v
      Runner          The Works        Guidance
        |                |                |
        v                v                v
     Protocol        Research         Comparisons
        |                |                |
        v                v                v
   Validation        Findings          Value
        |                |                |
        +--------+-------+-------+--------+
                 |
                 v
        Canonical Benchmark Data
                 |
                 v
        Historical Local AI Record
```

The canonical dataset remains the center.

The Runner creates evidence.

The publication lifecycle protects evidence.

The website exposes evidence.

The Works explains evidence.

Future analytics translate evidence.

Future guidance applies evidence.

---

# Project Guardrails

As OpenLLMWorks grows:

1. **Do not sacrifice reproducibility for feature velocity.**

2. **Do not change frozen protocols for presentation problems.**

3. **Do not allow contributor systems to write directly to canonical data.**

4. **Do not confuse operational state with historical benchmark truth.**

5. **Do not hide backend differences that matter to reproducibility.**

6. **Do not claim comparability that has not been validated.**

7. **Do not turn observations into causal claims without evidence.**

8. **Do not publish AI-generated research without human review.**

9. **Do not let commerce influence measurement or conclusions.**

10. **Do not build abstractions substantially ahead of validated use cases.**

11. **Prefer one proven path before broad generalization.**

12. **Preserve historical results even as future protocols evolve.**

---

# Current Critical Path

```text
PUBLIC BENCHMARK FOUNDATION
        COMPLETE
            |
            v
DIRECT SUBMISSION
        COMPLETE
            |
            v
CONTROL ROOM + PUBLICATION LIFECYCLE
        COMPLETE
            |
            v
PUBLIC RESEARCH FOUNDATION
        ESTABLISHED
            |
            v
AMD / VULKAN EXPANSION
        CURRENT
            |
            v
FIRST PUBLISHED AMD RESULT
            |
            v
CROSS-VENDOR DATASET GROWTH
            |
            v
EVIDENCE-DRIVEN RESEARCH
            |
            v
TRANSLATION LAYERS
            |
            v
HARDWARE GUIDANCE
```

---

# Current Roadmap Summary

```text
Protocol v1.0                              FROZEN

Windows NVIDIA CUDA                        PROVEN
Standalone Runner                          PROVEN
Managed Assets                             PROVEN
Canonical Validation                       PROVEN

Direct Submission                          PROVEN
Server-Side Validation                     PROVEN
D1 Operational State                       PROVEN
Control Room                               PROVEN
Maintainer Approval                        PROVEN
Controlled Import                          PROVEN
Publication Verification                   PROVEN
Recovery                                   PROVEN

External Contributor Validation            PROVEN
External Result Publication                PROVEN

OpenLLMWorks.com                           LIVE
Hardware Explorer                          LIVE
GPU Compare                                LIVE
Leaderboards                               LIVE
Methodology                                LIVE
The Works                                  LIVE
Research Publishing                        LIVE
Search / Sitemap Foundation                LIVE

Dataset Growth                             ACTIVE / EARLY

AMD / Vulkan Architecture                  CURRENT
First AMD Benchmark                        NEXT
First Validated AMD Submission             UPCOMING
First Published AMD Result                 UPCOMING
Cross-Vendor Dataset Growth                UPCOMING

Additional NVIDIA Coverage                 ACTIVE / OPPORTUNISTIC
Contributor Growth                         ACTIVE
The Works Research                         ACTIVE

Value Analytics                            FUTURE
Power / Efficiency                         FUTURE
Hardware Guidance                          FUTURE
Intel Accelerator Support                  FUTURE
Additional Operating Systems               FUTURE
Future Protocol Versions                   FUTURE
```

---

## Current Direction

OpenLLMWorks has moved beyond proving that a local AI benchmark can be run,
submitted, validated, reviewed, imported, and published.

That system now exists.

The next phase is about making the historical record broader and more useful:

```text
Measure
    |
    v
Expand
    |
    v
Explain
    |
    v
Translate
    |
    v
Apply
```

Weekend 19 begins with the first major step in **Expand**:

**prove that OpenLLMWorks can support AMD/Vulkan with the same discipline that
established the NVIDIA/CUDA path.**