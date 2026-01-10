from __future__ import annotations

import datetime as _dt
from typing import Any, Dict, List, Tuple

XP_PER_LEVEL = 1000


def today_str() -> str:
    return _dt.date.today().isoformat()


def level_from_xp(xp: int) -> int:
    try:
        xp_i = int(xp or 0)
    except Exception:
        xp_i = 0
    return max(1, 1 + (xp_i // XP_PER_LEVEL))


def xp_progress(xp: int) -> Tuple[int, int, int, float]:
    """Return (level, xp_in_level, xp_to_next, pct)."""
    lvl = level_from_xp(xp)
    base = (lvl - 1) * XP_PER_LEVEL
    xp_in = max(0, int(xp or 0) - base)
    to_next = XP_PER_LEVEL
    pct = min(1.0, max(0.0, xp_in / to_next if to_next else 0.0))
    return lvl, xp_in, to_next, pct


def ensure_user_schema(user: Dict[str, Any]) -> Dict[str, Any]:
    # Profile
    user.setdefault("username", "Member")
    user.setdefault("avatar", "🧊")
    user.setdefault("bio", "")
    user.setdefault("wallet", {})
    user["wallet"].setdefault("address", "")
    user["wallet"].setdefault("rpc_url", "https://rpc.testnet.arc.network")
    user["wallet"].setdefault("explorer", "https://testnet.arcscan.app")
    user["wallet"].setdefault("usdc_erc20", "0x3600000000000000000000000000000000000000")
    user["wallet"].setdefault("usdc_decimals", 6)

    # Economy
    user.setdefault("xp", 0)
    user.setdefault("coins", 500)
    user.setdefault("gems", 25)
    user.setdefault("cash_usdc", 20.0)  # demo cash (not on-chain)
    user.setdefault("inventory", [])
    user.setdefault("friends", [])
    user.setdefault("notifications", [])
    user.setdefault("activity", [])
    user.setdefault("active_days", [])

    # Market / trading demo
    user.setdefault("portfolio", {"positions": {}, "trades": [], "cash_usdc": 1000.0})

    # Receipts / purchases
    user.setdefault("purchases", [])  # [{ts,item_id,name,price,currency,tx_hash,status}]
    user.setdefault("visits", {})  # page_id -> count
    user.setdefault("quests_claimed", {})  # date -> [quest_id]

    return user


def record_visit(user: Dict[str, Any], page_id: str) -> None:
    v = user.setdefault("visits", {})
    v[page_id] = int(v.get(page_id, 0)) + 1


def record_active_day(user: Dict[str, Any]) -> None:
    days: List[str] = user.setdefault("active_days", [])
    t = today_str()
    if t not in days:
        days.append(t)


def compute_streak(active_days: List[str]) -> int:
    """Consecutive-day streak ending today."""
    if not active_days:
        return 0
    # Parse unique days
    try:
        day_set = { _dt.date.fromisoformat(d) for d in active_days if d }
    except Exception:
        return 0

    streak = 0
    cur = _dt.date.today()
    while cur in day_set:
        streak += 1
        cur = cur - _dt.timedelta(days=1)
    return streak


def add_notification(user: Dict[str, Any], text: str, kind: str = "info") -> None:
    user.setdefault("notifications", []).insert(
        0,
        {
            "ts": _dt.datetime.utcnow().isoformat(timespec="seconds") + "Z",
            "kind": kind,
            "text": text,
        },
    )
    # Keep it lightweight
    user["notifications"] = user["notifications"][:30]


def log_activity(user: Dict[str, Any], text: str, icon: str = "✨") -> None:
    user.setdefault("activity", []).insert(
        0,
        {
            "ts": _dt.datetime.utcnow().isoformat(timespec="seconds") + "Z",
            "icon": icon,
            "text": text,
        },
    )
    user["activity"] = user["activity"][:60]
    record_active_day(user)


def grant_xp(user: Dict[str, Any], amount: int, source: str, description: str) -> None:
    if amount <= 0:
        return
    user["xp"] = int(user.get("xp", 0)) + int(amount)
    # Light coin drip: 1 coin per 10 XP
    user["coins"] = int(user.get("coins", 0)) + int(amount // 10)
    log_activity(user, f"+{amount} XP • {source}: {description}", icon="⚡")
