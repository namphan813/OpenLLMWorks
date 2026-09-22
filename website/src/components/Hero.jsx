import { Link } from "react-router-dom";

const RUNNER_URL =
    "https://github.com/namphan813/OpenLLMWorks/releases/tag/v0.4.0-beta.1";

function Hero() {
    return (
        <section className="hero">
            <div className="hero-beta">
                PUBLIC BETA
            </div>

            <h1>
                Open benchmarks for
                <br />
                local AI hardware.
            </h1>

            <p className="hero-description">
                Real-world local AI performance across consumer and
                workstation hardware, measured with a standardized and
                reproducible benchmark.
            </p>

            <div className="hero-actions">
                <Link
                    className="hero-action hero-action-primary"
                    to="/hardware"
                >
                    Explore Benchmarks
                </Link>

                <a
                    className="hero-action hero-action-secondary"
                    href={RUNNER_URL}
                    target="_blank"
                    rel="noreferrer"
                >
                    Run the Benchmark
                </a>
            </div>

        </section>
    );
}

export default Hero;