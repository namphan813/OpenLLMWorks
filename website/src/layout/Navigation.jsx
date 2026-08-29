import { useState } from "react";
import { Link } from "react-router-dom";

const GITHUB_URL = "https://github.com/namphan813/OpenLLMWorks";
const RUNNER_URL =
    "https://github.com/namphan813/OpenLLMWorks/releases/tag/v0.3.0-beta.1";

function Navigation() {
    const [menuOpen, setMenuOpen] = useState(false);

    function closeMenu() {
        setMenuOpen(false);
    }

    return (
        <nav className="navigation">
            <div className="logo">
                <Link to="/" onClick={closeMenu}>
                    OpenLLMWorks
                </Link>
            </div>

            <button
                className="mobile-menu-button"
                type="button"
                aria-label="Toggle navigation menu"
                aria-expanded={menuOpen}
                onClick={() => setMenuOpen((current) => !current)}
            >
                <span></span>
                <span></span>
                <span></span>
            </button>

            <div className={`nav-links ${menuOpen ? "nav-links-open" : ""}`}>
                <Link to="/" onClick={closeMenu}>
                    Home
                </Link>

                <Link to="/hardware" onClick={closeMenu}>
                    Hardware
                </Link>

                <a
                    href={GITHUB_URL}
                    target="_blank"
                    rel="noreferrer"
                    onClick={closeMenu}
                >
                    GitHub
                </a>

                <a
                    href={RUNNER_URL}
                    target="_blank"
                    rel="noreferrer"
                    onClick={closeMenu}
                >
                    Run Benchmark
                </a>
            </div>
        </nav>
    );
}

export default Navigation;
