import streamlit as st

from crowdlike.ui import apply_ui, nav, soft_divider, callout, metric_card, button_style
from crowdlike.layout import render_sidebar
from crowdlike.auth import require_login, save_current_user
from crowdlike.agents import get_active_agent, get_agents
from crowdlike.events import recent_events
from crowdlike.ui import event_feed
from crowdlike.game import ensure_user_schema

st.set_page_config(page_title="Crowdlike — Dashboard", page_icon="🚀", layout="wide")
apply_ui()

user = require_login("Crowdlike")
ensure_user_schema(user)

# v1.5: onboarding gate
if not st.session_state.get("onboard_complete") and not user.get("onboarded"):
    callout("You are in a fresh cloud session. Complete onboarding once for the smoothest flow.", tone="warning")
    button_style("dash_start_onb", "purple")
    if st.button("Start onboarding", key="dash_start_onb", use_container_width=True):
        st.switch_page("pages/journey.py")
    soft_divider()

render_sidebar(user)

# Highlight "Launch App" in the website-style top nav
nav(active="dashboard")

st.markdown("## Dashboard")

agents = get_agents(user)
active = get_active_agent(user)

c1, c2, c3 = st.columns([1.2, 1.0, 1.0], gap="large")
with c1:
    callout(
        "Your active agent",
        f"**{active.get('name','Agent')}** is selected. Use Agents to add more, or Coach to run a cycle.",
        tone="muted",
    )
with c2:
    metric_card("Agents", str(len(agents)), "Total agents")
with c3:
    metric_card("Activity", str(len(user.get("events", []))), "Recorded events")

soft_divider()

a, b, c = st.columns([1.0, 1.0, 1.0], gap="large")
with a:
    if st.button("🧠 Manage agents", key="dash_agents", use_container_width=True):
        st.switch_page("pages/agents.py")
with b:
    if st.button("🤖 Run in Coach", key="dash_coach", use_container_width=True):
        st.switch_page("pages/coach.py")
with c:
    if st.button("📈 Market / Checkout", key="dash_market", use_container_width=True):
        st.switch_page("pages/market.py")

soft_divider()

event_feed(recent_events(user, active), title="Recent activity", compact=True)

save_current_user()