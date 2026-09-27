const worksArticles = {
    "how-far-back-can-modern-local-ai-go": {
        slug: "how-far-back-can-modern-local-ai-go",
        type: "Experiment",
        status: "In Progress",
        visibility: "private",
        featured: true,
        title: "How far back can modern local AI go?",
        description:
            "An OpenLLMWorks experiment exploring how older " +
            "consumer GPUs handle a modern local AI workload.",
        question:
            "How useful is older hardware for running a modern " +
            "local AI workload, and where does performance begin " +
            "to break down?",
        sections: [
            {
                heading: "Why we're testing this",
                paragraphs: [
                    "Local AI hardware discussions tend to focus " +
                        "on current GPUs. OpenLLMWorks is also " +
                        "interested in the hardware people already " +
                        "own, including older consumer cards that " +
                        "predate today's local AI ecosystem.",
                    "This experiment will use the standard " +
                        "OpenLLMWorks benchmark protocol to examine " +
                        "how far back modern local AI workloads " +
                        "remain practical.",
                ],
            },
            {
                heading: "What we're measuring",
                paragraphs: [
                    "Results will be grounded in validated " +
                        "OpenLLMWorks benchmark data, including " +
                        "prompt processing and token generation " +
                        "performance under the frozen benchmark " +
                        "methodology.",
                ],
            },
        ],
        note: {
            heading: "Experiment in progress",
            body:
                "This article framework is live while the " +
                "underlying experiment is still being developed. " +
                "Findings will be added only after supporting " +
                "benchmark results have been validated and " +
                "published.",
        },
    },
};


export function getWorksArticle(slug) {
    return worksArticles[slug] ?? null;
}


export function getWorksArticles() {
    return Object.values(worksArticles);
}


export function getPublicWorksArticles() {
    return getWorksArticles().filter(
        (article) => article.visibility === "public",
    );
}


export function getFeaturedWorksArticle() {
    return (
        getWorksArticles().find(
            (article) => article.featured,
        ) ?? null
    );
}


export default worksArticles;
