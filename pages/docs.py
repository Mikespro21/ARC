import streamlit as st
from crowdlike.ui import apply_ui, nav, soft_divider, callout

from crowdlike.site import site_header, site_footer

st.set_page_config(page_title="Crowdlike — Docs", page_icon="📚", layout="wide")
apply_ui()

site_header(active="Docs")
nav(active="Docs")

st.markdown("## Docs")
st.write("This is the official demo documentation for Crowdlike (local-first).")

soft_divider()

callout(
    "Quickstart",
    "1) Launch App → 2) Create an agent → 3) Add wallet (testnet) → 4) Set limits → 5) Run a cycle in Coach → 6) Verify receipt in Market",
    tone="muted",
)

soft_divider()

col1, col2 = st.columns([1.1, 1.1], gap="large")
with col1:
    st.markdown("### Safety model")
    st.write("- Safety exits can force the agent to cash (USDC in demo).")
    st.write("- Max deviation blocks auto-execution and routes actions to approvals.")
    st.write("- Panic controls are intentionally one-click but confirmed.")
with col2:
    st.markdown("### Autonomy ladder")
    st.write("- OFF: no proposals")
    st.write("- ASSIST: proposes, requires approve")
    st.write("- AUTO: executes within tight caps")
    st.write("- AUTO+: higher caps if trust signals are strong")

soft_divider()

st.markdown("### FAQ")
with st.expander("Does Crowdlike store private keys?"):
    st.write("No. The demo is designed so keys are not stored by default. Testnet checkout uses an external wallet flow.")
with st.expander("What is crowd deviation?"):
    st.write("A percentile-based distance from the cohort median across behavioral metrics (riskness, trades/day, position size).")
with st.expander("What does the leaderboard score mean?"):
    st.write("Score = (profit * 100) + streaks, where streaks count consecutive profitable periods.")

site_footer()
