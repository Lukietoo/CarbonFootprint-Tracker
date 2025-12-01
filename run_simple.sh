#!/bin/bash

# Simple Carbon Footprint Tracker Runner
# This script runs the simplified single-file version

echo "🌍 Starting Simplified Carbon Footprint Tracker..."
echo ""

# Check if streamlit is installed
if ! command -v streamlit &> /dev/null; then
    echo "⚠️  Streamlit not found. Installing dependencies..."
    pip install -r requirements-simple.txt
fi

# Run the simplified app
echo "🚀 Launching app at http://localhost:8501"
echo ""
streamlit run simple_app.py
