from __future__ import annotations

"""Single source of truth for pages/navigation."""

from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class Page:
    id: str
    label: str
    path: str
    icon: str
    group: str = "More"
    core: bool = False
    order: int = 100
    desc: str = ""
    min_role: str = "human"  # human < bot < admin


_ROLE_RANK = {"human": 0, "bot": 1, "admin": 2}


def _allowed(role: str, min_role: str) -> bool:
    r = _ROLE_RANK.get(str(role or "human").lower(), 0)
    m = _ROLE_RANK.get(str(min_role or "human").lower(), 0)
    return r >= m


PAGES: List[Page] = [
    # Core (judge-friendly)
    Page("home", "Home", "app.py", "🏠", "Core", True, 1, "Command center"),
    Page("journey", "Journey", "pages/journey.py", "🧭", "Core", False, 1_5, "Guided setup wizard"),
    Page("market", "Market", "pages/market.py", "📈", "Core", True, 2, "Practice + testnet checkout"),
    Page("coach", "Coach", "pages/coach.py", "🤖", "Core", True, 3, "Agent console + approvals"),
    Page("agents", "Agents", "pages/agents.py", "🧠", "Core", True, 4, "Create & manage agents"),

    # More
    Page("chat", "Chat", "pages/chat.py", "💬", "More", False, 10, "Per-agent chat"),
    Page("compare", "Leaderboards", "pages/compare.py", "🏁", "More", False, 11, "Profit+streak scoreboards"),
    Page("analytics", "Analytics", "pages/analytics.py", "📊", "Core", False, 12, "Runs + risk + portfolio metrics"),

    Page("safety", "Safety", "pages/safety.py", "🛡️", "Controls", False, 20, "Panic sell + guardrails"),
    Page("pricing", "Pricing", "pages/pricing.py", "💳", "Controls", False, 21, "Per-day estimator"),
    Page("quests", "Quests", "pages/quests.py", "🧩", "Growth", False, 30, "Daily XP/coins"),
    Page("shop", "Shop", "pages/shop.py", "🛒", "Growth", False, 31, "Spend coins on perks"),
    Page("social", "Social", "pages/social.py", "❤️", "Growth", False, 32, "Likes + crowd score"),
    Page("profile", "Profile", "pages/profile.py", "👤", "Settings", False, 40, "Wallet + limits"),
    Page("admin", "Admin", "pages/admin.py", "🧾", "Settings", False, 41, "Trustless audit log", min_role="bot"),
]


def pages_for_role(role: str) -> List[Page]:
    role = str(role or "human").lower()
    return [p for p in PAGES if _allowed(role, p.min_role)]


def all_pages(role: str = "human") -> List[Page]:
    return sorted(pages_for_role(role), key=lambda p: (p.order, p.label))


def core_pages(role: str = "human") -> List[Page]:
    return [p for p in all_pages(role) if p.core]


def non_core_pages(role: str = "human") -> List[Page]:
    return [p for p in all_pages(role) if not p.core]


def groups(role: str = "human") -> List[str]:
    gs: List[str] = []
    for p in non_core_pages(role):
        if p.group not in gs:
            gs.append(p.group)
    return gs


def search_pages(q: str, role: str = "human") -> List[Page]:
    q = (q or "").strip().lower()
    if not q:
        return non_core_pages(role)
    out: List[Page] = []
    for p in non_core_pages(role):
        hay = f"{p.label} {p.desc} {p.group}".lower()
        if q in hay:
            out.append(p)
    return out
