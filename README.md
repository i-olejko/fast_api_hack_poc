# AI-Powered Browser Automation with FastAPI and React

This project demonstrates an AI-powered web automation system that allows users to describe tasks in natural language and have them executed automatically in a web browser. The system uses Google's Gemini AI model through LangChain for understanding and executing tasks, combined with browser automation capabilities.

## What it Does

- **Natural Language Task Input**: Users can describe tasks they want to perform on the web in plain English
- **AI-Powered Automation**: The system uses Google's Gemini AI model to:
  - Understand the user's task description
  - Plan the necessary steps to accomplish the task
  - Execute the steps using browser automation
- **Browser Automation**: Automatically controls a Chrome browser to:
  - Navigate to websites
  - Interact with web elements
  - Extract information
  - Perform complex web tasks
- **Real-Time Feedback**: Provides results and status updates through a modern React interface

## Example Use Cases

- Web research and data gathering
- Automated form filling
- Web testing and verification
- Content extraction and summarization
- Multi-step web workflows

**🚨 SECURITY WARNING ��**
This application performs automated browser actions based on user input. While it uses controlled browser automation, please be mindful of:
- Only use this tool on websites where you have permission to automate interactions
- Be careful with tasks involving sensitive data or authentication
- The tool should not be used for any malicious purposes or to violate websites' terms of service
- Consider rate limiting and respect websites' robots.txt files in production use

## System Requirements

- Python 3.11 or higher
- Node.js and npm (for frontend development)
- System dependencies for browser automation:
  ```bash
  # On Ubuntu/Debian:
  sudo apt-get install -y libgbm1

  # Or using Playwright's command (if available):
  sudo playwright install-deps
  ```

## Quick Start (Automated Setup)

The easiest way to get started is using our automated setup script:

```bash
# Make the script executable
chmod +x setup.sh

# Run the setup script
./setup.sh
```

The script will:
1. Create and activate a Python virtual environment
2. Install all required dependencies
3. Set up the Playwright browser
4. Create a `.env` file with default configurations
5. Build the frontend (if present)

After running the script:
1. Update the `.env` file with your Google API key
2. Activate the virtual environment: `source venv/bin/activate`
3. Run the application: `uvicorn main:app --reload`

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
├── .env                  # Environment configuration
├── setup.sh              # Automated setup script
└── README.md             # This file
```

## Manual Setup (Alternative)

If you prefer to set up manually or the automated script doesn't work for your environment:

1. **Clone/Setup Project:** Ensure you are in the project's root directory.

2. **Backend Setup (Python + FastAPI):**
    *   Create and activate a Python virtual environment (if not already done):
        ```bash
        python3 -m venv venv
        source venv/bin/activate  # On Linux/macOS
        # venv\Scripts\activate  # On Windows
        ```
    *   Install Python dependencies:
        ```bash
        pip install fastapi uvicorn python-dotenv browser-use playwright langchain-google-genai
        ```
    *   Install Playwright browser:
        ```bash
        playwright install chromium
        ```
    *   Create and configure `.env` file:
        ```bash
        cp .env.example .env
        # Edit .env with your API keys and configuration
        ```

3.  **Frontend Setup (React app in `/frontend` directory):**
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

## Environment Configuration

The `.env` file contains the following configurations:

```env
# API Keys
GEMINI_API_KEY=your_google_api_key_here  # Required for Gemini AI model

# FastAPI Configuration
HOST=127.0.0.1
PORT=8000

# Browser Configuration
BROWSER_HEADLESS=true  # Set to false for visible browser during development
BROWSER_TIMEOUT=30000  # 30 seconds timeout for browser operations

# Logging Configuration
LOG_LEVEL=INFO
```

Make sure to:
1. Replace `your_google_api_key_here` with your actual Google API key (get one from https://makersuite.google.com/app/apikey)
2. Adjust other configurations as needed for your environment
3. Never commit the `.env` file to version control

## Running the Application

1.  Ensure your virtual environment is activated (`source venv/bin/activate`).
2.  Start the FastAPI server from the project root directory:
    ```bash
    uvicorn main:app --reload --host 127.0.0.1 --port 8000
    ```
    *   `--reload` enables auto-reloading for backend development (optional).
3.  In a separate terminal, run the main Python application:
    ```bash
    python main.py
    ```
    *   This will start the browser automation and AI agent components.
4.  To build and start the entire project (frontend and backend) using npm, you can also run:
    ```bash
    npm run start
    ```

## Usage

1.  Open your web browser and navigate to `http://127.0.0.1:8000`.
2.  You should see the React application interface with a textarea.
3.  Enter Python code (e.g., `print("Hello from exec!")`) into the textarea.
4.  Click the "Run Code" button.
5.  The output (or any execution error) from the backend will be displayed below the form.

**Remember the security warning! Only run code you trust.**