"""
SIMPLIFIED Carbon Footprint Tracker Frontend
Easy to understand, great for presentations!

This app has 3 main pages:
1. Dashboard - See your total carbon footprint with charts
2. Add Purchase - Simple calculator to add new purchases
3. Suggestions - Tips to reduce your footprint
"""

import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from datetime import datetime

# ============================================
# CONFIGURATION
# ============================================

API_URL = "http://localhost:8000"  # Backend server
USER_ID = "default_user"

# Page setup
st.set_page_config(
    page_title="Carbon Footprint Tracker",
    page_icon="🌱",
    layout="wide"
)


# ============================================
# SIMPLE, CLEAN STYLING
# No complex CSS - just clean colors!
# ============================================

st.markdown("""
    <style>
    /* Clean green theme */
    .stApp {
        background-color: #f0f8f0;
    }

    /* Make headers green */
    h1, h2, h3 {
        color: #2d5a3d;
    }

    /* Nice cards for content */
    .metric-box {
        background: white;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #4CAF50;
        margin: 10px 0px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }

    /* Green sidebar */
    [data-testid="stSidebar"] {
        background-color: #2d5a3d;
    }

    [data-testid="stSidebar"] * {
        color: white !important;
    }
    </style>
""", unsafe_allow_html=True)


# ============================================
# HELPER FUNCTIONS
# Talk to the backend
# ============================================

def call_api(endpoint, method="GET", data=None):
    """
    Simple function to talk to our backend

    Args:
        endpoint: Which URL to call (e.g., "/api/dashboard")
        method: GET or POST
        data: Data to send (for POST)

    Returns:
        Response from server (or None if error)
    """
    url = f"{API_URL}{endpoint}"
    try:
        if method == "GET":
            response = requests.get(url)
        elif method == "POST":
            response = requests.post(url, json=data)
        elif method == "DELETE":
            response = requests.delete(url)

        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Error: {response.status_code}")
            return None
    except Exception as e:
        st.error(f"Can't connect to backend: {e}")
        st.info("Make sure the backend is running!")
        return None


# ============================================
# PAGE 1: DASHBOARD
# Show totals and pretty charts
# ============================================

def show_dashboard():
    """Main dashboard with stats and charts"""

    st.title("🌍 Your Carbon Footprint Dashboard")
    st.write("Track your environmental impact over time")

    # Get data from backend
    stats = call_api(f"/api/dashboard?user_id={USER_ID}")
    transactions = call_api(f"/api/transactions?user_id={USER_ID}")

    if not stats:
        st.warning("⚠️ Backend not running. Start it with: `python3 -m uvicorn backend.main_simple:app`")
        return

    if stats['transaction_count'] == 0:
        st.info("👋 No data yet! Add your first purchase or load sample data from the sidebar.")
        return

    # Top metrics in 3 columns
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Total CO₂ Emissions",
            f"{stats['total_carbon_kg']:.1f} kg",
            help="Total carbon footprint from all your purchases"
        )

    with col2:
        st.metric(
            "This Month",
            f"{stats['monthly_carbon_kg']:.1f} kg",
            help="Carbon emissions in the last 30 days"
        )

    with col3:
        st.metric(
            "Purchases Tracked",
            stats['transaction_count'],
            help="Number of transactions you've logged"
        )

    st.divider()

    # Charts side by side
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📊 Emissions by Category")

        if stats['category_breakdown']:
            # Create pie chart
            categories = list(stats['category_breakdown'].keys())
            values = list(stats['category_breakdown'].values())

            # Make category names prettier
            categories = [c.replace('_', ' ').title() for c in categories]

            fig = px.pie(
                names=categories,
                values=values,
                color_discrete_sequence=px.colors.sequential.Greens
            )
            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("📈 Top Categories")

        if stats['category_breakdown']:
            # Create bar chart
            df = pd.DataFrame({
                'Category': categories,
                'CO₂ (kg)': values
            })
            df = df.sort_values('CO₂ (kg)', ascending=True)

            fig = px.bar(
                df,
                x='CO₂ (kg)',
                y='Category',
                orientation='h',
                color='CO₂ (kg)',
                color_continuous_scale='Greens'
            )
            fig.update_layout(showlegend=False)
            st.plotly_chart(fig, use_container_width=True)

    # Recent transactions table
    st.divider()
    st.subheader("📝 Recent Purchases")

    if transactions:
        df = pd.DataFrame(transactions)
        df['date'] = pd.to_datetime(df['date']).dt.strftime('%Y-%m-%d')
        df['category'] = df['category'].str.replace('_', ' ').str.title()

        # Show only important columns
        display_df = df[['date', 'description', 'amount', 'category', 'carbon_kg']].head(10)
        display_df.columns = ['Date', 'Description', 'Amount ($)', 'Category', 'CO₂ (kg)']

        st.dataframe(display_df, use_container_width=True, hide_index=True)


# ============================================
# PAGE 2: ADD PURCHASE
# Simple calculator form
# ============================================

def show_add_purchase():
    """Simple form to add a new purchase"""

    st.title("🛒 Add New Purchase")
    st.write("Calculate the carbon footprint of a purchase")

    # Simple form
    with st.form("add_purchase"):
        st.subheader("Enter Purchase Details")

        col1, col2 = st.columns(2)

        with col1:
            description = st.text_input(
                "What did you buy?",
                placeholder="e.g., Starbucks coffee"
            )

            amount = st.number_input(
                "How much did it cost? ($)",
                min_value=0.01,
                value=10.00,
                step=0.50
            )

        with col2:
            category = st.selectbox(
                "Category",
                options=[
                    ("food_meat", "🥩 Food - Meat"),
                    ("food_plant", "🥗 Food - Plant-based"),
                    ("transportation", "🚗 Transportation"),
                    ("energy", "⚡ Energy/Utilities"),
                    ("shopping", "🛍️ Shopping"),
                    ("entertainment", "🎬 Entertainment"),
                    ("other", "📦 Other")
                ],
                format_func=lambda x: x[1]
            )

            date = st.date_input(
                "Date of purchase",
                value=datetime.now()
            )

        # Submit button
        submitted = st.form_submit_button("Calculate & Save", type="primary", use_container_width=True)

        if submitted:
            if not description:
                st.error("Please enter what you bought!")
            else:
                # Send to backend
                data = {
                    "description": description,
                    "amount": amount,
                    "category": category[0],  # Get the key (not the display name)
                    "date": date.isoformat(),
                    "user_id": USER_ID
                }

                result = call_api("/api/transactions", method="POST", data=data)

                if result:
                    st.success(f"✅ Added! Carbon footprint: **{result['carbon_kg']} kg CO₂**")
                    st.balloons()

                    # Show comparison
                    st.info(f"💡 That's like driving {result['carbon_kg'] * 3:.1f} miles in a car")


# ============================================
# PAGE 3: SUGGESTIONS
# Simple tips to reduce footprint
# ============================================

def show_suggestions():
    """Show simple suggestions based on user's data"""

    st.title("💡 Personalized Suggestions")
    st.write("Easy ways to reduce your carbon footprint")

    suggestions = call_api(f"/api/suggestions?user_id={USER_ID}")

    if not suggestions:
        st.info("Add some purchases first to get personalized suggestions!")
        return

    st.markdown("Based on your purchases, here are some easy changes you can make:")

    # Show each suggestion in a nice card
    for i, suggestion in enumerate(suggestions, 1):
        # Color code by difficulty
        if suggestion['difficulty'] == 'easy':
            icon = "🟢"
            color = "#E8F5E9"
        elif suggestion['difficulty'] == 'medium':
            icon = "🟡"
            color = "#FFF9C4"
        else:
            icon = "🔴"
            color = "#FFEBEE"

        st.markdown(f"""
        <div style="background: {color}; padding: 20px; border-radius: 10px; margin: 15px 0; border-left: 5px solid #4CAF50;">
            <h3>{i}. {suggestion['suggestion']}</h3>
            <p><strong>Potential Reduction:</strong> {suggestion['reduction_kg']:.1f} kg CO₂</p>
            <p><strong>Difficulty:</strong> {icon} {suggestion['difficulty'].title()}</p>
            <p><strong>Category:</strong> {suggestion['category'].replace('_', ' ').title()}</p>
        </div>
        """, unsafe_allow_html=True)

    # Show total impact
    st.divider()
    total_reduction = sum(s['reduction_kg'] for s in suggestions)
    st.success(f"🎯 If you follow all these tips, you could reduce your footprint by **{total_reduction:.1f} kg CO₂**!")

    # Fun comparison
    trees = total_reduction / 21.77  # Trees absorb ~22kg CO2/year
    st.info(f"🌳 That's like planting **{trees:.1f} trees** for a year!")


# ============================================
# PAGE 4: ABOUT
# Quick explanation of the app
# ============================================

def show_about():
    """Simple about page"""

    st.title("ℹ️ About This App")

    st.markdown("""
    ## What is this?

    This is a **simple Carbon Footprint Tracker** that helps you understand how your purchases impact the environment.

    ### How it works:

    1. **Add purchases** manually (description, amount, category)
    2. **We calculate** the CO₂ emissions using simple formulas
    3. **Track over time** and see your impact with charts
    4. **Get suggestions** to reduce your footprint

    ### Technology:

    - **Frontend**: Streamlit (Python)
    - **Backend**: FastAPI (Python)
    - **Database**: SQLite (file-based)
    - **Charts**: Plotly

    ### CO₂ Estimates:

    We use simple estimates based on spending:
    - **Meat**: 0.8 kg CO₂ per $1
    - **Plant-based food**: 0.2 kg CO₂ per $1
    - **Transportation**: 0.5 kg CO₂ per $1
    - **Energy**: 0.9 kg CO₂ per $1
    - **Shopping**: 0.3 kg CO₂ per $1

    ### Note:

    These are simplified estimates for learning purposes. Real carbon footprints are more complex!

    ---

    Made with 🌱 for the environment
    """)


# ============================================
# MAIN APP
# Sidebar navigation
# ============================================

def main():
    """Main app with sidebar navigation"""

    # Sidebar
    with st.sidebar:
        st.title("🌱 Carbon Tracker")
        st.write("Track your environmental impact")

        st.divider()

        # Navigation
        page = st.radio(
            "Navigate",
            ["Dashboard", "Add Purchase", "Suggestions", "About"],
            label_visibility="collapsed"
        )

        st.divider()

        # Quick actions
        st.subheader("Quick Actions")

        if st.button("📊 Load Sample Data", use_container_width=True):
            result = call_api(f"/api/sample-data?user_id={USER_ID}", method="POST")
            if result:
                st.success("Loaded sample data!")
                st.rerun()

        if st.button("🗑️ Clear All Data", use_container_width=True):
            result = call_api(f"/api/reset-data?user_id={USER_ID}", method="DELETE")
            if result:
                st.success(f"Deleted {result['deleted_count']} items")
                st.rerun()

        st.divider()

        # Stats in sidebar
        stats = call_api(f"/api/dashboard?user_id={USER_ID}")
        if stats:
            st.metric("Total CO₂", f"{stats['total_carbon_kg']:.1f} kg")
            st.metric("Purchases", stats['transaction_count'])

    # Show selected page
    if page == "Dashboard":
        show_dashboard()
    elif page == "Add Purchase":
        show_add_purchase()
    elif page == "Suggestions":
        show_suggestions()
    elif page == "About":
        show_about()


# Run the app!
if __name__ == "__main__":
    main()
