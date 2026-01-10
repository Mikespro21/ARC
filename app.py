import streamlit as st

from crowdlike.ui import apply_ui, hero, nav, soft_divider, xp_bar
from crowdlike.auth import require_login, save_current_user, logout
from crowdlike.game import xp_progress, compute_streak, record_visit, ensure_user_schema

st.set_page_config(page_title="Crowdlike", page_icon="🫧", layout="wide")
apply_ui()

user = require_login(app_name="Crowdlike")
ensure_user_schema(user)
record_visit(user, "home")
save_current_user()

# --- Sidebar (minimal) ---
with st.sidebar:
    st.markdown("### ⚙️ Quick menu")
    if st.button("Log out", key="sb_logout"):
        logout()
        st.rerun()
    st.caption("Saved locally on this device.")

nav(active="Home")

lvl, xp_in, xp_to_next, pct = xp_progress(int(user.get("xp", 0)))
streak = compute_streak(user.get("active_days") or [])

hero(
    f"{user.get('avatar','🧊')}  Welcome, {user.get('username','Member')}",
    "Agentic commerce meets community — powered by USDC testnet on Arc.",
    badge=f"Level {lvl} · Streak {streak}d",
)

# --- Calm top stats (3 cards, gems moved to a small line) ---
c1, c2, c3 = st.columns(3)
with c1:
    st.markdown(
        '<div class="card card-strong"><div style="font-weight:760">💵 Cash</div>'
        f'<div style="font-size:1.35rem;font-weight:820;margin-top:4px">${float(user.get("cash_usdc",0.0)):.2f}</div>'
        '<div style="color:var(--muted);font-size:0.9rem">Testnet USDC</div></div>',
        unsafe_allow_html=True
    )
with c2:
    st.markdown(
        '<div class="card card-strong"><div style="font-weight:760">🪙 Coins</div>'
        f'<div style="font-size:1.35rem;font-weight:820;margin-top:4px">{int(user.get("coins",0)):,}</div>'
        '<div style="color:var(--muted);font-size:0.9rem">Earned by quests</div></div>',
        unsafe_allow_html=True
    )
with c3:
    st.markdown(
        '<div class="card card-strong"><div style="font-weight:760">⚡ XP</div>'
        f'<div style="font-size:1.35rem;font-weight:820;margin-top:4px">{int(user.get("xp",0)):,}</div>'
        '<div style="color:var(--muted);font-size:0.9rem">Progress & reputation</div></div>',
        unsafe_allow_html=True
    )

st.caption(f"💎 Gems: **{int(user.get('gems',0)):,}**  ·  Wallet: **{((user.get('wallet') or {}).get('address','')[:6]+'…'+(user.get('wallet') or {}).get('address','')[-4:]) if ((user.get('wallet') or {}).get('address')) else 'Not set'}**")

xp_bar(pct, left=f"Level {lvl}", right=f"{xp_in}/{xp_to_next} XP")
soft_divider()

# --- Tabs reduce visual noise ---
tab1, tab2, tab3 = st.tabs(["🚀 Explore", "🔥 Activity", "🔔 Notifications"])

with tab1:
    st.markdown('<div class="card"><div style="font-weight:760">Pick your next move</div>'
                '<div style="color:var(--muted);margin-top:4px">Keep it simple: market → quests → shop.</div></div>',
                unsafe_allow_html=True)
    st.write("")
    a, b = st.columns(2)
    with a:
        st.page_link("pages/market.py", label="📈 Market")
        st.page_link("pages/quests.py", label="🎯 Quests")
        st.page_link("pages/shop.py", label="🛍️ Shop")
    with b:
        st.page_link("pages/social.py", label="👥 Social")
        st.page_link("pages/profile.py", label="🧑‍🚀 Profile")
        st.page_link("pages/coach.py", label="🤖 Coach")

with tab2:
    feed = user.get("activity") or []
    if not feed:
        st.caption("Do your first quest to light this up ✨")
    else:
        for item in feed[:10]:
            st.markdown(
                f'<div class="card" style="margin-bottom:0.55rem">'
                f'<div style="display:flex;gap:0.65rem;align-items:flex-start">'
                f'<div style="font-size:1.25rem">{item.get("icon","✨")}</div>'
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
