import Layout from "../layout/Layout";

import Hero from "../components/Hero";
import MetricCard from "../components/MetricCard";
import CommunityStory from "../components/CommunityStory";

import { metrics } from "../data/homepage";

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

            <CommunityStory />
        </Layout>
    );
}

export default Home;