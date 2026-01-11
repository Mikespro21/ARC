import streamlit as st

from crowdlike.ui import apply_ui, hero, nav, soft_divider
from crowdlike.tour import maybe_run_tour
from crowdlike.auth import require_login, save_current_user
from crowdlike.game import ensure_user_schema, record_visit, grant_xp, add_notification, log_activity

st.set_page_config(page_title="Shop", page_icon="🛍️", layout="wide")
apply_ui()

user = require_login(app_name="Crowdlike")
maybe_run_tour(user, current_page="shop")
ensure_user_schema(user)
record_visit(user, "shop")
save_current_user()

nav(active="Home")
hero("🛍️ Shop", "Spend coins for upgrades, or use testnet USDC for premium perks.", badge="Shop")

coins = int(user.get("coins", 0) or 0)

c1, c2 = st.columns(2)
with c1:
    st.markdown(f'<div class="card"><div style="font-weight:800">Your coins</div><div style="font-size:2rem;font-weight:900;margin-top:0.25rem">{coins}</div></div>', unsafe_allow_html=True)
with c2:
    crowd = user.get("crowd") if isinstance(user.get("crowd"), dict) else {}
    score = float(crowd.get("score", 50.0) or 50.0)
    st.markdown(f'<div class="card"><div style="font-weight:800">Crowd Score</div><div style="font-size:2rem;font-weight:900;margin-top:0.25rem">{score:.0f}</div><div style="color:var(--muted);margin-top:4px">Affects payment limits gently.</div></div>', unsafe_allow_html=True)

soft_divider()

st.subheader("Coin items (instant)")
items = [
    {"id": "glass_theme", "name": "Glassy Theme Pack", "desc": "Smoother cards + subtle motion.", "cost": 150, "type": "coins"},
    {"id": "agent_boost", "name": "Agent Readiness Boost", "desc": "Unlocks the Agent checklist & extra prompts.", "cost": 250, "type": "coins"},
    {"id": "social_badge", "name": "Community Badge", "desc": "Adds a badge to your profile + small crowd score bump.", "cost": 200, "type": "coins"},
]
owned = set(user.get("inventory") or [])

for it in items:
    with st.container():
        cols = st.columns([3, 1])
        with cols[0]:
            st.markdown(
                '<div class="card">'
                f'<div style="font-weight:820">{it["name"]}</div>'
                f'<div style="color:var(--muted);margin-top:4px">{it["desc"]}</div>'
                f'<div style="margin-top:0.6rem;font-weight:800">{it["cost"]} coins</div>'
                '</div>',
                unsafe_allow_html=True,
            )
        with cols[1]:
            if it["id"] in owned:
                st.button("Owned", key=f"owned_{it['id']}", disabled=True, use_container_width=True)
            else:
                can = coins >= it["cost"]
                if st.button("Buy", key=f"buy_{it['id']}", disabled=not can, use_container_width=True):
                    user["coins"] = int(user.get("coins", 0)) - int(it["cost"])
                    user.setdefault("inventory", []).append(it["id"])
                    grant_xp(user, 10, "Shop", f"Bought {it['name']}")
                    add_notification(user, "Purchased", it["name"])
                    log_activity(user, f"Bought {it['name']} for {it['cost']} coins", icon="🛒")
                    # Small optional crowd bump for badge
                    if it["id"] == "social_badge":
                        crowd = user.setdefault("crowd", {"score": 50.0, "likes_received": 0, "likes_given": 0})
                        crowd["score"] = float(crowd.get("score", 50.0)) + 2.0
                    save_current_user()
                    st.rerun()

soft_divider()

st.subheader("Premium perks (testnet USDC)")
st.markdown(
    '<div class="card card-strong">'
    '<b>Judge-friendly:</b> These use Arc testnet USDC. The app generates a command; you run it locally; then paste the tx hash.'
    '</div>',
    unsafe_allow_html=True,
)

p1, p2 = st.columns(2)
with p1:
    st.markdown('<div class="card"><div style="font-weight:820">VIP Pass</div><div style="color:var(--muted);margin-top:4px">Unlock VIP shop drops + flex badge.</div><div style="margin-top:0.6rem;font-weight:900">$1.00 USDC</div></div>', unsafe_allow_html=True)
    if st.button("Buy with USDC →", key="shop_buy_vip", use_container_width=True, type="primary"):
        st.session_state["checkout_offer_id"] = "vip_pass"
        st.session_state["checkout_step"] = 2
        st.switch_page("pages/market.py")

with p2:
    st.markdown('<div class="card"><div style="font-weight:820">Creator Tip</div><div style="color:var(--muted);margin-top:4px">Tip the community treasury (demo).</div><div style="margin-top:0.6rem;font-weight:900">$0.10 USDC</div></div>', unsafe_allow_html=True)
    if st.button("Tip with USDC →", key="shop_buy_tip", use_container_width=True):
        st.session_state["checkout_offer_id"] = "creator_tip"
        st.session_state["checkout_step"] = 2
        st.switch_page("pages/market.py")
