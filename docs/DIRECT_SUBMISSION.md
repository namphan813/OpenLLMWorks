# OpenLLMWorks Direct Submission Pipeline

**Status:** Development  
**Phase:** Weekend 17 - Direct Submission Pipeline  
**Initial Target:** OpenLLMWorks Runner for Windows / NVIDIA

---

## Purpose

The OpenLLMWorks Direct Submission Pipeline allows contributors to
submit a completed benchmark directly from the OpenLLMWorks Runner
without requiring a GitHub account or manual GitHub Issue.

The existing canonical OpenLLMWorks submission package remains the
unit of submission.

Direct submission adds a transport layer to the existing benchmark
workflow. It does not replace the canonical submission format,
validation architecture, database import process, or publisher.

---

## Goals

The Direct Submission Pipeline should:

- Reduce friction between completing a benchmark and contributing it.
- Preserve the existing canonical submission ZIP format.
- Require explicit contributor consent before uploading.
- Clearly disclose the information contained in the upload.
- Preserve the completed ZIP locally regardless of upload choice.
- Provide clear success and failure responses.
- Keep server-side validation authoritative.
- Store new uploads outside the canonical public database until they
  have passed the appropriate maintainer-controlled workflow.
- Preserve manual submission as a fallback.

---

## Non-Goals

The initial Direct Submission implementation does not require:

- OpenLLMWorks user accounts.
- GitHub authentication.
- OAuth.
- Contributor profiles.
- Automated database import.
- Automated publication.
- Synchronous website rebuilding.
- Public submission management.
- A sophisticated maintainer queue.
- Changes to OLBD Protocol v1.0.
- Changes to the canonical submission ZIP format.

These capabilities may be considered in future phases.

---

## Contributor Workflow

The intended contributor workflow is:

```text
Benchmark
    ↓
Local Validation
    ↓
Canonical Submission ZIP
    ↓
Upload Disclosure
    ↓
Explicit Y/N Consent
    ↓
HTTPS Upload
    ↓
OpenLLMWorks Submission API
    ↓
Private Incoming Storage
    ↓
Server Validation
    ↓
Maintainer Approval / Import
    ↓
Canonical Database
    ↓
Publisher
    ↓
Public Website
```

Direct submission occurs only after the Runner has successfully
created and locally validated the canonical submission package.

---

## Consent Model

OpenLLMWorks must never automatically upload benchmark results.

Before any network submission occurs, the Runner must:

1. Confirm that the canonical submission ZIP exists.
2. Display the submission name.
3. Display the detected GPU.
4. Display the ZIP package name.
5. Explain the categories of information contained in the package.
6. Explain that the ZIP remains saved locally.
7. Ask for explicit Y/N consent.

Example:

```text
============================================================
Submit Benchmark to OpenLLMWorks
============================================================

Your validated benchmark package is ready for optional submission.

Submission: Example-System-NVIDIA-GeForce-GTX-1050-Ti-20260829-180000
GPU:        NVIDIA GeForce GTX 1050 Ti
Package:    Example-System-NVIDIA-GeForce-GTX-1050-Ti-20260829-180000.zip

The package includes benchmark results and system information
collected by the Runner:

- CPU information
- Memory information
- Operating system information
- GPU and driver information
- Raw benchmark output
- OpenLLMWorks submission manifest

Your validated ZIP will remain saved locally whether or not you
upload it.

Upload this benchmark to OpenLLMWorks? [Y/N]:
```

Entering `N`, pressing Enter without entering a value, reaching EOF,
or interrupting the optional consent prompt must not invalidate the
completed benchmark.

---

## Benchmark Success vs Submission Success

Benchmark execution and network submission are separate operations.

A successfully validated and packaged benchmark remains successful
regardless of what happens during direct submission.

For example:

```text
Benchmark:  PASS
Submission: NOT REQUESTED
```

or:

```text
Benchmark:  PASS
Submission: RECEIVED
```

or:

```text
Benchmark:  PASS
Submission: UPLOAD FAILED
```

An unavailable API, network interruption, server error, rejected
upload, or contributor decision not to upload must not change the
benchmark result to failure.

The canonical ZIP remains available for manual submission.

---

## Canonical Submission Package

Direct submission uses the same ZIP package already produced by the
OpenLLMWorks Runner.

The initial implementation must not introduce a second submission
format.

The canonical package currently contains the validated submission
workspace, including:

```text
<submission-name>/
├── cpu.txt
├── memory.txt
├── system.txt
├── windows.txt
├── nvidia-smi.txt
├── benchmark-v1.0-p512-run1.txt
├── benchmark-v1.0-p512-run2.txt
├── benchmark-v1.0-p512-run3.txt
└── submission.json
```

The ZIP should be transmitted unchanged.

---

## Local Validation

The Runner performs local validation before creating the canonical
submission ZIP.

Local validation provides immediate contributor feedback and prevents
obviously incomplete submissions from being offered for upload.

Local validation does not establish authoritative acceptance by
OpenLLMWorks.

---

## Server Validation

Server-side validation is authoritative.

A submission that passes local Runner validation may still be rejected
by the server.

Server validation will be implemented as part of Direct Submission
hardening and may include:

- Canonical ZIP structure validation.
- Required-file validation.
- Manifest validation.
- Protocol compatibility validation.
- Evidence validation.
- File-size and archive safety checks.
- Duplicate detection.
- Additional integrity checks.

Receiving a ZIP is therefore not equivalent to accepting its benchmark
into the canonical database.

---

## Submission States

The Direct Submission system should distinguish between transport,
validation, import, and publication.

Initial state model:

```text
received
validated
rejected
imported
published
```

### received

The submission API successfully received and stored the canonical ZIP.

This does not mean that server validation has passed.

### validated

Authoritative server-side validation passed.

### rejected

The submission failed authoritative validation or was rejected during
maintainer review.

### imported

The submission was imported into the canonical OpenLLMWorks database.

### published

The imported submission is represented in generated public data and
the OpenLLMWorks website.

Stage 1 requires only the `received` state.

---

## Stage 1 API Contract

Initial endpoint:

```text
POST /v1/submissions
```

Initial content type:

```text
Content-Type: application/zip
```

The request body contains the raw canonical submission ZIP.

Multipart form encoding is intentionally unnecessary for the initial
implementation because the request contains a single canonical
artifact.

---

## Successful Response

When the submission has been successfully stored, the API should
return:

```text
HTTP 201 Created
```

Example body:

```json
{
  "submission_id": "sub_01...",
  "status": "received"
}
```

The submission ID must uniquely identify the received package.

The Runner should display this ID to the contributor.

Example:

```text
[OK] Benchmark received by OpenLLMWorks.

Submission ID: sub_01...

Your local ZIP has been preserved.
```

---

## Error Response

API errors should return an appropriate HTTP status code and a
machine-readable JSON response.

Example:

```json
{
  "error": "invalid_request",
  "message": "The submission could not be received."
}
```

Contributor-facing Runner messages should remain concise and should
not expose unnecessary server implementation details.

Regardless of API failure, the Runner should remind the contributor
that the validated ZIP remains available locally.

---

## Server Architecture

The initial production architecture is expected to use the existing
OpenLLMWorks Cloudflare environment.

Proposed architecture:

```text
OpenLLMWorks Runner
        |
        | HTTPS
        v
api.openllmworks.com
        |
        v
Submission Worker
        |
        v
Private R2 Incoming Storage
```

The submission service should remain logically separate from the
public OpenLLMWorks website.

This limits coupling between website delivery and submission
processing.

---

## Incoming Storage

New submissions must not be written directly into the canonical
OpenLLMWorks database.

Stage 1 uploads should be stored in a private incoming area.

Conceptually:

```text
incoming/
└── <submission-id>.zip
```

The original uploaded ZIP should be preserved unchanged.

Incoming storage acts as a quarantine boundary between untrusted
Internet uploads and trusted canonical benchmark data.

---

## API Authentication

The initial public Runner should not contain a private API credential.

Any secret embedded in a publicly distributed executable must be
assumed recoverable.

The submission endpoint is therefore designed as a public ingestion
endpoint with server-side abuse protections.

Future authentication mechanisms may be added if OpenLLMWorks later
introduces accounts or contributor identities.

---

## Security Boundary

Files submitted through the public API are untrusted input.

The Direct Submission service must not assume that a ZIP was created
by an authentic OpenLLMWorks Runner simply because it resembles a
canonical submission.

During Stage 1, the server should minimize processing of uploaded
content.

Stage 2 hardening should address controls including:

- Maximum request size.
- Supported content type.
- Request rate limiting.
- ZIP archive safety.
- Path traversal protection.
- Decompression limits.
- Required-file allowlists.
- Duplicate submissions.
- Malformed manifests.
- Unsupported protocol versions.
- Unexpected archive contents.
- Logging and operational visibility.

Uploaded files should not become public merely because they were
successfully received.

---

## Runner Architecture

Direct submission should remain separated from benchmark execution.

Runner transport functionality belongs in:

```text
runner/submission_client.py
```

The benchmark workflow remains in:

```text
runner/run_benchmark.py
```

The intended responsibility boundary is:

```text
run_benchmark.py
    |
    ├── benchmark execution
    ├── evidence collection
    ├── manifest generation
    ├── local validation
    ├── ZIP packaging
    |
    └── offer_direct_submission(...)
             |
             ├── disclosure
             ├── consent
             ├── HTTPS transport
             └── response handling
```

Direct submission should not determine whether the benchmark itself
passed.

---

## Manual Submission Fallback

The existing manual submission workflow remains supported.

A contributor who:

- selects `N`,
- loses network connectivity,
- encounters an API error,
- encounters server rejection,
- or chooses to submit later

can use the locally preserved canonical ZIP.

GitHub/manual submission therefore remains a fallback path during the
Direct Submission beta.

---

## Publication Architecture

Direct submission and website publication are asynchronous concerns.

The initial lifecycle is:

```text
API receives ZIP
    ↓
Incoming storage
    ↓
Server validation
    ↓
Maintainer review
    ↓
Canonical import
    ↓
Publisher
    ↓
Website deployment
```

The API does not need to rebuild or deploy the OpenLLMWorks website
while servicing the contributor's request.

This preserves the existing publisher and deployment architecture.

---

## Implementation Plan

### Stage 1 - Direct Submission MVP

Target:

```text
Runner consent
    ↓
HTTPS upload
    ↓
Submission API
    ↓
Private incoming storage
    ↓
Submission ID
```

Stage 1 work includes:

- Contributor disclosure.
- Explicit Y/N consent.
- Runner submission client.
- HTTPS upload transport.
- Submission Worker.
- Private incoming storage.
- Unique submission IDs.
- Clear received/error responses.
- Local ZIP preservation.
- Basic end-to-end testing.

Automated server validation is not required for Stage 1.

---

### Stage 2 - Validation and Hardening

Stage 2 work includes:

- Authoritative server-side validation.
- Archive safety controls.
- Duplicate handling.
- Improved API error handling.
- Request-size enforcement.
- Rate limiting and abuse controls.
- Maintainer processing workflow.
- Import integration.
- Publication integration.
- Contributor documentation.
- Operational documentation.
- Full end-to-end regression testing.

---

## Current Development State

The initial Runner-side consent layer has been implemented.

Current behavior:

```text
Validated ZIP
    ↓
Disclosure
    ↓
Y/N consent
```

The following consent behaviors have been validated:

```text
N
→ direct submission skipped
→ ZIP preserved

Y
→ development transport placeholder
→ no upload occurs
→ ZIP preserved

Ctrl+C during consent
→ treated as declining optional submission
→ completed benchmark remains valid
→ ZIP preserved
```

Network transport is intentionally not connected yet.

---

## Design Principles

1. **Consent before transport.**  
   OpenLLMWorks never uploads benchmark data automatically.

2. **One canonical artifact.**  
   Direct submission transports the same validated ZIP used by the
   existing manual workflow.

3. **Local results remain local too.**  
   Uploading does not remove or replace the contributor's local copy.

4. **Benchmark success is independent of upload success.**  
   Network failure cannot invalidate a completed benchmark.

5. **Server validation is authoritative.**  
   Local validation improves contributor experience but does not
   establish canonical acceptance.

6. **Incoming is not canonical.**  
   Internet uploads enter quarantine before trusted database import.

7. **Keep the MVP narrow.**  
   Accounts, profiles, automated publishing, and other platform
   capabilities are not required to remove the immediate contributor
   submission barrier.

8. **Preserve the existing Works.**  
   Direct submission extends the proven benchmark and publishing
   architecture rather than replacing it.