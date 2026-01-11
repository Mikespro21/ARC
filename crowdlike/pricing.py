from __future__ import annotations

from dataclasses import dataclass


@dataclass
class PriceQuote:
    agent_count: int
    risk: float
    autonomy: str
    total_per_day: float
    per_agent_per_day: float


def quote_daily(agent_count: int, risk: float, autonomy: str = "assist") -> PriceQuote:
    """Demo pricing: pay-per-day with exponential growth as agents/risk/autonomy increase.

    The master context describes pay-per-day + exponential costs, but doesn't define a formula.
    This is a simple, transparent approximation for the demo UI.
    """
    n = max(1, int(agent_count or 1))
    r = max(0.0, min(100.0, float(risk or 0.0)))

    # Base per-agent/day
    base = 0.10  # 10 cents/day

    # Risk multiplier (gentle but non-linear)
    risk_mult = (1.0 + r / 100.0) ** 1.35

    # Autonomy multiplier
    a = str(autonomy or "assist").lower()
    if a in ("auto", "autopilot"):
        auto_mult = 1.85
    elif a in ("off", "manual"):
        auto_mult = 0.85
    else:
        auto_mult = 1.20

    per_agent = base * risk_mult * auto_mult

    # Exponential scaling with agent count (core idea)
    total = per_agent * (n ** 1.18)

    return PriceQuote(agent_count=n, risk=r, autonomy=a, total_per_day=float(total), per_agent_per_day=float(per_agent))
