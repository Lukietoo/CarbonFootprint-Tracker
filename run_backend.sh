#!/bin/bash

# Run FastAPI backend server
echo "Starting Carbon Footprint Tracker Backend..."
echo "API will be available at http://localhost:8000"
echo "API docs at http://localhost:8000/docs"
echo ""

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Run the server
python -m uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
