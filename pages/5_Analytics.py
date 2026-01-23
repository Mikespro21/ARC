from __future__ import annotations

import pandas as pd
import plotly.express as px
import streamlit as st

from crowdlike.state import ensure_state
from crowdlike.style import apply, card_start, card_end

st.set_page_config(page_title="Analytics • Crowdlike", page_icon="📊", layout="wide")
apply()
ensure_state()

agents = st.session_state["agents"]
crowd = st.session_state["crowdMetrics"]

st.markdown("# Analytics")
st.caption("High-level analytics for agents and crowd metrics (demo).")

if not agents:
    st.info("Create an agent first (Agents page).")
    st.stop()

adf = pd.DataFrame([{
    "Agent": a["name"],
    "Strategy": a["strategy"]["type"],
    "Risk": a["riskness"],
    "Profit %": a["performance"]["totalProfitPercent"],
    "Win Rate %": a["performance"]["winRate"],
    "Trades": a["performance"]["totalTrades"],
    "Deviation %": a["performance"]["crowdDeviation"],
} for a in agents])

c1, c2 = st.columns(2, gap="large")

with c1:
    card_start("Profit % by Agent")
    fig = px.bar(adf, x="Agent", y="Profit %")
    fig.update_layout(height=330, margin=dict(l=10,r=10,t=10,b=10))
    st.plotly_chart(fig, use_container_width=True)
    card_end()

with c2:
    card_start("Risk vs Profit %")
    fig = px.scatter(adf, x="Risk", y="Profit %", hover_name="Agent")
    fig.update_layout(height=330, margin=dict(l=10,r=10,t=10,b=10))
    st.plotly_chart(fig, use_container_width=True)
    card_end()

card_start("Crowd Benchmark")
st.markdown(
    f"""
- **Crowd avg risk:** {crowd['avgRiskness']}
- **Crowd avg trades/day:** {crowd['avgTradesPerDay']:.1f}
- **Crowd avg position size:** {crowd['avgPositionSize']:.0f}%
"""
)
card_end()

card_start("Agent Table")
st.dataframe(adf, use_container_width=True, hide_index=True)
card_end()
