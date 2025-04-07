import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import './App.css';
import NavBar from './components/NavBar'; // Will be created
import FreeRunPage from './pages/FreeRunPage'; // Will be created
import ConsoleTestPage from './pages/ConsoleTestPage'; // Will be created

function App() {
  return (
    <Router>
      <div className="app-container"> {/* Main container for layout */}
        <NavBar /> {/* Navigation bar on the left */}
        <div className="content-area"> {/* Content area on the right */}
          <Routes>
            <Route path="/" element={<FreeRunPage />} />
            <Route path="/console-test" element={<ConsoleTestPage />} />
          </Routes>
        </div>
      </div>
    </Router>
  );
}

export default App;
