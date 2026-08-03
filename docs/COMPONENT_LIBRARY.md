# OpenLLMBench Component Library

The Component Library defines the reusable building blocks of the OpenLLMBench website.

Rather than designing each page independently, the website is assembled from a consistent set of reusable components.

This document serves as a bridge between product design and implementation.

Future frontend components should closely follow the concepts described here.

---

# Design Philosophy

Every component should satisfy four principles:

- reusable
- understandable
- data-driven
- responsive

A component should solve one problem well.

Components should not contain business logic.

Business logic belongs to the analytics engines.

---

# Component Hierarchy

```
Page

    ↓

Section

    ↓

Component

    ↓

Element
```

Example

```
Homepage

↓

Trending Hardware Section

↓

Hardware Card

↓

Title
Image
Statistics
Button
```

---

# Hero Banner

## Purpose

Introduce OpenLLMBench.

Immediately explain the project's mission.

## Used On

- Homepage

## Contains

- Project title
- Tagline
- Primary CTA
- Secondary CTA

Example

```
OpenLLMBench

Building the historical record
of local AI performance.

Measure.
Understand.
Preserve.

[ Run Your First Benchmark ]

[ Explore Hardware ]
```

---

# Metric Card

## Purpose

Present one important statistic.

## Used On

- Homepage
- Dashboard
- Snapshot pages

## Fields

- Title
- Value
- Optional trend
- Optional footer

Example

```
Benchmarks

18,432

+214 today
```

---

# Community Story Card

## Purpose

Highlight one meaningful community insight.

This replaces a generic "Interesting Facts" section.

## Used On

- Homepage
- Dashboard

## Fields

- Title
- Story
- Evidence
- Data Snapshot
- Link

Example

```
Today's Story

RTX 4070 submissions
increased 28%
this month.

Based on

418 benchmarks

Data Snapshot

2027-03-22
14:35 UTC

Read More →
```

---

# Community Snapshot Card

## Purpose

Summarize the current state of the benchmark database.

## Used On

- Homepage
- Dashboard

## Fields

- Benchmarks
- GPUs
- CPUs
- Contributors
- Snapshot timestamp

---

# Hardware Card

## Purpose

Represent one GPU or CPU.

## Used On

- Hardware Explorer
- Trending Hardware
- Search
- Recommendations

## Fields

- Hardware name
- Vendor
- Community score
- Typical performance
- Submission count
- Link

---

# Hardware Profile Summary

## Purpose

Provide a quick overview of one hardware platform.

## Fields

- Typical performance
- Best result
- Community range
- Submission count
- Typical memory
- Related hardware

---

# Leaderboard Table

## Purpose

Display ranked benchmark results.

## Used On

- Homepage preview
- Leaderboards
- Hardware pages

## Columns

- Rank
- Hardware
- Benchmark
- Performance
- Snapshot

---

# Trend Card

## Purpose

Show how something is changing.

## Used On

- Homepage
- Dashboard
- Trend Explorer

## Fields

- Metric
- Direction
- Percentage
- Time period

Example

```
RTX 5090

▲ 14%

Last 30 Days
```

---

# Trend Chart

## Purpose

Visualize change over time.

## Used On

- Trend Explorer
- Hardware pages
- Snapshot pages

Possible Metrics

- Performance
- Submission growth
- Hardware adoption
- Backend usage

---

# Snapshot Card

## Purpose

Represent one generated community snapshot.

## Fields

- Snapshot name
- Timestamp
- Benchmark count
- Summary
- Link

---

# Search Bar

## Purpose

Provide fast navigation.

## Search Targets

- GPUs
- CPUs
- Systems
- Models
- llama.cpp versions
- Operating systems

---

# Filter Panel

## Purpose

Allow advanced exploration.

Possible Filters

- GPU
- CPU
- RAM
- VRAM
- Operating system
- Backend
- Model
- Benchmark version

The filter panel should remain optional.

New visitors should not be overwhelmed.

---

# Run Benchmark Card

## Purpose

Guide users through the benchmark process.

## Steps

```
Download

↓

Run

↓

Review

↓

Compare

↓

Submit
```

---

# Recent Results Table

## Purpose

Display recent benchmark activity.

Columns

- Hardware
- Model
- Benchmark
- Date
- Verification

---

# Recommendation Card (Future)

## Purpose

Recommend hardware or models.

Status

Future

Fields

- Rating
- Explanation
- Confidence
- Supporting evidence

Possible Ratings

★★★★★ Excellent

★★★★ Good

★★★ Acceptable

★★ Limited

★ Not Recommended

---

# Build Planner Card (Future)

## Purpose

Recommend complete systems.

Inputs

- Budget
- Power
- Preferred OS
- Target Model

Outputs

- Recommended GPU
- CPU
- RAM
- Estimated experience

---

# Navigation Bar

## Purpose

Provide consistent navigation.

Items

- Home
- Run Benchmark
- Hardware
- Leaderboards
- Trends
- Documentation
- About

---

# Footer

## Purpose

Provide project resources.

Links

- GitHub
- Documentation
- Roadmap
- Contributing
- Privacy
- About

The footer should also display:

```
Community Snapshot

2027-03-22
14:35 UTC
```

---

# Data Snapshot Badge

## Purpose

Communicate when displayed data was generated.

Example

```
Data Snapshot

2027-03-22

14:35 UTC
```

Future versions may include:

- Snapshot ID
- Analytics version
- Database version

---

# Component Principles

Every component should answer at least one question.

Examples

| Component | Question |
|-----------|----------|
| Hero | What is this? |
| Metric Card | How big is the project? |
| Community Story | Why should I care today? |
| Hardware Card | What should I explore? |
| Leaderboard | Who is leading? |
| Trend Card | What is changing? |
| Snapshot Card | What changed recently? |
| Run Benchmark | What should I do next? |

Avoid components that exist only to decorate the interface.

Every component should provide information or guide action.

---

# Progressive Depth

Every page should present information in layers.

```
Meaning

↓

Summary

↓

Evidence

↓

Details

↓

Advanced Controls
```

A newcomer should understand the page in under thirty seconds.

An enthusiast should be able to spend thirty minutes exploring it.

---

# Future Components

Potential future additions include:

- Community Timeline
- OEM Hardware Badge
- Emerging Hardware Card
- Community Poll
- Fact of the Day
- Interactive Model Compatibility
- Build Comparison
- Export Card
- Research Summary

Ideas should remain in the Parking Lot until promoted into the roadmap.

---

# Final Principle

The website should not feel like a collection of pages.

It should feel like a consistent system built from reusable components.

Every component should reinforce the project's mission:

**Measure. Understand. Preserve.**