import streamlit as st

from crowdlike.ui import apply_ui, hero, nav, link_button, soft_divider, xp_bar
from crowdlike.auth import require_login, save_current_user, logout
from crowdlike.game import xp_progress, compute_streak, record_visit, ensure_user_schema

st.set_page_config(page_title="Crowdlike", page_icon="🫧", layout="wide")
apply_ui()

user = require_login(app_name="Crowdlike")
ensure_user_schema(user)
record_visit(user, "home")
save_current_user()

# --- Sidebar quick controls ---
with st.sidebar:
    st.markdown("### ⚙️ Quick menu")
    if st.button("Log out", key="sb_logout"):
        logout()
        st.rerun()
    st.caption("Tip: Your profile is saved locally on this device.")

nav(active="Home")

lvl, xp_in, xp_to_next, pct = xp_progress(int(user.get("xp", 0)))
streak = compute_streak(user.get("active_days") or [])

hero(
    f"{user.get('avatar','🧊')}  Welcome, {user.get('username','Member')}",
    "Agentic commerce meets community — powered by USDC testnet on Arc.",
    badge=f"Level {lvl} · Streak {streak}d",
)

# ---- Top stats ----
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown('<div class="card card-strong"><h3>💵 Cash</h3>'
                f'<div style="font-size:1.55rem;font-weight:800">${float(user.get("cash_usdc",0.0)):.2f}</div>'
                '<div style="color:var(--muted)">Testnet “cash” (USDC)</div></div>', unsafe_allow_html=True)
with col2:
    st.markdown('<div class="card card-strong"><h3>🪙 Coins</h3>'
                f'<div style="font-size:1.55rem;font-weight:800">{int(user.get("coins",0)):,}</div>'
                '<div style="color:var(--muted)">Earned by quests</div></div>', unsafe_allow_html=True)
with col3:
    st.markdown('<div class="card card-strong"><h3>💎 Gems</h3>'
                f'<div style="font-size:1.55rem;font-weight:800">{int(user.get("gems",0)):,}</div>'
                '<div style="color:var(--muted)">Premium drops</div></div>', unsafe_allow_html=True)
with col4:
    st.markdown('<div class="card card-strong"><h3>⚡ XP</h3>'
                f'<div style="font-size:1.55rem;font-weight:800">{int(user.get("xp",0)):,}</div>'
                '<div style="color:var(--muted)">Progress & reputation</div></div>', unsafe_allow_html=True)

st.write("")
xp_bar(pct, left=f"Level {lvl}", right=f"{xp_in}/{xp_to_next} XP")

soft_divider()

# ---- Quick actions ----
a1, a2, a3 = st.columns([1, 1, 1])
with a1:
    st.markdown('<div class="card"><h3>🚀 Start here</h3>'
                '<div style="color:var(--muted)">Choose a next move:</div></div>', unsafe_allow_html=True)
    st.write("")
    st.page_link("pages/market.py", label="📈 Go to Market")
    st.page_link("pages/shop.py", label="🛍️ Go to Shop")
    st.page_link("pages/quests.py", label="🎯 Go to Quests")

with a2:
    wallet = (user.get("wallet") or {}).get("address", "")
    st.markdown('<div class="card"><h3>🧑‍🚀 Wallet</h3>'
                '<div style="color:var(--muted)">Connect a wallet address to unlock testnet checkout.</div></div>',
                unsafe_allow_html=True)
    st.write("")
    if wallet:
        st.success(f"Connected: {wallet[:6]}…{wallet[-4:]}")
        st.page_link("pages/profile.py", label="Manage wallet")
    else:
        st.warning("No wallet yet.")
        st.page_link("pages/profile.py", label="Set up wallet")

with a3:
    st.markdown('<div class="card"><h3>👥 Social</h3>'
                '<div style="color:var(--muted)">Friends, leaderboards, and vibes.</div></div>', unsafe_allow_html=True)
    st.write("")
    st.page_link("pages/social.py", label="Open Social")
    st.page_link("pages/coach.py", label="Talk to Coach 🤖")

soft_divider()

# ---- Feed ----
c1, c2 = st.columns([1.25, 0.75])

with c1:
    st.subheader("🔥 Recent activity")
    feed = user.get("activity") or []
    if not feed:
        st.caption("Do your first quest to light this up ✨")
    else:
        for item in feed[:8]:
            st.markdown(
                f'<div class="card" style="margin-bottom:0.6rem">'
                f'<div style="display:flex;gap:0.65rem;align-items:flex-start">'
                f'<div style="font-size:1.25rem">{item.get("icon","✨")}</div>'
                f'<div><div style="font-weight:700">{item.get("text","")}</div>'
                f'<div style="color:var(--muted);font-size:0.82rem">{item.get("ts","")}</div></div>'
                f'</div></div>',
                unsafe_allow_html=True,
            )

with c2:
    st.subheader("🔔 Notifications")
    notes = user.get("notifications") or []
    if not notes:
        st.caption("You’re all caught up.")
    else:
        for n in notes[:6]:
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
