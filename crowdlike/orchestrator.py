from __future__ import annotations

"""A tiny agent orchestrator for the demo.

Goal:
- Show *agentic* behavior while keeping safety rails explicit.
- Never execute real on-chain payments automatically unless user approves.
"""

import datetime as _dt
import random
from typing import Any, Dict, Optional


def _now_iso() -> str:
    return _dt.datetime.utcnow().isoformat(timespec="seconds") + "Z"


def ensure_agent_runtime(agent: Dict[str, Any]) -> None:
    agent.setdefault("mode", "assist")  # off | assist | auto (auto is still policy-limited)
    agent.setdefault("approvals", [])   # queued proposed actions
    if not isinstance(agent.get("approvals"), list):
        agent["approvals"] = []


def propose_next_action(user: Dict[str, Any], agent: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Create a proposal and push to approvals queue.

    This is intentionally deterministic-ish and local-only.
    """
    ensure_agent_runtime(agent)
    if agent["mode"] == "off":
        return None

    # If there's already something pending, don't spam.
    if agent["approvals"]:
        return None

    # Simple decision: trade suggestion vs small donation/payment suggestion
    risk = float((agent.get("policy") or {}).get("risk") or (user.get("policy") or {}).get("risk") or 25.0)
    r = random.random()
    if r < 0.6:
        asset = random.choice(["BTC", "ETH", "SOL"])
        side = "BUY" if random.random() < 0.7 else "SELL"
        qty = round(0.001 + (risk/100.0)*0.01, 4)  # tiny demo qty
        proposal = {
            "id": f"appr_{random.randint(100000,999999)}",
            "ts": _now_iso(),
            "type": "trade",
            "title": f"{side} {qty} {asset}",
            "payload": {"asset": asset, "side": side, "qty": qty},
            "status": "pending",
        }
    else:
        amt = round(0.05 + (risk/100.0)*0.10, 2)  # $0.05-$0.15 demo
        proposal = {
            "id": f"appr_{random.randint(100000,999999)}",
            "ts": _now_iso(),
            "type": "payment",
            "title": f"Pay {amt} USDC (requires confirmation)",
            "payload": {"amount_usdc": amt, "to": "treasury"},
            "status": "pending",
        }

    agent["approvals"].append(proposal)
    return proposal


def decide_auto_execute(user: Dict[str, Any], agent: Dict[str, Any], proposal: Dict[str, Any]) -> bool:
    """Auto mode can execute *trade* proposals; payment proposals still require manual confirm."""
    ensure_agent_runtime(agent)
    if agent.get("mode") != "auto":
        return False
    if proposal.get("type") == "payment":
        return False
    return True
