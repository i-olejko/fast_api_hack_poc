import os
import json
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Dict, Any

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field

router = APIRouter(
    prefix="/api/recordings",
    tags=["recordings"],
)

RECORDINGS_BASE_DIR = Path("recordings")
DATETIME_FORMAT = "%d-%m-%Y_%H-%M-%S"

class RecordingMetadata(BaseModel):
    # Define expected structure if known, otherwise allow any dict
    pass

class RecordingInfo(BaseModel):
    id: str
    video_urls: List[str] = Field(..., description="List of relative URLs to .webm video files")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Content of metadata.json, or null if not found/invalid")


@router.get("/latest", response_model=List[RecordingInfo])
async def get_latest_recordings():
    """
    Fetches the latest 10 recordings based on directory name timestamp.
    """
    if not RECORDINGS_BASE_DIR.is_dir():
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Recordings directory not found: {RECORDINGS_BASE_DIR}"
        )

    recording_dirs = []
    try:
        for item in RECORDINGS_BASE_DIR.iterdir():
            if item.is_dir():
                try:
                    # Validate directory name format and parse datetime
                    dir_datetime = datetime.strptime(item.name, DATETIME_FORMAT)
                    recording_dirs.append((dir_datetime, item))
                except ValueError:
                    # Ignore directories that don't match the format
                    continue
    except PermissionError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Permission denied while accessing recordings directory: {RECORDINGS_BASE_DIR}"
        )
    except Exception as e:
         raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred while scanning recordings: {e}"
        )


    # Sort directories chronologically descending
    recording_dirs.sort(key=lambda x: x[0], reverse=True)

    latest_recordings_data = []
    for _, dir_path in recording_dirs[:10]: # Get top 10
        recording_id = dir_path.name
        video_files = list(dir_path.glob("*.webm"))
        video_urls = [f"/{RECORDINGS_BASE_DIR.name}/{recording_id}/{vf.name}" for vf in video_files]

        metadata_path = dir_path / "metadata.json"
        metadata_content = None
        if metadata_path.is_file():
            try:
                with open(metadata_path, 'r') as f:
                    metadata_content = json.load(f)
            except json.JSONDecodeError:
                # Handle invalid JSON, maybe log this?
                metadata_content = {"error": "Invalid JSON format"}
            except Exception as e:
                 # Handle other potential file reading errors
                 metadata_content = {"error": f"Could not read metadata: {e}"}
        else:
            # Handle missing metadata file
             metadata_content = {"error": "Metadata file not found"}


        latest_recordings_data.append(
            RecordingInfo(
                id=recording_id,
                video_urls=video_urls,
                metadata=metadata_content
            )
        )

    return latest_recordings_data