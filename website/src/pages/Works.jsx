import { motion } from "motion/react";

import Layout from "../layout/Layout";
import PageMeta from "../components/PageMeta";


const workTypes = [
    {
        label: "Experiment",
        description:
            "Controlled tests that explore a specific question " +
            "about local AI hardware.",
    },
    {
        label: "Finding",
        description:
            "Patterns and conclusions supported by published " +
            "OpenLLMWorks benchmark data.",
    },
    {
        label: "Research Note",
        description:
            "Focused observations that are useful without " +
            "requiring a full experiment.",
    },
    {
        label: "Work in Progress",
        description:
            "Early research, new hardware coverage, and questions " +
            "we are actively investigating.",
    },
];


function Works() {
    return (
        <Layout>
            <PageMeta
                title="The Works | Local AI Hardware Research | OpenLLMWorks"
                description="Explore experiments, findings, and research notes from OpenLLMWorks using real-world local AI hardware benchmark data."
                canonical="/works"
            />

            <div className="works-page">
                <motion.section
                    className="works-hero"
                    initial={{ opacity: 0, y: 24 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{
                        duration: 0.55,
                        ease: [0.22, 1, 0.36, 1],
                    }}
                >
                    <p className="works-eyebrow">
                        THE WORKS
                    </p>

                    <h1>
                        Experiments, findings, and notes
                        from the OpenLLMWorks lab.
                    </h1>

                    <p className="works-lead">
                        Exploring what real-world benchmark data
                        can teach us about local AI hardware.
                    </p>
                </motion.section>

                <motion.section
                    className="works-feature"
                    initial={{ opacity: 0, y: 24 }}
                    whileInView={{ opacity: 1, y: 0 }}
                    viewport={{
                        once: true,
                        amount: 0.25,
                    }}
                    transition={{
                        duration: 0.55,
                        ease: [0.22, 1, 0.36, 1],
                    }}
                >
                    <div className="works-feature-meta">
                        <span>FIRST EXPERIMENT</span>
                        <strong>Coming Soon</strong>
                    </div>

                    <div className="works-feature-content">
                        <div>
                            <p className="works-eyebrow">
                                EXPERIMENT
                            </p>

                            <h2>
                                How far back can modern local AI go?
                            </h2>

                            <p>
                                OpenLLMWorks is building a historical
                                record that reaches beyond current
                                generation GPUs. Our first experiments
                                will explore what happens when modern
                                local LLM workloads meet older
                                consumer hardware.
                            </p>
                        </div>

                        <div className="works-feature-question">
                            <span>THE QUESTION</span>

                            <p>
                                How useful is older hardware for
                                running a modern local AI workload,
                                and where does performance begin to
                                break down?
                            </p>
                        </div>
                    </div>
                </motion.section>

                <section className="works-library">
                    <div className="works-section-heading">
                        <p className="works-eyebrow">
                            FROM THE LAB
                        </p>

                        <h2>
                            More than a benchmark leaderboard.
                        </h2>

                        <p>
                            The Works is where OpenLLMWorks turns
                            measurements into experiments,
                            observations, and research questions.
                        </p>
                    </div>

                    <div className="works-type-grid">
                        {workTypes.map((type, index) => (
                            <article
                                className="works-type-card"
                                key={type.label}
                            >
                                <span>
                                    {String(index + 1).padStart(
                                        2,
                                        "0",
                                    )}
                                </span>

                                <h3>{type.label}</h3>

                                <p>{type.description}</p>
                            </article>
                        ))}
                    </div>
                </section>

                <section className="works-principle">
                    <p className="works-eyebrow">
                        BUILT ON THE DATA
                    </p>

                    <blockquote>
                        The benchmark database tells us what
                        happened. The Works explores what it means.
                    </blockquote>

                    <p>
                        Research published here will be grounded in
                        validated OpenLLMWorks results and the
                        methodology used to produce them.
                    </p>
                </section>
            </div>
        </Layout>
    );
}


export default Works;