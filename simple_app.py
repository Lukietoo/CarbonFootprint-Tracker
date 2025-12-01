"""
Simplified Carbon Footprint Tracker
A single-file Streamlit app for tracking carbon emissions from purchases.
No external APIs or database required.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
from typing import Dict, List, Tuple

# ===========================
# Data Storage (In-Memory)
# ===========================

if 'transactions' not in st.session_state:
    st.session_state.transactions = []


# ===========================
# Transaction Classifier
# ===========================

class SimpleClassifier:
    """Simple keyword-based transaction classifier."""

    CATEGORIES = {
        "food_meat": {
            "keywords": ["beef", "steak", "burger", "meat", "chicken", "pork", "butcher"],
            "carbon_per_dollar": 0.8,
        },
        "food_plant": {
            "keywords": ["vegetable", "fruit", "salad", "vegan", "organic", "whole foods"],
            "carbon_per_dollar": 0.2,
        },
        "transportation_air": {
            "keywords": ["airline", "flight", "airport", "airways", "jetblue", "united", "delta"],
            "carbon_per_dollar": 2.5,
        },
        "transportation_car": {
            "keywords": ["gas", "fuel", "shell", "chevron", "exxon", "petrol"],
            "carbon_per_dollar": 1.2,
        },
        "energy": {
            "keywords": ["electric", "electricity", "power", "utility", "energy"],
            "carbon_per_dollar": 0.9,
        },
        "retail": {
            "keywords": ["amazon", "walmart", "target", "clothing", "electronics"],
            "carbon_per_dollar": 0.5,
        },
        "dining": {
            "keywords": ["restaurant", "cafe", "coffee", "starbucks", "pizza"],
            "carbon_per_dollar": 0.5,
        },
        "other": {
            "keywords": [],
            "carbon_per_dollar": 0.3,
        }
    }

    def classify(self, description: str, amount: float) -> Tuple[str, float]:
        """
        Classify transaction and estimate carbon.

        Returns:
            (category, carbon_kg)
        """
        description_lower = description.lower()

        # Find matching category
        for category, data in self.CATEGORIES.items():
            if category == "other":
                continue
            for keyword in data["keywords"]:
                if keyword in description_lower:
                    carbon_kg = amount * data["carbon_per_dollar"]
                    return category, carbon_kg

        # Default to "other"
        carbon_kg = amount * self.CATEGORIES["other"]["carbon_per_dollar"]
        return "other", carbon_kg


# ===========================
# Suggestion Generator
# ===========================

def generate_suggestions(transactions: List[Dict]) -> List[str]:
    """Generate simple carbon reduction suggestions."""
    if not transactions:
        return ["Start tracking your purchases to get personalized suggestions!"]

    # Calculate category totals
    category_totals = {}
    for t in transactions:
        cat = t['category']
        category_totals[cat] = category_totals.get(cat, 0) + t['carbon_kg']

    # Get top categories
    top_categories = sorted(category_totals.items(), key=lambda x: x[1], reverse=True)[:3]

    # Category-specific suggestions
    suggestions_map = {
        "food_meat": "🥗 Reduce meat consumption by 50% to save ~{:.1f} kg CO₂",
        "transportation_air": "✈️ Consider train or bus for shorter trips to save ~{:.1f} kg CO₂",
        "transportation_car": "🚗 Use public transit or carpool to save ~{:.1f} kg CO₂",
        "energy": "⚡ Switch to renewable energy to save ~{:.1f} kg CO₂",
        "retail": "♻️ Buy second-hand or sustainable products to save ~{:.1f} kg CO₂",
        "dining": "🏠 Cook at home more often to save ~{:.1f} kg CO₂",
    }

    suggestions = []
    for category, carbon in top_categories:
        if category in suggestions_map:
            reduction = carbon * 0.5  # Assume 50% reduction potential
            suggestions.append(suggestions_map[category].format(reduction))

    if not suggestions:
        suggestions.append("Keep tracking to get personalized suggestions!")

    return suggestions


# ===========================
# Streamlit UI
# ===========================

st.set_page_config(
    page_title="Carbon Footprint Tracker",
    page_icon="🌍",
    layout="wide"
)

# Simple CSS
st.markdown("""
    <style>
    .main {
        background-color: #f0f8f0;
    }
    .stMetric {
        background-color: white;
        padding: 10px;
        border-radius: 5px;
    }
    /* Fix metric text visibility */
    [data-testid="stMetricValue"] {
        color: #1B5E20 !important;
    }
    [data-testid="stMetricLabel"] {
        color: #333333 !important;
    }
    [data-testid="stMetricDelta"] {
        color: #666666 !important;
    }
    </style>
""", unsafe_allow_html=True)

# Title
st.title("🌍 Carbon Footprint Tracker")
st.markdown("*Track your environmental impact from purchases*")

# Sidebar
with st.sidebar:
    st.header("📊 Menu")
    page = st.radio("Navigate", ["Dashboard", "Add Transaction", "Upload CSV", "Suggestions"])

    st.divider()

    # Sample data button
    if st.button("🎲 Load Sample Data"):
        sample_data = [
            {"date": "2024-11-01", "description": "Whole Foods Market", "amount": 87.50},
            {"date": "2024-11-02", "description": "Shell Gas Station", "amount": 45.00},
            {"date": "2024-11-03", "description": "United Airlines", "amount": 350.00},
            {"date": "2024-11-05", "description": "Starbucks Coffee", "amount": 5.50},
            {"date": "2024-11-07", "description": "Amazon - Electronics", "amount": 120.00},
            {"date": "2024-11-10", "description": "Electric Utility Bill", "amount": 85.00},
            {"date": "2024-11-12", "description": "Local Restaurant", "amount": 42.00},
            {"date": "2024-11-15", "description": "Chevron Gas", "amount": 50.00},
        ]

        classifier = SimpleClassifier()
        st.session_state.transactions = []

        for item in sample_data:
            category, carbon = classifier.classify(item["description"], item["amount"])
            st.session_state.transactions.append({
                "date": item["date"],
                "description": item["description"],
                "amount": item["amount"],
                "category": category,
                "carbon_kg": carbon
            })

        st.success("Sample data loaded!")
        st.rerun()

    # Clear data button
    if st.button("🗑️ Clear All Data"):
        st.session_state.transactions = []
        st.success("Data cleared!")
        st.rerun()


# ===========================
# Pages
# ===========================

if page == "Dashboard":
    st.header("📊 Dashboard")

    if not st.session_state.transactions:
        st.info("👋 Add transactions or load sample data to get started!")
    else:
        # Calculate metrics
        df = pd.DataFrame(st.session_state.transactions)
        total_carbon = df['carbon_kg'].sum()
        total_amount = df['amount'].sum()
        transaction_count = len(df)

        # Display metrics
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Emissions", f"{total_carbon:.1f} kg CO₂")
        col2.metric("Total Spent", f"${total_amount:.2f}")
        col3.metric("Transactions", transaction_count)

        st.divider()

        # Charts
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Emissions by Category")
            category_totals = df.groupby('category')['carbon_kg'].sum().reset_index()
            category_totals['category'] = category_totals['category'].str.replace('_', ' ').str.title()

            fig = px.pie(
                category_totals,
                values='carbon_kg',
                names='category',
                color_discrete_sequence=px.colors.sequential.Greens_r
            )
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.subheader("Top Categories")
            top_cats = category_totals.sort_values('carbon_kg', ascending=False).head(5)

            fig = px.bar(
                top_cats,
                x='carbon_kg',
                y='category',
                orientation='h',
                color='carbon_kg',
                color_continuous_scale='Reds',
                labels={'carbon_kg': 'CO₂ (kg)'}
            )
            st.plotly_chart(fig, use_container_width=True)

        # Timeline
        st.subheader("Emissions Over Time")
        df['date'] = pd.to_datetime(df['date'])
        daily = df.groupby('date')['carbon_kg'].sum().reset_index()

        fig = px.area(
            daily,
            x='date',
            y='carbon_kg',
            labels={'carbon_kg': 'CO₂ (kg)', 'date': 'Date'},
            color_discrete_sequence=['#4CAF50']
        )
        st.plotly_chart(fig, use_container_width=True)


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

                # Detect column names
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


elif page == "Suggestions":
    st.header("💡 Suggestions")

    suggestions = generate_suggestions(st.session_state.transactions)

    st.markdown("**Personalized recommendations to reduce your carbon footprint:**")

    for i, suggestion in enumerate(suggestions, 1):
        st.info(f"{i}. {suggestion}")

    if st.session_state.transactions:
        st.divider()
        total_carbon = sum(t['carbon_kg'] for t in st.session_state.transactions)
        potential_reduction = total_carbon * 0.3  # Assume 30% reduction potential

        st.success(f"🎯 Potential savings: **{potential_reduction:.1f} kg CO₂** (30% reduction)")

        trees = potential_reduction / 21.77
        st.info(f"🌳 That's like planting **{trees:.1f} trees** for a year!")


# Footer
st.divider()
st.markdown("*Made with 💚 for a sustainable future*")
