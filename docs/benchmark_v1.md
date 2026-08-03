# Open LLM Benchmark Database (OLBD)

# Benchmark Protocol v1.0

**Protocol ID:** OLBD-BP-1.0

**Status:** Frozen

---

# Purpose

The Open LLM Benchmark Database (OLBD) is an open-source project designed to provide standardized, transparent, and reproducible benchmarks for running Large Language Models (LLMs) on consumer, workstation, and enterprise hardware.

The purpose of this benchmark is to allow fair hardware comparisons by using a fixed benchmark protocol across all tested systems.

Benchmark Protocol v1.0 is considered frozen. All benchmark results collected using this protocol are directly comparable.

Future protocol improvements will be released under new version numbers (v1.1, v2.0, etc.) while preserving historical benchmark data.

---

# Revision History

| Version | Date | Notes |
|----------|------------|--------------------------------------|
| 1.0 | 2026-07-25 | Initial frozen benchmark protocol |

---

# Benchmark Software

| Item | Value |
|------|-------|
| Software | llama.cpp |
| Commit | 178a6c449 |
| Build | 10069 |
| Backend | CUDA |

---

# Model Configuration

| Item | Value |
|------|-------|
| Model | Qwen3-4B-Q4_K_M.gguf |
| Quantization | Q4_K_M |
| Source | Official GGUF Release |

---

# Benchmark Parameters

| Parameter | Value |
|-----------|-------|
| Prompt Tokens | 512 |
| Generation Tokens | 128 |
| Prompt Processing | Enabled |
| Token Generation | Enabled |

---

# Benchmark Execution

Each benchmark submission must complete **three independent benchmark runs**.

The official benchmark score is calculated as the arithmetic average of all completed runs.

All raw benchmark outputs must be retained for verification purposes.

---

# Metric Definitions

## pp512

Prompt Processing throughput using a **512-token prompt**.

Reported as:

**Tokens per Second**

---

## tg128

Token Generation throughput while generating **128 output tokens**.

Reported as:

**Tokens per Second**

---

# Required System Information

Each benchmark submission must include:

- CPU information
- Installed memory
- Operating system
- GPU information
- NVIDIA driver version
- CUDA version (if available)

---

# Required Benchmark Files

Each benchmark submission should include the following files:

```
cpu.txt
memory.txt
system.txt
windows.txt
nvidia-smi.txt

benchmark-run1.txt
benchmark-run2.txt
benchmark-run3.txt
```

---

# Reported Results

Each benchmark submission reports:

- Prompt Processing (pp512)
- Token Generation (tg128)

The official benchmark score is calculated as the average of all benchmark runs.

Both the individual runs and the averaged results should be preserved.

---

# Legacy Benchmark Results

Some initial OLBD benchmark results were collected using two runs before
the three-run requirement was formally adopted.

These results may remain in the database if:

- Both raw run files are preserved.
- The number of completed runs is clearly recorded.
- The result is labeled as a legacy two-run benchmark.
- The arithmetic average is calculated only from the available valid runs.

All new Benchmark Protocol v1.0 submissions should complete three runs.

---

# Operating System

Benchmark Protocol v1.0 is currently validated on:

- Windows 11

Operating system build numbers are recorded as part of every benchmark submission.

Future protocol versions may add support for Linux and additional operating systems.

---

# Hardware Policy

Benchmark submissions should reflect real-world hardware performance.

The following guidelines apply:

- Factory settings are recommended.
- Overclocking is not required.
- Hardware modifications should be documented.
- Significant deviations from stock configurations should be disclosed.

---

# Data Integrity

To maintain transparency and reproducibility:

- Raw benchmark files should never be modified.
- Parsed benchmark data should always be traceable back to the original output.
- Failed or incomplete benchmark runs should be documented rather than deleted.
- Any unusual benchmark behavior should be noted when possible.

---

# Project Goals

The Open LLM Benchmark Database aims to:

- Build a transparent benchmark database for local LLM inference.
- Provide reproducible hardware comparisons.
- Help users evaluate hardware for running LLMs locally.
- Encourage community participation and benchmark submissions.
- Preserve historical benchmark results across protocol versions.

---

# License

This benchmark protocol is part of the Open LLM Benchmark Database (OLBD).

Benchmark Protocol v1.0 is identified by:

**OLBD-BP-1.0**