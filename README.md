# FastAPI + React Python Code Runner (Hackathon PoC)

This project is a proof-of-concept demonstrating a Python FastAPI backend serving a React frontend. The frontend allows users to submit Python code as text, which the backend executes using Python's `exec()` function.

**🚨 SECURITY WARNING 🚨**
This application uses `exec()` to run arbitrary Python code submitted by the user. **This is extremely dangerous and should NEVER be used in a production environment or any environment where security is a concern.** This PoC is intended solely for demonstration purposes in a controlled hackathon setting.

## Folder Structure

```
/
├── frontend/             # React frontend application (created with Create React App)
│   ├── build/            # Production build of the React app (served by FastAPI)
│   ├── public/
│   ├── src/              # React component source files (App.js, etc.)
│   ├── package.json
│   └── ...               # Other CRA files
├── venv/                 # Python virtual environment
├── main.py               # FastAPI application file
└── README.md             # This file
```

## Setup

1.  **Clone/Setup Project:** Ensure you are in the project's root directory.
2.  **Backend Setup:**
    *   Create and activate a Python virtual environment (if not already done):
        ```bash
        python3 -m venv venv
        source venv/bin/activate  # On Linux/macOS
        # venv\Scripts\activate  # On Windows
        ```
    *   Install Python dependencies:
        ```bash
        pip install fastapi uvicorn
        ```
3.  **Frontend Setup:**
    *   Navigate to the frontend directory:
        ```bash
        cd frontend
        ```
    *   Install Node.js dependencies:
        ```bash
        npm install
        ```
    *   Build the React application:
        ```bash
        npm run build
        ```
    *   Return to the project root directory:
        ```bash
        cd ..
        ```

## Running the Application

1.  Ensure your virtual environment is activated (`source venv/bin/activate`).
2.  Start the FastAPI server from the project root directory:
    ```bash
    uvicorn main:app --reload --host 127.0.0.1 --port 8000
    ```
    *   `--reload` enables auto-reloading for backend development (optional).
    *   You can also run using `python main.py` if the `if __name__ == "__main__":` block is present.

## Usage

1.  Open your web browser and navigate to `http://127.0.0.1:8000`.
2.  You should see the React application interface with a textarea.
3.  Enter Python code (e.g., `print("Hello from exec!")`) into the textarea.
4.  Click the "Run Code" button.
5.  The output (or any execution error) from the backend will be displayed below the form.

**Remember the security warning! Only run code you trust.**