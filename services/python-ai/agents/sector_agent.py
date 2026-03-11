from agents.base_agent import BaseAgent, AgentSignal, Signal
from tools.stock_data import get_stock_info, get_historical_data


SECTOR_ETFS = {
    "Technology": "XLK",
    "Financial Services": "XLF",
    "Healthcare": "XLV",
    "Consumer Cyclical": "XLY",
    "Consumer Defensive": "XLP",
    "Energy": "XLE",
    "Industrials": "XLI",
    "Basic Materials": "XLB",
    "Real Estate": "XLRE",
    "Utilities": "XLU",
    "Communication Services": "XLC",
}


class SectorAgent(BaseAgent):
    """Analyzes sector rotation and relative strength vs sector peers."""

    def __init__(self):
        super().__init__("sector", "fast")

    def analyze(self, symbol: str) -> AgentSignal:
        info = get_stock_info(symbol)
        sector = info.get("sector", "Unknown")

        reasons = []
        score = 0.0

        sector_etf = SECTOR_ETFS.get(sector)
        if sector_etf:
            stock_df = get_historical_data(symbol, period="3mo")
            sector_df = get_historical_data(sector_etf, period="3mo")

            if not stock_df.empty and not sector_df.empty:
                stock_return = float(
                    (stock_df["Close"].iloc[-1] - stock_df["Close"].iloc[0]) / stock_df["Close"].iloc[0]
                )
                sector_return = float(
                    (sector_df["Close"].iloc[-1] - sector_df["Close"].iloc[0]) / sector_df["Close"].iloc[0]
                )

                relative_strength = stock_return - sector_return

                if relative_strength > 0.1:
                    score += 2.5
                    reasons.append(
                        f"Strong outperformance vs {sector} ETF ({sector_etf}): "
                        f"{symbol} +{stock_return:.1%} vs sector +{sector_return:.1%}"
                    )
                elif relative_strength > 0.03:
                    score += 1.0
                    reasons.append(
                        f"Slight outperformance vs {sector} sector: "
                        f"{relative_strength:+.1%}"
                    )
                elif relative_strength < -0.1:
                    score -= 2.5
                    reasons.append(
                        f"Significant underperformance vs {sector} ETF ({sector_etf}): "
                        f"{symbol} {stock_return:.1%} vs sector {sector_return:.1%}"
                    )
                elif relative_strength < -0.03:
                    score -= 1.0
                    reasons.append(
                        f"Underperformance vs {sector} sector: {relative_strength:+.1%}"
                    )
                else:
                    reasons.append(f"In line with {sector} sector performance")

                # Sector momentum (3-month sector return)
                if sector_return > 0.08:
                    score += 1.0
                    reasons.append(f"Sector {sector} in strong uptrend ({sector_return:.1%} in 3mo)")
                elif sector_return < -0.08:
                    score -= 1.0
                    reasons.append(f"Sector {sector} in downtrend ({sector_return:.1%} in 3mo)")
            else:
                reasons.append(f"Sector: {sector} (ETF data unavailable)")
        else:
            reasons.append(f"Sector: {sector} (no benchmark ETF mapped)")

        if score >= 3.0:
            signal, base_conf = Signal.STRONG_BUY, 0.80
        elif score >= 1.0:
            signal, base_conf = Signal.BUY, 0.68
        elif score >= -1.0:
            signal, base_conf = Signal.HOLD, 0.58
        elif score >= -3.0:
            signal, base_conf = Signal.SELL, 0.68
        else:
            signal, base_conf = Signal.STRONG_SELL, 0.80

        return AgentSignal(
            agent_type=self.agent_type,
            symbol=symbol,
            signal=signal,
            confidence=self._confidence_from_signal(signal, base_conf),
            reasoning=" | ".join(reasons),
            metadata={
                "sector": sector,
                "sector_etf": sector_etf,
                "score": score,
            },
        )
