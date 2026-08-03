# Open LLM Benchmark Database (OLBD)

An open-source benchmark database for measuring Large Language Model (LLM) inference performance across consumer, workstation, laptop, and enterprise hardware.

The goal of OLBD is to provide a standardized, transparent, and reproducible benchmark protocol that allows meaningful hardware comparisons for local LLM inference.

---

## Why OLBD?

Benchmark results for local LLM inference are scattered across forums, Reddit posts, YouTube videos, and personal blogs. Different models, quantizations, software versions, and benchmark settings often make direct comparisons impossible.

OLBD solves this problem by providing:

- A frozen benchmark protocol
- Transparent benchmark methodology
- Reproducible results
- Open benchmark data
- Community contributions
- Historical benchmark preservation

Every benchmark submitted to OLBD follows the same protocol, making results directly comparable.

---

## Project Goals

- Build a community-driven benchmark database.
- Standardize local LLM benchmarking.
- Help users choose hardware for local AI workloads.
- Preserve benchmark history across protocol versions.
- Provide an open dataset for analysis and visualization.

---

## Current Status

| Item | Status |
|------|--------|
| Benchmark Protocol v1.0 | ✅ Complete |
| Initial Hardware Database | 🚧 In Progress |
| Parser | 🚧 Planned |
| Leaderboards | 🚧 Planned |
| Website | 🚧 Planned |
| Community Submissions | 🚧 Planned |

---

## Benchmark Protocol

Current Protocol:

**OLBD-BP-1.0**

Benchmark Software:

- llama.cpp
- CUDA Backend

Model:

- Qwen3-4B-Q4_K_M.gguf

Benchmark Parameters:

- Prompt Tokens: 512
- Generation Tokens: 128
- Three benchmark runs
- Average score reported

Additional benchmark details are available in:

```
docs/benchmark_v1.md
```

---

## Current Hardware

Current benchmark database includes:

- NVIDIA GeForce RTX 4070
- NVIDIA GeForce RTX 3060
- NVIDIA RTX A3000 Laptop GPU
- NVIDIA GeForce GTX 1650
- NVIDIA Quadro T1000
- NVIDIA Quadro P1000

Additional hardware is continuously being added.

---

## Repository Structure

```
OpenLLMBench/

benchmark_database/
docs/
hardware/
parser/
scripts/
website/
```

---

## Roadmap

### Phase 1

- [x] Freeze Benchmark Protocol v1.0
- [x] Initial repository structure

### Phase 2

- [ ] Benchmark database
- [ ] JSON schema
- [ ] Automatic parser

### Phase 3

- [ ] Hardware leaderboards
- [ ] Performance comparisons
- [ ] Price/performance metrics

### Phase 4

- [ ] Website
- [ ] Community benchmark submissions
- [ ] Automated benchmark validation

---

## Contributing

Community contributions are planned for a future release.

Contribution guidelines will be published once the parser and submission workflow are complete.

---

## License

License information will be added prior to the first public release.

---

## Project Status

OLBD is currently under active development.

The benchmark protocol is considered stable; however, the repository structure, parser, and website are still evolving.

Development of OpenLLMBench has been supported by AI-assisted planning, coding, and documentation. See [ACKNOWLEDGMENTS.md](ACKNOWLEDGMENTS.md).