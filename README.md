# 🌍 Carbon Footprint Tracker

A Python-based web application that automatically estimates your carbon footprint from purchase data and offers actionable suggestions to reduce it.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 🚀 Quick Start - Simplified Version

**Want to get started in 30 seconds?** Try the simplified single-file version:

```bash
pip install -r requirements-simple.txt
./run_simple.sh
```

See [README-SIMPLE.md](README-SIMPLE.md) for details. The simple version:
- ✅ Single file (737 lines vs 2,200+)
- ✅ No database setup needed
- ✅ No API keys required
- ✅ Only 3 dependencies
- ✅ Runs instantly
- ✅ Data export/import to persist across sessions
- ✅ Carbon budget comparison (US, World, Paris targets)
- ✅ Enhanced suggestions with specific alternatives
- ✅ Multiple sample datasets (Low/Medium/High carbon)

---

## Overview

Most people want to live sustainably but don't know where to start. **Carbon Footprint Tracker** bridges that gap by analyzing receipts or bank transactions, estimating the CO₂ impact of each purchase, and providing data-driven recommendations to help users make greener choices.

This project combines sustainability data, NLP classification, and AI-generated insights to help users visualize and improve their environmental impact.

## Features

- **📊 Transaction Analysis**: Parse receipts or bank data (CSV or API input)
- **🤖 AI Classification**: Categorize purchases (e.g., food, transport, retail) using NLP
- **🌱 Carbon Estimation**: Fetch emission data via the Climatiq API or use local estimates
- **💡 Smart Suggestions**: Generate personalized tips with the OpenAI API
- **📈 Visualization**: Display monthly carbon usage with interactive Streamlit dashboard
- **📤 Easy Upload**: Upload CSV files or add transactions manually
- **🎯 Progress Tracking**: Monitor your carbon footprint over time

## Screenshots

### Dashboard Overview
Track your total emissions, monthly trends, and category breakdown with interactive visualizations.

### Transaction History
View all your purchases with carbon impact calculated for each transaction.

### Personalized Suggestions
Get AI-powered recommendations tailored to your spending habits.

## Tech Stack

| Component | Technology |
|-----------|-----------|
| Backend | FastAPI (Python) |
| Database | SQLite (default) / PostgreSQL (optional) |
| NLP & AI | Pattern Matching / OpenAI API |
| Carbon Data | Climatiq API + Local Estimates |
| Visualization | Streamlit |
| Charts | Plotly |
| OCR (optional) | Tesseract / AWS Textract |

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment (recommended)

### Quick Start

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/CarbonFootprint-Tracker.git
   cd CarbonFootprint-Tracker
   ```

2. **Run the setup script**
   ```bash
   chmod +x setup.sh
   ./setup.sh
   ```

   **Note**: The app uses SQLite by default. If you want to use PostgreSQL/Supabase instead, install additional dependencies:
   ```bash
   pip install -r requirements-postgres.txt
   ```

3. **Configure environment variables** (optional)

   Edit `.env` file with your API keys:
   ```bash
   # Optional: For AI-powered suggestions
   OPENAI_API_KEY=your_openai_api_key

   # Optional: For accurate carbon data
   CLIMATIQ_API_KEY=your_climatiq_api_key
   ```

   **Note**: The app works without API keys using local estimates and rule-based suggestions.

4. **Start the application**
   ```bash
   ./run_both.sh
   ```

   Or run backend and frontend separately:
   ```bash
   # Terminal 1 - Backend
   ./run_backend.sh

   # Terminal 2 - Frontend
   ./run_frontend.sh
   ```

5. **Access the application**
   - Frontend: http://localhost:8501
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

## Manual Installation

If you prefer manual setup:

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run backend
python -m uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000

# In another terminal, run frontend
streamlit run frontend/app.py
```

## Usage

### 1. Load Sample Data

Click the "Load Sample Data" button in the sidebar to populate the app with demo transactions.

### 2. Upload Your Own Data

Navigate to the "Upload Data" page and upload a CSV file with your transactions.

**CSV Format:**
```csv
date,description,amount
2024-01-15,Whole Foods Market,87.50
2024-01-16,Shell Gas Station,45.00
2024-01-17,United Airlines,350.00
```

**Required columns:**
- `description` (or `merchant`/`name`): Purchase description
- `amount` (or `total`/`price`): Transaction amount in USD

**Optional columns:**
- `date`: Transaction date (defaults to current date)
- `category`: Pre-labeled category (will be auto-classified if not provided)

### 3. View Dashboard

Explore your carbon footprint with:
- Total and monthly emissions
- Category breakdown (pie chart)
- Top emission categories (bar chart)
- Timeline of emissions over time

### 4. Get Suggestions

Visit the "Suggestions" page for personalized recommendations to reduce your carbon footprint.

### 5. Manual Entry

Add individual transactions manually through the "Upload Data" page.

## API Endpoints

The FastAPI backend provides the following endpoints:

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Health check |
| `/api/transactions` | GET | Get all transactions |
| `/api/transactions` | POST | Create a transaction |
| `/api/transactions/upload` | POST | Upload CSV file |
| `/api/dashboard` | GET | Get dashboard statistics |
| `/api/suggestions` | GET | Get carbon reduction suggestions |
| `/api/sample-data` | POST | Load sample data |

Full API documentation available at: http://localhost:8000/docs

## Project Structure

```
CarbonFootprint-Tracker/
├── backend/
│   ├── __init__.py
│   ├── main.py                    # FastAPI application
│   ├── config.py                  # Configuration settings
│   ├── database.py                # Database models
│   ├── classifier.py              # NLP transaction classifier
│   ├── carbon_estimator.py        # Carbon emission calculator
│   ├── suggestion_generator.py    # AI suggestion engine
│   └── transaction_parser.py      # CSV/receipt parser
├── frontend/
│   ├── __init__.py
│   └── app.py                     # Streamlit application
├── requirements.txt               # Python dependencies
├── .env.example                   # Environment variables template
├── .gitignore                     # Git ignore rules
├── sample_data.csv                # Sample transaction data
├── setup.sh                       # Setup script
├── run_backend.sh                 # Run backend server
├── run_frontend.sh                # Run frontend app
├── run_both.sh                    # Run both together
└── README.md                      # This file
```

## How It Works

### 1. Transaction Classification

The app uses keyword-based pattern matching to classify transactions into categories:

- Food (meat-based)
- Food (plant-based)
- Transportation (air, car, public)
- Energy
- Retail (clothing, electronics, general)
- Services
- Dining

### 2. Carbon Estimation

For each transaction, the app calculates CO₂ emissions using:

1. **Climatiq API** (if API key provided): Real-time emission factors from verified sources
2. **Local Estimates** (fallback): Research-based emission factors per dollar spent

Average emission factors (kg CO₂ per USD):
- Air travel: 2.5
- Meat products: 0.8
- Car fuel: 1.2
- Energy: 0.9
- Electronics: 0.7
- Clothing: 0.6
- Plant-based food: 0.2

### 3. AI Suggestions

The suggestion engine provides recommendations through:

1. **OpenAI API** (if API key provided): Personalized, context-aware suggestions
2. **Rule-Based System** (fallback): Category-specific recommendations based on your highest-impact purchases

### 4. Data Storage

Transactions are stored in SQLite (default) or PostgreSQL/Supabase for persistence across sessions.

## Configuration

### Environment Variables

Create a `.env` file based on `.env.example`:

```bash
# Supabase (optional - for PostgreSQL database)
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key

# OpenAI (optional - for AI suggestions)
OPENAI_API_KEY=your_openai_api_key

# Climatiq (optional - for accurate carbon data)
CLIMATIQ_API_KEY=your_climatiq_api_key

# Database (optional - defaults to SQLite)
DATABASE_URL=sqlite:///./carbon_tracker.db

# Application
APP_ENV=development
SECRET_KEY=your_secret_key
```

### API Keys

#### OpenAI API
- Get your key at: https://platform.openai.com/api-keys
- Used for: AI-generated carbon reduction suggestions
- Fallback: Rule-based suggestions work without this

#### Climatiq API
- Get your key at: https://www.climatiq.io/
- Used for: Accurate carbon emission data
- Fallback: Local emission factors work without this

## Development

### Running Tests

```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run all tests
pytest

# Run tests with coverage
pytest --cov=backend --cov-report=html

# Run specific test file
pytest tests/test_classifier.py

# Run tests in verbose mode
pytest -v

# Run only unit tests
pytest -m unit
```

### Code Quality

```bash
# Format code
black backend/ frontend/

# Sort imports
isort backend/ frontend/

# Lint code
flake8 backend/ frontend/

# Type checking
mypy backend/

# Run all quality checks
black backend/ frontend/ && isort backend/ frontend/ && flake8 backend/ frontend/
```

### Adding New Features

1. Backend changes: Edit files in `backend/`
2. Frontend changes: Edit `frontend/app.py`
3. Database changes: Update `backend/database.py`
4. New dependencies: Add to `requirements.txt`

## Deployment

### Docker (Coming Soon)

```bash
docker-compose up
```

### Cloud Deployment

The app can be deployed to:
- **Streamlit Cloud** (frontend)
- **Railway/Render/Heroku** (backend)
- **Vercel** (backend with serverless)

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## Roadmap

- [ ] Receipt OCR with Tesseract/AWS Textract
- [ ] Bank API integrations (Plaid, Stripe)
- [ ] Mobile app (React Native)
- [ ] Social features (compare with friends)
- [ ] Gamification (achievements, streaks)
- [ ] Export reports (PDF, CSV)
- [ ] Multi-currency support
- [ ] Carbon offset marketplace integration
- [ ] Advanced ML models (DistilBERT, custom NLP)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Carbon emission data based on research from EPA, IPCC, and academic sources
- Climatiq API for verified emission factors
- OpenAI for AI-powered suggestions
- Streamlit for the amazing visualization framework
- FastAPI for the high-performance backend

## Support

- **Documentation**: See this README and API docs at `/docs`
- **Issues**: Report bugs or request features via GitHub Issues
- **Discussions**: Join our community discussions

## Authors

- Your Name - Initial work

## Why This Matters

The average American generates about **16 tons of CO₂ per year**. Small changes in our purchasing habits can make a significant difference:

- 🥩 Reducing meat consumption by 50% → ~500 kg CO₂/year
- ✈️ One less flight → ~1,000-2,000 kg CO₂
- 🚗 Carpooling 2 days/week → ~700 kg CO₂/year
- ⚡ Switching to renewable energy → ~7,000 kg CO₂/year

**Every purchase is a vote for the kind of world you want to live in.**

Start tracking your carbon footprint today and make a difference! 🌱

---

Made with 💚 for a sustainable future
