from __future__ import annotations

import streamlit as st

from crowdlike.state import ensure_state
from crowdlike.style import apply, card_start, card_end
from crowdlike.actions import daily_price

st.set_page_config(page_title="AI Coach • Crowdlike", page_icon="🧠", layout="wide")
apply()
ensure_state()

agents = st.session_state["agents"]
user = st.session_state["user"]
crowd = st.session_state["crowdMetrics"]

st.markdown("# AI Coach")
st.caption("Personalized trading advice, strategy optimization, and crowd-based insights (demo logic).")

def generate_response(user_message: str) -> str:
    lower = user_message.lower()

    if any(k in lower for k in ["strategy","improve","better"]):
        avg_profit = sum(a["performance"]["totalProfitPercent"] for a in agents) / (len(agents) or 1)
        return (
            f"Based on your current performance (avg {avg_profit:.2f}% profit), I recommend:\n\n"
            f"1. **Diversify Risk Levels**: Balance aggressive (70–100) with conservative (20–40).\n\n"
            f"2. **Leverage Crowd Learning**: Crowd avg risk is **{crowd['avgRiskness']}**.\n\n"
            f"3. **Monitor Win Rates**: Focus on agents with win rates above **55%**.\n\n"
            f"4. **Position Sizing**: Crowd avg is **{crowd['avgPositionSize']:.0f}%** per trade.\n\n"
            "Want recommendations for a specific agent?"
        )

    if "agent" in lower:
        if not agents:
            return "You currently have no agents. Create one in **Agents** to start."
        best = max(agents, key=lambda a: a["performance"]["totalProfitPercent"])
        worst = min(agents, key=lambda a: a["performance"]["totalProfitPercent"])
        return (
            "Agent Performance Analysis:\n\n"
            f"**Best Performer**: {best['name']}\n"
            f"- Profit: {best['performance']['totalProfitPercent']:.2f}%\n"
            f"- Strategy: {best['strategy']['type']}\n"
            f"- Win Rate: {best['performance']['winRate']:.0f}%\n\n"
            f"**Needs Attention**: {worst['name']}\n"
            f"- Profit: {worst['performance']['totalProfitPercent']:.2f}%\n"
            f"- Strategy: {worst['strategy']['type']}\n"
            f"- Win Rate: {worst['performance']['winRate']:.0f}%\n\n"
            f"**Recommendation**: Consider copying {best['name']}'s approach or adjusting {worst['name']}'s risk parameters."
        )

    if any(k in lower for k in ["market","buy","sell","trend"]):
        return (
            "Market Strategy Insights:\n\n"
            f"1. **Crowd Behavior**: {crowd['totalAgents']} active agents with avg {crowd['avgTradesPerDay']:.1f} trades/day.\n\n"
            f"2. **Popular Strategies**: {', '.join([s['strategy'] for s in crowd['topStrategies']]) or 'N/A'}.\n\n"
            f"3. **Risk Analysis**: Crowd avg risk is {crowd['avgRiskness']}.\n\n"
            f"4. **Position Sizing**: Stay within {crowd['avgPositionSize']:.0f}% ± 10% for stable risk-adjusted results."
        )

    if any(k in lower for k in ["safety","risk","loss","drawdown"]):
        return (
            "Safety & Risk Management Tips:\n\n"
            "1. **Exit Triggers**: Set max daily loss (10–15%) and max drawdown (20–30%).\n\n"
            "2. **Diversify**: Multiple agents with different strategies reduce risk concentration.\n\n"
            "3. **Monitor Deviation**: High crowd deviation can increase volatility.\n\n"
            "4. **Review Large Trades**: Even in paper mode, review outsized positions."
        )

    if any(k in lower for k in ["price","cost","pay"]):
        return (
            "Pricing Information (demo):\n\n"
            "**Formula**: Daily cost = (agentCount²) × (risk / 100)\n\n"
            f"- Agents: {len(agents)}\n"
            f"- Default Risk: {user['settings']['defaultRiskLevel']}\n"
            f"- Daily Cost: ${daily_price():.2f}\n"
            f"- Monthly Estimate: ${daily_price()*30:.2f}"
        )

    return (
        "I can help with:\n\n"
        "- Strategy optimization\n"
        "- Agent analysis\n"
        "- Market insights\n"
        "- Safety & risk management\n"
        "- Pricing (demo)\n\n"
        "Try: “How can I improve my strategy?” or “Analyze my agents performance”."
    )

# Init chat
if "coach_messages" not in st.session_state:
    st.session_state["coach_messages"] = [
        {"role": "assistant", "content": "Hello! I'm your AI Coach. How can I help you today?"}
    ]

# Quick prompts
qp1, qp2, qp3, qp4 = st.columns(4)
if qp1.button("Improve my strategy"):
    st.session_state["coach_draft"] = "How can I improve my trading strategy?"
if qp2.button("Agent analysis"):
    st.session_state["coach_draft"] = "Analyze my agents performance"
if qp3.button("Risk management"):
    st.session_state["coach_draft"] = "Give me safety and risk management tips"
if qp4.button("Market insights"):
    st.session_state["coach_draft"] = "What are the current market trends?"

# Chat display
card_start("Chat")
for m in st.session_state["coach_messages"]:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])
card_end()

prompt = st.chat_input("Ask your AI Coach...", key="coach_input")
draft = st.session_state.pop("coach_draft", None)
if draft and not prompt:
    prompt = draft

if prompt:
    st.session_state["coach_messages"].append({"role":"user","content":prompt})
    resp = generate_response(prompt)
    st.session_state["coach_messages"].append({"role":"assistant","content":resp})
    st.rerun()
