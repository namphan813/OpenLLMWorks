
const RUNNER_ADVISORY_ENABLED = true;

function RunnerAdvisory() {
    if (!RUNNER_ADVISORY_ENABLED) {
        return null;
    }

    return (
        <aside
            className="runner-advisory"
            aria-label="Runner service advisory"
            role="status"
        >
            <div className="runner-advisory-inner">
                <div className="runner-advisory-heading">
                    <span className="runner-advisory-indicator" />

                    <strong>
                        Runner Advisory
                    </strong>

                    <span className="runner-advisory-status">
                        Investigating
                    </span>
                </div>

                <p>
                    We are investigating an HTTPS certificate
                    verification issue affecting CUDA runtime
                    downloads on some Windows systems.
                    Benchmark setup may be interrupted.
                    We will provide an update when a fix
                    is available.
                </p>

                <span className="runner-advisory-date">
                    Updated November 3, 2026
                </span>
            </div>
        </aside>
    );
}

export default RunnerAdvisory;
