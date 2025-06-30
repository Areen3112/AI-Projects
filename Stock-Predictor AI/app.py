import streamlit as st
import pandas as pd
from collections import Counter
from utils.data_loader import fetch_stock_data
from utils.lstm_predictor import prepare_data, build_lstm_model, predict_features
from utils.sentiment import analyze_sentiments
from utils.investment_recommender import calculate_investment_recommendation
from utils.news_scraper import get_company_news
from utils.analysis import generate_analysis_report

st.set_page_config(page_title="📈 Stock Scope AI", layout="wide")

st.title("📊 Stock Scope AI")
st.markdown("An AI-powered tool for analyzing stocks with predictions, news sentiment, and recommendations.")

# --- Sidebar Inputs ---
# 🧠 Improved handling of Indian and global tickers
def resolve_ticker(ticker_input):
    known_us_tickers = {
  "NVDA", "MSFT", "AAPL", "AMZN", "GOOG", "META", "2222", "AVGO", "BRK.A", "TSLACO", "TSLA", "2330", "JPM", "WMT", "LLY", "V", "700", "ORCL", "NFLX", "MA", "XOM", "COST", "PG", "HD", "JNJ", "BAC", "SAP", "601398", "ABBV", "ASML", "PLTR", "NOVO_B", "KO", "005930", "601288", "PM", "UNH", "RMS", "601939", "BABA", "CSCO", "GE", "IBM", "TMUS", "RO", "MC", "CRM", "WFC", "CVX", "NESN", "600519", "600941", "RELIANCE", "IHC", "ABT", "AMD", "NOVN", "7203", "MS", "AXP", "OR", "DIS", "LIN", "AZN", "INTU", "601988", "601857", "GS", "HSBA", "NOW", "SHEL", "MCD", "SIE", "CBA", "T", "ACN", "MRK", "1810", "RTX", "UBER", "ISRG", "TXN", "BKNG", "BX", "RY", "DTE", "CAT", "HDFCBANK", "PEP", "VZ", "ARM", "QCOM", "AIR", "600036", "ADBE", "SCHW", "BLK", "BA", "ITX", "300750"
}

    
    if '.' in ticker_input:
        return ticker_input  # Already a resolved ticker like RELIANCE.NS or AAPL
    elif ticker_input in known_us_tickers:
        return ticker_input  # Global ticker, no change
    else:
        return f"{ticker_input}.NS"  # Assume Indian NSE stock

ticker = resolve_ticker(st.text_input("Enter Stock Ticker (e.g., AAPL, MSFT, RELIANCE):", value="AAPL").upper())


start_date = st.sidebar.date_input("Start Date", value=None)
end_date = st.sidebar.date_input("End Date", value=None)
submit = st.sidebar.button("Run Analysis")

if submit:
    try:
        df = fetch_stock_data(ticker, str(start_date), str(end_date))
        if df is None or df.empty or 'Close' not in df.columns:
            st.error("⚠️ No data found for this ticker and date range. Please check your input (e.g., use RELIANCE.NS).")
            st.stop()
        else:
            st.subheader("📈 Historical Price Data")
            st.line_chart(df.set_index("Date")["Close"])

            # --- Price Prediction ---
            st.subheader("📉 LSTM Future Stock Prediction")
            X, y, scaler = prepare_data(df)
            model = build_lstm_model(X.shape[1:])
            model.fit(X, y, epochs=5, batch_size=16, verbose=0)

            future_prices = predict_features(df, feature="Close")
            st.write("🔮 Next 5 Predicted Closing Prices:")
            st.write(future_prices)

            # --- Investment Recommendation ---
            st.subheader("💰 Investment Recommendation")
            recommendation = calculate_investment_recommendation(future_prices)
            amount = recommendation['amount']
            expected_return = float(recommendation['expected_return'])
            risk_level = recommendation['risk_level']

            investment_summary = f"""
            ### 📌 Suggested Strategy:
            Based on the predicted stock trend over the next 30 days:

            - ✅ **Suggested Investment**: ₹{amount:,.0f}
            - 📈 **Expected Return**: ~₹{expected_return:,.2f} (estimated)
            - 🧠 **Risk Profile**: {risk_level}

            ---

            ### 🔍 Rationale:
            The LSTM model indicates a potential upward trend, supported by recent historical volatility and news sentiment.

            - Volatility appears to be within moderate range for short-term entry.
            - Sentiment analysis shows {risk_level.lower()} investor confidence.
            - This recommendation assumes a **short-term trading** approach (not long-term value investing).

            > ℹ️ Disclaimer: This is not financial advice. Always consider your risk appetite and consult a certified financial advisor.
            """
            st.markdown(investment_summary, unsafe_allow_html=True)

            # --- News Sentiment Analysis ---
            st.subheader("📰 News Sentiment Analysis")
            sentiment_summary = {"overall_sentiment": "Neutral"}

            try:
                news_list = get_company_news(ticker)
                if news_list:
                    descriptions = [article["description"] for article in news_list if isinstance(article, dict) and "description" in article]
                    sentiments = analyze_sentiments(news_list)
                    labels = [s["label"] for s in sentiments if isinstance(s, dict) and "label" in s]

                    if labels:
                        counts = Counter(labels)
                        overall = max(counts, key=counts.get)
                        sentiment_summary["overall_sentiment"] = overall

                    for article in news_list:
                        if isinstance(article, dict):
                            st.markdown(f"**🔹 [{article.get('title', 'No Title')}]({article.get('url', '#')})**")
                            st.caption(article.get("description", "No Description"))
                            st.markdown("---")
                else:
                    st.warning("⚠️ No recent news found for this stock.")
            except Exception as e:
                st.error(f"❌ Error occurred: {e}")

            # --- Company Analysis Report ---
            st.subheader("📄 Company Analysis Report")
            try:
                ma_signal = (df['Close'].rolling(window=5).mean() > df['Close'].rolling(window=10).mean())
                technical_signals = {
                    "buy": ma_signal.iloc[-1]
                }
                report = generate_analysis_report(
                    predicted_prices=future_prices,
                    sentiment_summary=sentiment_summary,
                    technical_signals=technical_signals
                )
                st.markdown(report)
            except Exception as e:
                st.error(f"❌ Error generating report: {e}")

    except Exception as e:
        st.error(f"❌ Error occurred: {e}")
