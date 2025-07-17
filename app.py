import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta

# Page configuration
st.set_page_config(
    page_title="MarketMind AI",
    page_icon="📈",
    layout="wide", # using full width of the browser
    initial_sidebar_state="expanded" # sidebar starts expanded
)

# custom css for styling
st.markdown("""
<style>
    /* Main header styling */
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }

    /* Metric container styling */
    .metric-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }

    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 5px;
        padding: 0.5rem 1rem;
        font-weight: bold;
        transition: all 0.3s ease;
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }

    /* Sidebar styling */
    .css-1d391kg {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }

    /* Info box styling */
    .info-box {
        background-color: #e8f4f8;
        border-left: 4px solid #1f77b4;
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 0 5px 5px 0;
    }
</style>
""", unsafe_allow_html=True)

def main():

    # main header
    st.markdown('<h1 class="main-header">📈 MarketMind AI</h1>', unsafe_allow_html=True)

    # sidebar
    st.sidebar.title("🚀 Navigation")
    st.sidebar.markdown("---")

    # page selection
    page = st.sidebar.selectbox(
        "Choose a page",
        [
            "🌍 Market Overview",
            "📊 Technical Analysis",
            "🤖 ML Predictions",
            "💼 Portfolio Optimization",
            "😊 Sentiment Analysis",
            "⚙️ Settings"
        ]
    )

    # add info in the sidebar
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📊 Quick Stats")
    st.sidebar.info("Dashboard loaded successfully!")

    # Route to appropriate page based on selection
    if page == "🌍 Market Overview":
        show_market_overview()
    elif page == "📊 Technical Analysis":
        show_technical_analysis()
    elif page == "🤖 ML Predictions":
        show_ml_predictions()
    elif page == "💼 Portfolio Optimization":
        show_portfolio_optimization()
    elif page == "😊 Sentiment Analysis":
        show_sentiment_analysis()
    elif page == "⚙️ Settings":
        show_settings()

    # footer
    st.markdown("---")
    st.markdown("*Built with ❤️ using Streamlit - MarketMind AI*")
