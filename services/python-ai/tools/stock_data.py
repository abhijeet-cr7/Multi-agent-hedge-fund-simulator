import yfinance as yf
import pandas as pd
from typing import Dict, Any, Optional


def get_stock_info(symbol: str) -> Dict[str, Any]:
    """Fetch current stock information from Yahoo Finance."""
    try:
        ticker = yf.Ticker(symbol)
        info = ticker.info
        return {
            "symbol": symbol,
            "name": info.get("longName", symbol),
            "price": info.get("currentPrice") or info.get("regularMarketPrice"),
            "open": info.get("open"),
            "high": info.get("dayHigh"),
            "low": info.get("dayLow"),
            "volume": info.get("volume"),
            "market_cap": info.get("marketCap"),
            "pe_ratio": info.get("trailingPE"),
            "eps": info.get("trailingEps"),
            "forward_pe": info.get("forwardPE"),
            "dividend_yield": info.get("dividendYield"),
            "52w_high": info.get("fiftyTwoWeekHigh"),
            "52w_low": info.get("fiftyTwoWeekLow"),
            "beta": info.get("beta"),
            "sector": info.get("sector"),
            "industry": info.get("industry"),
        }
    except Exception as e:
        return {"symbol": symbol, "error": str(e)}


def get_historical_data(symbol: str, period: str = "3mo", interval: str = "1d") -> pd.DataFrame:
    """Fetch historical OHLCV data for a stock."""
    try:
        ticker = yf.Ticker(symbol)
        df = ticker.history(period=period, interval=interval)
        df.reset_index(inplace=True)
        return df
    except Exception as e:
        return pd.DataFrame()


def get_financial_statements(symbol: str) -> Dict[str, Any]:
    """Fetch financial statements for fundamental analysis."""
    try:
        ticker = yf.Ticker(symbol)
        income_stmt = ticker.income_stmt
        balance_sheet = ticker.balance_sheet
        cash_flow = ticker.cash_flow

        result: Dict[str, Any] = {}

        if income_stmt is not None and not income_stmt.empty:
            latest = income_stmt.iloc[:, 0]
            result["total_revenue"] = float(latest.get("Total Revenue", 0) or 0)
            result["gross_profit"] = float(latest.get("Gross Profit", 0) or 0)
            result["net_income"] = float(latest.get("Net Income", 0) or 0)
            result["ebit"] = float(latest.get("EBIT", 0) or 0)

        if balance_sheet is not None and not balance_sheet.empty:
            latest = balance_sheet.iloc[:, 0]
            result["total_assets"] = float(latest.get("Total Assets", 0) or 0)
            result["total_debt"] = float(latest.get("Total Debt", 0) or 0)
            result["cash"] = float(latest.get("Cash And Cash Equivalents", 0) or 0)

        if cash_flow is not None and not cash_flow.empty:
            latest = cash_flow.iloc[:, 0]
            result["free_cash_flow"] = float(latest.get("Free Cash Flow", 0) or 0)
            result["operating_cash_flow"] = float(latest.get("Operating Cash Flow", 0) or 0)

        return result
    except Exception as e:
        return {"error": str(e)}
