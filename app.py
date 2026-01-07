import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json
import os

# Page config
st.set_page_config(page_title="Stock Watchlist", layout="wide")

# Initialize session state for watchlist
if 'watchlist' not in st.session_state:
    st.session_state.watchlist = []

# Load watchlist from file if exists
WATCHLIST_FILE = 'watchlist.json'

def load_watchlist():
    if os.path.exists(WATCHLIST_FILE):
        with open(WATCHLIST_FILE, 'r') as f:
            st.session_state.watchlist = json.load(f)

def save_watchlist():
    with open(WATCHLIST_FILE, 'w') as f:
        json.dump(st.session_state.watchlist, f)

# Load watchlist on startup
load_watchlist()

def get_stock_data(ticker, start_date=None, end_date=None, period='1mo'):
    try:
        stock = yf.Ticker(ticker)
        if start_date and end_date:
            # Use date range if provided
            hist = stock.history(start=start_date, end=end_date)
        else:
            # Fall back to period
            hist = stock.history(period=period)
        return hist, stock, None
    except Exception as e:
        return None, None, str(e)

def add_to_watchlist(ticker):
    if ticker and ticker.upper() not in [t['symbol'] for t in st.session_state.watchlist]:
        st.session_state.watchlist.append({
            'symbol': ticker.upper(),
            'added_date': datetime.now().strftime('%Y-%m-%d')
        })
        save_watchlist()
        st.success(f"{ticker.upper()} added to watchlist!")
    elif ticker:
        st.warning(f"{ticker.upper()} is already in your watchlist!")

def remove_from_watchlist(ticker):
    st.session_state.watchlist = [t for t in st.session_state.watchlist if t['symbol'] != ticker]
    save_watchlist()
    st.success(f"{ticker} removed from watchlist!")

# Sidebar for adding stocks
with st.sidebar:
    st.title("📈 Stock Watchlist")
    
    # Add stock form
    with st.form("add_stock"):
        ticker = st.text_input("Enter stock ticker (e.g., AAPL, MSFT, GOOGL):").strip().upper()
        submitted = st.form_submit_button("Add to Watchlist")
        if submitted and ticker:
            add_to_watchlist(ticker)
    
    # Display watchlist
    st.subheader("Your Watchlist")
    for stock in st.session_state.watchlist:
        col1, col2 = st.columns([3, 1])
        with col1:
            st.write(f"📊 {stock['symbol']}")
        with col2:
            if st.button("❌", key=f"del_{stock['symbol']}"):
                remove_from_watchlist(stock['symbol'])
                st.rerun()

# Main content
st.title("Stock Price Tracker")

# Date range selection
col1, col2 = st.columns(2)
with col1:
    start_date = st.date_input("Start Date", datetime.now() - timedelta(days=365))
with col2:
    end_date = st.date_input("End Date", datetime.now())
    
# Validate date range
if start_date >= end_date:
    st.warning("⚠️ Start date must be before end date. Using default 1-year period.")

# Display stock data
if st.session_state.watchlist:
    selected_stock = st.selectbox(
        "Select a stock to view:",
        [stock['symbol'] for stock in st.session_state.watchlist]
    )
    
    if selected_stock:
        # Use date range if provided, otherwise use default period
        if start_date and end_date and start_date < end_date:
            data, stock_obj, error = get_stock_data(selected_stock, start_date=start_date, end_date=end_date)
        else:
            period = '1y'  # Default period
            data, stock_obj, error = get_stock_data(selected_stock, period=period)
        
        if error:
            st.error(f"Error fetching data for {selected_stock}: {error}")
        elif data is not None and not data.empty:
            # Display basic info
            try:
                stock_name = stock_obj.info.get('longName', selected_stock) if stock_obj else selected_stock
            except Exception:
                stock_name = selected_stock
            st.subheader(f"{selected_stock} - {stock_name}")
            
            # Current price and change
            current_price = data['Close'].iloc[-1]
            prev_close = data['Close'].iloc[-2] if len(data) > 1 else current_price
            price_change = current_price - prev_close
            percent_change = (price_change / prev_close) * 100 if prev_close != 0 else 0
            
            col1, col2, col3 = st.columns(3)
            col1.metric("Current Price", f"${current_price:.2f}")
            col2.metric("Price Change", f"${price_change:.2f}", f"{percent_change:.2f}%")
            
            # Additional metrics
            try:
                if stock_obj:
                    info = stock_obj.info
                    market_cap = info.get('marketCap', 'N/A')
                    if market_cap != 'N/A' and market_cap:
                        market_cap_str = f"${market_cap/1e9:.2f}B" if market_cap >= 1e9 else f"${market_cap/1e6:.2f}M"
                        col3.metric("Market Cap", market_cap_str)
            except Exception:
                pass
            
            # Stock chart
            fig = go.Figure()
            fig.add_trace(go.Candlestick(x=data.index,
                            open=data['Open'],
                            high=data['High'],
                            low=data['Low'],
                            close=data['Close'],
                            name=selected_stock))
            
            fig.update_layout(
                title=f"{selected_stock} Stock Price",
                xaxis_title="Date",
                yaxis_title="Price ($)",
                template="plotly_white"
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Display historical data
            st.subheader("Historical Data")
            st.dataframe(data[['Open', 'High', 'Low', 'Close', 'Volume']].sort_index(ascending=False).head(10))
else:
    st.info("Your watchlist is empty. Add stocks using the sidebar to get started!")

# Add some styling
st.markdown("""
<style>
    .stButton>button {
        padding: 0.25rem 0.5rem;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: #f0f2f6;
        border-radius: 4px 4px 0px 0px;
        gap: 1px;
        padding-top: 10px;
        padding-bottom: 10px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #ffffff;
    }
</style>
""", unsafe_allow_html=True)
