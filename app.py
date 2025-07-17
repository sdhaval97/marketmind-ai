import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import json

# Import our data loader
from components.data_loader import DataLoader

# Page configuration
st.set_page_config(
    page_title="MarketMind AI",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS (same as before)
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }

    .metric-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }

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

    .info-box {
        background-color: #e8f4f8;
        border-left: 4px solid #1f77b4;
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 0 5px 5px 0;
    }
</style>
""", unsafe_allow_html=True)


# Initialize data loader as singleton
@st.cache_resource
def initialize_data_loader():
    """Initialize and cache the data loader instance"""
    return DataLoader()


def main():
    """Main application function"""

    st.markdown('<h1 class="main-header">📈 MarketMind AI</h1>', unsafe_allow_html=True)

    # Sidebar navigation
    st.sidebar.title("🚀 Navigation")
    st.sidebar.markdown("---")

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

    # Add cache status info
    st.sidebar.markdown("### 💾 Cache Status")
    if st.sidebar.button("Clear Cache"):
        st.cache_data.clear()
        st.sidebar.success("Cache cleared!")
        st.rerun()

    # Route to appropriate page - data_loader is accessed within each function
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
    """Enhanced Market Overview with real data"""
    st.header("🌍 Market Overview")

    # Get data loader instance
    data_loader = initialize_data_loader()

    # Market indices section
    st.subheader("📈 Major Market Indices")

    with st.spinner("Loading market indices..."):
        indices = data_loader.get_market_indices()

    if indices:
        # Create columns for indices
        cols = st.columns(len(indices))

        for i, (name, data) in enumerate(indices.items()):
            with cols[i]:
                delta_color = "normal" if data['change'] >= 0 else "inverse"

                st.metric(
                    label=name,
                    value=f"{data['current']:.2f}",
                    delta=f"{data['change']:.2f} ({data['change_pct']:.2f}%)",
                    delta_color=delta_color
                )

        # Market performance chart
        st.subheader("📊 Market Performance (5-Day)")

        # Create multi-line chart with all indices
        fig = go.Figure()

        for name, data in indices.items():
            if 'data' in data and data['data'] is not None:
                fig.add_trace(go.Scatter(
                    x=data['data'].index,
                    y=data['data']['Close'],
                    mode='lines',
                    name=name,
                    line=dict(width=2),
                    hovertemplate=f"<b>{name}</b><br>" +
                                  "Date: %{x}<br>" +
                                  "Value: %{y:.2f}<extra></extra>"
                ))

        fig.update_layout(
            title="Market Indices Performance",
            xaxis_title="Date",
            yaxis_title="Index Value",
            hovermode='x unified',
            showlegend=True,
            height=500
        )

        st.plotly_chart(fig, use_container_width=True)

    else:
        st.error("Could not load market indices data. Please check your internet connection.")

    # Individual stock analysis
    st.subheader("🔍 Individual Stock Analysis")

    col1, col2, col3 = st.columns(3)

    with col1:
        selected_stock = st.selectbox(
            "Select a stock:",
            options=["AAPL", "GOOGL", "MSFT", "AMZN", "TSLA", "META", "NVDA", "NFLX", "JPM", "JNJ"],
            index=0
        )

    with col2:
        time_period = st.selectbox(
            "Time period:",
            options=["1mo", "3mo", "6mo", "1y", "2y"],
            index=2
        )

    with col3:
        if st.button("🚀 Analyze Stock"):
            analyze_individual_stock(selected_stock, time_period)


def analyze_individual_stock(symbol, period):
    """Analyze individual stock with real data"""

    # Get data loader instance
    data_loader = initialize_data_loader()

    with st.spinner(f"Loading data for {symbol}..."):
        # Get stock data and company info
        stock_data = data_loader.get_stock_data(symbol, period)
        company_info = data_loader.get_company_info(symbol)

        if stock_data is not None and company_info is not None:
            # Company information section
            st.markdown(f"### {company_info['name']} ({symbol})")

            # Basic company info
            col1, col2 = st.columns(2)

            with col1:
                st.markdown(f"**Sector:** {company_info['sector']}")
                st.markdown(f"**Industry:** {company_info['industry']}")
                st.markdown(f"**Country:** {company_info['country']}")
                st.markdown(f"**Market Cap:** {data_loader.format_currency(company_info['market_cap'])}")
                st.markdown(f"**Enterprise Value:** {data_loader.format_currency(company_info['enterprise_value'])}")

            with col2:
                st.markdown(f"**P/E Ratio:** {company_info['pe_ratio']:.2f}" if company_info[
                    'pe_ratio'] else "**P/E Ratio:** N/A")
                st.markdown(f"**Forward P/E:** {company_info['forward_pe']:.2f}" if company_info[
                    'forward_pe'] else "**Forward P/E:** N/A")
                st.markdown(f"**PEG Ratio:** {company_info['peg_ratio']:.2f}" if company_info[
                    'peg_ratio'] else "**PEG Ratio:** N/A")
                st.markdown(f"**Price-to-Book:** {company_info['price_to_book']:.2f}" if company_info[
                    'price_to_book'] else "**Price-to-Book:** N/A")
                st.markdown(f"**Beta:** {company_info['beta']:.2f}" if company_info['beta'] else "**Beta:** N/A")

            # Financial metrics
            st.subheader("💰 Financial Metrics")

            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.metric("Revenue", data_loader.format_currency(company_info['revenue']))
                st.metric("EPS", f"${company_info['eps']:.2f}" if company_info['eps'] else "N/A")

            with col2:
                st.metric("Profit Margin", data_loader.format_percentage(company_info['profit_margin']))
                st.metric("Operating Margin", data_loader.format_percentage(company_info['operating_margin']))

            with col3:
                st.metric("ROE", data_loader.format_percentage(company_info['return_on_equity']))
                st.metric("ROA", data_loader.format_percentage(company_info['return_on_assets']))

            with col4:
                st.metric("Dividend Yield", data_loader.format_percentage(company_info['dividend_yield']))
                st.metric("Payout Ratio", data_loader.format_percentage(company_info['payout_ratio']))

            # Price chart with volume
            st.subheader("📊 Stock Price & Volume")

            from plotly.subplots import make_subplots

            fig = make_subplots(
                rows=2, cols=1,
                shared_xaxes=True,
                vertical_spacing=0.1,
                subplot_titles=('Stock Price', 'Volume'),
                row_heights=[0.7, 0.3]
            )

            # Candlestick chart
            fig.add_trace(
                go.Candlestick(
                    x=stock_data.index,
                    open=stock_data['Open'],
                    high=stock_data['High'],
                    low=stock_data['Low'],
                    close=stock_data['Close'],
                    name='Price'
                ),
                row=1, col=1
            )

            # Volume chart
            fig.add_trace(
                go.Bar(
                    x=stock_data.index,
                    y=stock_data['Volume'],
                    name='Volume',
                    marker_color='rgba(158,202,225,0.8)'
                ),
                row=2, col=1
            )

            fig.update_layout(
                title=f"{symbol} Stock Analysis - {period.upper()}",
                xaxis_rangeslider_visible=False,
                height=600
            )

            st.plotly_chart(fig, use_container_width=True)

            # Performance metrics
            st.subheader("📈 Performance Metrics")

            returns = stock_data['Close'].pct_change().dropna()

            col1, col2, col3, col4 = st.columns(4)

            with col1:
                total_return = ((stock_data['Close'].iloc[-1] / stock_data['Close'].iloc[0]) - 1) * 100
                st.metric("Total Return", f"{total_return:.2f}%")

            with col2:
                volatility = returns.std() * np.sqrt(252) * 100
                st.metric("Annualized Volatility", f"{volatility:.2f}%")

            with col3:
                sharpe_ratio = (returns.mean() * 252) / (returns.std() * np.sqrt(252))
                st.metric("Sharpe Ratio", f"{sharpe_ratio:.2f}")

            with col4:
                max_drawdown = (stock_data['Close'] / stock_data['Close'].cummax() - 1).min() * 100
                st.metric("Max Drawdown", f"{max_drawdown:.2f}%")

            # Data quality report
            with st.expander("📋 Data Quality Report"):
                quality_report = data_loader.get_data_quality_report(stock_data)
                st.json(quality_report)

            # Recent news (placeholder)
            st.subheader("📰 Recent News")
            news_items = data_loader.get_stock_news(symbol, 5)

            for news in news_items:
                with st.expander(f"📰 {news['title']}"):
                    st.write(f"**Source:** {news['source']}")
                    st.write(f"**Published:** {news['published_at'].strftime('%Y-%m-%d %H:%M')}")
                    st.write(f"**Summary:** {news['summary']}")
                    st.write(f"**URL:** {news['url']}")

        else:
            st.error(f"Could not load data for {symbol}. Please try again or select a different stock.")


def show_technical_analysis():
    """Technical Analysis page"""
    st.header("📊 Technical Analysis")
    st.markdown('<div class="info-box">Technical Analysis with real data implementation coming in Step 3!</div>',
                unsafe_allow_html=True)


def show_ml_predictions():
    """Machine Learning Predictions page"""
    st.header("🤖 Machine Learning Predictions")
    st.markdown('<div class="info-box">ML model implementation coming in Step 4!</div>', unsafe_allow_html=True)


def show_portfolio_optimization():
    """Portfolio Optimization page"""
    st.header("💼 Portfolio Optimization")
    st.markdown('<div class="info-box">Portfolio optimization implementation coming in Step 5!</div>',
                unsafe_allow_html=True)


def show_sentiment_analysis():
    """Sentiment Analysis page"""
    st.header("😊 Sentiment Analysis")
    st.markdown('<div class="info-box">Sentiment analysis implementation coming in Step 6!</div>',
                unsafe_allow_html=True)


def show_settings():
    """Settings page"""
    st.header("⚙️ Settings")
    st.markdown('<div class="info-box">Settings and configuration options.</div>', unsafe_allow_html=True)

    # Get data loader instance
    data_loader = initialize_data_loader()

    # Cache management
    st.subheader("💾 Cache Management")

    col1, col2 = st.columns(2)

    with col1:
        st.write("**Cache Status:**")
        st.write("- Stock data: 5 minutes")
        st.write("- Market indices: 10 minutes")
        st.write("- Company info: 1 hour")
        st.write("- News data: 30 minutes")

    with col2:
        if st.button("🗑️ Clear All Cache"):
            st.cache_data.clear()
            st.success("Cache cleared successfully!")
            st.rerun()

    # API settings
    st.subheader("🔧 API Settings")

    st.write("**Data Sources:**")
    st.write("- Stock data: Yahoo Finance (yfinance)")
    st.write("- Market indices: Yahoo Finance")
    st.write("- Company fundamentals: Yahoo Finance")
    st.write("- News: Placeholder (integrate with NewsAPI)")

    # Data refresh settings
    st.subheader("🔄 Data Refresh Settings")

    auto_refresh = st.checkbox("Auto-refresh data", value=True)

    if auto_refresh:
        refresh_interval = st.slider("Refresh interval (minutes)", 1, 60, 5)
        st.info(f"Data will refresh every {refresh_interval} minutes")

    # Performance settings
    st.subheader("⚡ Performance Settings")

    max_retries = st.slider("Max API retries", 1, 5, 3)
    retry_delay = st.slider("Retry delay (seconds)", 1, 10, 2)

    st.info(f"API will retry {max_retries} times with {retry_delay}s delay")


if __name__ == "__main__":
    main()