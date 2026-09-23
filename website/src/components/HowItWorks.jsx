import { motion } from "motion/react";

const stages = [
    {
        number: "01",
        title: "Run",
        copy:
            "Run the standardized OpenLLMWorks benchmark locally. " +
            "The Runner captures benchmark results and relevant " +
            "system metadata.",
    },
    {
        number: "02",
        title: "Validate",
        copy:
            "The submission is checked against the benchmark " +
            "protocol and validation requirements before it enters " +
            "the dataset.",
    },
    {
        number: "03",
        title: "Publish",
        copy:
            "Approved results are imported and published as part " +
            "of the OpenLLMWorks hardware database.",
    },
];

function HowItWorks() {
    return (
        <motion.section
            className="how-it-works"
            initial={{ opacity: 0, y: 24 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true, amount: 0.2 }}
            transition={{
                duration: 0.55,
                ease: [0.22, 1, 0.36, 1],
            }}
        >
            <div className="how-it-works-header">
                <p className="how-it-works-eyebrow">
                    HOW IT WORKS
                </p>

                <h2>
                    From your hardware to the public dataset.
                </h2>

                <p className="how-it-works-intro">
                    Every published result follows the same path
                    through the OpenLLMWorks benchmark process.
                </p>
            </div>

            <div className="how-it-works-pipeline">
                {stages.map((stage, index) => (
                    <motion.article
                        className="how-it-works-stage"
                        key={stage.number}
                        initial={{
                            opacity: 0,
                            y: 20,
                        }}
                        whileInView={{
                            opacity: 1,
                            y: 0,
                        }}
                        viewport={{
                            once: true,
                            amount: 0.4,
                        }}
                        transition={{
                            duration: 0.5,
                            delay: index * 0.12,
                            ease: [0.22, 1, 0.36, 1],
                        }}
                    >
                        <div className="how-it-works-stage-top">
                            <span className="how-it-works-number">
                                {stage.number}
                            </span>

                            <span className="how-it-works-line" />
                        </div>

                        <h3>{stage.title}</h3>

                        <p>{stage.copy}</p>
                    </motion.article>
                ))}
            </div>

            <div className="how-it-works-methodology">
                <div>
                    <strong>
                        Want to understand the benchmark itself?
                    </strong>

                    <span>
                        Protocol design, workload selection,
                        limitations, and reproducibility.
                    </span>
                </div>

                <span
                    className="how-it-works-methodology-link"
                    aria-disabled="true"
                >
                    Methodology coming soon
                </span>
            </div>
        </motion.section>
    );
}

export default HowItWorks;