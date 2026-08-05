import Navigation from "../layout/Navigation";
import Hero from "../components/Hero";
import MetricCard from "../components/MetricCard";
import CommunityStory from "../components/CommunityStory";
import Footer from "../components/Footer";

import { metrics } from "../data/homepage";

function Home() {
    return (
        <>
            <Navigation />

            <main>
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
            </main>

            <Footer />
        </>
    );
}

export default Home;