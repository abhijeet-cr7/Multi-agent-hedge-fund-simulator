from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import httpx
import logging

from config import settings
from agents.fundamental_agent import FundamentalAgent
from agents.technical_agent import TechnicalAgent
from agents.sentiment_agent import SentimentAgent
from agents.risk_agent import RiskAgent
from agents.sector_agent import SectorAgent
from agents.portfolio_manager import PortfolioManager

logging.basicConfig(level=settings.log_level)
logger = logging.getLogger(__name__)

app = FastAPI(title="Hedge Fund AI Service", version="1.0.0")

AGENTS = {
    "fundamental": FundamentalAgent,
    "technical": TechnicalAgent,
    "sentiment": SentimentAgent,
    "risk": RiskAgent,
    "sector": SectorAgent,
    "portfolio_manager": PortfolioManager,
}


class AnalyzeRequest(BaseModel):
    symbol: str
    agent_type: Optional[str] = "all"


async def post_decision_to_nestjs(decision: dict) -> None:
    """Post an agent decision back to the NestJS callback endpoint."""
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            await client.post(settings.nestjs_callback_url, json=decision)
    except Exception as e:
        logger.warning(f"Failed to post decision to NestJS: {e}")


@app.get("/health")
def health_check():
    return {"status": "ok", "service": "python-ai"}


@app.post("/analyze")
async def analyze_stock(request: AnalyzeRequest):
    symbol = request.symbol.upper()
    agent_type = request.agent_type or "all"

    results = []

    if agent_type == "all":
        # Run all agents and collect individual results
        for name, AgentClass in AGENTS.items():
            if name == "portfolio_manager":
                continue  # Run PM last
            try:
                agent = AgentClass()
                signal = agent.analyze(symbol)
                decision = {
                    "agentType": signal.agent_type,
                    "symbol": signal.symbol,
                    "signal": signal.signal.value,
                    "confidence": signal.confidence,
                    "reasoning": signal.reasoning,
                    "metadata": signal.metadata or {},
                }
                results.append(decision)
                await post_decision_to_nestjs(decision)
            except Exception as e:
                logger.error(f"Agent {name} failed for {symbol}: {e}")

        # Run Portfolio Manager
        try:
            pm = PortfolioManager()
            pm_signal = pm.analyze(symbol)
            pm_decision = {
                "agentType": pm_signal.agent_type,
                "symbol": pm_signal.symbol,
                "signal": pm_signal.signal.value,
                "confidence": pm_signal.confidence,
                "reasoning": pm_signal.reasoning,
                "metadata": pm_signal.metadata or {},
            }
            results.append(pm_decision)
            await post_decision_to_nestjs(pm_decision)
        except Exception as e:
            logger.error(f"Portfolio manager failed for {symbol}: {e}")

    elif agent_type in AGENTS:
        try:
            agent = AGENTS[agent_type]()
            signal = agent.analyze(symbol)
            decision = {
                "agentType": signal.agent_type,
                "symbol": signal.symbol,
                "signal": signal.signal.value,
                "confidence": signal.confidence,
                "reasoning": signal.reasoning,
                "metadata": signal.metadata or {},
            }
            results.append(decision)
            await post_decision_to_nestjs(decision)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Agent analysis failed: {str(e)}")
    else:
        raise HTTPException(
            status_code=400,
            detail=f"Unknown agent type: {agent_type}. Valid: {list(AGENTS.keys())} or 'all'",
        )

    return {"symbol": symbol, "agent_type": agent_type, "decisions": results}


@app.post("/analyze/{agent_type}")
async def analyze_stock_with_agent(agent_type: str, request: AnalyzeRequest):
    request.agent_type = agent_type
    return await analyze_stock(request)
