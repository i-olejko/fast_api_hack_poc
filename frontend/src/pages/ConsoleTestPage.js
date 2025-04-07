import React, { useState } from 'react';
import '../App.css'; // Assuming styles are still in App.css

function ConsoleTestPage() {
  const [strTask, setStrTask] = useState('');
  const [strFollowUpTask, setStrFollowUpTask] = useState('');
  const [resultData, setResultData] = useState(null); // To store API response
  const [error, setError] = useState('');

  const handleConsoleSubmit = async () => {
    setResultData(null); // Clear previous results
    setError('');       // Clear previous error

    try {
      // TODO: Make the URL configurable if needed
      const response = await fetch('http://localhost:8000/run_console_task', { // Endpoint for console test
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          strTask: strTask,
          strFollowUpTask: strFollowUpTask,
        }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      // Assuming the backend returns { createdName: "...", foundName: "...", createdDesc: "...", fondDesc: "..." }
      // Correcting potential typo 'fondDesc' to 'foundDesc' based on context
      setResultData({
        createdName: data.createdName || 'N/A',
        foundName: data.foundName || 'N/A',
        createdDesc: data.createdDesc || 'N/A',
        foundDesc: data.fondDesc || data.foundDesc || 'N/A' // Handle both possible keys
      });

    } catch (e) {
      console.error("Error submitting console task:", e);
      setError(`Error: ${e.message}`);
      setResultData(null); // Clear results on error
    }
  };

  return (
    <div className="page-container">
      <h1>Console Test</h1>
      <div className="console-input-area">
        <div>
          <label htmlFor="taskInput">Task Input:</label>
          <textarea
            id="taskInput"
            value={strTask}
            onChange={(e) => setStrTask(e.target.value)}
            placeholder="Enter your task here..."
            rows={10}
            cols={80}
            style={{ fontFamily: 'monospace', fontSize: '14px' }} // Basic styling
          ></textarea>
        </div>
        <div>
          <label htmlFor="followUpInput">Follow-up Task:</label>
          <textarea
            id="followUpInput"
            value={strFollowUpTask}
            onChange={(e) => setStrFollowUpTask(e.target.value)}
            rows={10}
            cols={80}
            style={{ fontFamily: 'monospace', fontSize: '14px' }} // Basic styling
          ></textarea>
        </div>
        <button onClick={handleConsoleSubmit}>Run Task</button>
      </div>

      {error && <div className="error-message">Error: {error}</div>}

      {resultData && (
        <div className="results-table-container">
          <h2>Results</h2>
          <table className="results-table">
            <thead>
              <tr>
                <th>Created Name</th>
                <th>Found Name</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td>{resultData.createdName}</td>
                <td>{resultData.foundName}</td>
              </tr>
              <tr>
                <th>Created Description</th>
                <th>Found Description</th>
              </tr>
              <tr>
                <td>{resultData.createdDesc}</td>
                <td>{resultData.foundDesc}</td>
              </tr>
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}

export default ConsoleTestPage;