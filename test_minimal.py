"""
Minimal test to verify Streamlit is working
"""
import streamlit as st

st.set_page_config(page_title="Test", layout="wide")

st.title("🔴 TEST - If you see this, Streamlit works!")
st.write("This is a minimal test page")
st.sidebar.title("Sidebar Test")
st.sidebar.write("If you see this sidebar, rendering works")
st.button("Test Button")
st.metric("Test Metric", "123")
