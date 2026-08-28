# OpenLLMWorks Website Vision

## Purpose

The OpenLLMWorks website is the public-facing experience for the benchmark data, analytics, and historical records created by the project.

The website should help visitors:

- understand what OpenLLMWorks is;
- discover what their hardware can do;
- explore community benchmark data;
- learn what is changing in local AI;
- run and submit their own benchmark;
- return regularly for new data, trends, and community insights.

The website is not the source of benchmark intelligence.

It is a presentation layer built on top of the existing OpenLLMWorks engines.

```text
Parser and Database
        ↓
Analytics and Utilities
        ↓
Website and API
```

Business logic should remain outside the website whenever practical.

---

# Product Vision

OpenLLMWorks should feel like a modern hardware-intelligence platform rather than a traditional benchmark table.

It should combine:

- the usefulness of a benchmark database;
- the approachability of a consumer product;
- the depth expected by technical enthusiasts;
- the transparency of an open-source project;
- the historical perspective of a long-term archive.

The website should be simple at first glance and powerful when explored.

---

# Core Message

The website should communicate the project’s purpose immediately:

> **Building the historical record of local AI performance.**

The supporting project identity is:

> **Measure. Understand. Preserve.**

Visitors should understand that OpenLLMWorks is not only concerned with identifying the fastest system today.

It is also designed to explain:

- how performance changes;
- why it changes;
- which hardware and software combinations work well;
- what a user can realistically run;
- how the local AI ecosystem evolves over time.

---

# Primary Audience

OpenLLMWorks should be approachable to everyone, while naturally leaning toward curious and technically interested users.

The core audience includes:

- people wondering how fast their computer is;
- local-LLM enthusiasts;
- PC and workstation builders;
- gamers experimenting with local AI;
- developers using llama.cpp;
- Home Assistant and homelab enthusiasts;
- Linux users;
- hardware hobbyists;
- students;
- researchers;
- data-oriented users who enjoy exploring trends;
- newcomers who do not yet understand benchmark terminology.

The website should not require expert knowledge to provide value.

Curiosity is the entry requirement, not technical expertise.

---

# User Experience Goal

Within the first 30 seconds, a visitor should feel:

> **“I understand what this is, and I know what I can do next.”**

The experience should feel:

- welcoming;
- clear;
- modern;
- technically credible;
- calm rather than overwhelming;
- polished without becoming decorative;
- useful before requiring an account or commitment.

The first page should not feel like a dense administrative dashboard or spreadsheet.

It should feel like an introduction to what is happening in local AI performance.

---

# Primary Visitor Journey

The primary first-time visitor journey is:

```text
Discover OpenLLMWorks
        ↓
Understand the project
        ↓
See interesting community data
        ↓
Run the benchmark tool
        ↓
Understand the machine’s capabilities
        ↓
Explore related hardware and models
        ↓
Contribute a benchmark
```

The most important homepage action should be:

> **Run Your First Benchmark**

This is preferable to a generic button such as “Download.”

It communicates an experience rather than a file transfer.

---

# Returning Visitor Journey

Returning visitors are likely to come back for:

- updated benchmark data;
- hardware rankings;
- interesting facts;
- monthly snapshots;
- performance trends;
- new hardware;
- new llama.cpp builds;
- model compatibility information;
- community discussion;
- comparison and filtering tools.

The website should reward repeat visits by showing what has changed.

Examples include:

- new benchmark submissions;
- newly represented hardware;
- changing averages;
- trending GPUs or CPUs;
- notable performance improvements;
- monthly community summaries;
- emerging model and hardware combinations.

---

# Homepage Objectives

The homepage should answer four questions quickly:

1. What is OpenLLMWorks?
2. Why does it matter?
3. What is happening in local AI right now?
4. How can I test my own machine?

The homepage should prioritize understanding over completeness.

Detailed filtering and technical exploration belong on deeper pages.

---

# Proposed Homepage Structure

## 1. Hero

The hero should introduce the project without excessive marketing language.

Suggested structure:

```text
OpenLLMWorks

Building the historical record
of local AI performance.

Measure. Understand. Preserve.

[ Run Your First Benchmark ]
[ Explore the Data ]
```

The primary button should be visually dominant.

The secondary button should lead toward the hardware or benchmark explorer.

---

## 2. Community Snapshot

Show a small collection of high-level metrics.

Potential cards include:

- total benchmark results;
- represented GPU models;
- represented CPU models;
- represented operating systems;
- latest monthly snapshot;
- fastest current result.

These cards should be understandable without benchmark expertise.

---

## 3. Interesting Right Now

Use the Interesting Facts and Trend engines to summarize what is happening.

Examples:

- the fastest new result;
- a rapidly growing hardware family;
- a change in average performance;
- a newly represented GPU;
- a shift in operating-system use;
- a notable llama.cpp improvement.

This section should explain the significance of the data instead of merely listing numbers.

---

## 4. Run Your First Benchmark

Explain the process in a small number of steps:

```text
Download the tool
        ↓
Run the benchmark
        ↓
Review your results
        ↓
Compare with the community
```

The process should feel safe, understandable, and achievable.

Future versions should explain:

- what the tool measures;
- what information is collected;
- what is not collected;
- how results are reviewed;
- how submission works;
- how privacy is protected.

---

## 5. Leaderboard Preview

Show only a small preview on the homepage.

Possible categories:

- fastest prompt processing;
- fastest token generation;
- top consumer GPU;
- top low-power system;
- top integrated graphics result.

The full leaderboard should remain a separate experience with filters and methodology details.

---

## 6. Trending Hardware

Highlight hardware receiving growing attention or producing notable results.

Each item may show:

- hardware name;
- submission count;
- recent change;
- typical performance;
- link to the full profile.

This section should not imply that popularity always equals quality.

---

## 7. Latest Snapshot

Provide a summary of the current month or most recent reporting period.

The snapshot may include:

- benchmark growth;
- average performance;
- new hardware;
- current leaders;
- notable facts;
- links to historical comparisons.

---

## 8. Explore Hardware

Provide clear entry points for:

- GPUs;
- CPUs;
- complete systems;
- integrated graphics;
- operating systems;
- future model compatibility.

The initial release may focus primarily on GPUs because they are likely to be the strongest discovery path.

---

## 9. Recent Benchmarks

Show a small, readable selection of recent community results.

Each result should communicate:

- hardware;
- performance;
- benchmark date or available timestamp source;
- operating system;
- llama.cpp information when available;
- verification status.

The website should remain transparent when true benchmark dates are unavailable.

---

## 10. Project and Community

Provide links to:

- GitHub;
- documentation;
- roadmap;
- discussions;
- contributing guide;
- manifesto;
- development status.

GitHub Discussions should be the initial community venue.

OpenLLMWorks should avoid creating and maintaining multiple community platforms before demand justifies them.

---

# Navigation

The first version should use a focused navigation structure.

```text
Home
Run Benchmark
Hardware
Leaderboards
Trends
Snapshots
Documentation
About
```

A search control should be easy to find.

Potential search targets include:

- GPU models;
- CPU models;
- complete systems;
- model names;
- llama.cpp commits or builds;
- operating systems;
- benchmark submissions.

Navigation should remain stable as the site grows.

Avoid adding a top-level menu item for every feature.

---

# Hardware Explorer

The Hardware Explorer should be one of the most important parts of the website.

A hardware profile should answer:

- How many submissions represent this hardware?
- What performance is typical?
- What is the observed range?
- What are the best and worst results?
- How has performance changed over time?
- Which operating systems are represented?
- Which llama.cpp builds are represented?
- What system-memory and VRAM configurations are common?
- What hardware is similar?
- What models may be appropriate for this hardware?

The page should serve both newcomers and experts.

---

# Beginner and Advanced Views

OpenLLMWorks should expose different levels of detail without maintaining separate products.

## Beginner experience

Use approachable descriptions such as:

- Typical Performance
- Best Observed Result
- Community Range
- Good for Smaller Models
- Limited by Available VRAM
- Similar Systems

Avoid forcing newcomers to understand every benchmark field immediately.

## Advanced experience

Allow enthusiasts to explore:

- raw result values;
- individual runs;
- timestamp sources;
- backend;
- protocol;
- llama.cpp commit and build;
- memory;
- VRAM;
- operating system;
- filters;
- distributions;
- historical comparisons.

Advanced information may be shown through expandable areas, tabs, or optional controls.

The interface should not hide evidence, but it should organize complexity.

---

# Recommendations Vision

A future Recommendation Engine should turn benchmark evidence into practical guidance.

Potential questions include:

- What models can my machine run?
- What quantization should I choose?
- What experience should I expect?
- Which component is limiting me?
- What should I upgrade?
- What hardware fits my target model?
- What system fits my budget and power limit?

Potential classifications include:

```text
Excellent
Good
Acceptable
Limited
Not Recommended
```

Recommendations should explain why they received a classification.

They should be based on community data and documented assumptions.

Commercial relationships must never determine the recommendation.

Any affiliate link should follow a recommendation rather than influence it.

---

# Community Strategy

OpenLLMWorks should begin with one primary community location:

> **GitHub Discussions**

Reasons include:

- low operational overhead;
- proximity to the project;
- searchable discussions;
- contributor familiarity;
- no separate account system;
- easier moderation than managing several social communities.

Possible future community channels may include Reddit, Discord, or an onsite forum.

They should be added only when there is enough demand and moderation capacity.

A community channel is not free merely because it has no hosting bill.

Maintainer time is a real cost.

---

# Articles and Editorial Content

The website may eventually include local-AI articles or editorial summaries.

Possible content includes:

- monthly benchmark summaries;
- new hardware analysis;
- llama.cpp performance changes;
- model compatibility guides;
- benchmark methodology explanations;
- community system spotlights;
- hardware buying guides;
- historical retrospectives.

Editorial content should be evidence-driven and clearly distinguish observation from interpretation.

Articles should support the benchmark platform rather than turn OpenLLMWorks into a general AI-news site.

---

# Visual Direction

OpenLLMWorks should feel more refined than a traditional desktop benchmark utility.

The visual direction should be:

- dark-first;
- modern;
- spacious;
- information-rich without appearing crowded;
- technical without resembling a BIOS screen;
- polished without resembling a marketing landing page;
- visually engaging without distracting from the data.

The design should borrow principles rather than imitate brands.

Useful references include:

- GitHub for clarity and information structure;
- Apple for typography and breathing room;
- Grafana for data presentation;
- modern PC-hardware interfaces for technical personality;
- Home Assistant for progressive depth and enthusiast credibility.

---

# Visual Hierarchy

The interface should establish a clear reading order:

```text
Meaning
    ↓
Important Metrics
    ↓
Explanation
    ↓
Detailed Evidence
    ↓
Advanced Controls
```

Do not begin with the densest possible table.

High-level information should lead visitors toward deeper exploration.

---

# Data Presentation

Use the appropriate presentation for each question.

## Metric cards

Use for:

- result count;
- unique hardware;
- current leader;
- average performance;
- monthly growth.

## Short facts

Use for:

- meaningful changes;
- notable community activity;
- surprising relationships;
- newly represented hardware.

## Tables

Use for:

- detailed leaderboards;
- raw results;
- searchable submissions;
- advanced comparisons.

## Charts

Use when shape and change matter.

Examples:

- performance over time;
- submission growth;
- hardware adoption;
- observed range;
- distribution of results.

Do not create a chart merely because data exists.

---

# Trust and Transparency

The website should clearly communicate:

- benchmark methodology;
- protocol requirements;
- timestamp sources;
- verification status;
- number of supporting results;
- limitations;
- missing values;
- confidence levels for future recommendations.

The project should not imply precision that the data cannot support.

Examples:

Prefer:

> Based on 34 community results.

Avoid:

> This hardware will always achieve exactly 31.4 tokens per second.

---

# AI Collaboration Transparency

OpenLLMWorks has used AI-assisted planning, coding, debugging, and documentation.

The website and repository should explain this transparently.

AI-generated or AI-assisted output is not treated as authoritative.

Human maintainers remain responsible for:

- reviewing decisions;
- understanding accepted code;
- testing features;
- verifying data;
- publishing content;
- maintaining the project.

Transparency should remove uncertainty without making AI usage the central identity of the project.

---

# Monetization Principles

The website may eventually use:

- clearly labeled advertising;
- affiliate links;
- sponsorships;
- donations;
- API subscriptions;
- paid data services.

Monetization should support the project without compromising trust.

The order of priorities should remain:

```text
Help the user
      ↓
Explain the evidence
      ↓
Make a recommendation
      ↓
Offer an optional commercial link
```

Commercial relationships must not change rankings, conclusions, or recommendations.

---

# Technical Direction

The website should remain a thin presentation layer.

```text
Browser
    ↓
Website
    ↓
Published JSON or API
    ↓
Existing Analytics Engines
    ↓
Benchmark Database
```

Early versions may rely heavily on precomputed static JSON.

Benefits include:

- low hosting cost;
- strong CDN caching;
- reduced public attack surface;
- simple deployment;
- predictable performance;
- limited backend infrastructure.

The website should not recalculate analytics logic that already exists in Python modules.

---

# Performance Goals

The website should feel fast on ordinary consumer hardware and mobile devices.

Priorities include:

- small initial page payload;
- responsive layout;
- cached data;
- minimal blocking scripts;
- progressive loading of deeper data;
- useful content before advanced visualizations finish loading.

Visual polish should not come at the expense of usability or speed.

---

# Accessibility

Accessibility should be treated as a requirement, not a later enhancement.

The website should provide:

- semantic headings;
- keyboard-accessible controls;
- sufficient contrast;
- visible focus states;
- meaningful link labels;
- text alternatives for visuals;
- clear chart labels;
- information that does not depend on color alone;
- readable typography;
- responsive layouts.

Technical users also benefit from accessible design.

---

# Privacy

The website and benchmark tool should collect only information required to provide the service.

Future documentation should clearly explain:

- what hardware data is collected;
- what software data is collected;
- whether usernames are required;
- whether personal information is stored;
- how submissions can be removed;
- whether IP addresses are retained;
- how analytics and advertising are handled.

The first version should avoid unnecessary accounts and tracking.

---

# Accounts

User accounts should not be required during the first website phase unless a necessary workflow cannot function without them.

Possible future benefits include:

- managing submissions;
- saving comparisons;
- claiming systems;
- contributor recognition;
- notification preferences.

Accounts also create:

- security obligations;
- privacy obligations;
- password or identity-management work;
- moderation requirements;
- support burden.

They should be introduced only when their benefit clearly exceeds their cost.

---

# Homepage Success Criteria

The homepage succeeds when a first-time visitor can answer:

- What is OpenLLMWorks?
- Why does benchmark history matter?
- What is interesting right now?
- How do I benchmark my machine?
- Where can I explore hardware?
- How can I trust the data?

A successful homepage should lead naturally toward action without pressuring the visitor.

---

# Weekend 6 Scope

The Community phase should focus on:

- website information architecture;
- homepage;
- navigation;
- hardware exploration;
- leaderboard presentation;
- trend and snapshot presentation;
- public analytics access;
- responsive visual polish.

The following ideas are valuable but should remain outside the immediate scope unless promoted from the Parking Lot:

- full Recommendation Engine;
- Build Planner;
- onsite forum;
- complex user accounts;
- paid API;
- broad AI-news publishing;
- marketplace features;
- advanced social features.

---

# Design Questions for Every Page

Before building a page, ask:

1. Who is this page for?
2. What question are they trying to answer?
3. What should they understand first?
4. What is the primary action?
5. Which existing engine provides the data?
6. What evidence supports the conclusion?
7. What complexity can be deferred?
8. What would make the visitor return?

---

# Guiding Experience

OpenLLMWorks should be:

> Easy enough for someone asking, “How fast is my computer?”

and

> Deep enough for someone comparing timestamp sources, llama.cpp builds, hardware ranges, and historical trends.

That balance is central to the product.

---

# Final Vision

The website tells the story.

The benchmark tool creates the story.

The database preserves the story.

The analytics explain the story.

The community expands the story.

---

**Measure. Understand. Preserve.**