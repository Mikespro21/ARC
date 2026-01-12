from __future__ import annotations

"""Shared layout helpers.

This project is intentionally Streamlit-first.

UX goal: keep the demo "impossible to get lost" during judge runs.
"""

from typing import Any, Dict

import streamlit as st

from crowdlike.agents import agent_label, get_agents, get_active_agent, set_active_agent
from crowdlike.auth import logout, save_current_user
from crowdlike.ui import soft_divider, callout, button_style, pills
from crowdlike.flow import sidebar_flow_card
from crowdlike.version import VERSION


def _readiness(user: Dict[str, Any]) -> Dict[str, bool]:
    wallet = (user.get("wallet") or {}) if isinstance(user.get("wallet"), dict) else {}
    wallet_set = bool((wallet.get("address") or "").strip())

    policy = user.get("policy") if isinstance(user.get("policy"), dict) else {}
    limits_set = any(k in policy for k in ("max_per_tx_usdc", "daily_cap_usdc", "cooldown_s", "risk"))

    has_verified = any((p or {}).get("status") == "verified" for p in (user.get("purchases") or []))
    agents = get_agents(user)
    has_agents = bool(agents)

    return {
        "wallet_set": wallet_set,
        "limits_set": limits_set,
        "has_verified": has_verified,
        "has_agents": has_agents,
    }


def render_sidebar(user: Dict[str, Any], *, active_page: str = "") -> None:
    """Consistent sidebar across every page.

    - Always shows the active agent + quick switch.
    - Shows a tiny readiness checklist so judges can understand what to do next.
    - Keeps navigation consistent even if Streamlit's default pages menu is hidden.
    """

    with st.sidebar:
        st.markdown("### 🫧 Crowdlike")
        pills([
            ("Version", f"v{VERSION}", "info"),
            ("Network", "Arc testnet", "info"),
        ])
        st.caption("Local-first demo · Safe-by-default UX")

        # --- Agent switcher (global) ---
        agents = get_agents(user)
        active = get_active_agent(user)
        ids = [str(a.get("id")) for a in agents]
        id_to_label = {str(a.get("id")): agent_label(a) for a in agents}

        if ids:
            try:
                idx = ids.index(str(user.get("active_agent_id")))
            except Exception:
                idx = 0
            sel = st.selectbox(
                "Active agent",
                options=ids,
                format_func=lambda x: id_to_label.get(x, x),
                index=idx,
                key=f"sb_active_agent_{active_page or 'page'}",
            )
            if str(sel) != str(user.get("active_agent_id")):
                set_active_agent(user, str(sel))
                save_current_user()
                st.rerun()

        # --- Quick demo actions ---
        st.markdown("**Quick actions**")
        c1, c2 = st.columns(2)
        with c1:
            button_style("sb_go_checkout", "purple")
            if st.button("Checkout", key="sb_go_checkout", use_container_width=True):
                wallet = (user.get("wallet") or {}) if isinstance(user.get("wallet"), dict) else {}
                if not (wallet.get("address") or "").strip():
                    st.switch_page("pages/profile.py")
                else:
                    st.session_state["checkout_offer_id"] = "vip_pass"
                    st.session_state["checkout_step"] = 1
                    st.switch_page("pages/market.py")
        with c2:
            if st.button("Coach", key="sb_go_coach", use_container_width=True):
                st.switch_page("pages/coach.py")

        soft_divider()

        # --- Readiness checklist ---
        r = _readiness(user)
        st.markdown("**Demo readiness**")
        st.write(("✅ " if r["has_agents"] else "⬜ ") + "Agents ready")
        st.write(("✅ " if r["wallet_set"] else "⬜ ") + "Wallet added")
        st.write(("✅ " if r["limits_set"] else "⬜ ") + "Limits set")
        st.write(("✅ " if r["has_verified"] else "⬜ ") + "Receipt verified")

        if not r["wallet_set"]:
            callout("info", "Next", "Open Profile → Wallet and paste a public address.")
        elif not r["limits_set"]:
            callout("info", "Next", "Open Profile → Limits and choose a preset.")
        elif not r["has_verified"]:
            callout("info", "Next", "Open Market → Testnet checkout and verify a tx hash.")

        soft_divider()

        st.markdown("**Pages**")
        
        # --- Quick nav (kept short on purpose) ---
        st.page_link("app.py", label="🏠 Home")
        st.page_link("pages/market.py", label="📈 Market")
        st.page_link("pages/coach.py", label="🤖 Coach")
        st.page_link("pages/agents.py", label="🧠 Agents")

        soft_divider()

        # --- More pages (searchable + scrollable) ---
        from crowdlike.registry import all_pages

        with st.expander("⋯ More pages", expanded=False):
            q = st.text_input("Search", key=f"sb_search_{active_page}", placeholder="Type to filter…")
            role = str(user.get("role") or "human").lower()
            pages = [p for p in all_pages(role) if p.path not in ("app.py","pages/market.py","pages/coach.py","pages/agents.py")]
            ql = (q or "").strip().lower()
            if ql:
                pages = [p for p in pages if ql in (f"{p.label} {p.group} {p.desc}").lower()]

            st.markdown('<div style="max-height:360px; overflow-y:auto; padding-right:6px;">', unsafe_allow_html=True)
            last_group = None
            for p in pages:
                if last_group != p.group:
                    st.markdown(f"**{p.group}**")
                    last_group = p.group
                st.page_link(p.path, label=f"{p.icon} {p.label}".strip())
            st.markdown("</div>", unsafe_allow_html=True)

        soft_divider()
        if st.button("Log out", key=f"sb_logout_{active_page}"):
            logout()
            st.rerun()
        st.caption("Saved locally on this device.")
