# OpenLLMWorks - Project Status

## Weekend 17 - Direct Submission MVP

**Focus:** Direct contributor submission, production ingestion, Runner transport, and end-to-end validation  
**Status:** Direct Submission MVP / Production E2E PASS / Clean Checkpoint

---

## Current Objective

Move OpenLLMWorks from a publicly available benchmark with a GitHub-based
submission handoff into a community benchmark that can accept validated
contributor packages directly from the standalone Runner.

Weekend 16 established the public product, standalone Windows NVIDIA Runner,
managed Protocol v1.0 assets, recovery behavior, contributor UX, public GitHub
repository, OpenLLMWorks.com, and analytics baseline.

Weekend 17 removes one of the largest remaining contributor barriers:

```text
Run benchmark
    |
    v
Create validated canonical ZIP
    |
    v
Review submission disclosure
    |
    v
Upload to OpenLLMWorks? [Y/N]
    |
    +--> N --> Preserve local ZIP / manual fallback
    |
    +--> Y --> HTTPS direct submission
```

The direct-submission architecture is now proven end to end in production.

A fresh standalone Runner build was executed on Bench-001, completed the full
OLBD Protocol v1.0 benchmark, generated and locally validated the canonical
submission package, received explicit contributor consent, uploaded the ZIP to
the production OpenLLMWorks submission API, returned a traceable submission ID,
and preserved the local ZIP.

The matching object was independently confirmed in production private R2
storage.

The next major engineering gate is therefore no longer basic Runner transport.

It is:

```text
DIRECT SUBMISSION HARDENING
```

This includes authoritative server-side validation, maintainer intake,
duplicate/error handling, security and abuse controls, and publication
integration.

External contributor validation remains an important Public Beta gate.

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
    |       +-- OLBD Protocol v1.0
    |
    +-- Hardware Results / Comparisons
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
**Development version:** `0.3.0-dev3`  
**First public beta release:** `v0.3.0-beta.1`  
**Current platform:** Windows  
**Current accelerator:** NVIDIA  
**Benchmark Protocol:** OLBD Protocol v1.0

The current contributor-side workflow is:

```text
Start OpenLLMWorks Runner
    |
    v
Detect NVIDIA Environment
    |
    v
Verify / Provision Managed Protocol Assets
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
Canonical Local Validation
    |
    v
Create Canonical Submission ZIP
    |
    v
Show Submission Disclosure
    |
    v
Upload to OpenLLMWorks? [Y/N]
    |
    +--> N --> Preserve ZIP / manual submission available
    |
    +--> Y
             |
             v
         HTTPS Upload
             |
             v
         Submission ID
```

The Runner remains intentionally isolated from the canonical Open LLM
Benchmark Database.

Direct submission does not grant contributor systems write access to the
canonical database.

---

## Direct Submission Architecture

Weekend 17 introduced a direct submission path while preserving the existing
canonical submission format.

The Runner does not create a second submission format.

It uploads the same canonical ZIP that is already generated and locally
validated by the existing benchmark workflow.

Current architecture:

```text
Contributor System
    |
    v
OpenLLMWorks-Runner.exe
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
Contributor Disclosure
    |
    v
Upload to OpenLLMWorks? [Y/N]
    |
    +--> N
    |     |
    |     v
    |   Preserve Local ZIP
    |     |
    |     v
    |   Manual Submission Available
    |
    +--> Y
          |
          v
https://api.openllmworks.com/v1/submissions
          |
          v
openllmworks-submissions Worker
          |
          v
Private R2 Bucket
openllmworks-submissions
          |
          v
incoming/sub_<uuid>.zip
          |
          v
Status: received
```

The production API is intentionally an ingestion boundary rather than a direct
database-write endpoint.

Current response semantics use:

```text
received
```

rather than:

```text
accepted
```

This distinction is deliberate.

A package being successfully received does not yet mean it has passed
authoritative server-side validation, been imported into the canonical
database, or been published.

Future submission lifecycle states may include:

```text
received
validated
rejected
imported
published
```

---

## Contributor Consent and Disclosure

Direct submission is explicitly opt-in.

The Runner does not automatically upload benchmark results.

After canonical ZIP creation, the contributor is shown submission information
and asked:

```text
Upload this benchmark to OpenLLMWorks? [Y/N]
```

If the contributor selects `N`:

- the benchmark remains successful
- the canonical ZIP remains local
- no direct upload occurs
- manual submission remains available

If the contributor selects `Y`:

- the existing canonical ZIP is uploaded over HTTPS
- the production service stores the package in private incoming storage
- a traceable submission ID is returned
- the local ZIP remains preserved

Cancellation during the consent stage is handled deliberately.

Upload failure also does not convert a successful benchmark into a failed
benchmark. The local canonical package remains available for retry or manual
submission.

---

## Direct Submission Client

Runner-side direct submission transport is implemented in:

```text
runner/submission_client.py
```

Current production endpoint:

```text
https://api.openllmworks.com/v1/submissions
```

Current transport:

```text
HTTPS POST
Content-Type: application/zip
```

The client uses Python standard-library HTTP functionality to avoid introducing
an additional runtime dependency solely for submission transport.

Current client behavior includes:

- local ZIP existence checks
- non-empty package checks
- explicit contributor consent
- HTTPS upload
- upload timeout handling
- HTTP error handling
- network error handling
- malformed response handling
- expected HTTP 201 handling
- expected `status = received` verification
- submission ID verification
- preservation of the local ZIP
- graceful fallback when upload fails

A successful production response returns a submission identifier in the form:

```text
sub_<uuid>
```

---

## Submission Ingestion Worker

Direct submission ingestion is handled by a dedicated Cloudflare Worker
separate from the public website Worker.

Worker:

```text
openllmworks-submissions
```

Production API hostname:

```text
api.openllmworks.com
```

Current endpoint:

```text
POST /v1/submissions
```

The submission Worker currently:

1. accepts the supported submission endpoint
2. rejects unsupported HTTP methods
3. requires `application/zip`
4. generates a unique `sub_<uuid>` submission ID
5. stores the uploaded body in private incoming R2 storage
6. returns HTTP 201
7. reports submission status as `received`

Validated production behavior includes:

```text
GET submission endpoint                   HTTP 405
Wrong Content-Type                        HTTP 415
Valid ZIP POST                            HTTP 201
Submission ID returned                    PASS
Status = received                         PASS
Matching production R2 object             PASS
```

The Worker does not currently perform authoritative OLBD canonical validation.

That is a deliberate Stage 1 MVP boundary.

---

## Private Submission Storage

Incoming direct submissions are stored in Cloudflare R2.

Bucket:

```text
openllmworks-submissions
```

Incoming object convention:

```text
incoming/sub_<uuid>.zip
```

The bucket is an intake/quarantine boundary.

Receiving a package into this bucket does not publish it and does not directly
modify the canonical Open LLM Benchmark Database.

This preserves the architectural separation:

```text
Contributor Upload
    !=
Canonical Database Import
```

Maintainer-controlled validation and import remain required until a future
trusted server-side workflow deliberately automates additional stages.

---

## Weekend 17 Production E2E Acceptance

Weekend 17 concluded the Direct Submission MVP with a real production
acceptance test using Bench-001.

The test used a freshly rebuilt standalone:

```text
OpenLLMWorks-Runner.exe
```

The complete acceptance path was:

```text
OpenLLMWorks-Runner.exe
        |
        v
Hardware Detection
        |
        v
Managed Protocol Assets
        |
        v
Three Benchmark Runs
        |
        v
Canonical Local Validation
        |
        v
Canonical Submission ZIP
        |
        v
Contributor Disclosure
        |
        v
Y Consent
        |
        v
Production HTTPS Upload
        |
        v
api.openllmworks.com
        |
        v
openllmworks-submissions Worker
        |
        v
Private Production R2
        |
        v
Submission ID Returned
```

Acceptance matrix:

```text
Hardware detection                        PASS
Managed assets                            PASS
Three benchmark runs                      PASS
Canonical validation                      PASS
Submission ZIP creation                   PASS
Contributor disclosure                    PASS
Explicit Y consent                        PASS
HTTPS upload                              PASS
Production API                            PASS
Submission Worker                         PASS
Private R2 ingestion                      PASS
Submission ID returned                    PASS
Matching R2 ZIP verified                  PASS
Local ZIP preserved                       PASS
```

This establishes:

```text
WEEKEND 17 - DIRECT SUBMISSION MVP
END-TO-END PRODUCTION PASS
```

---

## Manual Submission Fallback

The GitHub submission workflow remains useful as a fallback and compatibility
path.

Current relationship:

```text
Primary path:
Runner -> Y -> OpenLLMWorks Submission API

Fallback path:
Runner -> Local Canonical ZIP -> Manual GitHub Submission
```

The fallback remains valuable when contributors decline direct upload, network
connectivity fails, the submission service is temporarily unavailable, or a
manual recovery path is useful during beta.

Direct submission therefore improves convenience without making benchmark
completion dependent on the ingestion service.

---

## First Public Runner Release

The first publicly distributed OpenLLMWorks Runner is:

```text
OpenLLMWorks Runner v0.3.0-beta.1
```

Distribution location:

```text
GitHub Releases
```

Public release:

```text
https://github.com/namphan813/OpenLLMWorks/releases/tag/v0.3.0-beta.1
```

The public release was treated as a beta artifact rather than an implied
production-final binary.

The current development Runner has advanced beyond the original beta.1
artifact through the Weekend 17 direct-submission work.

A future public Runner release should incorporate the proven direct-submission
client after the desired beta checkpoint and release validation are complete.

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
- direct submission client code

Large Benchmark Protocol assets are intentionally not embedded in the
executable.

The Runner acquires and verifies those assets separately.

Weekend 16 confirmed that the standalone executable can complete the benchmark
workflow without requiring the development repository.

Weekend 17 confirmed that a freshly built standalone executable can also
complete the production direct-submission path.

Python and Git are not contributor requirements.

---

## Managed Protocol Storage and Rebrand Compatibility

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

This avoids forcing existing contributors to redownload frozen multi-gigabyte
assets or destructively migrating a known-good managed environment.

The legacy directory is compatibility infrastructure, not the current public
product identity.

---

## Asset Manifest and Provisioning

Runner asset acquisition is controlled by:

```text
runner/assets.json
```

**Manifest schema:** `1.1`

Current frozen model:

```text
Qwen3-4B-Q4_K_M.gguf
```

Current frozen model size:

```text
2,497,280,256 bytes
```

Asset-management logic is implemented in:

```text
runner/provisioning.py
```

The Runner verifies frozen assets using exact size and SHA-256 before they are
accepted into the managed Protocol v1.0 environment.

Current provisioning responsibilities include:

- managed protocol path resolution
- asset manifest loading
- local asset inspection
- size validation
- SHA-256 validation
- verified file download
- contributor-visible artifact status
- download-progress milestones
- verified local artifact reuse
- upstream runtime-source acquisition
- staging and extraction
- required-file validation
- deterministic runtime assembly
- safe replacement of managed runtime assets
- cleanup of temporary staging data

The earlier custom runtime archive architecture has been retired.

---

## Preserved Benchmark Guarantees

The standalone, managed-asset, recovery, UX, rebrand, release, website, and
direct-submission work does not change the core Protocol v1.0 guarantees.

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

Direct submission changes transport and contributor convenience.

It does not change benchmark methodology.

It also does not currently replace authoritative maintainer-side validation.

---

## Website and Public Infrastructure

Production website:

```text
https://openllmworks.com
```

Additional public hostname:

```text
https://www.openllmworks.com
```

Production submission API:

```text
https://api.openllmworks.com
```

The website and submission API are served by separate Cloudflare Workers.

Current public homepage identity includes:

```text
OpenLLMWorks

PUBLIC BETA

Building the historical record
of local AI performance.

Measure. Understand. Preserve.
```

The primary contributor CTA remains:

```text
Run Your First Benchmark
```

Website messaging and the contributor funnel may be refined as direct
submission moves into a public Runner release.

A private-browser public smoke test previously validated primary navigation,
hardware pages, GPU comparison interaction, GitHub destinations, and the
benchmark path.

---

## Analytics Baseline

Google Analytics 4 baseline collection is active on the production website.

GA4 property:

```text
OpenLLMWorks Website
```

Measurement ID:

```text
G-K47WJHVSNY
```

Collection was verified through GA4 Realtime.

The current analytics strategy remains intentionally minimal:

```text
Collect historical baseline data now.
Transform and analyze it later.
```

Potential future high-value events include:

```text
Runner download / release clicks
GitHub visits
Direct submission attempts
Direct submission success
Hardware comparison usage
Contributor conversion
```

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

### Weekend 16 - Managed Assets and Recovery

The Runner moved to managed, self-provisioning Protocol v1.0 assets and was
exercised through clean-state, reuse, corruption, interruption, offline, and
recovery scenarios.

Validation included:

```text
Clean-state first run                    PASS
Existing asset reuse                     PASS
Corrupt managed model recovery           PASS
Forced model re-download                 PASS
Managed runtime recovery                 PASS
User-aborted benchmark                   PASS
Offline provisioning failure             PASS
Connectivity-restored recovery           PASS
Final healthy regression                 PASS
```

### Weekend 16 - Contributor UX

Contributor-facing lifecycle improvements included:

- packaged completion pause
- workspace and ZIP visibility
- deliberate Ctrl+C handling
- retained partial-workspace messaging
- safe-rerun guidance
- failure visibility
- artifact verification status
- provisioning progress

### Weekend 16 - Product / Name Gate

Major work included:

- competitive and naming review
- selection of **OpenLLMWorks** as the public project identity
- preservation of **Open LLM Benchmark Database / OLBD Protocol v1.0**
- GitHub repository rename
- acquisition of `OpenLLMWorks.com`
- project and Runner rebrand
- backward-compatible managed-asset root resolution
- separation of new results from legacy asset storage
- repository-wide rebrand reconciliation

### Weekend 16 - Public Beta Launch

Major work included:

- public GitHub repository
- first public Runner beta release
- public release artifact verification
- production website build and deployment
- OpenLLMWorks.com activation
- HTTPS validation
- `www.openllmworks.com` activation
- public visitor smoke testing
- GA4 baseline installation and verification

Weekend 16 crossed the Public Beta launch boundary.

### Weekend 17 - Direct Submission MVP

Weekend 17 removed the GitHub Issue workflow as a requirement for the primary
future contributor submission experience.

Major work included:

- direct-submission architecture and design principles
- `docs/DIRECT_SUBMISSION.md`
- contributor disclosure and explicit `[Y/N]` consent
- `runner/submission_client.py`
- direct HTTPS transport using the existing canonical ZIP
- dedicated Cloudflare submission Worker
- private R2 incoming storage
- production `api.openllmworks.com` hostname
- unique `sub_<uuid>` submission identity
- `received` status semantics
- upload failure fallback
- local ZIP preservation
- production API method and media-type testing
- direct transport testing
- contributor-facing consent/upload testing
- fresh standalone Runner rebuild
- Bench-001 full benchmark acceptance test
- production R2 verification

Final acceptance:

```text
Runner -> Benchmark -> Canonical Validation -> ZIP
       -> Disclosure -> Y
       -> Production HTTPS API
       -> Private Incoming R2
       -> Submission ID

PASS
```

---

## Current Contributor Handoff

The current preferred contributor lifecycle is:

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
Hardware Evidence + Three Benchmark Runs
    |
    v
Canonical Local Validation
    |
    v
Canonical Submission ZIP
    |
    v
Contributor Disclosure
    |
    v
Upload to OpenLLMWorks? [Y/N]
    |
    +--> N --> Preserve ZIP / manual fallback
    |
    +--> Y
             |
             v
         HTTPS Submission API
             |
             v
         Private Incoming Storage
             |
             v
         Submission ID
             |
             v
         Maintainer Validation
             |
             v
         Controlled Canonical Import
             |
             v
         Open LLM Benchmark Database
             |
             v
         Publisher
             |
             v
         OpenLLMWorks.com
```

Contributor execution and canonical ingestion remain deliberately separated.

The direct transport layer is now proven.

---

## Current Constraints

Current primary target:

```text
Windows + NVIDIA
```

Current constraints and open questions include:

- direct submission is proven internally but has not yet been validated by an
  unrelated external contributor
- authoritative server-side canonical validation is not yet implemented
- incoming submissions still require maintainer-controlled processing
- duplicate/idempotency handling needs hardening
- malformed ZIP and hostile-input handling needs hardening
- submission size and abuse controls need deliberate review
- rate limiting is not yet a mature submission policy
- submission status visibility is minimal
- the currently published beta.1 Runner predates the Weekend 17 direct
  submission implementation
- unsigned Windows executable may trigger SmartScreen or trust friction
- contributor documentation needs real-world external validation
- broader NVIDIA GPU coverage remains valuable
- AMD support is not yet part of the public Runner
- Intel accelerator support is not yet part of the public Runner
- public dataset breadth remains early
- SEO and public discovery remain early

These are now primarily submission-hardening, beta-learning,
platform-expansion, dataset-growth, and public-discovery concerns.

---

## Current Roadmap

```text
Managed Assets                              COMPLETE
    |
    v
Pristine / Recovery Validation              COMPLETE
    |
    v
Contributor UX / Failure Recovery           COMPLETE
    |
    v
Product / Name Gate                         COMPLETE
    |
    v
OpenLLMWorks Rebrand                        COMPLETE
    |
    v
Public GitHub + Runner Release              COMPLETE
    |
    v
OpenLLMWorks.com                            LIVE
    |
    v
Public Visitor Smoke Test                   PASS
    |
    v
Analytics Baseline                         LIVE
    |
    v
OPENLLMWORKS PUBLIC BETA                    LIVE
    |
    v
Direct Submission MVP                      E2E PASS
    |
    v
Submission Hardening                       NEXT
    |
    +--> Server-Side Validation
    +--> Maintainer Intake
    +--> Duplicate / Error Handling
    +--> Security / Abuse Controls
    +--> Publication Integration
    |
    v
External Contributor Validation            UPCOMING
    |
    v
Small External Beta                        UPCOMING
```

The roadmap should continue to be driven by observed contributor behavior and
real production constraints rather than speculative feature accumulation.

---

## Repository State

The OpenLLMWorks repository is public.

Repository:

```text
https://github.com/namphan813/OpenLLMWorks
```

Relevant current components include:

```text
runner/run_benchmark.py
runner/provisioning.py
runner/submission_client.py
runner/assets.json
runner/build_runner.ps1

submission-worker/

docs/benchmark_v1.md
docs/DIRECT_SUBMISSION.md

scripts/
results/
analytics/
leaderboards/
website/
```

Current high-level checkpoint:

```text
OpenLLMWorks public repository             LIVE
OpenLLMWorks Runner beta                   LIVE
OpenLLMWorks.com                           LIVE
www.openllmworks.com                       LIVE
HTTPS                                      PASS
Hardware / Compare public smoke test       PASS
GA4 baseline collection                    LIVE
api.openllmworks.com                       LIVE
Submission Worker                          LIVE
Private R2 incoming storage                LIVE
Runner direct submission transport         PASS
Bench-001 production direct submission     PASS
Direct Submission MVP                      E2E PASS
Server-side canonical validation           NEXT
External contributor validation            UPCOMING
```

Historical database provenance and frozen Protocol v1.0 identity remain intact
where intentional.

Legacy OpenLLMBench paths remain only where required for historical provenance
or backward compatibility.

---

## Next

### Direct Submission Hardening

The next highest-value engineering work is to strengthen the production intake
boundary established during Weekend 17.

The MVP currently proves:

```text
Canonical ZIP
    |
    v
Explicit Consent
    |
    v
HTTPS Upload
    |
    v
Private Incoming Storage
    |
    v
Submission ID
```

The next stage should build toward:

```text
Incoming Submission
    |
    v
Authoritative Server Validation
    |
    +--> Invalid --> Reject / Quarantine / Record Reason
    |
    +--> Valid
           |
           v
       Maintainer Intake
           |
           v
       Controlled Import
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

Near-term engineering priorities:

1. authoritative server-side validation of received packages
2. malformed ZIP and canonical-format rejection
3. duplicate and idempotency handling
4. submission size and resource limits
5. security, abuse, and rate-limit controls
6. clearer submission status semantics
7. maintainer intake tooling
8. controlled publication integration
9. contributor and maintainer documentation updates
10. end-to-end regression after hardening

The existing Python canonical validator should remain the source of truth for
benchmark validity.

The ingestion Worker should not independently reinvent Protocol v1.0 validation
rules in JavaScript merely for convenience.

### External Contributor Validation

External contributor testing remains an important Public Beta milestone.

A contributor who did not build the Runner should eventually attempt the public
workflow using only resources available to a normal visitor.

Preferred future path:

```text
OpenLLMWorks.com
    |
    v
Download OpenLLMWorks-Runner.exe
    |
    v
Launch Runner
    |
    v
Provision Protocol Assets
    |
    v
Complete Three Benchmark Runs
    |
    v
Review Submission Disclosure
    |
    v
Select Y
    |
    v
Receive Submission ID
```

A successful external direct contribution would establish another project
milestone:

```text
OpenLLMWorks is not only a benchmark we can operate.

It is a benchmark someone else can run and submit to directly.
```

---

## Near-Term Priorities

Current priority order:

1. preserve the Weekend 17 clean production checkpoint
2. implement authoritative server-side submission validation
3. harden malformed-input, duplicate, resource, and abuse handling
4. improve maintainer intake from private incoming storage
5. update contributor documentation for direct submission
6. prepare and validate the next public Runner beta containing direct submission
7. run an external contributor test
8. fix observed contributor friction
9. expand to a small external beta
10. continue internal NVIDIA dataset growth where useful

AMD and Intel remain valuable platform-expansion tracks, but they should not
interrupt completion of the direct-submission trust and intake boundary unless
new evidence changes the priority.

Do not change OLBD Protocol v1.0 merely to solve presentation, onboarding, or
transport problems.

Protocol changes require a benchmark-methodology reason.

---

## Longer-Term Direction

Once the public Windows NVIDIA path and direct-submission intake are externally
validated, OpenLLMWorks can expand along several independent dimensions.

```text
Dataset Growth
    |
    +-- More NVIDIA generations
    +-- Historical GPUs
    +-- Workstation GPUs
    +-- More contributor systems

Platform Expansion
    |
    +-- AMD
    +-- Intel
    +-- Additional operating systems

Submission Infrastructure
    |
    +-- Automated server validation
    +-- Submission status
    +-- Duplicate detection
    +-- Safer automated intake
    +-- Contributor recognition

Benchmark Evolution
    |
    +-- Future protocol versions
    +-- Additional models
    +-- Additional workloads
    +-- Historical cross-protocol preservation

Public Experience
    |
    +-- Better discovery
    +-- SEO
    +-- Richer comparisons
    +-- Hardware recommendations
    +-- Contributor profiles / recognition

Research / Editorial
    |
    +-- The Works
    +-- Benchmark methodology articles
    +-- Hardware-generation analysis
    +-- Local LLM model analysis
    +-- Historical performance research
```

These tracks should build on the current reproducibility, provenance, and
submission-trust foundation rather than replacing it.

---

## Current Checkpoint

As of the end of the current Weekend 17 Direct Submission MVP work:

```text
OpenLLMWorks brand                         ESTABLISHED
OpenLLMWorks.com                           LIVE
www.openllmworks.com                       LIVE
GitHub repository                          PUBLIC
OpenLLMWorks Runner                        PUBLIC BETA
Runner v0.3.0-beta.1                       RELEASED
Windows NVIDIA path                        PROVEN INTERNALLY
Managed Protocol v1.0 assets               PROVEN
Asset corruption recovery                  PROVEN
Offline failure / recovery                 PROVEN
Contributor UX hardening                   COMPLETE
Legacy asset compatibility                 PROVEN
Canonical local validation                 PROVEN
Canonical submission ZIP                   PROVEN
Maintainer import                          PROVEN
Publisher                                  PROVEN
Website                                    LIVE
Hardware pages                             LIVE
GPU Compare                                LIVE
Public visitor smoke test                  PASS
GA4 baseline collection                    LIVE

Direct submission architecture             ESTABLISHED
Contributor disclosure                     PROVEN
Explicit Y/N consent                       PROVEN
api.openllmworks.com                       LIVE
Submission Worker                          LIVE
Private R2 incoming storage                LIVE
Unique submission ID                       PROVEN
Runner HTTPS transport                     PROVEN
Upload failure fallback                    PROVEN
Local ZIP preservation                     PROVEN
Bench-001 production direct submission     PASS
Direct Submission MVP                      E2E PASS

Authoritative server validation             NEXT
Maintainer intake hardening                 NEXT
External direct contributor                 UPCOMING
AMD support                                 FUTURE
Intel accelerator support                   FUTURE
```

The benchmark execution, managed assets, asset recovery, contributor UX,
evidence, canonical validation, submission packaging, maintainer import,
publishing, canonical database, public identity, public Runner, public
repository, production website, domain, analytics baseline, production
submission API, private intake storage, and direct Runner transport foundations
are now in place.

Weekend 16 made the Works public.

Weekend 17 made the Works directly reachable from the Runner.

The next phase is about making that intake boundary as trustworthy and
maintainable as the benchmark itself.
