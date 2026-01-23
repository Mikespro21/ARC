from __future__ import annotations

import random
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from typing import Any, Dict, List, Literal, Optional

StrategyType = Literal["aggressive","conservative","balanced","swing","daytrading","hodl","custom"]
AgentStatus = Literal["active","paused","exited"]
SafetyExitType = Literal["max_daily_loss","max_drawdown","fraud_alert"]


def _now() -> datetime:
    return datetime.utcnow()


def generate_mock_user() -> Dict[str, Any]:
    return {
        "id": "user_1",
        "name": "Miguel",
        "email": "miguel@crowdlike.app",
        "walletAddress": None,
        "usdcBalance": 10000.0,
        "createdAt": datetime(2024, 1, 1),
        "settings": {
            "maxAgents": 10,
            "defaultRiskLevel": 50,
            "maxDeviationPercent": 30,
            "notifications": True,
        },
    }


def _random_positions(count: int) -> List[Dict[str, Any]]:
    assets = [
        {"id": "bitcoin", "symbol": "BTC", "price": 45000.0},
        {"id": "ethereum", "symbol": "ETH", "price": 2500.0},
        {"id": "solana", "symbol": "SOL", "price": 100.0},
        {"id": "cardano", "symbol": "ADA", "price": 0.5},
        {"id": "polkadot", "symbol": "DOT", "price": 7.0},
    ]
    positions = []
    for i in range(min(count, len(assets))):
        a = assets[i]
        amount = random.random() * 2
        avg_price = a["price"] * (0.85 + random.random() * 0.3)
        current_price = a["price"]
        value = amount * current_price
        pnl = value - (amount * avg_price)
        positions.append({
            "id": f"pos_{i+1}",
            "asset": a["id"],
            "symbol": a["symbol"],
            "amount": float(amount),
            "averagePrice": float(avg_price),
            "currentPrice": float(current_price),
            "value": float(value),
            "profitLoss": float(pnl),
            "profitLossPercent": float((pnl / (amount * avg_price)) * 100 if amount * avg_price else 0.0),
            "openedAt": _now() - timedelta(days=random.random() * 30),
        })
    return positions


def generate_mock_agents(count: int, user_id: str = "user_1") -> List[Dict[str, Any]]:
    strategies: List[StrategyType] = ["aggressive","conservative","balanced","swing","daytrading","hodl"]
    names = ["Alpha","Beta","Gamma","Delta","Epsilon","Zeta","Eta","Theta","Iota","Kappa"]

    agents: List[Dict[str, Any]] = []
    for i in range(count):
        initial_balance = 1000 + random.random() * 4000
        profit = (random.random() - 0.3) * initial_balance * 0.3  # -30% to +70%
        total_value = initial_balance + profit
        profit_pct = (profit / initial_balance) * 100 if initial_balance else 0.0

        total_trades = int(random.random() * 50) + 5
        profitable_trades = int(total_trades * (0.4 + random.random() * 0.4))

        status: AgentStatus
        if random.random() > 0.1:
            status = "active"
        else:
            status = "paused" if random.random() > 0.5 else "exited"

        strategy = random.choice(strategies)

        agent_id = f"agent_{i+1}"
        agent = {
            "id": agent_id,
            "botId": "BOT" + "".join(random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789") for _ in range(6)),
            "name": f"Agent {names[i]}" if i < len(names) else f"Agent {i+1}",
            "userId": user_id,
            "strategy": {"type": strategy},
            "riskness": int(random.random() * 100),
            "status": status,
            "portfolio": {
                "agentId": agent_id,
                "usdcBalance": float(total_value * 0.3),
                "totalValue": float(total_value),
                "positions": _random_positions(3),
                "trades": [],
                "lastUpdated": _now(),
            },
            "settings": {
                "maxPositionSize": float(15 + random.random() * 20),
                "maxTradesPerDay": int(5 + random.random() * 15),
                "allowedAssets": None,
                "autoApprove": bool(random.random() > 0.3),
                "safetyExits": [
                    {"id": "1", "type": "max_daily_loss", "threshold": float(5 + random.random()*15), "enabled": True, "triggeredAt": None},
                    {"id": "2", "type": "max_drawdown", "threshold": float(20 + random.random()*20), "enabled": True, "triggeredAt": None},
                    {"id": "3", "type": "fraud_alert", "threshold": 0.0, "enabled": True, "triggeredAt": None},
                ],
            },
            "performance": {
                "totalProfit": float(profit),
                "totalProfitPercent": float(profit_pct),
                "streaks": int(random.random() * 10),
                "winRate": float((profitable_trades / total_trades) * 100 if total_trades else 0.0),
                "totalTrades": int(total_trades),
                "profitableTrades": int(profitable_trades),
                "avgTradeSize": float(total_value * 0.1),
                "maxDrawdown": float(random.random() * 20),
                "sharpeRatio": float(0.5 + random.random() * 2),
                "crowdDeviation": float(random.random() * 40),
            },
            "createdAt": _now() - timedelta(days=random.random() * 90),
            "lastTradeAt": _now() - timedelta(hours=random.random() * 24),
        }
        agents.append(agent)

    return agents


def calculate_pricing(agent_count: int, risk_level: float) -> float:
    # (agentCount^2) * (risk / 100)
    return (agent_count ** 2) * (risk_level / 100.0)


def calculate_crowd_metrics(agents: List[Dict[str, Any]]) -> Dict[str, Any]:
    active = [a for a in agents if a.get("status") == "active"]
    if not active:
        return {
            "avgRiskness": 0,
            "avgTradesPerDay": 0.0,
            "avgPositionSize": 0.0,
            "totalAgents": 0,
            "totalVolume": 0.0,
            "topStrategies": [],
        }

    avg_risk = sum(a["riskness"] for a in active) / len(active)
    avg_pos = sum(a["settings"]["maxPositionSize"] for a in active) / len(active)
    total_vol = sum(a["portfolio"]["totalValue"] for a in active)

    counts: Dict[str, int] = {}
    for a in active:
        s = a["strategy"]["type"]
        counts[s] = counts.get(s, 0) + 1

    top_strats = sorted(
        [{"strategy": k, "count": v} for k, v in counts.items()],
        key=lambda x: x["count"],
        reverse=True,
    )[:5]

    return {
        "avgRiskness": int(round(avg_risk)),
        "avgTradesPerDay": 8.5,  # demo constant (matches React demo)
        "avgPositionSize": float(round(avg_pos)),
        "totalAgents": len(active),
        "totalVolume": float(total_vol),
        "topStrategies": top_strats,
    }


def generate_leaderboard(agents: List[Dict[str, Any]], period: str) -> List[Dict[str, Any]]:
    active = [a for a in agents if a.get("status") == "active"]
    entries = []
    for a in active:
        profit = float(a["performance"]["totalProfit"])
        profit_round = round(profit, 2)
        score = (profit_round * 100) + int(a["performance"]["streaks"])
        entries.append({
            "rank": 0,
            "botId": a["botId"],
            "agentName": a["name"],
            "score": float(score),
            "profit": float(profit_round),
            "profitPercent": float(a["performance"]["totalProfitPercent"]),
            "streaks": int(a["performance"]["streaks"]),
            "totalTrades": int(a["performance"]["totalTrades"]),
            "winRate": float(a["performance"]["winRate"]),
            "period": period,
        })
    entries.sort(key=lambda x: x["score"], reverse=True)
    for i, e in enumerate(entries[:100], start=1):
        e["rank"] = i
    return entries[:100]
