# OpenLLMWorks Maintainer Workflow

## Purpose

This document describes the trusted maintainer workflow for processing one
OpenLLMWorks submission after it has been downloaded and extracted.

The workflow is intentionally orchestrated through existing canonical
OpenLLMWorks components rather than reimplementing validation, parsing,
database ingestion, or publishing logic.

The normal pipeline is:

```text
Extracted Submission
        ↓
Contributor Validation
        ↓
Stage in incoming/
        ↓
Targeted Database Import
        ↓
Publisher
        ↓
Generated Website Data
```

The maintainer helper script for this workflow is:

```text
scripts/process_submission.py
```

---

## Standard Command

From the repository root:

```powershell
python .\scripts\process_submission.py `
    "C:\path\to\extracted\submission" `
    --source-type "<trusted source type>" `
    --contributor-id "<trusted contributor id>" `
    --contributor-type "<trusted contributor type>" `
    --verification-status "<maintainer verification status>"
```

All four provenance fields are required by the maintainer workflow.

They should be assigned deliberately by the maintainer based on the trusted
submission source and verification process.

---

## Workflow Stages

### 1. Validate Submission

The maintainer workflow first invokes the canonical contributor-facing
validator:

```powershell
python -m parser.validate <submission_path>
```

If validation fails:

- The workflow stops immediately.
- Nothing is copied into `incoming/`.
- The database is not modified.
- The publisher is not run.

---

### 2. Stage Submission

After validation passes, the source submission is copied into:

```text
incoming/<submission-folder-name>/
```

The original extracted submission remains untouched.

If the destination already exists, the workflow stops rather than
overwriting it.

This protects existing staged evidence and prevents accidental replacement
of another submission.

---

### 3. Import Submission

The workflow imports exactly the staged submission by invoking:

```powershell
python -m parser.parser `
    --submission "<submission-folder-name>" `
    --source-type "<trusted source type>" `
    --contributor-id "<trusted contributor id>" `
    --contributor-type "<trusted contributor type>" `
    --verification-status "<maintainer verification status>"
```

The parser remains the authority for:

- submission parsing
- benchmark result extraction
- normalized record creation
- deterministic result IDs
- duplicate detection
- database updates
- import history

The maintainer workflow does not duplicate this logic.

---

### 4. Publish Website Data

Publishing runs only after the import command completes successfully.

The workflow invokes:

```powershell
python -m publisher.generate_site
```

The publisher remains the authority for generating public website data from
the canonical benchmark database.

---

## Trusted Provenance Fields

The parser currently defines these internal defaults:

```text
source_type:          internal_seed
contributor_id:       founder_000001
contributor_type:     founder
verification_status: internally_verified
```

These defaults represent the historical/internal seed workflow.

The maintainer helper intentionally requires provenance values to be supplied
explicitly so that external or community submissions are not accidentally
classified as internal seed data.

Do not copy the internal defaults into a community submission unless they
accurately describe that submission.

---

## Safety Behavior

The maintainer workflow is designed to stop safely.

### Missing Source Path

If the supplied submission path does not exist:

```text
[FAIL] Submission path was not found
```

The workflow stops before validation, staging, import, or publishing.

### Validation Failure

If canonical submission validation fails:

```text
[FAIL] Submission validation
```

The workflow stops before staging or database modification.

### Existing Staging Destination

If the corresponding directory already exists in `incoming/`, the workflow
refuses to overwrite it.

The workflow stops before database import.

### Import Failure

If the parser import command fails:

- Publishing is not started.
- The staged submission remains in `incoming/` for inspection.

### Publish Failure

If publishing fails after a successful database import:

- The database import remains complete.
- The maintainer should review the publisher error before continuing.
- Existing source submission evidence remains preserved.

---

## Expected Successful Run

A successful workflow should resemble:

```text
OpenLLMWorks Maintainer Workflow

[1/4] Validate submission
[PASS] Submission validation

[2/4] Stage submission
[PASS] Copied to incoming\<submission-name>

[3/4] Import submission
[PASS] Submission import

[4/4] Publish website data
[PASS] Website publishing

Maintainer workflow completed successfully.
```

---

## Duplicate Submissions

OpenLLMWorks uses deterministic result IDs to detect duplicate benchmark
measurements.

A duplicate result is not added as a second benchmark result.

However, the parser records duplicate import attempts in database import
history. For that reason, maintainers should not intentionally reprocess
known duplicate submissions merely as a workflow test against the canonical
database.

Use a disposable repository/database copy for end-to-end workflow testing.

---

## Maintainer Testing

For workflow development or regression testing, use a temporary copy of the
repository rather than the canonical database.

A safe test should verify:

```text
Validate
    ↓
Stage
    ↓
Import
    ↓
Publish
```

while leaving the real repository unchanged.

After testing, confirm the canonical repository with:

```powershell
git status
```

Unexpected changes to the canonical database, generated publisher outputs, or
tracked submission content should be investigated before continuing.

---

## Design Principle

The maintainer workflow orchestrates existing OpenLLMWorks authorities.

```text
Validator validates.
Parser parses and imports.
Database preserves.
Publisher publishes.
Maintainer workflow orchestrates.
```

The helper script should remain thin.

It should not become a second validation engine, parser, database writer, or
publisher.
