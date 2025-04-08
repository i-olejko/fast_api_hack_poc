import React from 'react';
import { Link } from 'react-router-dom';
import '../App.css'; // Assuming styles will be in App.css for simplicity

function NavBar({ theme, onThemeChange }) {
  const handleThemeChange = (event) => {
    if (onThemeChange) {
      onThemeChange(event.target.value);
    }
  };

  return (
    <nav className="nav-bar"> {/* Class for styling */}
      <div className="nav-content">
        <div className="nav-left">
          <ul>
            <li>
              <Link to="/">Free Run</Link>
            </li>
            <li>
              <Link to="/console-test">Console Test</Link>
            </li>
            <li>
              <Link to="/recording">Recordings</Link> {/* Add link to Recordings page */}
            </li>
          </ul>
        </div>
      </div>
    </nav>
  );
}

export default NavBar;