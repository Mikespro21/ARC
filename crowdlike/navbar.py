from __future__ import annotations

import streamlit as st

from crowdlike.registry import all_pages, Page
from crowdlike.auth import current_user
from crowdlike.ui import button_style


NAV = [
    ("Product", ["home", "product", "pricing", "docs"]),
    ("Company", ["company"]),
    ("App", ["dashboard", "journey", "agents", "coach", "market", "analytics", "compare", "profile", "safety"]),
    ("Tools", ["quests", "shop", "social", "chat"]),
]


def _page_map(role: str = "human") -> dict[str, Page]:
    return {p.id: p for p in all_pages(role)}


def _link(p: Page, *, key: str, active: bool = False) -> None:
    label = f"{p.icon} {p.label}"
    if active:
        button_style(key, "purple")
    else:
        button_style(key, "ghost")
    if st.button(label, key=key, use_container_width=True):
        st.switch_page(p.path)


def render_navbar(*, active: str = "home") -> None:
    """Sticky top navbar with grouped dropdowns + user menu.

    This intentionally avoids exotic components so it works in Streamlit Cloud.
    """
    u = current_user() or {}
    role = str((u.get("role") or "human")).lower()
    pages = _page_map(role)

    st.markdown('<div class="topbar">', unsafe_allow_html=True)

    left, mid, right = st.columns([1.4, 3.6, 1.6], gap="large")

    with left:
        st.markdown('<div class="topbar-logo">🫧 <span>Crowdlike</span></div>', unsafe_allow_html=True)
        st.caption("v1.5 • Cloud-ready demo")

    with mid:
        cols = st.columns(5, gap="small")
        # Search / command palette
        with cols[0]:
            with st.popover("⌘ Search", use_container_width=True):
                q = st.text_input("Search pages", key="nav_search_q", placeholder="Type to filter…")
                if q:
                    ql = q.lower().strip()
                    matches = [p for p in pages.values() if ql in p.label.lower() or ql in p.id.lower()]
                else:
                    matches = []
                if matches:
                    st.caption("Matches")
                    for i, p in enumerate(matches[:10]):
                        _link(p, key=f"nav_search_{i}")
                else:
                    st.caption("Type to search the site + app pages.")

        # Grouped dropdowns
        group_names = ["Product", "Company", "App", "Tools"]
        for i, g in enumerate(group_names, start=1):
            with cols[i]:
                is_active = any(pages.get(pid, None) and pages[pid].id == active for (gn, ids) in NAV for pid in ids if gn == g)
                label = f"{g}"
                if is_active:
                    label = f"• {g}"
                with st.popover(label, use_container_width=True):
                    ids = next((ids for gn, ids in NAV if gn == g), [])
                    for j, pid in enumerate(ids):
                        p = pages.get(pid)
                        if not p:
                            continue
                        _link(p, key=f"nav_{g}_{pid}", active=(pid==active))

    with right:
        # Primary CTA
        button_style("nav_launch", "purple")
        if st.button("Launch App", key="nav_launch", use_container_width=True):
            st.switch_page(pages.get("dashboard").path if pages.get("dashboard") else "pages/dashboard.py")

        # User menu
        uname = (u.get("display_name") or u.get("username") or "Guest")
        avatar = u.get("avatar") or "🧑‍🚀"
        with st.popover(f"{avatar} {uname}", use_container_width=True):
            st.caption("Session user (cloud demo)")
            st.write(f"**Role:** {role}")
            st.write(f"**User ID:** `{u.get('id','')}`")
            if st.button("Open Profile", key="nav_profile", use_container_width=True):
                st.switch_page(pages.get("profile").path if pages.get("profile") else "pages/profile.py")
            if st.button("Restart onboarding", key="nav_restart", use_container_width=True):
                st.session_state["onboard_complete"] = False
                st.switch_page(pages.get("journey").path if pages.get("journey") else "pages/journey.py")

    st.markdown("</div>", unsafe_allow_html=True)
