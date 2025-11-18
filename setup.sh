#!/bin/bash

echo "Setting up Carbon Footprint Tracker..."
echo ""

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo "Installing dependencies..."
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "Creating .env file from template..."
    cp .env.example .env
    echo ""
    echo "⚠️  IMPORTANT: Please edit .env file with your API keys:"
    echo "   - OPENAI_API_KEY (for AI suggestions)"
    echo "   - CLIMATIQ_API_KEY (for carbon data)"
    echo ""
fi

# Make scripts executable
chmod +x run_backend.sh
chmod +x run_frontend.sh
chmod +x run_both.sh

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env file with your API keys (optional, app works without them)"
echo "2. Run './run_both.sh' to start both backend and frontend"
echo "   OR"
echo "   Run './run_backend.sh' and './run_frontend.sh' in separate terminals"
echo ""
echo "The app will be available at:"
echo "  - Frontend: http://localhost:8501"
echo "  - Backend API: http://localhost:8000"
echo "  - API Docs: http://localhost:8000/docs"
echo ""
