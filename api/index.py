"""
Vercel serverless function - main entry point
This file serves as the FastAPI entrypoint that Vercel detects
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import OpenAI
import os
import httpx

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

class ChatRequest(BaseModel):
    message: str

def get_openai_client():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="OPENAI_API_KEY not configured")
    # Configure HTTP client with extended timeout for serverless environments
    http_client = httpx.Client(
        timeout=httpx.Timeout(60.0, connect=10.0),
        limits=httpx.Limits(max_keepalive_connections=5, max_connections=10)
    )
    # Configure OpenAI client with custom HTTP client for better serverless compatibility
    return OpenAI(
        api_key=api_key,
        http_client=http_client,
        max_retries=3
    )

@app.get("/api/")
def root():
    return {"status": "ok"}

@app.get("/api/health")
def health():
    api_key = os.getenv("OPENAI_API_KEY")
    return {
        "status": "ok",
        "openai_configured": bool(api_key)
    }

@app.post("/api/chat")
def chat(request: ChatRequest):
    try:
        # Debug: Check if API key is present (don't log the actual key)
        api_key = os.getenv("OPENAI_API_KEY")
        print(f"DEBUG: API key present: {bool(api_key)}, length: {len(api_key) if api_key else 0}, starts with 'sk-': {api_key.startswith('sk-') if api_key else False}")
        
        client = get_openai_client()
        print(f"DEBUG: Attempting OpenAI API call with model: gpt-4o")
        # Try gpt-3.5-turbo first (most reliable), fallback to gpt-4o if needed
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # Most reliable model for serverless
            messages=[
                {"role": "system", "content": "You are a supportive mental coach."},
                {"role": "user", "content": request.message}
            ],
            max_tokens=500,
            temperature=0.7
        )
        print(f"DEBUG: OpenAI API call successful")
        return {"reply": response.choices[0].message.content}
    except Exception as e:
        error_msg = str(e)
        error_type = type(e).__name__
        
        # Log the full error for debugging (this will appear in Vercel logs)
        print(f"OpenAI API Error - Type: {error_type}, Message: {error_msg}")
        
        # Provide more helpful error messages based on error type
        if "Connection" in error_msg or "timeout" in error_msg.lower() or "ConnectTimeout" in error_type:
            error_msg = f"Connection error. The OpenAI API is temporarily unavailable. Please try again. (Details: {error_type}: {error_msg})"
        elif "Invalid" in error_msg or "model" in error_msg.lower() or "NotFoundError" in error_type or "does not exist" in error_msg.lower():
            error_msg = f"Model error: The model 'gpt-5.2' may not be available. Please use a valid model like 'gpt-4o', 'gpt-4-turbo', or 'gpt-3.5-turbo'. (Details: {error_type}: {error_msg})"
        elif "rate limit" in error_msg.lower() or "RateLimitError" in error_type:
            error_msg = "Rate limit exceeded. Please try again in a moment."
        elif "Authentication" in error_msg or "InvalidAPIKey" in error_type:
            error_msg = "API key error. Please check your OpenAI API key configuration."
        else:
            # Return the actual error for debugging
            error_msg = f"{error_type}: {error_msg}"
        
        raise HTTPException(status_code=500, detail=f"Error calling OpenAI API: {error_msg}")
