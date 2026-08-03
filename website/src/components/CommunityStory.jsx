function CommunityStory() {
    return (
        <section className="community-story">
            <div className="story-header">
                <p className="story-eyebrow">
                    Community Story
                </p>

                <span className="snapshot-badge">
                    Data Snapshot
                </span>
            </div>

            <h2>
                The GTX 1650 is OpenLLMBench&apos;s first recorded GPU.
            </h2>

            <p className="story-copy">
                The current database contains one verified benchmark result,
                establishing the first historical reference point for the
                OpenLLMBench community.
            </p>

            <div className="story-evidence">
                <div>
                    <span className="evidence-label">
                        Based on
                    </span>

                    <strong>
                        1 benchmark result
                    </strong>
                </div>

                <div>
                    <span className="evidence-label">
                        Snapshot
                    </span>

                    <strong>
                        2026-08-02 14:17 UTC
                    </strong>
                </div>

                <div>
                    <span className="evidence-label">
                        Average tg128
                    </span>

                    <strong>
                        31.69 tokens/sec
                    </strong>
                </div>
            </div>
        </section>
    );
}

export default CommunityStory;