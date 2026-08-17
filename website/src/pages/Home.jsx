import { useEffect, useState } from "react";

import Layout from "../layout/Layout";

import Hero from "../components/Hero";
import MetricCard from "../components/MetricCard";
import CommunityStory from "../components/CommunityStory";

import {
  metrics as fallbackMetrics,
  communityStory as fallbackCommunityStory,
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


function buildPublishedCommunityStory(
  featuredStory,
  stats,
) {
  return {
    eyebrow: "COMMUNITY STORY",
    badge:
      featuredStory.badge ||
      "Data Snapshot",
    title:
      featuredStory.title ||
      "",
    description:
      featuredStory.description ||
      "",
    evidence: [
      {
        label: "Based on",
        value:
          `${stats.benchmarkResults} benchmark ` +
          `${
            stats.benchmarkResults === 1
              ? "result"
              : "results"
          }`,
      },
      {
        label: "Snapshot",
        value:
          featuredStory.snapshot ||
          "",
      },
      {
        label: "Average tg128",
        value:
          `${formatNumber(
            stats.averageTg128,
          )} tokens/sec`,
      },
    ],
  };
}


function Home() {
  const [metrics, setMetrics] = useState(
    fallbackMetrics,
  );

  const [
    communityStory,
    setCommunityStory,
  ] = useState(
    fallbackCommunityStory,
  );

  useEffect(() => {
    const homepageDataUrl =
      `${import.meta.env.BASE_URL}homepage.json`;

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

        if (homepageData.featuredStory) {
          setCommunityStory(
            buildPublishedCommunityStory(
              homepageData.featuredStory,
              homepageData.stats,
            ),
          );
        }
      } catch (error) {
        console.error(
          "Unable to load published homepage data. " +
          "Using fallback homepage data.",
          error,
        );
      }
    }

    loadPublishedHomepage();
  }, []);

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
        description={
          communityStory.description
        }
        evidence={communityStory.evidence}
      />
    </Layout>
  );
}


export default Home;