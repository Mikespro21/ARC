import streamlit as st

from crowdlike.ui import apply_ui, hero, nav, soft_divider, xp_bar, button_style
from crowdlike.tour import maybe_run_tour, tour_complete_step
from crowdlike.auth import require_login, save_current_user, logout
from crowdlike.game import xp_progress, compute_streak, record_visit, ensure_user_schema
from crowdlike.version import VERSION

st.set_page_config(page_title="Crowdlike", page_icon="🫧", layout="wide")
apply_ui()

user = require_login(app_name="Crowdlike")

maybe_run_tour(user, current_page="home")
ensure_user_schema(user)
record_visit(user, "home")
save_current_user()

with st.sidebar:
    st.markdown("### Quick menu")
    if st.button("Log out", key="sb_logout"):
        logout()
        st.rerun()
    st.caption("Saved locally on this device.")

nav(active="Home")

lvl, xp_in, xp_to_next, pct = xp_progress(int(user.get("xp", 0)))
streak = compute_streak(user.get("active_days") or [])

# Avatar kept (does NOT count toward emoji limit)
# Emojis on this page (excluding avatar): tabs = 🚀 🔥 🔔 (3) + badge 🔥 (1) = 4 total
hero(
    f"{user.get('avatar','🧊')}  Welcome, {user.get('username','Member')}",
    f"Crowdlike v{VERSION} · Agentic commerce meets community — powered by USDC testnet on Arc.",
    badge=f"Level {lvl} · 🔥 Streak {streak}d",
)

# Calm top stats (no emojis here)
c1, c2, c3 = st.columns(3)
with c1:
    st.markdown(
        '<div class="card card-strong" style="border:1px solid rgba(167,139,250,0.24); background: radial-gradient(680px 220px at 88% 10%, rgba(167,139,250,0.06), transparent 70%), rgba(255,255,255,0.94);"><div style="font-weight:760">Cash</div>'
        f'<div style="font-size:1.35rem;font-weight:820;margin-top:4px">${float(user.get("cash_usdc",0.0)):.2f}</div>'
        '<div style="color:var(--muted);font-size:0.9rem">Testnet USDC</div></div>',
        unsafe_allow_html=True
    )
with c2:
    st.markdown(
        '<div class="card card-strong"><div style="font-weight:760">Coins</div>'
        f'<div style="font-size:1.35rem;font-weight:820;margin-top:4px">{int(user.get("coins",0)):,}</div>'
        '<div style="color:var(--muted);font-size:0.9rem">Earned by quests</div></div>',
        unsafe_allow_html=True
    )
with c3:
    st.markdown(
        '<div class="card card-strong"><div style="font-weight:760">XP</div>'
        f'<div style="font-size:1.35rem;font-weight:820;margin-top:4px">{int(user.get("xp",0)):,}</div>'
        '<div style="color:var(--muted);font-size:0.9rem">Progress & reputation</div></div>',
        unsafe_allow_html=True
    )

wallet_addr = (user.get("wallet") or {}).get("address", "")
wallet_short = (wallet_addr[:6] + "…" + wallet_addr[-4:]) if wallet_addr else "Not set"
st.caption(f"Gems: **{int(user.get('gems',0)):,}**  ·  Wallet: **{wallet_short}**")

xp_bar(pct, left=f"Level {lvl}", right=f"{xp_in}/{xp_to_next} XP")
soft_divider()

# --- Primary CTA (60/30/10) ---
st.markdown(
    '<div class="card card-strong">'
    '<div style="display:flex; align-items:center; justify-content:space-between; gap:14px; flex-wrap:wrap">'
    '<div style="min-width:240px">'
    '<div style="font-weight:820; font-size:1.05rem">Automate your workflow with AI agents</div>'
    '<div style="color:var(--muted); margin-top:4px">'
    'Make plans, track goals, and turn decisions into actions — with a simple agent loop.'
    '</div>'
    '</div>'
    '<div style="display:flex; gap:10px; align-items:center">'
    '</div>'
    '</div>'
    '</div>',
    unsafe_allow_html=True
)

# Make this CTA button look like the primary action (blue = 30%)
button_style("cta_automate", "purple")
if st.button("Start Automating My Workflow", key="cta_automate", use_container_width=True):
    st.switch_page("pages/coach.py")

tab1, tab2, tab3 = st.tabs(["Explore 🚀", "Activity 🔥", "Updates 🔔"])

with tab1:
    st.markdown(
        '<div class="card"><div style="font-weight:760">Pick your next move</div>'
        '<div style="color:var(--muted);margin-top:4px">Market → Quests → Shop is the fastest loop.</div></div>',
        unsafe_allow_html=True
    )
    st.write("")

    # 6 buttons, each a different subtle color (premium, not rainbow)
    b1, b2, b3 = st.columns(3)
    with b1:
        button_style("home_go_market", "blue")
        if st.button("Market", key="home_go_market", use_container_width=True):
            st.switch_page("pages/market.py")

        button_style("home_go_shop", "violet")
        if st.button("Shop", key="home_go_shop", use_container_width=True):
            st.switch_page("pages/shop.py")

    with b2:
        button_style("home_go_quests", "indigo")
        if st.button("Quests", key="home_go_quests", use_container_width=True):
            st.switch_page("pages/quests.py")

        button_style("home_go_social", "teal")
        if st.button("Social", key="home_go_social", use_container_width=True):
            st.switch_page("pages/social.py")

    with b3:
        button_style("home_go_profile", "slate")
        if st.button("Profile", key="home_go_profile", use_container_width=True):
            st.switch_page("pages/profile.py")

        button_style("home_go_coach", "rose")
        if st.button("Coach", key="home_go_coach", use_container_width=True):
            st.switch_page("pages/coach.py")

with tab2:
    feed = user.get("activity") or []
    if not feed:
        st.caption("Do your first quest to light this up.")
    else:
        for item in feed[:10]:
            st.markdown(
                f'<div class="card" style="margin-bottom:0.55rem">'
                f'<div style="display:flex;gap:0.65rem;align-items:flex-start">'
                f'<div style="font-size:1.10rem;opacity:0.85">{item.get("icon","")}</div>'
                f'<div><div style="font-weight:740">{item.get("text","")}</div>'
                f'<div style="color:var(--muted);font-size:0.82rem">{item.get("ts","")}</div></div>'
                f'</div></div>',
                unsafe_allow_html=True,
            )

with tab3:
    notes = user.get("notifications") or []
    if not notes:
        st.caption("You’re all caught up.")
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

# Guided tutorial (spotlight tour)
