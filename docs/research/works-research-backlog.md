\# The Works Research Backlog



Internal research notes for potential OpenLLMWorks experiments,

findings, and research notes.



This document is not published website content. It records observations

from validated benchmark data, questions worth investigating, and

additional evidence needed before conclusions are published in The Works.



\## Research principles



\- Start with validated OpenLLMWorks benchmark results.

\- Separate observations from explanations.

\- Do not infer causation from a small number of results.

\- Prefer controlled comparisons on the same benchmark system when possible.

\- Record missing evidence explicitly.

\- Treat unexpected or failed benchmark runs as potentially useful evidence.

\- Publish conclusions only when the available data supports them.



\---



\## Pascal vs. Turing GTX prompt processing



\*\*Status:\*\* Investigating



\### Research question



Why do current OpenLLMWorks results show substantially stronger PP512

performance on some Pascal GTX GPUs than on Turing GTX GPUs, while TG128

performance does not follow the same pattern?



\### Current observation



A controlled Bench-001 comparison currently shows:



| GPU | Architecture | PP512 | TG128 |

| --- | --- | ---: | ---: |

| GTX 1070 Ti 8 GB | Pascal | 1162.10 | 57.17 |

| GTX 1660 Ti 6 GB | Turing | 289.10 | 76.38 |



The GTX 1070 Ti is approximately four times faster in PP512, while the

GTX 1660 Ti is faster in TG128.



Additional results suggest that this may not be isolated to these two

cards:



| GPU | Architecture | PP512 | TG128 |

| --- | --- | ---: | ---: |

| GTX 1050 Ti 4 GB | Pascal | 348.04 | 22.11 |

| Quadro P1000 4 GB | Pascal | 211.03 | 13.99 |

| GTX 1650 4 GB | Turing | 153.58 avg | 35.29 avg |

| Quadro T1000 4 GB | Turing | 132.78 avg | 29.21 avg |



These additional systems are not all controlled comparisons and should

be treated as supporting observations rather than proof of an

architecture-level effect.



\### Relevant result IDs



\- GTX 1070 Ti:

&#x20; `result\_b86c443089518944`

\- GTX 1660 Ti, Bench-001:

&#x20; `result\_b84a1e21fdb0ccfa`

\- GTX 1050 Ti:

&#x20; `result\_dc6fdd4e1cbb5176`

\- Quadro P1000:

&#x20; `result\_a66ff7ef3577be89`

\- Quadro T1000:

&#x20; `result\_0200fb0ee70bb08a`

&#x20; and `result\_77913dd17782a6ce`



\### Additional evidence wanted



\- GTX 1060 3 GB on Bench-001

\- GTX 1060 6 GB

\- Additional GTX 16-series results

\- RTX 20-series Turing result for comparison

\- Repeat or controlled runs where useful



\### Possible explanations to investigate



These are hypotheses only and should not be presented as conclusions.



\- Memory bandwidth or memory subsystem differences

\- Differences in compute characteristics between Pascal and Turing

\- llama.cpp CUDA kernel behavior

\- Differences between prompt processing and token generation workloads

\- VRAM capacity or model offload behavior

\- Driver or CUDA runtime differences



\---



\## How far back can modern local AI go?



\*\*Status:\*\* Collecting hardware



\### Research question



How old can consumer GPU hardware become before the standard

OpenLLMWorks Protocol v1.0 workload stops being useful or stops

completing successfully?



\### Current observation



The GTX 970 4 GB successfully completes Protocol v1.0:



| GPU | PP512 | TG128 |

| --- | ---: | ---: |

| GTX 970 4 GB | 331.15 | 28.76 |



This provides a useful older baseline, but the lower boundary has not

yet been established.



\### Relevant result IDs



\- GTX 970:

&#x20; `result\_8e055302f50da311`



\### Hardware wanted



\- GTX 750

\- GTX 750 Ti

\- GT 1030



Additional older supported GPUs may be useful if acquired inexpensively.



\### Experimental principle



Protocol v1.0 should not be modified to make older hardware pass.



If a GPU cannot successfully complete the frozen benchmark workload,

that failure may itself establish an important boundary.



\---



\## VRAM-constrained local AI performance



\*\*Status:\*\* Early observation



\### Research question



What happens to Protocol v1.0 performance as GPU VRAM becomes

insufficient to comfortably contain the workload?



\### Current observation



Current Pascal results include:



| GPU | VRAM | PP512 | TG128 |

| --- | ---: | ---: | ---: |

| GTX 1050 | 2 GB | 125.14 | 3.99 |

| GTX 1050 Ti | 4 GB | 348.04 | 22.11 |



The very low TG128 result on the 2 GB GTX 1050 makes low-VRAM behavior

worth investigating.



These cards differ in more than VRAM capacity, so the difference cannot

be attributed to VRAM alone.



\### Relevant result IDs



\- GTX 1050:

&#x20; `result\_a64036c1c64f3997`

\- GTX 1050 Ti:

&#x20; `result\_dc6fdd4e1cbb5176`



\### Additional evidence wanted



\- GTX 1060 3 GB

\- GTX 1060 6 GB

\- Other comparable GPUs with differing VRAM capacities



\---



\## RTX 2050 prompt-processing result



\*\*Status:\*\* Observation



\### Research question



Why does the low-end RTX 2050 produce unusually high PP512 performance

relative to several older GTX GPUs?



\### Current observation



The published RTX 2050 result is:



| GPU | VRAM | PP512 | TG128 |

| --- | ---: | ---: | ---: |

| RTX 2050 | 4 GB | 1634.20 | 37.42 |



The PP512 result is higher than the current GTX 1070 Ti result despite

the RTX 2050 being a low-end mobile GPU.



The RTX 2050 was tested on a different host system, so this result

should currently be treated as an interesting observation rather than

a controlled generational comparison.



\### Relevant result IDs



\- RTX 2050:

&#x20; `result\_9dc8fe61d363dd7b`



\### Additional evidence wanted



\- RTX 2060

\- Additional RTX 20-series results

\- Comparable controlled-system testing if suitable hardware becomes

&#x20; available



\---



\## Candidate Works stories



Potential stories should remain provisional until their supporting

experiments are complete.



\### Experiment



\*\*How far back can modern local AI go?\*\*



Use the frozen OpenLLMWorks benchmark protocol to progressively test

older GPU generations until a practical or technical boundary emerges.



\### Research Note



\*\*Pascal vs. Turing: An unexpected prompt-processing result\*\*



Document the PP512/TG128 crossover observed in current GTX results

without assigning a cause until additional evidence is available.



\### Finding



A finding should be created only if further controlled testing supports

a defensible explanation for one of the observed performance patterns.



\---



\## Acquisition watchlist



Hardware with unusually high research value:



\- GTX 750 / GTX 750 Ti

\- GT 1030

\- GTX 1060 3 GB

\- GTX 1060 6 GB

\- GTX 1080 Ti

\- RTX 2060

\- Additional GTX 16-series cards when inexpensive



Acquisitions should prioritize filling meaningful gaps in the dataset

rather than collecting every model in a product family.