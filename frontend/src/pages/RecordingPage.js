import React, { useState, useEffect } from 'react';
import './RecordingPage.css'; // We'll create this CSS file later for styling

function RecordingPage() {
  const [recordings, setRecordings] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchRecordings = async () => {
      try {
        setLoading(true);
        setError(null);
        const response = await fetch('/api/recordings/latest');
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        setRecordings(data);
      } catch (e) {
        console.error("Failed to fetch recordings:", e);
        setError(`Failed to load recordings: ${e.message}`);
      } finally {
        setLoading(false);
      }
    };

    fetchRecordings();
  }, []); // Empty dependency array means this effect runs once on mount

  if (loading) {
    return <div>Loading recordings...</div>;
  }

  if (error) {
    return <div className="error-message">Error: {error}</div>;
  }

  return (
    <div className="recording-page">
      <h1>Latest Recordings</h1>
      {recordings.length === 0 ? (
        <p>No recordings found.</p>
      ) : (
        <ul className="recording-list">
          {recordings.map((recording) => (
            <li key={recording.id} className="recording-item">
              <h2>Recording ID: {recording.id}</h2>
              <div className="metadata-section">
                <h3>Metadata:</h3>
                {recording.metadata?.error ? (
                  <pre className="error-message">Error parsing metadata: {recording.metadata.error}</pre>
                ) : (
                  <pre>{JSON.stringify(recording.metadata, null, 2)}</pre>
                )}
              </div>
              <div className="videos-section">
                <h3>Videos:</h3>
                {recording.video_urls && recording.video_urls.length > 0 ? (
                  <div className="video-container">
                    {recording.video_urls.map((videoUrl, index) => (
                      <div key={index} className="video-wrapper">
                         {/* Ensure the src is correctly formed relative to the server root */}
                        <video controls width="400" src={videoUrl}>
                          Your browser does not support the video tag.
                        </video>
                      </div>
                    ))}
                  </div>
                ) : (
                  <p>No videos available for this recording.</p>
                )}
              </div>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

export default RecordingPage;