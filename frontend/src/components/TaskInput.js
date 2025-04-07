import React from 'react';

function TaskInput({ taskText, setTaskText, onSubmit }) {
  return (
    <div>
      <textarea
        value={taskText}
        onChange={(e) => setTaskText(e.target.value)}
        placeholder="Enter your task here..."
        rows={10}
        cols={80}
        style={{ fontFamily: 'monospace', fontSize: '14px' }} // Basic styling
      />
      <br />
      <button type="button" onClick={onSubmit}>Run Task</button>
    </div>
  );
}

export default TaskInput;