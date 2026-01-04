"""
Vercel serverless function - main entry point
This file serves as the FastAPI entrypoint that Vercel detects
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import OpenAI
from openai import APIError, APIConnectionError, RateLimitError
import os
import traceback
import sys

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
    print(f"DEBUG: get_openai_client() called")
    print(f"DEBUG: API key exists: {bool(api_key)}")
    print(f"DEBUG: API key length (before strip): {len(api_key) if api_key else 0}")
    
    # CRITICAL FIX: Strip whitespace and newlines from API key
    # This fixes the "Illegal header value" error caused by \r\n in the key
    if api_key:
        api_key = api_key.strip()
        print(f"DEBUG: API key length (after strip): {len(api_key)}")
        print(f"DEBUG: API key has newlines: {'\\n' in api_key or '\\r' in api_key}")
        print(f"DEBUG: API key prefix: {api_key[:10] if len(api_key) > 10 else 'N/A'}...")
    
    if not api_key:
        print("DEBUG: ERROR - OPENAI_API_KEY not configured")
        raise HTTPException(status_code=500, detail="OPENAI_API_KEY not configured")
    
    # Use default HTTP client (simpler, more reliable)
    print("DEBUG: Creating OpenAI client with default configuration...")
    print("DEBUG: Using timeout=30.0, max_retries=0")
    try:
        client = OpenAI(
            api_key=api_key,
            timeout=30.0,
            max_retries=0  # No automatic retries - we want to see the actual error
        )
        print("DEBUG: ✅ OpenAI client created successfully")
        return client
    except Exception as e:
        print(f"DEBUG: ❌ ERROR creating OpenAI client: {type(e).__name__}: {str(e)}")
        print(f"DEBUG: Full traceback:\n{traceback.format_exc()}")
        raise

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
    print("=" * 80)
    print("DEBUG: ========== CHAT ENDPOINT CALLED ==========")
    print(f"DEBUG: Request message: {request.message[:100]}...")
    print(f"DEBUG: Python version: {sys.version}")
    print(f"DEBUG: Current working directory: {os.getcwd()}")
    
    # Check environment
    env_vars = [k for k in os.environ.keys() if 'OPENAI' in k.upper()]
    print(f"DEBUG: Environment variables with 'OPENAI': {', '.join(env_vars) if env_vars else 'NONE'}")
    
    try:
        # Get API key and log details
        api_key = os.getenv("OPENAI_API_KEY")
        print(f"DEBUG: API key retrieved from environment")
        print(f"DEBUG: API key present: {bool(api_key)}")
        print(f"DEBUG: API key length (raw): {len(api_key) if api_key else 0}")
        
        # CRITICAL FIX: Strip whitespace and newlines from API key
        if api_key:
            api_key = api_key.strip()
            print(f"DEBUG: API key length (stripped): {len(api_key)}")
            print(f"DEBUG: API key contains newlines: {'\\n' in api_key or '\\r' in api_key}")
            print(f"DEBUG: API key starts with 'sk-': {api_key.startswith('sk-')}")
            print(f"DEBUG: API key starts with 'sk-proj-': {api_key.startswith('sk-proj-')}")
        
        # Create OpenAI client
        print("DEBUG: Creating OpenAI client...")
        client = get_openai_client()
        print("DEBUG: OpenAI client created successfully")
        
        # Prepare the API call
        model = "gpt-3.5-turbo"
        messages = [
            {"role": "system", "content": "You are a supportive mental coach."},
            {"role": "user", "content": request.message}
        ]
        
        print(f"DEBUG: Model: {model}")
        print(f"DEBUG: Messages count: {len(messages)}")
        print(f"DEBUG: Max tokens: 500")
        print(f"DEBUG: Temperature: 0.7")
        print("DEBUG: Making OpenAI API call NOW...")
        print(f"DEBUG: API endpoint should be: https://api.openai.com/v1/chat/completions")
        
        # Make the API call
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            max_tokens=500,
            temperature=0.7
        )
        
        print("DEBUG: ✅ OpenAI API call successful!")
        print(f"DEBUG: Response received, choices count: {len(response.choices)}")
        reply = response.choices[0].message.content
        print(f"DEBUG: Reply length: {len(reply)}")
        print(f"DEBUG: Reply preview: {reply[:100]}...")
        print("=" * 80)
        
        return {"reply": reply}
        
    except APIConnectionError as e:
        error_msg = str(e)
        error_type = type(e).__name__
        print("=" * 80)
        print(f"DEBUG: ❌ APIConnectionError caught")
        print(f"DEBUG: Error type: {error_type}")
        print(f"DEBUG: Error message: {error_msg}")
        print(f"DEBUG: Error args: {e.args}")
        print(f"DEBUG: Error repr: {repr(e)}")
        
        # Try to get more details
        detailed_info = f"APIConnectionError Details:\n"
        detailed_info += f"- Type: {error_type}\n"
        detailed_info += f"- Message: {error_msg}\n"
        detailed_info += f"- Args: {e.args}\n"
        
        if hasattr(e, 'request'):
            req = e.request
            detailed_info += f"- Request method: {getattr(req, 'method', 'N/A')}\n"
            detailed_info += f"- Request URL: {getattr(req, 'url', 'N/A')}\n"
            detailed_info += f"- Request headers: {getattr(req, 'headers', 'N/A')}\n"
        
        if hasattr(e, 'response'):
            resp = e.response
            detailed_info += f"- Response status: {getattr(resp, 'status_code', 'N/A')}\n"
            detailed_info += f"- Response text: {getattr(resp, 'text', 'N/A')}\n"
        
        print(f"DEBUG: Detailed info:\n{detailed_info}")
        print(f"DEBUG: Full traceback:\n{traceback.format_exc()}")
        print("=" * 80)
        
        raise HTTPException(
            status_code=500, 
            detail=f"OpenAI API Connection Error: {error_msg}\n\nDebug Info:\n{detailed_info}\n\nCheck Vercel logs for full traceback."
        )
        
    except APIError as e:
        error_msg = str(e)
        error_type = type(e).__name__
        print("=" * 80)
        print(f"DEBUG: ❌ APIError caught")
        print(f"DEBUG: Error type: {error_type}")
        print(f"DEBUG: Error message: {error_msg}")
        print(f"DEBUG: Full traceback:\n{traceback.format_exc()}")
        print("=" * 80)
        
        raise HTTPException(
            status_code=500,
            detail=f"OpenAI API Error ({error_type}): {error_msg}\n\nCheck Vercel logs for full traceback."
        )
        
    except Exception as e:
        error_msg = str(e)
        error_type = type(e).__name__
        print("=" * 80)
        print(f"DEBUG: ❌ Unexpected error caught")
        print(f"DEBUG: Error type: {error_type}")
        print(f"DEBUG: Error message: {error_msg}")
        print(f"DEBUG: Full traceback:\n{traceback.format_exc()}")
        print("=" * 80)
        
        raise HTTPException(
            status_code=500,
            detail=f"Unexpected Error ({error_type}): {error_msg}\n\nFull traceback available in Vercel logs."
        )
