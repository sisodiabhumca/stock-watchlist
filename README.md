# 📈 Stock Watchlist Application

A powerful stock monitoring tool that allows you to track your favorite stocks and view their performance with beautiful, interactive charts.

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://your-username-stock-watchlist-app.streamlit.app/)

## ✨ Features

- 📱 **Responsive Design**: Works on all devices
- 📊 **Interactive Charts**: Beautiful candlestick charts with Plotly
- 🔔 **Real-time Data**: Get the latest stock prices
- 📅 **Historical Data**: View price history with date range selection
- ⭐ **Watchlist**: Add/remove stocks with a single click
- 🌓 **Dark/Light Mode**: Automatic theme detection

## 🚀 Deployment

### Option 1: Deploy on Streamlit Cloud (Recommended)

1. Fork this repository
2. Go to [Streamlit Cloud](https://share.streamlit.io/)
3. Click "New app" and select your forked repository
4. Set the main file path to `app.py`
5. Click "Deploy!"

### Option 2: Run Locally

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/stock-watchlist.git
   cd stock-watchlist
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the application:
   ```bash
   streamlit run app.py
   ```

5. Open your browser to `http://localhost:8501`

## 🛠️ Built With

- [Streamlit](https://streamlit.io/) - The web framework
- [yfinance](https://pypi.org/project/yfinance/) - Yahoo Finance API for stock data
- [Plotly](https://plotly.com/) - Interactive data visualization
- [Pandas](https://pandas.pydata.org/) - Data manipulation

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Data provided by [Yahoo Finance](https://finance.yahoo.com/)
- Built with [Streamlit](https://streamlit.io/)
