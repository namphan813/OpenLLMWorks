import "./App.css";

import Navigation from "./layout/Navigation";
import Hero from "./components/Hero";
import MetricCard from "./components/MetricCard";
import CommunityStory from "./components/CommunityStory";
import Footer from "./components/Footer";

function App() {
    return (
        <>
            <Navigation />

            <main>
                <Hero />

                <section className="metrics">
                    <MetricCard
                        label="Benchmark Results"
                        value="1"
                        detail="Unique result recorded"
                    />

                    <MetricCard
                        label="GPU Models"
                        value="1"
                        detail="Currently represented"
                    />

                    <MetricCard
                        label="Import Events"
                        value="4"
                        detail="3 duplicates blocked"
                    />

                    <MetricCard
                        label="Average tg128"
                        value="31.69"
                        detail="Tokens per second"
                    />
                </section>

                <CommunityStory />
            </main>

            <Footer />
        </>
    );
}

export default App;