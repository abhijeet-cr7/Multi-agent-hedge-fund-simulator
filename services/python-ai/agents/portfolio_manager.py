from typing import List
from agents.base_agent import BaseAgent, AgentSignal, Signal

SIGNAL_WEIGHTS = {
    Signal.STRONG_BUY: 2.0,
    Signal.BUY: 1.0,
    Signal.HOLD: 0.0,
    Signal.SELL: -1.0,
    Signal.STRONG_SELL: -2.0,
}

AGENT_WEIGHTS = {
    "fundamental": 1.5,
    "technical": 1.2,
    "sentiment": 0.8,
    "risk": 1.3,
    "sector": 0.9,
}


class PortfolioManager(BaseAgent):
    """
    Meta-agent that aggregates signals from all other agents,
    weighs them by confidence and agent type, then produces a final decision.
    """

    def __init__(self):
        super().__init__("portfolio_manager", "reasoning")

    def aggregate(self, signals: List[AgentSignal], symbol: str) -> AgentSignal:
        """Aggregate multiple agent signals into a final portfolio decision."""
        if not signals:
            return AgentSignal(
                agent_type=self.agent_type,
                symbol=symbol,
                signal=Signal.HOLD,
                confidence=0.3,
                reasoning="No agent signals available",
            )

        total_weight = 0.0
        weighted_score = 0.0
        agent_summaries = []

        for sig in signals:
            agent_w = AGENT_WEIGHTS.get(sig.agent_type, 1.0)
            signal_score = SIGNAL_WEIGHTS.get(sig.signal, 0.0)
            weight = agent_w * sig.confidence
            weighted_score += signal_score * weight
            total_weight += weight
            agent_summaries.append(
                f"{sig.agent_type.upper()}: {sig.signal.value} ({sig.confidence:.0%})"
            )

        final_score = weighted_score / total_weight if total_weight > 0 else 0.0

        if final_score >= 1.3:
            signal = Signal.STRONG_BUY
        elif final_score >= 0.5:
            signal = Signal.BUY
        elif final_score >= -0.5:
            signal = Signal.HOLD
        elif final_score >= -1.3:
            signal = Signal.SELL
        else:
            signal = Signal.STRONG_SELL

        avg_confidence = sum(s.confidence for s in signals) / len(signals)
        confidence = min(0.95, avg_confidence * 1.1)  # Slightly boost confidence through aggregation

        summary = " | ".join(agent_summaries)
        reasoning = (
            f"Aggregated decision from {len(signals)} agents. "
            f"Weighted score: {final_score:.2f}. "
            f"Agent signals: {summary}"
        )

        # Use LLM to enhance the final reasoning
        if self.llm:
            prompt = (
                f"You are a portfolio manager for a hedge fund. You have received the following signals for {symbol}:\n"
                f"{summary}\n\n"
                f"The quantitative aggregation gives a weighted score of {final_score:.2f}, "
                f"suggesting a {signal.value} signal.\n\n"
                f"Provide a professional 2-3 sentence investment thesis and final recommendation. "
                f"Include suggested position sizing (e.g., 'Allocate 5-8% of portfolio')."
            )
            llm_reasoning = self._prompt_llm(prompt)
            reasoning = f"{reasoning}\n\nPortfolio Manager Analysis:\n{llm_reasoning}"

        return AgentSignal(
            agent_type=self.agent_type,
            symbol=symbol,
            signal=signal,
            confidence=confidence,
            reasoning=reasoning,
            metadata={
                "weighted_score": final_score,
                "agent_count": len(signals),
                "individual_signals": [
                    {
                        "agent": s.agent_type,
                        "signal": s.signal.value,
                        "confidence": s.confidence,
                    }
                    for s in signals
                ],
            },
        )

    def analyze(self, symbol: str) -> AgentSignal:
        """Run all agents and aggregate their signals."""
        from agents.fundamental_agent import FundamentalAgent
        from agents.technical_agent import TechnicalAgent
        from agents.sentiment_agent import SentimentAgent
        from agents.risk_agent import RiskAgent
        from agents.sector_agent import SectorAgent

        agents = [
            FundamentalAgent(),
            TechnicalAgent(),
            SentimentAgent(),
            RiskAgent(),
            SectorAgent(),
        ]

        signals = []
        for agent in agents:
            try:
                sig = agent.analyze(symbol)
                signals.append(sig)
            except Exception as e:
                print(f"Agent {agent.agent_type} failed for {symbol}: {e}")

        return self.aggregate(signals, symbol)
