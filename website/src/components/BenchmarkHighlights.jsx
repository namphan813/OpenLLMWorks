import { motion } from "motion/react";
import { Link } from "react-router-dom";

function formatScore(value) {
    if (typeof value !== "number") {
        return "N/A";
    }

    return value.toFixed(2);
}

function shortenGpuName(name) {
    if (typeof name !== "string") {
        return "Unknown GPU";
    }

    return name
        .replace(/^NVIDIA\s+/i, "")
        .replace(/^AMD\s+/i, "");
}

function BenchmarkHighlights({ hardware = [] }) {
    const rankedHardware = hardware
        .filter(
            (item) =>
                typeof item?.performance?.averageTg128 === "number"
        )
        .sort(
            (left, right) =>
                right.performance.averageTg128 -
                left.performance.averageTg128
        )
        .slice(0, 5);

    const bestScore =
        rankedHardware[0]?.performance?.averageTg128 ?? 0;

    if (rankedHardware.length === 0) {
        return null;
    }

    return (
        <motion.section
            className="benchmark-highlights"
            initial={{ opacity: 0, y: 24 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true, amount: 0.2 }}
            transition={{ duration: 0.55, ease: "easeOut" }}
        >
            <div className="benchmark-highlights-header">
                <div>
                    <p className="benchmark-highlights-eyebrow">
                        BENCHMARK HIGHLIGHTS
                    </p>

                    <h2>
                        tg128 performance across the dataset
                    </h2>

                    <p className="benchmark-highlights-copy">
                        Average token generation performance from
                        published OpenLLMWorks benchmark results.
                    </p>
                </div>

                <Link
                    className="benchmark-highlights-link"
                    to="/hardware"
                >
                    Explore All Hardware
                </Link>
            </div>

            <div className="benchmark-highlight-list">
                {rankedHardware.map((item, index) => {
                    const score =
                        item.performance.averageTg128;

                    const width =
                        bestScore > 0
                            ? (score / bestScore) * 100
                            : 0;

                    return (
                        <Link
                            className="benchmark-highlight-row"
                            to={`/hardware/${item.variantId}`}
                            key={item.variantId}
                        >
                            <div className="benchmark-highlight-meta">
                                <div>
                                    <span className="benchmark-highlight-rank">
                                        {String(index + 1).padStart(2, "0")}
                                    </span>

                                    <strong>
                                        {shortenGpuName(item.gpuModel)}
                                    </strong>
                                </div>

                                <span className="benchmark-highlight-score">
                                    {formatScore(score)}
                                    <small> tok/s</small>
                                </span>
                            </div>

                            <div className="benchmark-highlight-track">
                                <motion.div
                                    className="benchmark-highlight-bar"
                                    initial={{ scaleX: 0 }}
                                    whileInView={{ scaleX: 1 }}
                                    viewport={{
                                        once: true,
                                        amount: 0.5,
                                    }}
                                    transition={{
                                        duration: 0.7,
                                        delay: 0.08 * index,
                                        ease: [0.22, 1, 0.36, 1],
                                    }}
                                    style={{
                                        width: `${width}%`,
                                        transformOrigin: "left",
                                    }}
                                />
                            </div>
                        </Link>
                    );
                })}
            </div>

            <p className="benchmark-highlights-note">
                Higher tg128 indicates faster token generation.
                Results reflect the current published dataset and may
                change as additional hardware is submitted.
            </p>
        </motion.section>
    );
}

export default BenchmarkHighlights;