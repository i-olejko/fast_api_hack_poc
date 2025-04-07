import React from 'react';
import '../App.css';

function TopBar({ theme, onThemeChange }) {
  const handleThemeChange = (event) => {
    if (onThemeChange) {
      onThemeChange(event.target.value);
    }
  };

  return (
    <div className="top-bar">
      <div className="top-bar-content">
        <span className="nav-title">HACK DAY 2025</span>
        <select className="theme-switcher" onChange={handleThemeChange} value={theme}>
          <option value="LIGHT">LIGHT</option>
          <option value="DARK">DARK</option>
        </select>
      </div>
    </div>
  );
}

export default TopBar;