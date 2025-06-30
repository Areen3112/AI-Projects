import pandas as pd

def generate_analysis_report(predicted_prices, sentiment_summary, technical_signals):
    try:
        if not predicted_prices or len(predicted_prices) < 2:
            raise ValueError("Not enough predicted price data to determine trend.")

        if not isinstance(sentiment_summary, dict):
            raise ValueError("Sentiment summary is invalid.")
        if not isinstance(technical_signals, dict):
            raise ValueError("Technical signals are invalid.")

        trend = "Bullish 📈" if predicted_prices[-1] > predicted_prices[0] else "Bearish 📉"

        sentiment = sentiment_summary.get("overall_sentiment", "Neutral")
        sentiment_text = f"Market sentiment is {sentiment.lower()} based on recent news."

        raw_signal = technical_signals.get("buy", False)
        if isinstance(raw_signal, (pd.Series, pd.DataFrame)):
            raw_signal = raw_signal.iloc[0] if hasattr(raw_signal, 'iloc') else raw_signal.values[0]
        buy_signal = bool(raw_signal)

        tech_signal = f"Technical indicators suggest a {'buy' if buy_signal else 'hold/sell'} signal."

        future_direction = (
            "The stock is likely to go **up** in the short term."
            if trend == "Bullish 📈" else
            "The stock might **decline** in the short term."
        )

        return f"""
### 📊 Analysis Report
**Trend**: {trend}  
**News Sentiment**: {sentiment}  
**Technical Signal**: {tech_signal}  
**Expected Movement**: {future_direction}  

🧠 {sentiment_text}
"""
    except Exception as e:
        return f"❌ Could not generate report: {e}"
