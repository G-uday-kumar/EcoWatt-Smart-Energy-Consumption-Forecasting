import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_energy_data(start_date='2020-01-01', periods=365*2, freq='D'):
    """
    Generate synthetic energy consumption data.
    """
    date_range = pd.date_range(start=start_date, periods=periods, freq=freq)
    np.random.seed(42)  # For reproducibility

    # Base consumption with seasonal and daily patterns
    base_consumption = 100  # kWh
    seasonal_amplitude = 20
    daily_amplitude = 10

    # Seasonal component (yearly cycle)
    seasonal = seasonal_amplitude * np.sin(2 * np.pi * np.arange(periods) / 365)

    # Daily component (weekly cycle)
    daily = daily_amplitude * np.sin(2 * np.pi * np.arange(periods) / 7)

    # Random noise
    noise = np.random.normal(0, 5, periods)

    # Trend (slight increase over time)
    trend = 0.01 * np.arange(periods)

    consumption = base_consumption + seasonal + daily + noise + trend

    # Ensure non-negative values
    consumption = np.maximum(consumption, 0)

    df = pd.DataFrame({
        'date': date_range,
        'consumption_kwh': consumption
    })

    return df

if __name__ == "__main__":
    data = generate_energy_data()
    data.to_csv('energy_data.csv', index=False)
    print("Synthetic energy data generated and saved to energy_data.csv")
