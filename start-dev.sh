#!/bin/bash

echo "Starting Mental Coach Application..."
echo ""
echo "This will start both the backend and frontend servers."
echo ""
echo "Make sure you have:"
echo "  1. Python 3.12+ and uv installed"
echo "  2. Node.js 18+ and npm installed"
echo "  3. OPENAI_API_KEY environment variable set"
echo ""
read -p "Press Enter to continue..."

# Start backend in background
echo ""
echo "Starting Backend API server..."
cd api
uv run uvicorn api.index:app --reload &
BACKEND_PID=$!
cd ..

# Wait a moment for backend to start
sleep 3

# Start frontend in background
echo ""
echo "Starting Frontend development server..."
cd frontend
npm run dev &
FRONTEND_PID=$!
cd ..

echo ""
echo "Both servers are starting..."
echo "Backend: http://localhost:8000"
echo "Frontend: http://localhost:3000"
echo ""
echo "Press Ctrl+C to stop both servers..."

# Wait for user interrupt
trap "kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; exit" INT TERM
wait

