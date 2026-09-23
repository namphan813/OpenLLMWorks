import { useEffect, useState } from "react";
import { motion } from "motion/react";

import Layout from "../layout/Layout";
import BenchmarkHighlights from "../components/BenchmarkHighlights";


const protocolFacts = [
    {
        label: "Protocol",
        value: "v1.0",
        detail: "OLBD-BP-1.0",
    },
    {
        label: "Model",
        value: "Qwen3-4B",
        detail: "Q4_K_M",
    },
    {
        label: "Runtime",
        value: "llama.cpp",
        detail: "Build 10069",
    },
    {
        label: "Prompt",
        value: "pp512",
        detail: "512 tokens",
    },
    {
        label: "Generation",
        value: "tg128",
        detail: "128 tokens",
    },
    {
        label: "Runs",
        value: "3",
        detail: "Arithmetic average",
    },
];


function Methodology() {
    const [hardware, setHardware] = useState([]);

    useEffect(() => {
        const hardwareDataUrl =
            `${import.meta.env.BASE_URL}hardware.json`;

        async function loadPublishedHardware() {
            try {
                const response = await fetch(
                    hardwareDataUrl,
                );

                if (!response.ok) {
                    throw new Error(
                        `Hardware data request failed: ` +
                        `${response.status}`,
                    );
                }

                const hardwareData =
                    await response.json();

                if (!Array.isArray(hardwareData.hardware)) {
                    throw new Error(
                        "Published hardware data does not " +
                        "contain a hardware list.",
                    );
                }

                setHardware(hardwareData.hardware);
            } catch (error) {
                console.error(
                    "Unable to load published hardware data.",
                    error,
                );
            }
        }

        loadPublishedHardware();
    }, []);

    return (
        <Layout>
            <div className="methodology-page">
                <motion.section
                    className="methodology-hero"
                    initial={{ opacity: 0, y: 24 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{
                        duration: 0.55,
                        ease: [0.22, 1, 0.36, 1],
                    }}
                >
                    <p className="methodology-eyebrow">
                        BENCHMARK METHODOLOGY
                    </p>

                    <h1>
                        A reproducible baseline for measuring
                        local AI hardware.
                    </h1>

                    <p className="methodology-lead">
                        OpenLLMWorks uses a fixed benchmark workload
                        so results collected across different systems
                        remain meaningful, comparable, and useful over
                        time.
                    </p>

                    <div className="methodology-status">
                        <span>PROTOCOL v1.0</span>
                        <strong>Frozen</strong>
                    </div>
                </motion.section>

                <section className="methodology-protocol">
                    <div className="methodology-section-heading">
                        <p className="methodology-eyebrow">
                            CURRENT PROTOCOL
                        </p>

                        <h2>One workload. One baseline.</h2>

                        <p>
                            Benchmark Protocol v1.0 fixes the model,
                            runtime, benchmark parameters, and execution
                            requirements used for published results.
                            Future protocol generations can evolve
                            without changing what historical v1.0
                            results mean.
                        </p>
                    </div>

                    <div className="methodology-facts">
                        {protocolFacts.map((fact, index) => (
                            <motion.article
                                className="methodology-fact"
                                key={fact.label}
                                initial={{
                                    opacity: 0,
                                    y: 18,
                                }}
                                whileInView={{
                                    opacity: 1,
                                    y: 0,
                                }}
                                viewport={{
                                    once: true,
                                    amount: 0.35,
                                }}
                                transition={{
                                    duration: 0.45,
                                    delay: index * 0.06,
                                    ease: [0.22, 1, 0.36, 1],
                                }}
                            >
                                <span>{fact.label}</span>
                                <strong>{fact.value}</strong>
                                <small>{fact.detail}</small>
                            </motion.article>
                        ))}
                    </div>

                    <p className="methodology-protocol-note">
                        Protocol v1.0 uses llama.cpp commit
                        178a6c449, build 10069, with the CUDA
                        backend.
                    </p>
                </section>

                <section className="methodology-content">
                    <article className="methodology-block">
                        <p className="methodology-eyebrow">
                            WHY QWEN3-4B?
                        </p>

                        <h2>
                            Broad hardware coverage without reducing
                            the benchmark to a synthetic test.
                        </h2>

                        <p>
                            The reference workload needs to work
                            across a wide range of local AI hardware.
                            A model that is too large would exclude
                            much of the older and lower-VRAM hardware
                            that OpenLLMWorks is designed to preserve
                            and compare.
                        </p>

                        <p>
                            Qwen3-4B occupies a useful middle ground:
                            compact enough to provide meaningful
                            coverage toward the lower end of the
                            hardware stack, while still representing
                            the kind of modern LLM workload someone
                            might genuinely run locally.
                        </p>

                        <p>
                            OpenLLMWorks is therefore benchmarking
                            hardware running a real local AI workload.
                            It is not intended to rank which language
                            model is the smartest.
                        </p>
                    </article>

                    <article className="methodology-block">
                        <p className="methodology-eyebrow">
                            WHAT WE MEASURE
                        </p>

                        <h2>
                            Prompt processing and token generation
                            tell different parts of the story.
                        </h2>

                        <div className="methodology-metrics">
                            <div>
                                <strong>pp512</strong>
                                <span>Prompt Processing</span>

                                <p>
                                    Measures throughput while
                                    processing a 512-token prompt,
                                    reported in tokens per second.
                                </p>
                            </div>

                            <div>
                                <strong>tg128</strong>
                                <span>Token Generation</span>

                                <p>
                                    Measures throughput while
                                    generating 128 output tokens,
                                    reported in tokens per second.
                                </p>
                            </div>
                        </div>
                    </article>

                    <article className="methodology-block">
                        <p className="methodology-eyebrow">
                            REPRODUCIBILITY
                        </p>

                        <h2>
                            Preserve the conditions, not just the
                            score.
                        </h2>

                        <p>
                            Every new Protocol v1.0 submission
                            completes three independent benchmark
                            runs. The published score is the
                            arithmetic average, while the individual
                            raw outputs are retained for verification.
                        </p>

                        <p>
                            Submissions also capture relevant system
                            information including CPU, installed
                            memory, operating system, GPU, driver,
                            and CUDA information. That evidence helps
                            keep published results traceable to the
                            hardware and environment that produced
                            them.
                        </p>
                    </article>

                    <article className="methodology-block">
                        <p className="methodology-eyebrow">
                            CURRENT LIMITATIONS
                        </p>

                        <h2>
                            A controlled baseline is intentionally
                            narrower than the entire local AI
                            ecosystem.
                        </h2>

                        <p>
                            Protocol v1.0 currently represents a
                            single Qwen3-4B Q4_K_M workload using a
                            frozen llama.cpp build and the CUDA
                            backend. The protocol is currently
                            validated on Windows 11.
                        </p>

                        <p>
                            That makes v1.0 useful for controlled
                            comparisons, but it does not claim to
                            represent every model, quantization,
                            operating system, inference backend, or
                            local AI workload.
                        </p>
                    </article>

                    <article className="methodology-block">
                        <p className="methodology-eyebrow">
                            FUTURE PROTOCOLS
                        </p>

                        <h2>
                            Evolve the benchmark without rewriting
                            its history.
                        </h2>

                        <p>
                            Future OpenLLMWorks protocols may expand
                            hardware and software coverage, explore
                            additional workload sizes, and support
                            additional inference backends or
                            operating systems.
                        </p>

                        <p>
                            Those additions should be introduced
                            deliberately. Protocol v1.0 remains
                            frozen so its results retain the same
                            meaning as the project grows.
                        </p>
                    </article>
                </section>
            </div>

            <BenchmarkHighlights hardware={hardware} />
        </Layout>
    );
}

export default Methodology;