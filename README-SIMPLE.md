# 🌍 Simple Carbon Footprint Tracker

A simplified, single-file carbon footprint tracker built with Streamlit. No database, no external APIs, no complexity - just track your carbon emissions from purchases!

## ✨ Features

- **📊 Dashboard**: View your total emissions and category breakdown
- **🎯 Carbon Budget**: Compare your footprint to US average, world average, and Paris Agreement targets
- **➕ Add Transactions**: Manually add individual purchases
- **📤 CSV Upload**: Bulk import transactions from CSV files
- **💡 Enhanced Suggestions**: Get detailed, actionable recommendations with specific alternatives
- **🎲 Multiple Sample Datasets**: Choose from Eco-Conscious, Average American, or High Carbon lifestyle profiles
- **💾 Data Import/Export**: Save your data as JSON and reload it later - no more lost data on refresh!

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements-simple.txt
```

Only 3 dependencies needed:
- streamlit
- pandas
- plotly

### 2. Run the App

```bash
./run_simple.sh
```

Or manually:
```bash
streamlit run simple_app.py
```

### 3. Open in Browser

The app will automatically open at: **http://localhost:8501**

## 📝 How to Use

### Load Sample Data
1. Click "🎲 Load Sample Data" in the sidebar
2. Explore the dashboard and features

### Add Individual Transactions
1. Go to "Add Transaction" page
2. Enter description, amount, and date
3. Click "Add Transaction"

### Upload CSV File
1. Go to "Upload CSV" page
2. Upload a CSV with columns: `description`, `amount`, `date`
3. Click "Process & Add Transactions"

**CSV Example:**
```csv
date,description,amount
2024-11-01,Whole Foods Market,87.50
2024-11-02,Shell Gas Station,45.00
2024-11-03,United Airlines,350.00
```

## 📊 Carbon Estimation

Simple keyword-based classification:

| Category | Examples | CO₂ per $ |
|----------|----------|-----------|
| Food (Meat) | Beef, Steak, Burger | 0.8 kg |
| Food (Plant) | Vegetables, Fruit, Salad | 0.2 kg |
| Air Travel | Airlines, Flights | 2.5 kg |
| Car Fuel | Gas, Shell, Chevron | 1.2 kg |
| Energy | Electricity, Utility | 0.9 kg |
| Retail | Amazon, Walmart | 0.5 kg |
| Dining | Restaurants, Coffee | 0.5 kg |
| Other | Everything else | 0.3 kg |

## 🆕 New Features

### Carbon Budget Comparison
- Compare your emissions to US average (1,333 kg/month)
- World average (417 kg/month)
- Paris Agreement target (167 kg/month)
- Visual bar chart with color-coded comparisons

### Enhanced Suggestions
- Detailed action plans with specific alternatives
- Calculate exact reduction potential for each suggestion
- Difficulty ratings (easy, medium, hard)
- Environmental equivalents (trees planted, miles not driven, etc.)

### Multiple Sample Datasets
Choose from 3 different lifestyle profiles spanning Jan-Nov 2025:
- 🌱 **Eco-Conscious** (27 transactions, ~220 kg CO₂) - Plant-based diet, public transit, second-hand shopping
- 🏙️ **Average American** (38 transactions, ~4,200 kg CO₂) - Mixed diet, car commuting, occasional flights
- 🔥 **High Carbon** (44 transactions, ~28,000 kg CO₂) - Frequent flying, luxury dining, high consumption

### Data Persistence
- Export your data to JSON format
- Import previously exported data
- Never lose your tracking data again!

## 🎯 What's Different from Full Version?

This simplified version:

- ✅ **Single file** (simple_app.py) vs multiple modules
- ✅ **In-memory storage** with export/import vs SQLite/PostgreSQL database
- ✅ **No external APIs** (no Climatiq, no OpenAI)
- ✅ **3 dependencies** vs 15+ packages
- ✅ **737 lines of code** vs 2,200+ lines
- ✅ **Runs instantly** - no setup needed

## 📁 Files

```
simple_app.py              # Single-file Streamlit app
requirements-simple.txt    # Minimal dependencies
run_simple.sh             # Quick run script
README-SIMPLE.md          # This file
```

## 🔧 Technical Details

- **Framework**: Streamlit (single page app)
- **Storage**: Session state (in-memory, resets on reload)
- **Classification**: Keyword matching
- **Carbon Calc**: Fixed emission factors per category
- **Charts**: Plotly Express

## 💡 Tips

- Data is stored in memory - it will be lost when you close the browser
- To persist data, export your dashboard as an image
- Upload the same CSV again to reload your data
- Use "Clear All Data" to start fresh

## 🌱 Why This Matters

The average American generates **16 tons of CO₂ per year**. Small changes matter:

- 🥩 Reduce meat 50% → Save ~500 kg CO₂/year
- ✈️ One less flight → Save ~1,000-2,000 kg CO₂
- 🚗 Carpool 2 days/week → Save ~700 kg CO₂/year

**Start tracking today!** 🌍

---

Made with 💚 for a sustainable future
