import numpy as np
from agents.base_agent import BaseAgent, AgentSignal, Signal
from tools.stock_data import get_historical_data, get_stock_info


class RiskAgent(BaseAgent):
    """Calculates risk metrics: VaR, Sharpe ratio, max drawdown, beta."""

    def __init__(self):
        super().__init__("risk", "fast")

    def analyze(self, symbol: str) -> AgentSignal:
        df = get_historical_data(symbol, period="1y")
        info = get_stock_info(symbol)

        if df.empty:
            return AgentSignal(
                agent_type=self.agent_type,
                symbol=symbol,
                signal=Signal.HOLD,
                confidence=0.3,
                reasoning=f"Could not fetch data for risk analysis of {symbol}",
            )

        close = df["Close"]
        returns = close.pct_change().dropna()

        # Value at Risk (95% confidence)
        var_95 = float(np.percentile(returns, 5))

        # Sharpe Ratio (annualized, assuming risk-free rate of 5%)
        risk_free_daily = 0.05 / 252
        excess_returns = returns - risk_free_daily
        sharpe = float(excess_returns.mean() / excess_returns.std() * np.sqrt(252)) if excess_returns.std() > 0 else 0.0

        # Maximum Drawdown
        cumulative = (1 + returns).cumprod()
        rolling_max = cumulative.expanding().max()
        drawdown = (cumulative - rolling_max) / rolling_max
        max_drawdown = float(drawdown.min())

        # Volatility (annualized)
        volatility = float(returns.std() * np.sqrt(252))

        # Beta from stock info
        beta = info.get("beta") or 1.0

        reasons = []
        score = 0.0

        if var_95 < -0.05:
            score -= 2.0
            reasons.append(f"High daily VaR at 95% confidence: {var_95:.1%}")
        elif var_95 < -0.03:
            score -= 1.0
            reasons.append(f"Moderate VaR: {var_95:.1%}")
        else:
            score += 0.5
            reasons.append(f"Acceptable VaR: {var_95:.1%}")

        if sharpe > 1.5:
            score += 2.0
            reasons.append(f"Excellent Sharpe ratio: {sharpe:.2f}")
        elif sharpe > 0.8:
            score += 1.0
            reasons.append(f"Good Sharpe ratio: {sharpe:.2f}")
        elif sharpe < 0:
            score -= 2.0
            reasons.append(f"Negative Sharpe ratio: {sharpe:.2f} — risk not being rewarded")
        else:
            reasons.append(f"Below-average Sharpe ratio: {sharpe:.2f}")

        if max_drawdown < -0.4:
            score -= 2.0
            reasons.append(f"Severe max drawdown: {max_drawdown:.1%}")
        elif max_drawdown < -0.2:
            score -= 1.0
            reasons.append(f"Significant max drawdown: {max_drawdown:.1%}")
        else:
            score += 0.5
            reasons.append(f"Manageable max drawdown: {max_drawdown:.1%}")

        if volatility > 0.5:
            score -= 1.5
            reasons.append(f"Extremely high annual volatility: {volatility:.1%}")
        elif volatility > 0.3:
            score -= 0.5
            reasons.append(f"High annual volatility: {volatility:.1%}")
        else:
            score += 0.5
            reasons.append(f"Moderate annual volatility: {volatility:.1%}")

        # Risk agent rarely gives strong buy — it flags risks or clears them
        if score >= 2.0:
            signal, base_conf = Signal.BUY, 0.70
        elif score >= 0:
            signal, base_conf = Signal.HOLD, 0.62
        elif score >= -2.0:
            signal, base_conf = Signal.SELL, 0.68
        else:
            signal, base_conf = Signal.STRONG_SELL, 0.78

        reasoning = " | ".join(reasons)

        return AgentSignal(
            agent_type=self.agent_type,
            symbol=symbol,
            signal=signal,
            confidence=self._confidence_from_signal(signal, base_conf),
            reasoning=reasoning,
            metadata={
                "var_95": var_95,
                "sharpe_ratio": sharpe,
                "max_drawdown": max_drawdown,
                "annual_volatility": volatility,
                "beta": beta,
                "score": score,
            },
        )
