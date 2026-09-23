import { motion } from "motion/react";

function MetricCard({
    label,
    value,
    detail,
    index = 0,
}) {
    return (
        <motion.article
            className="metric-card"
            initial={{
                opacity: 0,
                y: 28,
            }}
            animate={{
                opacity: 1,
                y: 0,
            }}
            transition={{
                duration: 0.55,
                delay: 0.35 + index * 0.1,
                ease: [0.22, 1, 0.36, 1],
            }}
            whileHover={{
                y: -4,
                transition: {
                    duration: 0.18,
                },
            }}
        >
            <p className="metric-label">
                {label}
            </p>

            <p className="metric-value">
                {value}
            </p>

            <p className="metric-detail">
                {detail}
            </p>
        </motion.article>
    );
}

export default MetricCard;