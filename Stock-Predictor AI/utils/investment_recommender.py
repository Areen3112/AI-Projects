# utils/investment.py
import numpy as np

def calculate_investment_recommendation(predictions):
    if predictions is None or len(predictions) == 0:
        return {
            "amount": "N/A",
            "expected_return": "N/A",
            "risk_level": "Unknown"
        }

    # Get the last predicted value
    latest = predictions[-1]
    
    # If it's an array (e.g. [[128.23]]), extract the float
    if isinstance(latest, (np.ndarray, list)):
        latest_price = float(latest[0])
    else:
        latest_price = float(latest)

    investment_amount = 10000  # Default investment
    expected_return = np.round(latest_price * 1.05, 2)  # 5% return

    risk = "Medium" if latest_price > 200 else "Low"

    return {
        "amount": investment_amount,
        "expected_return": expected_return,
        "risk_level": risk
    }
