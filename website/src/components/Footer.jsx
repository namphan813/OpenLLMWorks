import { Link } from "react-router-dom";

const GITHUB_URL = "https://github.com/namphan813/OpenLLMWorks";
const RUNNER_URL =
    "https://github.com/namphan813/OpenLLMWorks/releases/tag/v0.3.0-beta.1";
const ISSUES_URL =
    "https://github.com/namphan813/OpenLLMWorks/issues";
const SUBMIT_URL =
    "https://github.com/namphan813/OpenLLMWorks/issues/new/choose";
const README_URL =
    "https://github.com/namphan813/OpenLLMWorks/blob/main/README.md";
const ROADMAP_URL =
    "https://github.com/namphan813/OpenLLMWorks/blob/main/ROADMAP.md";
const STATUS_URL =
    "https://github.com/namphan813/OpenLLMWorks/blob/main/STATUS.md";
const PROTOCOL_URL =
    "https://github.com/namphan813/OpenLLMWorks/blob/main/docs/benchmark_v1.md";

function Footer() {
    return (
        <footer className="site-footer">
            <div className="footer-content">
                <div className="footer-brand">
                    <p className="footer-logo">
                        OpenLLMWorks
                    </p>

                    <p className="footer-description">
                        Building the historical record of local AI hardware
                        performance.
                    </p>

                    <p className="footer-mission">
                        Measure. Understand. Preserve.
                    </p>
                </div>

                <div className="footer-column">
                    <h2>Explore</h2>

                    <Link to="/hardware">Hardware</Link>
                    <Link to="/compare">Compare GPUs</Link>
                    <a
                        href={PROTOCOL_URL}
                        target="_blank"
                        rel="noreferrer"
                    >
                        Benchmark Protocol
                    </a>
                </div>

                <div className="footer-column">
                    <h2>Participate</h2>

                    <a
                        href={RUNNER_URL}
                        target="_blank"
                        rel="noreferrer"
                    >
                        Run a Benchmark
                    </a>

                    <a
                        href={SUBMIT_URL}
                        target="_blank"
                        rel="noreferrer"
                    >
                        Submit Results
                    </a>

                    <a
                        href={ISSUES_URL}
                        target="_blank"
                        rel="noreferrer"
                    >
                        Report an Issue
                    </a>

                    <a
                        href={GITHUB_URL}
                        target="_blank"
                        rel="noreferrer"
                    >
                        GitHub
                    </a>
                </div>

                <div className="footer-column">
                    <h2>Project</h2>

                    <a
                        href={README_URL}
                        target="_blank"
                        rel="noreferrer"
                    >
                        Documentation
                    </a>

                    <a
                        href={ROADMAP_URL}
                        target="_blank"
                        rel="noreferrer"
                    >
                        Roadmap
                    </a>

                    <a
                        href={STATUS_URL}
                        target="_blank"
                        rel="noreferrer"
                    >
                        Project Status
                    </a>
                </div>

                <div className="footer-bottom">
                    <p>
                        © 2026 OpenLLMWorks
                    </p>

                    <p>
                        Public Beta
                    </p>

                    <p>
                        Data Snapshot: 2026-08-02 14:17 UTC
                    </p>
                </div>
            </div>
        </footer>
    );
}

export default Footer;
