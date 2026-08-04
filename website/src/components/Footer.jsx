function Footer() {
    return (
        <footer className="site-footer">
            <div className="footer-content">
                <div className="footer-brand">
                    <p className="footer-logo">
                        OpenLLMBench
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

                    <a href="#">Hardware</a>
                    <a href="#">Leaderboards</a>
                    <a href="#">Trends</a>
                    <a href="#">Snapshots</a>
                </div>

                <div className="footer-column">
                    <h2>Participate</h2>

                    <a href="#">Run a Benchmark</a>
                    <a href="#">Submit Results</a>
                    <a href="#">Contributing</a>
                    <a href="#">GitHub</a>
                </div>

                <div className="footer-column">
                    <h2>Project</h2>

                    <a href="#">Documentation</a>
                    <a href="#">Roadmap</a>
                    <a href="#">About</a>
                    <a href="#">Project Status</a>
                </div>
            </div>

            <div className="footer-bottom">
                <p>
                    © 2026 OpenLLMBench
                </p>

                <p>
                    License under consideration
                </p>

                <p>
                    Data Snapshot: 2026-08-02 14:17 UTC
                </p>
            </div>
        </footer>
    );
}

export default Footer;