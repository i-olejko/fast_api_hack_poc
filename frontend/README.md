# Frontend - React Application

This is the React frontend for the FastAPI + React Python Code Runner project. It allows users to input Python code, send it to the backend, and display the execution output.

## Setup

1. Navigate to the `frontend` directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

## Running the Development Server

Start the React development server with:

```bash
npm start
```

This will open the app at [http://localhost:3000](http://localhost:3000). The page reloads automatically on code changes.

## Building for Production

To build the optimized production bundle:

```bash
npm run build
```

The build output will be in the `build/` directory, which is served by the FastAPI backend in production.

## Project Structure

- **src/components/**
  - `NavBar.js` - Top navigation bar
  - `TaskInput.js` - Textarea and button for submitting Python code
  - `OutputDisplay.js` - Displays the output or errors from backend execution
- **src/pages/**
  - `FreeRunPage.js` - Main page for running arbitrary Python code
  - `ConsoleTestPage.js` - Additional console testing interface
- **src/App.js** - Main React component that sets up routing and layout
- **public/** - Static assets and HTML template

## Notes

- This project was bootstrapped with [Create React App](https://create-react-app.dev/).
- The frontend communicates with the FastAPI backend running on `http://127.0.0.1:8000` by default.
