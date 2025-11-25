"""
Carbon Footprint Tracker - NO CSS VERSION FOR TESTING
"""
import streamlit as st
import requests

# Configuration
API_BASE_URL = "http://localhost:8000"
USER_ID = "default_user"

# Page config - NO CUSTOM CSS
st.set_page_config(
    page_title="Carbon Footprint Tracker",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# NO CUSTOM CSS AT ALL - Just test if content shows

st.title("🔴 TESTING VERSION - NO CSS")
st.write("If you can see this text, the issue is CSS-related")
st.write("If you CANNOT see this text, the issue is deeper")

with st.sidebar:
    st.header("Sidebar Test")
    if st.button("Test Button"):
        st.success("Button clicked!")
    st.metric("Test Metric", "100 kg CO₂")

st.header("Main Content Area")
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Metric 1", "Value 1")
with col2:
    st.metric("Metric 2", "Value 2")
with col3:
    st.metric("Metric 3", "Value 3")

st.divider()
st.info("This is an info message - can you see it?")
st.success("This is a success message - can you see it?")
st.warning("This is a warning message - can you see it?")
