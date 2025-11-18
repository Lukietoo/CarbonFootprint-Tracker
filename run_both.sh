#!/bin/bash

# Run both backend and frontend together
echo "Starting Carbon Footprint Tracker..."
echo ""

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Start backend in background
echo "Starting backend server..."
python -m uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!

# Wait a moment for backend to start
sleep 3

# Start frontend
echo "Starting frontend..."
streamlit run frontend/app.py

# When Streamlit exits, kill the backend
kill $BACKEND_PID
