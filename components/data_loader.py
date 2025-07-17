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
        self.cache_duration = 300 # 5 minute cache
        self.max_retries = 3
        self.retry_delay = 1 # second

    @st.cache_data(ttl=300)
    def get_stock_data(self, symbol, period = "1y", interval = "1d"):
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
                # create ticker object
                ticker = yf.Ticker(symbol)

                # fetch historical data
                data = ticker.history(period=period, interval=interval)

                if data.empty:
                    st.error(f"No data found for the symbol: {symbol}")
                    return None

                # clean the data
                data = self._clean_stock_data(data, symbol)

                return data

            except Exception as e:
                if attempt < self.max_retries - 1:
                    st.warning(f"Attempt {attempt + 1} failed for {symbol}, retrying...")
                    time.sleep(self.retry_delay * (attempt + 1))
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

        # Remove rows with NaN
        data = data.dropna(how='all')

        # Forward fill missing values
        data = data.fillna(method='ffill')

        # Add symbol value
        data['Symbol'] = symbol

        # Calculate additional features
        data['Returns'] = data['Close'].pct_change()
        data['Log_Returns'] = np.log(data['Close'] / data['Close'].shift(1))

        # Volatility (20 day rolling)
