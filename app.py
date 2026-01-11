import streamlit as st

from crowdlike.settings import bool_setting
from crowdlike.ui import apply_ui, hero, nav, soft_divider, xp_bar, button_style, status_bar, metric_card, callout
from crowdlike.tour import maybe_run_tour
from crowdlike.auth import require_login, save_current_user, logout
from crowdlike.game import xp_progress, compute_streak, record_visit, ensure_user_schema
from crowdlike.agents import get_active_agent, get_agents, agent_label
from crowdlike.version import VERSION

st.set_page_config(page_title="Crowdlike", page_icon="🫧", layout="wide")
apply_ui()

user = require_login(app_name="Crowdlike")

maybe_run_tour(user, current_page="home")
ensure_user_schema(user)
record_visit(user, "home")
save_current_user()

_demo = bool_setting("DEMO_MODE", True)

with st.sidebar:
    st.markdown("### Quick menu")
    st.page_link("app.py", label="Home")
    st.page_link("pages/agents.py", label="Agents")
    st.page_link("pages/compare.py", label="Compare")
    st.page_link("pages/chat.py", label="Chat")
    st.page_link("pages/market.py", label="Market")
    st.page_link("pages/safety.py", label="Safety")
    st.page_link("pages/pricing.py", label="Pricing")
    st.page_link("pages/quests.py", label="Quests")
    st.page_link("pages/shop.py", label="Shop")
    st.page_link("pages/social.py", label="Social")
    st.page_link("pages/profile.py", label="Profile")
    soft_divider()
    if st.button("Log out", key="sb_logout"):
        logout()
        st.rerun()
    st.caption("Saved locally on this device.")

nav(active="Home")

lvl, xp_in, xp_to_next, pct = xp_progress(int(user.get("xp", 0)))
streak = compute_streak(user.get("active_days") or [])

crowd = user.get("crowd") if isinstance(user.get("crowd"), dict) else {}
crowd_score = float(crowd.get("score", 50.0) or 50.0)

wallet = (user.get("wallet") or {}) if isinstance(user.get("wallet"), dict) else {}
wallet_addr = (wallet.get("address") or "").strip()
wallet_short = (wallet_addr[:6] + "…" + wallet_addr[-4:]) if wallet_addr else "Not set"

active_agent = get_active_agent(user)
agents = get_agents(user)

hero(
    f"{user.get('avatar','🧊')}  Welcome, {user.get('username','Member')}",
    f"Crowdlike v{VERSION} · multi-agent investing + agentic payments · Arc USDC testnet demo.",
    badge=f"{agent_label(active_agent)} · Level {lvl} · Streak {streak}d",
)

status_bar(wallet_set=bool(wallet_addr), demo_mode=_demo, crowd_score=crowd_score)

# --- Snapshot ---
c1, c2, c3, c4 = st.columns(4)
with c1:
    port = active_agent.get("portfolio") if isinstance(active_agent.get("portfolio"), dict) else {}
    cash = float(port.get("cash_usdc", 0.0) or 0.0)
    metric_card("Active cash", f"${cash:.2f}", "Agent portfolio", accent="purple")
with c2:
    metric_card("Agents", f"{len(agents)}", "Separate portfolios", accent="blue")
with c3:
    metric_card("Crowd Score", f"{crowd_score:.0f}", "Gently boosts limits", accent="blue")
with c4:
    metric_card("Wallet", wallet_short, "Public address", accent="none")

xp_bar(pct, left=f"Level {lvl}", right=f"{xp_in}/{xp_to_next} XP")
soft_divider()

# --- Quickstart (judge-friendly) ---
has_verified = any((p or {}).get("status") == "verified" for p in (user.get("purchases") or []))
limits_set = isinstance(user.get("policy"), dict) and any(k in user["policy"] for k in ("max_per_tx_usdc", "daily_cap_usdc", "cooldown_s"))
wallet_set = bool(wallet_addr)

st.markdown(
    '<div class="card card-strong">'
    '<div style="font-weight:860; font-size:1.05rem">Quickstart (fastest demo loop)</div>'
    '<div style="color:var(--muted);margin-top:4px">'
    'Set wallet → set limits → run a testnet checkout → paste receipt (tx hash) → verified.'
    '</div>'
    '</div>',
    unsafe_allow_html=True,
)

q1, q2, q3 = st.columns(3)
with q1:
    st.write(("✅ " if wallet_set else "⬜ ") + "Wallet added")
    st.caption("Profile → paste your public 0x address")
with q2:
    st.write(("✅ " if limits_set else "⬜ ") + "Limits set")
    st.caption("Profile → Autonomy & Limits")
with q3:
    st.write(("✅ " if has_verified else "⬜ ") + "Receipt verified")
    st.caption("Market → Testnet checkout")

soft_divider()

# Two clear CTAs (keep it simple)
cta1, cta2, cta3 = st.columns([1.2, 1.0, 1.0])
with cta1:
    button_style("home_cta_checkout", "purple")
    label = "Do a testnet checkout"
    if not wallet_set:
        label = "Add wallet (required)"
    if st.button(label, key="home_cta_checkout", use_container_width=True):
        if not wallet_set:
            st.switch_page("pages/profile.py")
        else:
            st.session_state["checkout_offer_id"] = "vip_pass"
            st.session_state["checkout_step"] = 1
            st.switch_page("pages/market.py")
with cta2:
    button_style("home_cta_agents", "blue")
    if st.button("Manage agents", key="home_cta_agents", use_container_width=True):
        st.switch_page("pages/agents.py")
with cta3:
    button_style("home_cta_compare", "slate")
    if st.button("Compare performance", key="home_cta_compare", use_container_width=True):
        st.switch_page("pages/compare.py")

soft_divider()

tab1, tab2, tab3 = st.tabs(["Explore", "Activity", "Updates"])

with tab1:
    g1, g2, g3 = st.columns(3)
    with g1:
        st.markdown('<div class="card"><div style="font-weight:820">Market</div><div style="color:var(--muted);margin-top:4px">Prices, practice trading, and on-chain checkout.</div></div>', unsafe_allow_html=True)
        if st.button("Open Market", key="go_market", use_container_width=True):
            st.switch_page("pages/market.py")
    with g2:
        st.markdown('<div class="card"><div style="font-weight:820">Shop</div><div style="color:var(--muted);margin-top:4px">Spend coins or trigger checkout from perks.</div></div>', unsafe_allow_html=True)
        if st.button("Open Shop", key="go_shop", use_container_width=True):
            st.switch_page("pages/shop.py")
    with g3:
        st.markdown('<div class="card"><div style="font-weight:820">Social</div><div style="color:var(--muted);margin-top:4px">Likes → Crowd Score → smoother autonomy.</div></div>', unsafe_allow_html=True)
        if st.button("Open Social", key="go_social", use_container_width=True):
            st.switch_page("pages/social.py")

    st.write("")
    callout(
        "info",
        "Tip",
        "For judges: the on-chain proof is the tx hash. You can always open ArcScan from Market → Verify.",
    )

with tab2:
    feed = user.get("activity") or []
    if not feed:
        callout("info", "No activity yet", "Complete one quest to populate your activity feed.")
    else:
        for item in feed[:10]:
            st.markdown(
                f'<div class="card" style="margin-bottom:0.55rem">'
                f'<div style="display:flex;gap:0.65rem;align-items:flex-start">'
                f'<div style="font-size:1.10rem;opacity:0.85">{item.get("icon","")}</div>'
                f'<div><div style="font-weight:760">{item.get("text","")}</div>'
                f'<div style="color:var(--muted);font-size:0.82rem">{item.get("ts","")}</div></div>'
                f'</div></div>',
                unsafe_allow_html=True,
            )

with tab3:
    notes = user.get("notifications") or []
    if not notes:
        callout("good", "All caught up", "No new updates.")
    else:
        for n in notes[:10]:
            kind = n.get("kind", "info")
            text = n.get("text", "")
            if kind == "success":
                st.success(text)
            elif kind == "warning":
                st.warning(text)
            elif kind == "error":
                st.error(text)
            else:
                st.info(text)

save_current_user()
