"""
Vercel serverless function handler for FastAPI backend
This allows the FastAPI app to run as a Vercel serverless function
"""
from api.index import app
from mangum import Mangum

# Wrap FastAPI app with Mangum for AWS Lambda/Vercel compatibility
handler = Mangum(app, lifespan="off")

