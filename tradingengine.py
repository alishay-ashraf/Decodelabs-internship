import numpy as np
import pandas as pd


def build_trading_engine(df: pd.DataFrame) -> pd.DataFrame:
    """Processes raw OHLC data to map market architectures and identify regime changes.

    Expects a pandas DataFrame with columns: 'Open', 'High', 'Low', 'Close',
    'Volume'
    """
    # Ensure data is sorted chronologically
    df = df.sort_index()

    # --- STEP 1: CANDLESTICK MICROSTRUCTURE ---
    # Candle Body: Sustained market consensus
    df["body"] = (df["Open"] - df["Close"]).abs()

    # Upper Wick: Localized supply overhang
    df["upper_wick"] = df["High"] - df[["Open", "Close"]].max(axis=1)

    # Lower Wick: Localized demand absorption
    df["lower_wick"] = df[["Open", "Close"]].min(axis=1) - df["Low"]

    # Wick-to-Body Ratio (R_wb)
    # Adding a small epsilon (1e-8) to prevent division by zero on perfectly flat candles
    df["R_wb"] = (df["upper_wick"] + df["lower_wick"]) / (df["body"] + 1e-8)

    # --- STEP 2: EXPONENTIAL TREND SMOOTHING ---
    # 50-Day Responsive Smoothing & 200-Day Rigid Trend Boundary
    df["EMA_50"] = df["Close"].ewm(span=50, adjust=False).mean()
    df["EMA_200"] = df["Close"].ewm(span=200, adjust=False).mean()

    # --- STEP 3: SCANNER REGIME LOGIC ---
    # Calculate Average True Range (ATR) for volatility expansion tracking
    high_low = df["High"] - df["Low"]
    high_close_prev = (df["High"] - df["Close"].shift(1)).abs()
    low_close_prev = (df["Low"] - df["Close"].shift(1)).abs()
    tr = pd.concat([high_low, high_close_prev, low_close_prev], axis=1).max(
        axis=1
    )
    df["ATR_14"] = tr.ewm(span=14, adjust=False).mean()

    # Volume benchmarks (1-Month/20 Days vs 1-Year/252 Days)
    df["volume_1m"] = df["Volume"].rolling(window=20).mean()
    df["volume_1y"] = df["Volume"].rolling(window=252).mean()

    # Crossover Signals
    # 1. Golden Cross Criteria
    df["golden_cross"] = (df["EMA_50"] > df["EMA_200"]) & (
        df["volume_1m"] > df["volume_1y"]
    )

    # 2. Death Cross Criteria
    df["death_cross"] = (df["EMA_50"] < df["EMA_200"]) & (
        df["ATR_14"] > df["ATR_14"].shift(1)
    )

    # --- STEP 4: SIGNAL LOGS (TRADING DESK EXECUTIONS) ---
    df["Regime_Signal"] = "Neutral"
    df.loc[df["golden_cross"], "Regime_Signal"] = "Bullish Macro Cycle"
    df.loc[df["death_cross"], "Regime_Signal"] = "Bearish Macro Regime"

    return df


# --- SIMULATION EXAMPLE ---
if __name__ == "__main__":
    # Generating mock market data for verification
    np.random.seed(42)
    dates = pd.date_range(start="2024-01-01", periods=300, freq="D")

    # Generate a random walk price sequence
    close_prices = 100 + np.random.randn(300).cumsum() * 2

    mock_data = pd.DataFrame(
        {
            "Open": close_prices + np.random.randn(300),
            # FIXED: Wrapped the numpy array with np.abs()
            "High": close_prices + np.abs(np.random.randn(300)) + 1,
            "Low": close_prices - np.abs(np.random.randn(300)) - 1,
            "Close": close_prices,
            "Volume": np.random.randint(10000, 50000, size=300),
        },
        index=dates,
    )

    # Run the engine
    processed_tape = build_trading_engine(mock_data)

    print("--- Sample Processing Output ---")
    print(
        processed_tape[
            ["Close", "R_wb", "EMA_50", "EMA_200", "Regime_Signal"]
        ].tail()
    )