from __future__ import annotations

import streamlit as st

from crowdlike.state import ensure_state
from crowdlike.style import apply, card_start, card_end
from crowdlike.ui import status_chip

st.set_page_config(page_title="Safety • Crowdlike", page_icon="🛡️", layout="wide")
apply()
ensure_state()

agents = st.session_state["agents"]
user = st.session_state["user"]

st.markdown("# Safety")
st.caption("Risk controls and safety exits for agents (demo configuration).")

card_start("Principles")
st.markdown(
    """
- **Paper trading**: this demo does not execute real trades.
- **Safety exits**: each agent can have max daily loss, max drawdown, and fraud alert thresholds.
- **Crowd deviation**: large deviation from the crowd can increase volatility.
"""
)
card_end()

if not agents:
    st.info("Create an agent first (Agents page).")
    st.stop()

for a in agents:
    card_start(f"{a['name']}")
    st.markdown(status_chip(a["status"]), unsafe_allow_html=True)
    st.markdown(f"**Risk:** {a['riskness']}/100 • **Strategy:** `{a['strategy']['type']}`")
    st.markdown("**Safety Exits**")
    for ex in a["settings"]["safetyExits"]:
        label = "Max Daily Loss" if ex["type"] == "max_daily_loss" else ("Max Drawdown" if ex["type"] == "max_drawdown" else "Fraud Alert")
        st.write(f"- {label}: {ex['threshold']:.0f}% — {'Enabled' if ex['enabled'] else 'Disabled'}")
    card_end()

card_start("Suggested defaults")
st.markdown(
    """
- Max daily loss: **10–15%**
- Max drawdown: **20–30%**
- Review any single trade above **15–25%** of portfolio
"""
)
card_end()
