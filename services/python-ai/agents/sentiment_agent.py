from agents.base_agent import BaseAgent, AgentSignal, Signal
from tools.stock_data import get_stock_info


class SentimentAgent(BaseAgent):
    """Analyzes market sentiment using LLM reasoning and available data."""

    def __init__(self):
        super().__init__("sentiment", "reasoning")

    def analyze(self, symbol: str) -> AgentSignal:
        info = get_stock_info(symbol)

        if "error" in info:
            return AgentSignal(
                agent_type=self.agent_type,
                symbol=symbol,
                signal=Signal.HOLD,
                confidence=0.3,
                reasoning=f"Could not fetch data for {symbol}",
            )

        sector = info.get("sector", "Unknown")
        name = info.get("name", symbol)

        # Use LLM for sentiment analysis based on sector and company context
        if self.llm:
            prompt = (
                f"You are a market sentiment analyst. Analyze the current market sentiment for {name} ({symbol}).\n"
                f"Sector: {sector}\n"
                f"Current Price: ${info.get('price', 'N/A')}\n"
                f"52-week High: ${info.get('52w_high', 'N/A')}, Low: ${info.get('52w_low', 'N/A')}\n\n"
                f"Based on general market knowledge:\n"
                f"1. What is the overall market sentiment toward this stock/sector?\n"
                f"2. Are there any notable trends or concerns?\n"
                f"3. Provide a sentiment signal: STRONG_BUY, BUY, HOLD, SELL, or STRONG_SELL\n"
                f"4. Provide a confidence score 0.0-1.0\n\n"
                f"Respond in this exact format:\n"
                f"SIGNAL: <signal>\n"
                f"CONFIDENCE: <score>\n"
                f"REASONING: <2-3 sentences>\n"
            )

            llm_response = self._prompt_llm(prompt)

            # Parse LLM response
            signal = Signal.HOLD
            confidence = 0.55
            reasoning = llm_response

            for line in llm_response.split("\n"):
                if line.startswith("SIGNAL:"):
                    signal_str = line.replace("SIGNAL:", "").strip()
                    try:
                        signal = Signal(signal_str)
                    except ValueError:
                        signal = Signal.HOLD
                elif line.startswith("CONFIDENCE:"):
                    try:
                        confidence = float(line.replace("CONFIDENCE:", "").strip())
                    except ValueError:
                        confidence = 0.55
                elif line.startswith("REASONING:"):
                    reasoning = line.replace("REASONING:", "").strip()

            return AgentSignal(
                agent_type=self.agent_type,
                symbol=symbol,
                signal=signal,
                confidence=min(1.0, max(0.0, confidence)),
                reasoning=reasoning,
                metadata={"sector": sector, "llm_analysis": True},
            )

        # Fallback: rule-based sentiment based on price position
        price = info.get("price")
        high_52w = info.get("52w_high")
        low_52w = info.get("52w_low")

        if price and high_52w and low_52w and high_52w > low_52w:
            pct_from_low = (price - low_52w) / (high_52w - low_52w)
            if pct_from_low > 0.85:
                signal = Signal.SELL
                reasoning = f"{symbol} trading near 52-week high — momentum may be fading"
                confidence = 0.55
            elif pct_from_low < 0.2:
                signal = Signal.BUY
                reasoning = f"{symbol} trading near 52-week low — potential value opportunity"
                confidence = 0.55
            else:
                signal = Signal.HOLD
                reasoning = f"{symbol} trading in mid-range — neutral sentiment"
                confidence = 0.45
        else:
            signal = Signal.HOLD
            reasoning = "Insufficient data for sentiment analysis"
            confidence = 0.35

        return AgentSignal(
            agent_type=self.agent_type,
            symbol=symbol,
            signal=signal,
            confidence=confidence,
            reasoning=reasoning,
            metadata={"sector": sector},
        )
