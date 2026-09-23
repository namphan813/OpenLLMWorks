import { useEffect, useState } from "react";

import Layout from "../layout/Layout";

import Hero from "../components/Hero";
import MetricCard from "../components/MetricCard";
import BenchmarkHighlights from "../components/BenchmarkHighlights";
import HowItWorks from "../components/HowItWorks";

import {
    metrics as fallbackMetrics,
} from "../data/homepage";


function formatNumber(value, digits = 2) {
    if (typeof value !== "number") {
        return "N/A";
    }

    return value.toFixed(digits);
}


function buildPublishedMetrics(stats) {
    return [
        {
            label: "Benchmark Results",
            value: stats.benchmarkResults,
            detail: "Unique results recorded",
        },
        {
            label: "GPU Models",
            value: stats.gpuModels,
            detail: "Currently represented",
        },
        {
            label: "Import Events",
            value: stats.importEvents,
            detail: "Import events recorded",
        },
        {
            label: "Average tg128",
            value: formatNumber(stats.averageTg128),
            detail: "Tokens per second",
        },
    ];
}


function Home() {
    const [metrics, setMetrics] = useState(
        fallbackMetrics,
    );

    const [hardware, setHardware] = useState([]);

    useEffect(() => {
        const homepageDataUrl =
            `${import.meta.env.BASE_URL}homepage.json`;

        const hardwareDataUrl =
            `${import.meta.env.BASE_URL}hardware.json`;

        async function loadPublishedHomepage() {
            try {
                const response = await fetch(
                    homepageDataUrl,
                );

                if (!response.ok) {
                    throw new Error(
                        `Homepage data request failed: ` +
                        `${response.status}`,
                    );
                }

                const homepageData =
                    await response.json();

                if (!homepageData.stats) {
                    throw new Error(
                        "Published homepage data does not " +
                        "contain stats.",
                    );
                }

                setMetrics(
                    buildPublishedMetrics(
                        homepageData.stats,
                    ),
                );
            } catch (error) {
                console.error(
                    "Unable to load published homepage data. " +
                    "Using fallback homepage data.",
                    error,
                );
            }
        }

        async function loadPublishedHardware() {
            try {
                const response = await fetch(
                    hardwareDataUrl,
                );

                if (!response.ok) {
                    throw new Error(
                        `Hardware data request failed: ` +
                        `${response.status}`,
                    );
                }

                const hardwareData =
                    await response.json();

                if (!Array.isArray(hardwareData.hardware)) {
                    throw new Error(
                        "Published hardware data does not " +
                        "contain a hardware list.",
                    );
                }

                setHardware(hardwareData.hardware);
            } catch (error) {
                console.error(
                    "Unable to load published hardware data.",
                    error,
                );
            }
        }

        loadPublishedHomepage();
        loadPublishedHardware();
    }, []);

    return (
        <Layout>
            <Hero />

            <section className="metrics">
                {metrics.map((metric, index) => (
                    <MetricCard
                        key={metric.label}
                        label={metric.label}
                        value={metric.value}
                        detail={metric.detail}
                        index={index}
                    />
                ))}
            </section>

            <BenchmarkHighlights hardware={hardware} />

            <HowItWorks />
        </Layout>
    );
}


export default Home;