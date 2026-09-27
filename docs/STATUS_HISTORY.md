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


---

# OpenLLMWorks - Project Status

## Weekend 18 - Control Room

**Focus:** Submission automation, operational state, maintainer review, and production administration
**Status:** Control Room MVP / Production Authentication Boundary PASS / Clean Checkpoint

---

## Current Objective

OpenLLMWorks now has a proven contributor-to-intake pipeline:

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
Contributor Consent
        |
        v
HTTPS Direct Submission
        |
        v
Private R2 Intake
        |
        v
Automatic GitHub Actions Validation
        |
        v
D1 Operational State
        |
        v
Maintainer Review
        |
        v
Canonical Import
        |
        v
Publisher
        |
        v
OpenLLMWorks.com
```

Weekend 18 is focused on completing the maintainer side of this lifecycle.

The current engineering boundary is:

```text
Automatic validation
        |
        v
Authenticated Control Room
        |
        v
Manual approval / rejection
        |
        v
Automated controlled import
        |
        v
Publication
```

The guiding principle remains:

```text
Validation is automatic.

Approval is deliberate.

Canonical publication remains controlled.
```

---

## Public Product Identity

```text
OpenLLMWorks
├── OpenLLMWorks Runner
├── Open LLM Benchmark Database
│   └── OLBD Protocol v1.0
├── Hardware Results / Comparisons
├── The Works
│   └── Future research / editorial
└── Community
```

Brand roles:

- **OpenLLMWorks** - public project and ecosystem
- **OpenLLMWorks Runner** - contributor benchmark application
- **Open LLM Benchmark Database** - canonical technical benchmark dataset
- **OLBD Protocol v1.0** - frozen benchmark methodology and provenance
- **The Works** - reserved future research/editorial identity

Current positioning:

```text
Real hardware. Reproducible local AI benchmarks.
```

Production website: `https://openllmworks.com`

GitHub repository: `https://github.com/namphan813/OpenLLMWorks`

Submission API: `https://api.openllmworks.com/v1/submissions`

---

## Current Runner

**Runner:** OpenLLMWorks Runner
**Current public release:** `v0.4.0-beta.1`
**Current platform:** Windows
**Current accelerator:** NVIDIA
**Benchmark Protocol:** OLBD Protocol v1.0

Current contributor workflow:

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
Direct submission grants no contributor system write access to canonical data.

---

## Direct Submission Pipeline

Production intake:

```text
Contributor
    |
    v
OpenLLMWorks Runner
    |
    v
POST /v1/submissions
    |
    v
Cloudflare Submission Worker
    |
    +--> Private R2
    |
    +--> D1: received
    |
    +--> GitHub Actions validation
              |
              v
          D1: validating
              |
              +--> PASS --> validated
              |
              +--> FAIL --> rejected
```

Private R2 bucket: `openllmworks-submissions`

Object convention: `incoming/sub_<uuid>.zip`

Operations database: `openllmworks-operations`

The canonical benchmark database and D1 have deliberately different roles:

```text
D1
= operational/control-plane state

Open LLM Benchmark Database
= canonical historical benchmark record
```

R2 remains the artifact/evidence store.

---

## Authoritative Server-Side Validation

Authoritative validation is now automatic.

GitHub Actions workflow: `.github/workflows/validate-submission.yml`

The workflow:

1. receives a submission ID
2. downloads the exact incoming ZIP from private R2
3. performs safe archive inspection and extraction
4. discovers the canonical submission
5. executes the existing Python canonical validator
6. reports lifecycle state back to D1

Shared archive safety logic: `parser/submission_archive.py`

Current archive controls include:

- 10 MiB archive-size limit
- 25 MiB uncompressed-size limit
- 100-entry maximum
- absolute-path rejection
- parent-traversal rejection
- drive-qualified-path rejection
- symbolic-link rejection
- exactly one `submission.json`
- controlled extraction

The existing Python validator remains the source of truth for OLBD benchmark validity. Protocol v1.0 validation rules are not reimplemented in JavaScript.

Production automatic lifecycle has been proven:

```text
Direct Submission
        |
        v
R2 Intake
        |
        v
D1 received
        |
        v
GitHub Actions Dispatch
        |
        v
D1 validating
        |
        v
Canonical Validation PASS
        |
        v
D1 validated
```

**Status: PRODUCTION PASS**

---

## Submission Operations Database

Cloudflare D1 provides operational submission state.

Database: `openllmworks-operations`

Primary tables:

```text
submissions
submission_events
```

Current lifecycle model:

```text
received
    |
    v
validating
    |
    +--> validated
    |
    +--> rejected
```

Future lifecycle:

```text
validated
    |
    v
awaiting review
    |
    +--> approved
    |
    +--> rejected
            |
            v
        imported
            |
            v
        published
```

`submission_events` provides an audit trail for lifecycle transitions.
The operations database is not a replacement for the canonical benchmark database.

---

## Control Room MVP

Weekend 18 introduced the first maintainer-facing Control Room.

Route: `/admin`

Current UI includes:

```text
Control Room
├── Total submissions
├── Validated
├── Validating
├── Received
├── Rejected
└── Recent submissions
```

The dashboard reads live production submission state from D1 through:

`GET /v1/admin/submissions`

Browser acceptance has proven:

```text
Admin route rendering                  PASS
Control Room UI                        PASS
Production API fetch                   PASS
Live D1 data                           PASS
Submission counts                      PASS
Recent submission table                PASS
```

Current Control Room implementation is on `weekend-18-control-room-ui`.

Current relevant commits:

```text
dbd1336  Add Control Room submissions API
9c3a221  Add Control Room submissions dashboard
```

The branch remains intentionally unmerged while production authentication is completed.

---

## Control Room Production Authentication

Cloudflare Access is now the production authentication boundary for the maintainer Control Room.

Two Access applications protect the administrative surfaces.

### Control Room UI

Destination: `openllmworks.com/admin*`

Application: `OpenLLMWorks Control Room`

### Control Room API

Destination: `api.openllmworks.com/v1/admin/*`

Application: `OpenLLMWorks Control Room API`

Both use `OpenLLMWorks Maintainer` as the Access policy.

The policy is restricted to the explicitly allowlisted maintainer identity.

Production private-browser testing confirmed that unauthenticated requests to both administrative surfaces are intercepted by Cloudflare Access before reaching the application.

Validated security boundary:

```text
Internet
    |
    v
Cloudflare Access
    |
    v
Maintainer Authentication
    |
    v
OpenLLMWorks Maintainer Policy
    |
    +--> /admin*
    |
    +--> api.openllmworks.com/v1/admin/*
```

Results:

```text
Control Room UI Access interception       PASS
Maintainer authentication                 PASS
Post-authentication redirect              PASS
Control Room API Access interception      PASS
Public OpenLLMWorks site                  UNAFFECTED
```

The temporary `ADMIN_API_TOKEN` mechanism remains intentionally active.

It must not be removed until authenticated browser-to-API communication through Cloudflare Access is proven end to end.

---

## Current Security Boundary

Current layered protection:

```text
Browser
    |
    v
Cloudflare Access
    |
    v
Allowlisted Maintainer Identity
    |
    v
Control Room
    |
    v
Cloudflare Access
    |
    v
Admin API
    |
    v
Temporary ADMIN_API_TOKEN
    |
    v
D1 Operations Database
```

The token is currently a transitional second layer rather than the intended long-term Control Room authentication mechanism.

Do not remove it prematurely.

---

## Current Architecture

```text
Contributor Side

OpenLLMWorks Runner
        |
        v
Canonical ZIP
        |
        v
Explicit Consent
        |
        v
HTTPS
        |
        v

Production Intake

Submission Worker
        |
        +--> Private R2
        |
        +--> D1 received
        |
        +--> GitHub Actions
                  |
                  v
             Canonical Validator
                  |
                  v
             D1 validated/rejected
                  |
                  v

Maintainer Side

Cloudflare Access
        |
        v
Control Room
        |
        v
Admin API
        |
        v
D1 Operations State
        |
        v
Future Approve / Reject
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

---

## Preserved Benchmark Guarantees

Current infrastructure work does not change OLBD Protocol v1.0.

OpenLLMWorks continues to preserve:

- frozen benchmark protocol
- frozen benchmark model
- frozen benchmark runtime
- SHA-256 asset verification
- three required benchmark runs
- raw benchmark evidence
- required hardware evidence
- canonical submission validation
- deterministic result identity
- maintainer-controlled provenance
- canonical database separation
- historical benchmark identity

Submission automation changes transport and operations. It does not change benchmark methodology.

---

## Proven Major Milestones

### Weekend 14

First complete Runner -> Submission ZIP -> GitHub Issue -> Maintainer Validation -> Canonical Import -> Publisher -> Website lifecycle proven.

### Weekend 15

Contributor workflow and maintainer tooling hardened.

### Weekend 16

```text
Managed assets                         PASS
Recovery testing                       PASS
Contributor UX                         PASS
OpenLLMWorks rebrand                   COMPLETE
Public GitHub repository               LIVE
Runner public beta                     LIVE
OpenLLMWorks.com                       LIVE
GA4 baseline                           LIVE
```

### Weekend 17

Direct Submission MVP:

```text
Runner
-> Canonical ZIP
-> Explicit Consent
-> HTTPS
-> Submission Worker
-> Private R2
-> Submission ID

E2E PRODUCTION PASS
```

Runner `v0.4.0-beta.1` released with Direct Submission support.

A real GTX 970 Direct Submission was subsequently validated, imported into the canonical database, and published.

### Weekend 18

```text
Safe archive extraction                COMPLETE
Automatic GitHub validation            COMPLETE
D1 operations database                 LIVE
received state recording               PASS
Validation callbacks                   PASS
Automatic received->validated flow     PASS
Control Room Admin API                 PASS
Control Room UI                        PASS
Live D1 dashboard                      PASS
Cloudflare Access UI boundary          PASS
Cloudflare Access API boundary         PASS
```

---

## Current Roadmap

```text
Managed Assets                              COMPLETE
    |
    v
Recovery / Contributor UX                   COMPLETE
    |
    v
OpenLLMWorks Public Beta                    LIVE
    |
    v
Direct Submission MVP                      E2E PASS
    |
    v
Safe Server-Side Validation                COMPLETE
    |
    v
Automatic Validation Pipeline              COMPLETE
    |
    v
D1 Operational State                       LIVE
    |
    v
Control Room MVP                           LIVE-DATA PASS
    |
    v
Cloudflare Access Boundary                 PASS
    |
    v
Browser/API Access Integration             NEXT
    |
    v
Production Control Room Deployment         NEXT
    |
    v
Submission Detail View                     UPCOMING
    |
    v
Manual Approve / Reject                    UPCOMING
    |
    v
Automated Controlled Import                UPCOMING
    |
    v
Automated Publication                      UPCOMING
    |
    v
Operational QoL                            UPCOMING
    |
    v
External Contributor Growth                UPCOMING
    |
    v
AMD / Intel Platform Expansion             FUTURE
```

---

## Current Constraints

Current primary benchmark target: `Windows + NVIDIA`

Current operational constraints:

- Control Room UI branch is not yet merged to `main`
- production `/admin` UI is not yet deployed
- authenticated browser-to-Admin-API communication through Cloudflare Access still needs end-to-end validation
- `ADMIN_API_TOKEN` remains a temporary compatibility/security layer
- approval and rejection are not yet available in the Control Room
- canonical import is not yet triggered from the Control Room
- publication after approval remains a maintainer workflow
- validation failure currently does not fully distinguish canonical rejection from workflow/infrastructure failure
- submission detail/event-history UI is not yet implemented
- external contributor testing remains incomplete
- AMD support is not yet part of the public Runner
- Intel accelerator support is not yet part of the public Runner
- public dataset breadth remains early

---

## Repository State

Current development branch: `weekend-18-control-room-ui`

Current branch checkpoint:

```text
9c3a221  Add Control Room submissions dashboard
dbd1336  Add Control Room submissions API
6e70fac  Merge Weekend 18 Control Room foundation
```

At the current checkpoint, `git status --short` is clean before this documentation update.

The branch is backed up at `origin/weekend-18-control-room-ui`.

Do not merge to `main` until the production Access/browser/API integration is proven.

---

## Next

### Weekend 18 - Control Room Production Integration

```text
Cloudflare Access UI boundary          PASS
Cloudflare Access API boundary         PASS
        |
        v
Test authenticated browser -> API
        |
        v
Resolve cross-origin Access behavior
        |
        v
Remove temporary token-entry UI
        |
        v
Build / Regression Test
        |
        v
Merge Control Room branch
        |
        v
Deploy production website
        |
        v
Visit /admin
        |
        v
Authenticate
        |
        v
Live D1 Control Room
```

Do not remove `ADMIN_API_TOKEN` until this complete path is proven.

After production Control Room authentication is complete:

```text
Submission Detail View
        |
        v
Submission Event History
        |
        v
Approve / Reject
        |
        v
Controlled Automated Import
        |
        v
Automatic Publication
```

---

## Near-Term Priorities

1. prove authenticated browser-to-Admin-API communication
2. remove the temporary Control Room token-entry UX
3. deploy the authenticated production Control Room
4. add submission detail and event-history views
5. implement deliberate Approve / Reject actions
6. automate canonical import only after explicit approval
7. automate publication after successful controlled import
8. add operational retry, stuck-submission, filter, and search tooling
9. complete external contributor validation
10. expand platform support after the submission lifecycle is maintainable

The submission lifecycle should be completed before increasing submission volume through broader platform support.

---

## Current Checkpoint

```text
OpenLLMWorks brand                         ESTABLISHED
OpenLLMWorks.com                           LIVE
GitHub repository                          PUBLIC

OpenLLMWorks Runner                        PUBLIC BETA
Runner v0.4.0-beta.1                       RELEASED
Windows NVIDIA benchmark path              PROVEN
Managed Protocol v1.0 assets               PROVEN
Canonical local validation                 PROVEN
Canonical submission ZIP                   PROVEN

Direct submission                          PRODUCTION PASS
Submission Worker                          LIVE
Private R2 intake                          LIVE
Automatic GitHub Actions validation        LIVE
Safe archive extraction                    PROVEN
D1 operations database                     LIVE
Automatic lifecycle state                  PROVEN

Control Room Admin API                     PROVEN
Control Room UI                            PROVEN
Live production D1 dashboard               PROVEN

Cloudflare Access Control Room             PASS
Cloudflare Access Admin API                PASS
Maintainer allow policy                    ACTIVE

Authenticated browser -> Admin API         NEXT
Production Control Room deployment         NEXT
Submission detail view                     UPCOMING
Approve / Reject                           UPCOMING
Automated controlled import                UPCOMING
Automated publication                      UPCOMING

External contributor validation            UPCOMING
AMD support                                FUTURE
Intel accelerator support                  FUTURE
```

Weekend 16 made the Works public.

Weekend 17 connected the Runner directly to the Works.

Weekend 18 is building the Control Room that lets the Works operate safely at scale.
