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
    # Website (official)
    Page("home", "Home", "app.py", "🏠", "Website", True, 1, "Official landing page"),
    Page("product", "Product", "pages/product.py", "✨", "Website", True, 2, "What Crowdlike is"),
    Page("pricing", "Pricing", "pages/pricing.py", "💳", "Website", True, 3, "Per-day estimator"),
    Page("docs", "Docs", "pages/docs.py", "📚", "Website", True, 4, "Quickstart + FAQ"),
    Page("dashboard", "Launch App", "pages/dashboard.py", "🚀", "Website", True, 5, "App dashboard"),

    # App (workflow)
    Page("journey", "Journey", "pages/journey.py", "🧭", "App", False, 10, "Guided setup wizard"),
    Page("agents", "Agents", "pages/agents.py", "🧠", "App", False, 11, "Create & manage agents"),
    Page("coach", "Coach", "pages/coach.py", "🤖", "App", False, 12, "Runs + approvals"),
    Page("market", "Market", "pages/market.py", "📈", "App", False, 13, "Practice + checkout"),
    Page("analytics", "Analytics", "pages/analytics.py", "📊", "App", False, 14, "Portfolio metrics"),
    Page("compare", "Leaderboards", "pages/compare.py", "🏁", "App", False, 15, "Profit+streak scoreboards"),
    Page("profile", "Profile", "pages/profile.py", "👤", "App", False, 16, "Wallet + limits"),

    # Engagement
    Page("quests", "Quests", "pages/quests.py", "🧩", "Engagement", False, 30, "Daily XP/coins"),
    Page("shop", "Shop", "pages/shop.py", "🛒", "Engagement", False, 31, "Spend coins on perks"),
    Page("social", "Social", "pages/social.py", "❤️", "Engagement", False, 32, "Likes + crowd score"),
    Page("chat", "Chat", "pages/chat.py", "💬", "Engagement", False, 33, "Per-agent chat"),

    # Controls
    Page("safety", "Safety", "pages/safety.py", "🛡️", "Controls", False, 40, "Panic sell + guardrails"),

    # Company
    Page("company", "Company", "pages/company.py", "🏢", "Website", False, 50, "About"),

    # Admin
    Page("admin", "Admin", "pages/admin.py", "🧾", "Settings", False, 90, "Trustless audit log", min_role="bot"),
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
