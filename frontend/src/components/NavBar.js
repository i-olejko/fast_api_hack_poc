import React from 'react';
import { Link } from 'react-router-dom';
import '../App.css'; // Assuming styles will be in App.css for simplicity

function NavBar() {
  return (
    <nav className="nav-bar"> {/* Class for styling */}
      <ul>
        <li>
          <Link to="/">FreeRun</Link>
        </li>
        <li>
          <Link to="/console-test">Console Test</Link>
        </li>
      </ul>
    </nav>
  );
}

export default NavBar;