function CommunityStory({
    eyebrow,
    badge,
    title,
    description,
    evidence,
}) {
    return (
        <section className="community-story">
            <div className="story-header">
                <p className="story-eyebrow">
                    {eyebrow}
                </p>

                <span className="snapshot-badge">
                    {badge}
                </span>
            </div>

            <h2>{title}</h2>

            <p className="story-copy">
                {description}
            </p>

            <div className="story-evidence">
                {evidence.map((item) => (
                    <div key={item.label}>
                        <span className="evidence-label">
                            {item.label}
                        </span>

                        <strong>
                            {item.value}
                        </strong>
                    </div>
                ))}
            </div>
        </section>
    );
}

export default CommunityStory;