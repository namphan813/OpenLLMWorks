# OpenLLMWorks Architecture

## Overview

OpenLLMWorks is an open-source platform for collecting, normalizing, preserving, and analyzing local Large Language Model inference benchmarks.

The project is organized around a simple lifecycle:

```text
Measure
   ↓
Normalize
   ↓
Preserve
   ↓
Understand
   ↓
Share
```

Each stage has a distinct responsibility. This separation keeps the project understandable, testable, and adaptable as it grows.

---

## Architectural Goals

OpenLLMWorks is designed to:

- preserve benchmark data without inventing missing values;
- keep computation separate from presentation;
- support safe database and schema evolution;
- make critical operations verifiable and reversible;
- reuse the same analytics across terminal tools, websites, reports, and APIs;
- remain approachable to new contributors;
- scale from a local project to a community platform.

The architecture favors small modules with clear responsibilities over large, tightly coupled systems.

---

## System Overview

```text
┌─────────────────────────────────────────────────────────────┐
│                    Benchmark Environment                    │
│                                                             │
│  Hardware + Operating System + llama.cpp + Benchmark Runs   │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│                       Parser Layer                          │
│                                                             │
│  Discovers submissions                                     │
│  Parses benchmark files                                    │
│  Extracts hardware and software details                    │
│  Normalizes values                                         │
│  Validates incoming records                                │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│                       Database Layer                        │
│                                                             │
│  Stores normalized benchmark records                       │
│  Generates deterministic result IDs                        │
│  Detects duplicate submissions                             │
│  Maintains import and migration history                    │
│  Supports schema evolution                                 │
└───────────────┬──────────────────────┬──────────────────────┘
                │                      │
                ▼                      ▼
┌───────────────────────────┐  ┌──────────────────────────────┐
│      Utilities Layer      │  │       Analytics Layer        │
│                           │  │                              │
│  Hashing                  │  │  Statistics                  │
│  Verified backups         │  │  Leaderboards               │
│  Database verification    │  │  Hardware profiles          │
│  Migration support        │  │  Interesting facts          │
│  Restore and health       │  │  Current snapshots          │
│  services                 │  │  Trends and history         │
└───────────────┬───────────┘  └──────────────┬───────────────┘
                │                             │
                └──────────────┬──────────────┘
                               ▼
┌─────────────────────────────────────────────────────────────┐
│                    Presentation Layer                       │
│                                                             │
│  Terminal viewers                                          │
│  Future website                                            │
│  Future public API                                         │
│  Reports and infographics                                  │
│  Monthly and historical snapshots                          │
└─────────────────────────────────────────────────────────────┘
```

---

## Repository Structure

```text
OpenLLMWorks/
│
├── parser/
│   ├── parser.py
│   ├── database.py
│   ├── submission.py
│   ├── validator.py
│   ├── timestamps.py
│   └── migrations.py
│
├── analytics/
│   ├── statistics.py
│   ├── leaderboards.py
│   ├── profiles.py
│   ├── facts.py
│   ├── snapshots.py
│   ├── trends.py
│   └── historical_snapshots.py
│
├── utilities/
│   ├── hashes.py
│   ├── backup.py
│   └── verify.py
│
├── database/
│   ├── benchmark_database.json
│   └── backups/
│
├── docs/
│   ├── ARCHITECTURE.md
│   ├── DESIGN_PRINCIPLES.md
│   ├── OPERATIONS.md
│   ├── ROADMAP.md
│   ├── VISION.md
│   ├── decisions/
│   └── history/
│
├── stats.py
├── leaderboard.py
├── profile.py
├── facts.py
├── snapshot.py
├── trends.py
└── historical_snapshots.py
```

Some files and folders shown above represent the intended architecture and may still be under active development.

---

# Core Layers

## 1. Parser Layer

**Location:** `parser/`

The Parser layer converts incoming benchmark files into normalized records that the rest of OpenLLMWorks can trust.

Its responsibilities include:

- locating benchmark submissions;
- reading benchmark result files;
- extracting hardware information;
- extracting benchmark measurements;
- enforcing benchmark protocol requirements;
- normalizing names and values;
- building submission objects;
- rejecting malformed or incomplete input.

The Parser layer answers:

> What was measured?

### Important modules

#### `parser/parser.py`

Coordinates the end-to-end import workflow.

It discovers submissions, invokes parsing and validation, creates records, and sends them to the Database layer.

#### `parser/submission.py`

Represents one benchmark submission and its associated source files.

#### `parser/validator.py`

Defines the structural rules that determine whether databases and records are acceptable.

Validation rules belong here rather than inside viewers or utilities.

#### `parser/timestamps.py`

Creates, parses, normalizes, and compares timestamps.

All stored timestamps are normalized to timezone-aware UTC values.

#### `parser/migrations.py`

Transforms supported older database schemas into newer schemas without discarding historical records.

Unknown historical values remain unknown rather than being inferred.

---

## 2. Database Layer

**Primary module:** `parser/database.py`  
**Persistent data:** `database/benchmark_database.json`

The Database layer is the system of record for OpenLLMWorks.

It is responsible for:

- creating normalized result records;
- generating deterministic result IDs;
- identifying duplicate benchmark content;
- storing results and import events;
- loading supported database schemas;
- routing older schemas through migrations;
- writing updated databases;
- preserving migration history.

The Database layer answers:

> What does OpenLLMWorks know?

### Deterministic result identity

A result ID is derived from the normalized benchmark content rather than from a filename, path, or submission timestamp.

Conceptually:

```text
Normalized Hardware
        +
Benchmark Protocol
        +
llama.cpp Information
        +
Run Measurements
        +
Calculated Averages
        ↓
Canonical JSON
        ↓
SHA-256
        ↓
Deterministic Result ID
```

This allows identical benchmark content to be recognized even when it is submitted under a different folder or filename.

### Database evolution

OpenLLMWorks supports explicit schema migration:

```text
Schema 0.6
    ↓
Migration Engine
    ↓
Schema 0.7
    ↓
Future Migrations
    ↓
Schema 1.0+
```

Migrations operate on copies before any live data is replaced.

Historical fields that cannot be reconstructed remain `None`.

---

## 3. Utilities Layer

**Location:** `utilities/`

Utilities protect and maintain the data used by OpenLLMWorks.

They orchestrate critical operations by reusing Parser and Database capabilities rather than duplicating them.

The Utilities layer answers:

> Is the data protected and healthy?

### Current utilities

#### `utilities/hashes.py`

Calculates reusable SHA-256 file hashes.

Hashing supports:

- backup verification;
- migration verification;
- restore verification;
- exported dataset verification;
- future download integrity checks.

#### `utilities/backup.py`

Creates a copy of the database and confirms that its SHA-256 hash matches the source.

A successful copy proves that the backup is byte-for-byte identical to the source at the time of creation.

### Planned utilities

#### `utilities/verify.py`

Will evaluate database readability, structure, schema consistency, result counts, and duplicate IDs.

#### `utilities/restore.py`

Will restore a selected verified backup and validate the restored database before it becomes active.

#### `utilities/health.py`

Will summarize database, backup, migration, and system health in one report.

#### `utilities/migrate.py`

Will coordinate:

```text
Recovery Copy
      ↓
Source Validation
      ↓
Verified Backup
      ↓
Migration
      ↓
Migrated-Copy Validation
      ↓
Atomic Replacement
      ↓
Final Verification
```

### Utilities do not define the schema

The Parser layer owns validation rules and database structure.

Utilities call those components and report their results.

This prevents validation logic from being duplicated across backup, restore, health, and migration tools.

---

## 4. Analytics Layer

**Location:** `analytics/`

The Analytics layer converts benchmark records into reusable knowledge.

Analytics modules return structured Python data. They do not print terminal output, generate HTML, or make UI decisions.

The Analytics layer answers:

> What can we learn from the database?

### `analytics/statistics.py`

Describes the complete database.

Examples:

- result count;
- hardware counts;
- vendor counts;
- operating systems;
- average performance;
- memory and VRAM averages;
- import history.

Question answered:

> What is in the database?

### `analytics/leaderboards.py`

Ranks results and common hardware values.

Examples:

- fastest `pp512`;
- fastest `tg128`;
- largest VRAM;
- largest system memory;
- most common GPU;
- most common CPU.

Question answered:

> Who is leading?

### `analytics/profiles.py`

Groups results by hardware model and produces reusable profiles.

Examples:

- submission count;
- average performance;
- best and worst performance;
- average RAM and VRAM;
- represented operating systems.

Question answered:

> What does OpenLLMWorks know about this hardware?

### `analytics/facts.py`

Transforms statistics and leaderboard results into short, understandable facts.

Examples:

- database size;
- average prompt-processing speed;
- most common GPU;
- fastest result;
- average system memory.

Question answered:

> What is interesting right now?

### `analytics/snapshots.py`

Combines statistics, leaderboards, profiles, and facts into one current-state report.

Question answered:

> What does OpenLLMWorks look like at this moment?

### `analytics/trends.py`

Selects the best available timestamp for each result and aggregates observations over time.

Timestamp priority:

```text
benchmark_timestamp
        ↓
submitted_at
        ↓
imported_at
        ↓
processed_at
```

The selected timestamp source is preserved in the trend report so the platform remains transparent about the historical evidence being used.

Question answered:

> What is changing over time?

### `analytics/historical_snapshots.py`

Builds monthly snapshots and month-over-month comparisons from Trend Engine output.

Examples:

- monthly result volume;
- average monthly performance;
- fastest monthly results;
- submission growth;
- performance percentage changes.

Question answered:

> How does one period compare with another?

---

## 5. Presentation Layer

The Presentation layer turns structured engine output into something a person or another system can consume.

Current terminal viewers live at the project root:

```text
stats.py
leaderboard.py
profile.py
facts.py
snapshot.py
trends.py
historical_snapshots.py
```

These viewers should:

- load or request structured data;
- format it;
- display it;
- handle presentation-specific errors.

They should not:

- calculate averages;
- rank results;
- define database schemas;
- detect duplicates;
- implement backup logic;
- modify analytics data.

### Engine and viewer pattern

```text
analytics/statistics.py
          ↓
        stats.py
```

```text
analytics/leaderboards.py
          ↓
     leaderboard.py
```

```text
analytics/profiles.py
          ↓
       profile.py
```

The future website and API will consume the same analytics engines.

```text
Analytics Engine
   ├── Terminal Viewer
   ├── Website
   ├── Public API
   ├── Reports
   └── Snapshot Exports
```

No business logic should need to be rewritten for each presentation.

---

# Data Flow

## Benchmark ingestion

```text
Benchmark Files
      ↓
Submission Discovery
      ↓
Parsing
      ↓
Normalization
      ↓
Validation
      ↓
Result Record Creation
      ↓
Deterministic ID Generation
      ↓
Duplicate Detection
      ↓
Persistent Database
```

## Analytics flow

```text
Persistent Database
      ↓
Result Extraction
      ↓
Statistics / Rankings / Grouping / Time Buckets
      ↓
Structured Report Objects
      ↓
Terminal / Website / API / Reports
```

## Backup flow

```text
Source Database
      ↓
Source Hash
      ↓
Backup Copy
      ↓
Backup Hash
      ↓
Hash Comparison
      ↓
Structured Backup Report
```

## Future safe-migration flow

```text
Live Database
      ↓
Raw Recovery Copy
      ↓
Source Validation
      ↓
Verified Backup
      ↓
In-Memory Migration
      ↓
Migrated-Copy Validation
      ↓
Atomic Live-File Replacement
      ↓
Final Verification
```

---

# Data Integrity Rules

OpenLLMWorks follows several non-negotiable rules.

## Unknown means unknown

Missing historical timestamps are stored as `None`.

The system does not invent submission dates or benchmark dates merely to make reports more complete.

## Backups must be verifiable

A backup is trusted only when:

- the source can be read;
- the copy exists;
- both files can be hashed;
- source and backup SHA-256 hashes match.

Future validation will also confirm the logical health of the database before the backup is marked as verified.

## Migrations must preserve history

Migration metadata records:

- source schema;
- target schema;
- migration timestamp;
- migration module version;
- number of migrated records.

## Critical operations must be reversible

Live files should not be replaced until:

- a recovery copy exists;
- a verified backup exists;
- the proposed replacement passes validation.

---

# Dependency Direction

Dependencies should flow toward foundational modules.

```text
Presentation
     ↓
Analytics
     ↓
Database and Parser

Utilities
     ↓
Database and Parser

Parser and Database
     ↓
Standard Library
```

The project should avoid circular dependencies.

Examples of acceptable dependencies:

```text
leaderboard.py
    → analytics.leaderboards
    → analytics.statistics
```

```text
utilities.backup
    → utilities.hashes
```

```text
utilities.verify
    → parser.validator
```

Examples to avoid:

```text
analytics.statistics
    → stats.py
```

```text
parser.database
    → website
```

```text
utilities.hashes
    → utilities.backup
```

Foundational modules must not depend on the presentation modules that consume them.

---

# Architectural Boundaries

## Parser code should not:

- print website content;
- calculate leaderboards;
- choose UI labels;
- upload data to social platforms;
- contain advertisement logic.

## Analytics code should not:

- write directly to the live database;
- decide terminal colors;
- generate HTML markup;
- perform backup operations.

## Utilities should not:

- redefine database schemas;
- calculate benchmark insights;
- silently repair or invent benchmark values.

## Viewers should not:

- duplicate calculations already provided by Analytics;
- change database records;
- implement migrations;
- perform destructive operations.

---

# Current State and Planned Components

## Implemented or in active development

- benchmark parsing;
- normalized result records;
- deterministic IDs;
- duplicate detection;
- persistent JSON database;
- schema migration foundation;
- UTC timestamp normalization;
- statistics;
- leaderboards;
- hardware profiles;
- interesting facts;
- current snapshots;
- trend analytics;
- historical snapshots;
- SHA-256 hashing;
- verified backup creation;
- terminal viewers.

## Planned

- complete schema 0.7 live rollout;
- full database verification;
- safe atomic migration;
- restore utility;
- health utility;
- benchmark execution and upload tool;
- website;
- hardware explorer;
- submission explorer;
- public API;
- interactive charts;
- public community submissions.

Planned components should follow the same boundaries described in this document.

---

# Future Website Architecture

The initial website should remain thin.

```text
Browser
   ↓
Website Presentation
   ↓
Precomputed JSON or API
   ↓
Existing Analytics Engines
   ↓
Benchmark Database
```

The website should not duplicate ranking, profile, trend, or snapshot calculations.

A local or controlled processing system may periodically:

1. load the database;
2. build analytics reports;
3. export website-ready JSON;
4. publish static assets;
5. allow a CDN to serve them.

This approach can keep early infrastructure costs low while reducing the public attack surface.

---

# Architectural Decision Process

Significant architectural decisions should eventually be recorded in:

```text
docs/decisions/
```

Suggested records include:

```text
0001-project-structure.md
0002-deterministic-result-identity.md
0003-schema-evolution.md
0004-verified-backup-strategy.md
0005-utilities-layer.md
0006-engine-viewer-separation.md
```

Each Architecture Decision Record should explain:

- the problem;
- the decision;
- alternatives considered;
- consequences;
- current status.

This preserves the reasoning behind the architecture rather than documenting only the final structure.

---

# Guiding Principle

OpenLLMWorks architecture should remain:

- simple at first glance;
- powerful when explored;
- honest about its data;
- safe to operate;
- easy to extend;
- useful for years.

When deciding where new work belongs, ask:

1. What question does this component answer?
2. Which layer owns that responsibility?
3. Can the logic be reused by more than one presentation?
4. Does it preserve data integrity?
5. Does it help OpenLLMWorks measure, understand, or preserve?

---

**Measure. Understand. Preserve.**