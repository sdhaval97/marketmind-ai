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
