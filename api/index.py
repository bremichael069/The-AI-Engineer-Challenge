from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import OpenAI
import os
from dotenv import load_dotenv
from pathlib import Path

# Load .env file from project root (parent of api directory)
# This ensures we find the .env file regardless of where uvicorn is run from
env_path = Path(__file__).parent.parent / '.env'

# Try loading with dotenv first
load_dotenv(dotenv_path=env_path, override=True)
load_dotenv(override=False)

# If still not set, manually read the .env file as fallback
if not os.getenv("OPENAI_API_KEY") and env_path.exists():
    with open(env_path, 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                if key.strip() == 'OPENAI_API_KEY':
                    os.environ['OPENAI_API_KEY'] = value.strip()
                    break

app = FastAPI()

# CORS so the frontend can talk to backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

# Initialize OpenAI client lazily - will be created when needed
def get_openai_client():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="OPENAI_API_KEY not configured")
    return OpenAI(api_key=api_key)

class ChatRequest(BaseModel):
    message: str

@app.get("/")
def root():
    return {"status": "ok"}

@app.get("/api/health")
def health():
    """Health check endpoint for frontend to verify backend connectivity"""
    api_key = os.getenv("OPENAI_API_KEY")
    # Debug info (remove in production)
    env_file = Path(__file__).parent.parent / '.env'
    return {
        "status": "ok",
        "openai_configured": bool(api_key),
        "env_file_exists": env_file.exists(),
        "env_file_path": str(env_file),
        "cwd": str(Path.cwd())
    }

@app.post("/api/chat")
def chat(request: ChatRequest):
    try:
        client = get_openai_client()
        user_message = request.message
        response = client.chat.completions.create(
            model="gpt-5",
            messages=[
                {"role": "system", "content": "You are a supportive mental coach."},
                {"role": "user", "content": user_message}
            ]
        )
        return {"reply": response.choices[0].message.content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error calling OpenAI API: {str(e)}")
