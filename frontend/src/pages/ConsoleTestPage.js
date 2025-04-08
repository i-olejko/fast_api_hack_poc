import React, { useState } from 'react';
import '../App.css'; // Assuming styles are still in App.css

const TEST_TASK = `
1. Try to login with company email: x_email and password: x_password
2. Navigate to the Browsing Roles by using nav bar on the left.
3. Open a new role modal by clicking on the New Role button.
4. Fill in the role name and description.
5. Select "VIP" option from the "User Groups" dropdown.
6. Close the "User Groups" dropdown list by clicking on open/close caret.
7. Click on the "Save" button.
8. Validate Role added. `;

const TEST_FOLLOW_UP_TASK = `Click on the Browsing Roles nav item from nav bar on the left
get the first role name and role description from the table of roles
provide result as {foundName: str, foundDesc: str}
Call done`;



function ConsoleTestPage() {
  const [strTask, setStrTask] = useState(TEST_TASK);
  const [strFollowUpTask, setStrFollowUpTask] = useState(TEST_FOLLOW_UP_TASK);
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
        createdName: data.result.createdName || 'N/A',
        foundName: data.result.foundName || 'N/A',
        createdDesc: data.result.createdDesc || 'N/A',
        foundDesc: data.result.foundDesc || data.foundDesc || 'N/A' // Handle both possible keys
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
        <div className="results-card-container" style={{ border: '1px solid #ccc', padding: '16px', marginTop: '20px', borderRadius: '8px', maxWidth: '600px' }}>
          <h2>Results</h2>
          <p><strong>created name:</strong> {resultData.createdName}</p>
          <p><strong>Created Description:</strong> {resultData.createdDesc}</p>
          <p><strong>Agent output:</strong> {resultData.foundDesc}</p>
        </div>
      )}
    </div>
  );
}

export default ConsoleTestPage;