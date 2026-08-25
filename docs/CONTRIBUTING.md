# Contributing to OpenLLMBench

Thank you for your interest in OpenLLMBench.

OpenLLMBench is an open-source, community-driven project focused on measuring, understanding, and preserving the history of local Large Language Model inference performance.

Contributions of many kinds are welcome. You do not need to be an experienced software engineer to help.

Useful contributions may include benchmark results, bug reports, documentation improvements, testing, hardware-normalization corrections, feature ideas, analytics improvements, website design, accessibility feedback, and code contributions.

Every thoughtful contribution helps improve the project.

---

# Before You Begin

Please become familiar with the project's guiding documents:

- `README.md`
- `MANIFESTO.md`
- `FOUNDING_STORY.md`
- `docs/DESIGN_PRINCIPLES.md`
- `docs/ARCHITECTURE.md`

The short version is:

> Measure. Understand. Preserve.

---

# Submit Benchmark Results

Benchmark submissions are the foundation of OpenLLMBench.

The preferred submission path is the OpenLLMBench Runner. The Runner automates environment verification, hardware evidence collection, benchmark execution, result parsing, manifest generation, validation, and submission packaging.

## Runner Status

The current OpenLLMBench Runner is a development version.

It currently requires:

- Windows 11
- an NVIDIA GPU with a working NVIDIA driver
- Python
- the frozen OpenLLMBench benchmark model
- the frozen `llama-bench.exe` benchmark engine
- the OpenLLMBench repository or Runner source

A standalone contributor-facing OpenLLMBench Runner executable is planned but is not yet available.

---

# Current Runner Setup

The development Runner currently expects:

```text
C:\AI-Benchmark\
    models\
        Qwen3-4B-Q4_K_M.gguf

    llama.cpp\
        llama-bench.exe

    results\
```

The Runner verifies the benchmark model and `llama-bench.exe` using the frozen SHA-256 values defined in `runner/run_benchmark.py`.

Do not substitute a different model or benchmark executable and expect the result to be accepted as Benchmark Protocol v1.0.

See `docs/benchmark_v1.md` for the frozen benchmark specification.

---

# Run the Benchmark

From the OpenLLMBench repository root:

```powershell
python runner\run_benchmark.py
```

A normal successful run follows:

```text
Environment Verification
        ↓
Hardware Evidence Capture
        ↓
Benchmark Readiness Guidance
        ↓
Three Benchmark Runs
        ↓
Result Parsing
        ↓
submission.json
        ↓
Canonical Submission Validation
        ↓
Upload-Ready ZIP
```

For best consistency:

- allow the system to reach a normal idle state;
- close unnecessary heavy applications or workloads;
- avoid changing GPU clocks or power settings during the run.

Benchmark Protocol v1.0 does not require a fixed cooldown period.

---

# What the Runner Collects

The Runner automatically collects:

```text
cpu.txt
memory.txt
system.txt
windows.txt
nvidia-smi.txt
```

It creates three raw benchmark outputs:

```text
benchmark-v1.0-p512-run1.txt
benchmark-v1.0-p512-run2.txt
benchmark-v1.0-p512-run3.txt
```

It then generates `submission.json` and validates the completed workspace using the canonical OpenLLMBench submission validator.

A ZIP package is created only when validation passes.

---

# Runner Output

Successful submissions are written under:

```text
C:\AI-Benchmark\results\
```

The Runner uses a controlled submission name based on the benchmark system, detected GPU, and timestamp.

A successful run produces:

```text
C:\AI-Benchmark\results\
    <machine>-<GPU>-<timestamp>\
        benchmark-v1.0-p512-run1.txt
        benchmark-v1.0-p512-run2.txt
        benchmark-v1.0-p512-run3.txt
        cpu.txt
        memory.txt
        nvidia-smi.txt
        submission.json
        system.txt
        windows.txt

    <machine>-<GPU>-<timestamp>.zip
```

The ZIP contains one top-level submission directory so standard extraction tools recreate a validator-ready submission folder.

The generated ZIP is the package intended for contribution.

---

# Submit the Generated ZIP

After the Runner completes successfully, submit the generated ZIP through the OpenLLMBench GitHub Issue submission workflow.

Upload the Runner-generated ZIP rather than manually rebuilding or editing the submission package.

Maintainers will:

1. review the submitted evidence;
2. independently validate the submission;
3. assign trusted provenance and verification metadata;
4. import accepted results into the canonical database;
5. republish generated website data.

Contributors do not directly modify the canonical OpenLLMBench database.

Follow any additional instructions in the current GitHub submission Issue template.

---

# Manual Validation

The Runner automatically validates its completed workspace before creating the ZIP.

For troubleshooting, development, or manually assembled submissions, run the canonical validator from the repository root:

```powershell
python -m parser.validate .\path\to\submission
```

Successful validation exits with status code `0`. Failed validation exits with status code `1` and reports the failed checks.

Do not modify raw benchmark output merely to make validation pass.

---

# If the Runner Stops

## Environment Verification Failure

If environment verification fails, benchmarking does not start. Correct the failed checks shown by the Runner and run it again.

Common areas include NVIDIA GPU or driver detection, missing benchmark assets, or incorrect SHA-256 values.

## Benchmark Execution Failure

If `llama-bench.exe` exits unsuccessfully, the Runner reports the exit code and preserves the raw benchmark output for troubleshooting.

## Result Parsing Failure

If required results cannot be parsed, the Runner stops and reports the preserved benchmark workspace.

## Submission Validation Failure

If the completed workspace fails canonical validation, the Runner does not create an upload-ready ZIP.

---

# Manual and Advanced Submission Work

The Runner is the preferred path for new benchmark contributions because it reduces configuration mistakes and automatically creates the required evidence package.

Developers and maintainers may still use manually assembled submissions for parser development, validator testing, historical data preservation, regression testing, protocol development, and troubleshooting.

Reference material is available in `example_submission/`, and the frozen benchmark protocol is documented in `docs/benchmark_v1.md`.

Raw benchmark evidence should remain traceable to the original benchmark execution.

---

# Benchmark Integrity

When contributing benchmark results:

- do not edit raw benchmark output;
- do not falsify hardware evidence;
- do not substitute different benchmark assets while presenting the result as the frozen protocol;
- disclose significant hardware modifications when appropriate;
- preserve unusual or failed benchmark behavior when it may help troubleshooting;
- allow maintainers to independently validate submitted evidence.

Factory settings are recommended. See `docs/benchmark_v1.md` for the frozen protocol requirements.

---

# Other Ways to Contribute

Contributions are also welcome in bug reporting, Runner testing, GPU and platform testing, documentation, accessibility, hardware normalization, analytics, website development, design, feature proposals, and code improvements.

Keep the project's core principles in mind:

> Measure. Understand. Preserve.

---

# Maintainer Workflow

Trusted database ingestion is intentionally separate from the contributor workflow.

Maintainers should use `docs/MAINTAINER_WORKFLOW.md` for the validate, stage, targeted import, and publishing procedure.

Contributor-supplied metadata should never be treated as trusted maintainer provenance.

---

# Current Development Direction

The current Runner automates benchmark execution and validated submission packaging, but contributor UX remains under active development.

Planned improvements include:

- standalone OpenLLMBench Runner executable packaging;
- reduced or eliminated Python setup for contributors;
- simpler dependency/bootstrap handling;
- improved upload workflow;
- broader hardware support;
- continued Runner regression testing.

The long-term goal is a low-friction benchmark experience while preserving transparent raw evidence and maintainer-controlled ingestion.
