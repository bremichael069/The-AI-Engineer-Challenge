# Vercel Deployment Guide

This guide will help you deploy your Mental Coach application to Vercel.

## Deployment Options

### Option 1: Deploy Frontend Only (Recommended)

Deploy the Next.js frontend to Vercel and host the backend separately (Railway, Render, etc.).

#### Steps:

1. **Prepare the Frontend:**
   ```bash
   cd frontend
   npm install
   npm run build
   ```

2. **Deploy to Vercel:**
   - Install Vercel CLI: `npm i -g vercel`
   - Login: `vercel login`
   - Deploy: `cd frontend && vercel`

3. **Set Environment Variables in Vercel:**
   - Go to your project settings in Vercel dashboard
   - Add environment variable:
     - `NEXT_PUBLIC_API_URL` = Your backend API URL (e.g., `https://your-backend.railway.app`)

4. **Update Frontend API Client:**
   The frontend will automatically use `NEXT_PUBLIC_API_URL` if set, otherwise defaults to `http://localhost:8000`

### Option 2: Deploy Both Frontend and Backend to Vercel

Deploy both services to Vercel using serverless functions for the backend.

#### Prerequisites:
- Add `mangum` to your dependencies for AWS Lambda compatibility

#### Steps:

1. **Update Dependencies:**
   ```bash
   # Add mangum to pyproject.toml
   ```

2. **Create Vercel Serverless Function:**
   - Create `api/serverless.py` (already created)
   - Create `vercel.json` in root (already created)

3. **Deploy:**
   ```bash
   vercel
   ```

4. **Set Environment Variables:**
   - `OPENAI_API_KEY` - Your OpenAI API key
   - `NEXT_PUBLIC_API_URL` - Leave empty or set to your Vercel domain

## Recommended Setup

For best performance and simplicity:

1. **Frontend on Vercel** (automatic Next.js optimization)
2. **Backend on Railway/Render** (better for Python/FastAPI)

### Backend Deployment (Railway/Render):

1. **Railway:**
   - Connect your GitHub repo
   - Set `OPENAI_API_KEY` environment variable
   - Set start command: `uv run uvicorn api.index:app --host 0.0.0.0 --port $PORT`

2. **Render:**
   - Create new Web Service
   - Set build command: `uv sync`
   - Set start command: `uv run uvicorn api.index:app --host 0.0.0.0 --port $PORT`
   - Add environment variable: `OPENAI_API_KEY`

3. **Update Frontend:**
   - Set `NEXT_PUBLIC_API_URL` in Vercel to your backend URL

## Quick Deploy Commands

### Frontend Only:
```bash
cd frontend
vercel
```

### Full Stack (if using serverless):
```bash
vercel
```

## Environment Variables

### Frontend (Vercel):
- `NEXT_PUBLIC_API_URL` - Backend API URL (optional, defaults to localhost:8000)

### Backend (Railway/Render/Vercel):
- `OPENAI_API_KEY` - Your OpenAI API key (required)

## Troubleshooting

**Build fails:**
- Make sure all dependencies are in `package.json` (frontend) and `pyproject.toml` (backend)
- Check that Node.js version is compatible (18+)

**API calls fail:**
- Verify `NEXT_PUBLIC_API_URL` is set correctly
- Check CORS settings in backend
- Ensure backend is running and accessible

**Environment variables not loading:**
- Restart the deployment after adding variables
- Check variable names match exactly (case-sensitive)

