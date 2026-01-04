"""
Vercel serverless function handler
Wraps FastAPI app for Vercel deployment
"""
from mangum import Mangum
from api.index import app

handler = Mangum(app, lifespan="off")
