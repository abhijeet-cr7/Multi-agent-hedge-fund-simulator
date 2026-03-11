from agents.base_agent import BaseAgent, AgentSignal, Signal
from tools.stock_data import get_stock_info, get_financial_statements


class FundamentalAgent(BaseAgent):
    """Analyzes fundamental financial metrics to generate investment signals."""

    def __init__(self):
        super().__init__("fundamental", "accurate")

    def analyze(self, symbol: str) -> AgentSignal:
        info = get_stock_info(symbol)
        financials = get_financial_statements(symbol)

        if "error" in info:
            return AgentSignal(
                agent_type=self.agent_type,
                symbol=symbol,
                signal=Signal.HOLD,
                confidence=0.3,
                reasoning=f"Could not fetch data for {symbol}: {info.get('error')}",
            )

        # Score-based fundamental analysis
        score = 0.0
        reasons = []

        pe_ratio = info.get("pe_ratio")
        if pe_ratio is not None:
            if pe_ratio < 15:
                score += 2.0
                reasons.append(f"Low P/E ratio ({pe_ratio:.1f}) suggests undervaluation")
            elif pe_ratio < 25:
                score += 1.0
                reasons.append(f"Moderate P/E ratio ({pe_ratio:.1f})")
            elif pe_ratio < 40:
                score -= 0.5
                reasons.append(f"Elevated P/E ratio ({pe_ratio:.1f}) suggests premium pricing")
            else:
                score -= 2.0
                reasons.append(f"High P/E ratio ({pe_ratio:.1f}) indicates overvaluation risk")

        forward_pe = info.get("forward_pe")
        if forward_pe is not None and pe_ratio is not None and forward_pe < pe_ratio:
            score += 1.0
            reasons.append(f"Forward P/E ({forward_pe:.1f}) below trailing P/E — earnings growth expected")

        beta = info.get("beta")
        if beta is not None:
            if beta < 0.8:
                score += 0.5
                reasons.append(f"Low beta ({beta:.2f}) — defensive stock")
            elif beta > 1.5:
                score -= 0.5
                reasons.append(f"High beta ({beta:.2f}) — volatile stock")

        net_income = financials.get("net_income", 0)
        total_revenue = financials.get("total_revenue", 0)
        if total_revenue > 0 and net_income > 0:
            margin = net_income / total_revenue
            if margin > 0.2:
                score += 1.5
                reasons.append(f"Strong profit margin ({margin:.1%})")
            elif margin > 0.1:
                score += 0.5
                reasons.append(f"Healthy profit margin ({margin:.1%})")
            elif margin < 0:
                score -= 2.0
                reasons.append(f"Negative profit margin — company is losing money")

        total_debt = financials.get("total_debt", 0)
        total_assets = financials.get("total_assets", 0)
        if total_assets > 0:
            debt_ratio = total_debt / total_assets
            if debt_ratio < 0.3:
                score += 1.0
                reasons.append(f"Low debt ratio ({debt_ratio:.1%}) — strong balance sheet")
            elif debt_ratio > 0.7:
                score -= 1.5
                reasons.append(f"High debt ratio ({debt_ratio:.1%}) — leverage risk")

        free_cash_flow = financials.get("free_cash_flow", 0)
        if free_cash_flow > 0:
            score += 1.0
            reasons.append(f"Positive free cash flow (${free_cash_flow / 1e9:.2f}B)")
        elif free_cash_flow < 0:
            score -= 1.0
            reasons.append(f"Negative free cash flow")

        # Determine signal and confidence
        if score >= 4.0:
            signal, base_conf = Signal.STRONG_BUY, 0.85
        elif score >= 2.0:
            signal, base_conf = Signal.BUY, 0.72
        elif score >= -1.0:
            signal, base_conf = Signal.HOLD, 0.60
        elif score >= -3.0:
            signal, base_conf = Signal.SELL, 0.72
        else:
            signal, base_conf = Signal.STRONG_SELL, 0.85

        reasoning = " | ".join(reasons) if reasons else "Insufficient fundamental data."

        # Enhance reasoning with LLM if available
        if self.llm:
            llm_prompt = (
                f"You are a fundamental analyst. For {symbol}, the quantitative analysis shows:\n"
                f"Score: {score:.1f}, Signal: {signal.value}\n"
                f"Key factors: {reasoning}\n"
                f"P/E: {pe_ratio}, Beta: {beta}, Profit Margin: {(net_income/total_revenue*100):.1f}% (if applicable)\n"
                f"Provide a concise 2-sentence professional investment opinion."
            )
            llm_reasoning = self._prompt_llm(llm_prompt)
            reasoning = f"{reasoning}\n\nLLM Analysis: {llm_reasoning}"

        return AgentSignal(
            agent_type=self.agent_type,
            symbol=symbol,
            signal=signal,
            confidence=self._confidence_from_signal(signal, base_conf),
            reasoning=reasoning,
            metadata={
                "score": score,
                "pe_ratio": pe_ratio,
                "beta": beta,
                "net_income": net_income,
                "total_revenue": total_revenue,
                "free_cash_flow": free_cash_flow,
            },
        )
