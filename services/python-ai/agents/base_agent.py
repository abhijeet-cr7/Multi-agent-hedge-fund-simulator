from abc import ABC, abstractmethod
from typing import Optional, Dict, Any
from dataclasses import dataclass
from enum import Enum

from llm_router import route_llm


class Signal(str, Enum):
    STRONG_BUY = "STRONG_BUY"
    BUY = "BUY"
    HOLD = "HOLD"
    SELL = "SELL"
    STRONG_SELL = "STRONG_SELL"


@dataclass
class AgentSignal:
    agent_type: str
    symbol: str
    signal: Signal
    confidence: float
    reasoning: str
    metadata: Optional[Dict[str, Any]] = None


class BaseAgent(ABC):
    """Abstract base class for all hedge fund analysis agents."""

    def __init__(self, agent_type: str, llm_task_type: str = "default"):
        self.agent_type = agent_type
        self.llm = route_llm(llm_task_type)

    @abstractmethod
    def analyze(self, symbol: str) -> AgentSignal:
        """Analyze a stock and return a signal."""
        pass

    def _prompt_llm(self, prompt: str) -> str:
        """Send a prompt to the LLM and return the response."""
        if self.llm is None:
            return "LLM not available. Using rule-based analysis only."
        try:
            from langchain.schema import HumanMessage
            response = self.llm.invoke([HumanMessage(content=prompt)])
            return response.content
        except Exception as e:
            return f"LLM error: {str(e)}"

    def _confidence_from_signal(self, signal: Signal, base_confidence: float) -> float:
        """Adjust confidence based on signal strength."""
        multipliers = {
            Signal.STRONG_BUY: 1.0,
            Signal.BUY: 0.85,
            Signal.HOLD: 0.7,
            Signal.SELL: 0.85,
            Signal.STRONG_SELL: 1.0,
        }
        return min(1.0, base_confidence * multipliers[signal])
