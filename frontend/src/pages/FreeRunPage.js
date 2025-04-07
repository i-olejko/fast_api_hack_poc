import React, { useState } from 'react';
import '../App.css'; // Assuming styles are still in App.css
import TaskInput from '../components/TaskInput'; // Adjusted path
import OutputDisplay from '../components/OutputDisplay'; // Adjusted path

function FreeRunPage() {
  const [taskText, setTaskText] = useState('');
  const [output, setOutput] = useState('');
  const [error, setError] = useState(''); // Optional: for displaying fetch errors

  const handleSubmit = async () => {
    setOutput(''); // Clear previous output
    setError('');   // Clear previous error

    try {
      // TODO: Make the URL configurable if needed (e.g., via environment variables)
      const response = await fetch('http://localhost:8000/run_task', { // Endpoint for free run
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ task_text: taskText }), // Send task text
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      setOutput(data.result || JSON.stringify(data, null, 2));

    } catch (e) {
      console.error("Error submitting task:", e);
      setError(`Error: ${e.message}`);
      setOutput('');
    }
  };

  return (
    <div className="page-container"> {/* Optional container for page-specific layout */}
      <h1>Free Run Task</h1>
      <TaskInput
        taskText={taskText}
        setTaskText={setTaskText}
        onSubmit={handleSubmit}
      />
      <OutputDisplay output={output} error={error} />
    </div>
  );
}

export default FreeRunPage;