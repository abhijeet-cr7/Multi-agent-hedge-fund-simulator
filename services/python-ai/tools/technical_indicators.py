import pandas as pd
import numpy as np
from typing import Dict, Any


def calculate_rsi(prices: pd.Series, period: int = 14) -> float:
    """Calculate the Relative Strength Index."""
    if len(prices) < period + 1:
        return 50.0
    delta = prices.diff()
    gain = delta.where(delta > 0, 0).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss.replace(0, 1e-10)
    rsi = 100 - (100 / (1 + rs))
    return float(rsi.iloc[-1]) if not pd.isna(rsi.iloc[-1]) else 50.0


def calculate_macd(prices: pd.Series, fast: int = 12, slow: int = 26, signal: int = 9) -> Dict[str, float]:
    """Calculate MACD, Signal line, and Histogram."""
    ema_fast = prices.ewm(span=fast, adjust=False).mean()
    ema_slow = prices.ewm(span=slow, adjust=False).mean()
    macd_line = ema_fast - ema_slow
    signal_line = macd_line.ewm(span=signal, adjust=False).mean()
    histogram = macd_line - signal_line
    return {
        "macd": float(macd_line.iloc[-1]),
        "signal": float(signal_line.iloc[-1]),
        "histogram": float(histogram.iloc[-1]),
    }


def calculate_bollinger_bands(prices: pd.Series, period: int = 20, std_dev: float = 2.0) -> Dict[str, float]:
    """Calculate Bollinger Bands (upper, middle, lower)."""
    sma = prices.rolling(window=period).mean()
    std = prices.rolling(window=period).std()
    upper = sma + std_dev * std
    lower = sma - std_dev * std
    current_price = float(prices.iloc[-1])
    current_upper = float(upper.iloc[-1]) if not pd.isna(upper.iloc[-1]) else current_price
    current_lower = float(lower.iloc[-1]) if not pd.isna(lower.iloc[-1]) else current_price
    current_middle = float(sma.iloc[-1]) if not pd.isna(sma.iloc[-1]) else current_price
    band_width = current_upper - current_lower
    percent_b = (current_price - current_lower) / band_width if band_width > 0 else 0.5
    return {
        "upper": current_upper,
        "middle": current_middle,
        "lower": current_lower,
        "percent_b": percent_b,
        "bandwidth": band_width / current_middle if current_middle > 0 else 0,
    }


def calculate_sma(prices: pd.Series, period: int) -> float:
    """Calculate Simple Moving Average."""
    if len(prices) < period:
        return float(prices.mean())
    return float(prices.rolling(window=period).mean().iloc[-1])


def calculate_ema(prices: pd.Series, period: int) -> float:
    """Calculate Exponential Moving Average."""
    return float(prices.ewm(span=period, adjust=False).mean().iloc[-1])


def calculate_atr(high: pd.Series, low: pd.Series, close: pd.Series, period: int = 14) -> float:
    """Calculate Average True Range."""
    tr1 = high - low
    tr2 = (high - close.shift(1)).abs()
    tr3 = (low - close.shift(1)).abs()
    tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
    atr = tr.rolling(window=period).mean()
    return float(atr.iloc[-1]) if not pd.isna(atr.iloc[-1]) else 0.0


def calculate_volume_analysis(volume: pd.Series, period: int = 20) -> Dict[str, float]:
    """Analyze volume trends."""
    avg_volume = float(volume.rolling(window=period).mean().iloc[-1])
    current_volume = float(volume.iloc[-1])
    volume_ratio = current_volume / avg_volume if avg_volume > 0 else 1.0
    return {
        "current": current_volume,
        "average": avg_volume,
        "ratio": volume_ratio,
        "is_high": volume_ratio > 1.5,
    }


def get_all_indicators(df: pd.DataFrame) -> Dict[str, Any]:
    """Calculate all technical indicators for a given OHLCV DataFrame."""
    if df.empty or len(df) < 30:
        return {"error": "Insufficient data for technical analysis"}

    close = df["Close"]
    high = df["High"]
    low = df["Low"]
    volume = df["Volume"]

    return {
        "rsi": calculate_rsi(close),
        "macd": calculate_macd(close),
        "bollinger_bands": calculate_bollinger_bands(close),
        "sma_20": calculate_sma(close, 20),
        "sma_50": calculate_sma(close, 50),
        "sma_200": calculate_sma(close, 200),
        "ema_20": calculate_ema(close, 20),
        "ema_50": calculate_ema(close, 50),
        "atr": calculate_atr(high, low, close),
        "volume": calculate_volume_analysis(volume),
        "current_price": float(close.iloc[-1]),
        "price_change_pct": float((close.iloc[-1] - close.iloc[-2]) / close.iloc[-2] * 100) if len(close) > 1 else 0,
    }
