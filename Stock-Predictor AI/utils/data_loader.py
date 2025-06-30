import yfinance as yf
import pandas as pd

def fetch_stock_data(ticker, start_date, end_date):
    try:
        # Download data using yfinance
        data = yf.download(ticker, start=start_date, end=end_date)

        if data.empty:
            return None

        data = data.copy()
        data.reset_index(inplace=True)  # ✅ Ensure 'Date' becomes a column

        # Keep only necessary columns
        data = data[['Date', 'Open', 'High', 'Low', 'Close', 'Volume']]
        data.dropna(inplace=True)

        return data

    except Exception as e:
        print(f"Error fetching data: {e}")
        return None
