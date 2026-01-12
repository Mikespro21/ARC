import streamlit as st

from crowdlike.ui import apply_ui, hero, nav, soft_divider, status_bar, callout
from crowdlike.settings import bool_setting
from crowdlike.auth import require_login, save_current_user
from crowdlike.game import ensure_user_schema, record_visit
from crowdlike.agents import get_agents
from crowdlike.pricing import quote_daily
from crowdlike.layout import render_sidebar

st.set_page_config(page_title="Pricing", page_icon="💳", layout="wide")
apply_ui()

user = require_login(app_name="Crowdlike")
ensure_user_schema(user)
record_visit(user, "pricing")

render_sidebar(user, active_page="pricing")

_demo = bool_setting("DEMO_MODE", True)
wallet = (user.get("wallet") or {}) if isinstance(user.get("wallet"), dict) else {}
_wallet_set = bool((wallet.get("address") or "").strip())
crowd = user.get("crowd") if isinstance(user.get("crowd"), dict) else {}
status_bar(wallet_set=_wallet_set, demo_mode=_demo, crowd_score=float(crowd.get("score", 50.0) or 50.0))

nav(active="Pricing")
hero("💳 Pricing", "Pay-per-day with exponential scaling as you add agents and raise risk/autonomy.", badge="Monetization")

callout(
    "info",
    "Why pay-per-day?",
    "The vision describes daily billing that grows non-linearly with agent count, risk, and autonomy. This page is a transparent demo estimator (not final pricing).",
)

agents = get_agents(user)

c1, c2, c3 = st.columns([1.0, 1.0, 1.0])
with c1:
    n = st.number_input("Number of agents", min_value=1, max_value=200, value=max(1, len(agents)), step=1)
with c2:
    risk = st.slider("Risk level", min_value=0, max_value=100, value=int((user.get("policy") or {}).get("risk", 25) or 25))
with c3:
    autonomy = st.selectbox("Autonomy", options=["manual", "assist", "auto"], index=1)

q = quote_daily(int(n), float(risk), autonomy=str(autonomy))

soft_divider()

m1, m2, m3 = st.columns(3)
with m1:
    st.metric("Total / day", f"${q.total_per_day:,.2f}")
with m2:
    st.metric("Per-agent / day", f"${q.per_agent_per_day:,.2f}")
with m3:
    st.metric("Est. / month", f"${(q.total_per_day * 30.0):,.2f}")

st.markdown(
    '<div class="card">'
    '<div style="font-weight:850">How this demo estimate works</div>'
    '<div style="color:var(--muted);margin-top:6px">'
    'We use a base cost per agent/day, then apply (1) a non-linear risk multiplier, (2) an autonomy multiplier, '
    'and (3) exponential scaling on agent count. The goal is to reflect the <b>shape</b> of the model in the vision.'
    '</div>'
    '</div>',
    unsafe_allow_html=True,
)

soft_divider()

st.subheader("Example tiers")
examples = [
    (1, 15, "manual"),
    (5, 25, "assist"),
    (20, 40, "assist"),
    (100, 70, "auto"),
]

st.dataframe(
    [
        {
            "Agents": a,
            "Risk": r,
            "Autonomy": au,
            "Total/day": round(quote_daily(a, r, au).total_per_day, 2),
            "Total/month": round(quote_daily(a, r, au).total_per_day * 30.0, 2),
        }
        for a, r, au in examples
    ],
    use_container_width=True,
    hide_index=True,
)

save_current_user()
