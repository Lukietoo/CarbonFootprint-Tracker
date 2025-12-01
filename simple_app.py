"""
Simplified Carbon Footprint Tracker
A single-file Streamlit app for tracking carbon emissions from purchases.
No external APIs or database required.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
from typing import Dict, List, Tuple
import json


# ===========================
# CONSTANTS
# ===========================

# Monthly carbon benchmarks (kg CO₂ per month)
CARBON_BENCHMARKS = {
    "us_avg": 1333,      # 16 tons/year ÷ 12 months
    "world_avg": 417,    # 5 tons/year ÷ 12 months
    "paris_target": 167  # 2 tons/year ÷ 12 months (Paris Agreement)
}

# Chart colors
CHART_COLORS = {
    "your_footprint": "#4CAF50",
    "us_avg": "#FF9800",
    "world_avg": "#2196F3",
    "paris_target": "#9C27B0",
    "green_sequential": px.colors.sequential.Greens_r,
    "red_scale": "Reds"
}

# Environmental equivalents (for reduction impact)
ENVIRONMENTAL_FACTORS = {
    "tree_co2_per_year": 21.77,    # kg CO₂ absorbed per tree per year
    "car_co2_per_mile": 0.404,     # kg CO₂ per mile driven
    "phone_charge_per_year": 8.3   # kg CO₂ to charge phone for 1 year
}


# ===========================
# Data Storage (In-Memory)
# ===========================

if 'transactions' not in st.session_state:
    st.session_state.transactions = []


# ===========================
# Transaction Classifier
# ===========================

class SimpleClassifier:
    """Simple keyword-based transaction classifier with carbon estimation."""

    CATEGORIES = {
        "food_meat": {
            "keywords": ["beef", "steak", "burger", "meat", "chicken", "pork", "butcher"],
            "carbon_per_dollar": 0.8,
            "alternative": "plant-based meals",
            "reduction_percent": 75
        },
        "food_plant": {
            "keywords": ["vegetable", "fruit", "salad", "vegan", "organic", "whole foods"],
            "carbon_per_dollar": 0.2,
            "alternative": "local/seasonal produce",
            "reduction_percent": 20
        },
        "transportation_air": {
            "keywords": ["airline", "flight", "airport", "airways", "jetblue", "united", "delta"],
            "carbon_per_dollar": 2.5,
            "alternative": "train or bus for shorter trips",
            "reduction_percent": 80
        },
        "transportation_car": {
            "keywords": ["gas", "fuel", "shell", "chevron", "exxon", "petrol"],
            "carbon_per_dollar": 1.2,
            "alternative": "public transit, carpool, or electric vehicle",
            "reduction_percent": 60
        },
        "energy": {
            "keywords": ["electric", "electricity", "power", "utility", "energy"],
            "carbon_per_dollar": 0.9,
            "alternative": "renewable energy plan",
            "reduction_percent": 70
        },
        "retail": {
            "keywords": ["amazon", "walmart", "target", "clothing", "electronics"],
            "carbon_per_dollar": 0.5,
            "alternative": "second-hand or sustainable brands",
            "reduction_percent": 50
        },
        "dining": {
            "keywords": ["restaurant", "cafe", "coffee", "starbucks", "pizza"],
            "carbon_per_dollar": 0.5,
            "alternative": "home cooking with local ingredients",
            "reduction_percent": 40
        },
        "other": {
            "keywords": [],
            "carbon_per_dollar": 0.3,
            "alternative": "sustainable alternatives",
            "reduction_percent": 30
        }
    }

    def classify(self, description: str, amount: float) -> Tuple[str, float]:
        """
        Classify transaction and estimate carbon emissions.

        Args:
            description: Transaction description text
            amount: Purchase amount in USD

        Returns:
            Tuple of (category_name, carbon_kg rounded to 2 decimals)
        """
        description_lower = description.lower()

        # Find matching category by keyword
        for category, data in self.CATEGORIES.items():
            if category == "other":
                continue
            for keyword in data["keywords"]:
                if keyword in description_lower:
                    carbon_kg = round(amount * data["carbon_per_dollar"], 2)
                    return category, carbon_kg

        # Default to "other" category
        carbon_kg = round(amount * self.CATEGORIES["other"]["carbon_per_dollar"], 2)
        return "other", carbon_kg


# ===========================
# Sample Data Generator
# ===========================

def get_sample_datasets() -> Dict[str, List[Dict]]:
    """
    Generate sample datasets with different carbon profiles spanning 11 months.

    Returns:
        Dictionary mapping profile names to lists of transaction dictionaries
    """
    return {
        "🌱 Eco-Conscious (Low Carbon)": [
            # January 2025
            {"date": "2025-01-05", "description": "Whole Foods - Organic Vegetables", "amount": 45.00},
            {"date": "2025-01-12", "description": "Local Farmers Market", "amount": 32.00},
            {"date": "2025-01-18", "description": "Vegan Restaurant", "amount": 28.00},
            {"date": "2025-01-25", "description": "Second-hand Bookstore", "amount": 15.00},
            # February 2025
            {"date": "2025-02-03", "description": "Public Transit Pass", "amount": 85.00},
            {"date": "2025-02-14", "description": "Local Coffee Shop", "amount": 12.00},
            {"date": "2025-02-20", "description": "Community Garden Supplies", "amount": 25.00},
            # March 2025
            {"date": "2025-03-08", "description": "Bike Shop - Repair", "amount": 40.00},
            {"date": "2025-03-15", "description": "Farmers Market - Organic Produce", "amount": 38.00},
            {"date": "2025-03-22", "description": "Vegan Cafe", "amount": 22.00},
            # April 2025
            {"date": "2025-04-05", "description": "Second-hand Clothing Store", "amount": 35.00},
            {"date": "2025-04-18", "description": "Local Organic Grocery", "amount": 42.00},
            {"date": "2025-04-25", "description": "Plant Nursery", "amount": 28.00},
            # May 2025
            {"date": "2025-05-10", "description": "Bike Sharing Monthly Pass", "amount": 30.00},
            {"date": "2025-05-20", "description": "Farmers Market", "amount": 35.00},
            # June 2025
            {"date": "2025-06-08", "description": "Local Vegan Restaurant", "amount": 32.00},
            {"date": "2025-06-22", "description": "Community Supported Agriculture", "amount": 50.00},
            # July 2025
            {"date": "2025-07-12", "description": "Organic Market", "amount": 45.00},
            {"date": "2025-07-28", "description": "Second-hand Furniture", "amount": 80.00},
            # August 2025
            {"date": "2025-08-05", "description": "Local Farm Stand", "amount": 30.00},
            {"date": "2025-08-19", "description": "Eco-friendly Cleaning Supplies", "amount": 25.00},
            # September 2025
            {"date": "2025-09-10", "description": "Farmers Market", "amount": 40.00},
            {"date": "2025-09-25", "description": "Vegetarian Restaurant", "amount": 28.00},
            # October 2025
            {"date": "2025-10-08", "description": "Local Produce Market", "amount": 38.00},
            {"date": "2025-10-22", "description": "Second-hand Books", "amount": 18.00},
            # November 2025
            {"date": "2025-11-12", "description": "Organic Vegetables", "amount": 42.00},
            {"date": "2025-11-25", "description": "Vegan Thanksgiving Meal", "amount": 55.00},
        ],
        "🏙️ Average American": [
            # January 2025
            {"date": "2025-01-03", "description": "Whole Foods Market", "amount": 87.50},
            {"date": "2025-01-08", "description": "Shell Gas Station", "amount": 45.00},
            {"date": "2025-01-15", "description": "Starbucks Coffee", "amount": 5.50},
            {"date": "2025-01-22", "description": "Local Restaurant", "amount": 42.00},
            {"date": "2025-01-28", "description": "Electric Utility Bill", "amount": 85.00},
            # February 2025
            {"date": "2025-02-05", "description": "Chevron Gas", "amount": 50.00},
            {"date": "2025-02-12", "description": "Amazon - Clothing", "amount": 75.00},
            {"date": "2025-02-18", "description": "Target - Groceries", "amount": 95.00},
            {"date": "2025-02-25", "description": "United Airlines", "amount": 350.00},
            # March 2025
            {"date": "2025-03-05", "description": "Shell Gas Station", "amount": 48.00},
            {"date": "2025-03-12", "description": "Restaurant Dinner", "amount": 68.00},
            {"date": "2025-03-20", "description": "Electric Bill", "amount": 82.00},
            {"date": "2025-03-28", "description": "Grocery Store", "amount": 110.00},
            # April 2025
            {"date": "2025-04-03", "description": "Chevron Gas", "amount": 52.00},
            {"date": "2025-04-10", "description": "Amazon - Electronics", "amount": 120.00},
            {"date": "2025-04-18", "description": "Starbucks", "amount": 6.50},
            {"date": "2025-04-25", "description": "Local Steakhouse", "amount": 85.00},
            # May 2025
            {"date": "2025-05-08", "description": "Gas Station", "amount": 55.00},
            {"date": "2025-05-15", "description": "Walmart - Shopping", "amount": 125.00},
            {"date": "2025-05-28", "description": "Electric Utility", "amount": 88.00},
            # June 2025
            {"date": "2025-06-05", "description": "Shell Gas", "amount": 58.00},
            {"date": "2025-06-12", "description": "Restaurant", "amount": 72.00},
            {"date": "2025-06-25", "description": "United Airlines - Vacation", "amount": 420.00},
            # July 2025
            {"date": "2025-07-03", "description": "Gas Station", "amount": 62.00},
            {"date": "2025-07-15", "description": "Amazon - Summer Clothes", "amount": 95.00},
            {"date": "2025-07-28", "description": "Electric Bill", "amount": 105.00},
            # August 2025
            {"date": "2025-08-08", "description": "Chevron Gas", "amount": 60.00},
            {"date": "2025-08-18", "description": "Target Shopping", "amount": 88.00},
            {"date": "2025-08-25", "description": "Restaurant Dinner", "amount": 78.00},
            # September 2025
            {"date": "2025-09-05", "description": "Gas Station", "amount": 50.00},
            {"date": "2025-09-15", "description": "Grocery Store", "amount": 102.00},
            {"date": "2025-09-28", "description": "Electric Utility", "amount": 90.00},
            # October 2025
            {"date": "2025-10-05", "description": "Shell Gas", "amount": 48.00},
            {"date": "2025-10-18", "description": "Amazon - Halloween Decor", "amount": 65.00},
            {"date": "2025-10-28", "description": "Restaurant", "amount": 55.00},
            # November 2025
            {"date": "2025-11-08", "description": "Gas Station", "amount": 52.00},
            {"date": "2025-11-18", "description": "Grocery Store", "amount": 135.00},
            {"date": "2025-11-28", "description": "Thanksgiving Dinner Out", "amount": 95.00},
        ],
        "🔥 High Carbon Lifestyle": [
            # January 2025
            {"date": "2025-01-05", "description": "Premium Steakhouse", "amount": 150.00},
            {"date": "2025-01-10", "description": "Delta Airlines - International Flight", "amount": 1200.00},
            {"date": "2025-01-18", "description": "Luxury Car - Gas Fill-up", "amount": 95.00},
            {"date": "2025-01-25", "description": "High-end Fashion Store", "amount": 450.00},
            # February 2025
            {"date": "2025-02-08", "description": "Butcher Shop - Prime Beef", "amount": 180.00},
            {"date": "2025-02-14", "description": "Fine Dining - Valentine's Day", "amount": 280.00},
            {"date": "2025-02-20", "description": "Shell Gas Station", "amount": 85.00},
            {"date": "2025-02-28", "description": "United Airlines - Ski Trip", "amount": 650.00},
            # March 2025
            {"date": "2025-03-05", "description": "Luxury Steakhouse", "amount": 220.00},
            {"date": "2025-03-12", "description": "Amazon - Designer Clothing", "amount": 380.00},
            {"date": "2025-03-20", "description": "Gas Station - Premium", "amount": 92.00},
            {"date": "2025-03-28", "description": "Gourmet Butcher", "amount": 165.00},
            # April 2025
            {"date": "2025-04-08", "description": "Delta Airlines - Spring Break", "amount": 980.00},
            {"date": "2025-04-15", "description": "High-end Restaurant", "amount": 195.00},
            {"date": "2025-04-22", "description": "Luxury Fashion Boutique", "amount": 520.00},
            {"date": "2025-04-28", "description": "Premium Gas Station", "amount": 88.00},
            # May 2025
            {"date": "2025-05-05", "description": "Fine Dining", "amount": 175.00},
            {"date": "2025-05-12", "description": "United Airlines - Europe Trip", "amount": 1450.00},
            {"date": "2025-05-20", "description": "Steakhouse Dinner", "amount": 210.00},
            {"date": "2025-05-28", "description": "Designer Store", "amount": 425.00},
            # June 2025
            {"date": "2025-06-08", "description": "Gas Fill-up", "amount": 90.00},
            {"date": "2025-06-15", "description": "Premium Butcher Shop", "amount": 195.00},
            {"date": "2025-06-22", "description": "Luxury Restaurant", "amount": 245.00},
            {"date": "2025-06-28", "description": "Amazon - Fast Fashion Haul", "amount": 350.00},
            # July 2025
            {"date": "2025-07-05", "description": "Delta Airlines - Summer Vacation", "amount": 1350.00},
            {"date": "2025-07-15", "description": "High-end Steakhouse", "amount": 265.00},
            {"date": "2025-07-22", "description": "Luxury Shopping", "amount": 580.00},
            {"date": "2025-07-28", "description": "Gas Station", "amount": 95.00},
            # August 2025
            {"date": "2025-08-08", "description": "Fine Dining", "amount": 225.00},
            {"date": "2025-08-15", "description": "United Airlines - Coast Trip", "amount": 720.00},
            {"date": "2025-08-22", "description": "Premium Meat Market", "amount": 175.00},
            {"date": "2025-08-28", "description": "Designer Boutique", "amount": 495.00},
            # September 2025
            {"date": "2025-09-05", "description": "Gas Station", "amount": 88.00},
            {"date": "2025-09-12", "description": "Luxury Steakhouse", "amount": 240.00},
            {"date": "2025-09-20", "description": "Amazon - Electronics", "amount": 420.00},
            {"date": "2025-09-28", "description": "Gourmet Restaurant", "amount": 195.00},
            # October 2025
            {"date": "2025-10-08", "description": "Delta Airlines - Fall Getaway", "amount": 890.00},
            {"date": "2025-10-15", "description": "High-end Fashion", "amount": 465.00},
            {"date": "2025-10-22", "description": "Premium Steakhouse", "amount": 215.00},
            {"date": "2025-10-28", "description": "Gas Fill-up", "amount": 92.00},
            # November 2025
            {"date": "2025-11-08", "description": "Fine Dining", "amount": 230.00},
            {"date": "2025-11-15", "description": "United Airlines - Holiday Trip", "amount": 1100.00},
            {"date": "2025-11-22", "description": "Luxury Thanksgiving Dinner", "amount": 325.00},
            {"date": "2025-11-28", "description": "Black Friday - Designer Shopping", "amount": 850.00},
        ]
    }


# ===========================
# Enhanced Suggestion Generator
# ===========================

def generate_enhanced_suggestions(transactions: List[Dict]) -> List[Dict]:
    """
    Generate detailed carbon reduction suggestions based on transaction patterns.

    Args:
        transactions: List of transaction dictionaries

    Returns:
        List of suggestion dictionaries with reduction strategies
    """
    if not transactions:
        return [{
            "icon": "💡",
            "title": "Start Tracking",
            "description": "Add your purchases to get personalized suggestions!",
            "alternative": "sustainable choices",
            "reduction_kg": 0,
            "difficulty": "easy",
            "category": "general"
        }]

    # Calculate category totals
    category_totals = {}
    for t in transactions:
        cat = t['category']
        category_totals[cat] = category_totals.get(cat, 0) + t['carbon_kg']

    # Get top 3 highest-emission categories
    top_categories = sorted(category_totals.items(), key=lambda x: x[1], reverse=True)[:3]

    classifier = SimpleClassifier()
    suggestions = []

    # Category-specific suggestion templates
    suggestion_templates = {
        "food_meat": {
            "icon": "🥗",
            "title": "Switch to Plant-Based Meals",
            "description": "Replace 50% of meat meals with plant-based alternatives like beans, lentils, or tofu",
            "difficulty": "medium"
        },
        "transportation_air": {
            "icon": "🚂",
            "title": "Choose Ground Transportation",
            "description": "For trips under 500 miles, take the train or bus instead of flying",
            "difficulty": "easy"
        },
        "transportation_car": {
            "icon": "🚌",
            "title": "Use Public Transit or Carpool",
            "description": "Replace 3 car trips per week with public transit, biking, or carpooling",
            "difficulty": "medium"
        },
        "energy": {
            "icon": "⚡",
            "title": "Switch to Renewable Energy",
            "description": "Sign up for a renewable energy plan or install solar panels",
            "difficulty": "hard"
        },
        "retail": {
            "icon": "♻️",
            "title": "Buy Second-Hand First",
            "description": "Check thrift stores, consignment shops, or online marketplaces before buying new",
            "difficulty": "easy"
        },
        "dining": {
            "icon": "🏠",
            "title": "Cook More Meals at Home",
            "description": "Prepare 3 more home-cooked meals per week using local ingredients",
            "difficulty": "medium"
        }
    }

    # Generate suggestions for top categories
    for category, carbon in top_categories:
        if category in suggestion_templates:
            template = suggestion_templates[category]
            cat_data = classifier.CATEGORIES[category]

            # Calculate potential reduction (rounded to 2 decimal places)
            reduction = round(carbon * (cat_data["reduction_percent"] / 100), 2)

            suggestions.append({
                "icon": template["icon"],
                "title": template["title"],
                "description": template["description"],
                "alternative": cat_data["alternative"],
                "reduction_kg": reduction,
                "difficulty": template["difficulty"],
                "category": category
            })

    return suggestions if suggestions else [{
        "icon": "💡",
        "title": "Keep Tracking",
        "description": "Continue monitoring your purchases to find more opportunities!",
        "alternative": "sustainable choices",
        "reduction_kg": 0,
        "difficulty": "easy",
        "category": "general"
    }]


# ===========================
# Data Import/Export Functions
# ===========================

def export_data_to_json() -> str:
    """
    Export transactions to JSON format.

    Returns:
        JSON string of exported data, or None if no transactions
    """
    if not st.session_state.transactions:
        return None

    data = {
        "export_date": datetime.now().isoformat(),
        "transactions": st.session_state.transactions
    }
    return json.dumps(data, indent=2)


def import_data_from_json(json_str: str) -> Tuple[bool, any]:
    """
    Import transactions from JSON format.

    Args:
        json_str: JSON string containing transaction data

    Returns:
        Tuple of (success: bool, result: int or error_message: str)
    """
    try:
        data = json.loads(json_str)
        if "transactions" in data:
            st.session_state.transactions = data["transactions"]
            return True, len(data["transactions"])
        return False, "Invalid format: missing 'transactions' key"
    except json.JSONDecodeError as e:
        return False, f"Invalid JSON: {str(e)}"


# ===========================
# Helper Functions
# ===========================

def calculate_dashboard_metrics(df: pd.DataFrame) -> Dict[str, float]:
    """
    Calculate key metrics from transaction dataframe.

    Args:
        df: DataFrame with transaction data

    Returns:
        Dictionary containing calculated metrics
    """
    return {
        "total_carbon": df['carbon_kg'].sum(),
        "total_amount": df['amount'].sum(),
        "transaction_count": len(df),
        "avg_per_transaction": df['carbon_kg'].sum() / len(df) if len(df) > 0 else 0
    }


def create_horizontal_bar_chart(data: pd.DataFrame, x_col: str, y_col: str,
                                 color_col: str = None, title: str = None) -> go.Figure:
    """
    Create a horizontal bar chart with consistent styling.

    Args:
        data: DataFrame containing chart data
        x_col: Column name for x-axis values
        y_col: Column name for y-axis categories
        color_col: Optional column name for bar colors
        title: Optional chart title

    Returns:
        Plotly Figure object
    """
    fig = go.Figure()

    for idx, row in data.iterrows():
        color = row[color_col] if color_col and color_col in data.columns else CHART_COLORS["your_footprint"]
        fig.add_trace(go.Bar(
            x=[row[x_col]],
            y=[row[y_col]],
            orientation='h',
            name=row[y_col],
            marker_color=color,
            text=[f"{row[x_col]} kg"],
            textposition='auto',
        ))

    fig.update_layout(
        showlegend=False,
        xaxis_title="Monthly Emissions (kg CO₂)",
        title=title,
        height=300,
        margin=dict(l=0, r=0, t=30 if title else 0, b=0)
    )
    return fig


def load_sample_dataset(dataset_name: str, datasets: Dict[str, List[Dict]]) -> None:
    """
    Load a sample dataset into session state.

    Args:
        dataset_name: Name of the dataset to load
        datasets: Dictionary of available datasets
    """
    classifier = SimpleClassifier()
    st.session_state.transactions = []

    for item in datasets[dataset_name]:
        category, carbon = classifier.classify(item["description"], item["amount"])
        st.session_state.transactions.append({
            "date": item["date"],
            "description": item["description"],
            "amount": item["amount"],
            "category": category,
            "carbon_kg": carbon
        })


def render_comparison_metrics(monthly_carbon: float) -> None:
    """
    Render comparison metrics against benchmarks.

    Args:
        monthly_carbon: User's monthly carbon emissions in kg
    """
    us_percent = (monthly_carbon / CARBON_BENCHMARKS["us_avg"]) * 100
    world_percent = (monthly_carbon / CARBON_BENCHMARKS["world_avg"]) * 100
    paris_percent = (monthly_carbon / CARBON_BENCHMARKS["paris_target"]) * 100

    status_us = "🟢 Below" if monthly_carbon < CARBON_BENCHMARKS["us_avg"] else "🔴 Above"
    st.metric("vs US Avg", status_us, f"{us_percent:.0f}%")

    status_world = "🟢 Below" if monthly_carbon < CARBON_BENCHMARKS["world_avg"] else "🔴 Above"
    st.metric("vs World Avg", status_world, f"{world_percent:.0f}%")

    status_paris = "🟢 Below" if monthly_carbon < CARBON_BENCHMARKS["paris_target"] else "🔴 Above"
    st.metric("vs Paris Target", status_paris, f"{paris_percent:.0f}%")


# ===========================
# Streamlit UI Configuration
# ===========================

st.set_page_config(
    page_title="Carbon Footprint Tracker",
    page_icon="🌍",
    layout="wide"
)

# ===========================
# CSS Styling
# ===========================

st.markdown("""
    <style>
    /* ===== BASE STYLES ===== */
    /* Font settings with emoji support and fallbacks */
    * {
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto,
                     "Helvetica Neue", Arial, sans-serif, "Apple Color Emoji",
                     "Segoe UI Emoji", "Segoe UI Symbol" !important;
    }

    .main {
        background-color: #f0f8f0;
    }

    /* ===== METRIC STYLES ===== */
    .stMetric {
        background-color: white;
        padding: 10px;
        border-radius: 5px;
    }

    /* Ensure metric text is visible and properly formatted */
    [data-testid="stMetricValue"] {
        color: #1B5E20 !important;
        font-variant-numeric: tabular-nums;
        line-height: 1.2;
    }

    [data-testid="stMetricLabel"] {
        color: #333333 !important;
        line-height: 1.4;
    }

    [data-testid="stMetricDelta"] {
        color: #666666 !important;
        line-height: 1.3;
    }

    /* ===== TYPOGRAPHY ===== */
    /* Ensure emojis render properly in headings and buttons */
    h1, h2, h3, h4, .stButton button {
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto,
                     "Helvetica Neue", Arial, sans-serif, "Apple Color Emoji",
                     "Segoe UI Emoji", "Segoe UI Symbol" !important;
    }

    /* Code blocks should always be monospace */
    code, pre, .stCodeBlock {
        font-family: "SF Mono", Monaco, "Cascadia Code", "Roboto Mono",
                     Consolas, "Courier New", monospace !important;
    }

    /* Fix text in form elements */
    .stButton button, .stTextInput input, .stNumberInput input, .stSelectbox select {
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto,
                     "Helvetica Neue", Arial, sans-serif !important;
        line-height: 1.5;
    }

    /* ===== SUGGESTION CARDS ===== */
    .suggestion-card {
        background: linear-gradient(135deg, #E8F5E9 0%, #C8E6C9 100%);
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        border-left: 5px solid #4CAF50;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }

    .suggestion-card h4 {
        color: #1B5E20;
        margin-bottom: 0.5rem;
        line-height: 1.4;
    }

    .suggestion-card p {
        color: #333;
        margin: 0.3rem 0;
        line-height: 1.6;
    }
    </style>
""", unsafe_allow_html=True)


# ===========================
# Header
# ===========================

st.title("🌍 Carbon Footprint Tracker")
st.markdown("*Track your environmental impact from purchases*")


# ===========================
# Sidebar Navigation & Controls
# ===========================

with st.sidebar:
    st.header("📊 Menu")
    page = st.radio("Navigate", ["Dashboard", "Add Transaction", "Upload CSV", "Suggestions", "Data Manager"])

    st.divider()

    # Sample data loader
    st.subheader("📦 Load Sample Data")
    datasets = get_sample_datasets()
    selected_dataset = st.selectbox("Choose a profile:", list(datasets.keys()))

    if st.button("🎲 Load Selected Dataset", use_container_width=True):
        load_sample_dataset(selected_dataset, datasets)
        st.success(f"Loaded {len(datasets[selected_dataset])} transactions!")
        st.rerun()

    st.divider()

    # Quick stats in sidebar
    if st.session_state.transactions:
        st.markdown("### 💡 Quick Stats")
        metrics = calculate_dashboard_metrics(pd.DataFrame(st.session_state.transactions))
        st.metric("Total Emissions", f"{metrics['total_carbon']:.1f} kg CO₂")
        st.metric("Total Spent", f"${metrics['total_amount']:.2f}")
        st.metric("Transactions", metrics['transaction_count'])


# ===========================
# PAGE: Dashboard
# ===========================

if page == "Dashboard":
    st.header("📊 Dashboard")

    if not st.session_state.transactions:
        st.info("👋 Add transactions or load sample data to get started!")
    else:
        df = pd.DataFrame(st.session_state.transactions)
        metrics = calculate_dashboard_metrics(df)

        # Display main metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Emissions", f"{metrics['total_carbon']:.1f} kg CO₂")
        with col2:
            st.metric("Total Spent", f"${metrics['total_amount']:.2f}")
        with col3:
            st.metric("Transactions", metrics['transaction_count'])
        with col4:
            st.metric("Avg per Purchase", f"{metrics['avg_per_transaction']:.1f} kg CO₂")

        st.divider()

        # Carbon Budget Comparison Section
        st.subheader("🎯 Carbon Budget Comparison")

        col1, col2 = st.columns([2, 1])

        with col1:
            # Create comparison bar chart
            comparison_data = pd.DataFrame({
                'Category': ['Your Footprint', 'US Average', 'World Average', 'Paris Target'],
                'Emissions (kg CO₂)': [
                    metrics['total_carbon'],
                    CARBON_BENCHMARKS["us_avg"],
                    CARBON_BENCHMARKS["world_avg"],
                    CARBON_BENCHMARKS["paris_target"]
                ],
                'Color': [
                    CHART_COLORS["your_footprint"],
                    CHART_COLORS["us_avg"],
                    CHART_COLORS["world_avg"],
                    CHART_COLORS["paris_target"]
                ]
            })

            fig = create_horizontal_bar_chart(
                comparison_data,
                'Emissions (kg CO₂)',
                'Category',
                'Color'
            )
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            render_comparison_metrics(metrics['total_carbon'])

        # Paris Target explanation
        with st.expander("ℹ️ What is the Paris Target?"):
            st.markdown("""
            **The Paris Agreement** is a 2015 international treaty where 196 countries committed to limiting
            global warming to well below 2°C (preferably 1.5°C) above pre-industrial levels.

            **The Paris Target in our app: 2 tons CO₂/year per person**
            - **Monthly**: 167 kg CO₂/month
            - **Why this number?**: Scientists estimate we need to reduce global per-capita emissions to
              ~2 tons/year by 2050 to avoid catastrophic climate change

            **Context:**
            - 🔴 Current US average: ~16 tons/year **(8x over target!)**
            - 🟡 World average: ~5 tons/year **(2.5x over target)**
            - 🟢 Paris target: ~2 tons/year **(sustainable)**

            Meeting this target requires significant lifestyle changes, but every reduction helps! 🌱
            """)

        st.divider()

        # Emissions by Category Charts
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("📈 Emissions by Category")
            category_totals = df.groupby('category')['carbon_kg'].sum().reset_index()
            category_totals['category'] = category_totals['category'].str.replace('_', ' ').str.title()

            fig = px.pie(
                category_totals,
                values='carbon_kg',
                names='category',
                color_discrete_sequence=CHART_COLORS["green_sequential"]
            )
            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.subheader("🎯 Top Categories")
            top_cats = category_totals.sort_values('carbon_kg', ascending=False).head(5)

            fig = px.bar(
                top_cats,
                x='carbon_kg',
                y='category',
                orientation='h',
                color='carbon_kg',
                color_continuous_scale=CHART_COLORS["red_scale"],
                labels={'carbon_kg': 'CO₂ (kg)'}
            )
            fig.update_layout(showlegend=False)
            st.plotly_chart(fig, use_container_width=True)

        # Timeline Chart
        st.subheader("📅 Emissions Over Time")
        df['date'] = pd.to_datetime(df['date'])
        daily = df.groupby('date')['carbon_kg'].sum().reset_index()

        fig = px.area(
            daily,
            x='date',
            y='carbon_kg',
            labels={'carbon_kg': 'CO₂ (kg)', 'date': 'Date'},
            color_discrete_sequence=[CHART_COLORS["your_footprint"]]
        )
        fig.update_layout(hovermode='x unified')
        st.plotly_chart(fig, use_container_width=True)


# ===========================
# PAGE: Add Transaction
# ===========================

elif page == "Add Transaction":
    st.header("➕ Add Transaction")

    with st.form("add_transaction"):
        col1, col2 = st.columns(2)

        with col1:
            description = st.text_input("Description", placeholder="e.g., Coffee Shop")
            amount = st.number_input("Amount ($)", min_value=0.01, value=10.0, step=0.01)

        with col2:
            date = st.date_input("Date", value=datetime.now())

        submitted = st.form_submit_button("Add Transaction", type="primary")

        if submitted and description and amount > 0:
            classifier = SimpleClassifier()
            category, carbon = classifier.classify(description, amount)

            st.session_state.transactions.append({
                "date": date.strftime("%Y-%m-%d"),
                "description": description,
                "amount": amount,
                "category": category,
                "carbon_kg": carbon
            })

            st.success(f"✅ Added! Carbon impact: {carbon:.2f} kg CO₂")
            st.rerun()


# ===========================
# PAGE: Upload CSV
# ===========================

elif page == "Upload CSV":
    st.header("📤 Upload CSV")

    st.markdown("""
    Upload a CSV file with columns:
    - **description** (or merchant): Purchase description
    - **amount** (or total): Amount in USD
    - **date** (optional): Transaction date
    """)

    uploaded_file = st.file_uploader("Choose a CSV file", type=['csv'])

    if uploaded_file:
        try:
            df = pd.read_csv(uploaded_file)
            st.dataframe(df.head(), use_container_width=True)

            if st.button("Process & Add Transactions"):
                classifier = SimpleClassifier()

                # Detect column names (case-insensitive)
                desc_col = next((c for c in df.columns if c.lower() in ['description', 'merchant', 'name']), None)
                amt_col = next((c for c in df.columns if c.lower() in ['amount', 'total', 'price']), None)
                date_col = next((c for c in df.columns if c.lower() == 'date'), None)

                if not desc_col or not amt_col:
                    st.error("CSV must have 'description' and 'amount' columns")
                else:
                    count = 0
                    for _, row in df.iterrows():
                        description = str(row[desc_col])
                        amount = float(row[amt_col])
                        date = row[date_col] if date_col else datetime.now().strftime("%Y-%m-%d")

                        category, carbon = classifier.classify(description, amount)

                        st.session_state.transactions.append({
                            "date": str(date),
                            "description": description,
                            "amount": amount,
                            "category": category,
                            "carbon_kg": carbon
                        })
                        count += 1

                    st.success(f"✅ Added {count} transactions!")
                    st.rerun()

        except Exception as e:
            st.error(f"Error: {str(e)}")


# ===========================
# PAGE: Suggestions
# ===========================

elif page == "Suggestions":
    st.header("💡 Carbon Reduction Suggestions")

    suggestions = generate_enhanced_suggestions(st.session_state.transactions)

    st.markdown("**Personalized recommendations to reduce your carbon footprint:**")
    st.markdown("")

    for i, sug in enumerate(suggestions, 1):
        st.markdown(f"""
        <div class="suggestion-card">
            <h4>{sug['icon']} {i}. {sug['title']}</h4>
            <p><strong>Action:</strong> {sug['description']}</p>
            <p><strong>Alternative:</strong> {sug['alternative']}</p>
            <p><strong>Potential Reduction:</strong> {sug['reduction_kg']:.1f} kg CO₂/month</p>
            <p><strong>Difficulty:</strong> {sug['difficulty'].title()}</p>
        </div>
        """, unsafe_allow_html=True)

    if st.session_state.transactions:
        st.divider()

        # Calculate total potential impact
        total_carbon = sum(t['carbon_kg'] for t in st.session_state.transactions)
        total_reduction = sum(s['reduction_kg'] for s in suggestions)

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Current Footprint", f"{total_carbon:.1f} kg CO₂")

        with col2:
            reduction_percent = (total_reduction / total_carbon * 100) if total_carbon > 0 else 0
            st.metric("Potential Reduction", f"{total_reduction:.1f} kg CO₂", f"-{reduction_percent:.0f}%")

        with col3:
            new_footprint = total_carbon - total_reduction
            st.metric("After Changes", f"{new_footprint:.1f} kg CO₂")

        st.divider()

        # Environmental equivalents
        st.subheader("🌳 Environmental Impact")

        col1, col2, col3 = st.columns(3)

        with col1:
            trees = total_reduction / ENVIRONMENTAL_FACTORS["tree_co2_per_year"]
            st.info(f"**🌲 {trees:.1f} trees**  \nPlanted for 1 year")

        with col2:
            miles = total_reduction / ENVIRONMENTAL_FACTORS["car_co2_per_mile"]
            st.info(f"**🚗 {miles:.0f} miles**  \nNot driven")

        with col3:
            smartphones = total_reduction / ENVIRONMENTAL_FACTORS["phone_charge_per_year"]
            st.info(f"**📱 {smartphones:.1f} phones**  \nCharged for 1 year")


# ===========================
# PAGE: Data Manager
# ===========================

elif page == "Data Manager":
    st.header("💾 Data Management")

    st.markdown("Export your data to save it, or import previously exported data.")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📤 Export Data")

        if st.session_state.transactions:
            json_data = export_data_to_json()

            st.download_button(
                label="⬇️ Download as JSON",
                data=json_data,
                file_name=f"carbon_tracker_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json",
                use_container_width=True,
                key="download_json_button"
            )

            st.success(f"✅ Ready to export {len(st.session_state.transactions)} transactions")

            # Show preview
            with st.expander("📋 Preview Export Data", expanded=False):
                st.code(json_data, language="json")
        else:
            st.info("No data to export. Add some transactions first!")

    with col2:
        st.subheader("📥 Import Data")

        uploaded_json = st.file_uploader("Choose a JSON file", type=['json'], key="json_upload")

        if uploaded_json:
            json_str = uploaded_json.read().decode('utf-8')

            if st.button("Import Data", type="primary", use_container_width=True, key="import_data_button"):
                success, result = import_data_from_json(json_str)

                if success:
                    st.success(f"✅ Imported {result} transactions!")
                    st.rerun()
                else:
                    st.error(f"❌ Import failed: {result}")

    st.divider()

    # Clear data section
    st.subheader("🗑️ Clear Data")
    st.warning("⚠️ This will permanently delete all your transactions!")

    if st.button("Clear All Data", type="secondary", key="clear_data_button"):
        st.session_state.transactions = []
        st.success("Data cleared!")
        st.rerun()


# ===========================
# Footer
# ===========================

st.divider()
col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    st.markdown("<p style='text-align: center;'><em>Made with 💚 for a sustainable future</em></p>", unsafe_allow_html=True)
