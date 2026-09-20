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
