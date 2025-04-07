import React, { useState } from 'react';
import './App.css'; // Keep or modify default styling as needed

function App() {
  const [taskText, setTaskText] = useState(''); // Renamed from 'code'
  const [output, setOutput] = useState('');
  const [error, setError] = useState(''); // Optional: for displaying fetch errors

  const handleSubmit = async (event) => {
    event.preventDefault();
    setOutput(''); // Clear previous output
    setError('');   // Clear previous error

    try {
      // TODO: Make the URL configurable if needed (e.g., via environment variables)
      const response = await fetch('http://localhost:8000/run_task', { // Updated endpoint
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ task_text: taskText }), // Send task text in correct format
      });

      if (!response.ok) {
        // Handle HTTP errors (e.g., 4xx, 5xx)
        const errorData = await response.json(); // Try to parse error response from backend
        throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      // Assuming the backend returns { "result": "..." }
      setOutput(data.result || JSON.stringify(data, null, 2)); // Display result or full response if 'result' field is missing

    } catch (e) {
      console.error("Error submitting task:", e);
      setError(`Error: ${e.message}`); // Display fetch/network or backend error
      setOutput(''); // Clear output on error
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Python Code Runner (PoC)</h1>
        <form onSubmit={handleSubmit}>
          <textarea
            value={taskText}
            onChange={(e) => setTaskText(e.target.value)}
            placeholder="Enter your task here..."
            rows={10}
            cols={80}
            style={{ fontFamily: 'monospace', fontSize: '14px' }} // Basic styling
          />
          <br />
          <button type="submit">Run Task</button>
        </form>
        <h2>Output:</h2>
        {error && <pre style={{ color: 'red' }}>{error}</pre>}
        {output && <pre>{output}</pre>}
        {/* Optional: Add a status indicator for loading state */}
        {/* <p style={{ color: 'gray', marginTop: '20px' }}>Status: Idle/Running/Done</p> */}
      </header>
    </div>
  );
}

export default App;
