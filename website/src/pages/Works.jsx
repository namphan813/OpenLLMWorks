import { Link } from "react-router-dom";
import { motion } from "motion/react";

import Layout from "../layout/Layout";
import PageMeta from "../components/PageMeta";
import {
    getFeaturedWorksArticle,
    getPublicWorksArticles,
} from "../content/works/articles";


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
    const featuredArticle = getFeaturedWorksArticle();
    const publicArticles = getPublicWorksArticles();

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

                {featuredArticle && (
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
                            <strong>
                                {featuredArticle.visibility === "public"
                                    ? featuredArticle.status
                                    : "Coming Soon"}
                            </strong>
                        </div>

                        <div className="works-feature-content">
                            <div>
                                <p className="works-eyebrow">
                                    {featuredArticle.type.toUpperCase()}
                                </p>

                                <h2>
                                    {featuredArticle.title}
                                </h2>

                                <p>
                                    {featuredArticle.description}
                                </p>
                            </div>

                            <div className="works-feature-question">
                                <span>THE QUESTION</span>

                                <p>
                                    {featuredArticle.question}
                                </p>
                            </div>
                        </div>
                    </motion.section>
                )}

                {publicArticles.length > 0 && (
                    <section className="works-published">
                        <div className="works-section-heading">
                            <p className="works-eyebrow">
                                PUBLISHED RESEARCH
                            </p>

                            <h2>
                                From benchmark data to understanding.
                            </h2>

                            <p>
                                Notes, findings, and experiments
                                published from the OpenLLMWorks lab.
                            </p>
                        </div>

                        <div className="works-published-grid">
                            {publicArticles.map((article) => (
                                <Link
                                    className="works-published-card"
                                    key={article.slug}
                                    to={`/works/${article.slug}`}
                                >
                                    <div className="works-published-meta">
                                        <span>
                                            {article.type.toUpperCase()}
                                        </span>

                                        <strong>
                                            {article.status}
                                        </strong>
                                    </div>

                                    <h3>{article.title}</h3>

                                    <p>{article.description}</p>

                                    <span className="works-published-link">
                                        Read the research →
                                    </span>
                                </Link>
                            ))}
                        </div>
                    </section>
                )}

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