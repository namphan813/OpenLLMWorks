import { Link, useParams } from "react-router-dom";

import Layout from "../layout/Layout";
import PageMeta from "../components/PageMeta";
import WorksNotFound from "../components/WorksNotFound";
import {
    getWorksArticle,
} from "../content/works/articles";


function WorksArticle() {
    const { slug } = useParams();
    const article = getWorksArticle(slug);

    if (!article) {
        return (
            <Layout>
                <PageMeta
                    title="Research Not Found | The Works | OpenLLMWorks"
                    description="The requested OpenLLMWorks research entry could not be found."
                    canonical={`/works/${slug}`}
                />

                <WorksNotFound />
            </Layout>
        );
    }

    return (
        <Layout>
            <PageMeta
                title={`${article.title} | The Works | OpenLLMWorks`}
                description={article.description}
                canonical={`/works/${article.slug}`}
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

                {article.summary && (
                    <section className="works-article-summary">
                        <p className="works-eyebrow">
                            {article.summary.heading.toUpperCase()}
                        </p>

                        <p className="works-article-summary-intro">
                            {article.summary.intro}
                        </p>

                        <div className="works-article-summary-grid">
                            {article.summary.items.map((item) => (
                                <div
                                    className="works-article-summary-item"
                                    key={item.label}
                                >
                                    <span>{item.label}</span>

                                    <h2>{item.title}</h2>

                                    <p>{item.body}</p>
                                </div>
                            ))}
                        </div>
                    </section>
                )}

                <div className="works-article-body">
                    {article.sections.map((section) => (
                        <section key={section.heading}>
                            <h2>{section.heading}</h2>

                            {section.paragraphs.map(
                                (paragraph, index) => (
                                    <p key={index}>
                                        {paragraph}
                                    </p>
                                ),
                            )}
                        </section>
                    ))}

                    {article.note && (
                        <aside className="works-article-note">
                            <strong>
                                {article.note.heading}
                            </strong>

                            <p>{article.note.body}</p>
                        </aside>
                    )}
                </div>
            </article>
        </Layout>
    );
}


export default WorksArticle;