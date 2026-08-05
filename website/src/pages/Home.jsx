import Layout from "../layout/Layout";

import Hero from "../components/Hero";
import MetricCard from "../components/MetricCard";
import CommunityStory from "../components/CommunityStory";

import {
    metrics,
    communityStory,
} from "../data/homepage";

function Home() {
    return (
        <Layout>
            <Hero />

            <section className="metrics">
                {metrics.map((metric) => (
                    <MetricCard
                        key={metric.label}
                        label={metric.label}
                        value={metric.value}
                        detail={metric.detail}
                    />
                ))}
            </section>

            <CommunityStory
                eyebrow={communityStory.eyebrow}
                badge={communityStory.badge}
                title={communityStory.title}
                description={communityStory.description}
                evidence={communityStory.evidence}
            />
        </Layout>
    );
}

export default Home;