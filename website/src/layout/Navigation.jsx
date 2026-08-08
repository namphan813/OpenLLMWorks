import { useState } from "react";
import { Link } from "react-router-dom";

function Navigation() {
  const [menuOpen, setMenuOpen] = useState(false);

  function closeMenu() {
    setMenuOpen(false);
  }

  return (
    <nav className="navigation">
      <div className="logo">
        <Link to="/" onClick={closeMenu}>
          OpenLLMBench
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

        <a href="#" onClick={closeMenu}>
          Benchmarks
        </a>

        <Link to="/hardware" onClick={closeMenu}>
          Hardware
        </Link>

        <a href="#" onClick={closeMenu}>
          About
        </a>
      </div>
    </nav>
  );
}

export default Navigation;