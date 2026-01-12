from __future__ import annotations

"""Single source of truth for pages/navigation.

UX goal:
- Keep the top nav short (judge-friendly).
- Put everything else behind an expandable "More" drawer with search.
"""

from dataclasses import dataclass
from typing import Iterable, List, Optional


@dataclass(frozen=True)
class Page:
    id: str
    label: str
    path: str
    icon: str = ""
    group: str = "More"
    core: bool = False  # appears in top nav
    order: int = 100
    desc: str = ""


PAGES: List[Page] = [
    # Core
    Page("home", "Home", "app.py", "🏠", "Core", True, 1, "Command center"),
    Page("market", "Market", "pages/market.py", "📈", "Core", True, 2, "Practice + testnet checkout"),
    Page("coach", "Coach", "pages/coach.py", "🤖", "Core", True, 3, "Agent console + approvals"),
    Page("agents", "Agents", "pages/agents.py", "🧠", "Core", True, 4, "Create & manage agents"),

    # More
    Page("chat", "Chat", "pages/chat.py", "💬", "More", False, 10, "Per-agent chat"),
    Page("compare", "Compare", "pages/compare.py", "📊", "More", False, 11, "Profit/return leaderboards"),
    Page("safety", "Safety", "pages/safety.py", "🛡️", "Controls", False, 20, "Panic sell + guardrails"),
    Page("pricing", "Pricing", "pages/pricing.py", "💳", "Controls", False, 21, "Pay-per-day estimator"),
    Page("quests", "Quests", "pages/quests.py", "🧩", "Growth", False, 30, "Daily XP/coins"),
    Page("shop", "Shop", "pages/shop.py", "🛒", "Growth", False, 31, "Spend coins on perks"),
    Page("social", "Social", "pages/social.py", "❤️", "Growth", False, 32, "Likes + crowd score"),
    Page("profile", "Profile", "pages/profile.py", "👤", "Settings", False, 40, "Wallet + limits"),
]

def all_pages() -> List[Page]:
    return sorted(PAGES, key=lambda p: (p.order, p.label))

def core_pages() -> List[Page]:
    return [p for p in all_pages() if p.core]

def non_core_pages() -> List[Page]:
    return [p for p in all_pages() if not p.core]

def groups() -> List[str]:
    gs = []
    for p in all_pages():
        if p.group not in gs:
            gs.append(p.group)
    return gs

def search_pages(q: str) -> List[Page]:
    q = (q or "").strip().lower()
    if not q:
        return non_core_pages()
    out: List[Page] = []
    for p in non_core_pages():
        hay = f"{p.label} {p.desc} {p.group}".lower()
        if q in hay:
            out.append(p)
    return out

def get_page_by_id(page_id: str) -> Optional[Page]:
    for p in PAGES:
        if p.id == page_id:
            return p
    return None
