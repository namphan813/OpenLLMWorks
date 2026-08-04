import "./App.css";

import Navigation from "./layout/Navigation";
import Hero from "./components/Hero";
import MetricCard from "./components/MetricCard";
import CommunityStory from "./components/CommunityStory";
import Footer from "./components/Footer";

const metrics = [
    {
        label: "Benchmark Results",
        value: "1",
        detail: "Unique result recorded",
    },
    {
        label: "GPU Models",
        value: "1",
        detail: "Currently represented",
    },
    {
        label: "Import Events",
        value: "4",
        detail: "3 duplicates blocked",
    },
    {
        label: "Average tg128",
        value: "31.69",
        detail: "Tokens per second",
    },
];

function App() {
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

export default App;