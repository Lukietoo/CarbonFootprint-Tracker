#!/bin/bash

echo "======================================"
echo "  Carbon Footprint Tracker"
echo "======================================"

cd /home/user/CarbonFootprint-Tracker

# Kill any existing instances
pkill -f "uvicorn backend.main" 2>/dev/null
pkill -f "streamlit run frontend" 2>/dev/null
sleep 1

# Start backend
echo "Starting backend..."
/usr/local/bin/python3 -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload > backend.log 2>&1 &

# Wait for backend
sleep 3

# Start frontend
echo "Starting frontend..."
echo "Opening at: http://localhost:8501"
echo ""
streamlit run frontend/app.py

# Cleanup on exit
pkill -f "uvicorn backend.main" 2>/dev/null
