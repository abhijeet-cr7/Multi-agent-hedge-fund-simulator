from agents.base_agent import BaseAgent, AgentSignal, Signal
from tools.stock_data import get_historical_data
from tools.technical_indicators import get_all_indicators


class TechnicalAgent(BaseAgent):
    """Analyzes technical indicators to generate trading signals."""

    def __init__(self):
        super().__init__("technical", "fast")

    def analyze(self, symbol: str) -> AgentSignal:
        df = get_historical_data(symbol, period="6mo")

        if df.empty:
            return AgentSignal(
                agent_type=self.agent_type,
                symbol=symbol,
                signal=Signal.HOLD,
                confidence=0.3,
                reasoning=f"Could not fetch price history for {symbol}",
            )

        indicators = get_all_indicators(df)

        if "error" in indicators:
            return AgentSignal(
                agent_type=self.agent_type,
                symbol=symbol,
                signal=Signal.HOLD,
                confidence=0.3,
                reasoning=indicators["error"],
            )

        score = 0.0
        reasons = []

        rsi = indicators["rsi"]
        if rsi < 30:
            score += 2.5
            reasons.append(f"RSI={rsi:.1f} — oversold, strong buy signal")
        elif rsi < 45:
            score += 1.0
            reasons.append(f"RSI={rsi:.1f} — approaching oversold territory")
        elif rsi > 70:
            score -= 2.5
            reasons.append(f"RSI={rsi:.1f} — overbought, consider taking profits")
        elif rsi > 55:
            score -= 0.5
            reasons.append(f"RSI={rsi:.1f} — slightly elevated")
        else:
            reasons.append(f"RSI={rsi:.1f} — neutral range")

        macd = indicators["macd"]
        if macd["histogram"] > 0 and macd["macd"] > macd["signal"]:
            score += 1.5
            reasons.append("MACD bullish crossover — upward momentum")
        elif macd["histogram"] < 0 and macd["macd"] < macd["signal"]:
            score -= 1.5
            reasons.append("MACD bearish crossover — downward momentum")

        bb = indicators["bollinger_bands"]
        price = indicators["current_price"]
        if bb["percent_b"] < 0.1:
            score += 2.0
            reasons.append(f"Price near lower Bollinger Band — potential reversal")
        elif bb["percent_b"] > 0.9:
            score -= 1.5
            reasons.append(f"Price near upper Bollinger Band — overbought")

        sma_20 = indicators["sma_20"]
        sma_50 = indicators["sma_50"]
        sma_200 = indicators["sma_200"]

        if price > sma_20 > sma_50 > sma_200:
            score += 2.0
            reasons.append("Golden cross alignment — strong bullish trend")
        elif price > sma_50 > sma_200:
            score += 1.0
            reasons.append("Price above 50 and 200 SMA — bullish trend")
        elif price < sma_20 < sma_50 < sma_200:
            score -= 2.0
            reasons.append("Death cross alignment — strong bearish trend")
        elif price < sma_50 < sma_200:
            score -= 1.0
            reasons.append("Price below 50 and 200 SMA — bearish trend")

        volume = indicators["volume"]
        if volume["is_high"] and score > 0:
            score += 0.5
            reasons.append(f"High volume ({volume['ratio']:.1f}x average) confirms bullish move")
        elif volume["is_high"] and score < 0:
            score -= 0.5
            reasons.append(f"High volume ({volume['ratio']:.1f}x average) confirms bearish move")

        if score >= 5.0:
            signal, base_conf = Signal.STRONG_BUY, 0.88
        elif score >= 2.5:
            signal, base_conf = Signal.BUY, 0.74
        elif score >= -1.5:
            signal, base_conf = Signal.HOLD, 0.62
        elif score >= -4.0:
            signal, base_conf = Signal.SELL, 0.74
        else:
            signal, base_conf = Signal.STRONG_SELL, 0.88

        reasoning = " | ".join(reasons)

        return AgentSignal(
            agent_type=self.agent_type,
            symbol=symbol,
            signal=signal,
            confidence=self._confidence_from_signal(signal, base_conf),
            reasoning=reasoning,
            metadata={
                "score": score,
                "rsi": rsi,
                "macd": macd,
                "bollinger_bands": bb,
                "sma_20": sma_20,
                "sma_50": sma_50,
                "sma_200": sma_200,
                "current_price": price,
            },
        )
