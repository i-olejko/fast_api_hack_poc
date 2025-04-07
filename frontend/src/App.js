import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import './App.css';
import NavBar from './components/NavBar';
import TopBar from './components/TopBar';
import FreeRunPage from './pages/FreeRunPage';
import ConsoleTestPage from './pages/ConsoleTestPage';

function App() {
  const [theme, setTheme] = useState('LIGHT');

  const handleThemeChange = (newTheme) => {
    setTheme(newTheme);
  };

  return (
    <Router>
      <div className={`app-container ${theme === 'DARK' ? 'dark-theme' : 'light-theme'}`}> {/* Main container with theme class */}
        <TopBar theme={theme} onThemeChange={handleThemeChange} />
        <div className="main-layout">
          <NavBar />
          <div className="content-area">
            <Routes>
              <Route path="/" element={<FreeRunPage />} />
              <Route path="/console-test" element={<ConsoleTestPage />} />
            </Routes>
          </div>
        </div>
      </div>
    </Router>
  );
}

export default App;
