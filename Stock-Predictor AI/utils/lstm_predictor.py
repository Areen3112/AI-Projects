import numpy as np
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense

def prepare_data(df, feature='Close', look_back=30):
    values = df[[feature]].values
    if len(values) <= look_back:
        return None, None, None  # not enough data
    scaler = MinMaxScaler()
    scaled = scaler.fit_transform(values)

    X, y = [], []
    for i in range(look_back, len(scaled)):
        X.append(scaled[i - look_back:i])
        y.append(scaled[i])
    return np.array(X), np.array(y), scaler

def build_lstm_model(input_shape):
    model = Sequential()
    model.add(LSTM(50, return_sequences=True, input_shape=input_shape))
    model.add(LSTM(50))
    model.add(Dense(1))
    model.compile(optimizer='adam', loss='mse')
    return model

def predict_features(df, feature='Close', look_back=30, steps=5):
    try:
        values = df[[feature]].values
        if len(values) < look_back:
            return ["❌ Not enough data to predict future prices."]

        # Scale values
        scaler = MinMaxScaler()
        values_scaled = scaler.fit_transform(values)

        # Prepare last sequence for prediction
        last_sequence = values_scaled[-look_back:].reshape(1, look_back, 1)

        # Build and train model
        model = build_lstm_model((look_back, 1))
        X, y, _ = prepare_data(df, feature, look_back)
        if X is None or len(X) == 0:
            return ["❌ Insufficient data to train the model."]
        model.fit(X, y, epochs=10, verbose=0)

        # Predict multiple future values
        predictions = []
        for _ in range(steps):
            next_value = model.predict(last_sequence)[0][0]
            predictions.append(scaler.inverse_transform([[next_value]])[0][0])
            last_sequence = np.append(last_sequence[:, 1:, :], [[[next_value]]], axis=1)

        return predictions

    except Exception as e:
        return [f"❌ Error during prediction: {str(e)}"]
