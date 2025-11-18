#!/bin/bash

# Run Streamlit frontend
echo "Starting Carbon Footprint Tracker Frontend..."
echo "App will be available at http://localhost:8501"
echo ""

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Run Streamlit
streamlit run frontend/app.py
