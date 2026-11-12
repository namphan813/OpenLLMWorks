import { Link } from "react-router-dom";
import "./ReleaseAnnouncement.css";

const RELEASE_URL =
    "https://github.com/namphan813/OpenLLMWorks/releases/tag/v0.4.2-beta.1";

const ARTICLE_URL =
    "/works/runner-v0-4-2-amd-vulkan-support";

function ReleaseAnnouncement() {
    return (
        <aside
            className="release-announcement"
            aria-label="Latest Runner release"
        >
            <div className="release-announcement-meta">
                <span className="release-announcement-badge">
                    NEW RELEASE
                </span>
                <time dateTime="2026-11-12">
                    November 12, 2026
                </time>
            </div>

            <div className="release-announcement-content">
                <div className="release-announcement-copy">
                    <strong>
                        Runner v0.4.2-beta.1 is here
                    </strong>
                    <p>
                        Experimental AMD/Vulkan support joins
                        NVIDIA/CUDA benchmarking.
                    </p>
                </div>

                <div className="release-announcement-links">
                    <Link to={ARTICLE_URL}>
                        Read announcement
                    </Link>
                    <a
                        href={RELEASE_URL}
                        target="_blank"
                        rel="noopener noreferrer"
                    >
                        Download Runner
                    </a>
                </div>
            </div>
        </aside>
    );
}

export default ReleaseAnnouncement;
