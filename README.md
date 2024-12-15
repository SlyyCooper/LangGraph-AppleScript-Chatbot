# LangGraph AppleScript Chatbot

A modern chatbot built with LangGraph that can execute AppleScript commands on macOS, powered by Claude 3 Opus.

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On macOS/Linux
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file with your Anthropic API key:
```bash
ANTHROPIC_API_KEY=your_api_key_here
```

## Running the Application

Start the FastAPI server:
```bash
python main.py
```

The API will be available at `http://localhost:8000`

## Usage

Send POST requests to `/chat` endpoint with JSON payload:
```json
{
    "message": "execute applescript: tell application \"Finder\" to get name of every window",
    "history": []
}
```

The chatbot supports:
- General conversation using Claude 3
- AppleScript execution (prefix commands with "execute applescript:") 
