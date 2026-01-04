# Vercel Backend Deployment Issue

## Current Status
- ✅ Frontend: Successfully deployed and working
- ❌ Backend: Python serverless function not being built by Vercel

## Problem
Vercel's build logs only show the Next.js frontend being built. The Python backend function (`api/vercel_handler.py`) is not being detected or built.

## Possible Solutions

### Option 1: Deploy Backend Separately (Recommended)
Deploy the backend to a service better suited for Python/FastAPI:

**Railway:**
1. Go to [railway.app](https://railway.app)
2. New Project → Deploy from GitHub
3. Select your repository
4. Set environment variable: `OPENAI_API_KEY`
5. Set start command: `uv run uvicorn api.index:app --host 0.0.0.0 --port $PORT`
6. Get your Railway URL
7. Update frontend: Set `NEXT_PUBLIC_API_URL` in Vercel to your Railway URL

**Render:**
1. Go to [render.com](https://render.com)
2. New → Web Service
3. Connect GitHub repository
4. Build command: `uv sync`
5. Start command: `uv run uvicorn api.index:app --host 0.0.0.0 --port $PORT`
6. Add environment variable: `OPENAI_API_KEY`
7. Update frontend: Set `NEXT_PUBLIC_API_URL` in Vercel

### Option 2: Fix Vercel Python Function
The issue might be that Vercel needs:
1. The function in the root `api/` directory (not nested)
2. A `requirements.txt` in the same directory as the handler
3. Proper Python version specification

Try moving files to match Vercel's expected structure:
- `api/vercel_handler.py` (handler)
- `api/requirements.txt` (dependencies)
- Ensure `vercel.json` routes `/api/*` correctly

### Option 3: Use Vercel's New Function Format
Vercel might need the function in a different format. Check:
- Vercel dashboard → Functions tab
- See if any Python functions are detected
- Check build logs for Python-related errors

## Current Configuration

**vercel.json:**
```json
{
  "version": 2,
  "builds": [
    {
      "src": "frontend/package.json",
      "use": "@vercel/next"
    },
    {
      "src": "api/api/vercel_handler.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/api/(.*)",
      "dest": "api/api/vercel_handler.py"
    },
    {
      "src": "/(.*)",
      "dest": "frontend/$1"
    }
  ]
}
```

**Files:**
- `api/api/vercel_handler.py` - Handler
- `api/api/requirements.txt` - Dependencies
- `api/index.py` - FastAPI app

## Next Steps
1. Check Vercel dashboard for function build errors
2. Consider deploying backend separately (Railway/Render)
3. Or continue troubleshooting Vercel Python function deployment

