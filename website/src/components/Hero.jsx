function Hero() {
    return (
        <section className="hero">
            <h1>OpenLLMWorks</h1>

            <div
                style={{
                    display: "inline-block",
                    marginBottom: "1.5rem",
                    padding: "0.35rem 0.7rem",
                    border: "1px solid currentColor",
                    borderRadius: "999px",
                    fontSize: "0.75rem",
                    fontWeight: "700",
                    letterSpacing: "0.12em",
                }}
            >
                PUBLIC BETA
            </div>

            <h2>
                Building the historical record
                <br />
                of local AI performance.
            </h2>

            <p>
                Measure.
                <br />
                Understand.
                <br />
                Preserve.
            </p>

            <button>
                Run Your First Benchmark
            </button>
        </section>
    );
}

export default Hero;
