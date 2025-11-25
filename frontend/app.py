"""
Streamlit frontend for Carbon Footprint Tracker.
Interactive dashboard for visualizing and analyzing carbon footprint.
"""
import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json

# Configuration
API_BASE_URL = "http://localhost:8000"
USER_ID = "default_user"

# Page config
st.set_page_config(
    page_title="Carbon Footprint Tracker",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Clear Streamlit cache to force reload
st.cache_data.clear()
st.cache_resource.clear()

# Custom CSS with Forest Theme
st.markdown("""
    <style>
    /* Forest Background - CSS only (no external images) */
    .stApp {
        background: linear-gradient(135deg,
            #1a4d2e 0%,
            #2d5a3d 25%,
            #3d6b4d 50%,
            #2d5a3d 75%,
            #1a4d2e 100%);
        background-size: 400% 400%;
        animation: forestGradient 15s ease infinite;
        position: relative;
    }

    @keyframes forestGradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    /* Add texture overlay */
    .stApp::before {
        content: "";
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background:
            radial-gradient(circle at 20% 50%, rgba(76, 175, 80, 0.1) 0%, transparent 50%),
            radial-gradient(circle at 80% 20%, rgba(139, 195, 74, 0.1) 0%, transparent 50%),
            radial-gradient(circle at 40% 80%, rgba(56, 142, 60, 0.1) 0%, transparent 50%);
        pointer-events: none;
        z-index: 0;
    }

    /* Main content area with semi-transparent background */
    .main .block-container {
        background-color: rgba(255, 255, 255, 0.95);
        border-radius: 15px;
        padding: 2rem;
        backdrop-filter: blur(10px);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        position: relative;
        z-index: 1;
    }

    /* Sidebar with forest theme */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg,
            rgba(46, 125, 50, 0.95) 0%,
            rgba(27, 94, 32, 0.95) 100%);
        backdrop-filter: blur(10px);
        position: relative;
        z-index: 1;
    }

    section[data-testid="stSidebar"] * {
        color: white !important;
    }

    section[data-testid="stSidebar"] .stButton button {
        background-color: rgba(255, 255, 255, 0.2);
        color: white !important;
        border: 2px solid rgba(255, 255, 255, 0.5);
        border-radius: 10px;
        transition: all 0.3s ease;
    }

    section[data-testid="stSidebar"] .stButton button:hover {
        background-color: rgba(255, 255, 255, 0.3);
        border-color: white;
        transform: scale(1.05);
    }

    /* Header */
    .main-header {
        font-size: 3.5rem;
        font-weight: bold;
        color: #1B5E20;
        text-align: center;
        margin-bottom: 1rem;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.1);
        background: linear-gradient(135deg, #2E7D32, #66BB6A);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }

    /* Metric cards with nature theme */
    .metric-card {
        background: linear-gradient(135deg, #E8F5E9 0%, #C8E6C9 100%);
        padding: 1.5rem;
        border-radius: 15px;
        margin: 0.5rem 0;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        border-left: 5px solid #4CAF50;
        transition: transform 0.3s ease;
    }

    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.15);
    }

    /* Suggestion cards */
    .suggestion-card {
        background: linear-gradient(135deg, #E8F5E9 0%, #C8E6C9 100%);
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        border-left: 6px solid #4CAF50;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        transition: transform 0.3s ease;
    }

    .suggestion-card:hover {
        transform: translateX(10px);
        box-shadow: 0 6px 20px rgba(76, 175, 80, 0.3);
    }

    /* Streamlit metrics */
    div[data-testid="stMetricValue"] {
        font-size: 2rem;
        color: #1B5E20;
        font-weight: bold;
    }

    /* Headers */
    h1, h2, h3 {
        color: #1B5E20 !important;
    }

    /* Info boxes */
    .stAlert {
        background-color: rgba(232, 245, 233, 0.9);
        border-left: 5px solid #4CAF50;
        border-radius: 10px;
    }

    /* Dataframes */
    .dataframe {
        border-radius: 10px;
        overflow: hidden;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
    }

    /* Buttons */
    .stButton button {
        background: linear-gradient(135deg, #4CAF50 0%, #66BB6A 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.75rem 2rem;
        font-weight: bold;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(76, 175, 80, 0.3);
    }

    .stButton button:hover {
        background: linear-gradient(135deg, #388E3C 0%, #4CAF50 100%);
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(76, 175, 80, 0.4);
    }

    /* File uploader */
    .uploadedFile {
        background-color: rgba(232, 245, 233, 0.5);
        border-radius: 10px;
    }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        background-color: rgba(232, 245, 233, 0.5);
        border-radius: 10px;
    }

    .stTabs [data-baseweb="tab"] {
        color: #1B5E20;
        font-weight: 600;
    }

    .stTabs [aria-selected="true"] {
        background-color: #4CAF50;
        color: white !important;
    }

    /* Divider */
    hr {
        border-color: #4CAF50;
        opacity: 0.3;
    }

    /* Radio buttons */
    .stRadio > label {
        color: white !important;
        font-weight: 600;
    }

    /* Text inputs */
    .stTextInput input, .stNumberInput input, .stDateInput input {
        border-radius: 10px;
        border: 2px solid #4CAF50;
    }

    /* Success/Info messages */
    .success {
        background-color: rgba(76, 175, 80, 0.1);
        border-left: 5px solid #4CAF50;
        padding: 1rem;
        border-radius: 10px;
    }

    /* Force black text in suggestion cards */
    .suggestion-card h4,
    .suggestion-card p,
    .suggestion-card strong {
        color: #1B5E20 !important;
    }

    /* Ensure all text is readable */
    p, span, div {
        color: #212121;
    }

    /* Fix plotly charts background */
    .js-plotly-plot {
        background-color: white;
        border-radius: 10px;
    }
    </style>
""", unsafe_allow_html=True)


# Helper functions
def call_api(endpoint, method="GET", data=None, files=None):
    """Make API calls to the backend."""
    url = f"{API_BASE_URL}{endpoint}"
    try:
        if method == "GET":
            response = requests.get(url)
        elif method == "POST":
            if files:
                response = requests.post(url, files=files, data=data)
            else:
                response = requests.post(url, json=data)
        else:
            return None

        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"API Error: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        st.error(f"Connection Error: {str(e)}")
        st.info("Make sure the FastAPI backend is running on http://localhost:8000")
        return None


def get_dashboard_stats():
    """Get dashboard statistics."""
    return call_api(f"/api/dashboard?user_id={USER_ID}")


def get_transactions():
    """Get all transactions."""
    return call_api(f"/api/transactions?user_id={USER_ID}")


def get_suggestions():
    """Get carbon reduction suggestions."""
    return call_api(f"/api/suggestions?user_id={USER_ID}")


def load_sample_data():
    """Load sample data for demo."""
    return call_api(f"/api/sample-data?user_id={USER_ID}", method="POST")


# Main app
def main():
    # Header
    st.markdown('<div class="main-header">🌍 Carbon Footprint Tracker</div>', unsafe_allow_html=True)
    st.markdown(
        "<p style='text-align: center; color: #666;'>Track your environmental impact and get personalized suggestions to reduce your carbon footprint</p>",
        unsafe_allow_html=True
    )

    # Sidebar
    with st.sidebar:
        st.header("📊 Navigation")
        page = st.radio(
            "Select Page",
            ["Dashboard", "Transactions", "Upload Data", "Suggestions", "About"]
        )

        st.divider()

        # Sample data button
        if st.button("🎲 Load Sample Data", use_container_width=True):
            with st.spinner("Loading sample data..."):
                result = load_sample_data()
                if result:
                    st.success("Sample data loaded!")
                    st.rerun()

        st.divider()
        st.markdown("### 💡 Quick Stats")

        # Get quick stats
        stats = get_dashboard_stats()
        if stats:
            st.metric("Total Emissions", f"{stats['total_carbon_kg']:.1f} kg CO₂")
            st.metric("This Month", f"{stats['monthly_carbon_kg']:.1f} kg CO₂")
            st.metric("Transactions", stats['transaction_count'])

    # Main content based on selected page
    if page == "Dashboard":
        show_dashboard()
    elif page == "Transactions":
        show_transactions()
    elif page == "Upload Data":
        show_upload()
    elif page == "Suggestions":
        show_suggestions()
    elif page == "About":
        show_about()


def show_dashboard():
    """Display the main dashboard."""
    st.header("📊 Dashboard Overview")

    # Get data
    stats = get_dashboard_stats()
    if not stats or stats['transaction_count'] == 0:
        st.info("👋 Welcome! Upload your transaction data or load sample data to get started.")
        return

    # Top metrics
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Total Carbon Footprint",
            f"{stats['total_carbon_kg']:.1f} kg CO₂",
            help="Total carbon emissions from all tracked purchases"
        )

    with col2:
        st.metric(
            "Monthly Emissions",
            f"{stats['monthly_carbon_kg']:.1f} kg CO₂",
            help="Carbon emissions in the last 30 days"
        )

    with col3:
        comparison = stats['comparison_to_average']
        delta = comparison['difference_kg']
        delta_text = f"{abs(delta):.0f} kg vs avg"
        st.metric(
            "vs US Average",
            f"{comparison['percentage']:.0f}%",
            delta=delta_text,
            delta_color="inverse",
            help=f"US average: {comparison['average_monthly_kg']} kg CO₂/month"
        )

    with col4:
        st.metric(
            "Transactions Tracked",
            stats['transaction_count'],
            help="Total number of purchases analyzed"
        )

    st.divider()

    # Charts
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📈 Emissions by Category")
        if stats['category_breakdown']:
            # Create pie chart
            df_categories = pd.DataFrame([
                {"Category": k.replace("_", " ").title(), "CO₂ (kg)": v}
                for k, v in stats['category_breakdown'].items()
            ])

            fig = px.pie(
                df_categories,
                values="CO₂ (kg)",
                names="Category",
                color_discrete_sequence=px.colors.sequential.Greens_r
            )
            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("🎯 Top Categories")
        if stats['category_breakdown']:
            df_top = pd.DataFrame([
                {"Category": k.replace("_", " ").title(), "CO₂ (kg)": v}
                for k, v in sorted(
                    stats['category_breakdown'].items(),
                    key=lambda x: x[1],
                    reverse=True
                )[:5]
            ])

            fig = px.bar(
                df_top,
                x="CO₂ (kg)",
                y="Category",
                orientation='h',
                color="CO₂ (kg)",
                color_continuous_scale="Reds"
            )
            fig.update_layout(showlegend=False, yaxis={'categoryorder':'total ascending'})
            st.plotly_chart(fig, use_container_width=True)

    # Timeline view
    st.subheader("📅 Emissions Over Time")
    transactions = get_transactions()
    if transactions:
        df_trans = pd.DataFrame(transactions)
        df_trans['date'] = pd.to_datetime(df_trans['date'])
        df_trans['date_only'] = df_trans['date'].dt.date

        # Group by date
        daily_emissions = df_trans.groupby('date_only')['carbon_kg'].sum().reset_index()
        daily_emissions.columns = ['Date', 'CO₂ (kg)']

        fig = px.area(
            daily_emissions,
            x='Date',
            y='CO₂ (kg)',
            title="Daily Carbon Emissions",
            color_discrete_sequence=['#4CAF50']
        )
        fig.update_layout(hovermode='x unified')
        st.plotly_chart(fig, use_container_width=True)


def show_transactions():
    """Display all transactions."""
    st.header("💳 Transaction History")

    transactions = get_transactions()
    if not transactions:
        st.info("No transactions found. Upload data or load sample data to get started.")
        return

    # Create DataFrame
    df = pd.DataFrame(transactions)
    df['date'] = pd.to_datetime(df['date']).dt.strftime('%Y-%m-%d')
    df['category'] = df['category'].str.replace('_', ' ').str.title()

    # Filters
    col1, col2, col3 = st.columns(3)

    with col1:
        categories = ['All'] + sorted(df['category'].unique().tolist())
        selected_category = st.selectbox("Filter by Category", categories)

    with col2:
        min_amount = st.number_input("Min Amount ($)", min_value=0.0, value=0.0)

    with col3:
        sort_by = st.selectbox("Sort By", ["Date (Newest)", "Date (Oldest)", "Amount (High)", "Amount (Low)", "Carbon (High)"])

    # Apply filters
    filtered_df = df.copy()
    if selected_category != 'All':
        filtered_df = filtered_df[filtered_df['category'] == selected_category]
    if min_amount > 0:
        filtered_df = filtered_df[filtered_df['amount'] >= min_amount]

    # Apply sorting
    if sort_by == "Date (Newest)":
        filtered_df = filtered_df.sort_values('date', ascending=False)
    elif sort_by == "Date (Oldest)":
        filtered_df = filtered_df.sort_values('date', ascending=True)
    elif sort_by == "Amount (High)":
        filtered_df = filtered_df.sort_values('amount', ascending=False)
    elif sort_by == "Amount (Low)":
        filtered_df = filtered_df.sort_values('amount', ascending=True)
    elif sort_by == "Carbon (High)":
        filtered_df = filtered_df.sort_values('carbon_kg', ascending=False)

    # Display summary
    st.metric("Total Emissions (Filtered)", f"{filtered_df['carbon_kg'].sum():.2f} kg CO₂")

    # Display table
    display_df = filtered_df[['date', 'description', 'amount', 'category', 'carbon_kg', 'confidence_score']].copy()
    display_df.columns = ['Date', 'Description', 'Amount ($)', 'Category', 'CO₂ (kg)', 'Confidence']
    display_df['Amount ($)'] = display_df['Amount ($)'].apply(lambda x: f"${x:.2f}")
    display_df['CO₂ (kg)'] = display_df['CO₂ (kg)'].apply(lambda x: f"{x:.2f}")
    display_df['Confidence'] = display_df['Confidence'].apply(lambda x: f"{x:.0%}")

    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True
    )


def show_upload():
    """Upload transaction data."""
    st.header("📤 Upload Transaction Data")

    st.markdown("""
    Upload your transaction data in CSV format. The CSV should contain the following columns:
    - **description** (or merchant/name): Description of the purchase
    - **amount** (or total/price): Transaction amount in USD
    - **date** (optional): Transaction date

    Any additional columns will be preserved in the raw data.
    """)

    # File uploader
    uploaded_file = st.file_uploader(
        "Choose a CSV file",
        type=['csv'],
        help="Upload a CSV file with your transaction data"
    )

    if uploaded_file is not None:
        # Show preview
        try:
            df_preview = pd.read_csv(uploaded_file)
            st.subheader("📋 File Preview")
            st.dataframe(df_preview.head(10), use_container_width=True)

            # Reset file pointer
            uploaded_file.seek(0)

            # Upload button
            col1, col2 = st.columns([1, 3])
            with col1:
                if st.button("🚀 Process & Upload", type="primary", use_container_width=True):
                    with st.spinner("Processing transactions..."):
                        files = {"file": (uploaded_file.name, uploaded_file, "text/csv")}
                        data = {"user_id": USER_ID}
                        result = call_api("/api/transactions/upload", method="POST", files=files, data=data)

                        if result:
                            st.success(f"✅ Successfully processed {len(result)} transactions!")
                            st.balloons()

                            # Show summary
                            total_carbon = sum(t['carbon_kg'] for t in result)
                            st.metric("Total Carbon Added", f"{total_carbon:.2f} kg CO₂")

                            # Rerun to update dashboard
                            st.rerun()

        except Exception as e:
            st.error(f"Error reading file: {str(e)}")

    st.divider()

    # Manual entry
    st.subheader("✍️ Add Single Transaction")
    with st.form("manual_transaction"):
        col1, col2 = st.columns(2)

        with col1:
            description = st.text_input("Description", placeholder="e.g., Starbucks Coffee")
            amount = st.number_input("Amount ($)", min_value=0.01, value=10.0, step=0.01)

        with col2:
            date = st.date_input("Date", value=datetime.now())

        submitted = st.form_submit_button("Add Transaction", type="primary")

        if submitted and description and amount > 0:
            data = {
                "description": description,
                "amount": amount,
                "date": date.isoformat(),
                "user_id": USER_ID
            }

            result = call_api("/api/transactions", method="POST", data=data)
            if result:
                st.success(f"✅ Added transaction: {result['carbon_kg']:.2f} kg CO₂")
                st.rerun()


def show_suggestions():
    """Display carbon reduction suggestions."""
    st.header("💡 Personalized Suggestions")

    suggestions = get_suggestions()
    if not suggestions:
        st.info("Track some purchases first to get personalized suggestions!")
        return

    st.markdown("Based on your purchase history, here are personalized recommendations to reduce your carbon footprint:")

    for i, suggestion in enumerate(suggestions, 1):
        # Determine difficulty color
        difficulty_colors = {
            "easy": "🟢",
            "medium": "🟡",
            "hard": "🔴"
        }
        difficulty_icon = difficulty_colors.get(suggestion['difficulty'], "⚪")

        # Create suggestion card
        st.markdown(f"""
        <div class="suggestion-card">
            <h4>{i}. {suggestion['suggestion']}</h4>
            <p>
                <strong>Potential Reduction:</strong> {suggestion['reduction_kg']:.2f} kg CO₂<br>
                <strong>Difficulty:</strong> {difficulty_icon} {suggestion['difficulty'].title()}<br>
                <strong>Category:</strong> {suggestion['category'].replace('_', ' ').title()}
            </p>
        </div>
        """, unsafe_allow_html=True)

    # Impact summary
    st.divider()
    total_reduction = sum(s['reduction_kg'] for s in suggestions)
    st.success(f"🎯 If you implement all suggestions, you could reduce your carbon footprint by **{total_reduction:.2f} kg CO₂**!")

    # Trees equivalent
    trees = total_reduction / 21.77  # Average tree absorbs ~21.77 kg CO2/year
    st.info(f"🌳 That's equivalent to planting **{trees:.1f} trees** for a year!")


def show_about():
    """Display about page."""
    st.header("ℹ️ About Carbon Footprint Tracker")

    st.markdown("""
    ## What is Carbon Footprint Tracker?

    Carbon Footprint Tracker is an intelligent web application that helps you understand and reduce
    your environmental impact by analyzing your purchase data.

    ### 🎯 Features

    - **Transaction Analysis**: Upload receipts or bank transaction CSV files
    - **AI Classification**: Automatically categorize purchases using NLP
    - **Carbon Estimation**: Calculate CO₂ emissions for each purchase
    - **Smart Suggestions**: Get personalized recommendations to reduce your footprint
    - **Beautiful Visualizations**: Track your progress with interactive charts

    ### 🛠️ Technology Stack

    - **Backend**: FastAPI (Python)
    - **Frontend**: Streamlit
    - **Database**: SQLite / PostgreSQL
    - **NLP**: Pattern matching & classification
    - **APIs**: Climatiq (carbon data), OpenAI (suggestions)

    ### 📊 How It Works

    1. **Upload Data**: Import your transaction data via CSV upload
    2. **AI Analysis**: Machine learning classifies each purchase by category
    3. **Carbon Calculation**: Emissions are estimated using industry data
    4. **Get Insights**: View dashboards and receive personalized suggestions
    5. **Take Action**: Implement recommendations to reduce your footprint

    ### 🌍 Why It Matters

    The average American generates about **16 tons of CO₂ per year**. Small changes in our
    purchasing habits can make a significant difference. This tool helps you:

    - Understand where your emissions come from
    - Track progress over time
    - Make informed, sustainable choices
    - Visualize your environmental impact

    ### 🚀 Getting Started

    1. Load sample data or upload your own transaction CSV
    2. Explore the dashboard to see your carbon breakdown
    3. Review personalized suggestions
    4. Start making greener choices!

    ### 📝 CSV Format

    Your CSV file should include:
    - `description` or `merchant`: Purchase description
    - `amount` or `total`: Transaction amount in USD
    - `date` (optional): Transaction date

    Example:
    ```
    date,description,amount
    2024-01-15,Whole Foods Market,87.50
    2024-01-16,Shell Gas Station,45.00
    2024-01-17,United Airlines,350.00
    ```

    ### 🤝 Contributing

    This is an open-source project. Contributions are welcome!

    ### 📄 License

    MIT License - feel free to use and modify for your needs.

    ---

    Made with 💚 for a sustainable future
    """)


if __name__ == "__main__":
    main()
