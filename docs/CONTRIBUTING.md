# Contributing to OpenLLMBench

Thank you for your interest in OpenLLMBench.

OpenLLMBench is an open-source, community-driven project focused on measuring, understanding, and preserving the history of local Large Language Model inference performance.

Contributions of many kinds are welcome.

You do not need to be an experienced software engineer to help.

Useful contributions may include:

- benchmark results;
- bug reports;
- documentation improvements;
- testing;
- hardware-normalization corrections;
- feature ideas;
- analytics improvements;
- website design;
- accessibility feedback;
- code contributions.

Every thoughtful contribution helps improve the project.

---

# Before You Begin

Please become familiar with the project’s guiding documents:

- `README.md`
- `MANIFESTO.md`
- `FOUNDING_STORY.md`
- `docs/DESIGN_PRINCIPLES.md`
- `docs/ARCHITECTURE.md`

These documents explain what OpenLLMBench is trying to accomplish and why the project is structured the way it is.

The short version is:

> Measure. Understand. Preserve.

When proposing a change, consider whether it helps the project accomplish one or more of those goals.

---

# Ways to Contribute

## Submit Benchmark Results

Benchmark submissions are the foundation of OpenLLMBench.

A useful submission should contain enough information to understand:

- the hardware tested;
- the operating system;
- the inference backend;
- the llama.cpp build or commit, when available;
- the benchmark protocol;
- the individual benchmark runs;
- the calculated performance results.

Submission tooling and public submission instructions are still under development.

Until that workflow is complete, benchmark contributions may require manual review.

Never alter benchmark values merely to make a submission appear cleaner or more competitive.

Unknown information should remain unknown.

---

## Report a Bug

A useful bug report should include:

- what you expected to happen;
- what actually happened;
- the command you ran;
- the complete error message;
- your operating system;
- your Python version;
- the relevant OpenLLMBench version;
- steps that reproduce the issue;
- screenshots or sample files when helpful.

Please remove personal or sensitive information before sharing logs, screenshots, or files.

A small, reproducible example is often more useful than a long description without reproduction steps.

---

## Suggest a Feature

Feature ideas are welcome.

A strong feature request explains:

1. What problem are you trying to solve?
2. Who would benefit from the change?
3. What question should OpenLLMBench be able to answer?
4. Does the feature belong in Parser, Database, Utilities, Analytics, or Presentation?
5. Does it help OpenLLMBench measure, understand, or preserve?

Please describe the user need before prescribing a technical solution.

For example:

Less useful:

> Add another chart library.

More useful:

> Users need a clear way to compare a GPU’s typical performance with its best and worst community results.

The second description gives contributors room to choose the best implementation.

---

## Improve Documentation

Documentation contributions are especially welcome.

Useful improvements include:

- correcting unclear wording;
- adding examples;
- documenting setup steps;
- improving architecture explanations;
- clarifying command output;
- fixing broken links;
- adding troubleshooting guidance;
- improving accessibility;
- documenting a previously undocumented decision.

Documentation is part of the product, not an afterthought.

---

## Contribute Code

Before starting a large code change, open an issue or discussion describing the proposed work.

This helps avoid duplicated effort and gives maintainers an opportunity to confirm that the change fits the architecture.

Small bug fixes and documentation corrections may not require a prior discussion.

---

# Development Philosophy

OpenLLMBench follows a simple development rhythm:

```text
Think
  ↓
Build
  ↓
Test
  ↓
Green
  ↓
Repeat
```

Changes should be divided into small, complete pieces whenever practical.

A contribution should leave the repository in a runnable and understandable state.

Prefer:

- one focused improvement;
- one clear responsibility;
- one reliable test;
- one complete result.

Avoid combining unrelated changes into one pull request.

---

# Architectural Responsibilities

OpenLLMBench separates responsibilities into several layers.

```text
Parser
Database
Utilities
Analytics
Presentation
```

## Parser

Use `parser/` for work involving:

- submission discovery;
- reading benchmark files;
- normalization;
- timestamps;
- validation;
- database-record construction;
- schema migration logic.

The Parser layer answers:

> What was measured?

## Database

Database behavior currently lives primarily in `parser/database.py`.

Use it for:

- result identity;
- duplicate detection;
- database loading;
- database writing;
- import history;
- supported schema upgrades.

The Database layer answers:

> What does OpenLLMBench know?

## Utilities

Use `utilities/` for operational tools such as:

- hashing;
- backups;
- verification;
- restoration;
- health checks;
- migration orchestration.

Utilities should reuse Parser and Database rules rather than redefining them.

The Utilities layer answers:

> Is the data protected and healthy?

## Analytics

Use `analytics/` for reusable calculations such as:

- statistics;
- rankings;
- hardware profiles;
- facts;
- snapshots;
- trends;
- historical comparisons.

Analytics modules return structured data.

They should not print terminal reports or generate web pages.

The Analytics layer answers:

> What can we learn from the database?

## Presentation

Root-level viewers and the future website belong to the Presentation layer.

Presentation code may:

- format output;
- display reports;
- handle terminal or web-specific concerns.

Presentation code should not:

- define schemas;
- calculate analytics already handled by engines;
- modify benchmark records;
- perform migrations;
- implement backup logic.

---

# Coding Guidelines

## Keep Modules Focused

Every module should have one clear responsibility.

Prefer small reusable functions over large functions that perform unrelated work.

Avoid creating a generic utility module that becomes a dumping ground for unrelated helpers.

---

## Use Clear Names

Names should explain intent.

Prefer:

```python
build_historical_snapshots()
```

over:

```python
process_data()
```

Prefer:

```python
benchmark_timestamp
```

over:

```python
date_value
```

---

## Preserve Type Meaning

Do not silently convert unknown or invalid values into apparently valid data.

For example:

```python
benchmark_timestamp = None
```

is better than inventing a date.

Similarly, a missing performance value should not become `0` unless zero is the true measured value.

---

## Keep Engines Separate From Viewers

Analytics engines should return structured objects.

Example:

```python
report = build_trend_report(database)
```

A viewer may then format that report for a terminal, website, API, or exported document.

Do not place user-interface formatting inside the analytics engine.

---

## Avoid Circular Dependencies

Foundational modules must not import the presentation modules that consume them.

Acceptable:

```text
trends.py
    → analytics.trends
```

Avoid:

```text
analytics.trends
    → trends.py
```

Consult `docs/ARCHITECTURE.md` when unsure about dependency direction.

---

## Handle Errors Clearly

Errors should explain:

- what failed;
- which value or file caused the failure;
- what the user can do next.

Avoid silently ignoring failures that could affect data integrity.

For non-critical optional historical values, returning `None` may be appropriate when the behavior is explicitly documented.

---

## Use UTC for Stored Timestamps

Stored timestamps should be:

- timezone-aware;
- normalized to UTC;
- represented in ISO 8601 format.

Use the functions in:

```text
parser/timestamps.py
```

Do not implement new timestamp parsing independently in another module.

---

## Protect Database Integrity

Any operation that can replace or modify the live database should eventually follow this order:

```text
Recovery Copy
      ↓
Source Validation
      ↓
Verified Backup
      ↓
Proposed Change
      ↓
Changed-Copy Validation
      ↓
Atomic Replacement
      ↓
Final Verification
```

Do not bypass integrity checks for convenience.

---

# Formatting Conventions

The existing project generally favors:

- four spaces for indentation;
- descriptive docstrings;
- explicit intermediate variables;
- type hints where practical;
- readable line lengths;
- clear section comments;
- complete files when introducing major modules.

New code should match the surrounding style unless a broader formatting standard is formally adopted.

Avoid compressing important logic merely to reduce line count.

Readability is more valuable than cleverness.

---

# Testing Changes

Before submitting a pull request:

1. Run the relevant command or viewer.
2. Confirm the expected output.
3. Test invalid input when the change handles validation.
4. Confirm existing commands still run.
5. Verify that the live database was not unintentionally modified.
6. Include the exact test command in the pull request description.

Examples may include:

```powershell
py stats.py
```

```powershell
py leaderboard.py
```

```powershell
py trends.py
```

```powershell
py historical_snapshots.py
```

For module-level checks:

```powershell
py -c "from pathlib import Path; ..."
```

Automated tests will be added as the project matures. Until then, clearly documented reproducible checks are required.

---

# Working With Database Changes

Database and schema changes require extra care.

A pull request involving database structure should explain:

- the current schema;
- the proposed schema;
- why the change is necessary;
- how existing records are treated;
- whether values can be migrated truthfully;
- what remains unknown;
- how rollback works;
- how the migrated copy is validated.

Never require users to delete their database merely because the schema changed unless no responsible migration path is possible.

Migration code should preserve history and record its own activity.

---

# Working With Benchmark Data

Benchmark records should be treated as observations.

Do not:

- change scores to match expectations;
- remove valid low-performing results because they appear unusual;
- replace unknown values with guesses;
- merge distinct systems without evidence;
- hide inconvenient results.

Potential outliers may be flagged for review, but the original observation should be preserved.

Evidence should be separated from interpretation.

---

# Pull Request Guidelines

Keep pull requests focused.

A good pull request should include:

## Summary

What does this change do?

## Motivation

What problem does it solve?

## Architecture

Which layer owns this responsibility, and why?

## Testing

What commands did you run?

## Data Integrity

Could this change modify, delete, reinterpret, or migrate benchmark data?

## Screenshots

Include screenshots when output or user experience changes.

## Follow-Up Work

List intentionally deferred improvements rather than expanding the pull request indefinitely.

---

# Suggested Pull Request Template

```markdown
## Summary

Describe the change.

## Why

Explain the user or project need.

## Layer

- [ ] Parser
- [ ] Database
- [ ] Utilities
- [ ] Analytics
- [ ] Presentation
- [ ] Documentation

## Testing

List the commands and results used to verify the change.

## Data Integrity

Explain whether the change affects stored benchmark data.

## Screenshots

Add screenshots when relevant.

## Follow-Up

List related work that is intentionally outside this pull request.
```

---

# Commit Guidance

Commit messages should be short and descriptive.

Examples:

```text
Add monthly trend aggregation
```

```text
Verify backup SHA-256 hashes
```

```text
Document analytics architecture
```

```text
Fix date-only timestamp normalization
```

Avoid vague messages such as:

```text
Updates
```

```text
Fix stuff
```

```text
Changes
```

Small, understandable commits are easier to review and recover.

---

# Security and Privacy

Do not commit:

- passwords;
- API keys;
- access tokens;
- private email addresses;
- personal file paths when avoidable;
- precise home-network details;
- private benchmark submissions;
- credentials embedded in configuration files.

Report security-sensitive issues privately once a formal security process is available.

Until then, avoid publishing exploit details in a public issue when doing so could put users or data at risk.

---

# Community Expectations

Be respectful.

Assume good intent.

Explain decisions without belittling newcomers.

Ask questions when requirements are unclear.

Technical disagreement is welcome.

Personal attacks are not.

OpenLLMBench should remain approachable to:

- experienced engineers;
- local-AI enthusiasts;
- hardware hobbyists;
- students;
- first-time open-source contributors;
- curious users who are still learning.

Expertise should be shared, not used as a gatekeeping tool.

---

# Scope and Sustainability

Not every useful idea must be built immediately.

Before expanding the project, consider:

- maintenance burden;
- moderation burden;
- infrastructure cost;
- privacy implications;
- data-integrity risk;
- contributor availability;
- alignment with the mission.

A smaller dependable feature is usually more valuable than a broad unfinished one.

---

# Recognition

Contributors should receive appropriate credit for meaningful work.

Future recognition may include:

- Git commit history;
- release notes;
- contributor listings;
- benchmark-contributor acknowledgments;
- project-history documents.

OpenLLMBench is intended to be built with its community, not merely delivered to it.

---

# Questions

When unsure where to begin:

1. Review the open issues or discussions.
2. Read `docs/ARCHITECTURE.md`.
3. Choose a small, well-defined improvement.
4. Ask before beginning a large structural change.

Thoughtful questions are contributions too.

---

Thank you for helping OpenLLMBench measure, understand, and preserve the evolution of local AI performance.

**Measure. Understand. Preserve.**