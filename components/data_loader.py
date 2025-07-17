import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import requests
import time
import warnings

warnings.filterwarnings('ignore')


class DataLoader:
    """
    Professional data loading class for financial data
    Handles API connections, caching, and error management
    """

    def __init__(self):
        self.cache_duration = 300  # 5 minutes cache
        self.max_retries = 3
        self.retry_delay = 1  # seconds

    @st.cache_data(ttl=300)
    def get_stock_data(self, symbol, period="1y", interval="1d"):
        """
        Fetch stock data from Yahoo Finance with error handling

        Args:
            symbol (str): Stock symbol (e.g., 'AAPL')
            period (str): Time period ('1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max')
            interval (str): Data interval ('1m', '2m', '5m', '15m', '30m', '60m', '90m', '1h', '1d', '5d', '1wk', '1mo', '3mo')

        Returns:
            pd.DataFrame: Stock data with OHLCV columns, or None if failed
        """

        for attempt in range(self.max_retries):
            try:
                # Create ticker object
                ticker = yf.Ticker(symbol)

                # Fetch historical data
                data = ticker.history(period=period, interval=interval)

                if data.empty:
                    st.error(f"No data found for symbol: {symbol}")
                    return None

                # Clean and enhance the data
                data = self._clean_stock_data(data, symbol)

                return data

            except Exception as e:
                if attempt < self.max_retries - 1:
                    st.warning(f"Attempt {attempt + 1} failed for {symbol}, retrying...")
                    time.sleep(self.retry_delay * (attempt + 1))  # Exponential backoff
                else:
                    st.error(f"Failed to fetch data for {symbol} after {self.max_retries} attempts: {str(e)}")
                    return None

        return None

    def _clean_stock_data(self, data, symbol):
        """
        Clean and enhance stock data with additional features

        Args:
            data (pd.DataFrame): Raw stock data
            symbol (str): Stock symbol

        Returns:
            pd.DataFrame: Cleaned and enhanced data
        """

        # Remove any rows with all NaN values
        data = data.dropna(how='all')

        # Forward fill missing values (common for weekends/holidays)
        data = data.fillna(method='ffill')

        # Add symbol column
        data['Symbol'] = symbol

        # Calculate additional features
        data['Returns'] = data['Close'].pct_change()
        data['Log_Returns'] = np.log(data['Close'] / data['Close'].shift(1))

        # Volatility (20-day rolling)
        data['Volatility'] = data['Returns'].rolling(window=20).std()

        # Price range (High - Low)
        data['Price_Range'] = data['High'] - data['Low']
        data['Price_Range_Pct'] = (data['Price_Range'] / data['Close']) * 100

        # Volume moving average
        data['Volume_MA'] = data['Volume'].rolling(window=20).mean()
        data['Volume_Ratio'] = data['Volume'] / data['Volume_MA']

        # Support and resistance levels (basic)
        data['Support'] = data['Low'].rolling(window=20).min()
        data['Resistance'] = data['High'].rolling(window=20).max()

        return data

    @st.cache_data(ttl=300)
    def get_multiple_stocks(self, symbols, period="1y"):
        """
        Fetch data for multiple stocks efficiently

        Args:
            symbols (list): List of stock symbols
            period (str): Time period

        Returns:
            dict: Dictionary with symbol as key and DataFrame as value
        """

        stock_data = {}
        failed_symbols = []

        # Create progress bar
        progress_bar = st.progress(0)
        status_text = st.empty()

        for i, symbol in enumerate(symbols):
            status_text.text(f"Loading {symbol}...")

            data = self.get_stock_data(symbol, period)
            if data is not None:
                stock_data[symbol] = data
            else:
                failed_symbols.append(symbol)

            # Update progress
            progress_bar.progress((i + 1) / len(symbols))
            time.sleep(0.1)  # Small delay to show progress

        # Clear progress indicators
        progress_bar.empty()
        status_text.empty()

        if failed_symbols:
            st.warning(f"Failed to load data for: {', '.join(failed_symbols)}")

        return stock_data

    @st.cache_data(ttl=600)  # Cache for 10 minutes
    def get_market_indices(self):
        """
        Fetch major market indices data

        Returns:
            dict: Dictionary with index data and metrics
        """

        indices = {
            'S&P 500': '^GSPC',
            'NASDAQ': '^IXIC',
            'DOW JONES': '^DJI',
            'Russell 2000': '^RUT',
            'VIX': '^VIX'
        }

        index_data = {}

        for name, symbol in indices.items():
            try:
                data = self.get_stock_data(symbol, period="5d", interval="1d")

                if data is not None and len(data) >= 2:
                    current_price = data['Close'].iloc[-1]
                    previous_price = data['Close'].iloc[-2]

                    change = current_price - previous_price
                    change_pct = (change / previous_price) * 100

                    # Calculate additional metrics
                    week_high = data['High'].max()
                    week_low = data['Low'].min()
                    avg_volume = data['Volume'].mean()

                    index_data[name] = {
                        'symbol': symbol,
                        'current': current_price,
                        'previous': previous_price,
                        'change': change,
                        'change_pct': change_pct,
                        'week_high': week_high,
                        'week_low': week_low,
                        'avg_volume': avg_volume,
                        'data': data
                    }
                else:
                    st.warning(f"Insufficient data for {name}")

            except Exception as e:
                st.error(f"Error fetching {name}: {str(e)}")

        return index_data

    @st.cache_data(ttl=3600)  # Cache for 1 hour
    def get_company_info(self, symbol):
        """
        Get comprehensive company information and key metrics

        Args:
            symbol (str): Stock symbol

        Returns:
            dict: Company information and financial metrics
        """

        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info

            # Extract key metrics safely
            key_metrics = {
                'symbol': symbol,
                'name': info.get('longName', 'N/A'),
                'sector': info.get('sector', 'N/A'),
                'industry': info.get('industry', 'N/A'),
                'country': info.get('country', 'N/A'),
                'website': info.get('website', 'N/A'),

                # Financial metrics
                'market_cap': info.get('marketCap', 0),
                'enterprise_value': info.get('enterpriseValue', 0),
                'pe_ratio': info.get('trailingPE', 0),
                'forward_pe': info.get('forwardPE', 0),
                'peg_ratio': info.get('pegRatio', 0),
                'price_to_book': info.get('priceToBook', 0),
                'price_to_sales': info.get('priceToSalesTrailing12Months', 0),

                # Dividends
                'dividend_yield': info.get('dividendYield', 0),
                'dividend_rate': info.get('dividendRate', 0),
                'payout_ratio': info.get('payoutRatio', 0),

                # Performance metrics
                'beta': info.get('beta', 0),
                'eps': info.get('trailingEps', 0),
                'revenue': info.get('totalRevenue', 0),
                'profit_margin': info.get('profitMargins', 0),
                'operating_margin': info.get('operatingMargins', 0),
                'return_on_equity': info.get('returnOnEquity', 0),
                'return_on_assets': info.get('returnOnAssets', 0),

                # Trading metrics
                'volume': info.get('volume', 0),
                'avg_volume': info.get('averageVolume', 0),
                '52_week_high': info.get('fiftyTwoWeekHigh', 0),
                '52_week_low': info.get('fiftyTwoWeekLow', 0),

                # Analyst recommendations
                'target_price': info.get('targetMeanPrice', 0),
                'recommendation': info.get('recommendationKey', 'N/A'),
                'num_analyst_opinions': info.get('numberOfAnalystOpinions', 0),

                # Business description
                'business_summary': info.get('longBusinessSummary', 'N/A')
            }

            return key_metrics

        except Exception as e:
            st.error(f"Error fetching company info for {symbol}: {str(e)}")
            return None

    def format_currency(self, value):
        """
        Format currency values for display

        Args:
            value (float): Currency value

        Returns:
            str: Formatted currency string
        """
        if pd.isna(value) or value == 0:
            return "N/A"

        if value >= 1e12:
            return f"${value / 1e12:.2f}T"
        elif value >= 1e9:
            return f"${value / 1e9:.2f}B"
        elif value >= 1e6:
            return f"${value / 1e6:.2f}M"
        elif value >= 1e3:
            return f"${value / 1e3:.2f}K"
        else:
            return f"${value:.2f}"

    def format_percentage(self, value):
        """
        Format percentage values for display

        Args:
            value (float): Percentage value (as decimal)

        Returns:
            str: Formatted percentage string
        """
        if pd.isna(value) or value == 0:
            return "N/A"

        return f"{value:.2%}"

    def format_number(self, value):
        """
        Format large numbers for display

        Args:
            value (float): Number to format

        Returns:
            str: Formatted number string
        """
        if pd.isna(value) or value == 0:
            return "N/A"

        if value >= 1e9:
            return f"{value / 1e9:.2f}B"
        elif value >= 1e6:
            return f"{value / 1e6:.2f}M"
        elif value >= 1e3:
            return f"{value / 1e3:.2f}K"
        else:
            return f"{value:.2f}"

    def get_data_quality_report(self, data):
        """
        Generate a data quality report for debugging

        Args:
            data (pd.DataFrame): Stock data

        Returns:
            dict: Data quality metrics
        """

        if data is None or data.empty:
            return {"status": "No data"}

        total_rows = len(data)
        missing_values = data.isnull().sum()

        quality_report = {
            "total_rows": total_rows,
            "date_range": f"{data.index.min().date()} to {data.index.max().date()}",
            "missing_values": missing_values.to_dict(),
            "missing_percentage": (missing_values / total_rows * 100).to_dict(),
            "data_types": data.dtypes.to_dict(),
            "memory_usage": data.memory_usage(deep=True).sum(),
            "duplicate_rows": data.duplicated().sum()
        }

        return quality_report

    @st.cache_data(ttl=1800)  # Cache for 30 minutes
    def get_stock_news(self, symbol, count=10):
        """
        Fetch recent news for a stock (placeholder for future implementation)

        Args:
            symbol (str): Stock symbol
            count (int): Number of news items to fetch

        Returns:
            list: List of news items
        """

        # This is a placeholder - in a real implementation, you would
        # integrate with a news API like NewsAPI, Alpha Vantage, or others

        sample_news = [
            {
                "title": f"{symbol} Reports Strong Quarterly Earnings",
                "summary": f"Company {symbol} exceeded analyst expectations with revenue growth.",
                "published_at": datetime.now() - timedelta(hours=2),
                "source": "Financial Times",
                "url": "https://example.com/news1"
            },
            {
                "title": f"{symbol} Announces New Product Launch",
                "summary": f"{symbol} unveiled its latest innovation at the tech conference.",
                "published_at": datetime.now() - timedelta(hours=8),
                "source": "Reuters",
                "url": "https://example.com/news2"
            },
            {
                "title": f"Analyst Upgrades {symbol} Rating",
                "summary": f"Wall Street analyst raises price target for {symbol}.",
                "published_at": datetime.now() - timedelta(days=1),
                "source": "Bloomberg",
                "url": "https://example.com/news3"
            }
        ]

        return sample_news[:count]