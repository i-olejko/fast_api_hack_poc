import os
import json
from datetime import datetime
import asyncio
from pathlib import Path
import logging
from typing import List, Dict, Any, Optional

class SessionRecorder:
    def __init__(self, base_dir: str = "recordings"):
        """Initialize the session recorder with a base directory for storing recordings."""
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)
        self.current_session: Optional[Dict[str, Any]] = None
        self.visited_sites: List[str] = []
        
        # Configure logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

    def _generate_session_dir(self) -> Path:
        """Generate a unique directory name for the current session."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        session_dir = self.base_dir / timestamp
        session_dir.mkdir(parents=True, exist_ok=True)
        return session_dir

    def get_recording_config(self) -> Dict[str, Any]:
        """Get the recording configuration for browser context creation."""
        session_dir = self._generate_session_dir()
        recording_path = str(session_dir / "session.webm")
        
        self.current_session = {
            "directory": str(session_dir),
            "recording_path": recording_path,
            "metadata_path": str(session_dir / "metadata.json"),
            "visited_sites": [],
            "start_time": datetime.now().isoformat()
        }
        
        return {
            "recordVideo": {
                "dir": str(session_dir)
            }
        }

    def start_session(self, task: str) -> None:
        """Start a new recording session."""
        if not self.current_session:
            raise RuntimeError("Recording configuration not initialized. Call get_recording_config first.")
        
        self.current_session["task"] = task
        self.logger.info(f"Starting recording session in {self.current_session['directory']}")

    def add_visited_site(self, url: str) -> None:
        """Add a visited site to the current session."""
        if self.current_session and url not in self.current_session["visited_sites"]:
            self.current_session["visited_sites"].append(url)

    async def end_session(self, result: Any) -> Dict[str, Any]:
        """End the current recording session and save metadata."""
        if not self.current_session:
            raise RuntimeError("No active session to end")

        try:
            # Update session metadata
            self.current_session["end_time"] = datetime.now().isoformat()
            self.current_session["result"] = result

            # Save metadata
            metadata_path = Path(self.current_session["metadata_path"])
            with open(metadata_path, 'w') as f:
                json.dump(self.current_session, f, indent=2)

            self.logger.info(f"Session completed. Metadata saved to {metadata_path}")
            
            # Return session data
            return self.current_session

        except Exception as e:
            self.logger.error(f"Error ending session: {e}")
            raise
        finally:
            self.current_session = None
            self.visited_sites = []

    def get_session_info(self) -> Optional[Dict[str, Any]]:
        """Get information about the current session."""
        return self.current_session 