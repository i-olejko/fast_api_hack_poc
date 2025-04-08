#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}Starting setup process...${NC}"

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Python 3 is not installed. Please install Python 3 and try again.${NC}"
    exit 1
fi

# Install system dependencies
echo -e "${YELLOW}Installing system dependencies...${NC}"
if command -v apt-get &> /dev/null; then
    sudo apt-get update
    sudo apt-get install -y libgbm1
else
    echo -e "${YELLOW}Unable to automatically install system dependencies. Please install libgbm1 manually if needed.${NC}"
fi

# Create and activate virtual environment
echo -e "${YELLOW}Setting up Python virtual environment...${NC}"
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
echo -e "${YELLOW}Installing Python dependencies...${NC}"
pip install --upgrade pip
pip install fastapi uvicorn python-dotenv browser-use playwright langchain-google-genai

# Install Playwright browser
echo -e "${YELLOW}Installing Playwright browser...${NC}"
playwright install chromium

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo -e "${YELLOW}Creating .env file...${NC}"
    cat > .env << EOL
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
EOL
    echo -e "${YELLOW}Please update the .env file with your Google API key.${NC}"
fi

# Setup frontend
if [ -d "frontend" ]; then
    echo -e "${YELLOW}Setting up frontend...${NC}"
    cd frontend
    npm install
    npm run build
    cd ..
fi

echo -e "${GREEN}Setup completed successfully!${NC}"
echo -e "${YELLOW}Next steps:${NC}"
echo "1. Update the .env file with your Google API key"
echo "2. Activate the virtual environment: source venv/bin/activate"
echo "3. Run the application: uvicorn main:app --reload" 