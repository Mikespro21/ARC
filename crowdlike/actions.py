from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List, Optional

import streamlit as st

from .mock import calculate_pricing
from .state import recompute_metrics


def create_agent(name: str, strategy_type: str, riskness: int, initial_balance: float) -> None:
    user = st.session_state["user"]
    agents: List[Dict[str, Any]] = st.session_state["agents"]

    if len(agents) >= user["settings"]["maxAgents"]:
        st.warning(f"Maximum {user['settings']['maxAgents']} agents allowed.")
        return

    if user["usdcBalance"] < initial_balance:
        st.warning("Insufficient USDC balance.")
        return

    agent_id = f"agent_{int(datetime.utcnow().timestamp() * 1000)}"
    new_agent = {
        "id": agent_id,
        "botId": "BOT" + agent_id[-6:].upper(),
        "name": name,
        "userId": user["id"],
        "strategy": {"type": strategy_type},
        "riskness": int(riskness),
        "status": "active",
        "portfolio": {
            "agentId": agent_id,
            "usdcBalance": float(initial_balance),
            "totalValue": float(initial_balance),
            "positions": [],
            "trades": [],
            "lastUpdated": datetime.utcnow(),
        },
        "settings": {
            "maxPositionSize": 20.0,
            "maxTradesPerDay": 10,
            "allowedAssets": None,
            "autoApprove": True,
            "safetyExits": [
                {"id": "1", "type": "max_daily_loss", "threshold": 10.0, "enabled": True, "triggeredAt": None},
                {"id": "2", "type": "max_drawdown", "threshold": 25.0, "enabled": True, "triggeredAt": None},
                {"id": "3", "type": "fraud_alert", "threshold": 0.0, "enabled": True, "triggeredAt": None},
            ],
        },
        "performance": {
            "totalProfit": 0.0,
            "totalProfitPercent": 0.0,
            "streaks": 0,
            "winRate": 0.0,
            "totalTrades": 0,
            "profitableTrades": 0,
            "avgTradeSize": 0.0,
            "maxDrawdown": 0.0,
            "sharpeRatio": 0.0,
            "crowdDeviation": 0.0,
        },
        "createdAt": datetime.utcnow(),
        "lastTradeAt": None,
    }

    agents.append(new_agent)
    user["usdcBalance"] = float(user["usdcBalance"] - initial_balance)

    recompute_metrics()


def toggle_agent_status(agent_id: str) -> None:
    agents: List[Dict[str, Any]] = st.session_state["agents"]
    for a in agents:
        if a["id"] == agent_id:
            a["status"] = "paused" if a["status"] == "active" else "active"
            break
    recompute_metrics()


def delete_agent(agent_id: str) -> None:
    user = st.session_state["user"]
    agents: List[Dict[str, Any]] = st.session_state["agents"]

    refund = 0.0
    kept = []
    for a in agents:
        if a["id"] == agent_id:
            refund = float(a["portfolio"]["totalValue"])
        else:
            kept.append(a)

    st.session_state["agents"] = kept
    user["usdcBalance"] = float(user["usdcBalance"] + refund)

    recompute_metrics()


def daily_price() -> float:
    user = st.session_state["user"]
    agents: List[Dict[str, Any]] = st.session_state["agents"]
    return calculate_pricing(len(agents), float(user["settings"]["defaultRiskLevel"]))
