# Mental Coach - AI Support Chat Application

A full-stack application featuring a FastAPI backend and Next.js frontend that provides AI-powered mental coaching support.

## Architecture

- **Backend**: FastAPI server (`api/` folder) running on `http://localhost:8000`
- **Frontend**: Next.js application (`frontend/` folder) running on `http://localhost:3000`

## Quick Start

### Option 1: Run Both Services Together (Recommended)

**Windows:**
```bash
start-dev.bat
```

**Linux/Mac:**
```bash
chmod +x start-dev.sh
./start-dev.sh
```

This will start both the backend and frontend servers in separate terminal windows.

### Option 2: Run Services Separately

#### 1. Start the Backend

```bash
cd api
uv sync
uv run uvicorn api.index:app --reload
```

The backend will be available at `http://localhost:8000`

#### 2. Start the Frontend

In a new terminal:

```bash
cd frontend
npm install
npm run dev
```

The frontend will be available at `http://localhost:3000`

## Prerequisites

### Backend Requirements
- [`uv`](https://github.com/astral-sh/uv) package manager (`pip install uv`)
- `uv` will provision Python 3.12 automatically
- OpenAI API key set as `OPENAI_API_KEY` environment variable

### Frontend Requirements
- Node.js 18+ and npm
- All dependencies will be installed via `npm install`

## Environment Setup

### Backend Environment
Set your OpenAI API key:

**Windows (PowerShell):**
```powershell
$env:OPENAI_API_KEY="sk-your-key-here"
```

**Windows (CMD):**
```cmd
set OPENAI_API_KEY=sk-your-key-here
```

**Linux/Mac:**
```bash
export OPENAI_API_KEY=sk-your-key-here
```

Or create a `.env` file in the `api/` directory:
```
OPENAI_API_KEY=sk-your-key-here
```

### Frontend Environment (Optional)
If your backend runs on a different URL, create `frontend/.env.local`:
```
NEXT_PUBLIC_API_URL=http://your-backend-url:port
```

## Integration Details

The frontend and backend are fully integrated:

- **API Endpoint**: Frontend connects to `http://localhost:8000/api/chat` by default
- **CORS**: Backend is configured to accept requests from any origin
- **Health Check**: Frontend displays backend connection status
- **Error Handling**: Comprehensive error messages for connection issues

### Backend API Endpoints

- `GET /` - Root endpoint, returns `{"status": "ok"}`
- `GET /api/health` - Health check, returns backend status and OpenAI configuration
- `POST /api/chat` - Chat endpoint, accepts `{"message": "string"}` and returns `{"reply": "string"}`

### Frontend Features

- Real-time chat interface
- Backend connection status indicator
- Dark/light mode toggle
- Responsive design
- Error handling and user feedback

## Development

### Backend Development
- Backend auto-reloads on code changes (via `--reload` flag)
- API documentation available at `http://localhost:8000/docs` (Swagger UI)

### Frontend Development
- Frontend hot-reloads on code changes
- TypeScript for type safety
- Tailwind CSS for styling

## Testing the Integration

1. Start both services (see Quick Start above)
2. Open `http://localhost:3000` in your browser
3. You should see "Backend connected" status indicator
4. Type a message and send it
5. The AI coach should respond

## Troubleshooting

### Backend won't start
- Ensure `uv` is installed: `pip install uv`
- Check that Python 3.12+ is available
- Verify `OPENAI_API_KEY` is set

### Frontend won't connect to backend
- Ensure backend is running on port 8000
- Check browser console for CORS errors
- Verify the API URL in frontend configuration

### Port already in use
- Backend: Change port with `--port 8001` in uvicorn command
- Frontend: Next.js will automatically use the next available port (3001, 3002, etc.)

## Project Structure

```
.
├── api/                 # FastAPI backend
│   ├── index.py       # Main API server
│   └── README.md      # Backend documentation
├── frontend/           # Next.js frontend
│   ├── app/           # Next.js App Router pages
│   ├── components/    # React components
│   ├── lib/           # Utilities and API client
│   └── README.md      # Frontend documentation
├── start-dev.bat      # Windows script to run both services
├── start-dev.sh       # Linux/Mac script to run both services
└── README.md          # This file
```

## Deployment

### Backend Deployment
The backend can be deployed to any Python hosting service (Railway, Render, etc.)

### Frontend Deployment
The frontend is optimized for Vercel deployment. See `frontend/README.md` for details.

## License

This project is part of The AI Engineer Challenge.
