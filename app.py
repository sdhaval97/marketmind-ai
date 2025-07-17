import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta

# Importing data loader
from components.data_loader import DataLoader

# Page configuration - This must be the first Streamlit command
st.set_page_config(
    page_title="Financial Markets Intelligence",
    page_icon="📈",
    layout="wide",  # Use full width of the browser
    initial_sidebar_state="expanded"  # Sidebar starts expanded
)

# Custom CSS for styling
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
    """Main application function"""

    # Main header
    st.markdown('<h1 class="main-header">📈 MarketMind AI</h1>', unsafe_allow_html=True)

    # Sidebar navigation
    st.sidebar.title("🚀 Navigation")
    st.sidebar.markdown("---")

    # Page selection
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

    # Add some info in the sidebar
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

    # Footer
    st.markdown("---")
    st.markdown("*Built with ❤️ using Streamlit - MarketMind AI*")


def show_market_overview():
    """Market Overview page"""
    st.header("🌍 Market Overview")

    # Welcome message
    st.markdown(
        '<div class="info-box">Welcome to the Market Overview! This page will display real-time market data, major indices, and individual stock analysis.</div>',
        unsafe_allow_html=True)

    # Placeholder metrics using columns
    st.subheader("📈 Major Market Indices")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            label="S&P 500",
            value="4,200.50",
            delta="12.30 (0.29%)",
            delta_color="normal"
        )

    with col2:
        st.metric(
            label="NASDAQ",
            value="14,500.25",
            delta="-25.10 (-0.17%)",
            delta_color="inverse"
        )

    with col3:
        st.metric(
            label="DOW JONES",
            value="33,800.75",
            delta="5.50 (0.02%)",
            delta_color="normal"
        )

    with col4:
        st.metric(
            label="VIX",
            value="18.45",
            delta="-0.85 (-4.4%)",
            delta_color="normal"
        )

    # Sample chart
    st.subheader("📊 Market Performance")

    # Create sample data for demonstration
    dates = pd.date_range(start='2024-01-01', end='2024-01-31', freq='D')
    sample_data = pd.DataFrame({
        'Date': dates,
        'S&P 500': np.random.randn(len(dates)).cumsum() + 4200,
        'NASDAQ': np.random.randn(len(dates)).cumsum() + 14500,
        'DOW': np.random.randn(len(dates)).cumsum() + 33800
    })

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=sample_data['Date'],
        y=sample_data['S&P 500'],
        mode='lines',
        name='S&P 500',
        line=dict(color='blue', width=2)
    ))

    fig.add_trace(go.Scatter(
        x=sample_data['Date'],
        y=sample_data['NASDAQ'],
        mode='lines',
        name='NASDAQ',
        line=dict(color='red', width=2)
    ))

    fig.add_trace(go.Scatter(
        x=sample_data['Date'],
        y=sample_data['DOW'],
        mode='lines',
        name='DOW',
        line=dict(color='green', width=2)
    ))

    fig.update_layout(
        title="Market Indices Performance (Sample Data)",
        xaxis_title="Date",
        yaxis_title="Index Value",
        hovermode='x unified',
        showlegend=True
    )

    st.plotly_chart(fig, use_container_width=True)

    # Interactive stock selector
    st.subheader("🔍 Stock Analysis")

    col1, col2 = st.columns(2)

    with col1:
        selected_stock = st.selectbox(
            "Select a stock to analyze:",
            options=["AAPL", "GOOGL", "MSFT", "AMZN", "TSLA", "META", "NVDA"],
            index=0
        )

    with col2:
        time_period = st.selectbox(
            "Select time period:",
            options=["1D", "5D", "1M", "3M", "6M", "1Y"],
            index=3
        )

    if st.button("🚀 Analyze Stock"):
        st.success(f"Analysis for {selected_stock} over {time_period} period will be implemented in the next steps!")
        st.info("This will connect to real financial APIs and display detailed stock information.")


def show_technical_analysis():
    """Technical Analysis page"""
    st.header("📊 Technical Analysis")

    st.markdown(
        '<div class="info-box">Technical Analysis tools will help you analyze stock price movements using various indicators like RSI, MACD, and Bollinger Bands.</div>',
        unsafe_allow_html=True)

    # Placeholder content
    st.subheader("🔧 Available Technical Indicators")

    col1, col2 = st.columns(2)

    with col1:
        st.write("**Trend Indicators:**")
        st.write("- Moving Averages (SMA, EMA)")
        st.write("- MACD")
        st.write("- Bollinger Bands")

    with col2:
        st.write("**Momentum Indicators:**")
        st.write("- RSI (Relative Strength Index)")
        st.write("- Stochastic Oscillator")
        st.write("- Williams %R")

    st.info("📈 Technical analysis implementation coming in Step 3!")


def show_ml_predictions():
    """Machine Learning Predictions page"""
    st.header("🤖 Machine Learning Predictions")

    st.markdown(
        '<div class="info-box">Use advanced machine learning models to predict stock price movements and generate trading signals.</div>',
        unsafe_allow_html=True)

    # Model selection placeholder
    st.subheader("🧠 Available ML Models")

    col1, col2 = st.columns(2)

    with col1:
        st.write("**Random Forest Classifier**")
        st.write("- Feature-based prediction")
        st.write("- Technical indicator inputs")
        st.write("- High interpretability")

    with col2:
        st.write("**LSTM Neural Network**")
        st.write("- Time series prediction")
        st.write("- Deep learning approach")
        st.write("- Pattern recognition")

    st.info("🤖 ML model implementation coming in Step 4!")


def show_portfolio_optimization():
    """Portfolio Optimization page"""
    st.header("💼 Portfolio Optimization")

    st.markdown(
        '<div class="info-box">Create optimized portfolios using Modern Portfolio Theory, efficient frontier analysis, and risk management techniques.</div>',
        unsafe_allow_html=True)

    # Optimization methods placeholder
    st.subheader("⚖️ Optimization Methods")

    col1, col2 = st.columns(2)

    with col1:
        st.write("**Efficient Frontier**")
        st.write("- Risk-return optimization")
        st.write("- Sharpe ratio maximization")
        st.write("- Diversification analysis")

    with col2:
        st.write("**Monte Carlo Simulation**")
        st.write("- Scenario analysis")
        st.write("- Risk assessment")
        st.write("- Portfolio backtesting")

    st.info("💼 Portfolio optimization implementation coming in Step 5!")


def show_sentiment_analysis():
    """Sentiment Analysis page"""
    st.header("😊 Sentiment Analysis")

    st.markdown(
        '<div class="info-box">Analyze market sentiment from news articles, social media, and financial reports to gauge market mood and potential price movements.</div>',
        unsafe_allow_html=True)

    # Sentiment sources placeholder
    st.subheader("📰 Sentiment Sources")

    col1, col2 = st.columns(2)

    with col1:
        st.write("**News Analysis**")
        st.write("- Financial news sentiment")
        st.write("- Real-time processing")
        st.write("- Source credibility weighting")

    with col2:
        st.write("**Social Media**")
        st.write("- Twitter sentiment tracking")
        st.write("- Reddit discussions")
        st.write("- Influencer impact analysis")

    st.info("😊 Sentiment analysis implementation coming in Step 6!")


def show_settings():
    """Settings page"""
    st.header("⚙️ Settings")

    st.markdown('<div class="info-box">Configure your dashboard preferences, API settings, and data sources.</div>',
                unsafe_allow_html=True)

    # Settings sections
    st.subheader("🔧 Configuration Options")

    col1, col2 = st.columns(2)

    with col1:
        st.write("**Data Sources**")
        st.write("- API key management")
        st.write("- Data refresh intervals")
        st.write("- Cache settings")

    with col2:
        st.write("**Display Options**")
        st.write("- Theme customization")
        st.write("- Chart preferences")
        st.write("- Notification settings")

    # Sample settings
    st.subheader("📊 Dashboard Preferences")

    auto_refresh = st.checkbox("Auto-refresh data", value=True)
    refresh_interval = st.slider("Refresh interval (minutes)", 1, 60, 5)

    if st.button("💾 Save Settings"):
        st.success("Settings saved successfully!")
        st.balloons()


# Run the application
if __name__ == "__main__":
    main()