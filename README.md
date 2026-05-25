# RepoPilot AI

RepoPilot AI analyzes public GitHub repositories using AI and returns project summaries, tech stack insights, interview questions, and setup instructions in one workflow.

## Features

- Analyze public GitHub repositories from a URL
- Generate AI-powered project summaries and architecture notes
- Create interview questions by difficulty level
- Generate setup instructions and common issue notes
- Fetch GitHub metadata, README content, languages, file structure, and key config files
- React/TanStack frontend integrated with a FastAPI backend

## Tech Stack

- Backend: FastAPI, Python, LangChain, LangGraph
- AI: Gemini API
- Frontend: React, TanStack Start, Vite, TypeScript, Tailwind CSS
- APIs: GitHub REST API

## Project Structure

```text
.
|-- app/                  # FastAPI app, routes, services, graph workflow
|-- uploaded-ui/          # React/TanStack frontend
|-- main.py               # FastAPI entrypoint
|-- run_server.py         # Backend runner
|-- requirements.txt      # Python dependencies
`-- .env.example          # Environment variable template
```

## Setup

### Backend

```powershell
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
```

Update `.env` with your keys:

```env
GEMINI_API_KEY=your_gemini_api_key
GEMINI_MODEL=gemini-2.5-flash-lite
GITHUB_TOKEN=your_github_token_optional
DEBUG=true
```

Start the backend:

```powershell
.\.venv\Scripts\python.exe run_server.py
```

Backend runs at:

```text
http://127.0.0.1:8000
```

API docs:

```text
http://127.0.0.1:8000/docs
```

### Frontend

```powershell
cd uploaded-ui
npm install
npm run dev -- --host 127.0.0.1 --port 5178
```

Frontend runs at:

```text
http://127.0.0.1:5178
```

## API Endpoints

- `GET /api/v1/health`
- `POST /api/v1/analyze`
- `POST /api/v1/analyze/questions-only`
- `POST /api/v1/analyze/setup-only`

## Notes

- Do not commit `.env`; it contains private API keys.
- If Gemini generation fails with a quota error, switch to a model with available quota, wait for quota reset, or enable billing.
- For faster responses, use fewer questions and keep `GEMINI_MODEL=gemini-2.5-flash-lite`.
