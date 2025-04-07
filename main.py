from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
import os
import asyncio
from dotenv import load_dotenv
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

# Imports for the agent (based on newtest.py)
from browser_use import Agent
from langchain_google_genai import ChatGoogleGenerativeAI
from browser_use.controller.service import Controller
from browser_use.browser.browser import Browser, BrowserConfig
from browser_use.browser.context import BrowserContext, BrowserContextConfig
from agent_service import AgentService # Import the new service

# Load environment variables from .env file
load_dotenv()

app = FastAPI(docs_url="/doc")

# --- CORS Configuration ---
# Allow requests from your frontend origin (e.g., http://localhost:3000)
# Using "*" for simplicity in this PoC, restrict in production.
origins = [
    "http://localhost:3000", # React default dev port
    "http://localhost:8000", # Default FastAPI port
    "http://127.0.0.1:3000",
    "http://127.0.0.1:8000",
    # Add other origins if needed
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], # Allows all methods
    allow_headers=["*"], # Allows all headers
)

# --- Instantiate Agent Service ---
# Instantiate once to potentially reuse resources like the LLM client
agent_service = AgentService()

# --- Pydantic Model for Request Body ---
class TaskRequest(BaseModel):
    task_text: str

class ConsoleTaskRequest(BaseModel):
    strTask: str
    strFollowUpTask: str

build_dir = "frontend/build"
static_dir = os.path.join(build_dir, "static")

# Mount static files first
if os.path.exists(static_dir):
     app.mount("/static", StaticFiles(directory=static_dir), name="static")
else:
    print(f"Warning: Static directory not found at {static_dir}. Frontend might not load correctly.")


# --- New Endpoint for Running AI Agent Task ---
@app.post("/run_task")
async def run_task(request: TaskRequest):
    try:
        task_text = request.task_text
        if not task_text:
             raise HTTPException(status_code=400, detail="Missing 'task_text' in request body")

        # --- Run the Agent via Service ---
        # The AgentService now handles setup and execution
        result = await agent_service.run(task_text)

        return JSONResponse(content={"status": "success", "result": result})

    except HTTPException as http_exc:
        # Re-raise HTTPExceptions to let FastAPI handle them
        raise http_exc
    except Exception as e:
        # Catch other exceptions during agent setup or execution
        print(f"Error during /run_task execution: {e}") # Log the full error server-side
        # Consider logging traceback: import traceback; traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Internal Server Error during task execution: {str(e)}")


# --- New Endpoint for Running Console Task ---
@app.post("/run_console_task")
async def run_console_task(request: ConsoleTaskRequest):
    try:
        strTask = request.strTask
        strFollowUpTask = request.strFollowUpTask
        if not strTask: # Basic validation
             raise HTTPException(status_code=400, detail="Missing 'strTask' in request body")
        # strFollowUpTask can be empty, so no check needed here

        # --- Call the Agent Service Method ---
        result = await agent_service.run_console(strTask, strFollowUpTask)

        # Assuming the service returns a dictionary-like object suitable for JSONResponse
        return JSONResponse(content={"status": "success", "result": result})

    except HTTPException as http_exc:
        # Re-raise HTTPExceptions
        raise http_exc
    except Exception as e:
        # Catch other exceptions
        print(f"Error during /run_console_task execution: {e}")
        raise HTTPException(status_code=500, detail=f"Internal Server Error during console task execution: {str(e)}")


@app.get("/{full_path:path}") # Catch-all route for SPA routing
async def serve_react_app(full_path: str):
    index_path = os.path.join(build_dir, "index.html")
    if not os.path.exists(index_path):
         # This shouldn't happen if build was successful, but good to have a fallback
        return JSONResponse(content={"error": "index.html not found. Build the frontend."}, status_code=404)
    return FileResponse(index_path)


# Optional: Add if you want to run directly using 'python main.py'
if __name__ == "__main__":
    import uvicorn
    # Ensure the host allows connections from your frontend if running separately during dev
    # For serving the integrated build, 127.0.0.1 is usually fine.
    uvicorn.run(app, host="127.0.0.1", port=8000)