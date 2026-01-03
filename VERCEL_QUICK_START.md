# Quick Vercel Deployment Guide

## Deploy Your Frontend to Vercel

### Method 1: Using Vercel Dashboard (Easiest)

1. **Push your code to GitHub:**
   ```bash
   git add .
   git commit -m "Ready for Vercel deployment"
   git push
   ```

2. **Go to [vercel.com](https://vercel.com) and:**
   - Click "Add New Project"
   - Import your GitHub repository
   - **Important:** Set the root directory to `frontend`
   - Add environment variable: `NEXT_PUBLIC_API_URL` = your backend URL
   - Click "Deploy"

### Method 2: Using Vercel CLI

1. **Install Vercel CLI:**
   ```bash
   npm install -g vercel
   ```

2. **Login:**
   ```bash
   vercel login
   ```

3. **Deploy from frontend directory:**
   ```bash
   cd frontend
   vercel
   ```

4. **Set environment variables:**
   ```bash
   vercel env add NEXT_PUBLIC_API_URL
   # Enter your backend URL when prompted
   ```

### After Deployment

1. **Get your Vercel URL** (e.g., `https://your-app.vercel.app`)

2. **Set environment variable in Vercel dashboard:**
   - Go to Project Settings → Environment Variables
   - Add: `NEXT_PUBLIC_API_URL` = `https://your-backend-url.com`
   - Redeploy if needed

3. **Deploy your backend separately:**
   - Use Railway, Render, or another service
   - Set `OPENAI_API_KEY` environment variable
   - Update `NEXT_PUBLIC_API_URL` in Vercel to point to your backend

## Your URLs

- **Frontend:** `https://your-app.vercel.app`
- **Backend:** Deploy separately (Railway/Render recommended)

## Environment Variables Needed

### In Vercel (Frontend):
- `NEXT_PUBLIC_API_URL` - Your backend API URL

### In Backend Service (Railway/Render):
- `OPENAI_API_KEY` - Your OpenAI API key

That's it! Your app should be live on Vercel.

