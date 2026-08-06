# OpenLLMBench Publisher

## Purpose

The Publisher transforms internal OpenLLMBench data into stable, generated files that external consumers can safely use.

It acts as the boundary between the benchmark platform and presentation layers such as the React website.

The Publisher does not collect benchmarks, parse results, or calculate analytics itself.

Instead, it reads existing database and analytics outputs, then publishes them in documented JSON formats.

---

# Position in the System

```text
Benchmark Runner
        ↓
Parser
        ↓
Benchmark Database
        ↓
Analytics
        ↓
Publisher
        ↓
Generated JSON
        ↓
React Website
```

The website consumes published data rather than reading the internal database directly.

---

# Responsibilities

The Publisher is responsible for:

- Reading benchmark database records
- Reading precomputed analytics
- Reading historical snapshots
- Transforming internal structures into public data contracts
- Writing generated JSON files
- Adding generation timestamps
- Producing deterministic output
- Validating required fields before publication
- Reporting publication success or failure

---

# Non-Responsibilities

The Publisher must not:

- Modify benchmark source records
- Import raw benchmark files
- Parse llama.cpp output
- Calculate analytics that belong in the analytics layer
- Contain React or website presentation logic
- Store secrets or private contributor information
- Treat generated files as the primary database

Generated files are disposable outputs and must always be reproducible from the source database and analytics.

---

# Initial Output Directory

```text
database/
└── generated/
    ├── homepage.json
    ├── hardware.json
    ├── leaderboards.json
    ├── snapshots.json
    └── trends.json
```

The directory may expand as additional consumers and features are introduced.

---

# Initial Published Files

## homepage.json

Provides the information needed by the homepage.

Expected content:

- Generation timestamp
- Summary statistics
- Featured Community Story
- Data snapshot information
- Recent milestone information

---

## hardware.json

Provides hardware profiles and aggregate hardware information.

Expected content:

- Hardware identifiers
- Vendor
- Device category
- Submission count
- Typical performance
- Best recorded performance
- Supported platforms and backends
- Related hardware

---

## leaderboards.json

Provides precomputed rankings.

Expected content:

- pp512 rankings
- tg128 rankings
- GPU rankings
- CPU rankings
- Submission counts
- Snapshot timestamp
- Verification status

---

## snapshots.json

Provides historical database snapshots.

Expected content:

- Snapshot identifier
- Creation timestamp
- Benchmark count
- Hardware count
- Contributor count
- Database growth
- Summary changes

---

## trends.json

Provides long-term analytical trends.

Expected content:

- Hardware adoption
- Vendor distribution
- Backend distribution
- Model popularity
- Performance changes over time
- Submission growth

---

# Data Contract Principles

## Stable Field Names

Published field names should remain stable whenever possible.

Changing an internal Python class or database field should not automatically require changes to website components.

---

## Versioned Contracts

Every generated file should eventually include a contract version.

Example:

```json
{
  "contractVersion": "1.0",
  "generatedAt": "2026-08-06T01:30:00Z"
}
```

Breaking changes require a new contract version.

---

## Deterministic Output

Publishing the same source data and analytics should produce the same substantive output.

Generation timestamps may differ, but ordering, values, and identifiers should remain consistent.

---

## Read-Only Publication

The Publisher reads source data but never writes back into the benchmark database.

Its output is downstream and disposable.

---

## Validation Before Writing

The Publisher should validate required fields before replacing an existing generated file.

A failed publication must not leave behind malformed or partially written JSON.

Future versions should write to a temporary file first and replace the final file only after validation succeeds.

---

## Privacy

Published files must not expose private or unnecessary contributor information.

Public contributor identifiers should be deliberately designed rather than copied directly from internal records.

---

# Initial Publisher Command

The planned command is:

```powershell
python generate_site.py
```

Expected future output:

```text
OpenLLMBench Publisher

Loading benchmark database...
✓ Database loaded

Loading analytics...
✓ Analytics loaded

Publishing homepage.json...
✓ Complete

Publishing hardware.json...
✓ Complete

Publishing leaderboards.json...
✓ Complete

Publishing snapshots.json...
✓ Complete

Publishing trends.json...
✓ Complete

Website data published successfully.
```

The first implementation may generate only `homepage.json`.

Additional outputs should be added incrementally.

---

# Consumers

Initial consumer:

- React website

Potential future consumers:

- Public API
- Command-line interface
- Desktop application
- Mobile application
- Open Lab
- Research exports
- Third-party integrations

Consumers should depend on documented published contracts rather than internal Python modules.

---

# Error Handling

The Publisher should fail clearly and safely.

Possible failures include:

- Missing database
- Invalid JSON source
- Missing analytics fields
- Unsupported contract version
- Output directory unavailable
- Validation failure
- File write failure

Errors should identify:

- What failed
- Which file was affected
- Whether existing published data remains safe

---

# Future Capabilities

Potential future Publisher features include:

- Schema validation
- Contract migrations
- Incremental publishing
- Publication manifests
- File hashes
- Signed releases
- Compressed exports
- API-ready output
- Public and private publication profiles
- Automated publication after benchmark import

---

# Final Principle

The Publisher is the controlled gateway between OpenLLMBench's internal intelligence and its public consumers.

The parser parses.

The database preserves.

Analytics interprets.

The Publisher publishes.

The website presents.