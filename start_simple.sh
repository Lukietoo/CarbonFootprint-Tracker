#!/bin/bash

# ===========================================
# SIMPLE START SCRIPT
# Starts both backend and frontend easily!
# ===========================================

echo "========================================"
echo "  Carbon Footprint Tracker - SIMPLE"
echo "========================================"
echo ""

# Check if we're in the right directory
if [ ! -f "backend/main_simple.py" ]; then
    echo "❌ Error: Run this from the CarbonFootprint-Tracker directory"
    echo "Try: cd ~/CarbonFootprint-Tracker && ./start_simple.sh"
    exit 1
fi

# Find Python
PYTHON=$(which python3)
if [ -z "$PYTHON" ]; then
    echo "❌ Python 3 not found! Please install Python 3"
    exit 1
fi

echo "Using Python: $PYTHON"
echo ""

# Stop any existing instances
echo "Stopping any existing instances..."
pkill -f "uvicorn backend.main_simple" 2>/dev/null
pkill -f "streamlit run frontend/app_simple" 2>/dev/null
sleep 2

# Start backend
echo "Starting SIMPLE backend..."
$PYTHON -m uvicorn backend.main_simple:app --host 0.0.0.0 --port 8000 --reload &
BACKEND_PID=$!
echo "  Backend started (PID: $BACKEND_PID)"

# Wait for backend
echo "Waiting for backend to start..."
sleep 3

# Check if backend is running
if curl -s http://localhost:8000/ > /dev/null 2>&1; then
    echo "  ✓ Backend is ready!"
else
    echo "  ⚠️  Backend might not be running. Check for errors above."
fi

echo ""

# Start frontend
echo "Starting SIMPLE frontend..."
echo "  Frontend will open at: http://localhost:8501"
echo ""
echo "========================================"
echo "  SIMPLE VERSION IS RUNNING!"
echo "  - Backend: http://localhost:8000"
echo "  - Frontend: http://localhost:8501"
echo "========================================"
echo "  Press Ctrl+C to stop both services"
echo "========================================"
echo ""

streamlit run frontend/app_simple.py

# If streamlit exits, kill backend too
kill $BACKEND_PID 2>/dev/null
