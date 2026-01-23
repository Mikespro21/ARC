from __future__ import annotations

import streamlit as st

from crowdlike.state import ensure_state, recompute_metrics
from crowdlike.style import apply, card_start, card_end

st.set_page_config(page_title="Profile • Crowdlike", page_icon="👤", layout="wide")
apply()
ensure_state()

user = st.session_state["user"]

st.markdown("# Profile")
st.caption("User settings and preferences (demo).")

card_start("Account")
st.write("Name:", user["name"])
st.write("Email:", user["email"])
st.write("USDC Balance:", f"${user['usdcBalance']:,.2f}")
card_end()

card_start("Settings")
with st.form("settings_form"):
    max_agents = st.slider("Max Agents", 1, 25, int(user["settings"]["maxAgents"]))
    default_risk = st.slider("Default Risk Level", 0, 100, int(user["settings"]["defaultRiskLevel"]))
    max_dev = st.slider("Max Deviation from Crowd (%)", 0, 100, int(user["settings"]["maxDeviationPercent"]))
    notifications = st.checkbox("Notifications", value=bool(user["settings"]["notifications"]))
    saved = st.form_submit_button("Save settings")
    if saved:
        user["settings"]["maxAgents"] = int(max_agents)
        user["settings"]["defaultRiskLevel"] = int(default_risk)
        user["settings"]["maxDeviationPercent"] = int(max_dev)
        user["settings"]["notifications"] = bool(notifications)
        recompute_metrics()
        st.success("Settings saved.")
card_end()

card_start("About this build")
st.markdown(
    """
This is **Option A**: a full rebuild in Streamlit.

- No React build.
- Works on Streamlit Cloud as-is.
- UI is styled with a light blue → white → purple gradient and glass cards.
"""
)
card_end()
