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

If this is your first benchmark submission, start with:

1. `docs/benchmark_v1.md` for the benchmark protocol.
2. `example_submission/README.md` for the expected submission structure.
3. `example_submission/submission.json` for the submission manifest format.

Benchmark submissions are the foundation of OpenLLMBench.

A useful submission should contain enough information to understand:

- the hardware tested;
- the operating system;
- the inference backend;
- the llama.cpp build or commit, when available;
- the benchmark protocol;
- the individual benchmark runs;
- the calculated performance results.

### Validate Your Submission

Before submitting benchmark data, run the OpenLLMBench submission validator against the completed submission directory.

From the repository root:

```powershell
py -m parser.validate .\path\to\submission