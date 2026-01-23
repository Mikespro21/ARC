from __future__ import annotations

import streamlit as st

from crowdlike.state import ensure_state
from crowdlike.style import apply, card_start, card_end
from crowdlike.actions import create_agent, toggle_agent_status, delete_agent, daily_price
from crowdlike.ui import fmt_usd, status_chip

st.set_page_config(page_title="Agents • Crowdlike", page_icon="🤖", layout="wide")
apply()
ensure_state()

user = st.session_state["user"]
agents = st.session_state["agents"]

st.markdown("# Your Agents")
st.caption(f"Managing {len(agents)} agent{'s' if len(agents)!=1 else ''} • Daily cost: ${daily_price():.2f}")

with st.expander("➕ Create Agent", expanded=False):
    with st.form("create_agent_form", clear_on_submit=True):
        name = st.text_input("Agent Name", placeholder="e.g., Agent Sigma")
        strategy = st.selectbox("Strategy", ["balanced","aggressive","conservative","swing","daytrading","hodl"], index=0)
        risk = st.slider("Risk (0–100)", 0, 100, 50)
        balance = st.number_input("Initial USDC Balance", min_value=100.0, max_value=float(user["usdcBalance"]), value=min(1000.0, float(user["usdcBalance"])), step=50.0)
        submitted = st.form_submit_button("Create")
        if submitted:
            if not name.strip():
                st.warning("Please enter an agent name.")
            else:
                create_agent(name.strip(), strategy, risk, float(balance))
                st.success("Agent created.")
                st.rerun()

if not agents:
    card_start("No Agents Yet", "Create your first agent to start paper trading.")
    card_end()
    st.stop()

cols = st.columns(2, gap="large")
for idx, a in enumerate(agents):
    col = cols[idx % 2]
    with col:
        card_start(f"{a['name']}", None)
        st.markdown(status_chip(a["status"]), unsafe_allow_html=True)
        st.markdown(
            f"""
- **Bot ID:** `{a['botId']}`
- **Strategy:** `{a['strategy']['type']}`
- **Risk:** {a['riskness']}/100
- **USDC Balance:** {fmt_usd(a['portfolio']['usdcBalance'])}
- **Total Value:** {fmt_usd(a['portfolio']['totalValue'])}
- **Total Profit:** {fmt_usd(a['performance']['totalProfit'])} ({a['performance']['totalProfitPercent']:+.2f}%)
"""
        )

        b1, b2, b3 = st.columns(3)
        with b1:
            if st.button("Details", key=f"details_{a['id']}"):
                st.session_state["selected_agent_id"] = a["id"]
                st.session_state["show_agent_details"] = True
        with b2:
            if st.button("Pause/Play", key=f"toggle_{a['id']}"):
                toggle_agent_status(a["id"])
                st.rerun()
        with b3:
            if st.button("Delete", key=f"delete_{a['id']}"):
                delete_agent(a["id"])
                st.rerun()

        card_end()

# Agent details modal-like section (Streamlit doesn't have true modals in core)
if st.session_state.get("show_agent_details") and st.session_state.get("selected_agent_id"):
    aid = st.session_state["selected_agent_id"]
    agent = next((x for x in st.session_state["agents"] if x["id"] == aid), None)
    if agent:
        st.markdown("---")
        card_start(f"{agent['name']} Details")
        c1, c2 = st.columns(2)
        with c1:
            st.write("Bot ID:", f"`{agent['botId']}`")
        with c2:
            st.write("USDC Balance:", fmt_usd(agent["portfolio"]["usdcBalance"]))

        st.subheader("Performance Metrics")
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Total Profit", fmt_usd(agent["performance"]["totalProfit"]))
        m2.metric("Streaks", agent["performance"]["streaks"])
        m3.metric("Max Drawdown", f"{agent['performance']['maxDrawdown']:.2f}%")
        m4.metric("Crowd Deviation", f"{agent['performance']['crowdDeviation']:.0f}%")

        st.subheader(f"Current Positions ({len(agent['portfolio']['positions'])})")
        if agent["portfolio"]["positions"]:
            for p in agent["portfolio"]["positions"]:
                st.markdown(
                    f"**{p['symbol']}** — {p['amount']:.4f} @ ${p['averagePrice']:.2f} | Value {fmt_usd(p['value'])} | P/L {p['profitLossPercent']:+.2f}%"
                )
        else:
            st.caption("No open positions.")

        st.subheader("Safety Exits")
        for ex in agent["settings"]["safetyExits"]:
            label = "Max Daily Loss" if ex["type"] == "max_daily_loss" else ("Max Drawdown" if ex["type"] == "max_drawdown" else "Fraud Alert")
            st.write(f"- **{label}** — Threshold: {ex['threshold']:.0f}% — {'Enabled' if ex['enabled'] else 'Disabled'}")

        if st.button("Close details"):
            st.session_state["show_agent_details"] = False
            st.session_state["selected_agent_id"] = None
            st.rerun()

        card_end()
