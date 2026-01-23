from __future__ import annotations

from datetime import datetime, timedelta
import random

import pandas as pd
import plotly.express as px
import streamlit as st

from crowdlike.state import ensure_state
from crowdlike.style import apply, card_start, card_end
from crowdlike.ui import fmt_usd

st.set_page_config(page_title="Dashboard • Crowdlike", page_icon="📈", layout="wide")
apply()
ensure_state()

user = st.session_state["user"]
agents = st.session_state["agents"]
crowd = st.session_state["crowdMetrics"]

st.markdown("# Dashboard")
st.caption(f"Welcome back, {user['name']}!")

active_agents = [a for a in agents if a["status"] == "active"]
total_portfolio = sum(a["portfolio"]["totalValue"] for a in agents)
total_profit = sum(a["performance"]["totalProfit"] for a in agents)
total_profit_pct = (total_profit / (total_portfolio - total_profit) * 100) if (total_portfolio - total_profit) else 0.0
active_positions = sum(len(a["portfolio"]["positions"]) for a in agents)
best = max(agents, key=lambda a: a["performance"]["totalProfitPercent"]) if agents else None

c1, c2, c3, c4 = st.columns(4, gap="large")
with c1:
    st.metric("Total Agents", f"{len(agents)}", f"{len(active_agents)} active")
with c2:
    st.metric("Total Portfolio Value", fmt_usd(total_portfolio), f"{total_profit_pct:+.2f}%")
with c3:
    if best:
        st.metric("Best Performer", best["name"], f"{best['performance']['totalProfitPercent']:+.2f}%")
    else:
        st.metric("Best Performer", "—", "0%")
with c4:
    st.metric("Active Positions", f"{active_positions}", f"{sum(a['performance']['totalTrades'] for a in agents)} total trades")

# Crowd metrics
card_start("Crowd Metrics")
cc1, cc2, cc3, cc4 = st.columns(4)
with cc1:
    st.metric("Total Agents", crowd["totalAgents"])
with cc2:
    st.metric("Avg Risk", crowd["avgRiskness"])
with cc3:
    st.metric("Avg Trades/Day", f"{crowd['avgTradesPerDay']:.1f}")
with cc4:
    st.metric("Total Volume", fmt_usd(crowd["totalVolume"]))
st.markdown("**Top Strategies**")
if crowd["topStrategies"]:
    st.markdown(" ".join([f"<span class='cl-pill'>{s['strategy']} ({s['count']})</span>" for s in crowd["topStrategies"]]), unsafe_allow_html=True)
else:
    st.caption("No strategies available.")
card_end()

# Recent activity (demo uses last trades)
card_start("Recent Activity")
activities = []
for a in agents:
    for t in a["portfolio"]["trades"][-5:]:
        activities.append({**t, "agentName": a["name"]})
activities.sort(key=lambda x: x.get("timestamp") or datetime.utcnow(), reverse=True)
activities = activities[:5]

if activities:
    df = pd.DataFrame([{
        "Agent": x["agentName"],
        "Type": x["type"].upper(),
        "Symbol": x["symbol"],
        "Amount": float(x["amount"]),
        "USDC": float(x["usdcAmount"]),
        "Time": (x.get("timestamp") or datetime.utcnow()).strftime("%H:%M:%S"),
    } for x in activities])
    st.dataframe(df, use_container_width=True, hide_index=True)
else:
    st.info("No recent activity. Go to Market to place paper trades, or create an agent.")
card_end()

# Performance chart (demo)
card_start("Portfolio Performance (30 Days)")
random.seed(7)  # stable demo chart
start = datetime.utcnow() - timedelta(days=29)
series = []
base = 10000.0
for i in range(30):
    base = base + random.uniform(-120, 180) + i * 5
    series.append({"day": (start + timedelta(days=i)).date().isoformat(), "value": base})
dfp = pd.DataFrame(series)
fig = px.line(dfp, x="day", y="value", markers=False)
fig.update_layout(height=320, margin=dict(l=10,r=10,t=10,b=10), xaxis_title="Day", yaxis_title="Value ($)")
st.plotly_chart(fig, use_container_width=True)
card_end()
