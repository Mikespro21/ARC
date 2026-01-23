from __future__ import annotations

import streamlit as st

from crowdlike.state import ensure_state
from crowdlike.style import apply, card_start, card_end

st.set_page_config(
    page_title="Crowdlike",
    page_icon="🤖",
    layout="wide",
)

apply()
ensure_state()

st.markdown(
    """
# Welcome to Crowdlike

A personal finance app where AI agents paper‑trade and compare performance.
"""
)

c1, c2, c3 = st.columns(3, gap="large")
with c1:
    card_start("🤖 AI Agents", "Create and manage multiple AI trading agents with different strategies.")
    st.markdown("""- Build diverse portfolios
- Set risk levels and limits
- Track performance over time""")
    card_end()

with c2:
    card_start("📊 Real Market Data", "Paper trading with real market data (CoinGecko) with safe fallbacks.")
    st.markdown("""- Live prices (when available)
- Portfolio valuation
- Simple trading simulator""")
    card_end()

with c3:
    card_start("🏆 Leaderboards", "Compare performance across multiple timeframes.")
    st.markdown("""- Daily / Weekly / Monthly / Yearly
- Crowd benchmarks
- Score = profit × 100 + streaks""")
    card_end()

card_start("Getting Started")
st.markdown(
    """
1. **Dashboard**: overall performance, recent activity, and portfolio chart.
2. **Agents**: create agents, adjust status, and view positions and safety exits.
3. **Market**: paper trade against live market prices.
4. **Leaderboards**: see how your agents compare to the crowd.

This Streamlit build is **Option A**: pure Streamlit (no React build, no Node).
"""
)
card_end()

with st.sidebar:
    st.markdown("## Crowdlike")
    st.caption("Option A — Pure Streamlit")
    st.markdown("---")
    st.write("User:", st.session_state["user"]["name"])
    st.write("USDC balance:", f"${st.session_state['user']['usdcBalance']:,.2f}")
    st.markdown("---")
    if st.button("Reset demo state"):
        st.session_state["_cl_state_version"] = "reset"
        st.rerun()
