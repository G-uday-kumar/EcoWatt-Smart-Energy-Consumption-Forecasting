import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import joblib
import os

def prepare_data(df, lag_days=7):
    """
    Prepare data for time series forecasting by creating lag features.
    """
    df = df.copy()
    df['date'] = pd.to_datetime(df['date'])
    df = df.set_index('date')

    # Create lag features
    for i in range(1, lag_days + 1):
        df[f'lag_{i}'] = df['consumption_kwh'].shift(i)

    # Drop rows with NaN values
    df = df.dropna()

    # Features and target
    X = df[[f'lag_{i}' for i in range(1, lag_days + 1)]]
    y = df['consumption_kwh']

    return X, y

def train_model(X_train, y_train):
    """
    Train a linear regression model.
    """
    model = LinearRegression()
    model.fit(X_train, y_train)
    return model

def predict_future(model, last_known_data, days_ahead=30, lag_days=7):
    """
    Predict future energy consumption.
    """
    predictions = []
    current_data = last_known_data.copy()

    for _ in range(days_ahead):
        # Prepare features for prediction
        features = np.array([current_data[-lag_days:]])
        pred = model.predict(features)[0]
        predictions.append(pred)

        # Update current data with prediction
        current_data = np.append(current_data[1:], pred)

    return predictions

def save_model(model, filename='energy_model.pkl'):
    """
    Save the trained model.
    """
    joblib.dump(model, filename)

def load_model(filename='energy_model.pkl'):
    """
    Load a trained model.
    """
    if os.path.exists(filename):
        return joblib.load(filename)
    else:
        return None

if __name__ == "__main__":
    # Load data
    data = pd.read_csv('energy_data.csv')

    # Prepare data
    X, y = prepare_data(data)

    # Split into train and test (80-20)
    split_idx = int(len(X) * 0.8)
    X_train, X_test = X[:split_idx], X[split_idx:]
    y_train, y_test = y[:split_idx], y[split_idx:]

    # Train model
    model = train_model(X_train, y_train)

    # Evaluate
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    print(f"Mean Squared Error: {mse:.2f}")

    # Save model
    save_model(model)
    print("Model trained and saved.")
