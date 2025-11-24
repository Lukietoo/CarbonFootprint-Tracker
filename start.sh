#!/bin/bash

echo "======================================"
echo "  Carbon Footprint Tracker Startup"
echo "======================================"
echo ""

# Check if we're in the right directory
if [ ! -f "backend/main.py" ]; then
    echo "Error: Please run this from the CarbonFootprint-Tracker directory"
    echo "Run: cd /home/user/CarbonFootprint-Tracker"
    exit 1
fi

# Kill any existing instances
echo "Stopping any existing instances..."
pkill -f "uvicorn backend.main" 2>/dev/null
pkill -f "streamlit run frontend" 2>/dev/null
sleep 2

# Start backend
echo "Starting backend server..."
python3 -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload > backend.log 2>&1 &
BACKEND_PID=$!
echo "  Backend started (PID: $BACKEND_PID)"

# Wait for backend to be ready
echo "Waiting for backend to start..."
for i in {1..10}; do
    if curl -s http://localhost:8000/ > /dev/null 2>&1; then
        echo "  ✓ Backend is ready!"
        break
    fi
    sleep 1
done

# Check if backend is actually running
if ! curl -s http://localhost:8000/ > /dev/null 2>&1; then
    echo "  ✗ Backend failed to start!"
    echo "  Check backend.log for errors"
    exit 1
fi

# Start frontend
echo ""
echo "Starting frontend..."
echo "  Frontend will open at: http://localhost:8501"
echo ""
echo "======================================"
echo "  Press Ctrl+C to stop both services"
echo "======================================"
echo ""

# Run streamlit in foreground
streamlit run frontend/app.py

# When streamlit exits, kill backend
echo ""
echo "Shutting down..."
kill $BACKEND_PID 2>/dev/null
echo "Done!"
