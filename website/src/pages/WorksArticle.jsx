import { Link, useParams } from "react-router-dom";

import Layout from "../layout/Layout";
import PageMeta from "../components/PageMeta";


const articles = {
    "how-far-back-can-modern-local-ai-go": {
        type: "Experiment",
        status: "In Progress",
        title: "How far back can modern local AI go?",
        description:
            "An OpenLLMWorks experiment exploring how older " +
            "consumer GPUs handle a modern local AI workload.",
        question:
            "How useful is older hardware for running a modern " +
            "local AI workload, and where does performance begin " +
            "to break down?",
    },
};


function WorksArticle() {
    const { slug } = useParams();
    const article = articles[slug];

    if (!article) {
        return (
            <Layout>
                <div className="works-article-page">
                    <Link
                        className="works-article-back"
                        to="/works"
                    >
                        ← The Works
                    </Link>

                    <h1>Research note not found.</h1>

                    <p>
                        This Works entry does not exist or has not
                        been published yet.
                    </p>
                </div>
            </Layout>
        );
    }

    return (
        <Layout>
            <PageMeta
                title={`${article.title} | The Works | OpenLLMWorks`}
                description={article.description}
                canonical={`/works/${slug}`}
            />

            <article className="works-article-page">
                <header className="works-article-header">
                    <Link
                        className="works-article-back"
                        to="/works"
                    >
                        ← The Works
                    </Link>

                    <div className="works-article-meta">
                        <span>{article.type}</span>
                        <span>{article.status}</span>
                    </div>

                    <h1>{article.title}</h1>

                    <p className="works-article-dek">
                        {article.description}
                    </p>
                </header>

                <section className="works-article-question">
                    <p className="works-eyebrow">
                        THE QUESTION
                    </p>

                    <p>{article.question}</p>
                </section>

                <div className="works-article-body">
                    <section>
                        <h2>Why we're testing this</h2>

                        <p>
                            Local AI hardware discussions tend to
                            focus on current GPUs. OpenLLMWorks is
                            also interested in the hardware people
                            already own, including older consumer
                            cards that predate today's local AI
                            ecosystem.
                        </p>

                        <p>
                            This experiment will use the standard
                            OpenLLMWorks benchmark protocol to
                            examine how far back modern local AI
                            workloads remain practical.
                        </p>
                    </section>

                    <section>
                        <h2>What we're measuring</h2>

                        <p>
                            Results will be grounded in validated
                            OpenLLMWorks benchmark data, including
                            prompt processing and token generation
                            performance under the frozen benchmark
                            methodology.
                        </p>
                    </section>

                    <aside className="works-article-note">
                        <strong>Experiment in progress</strong>

                        <p>
                            This article framework is live while the
                            underlying experiment is still being
                            developed. Findings will be added only
                            after supporting benchmark results have
                            been validated and published.
                        </p>
                    </aside>
                </div>
            </article>
        </Layout>
    );
}


export default WorksArticle;