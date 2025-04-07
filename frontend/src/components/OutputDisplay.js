import React from 'react';

function OutputDisplay({ output, error }) {
  return (
    <div>
      <h2>Output:</h2>
      {error && <pre style={{ color: 'red' }}>{error}</pre>}
      {output && <pre>{output}</pre>}
      {/* Optional: Add a status indicator for loading state */}
      {/* <p style={{ color: 'gray', marginTop: '20px' }}>Status: Idle/Running/Done</p> */}
    </div>
  );
}

export default OutputDisplay;