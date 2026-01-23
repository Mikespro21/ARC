from __future__ import annotations

import datetime as dt
import random
from typing import List

import pandas as pd
import plotly.express as px
import requests
import streamlit as st

from crowdlike.data import (
    generate_mock_user,
    generate_mock_agents,
    calculate_crowd_metrics,
    generate_leaderboard,
    Agent,
    CrowdMetrics,
)
from crowdlike.ui import inject_global_css, sidebar_nav, hero_title, page_title, card

st.set_page_config(page_title="Crowdlike", layout="wide", initial_sidebar_state="expanded")
inject_global_css()

# --------- App state ----------
if "user" not in st.session_state:
    st.session_state.user = generate_mock_user()
if "agents" not in st.session_state:
    st.session_state.agents = generate_mock_agents(4, user_id=st.session_state.user.id)
if "crowd_metrics" not in st.session_state:
    st.session_state.crowd_metrics = calculate_crowd_metrics(generate_mock_agents(100))
if "page" not in st.session_state:
    st.session_state.page = "home"

# --------- Navigation ----------
chosen = sidebar_nav(st.session_state.page)
if chosen != st.session_state.page:
    st.session_state.page = chosen
    st.rerun()

user = st.session_state.user
agents: List[Agent] = st.session_state.agents
crowd: CrowdMetrics = st.session_state.crowd_metrics

# --------- Data helpers ----------
def coingecko_markets():
    ids = ["bitcoin","ethereum","solana","cardano","polkadot","binancecoin","ripple","dogecoin"]
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        "vs_currency": "usd",
        "ids": ",".join(ids),
        "order": "market_cap_desc",
        "per_page": 50,
        "page": 1,
        "sparkline": "false",
        "price_change_percentage": "24h",
    }
    try:
        r = requests.get(url, params=params, timeout=10)
        r.raise_for_status()
        return r.json()
    except Exception:
        return None

# --------- Pages ----------
def page_home():
    hero_title("Welcome to Crowdlike", "A personal finance app where AI agents trade and compare performance")

    col1, col2, col3 = st.columns(3, gap="large")
    with col1:
        card("""
            <div style="font-size:2.25rem; margin-bottom:0.75rem;">🤖</div>
            <div style="font-weight:900; font-size:1.1rem; margin-bottom:0.35rem;">AI Agents</div>
            <div class="c-muted">Create and manage multiple AI trading agents with different strategies</div>
        """)
    with col2:
        card("""
            <div style="font-size:2.25rem; margin-bottom:0.75rem;">📊</div>
            <div style="font-weight:900; font-size:1.1rem; margin-bottom:0.35rem;">Real Market Data</div>
            <div class="c-muted">Paper trading with real-time market data from CoinGecko</div>
        """)
    with col3:
        card("""
            <div style="font-size:2.25rem; margin-bottom:0.75rem;">🏆</div>
            <div style="font-weight:900; font-size:1.1rem; margin-bottom:0.35rem;">Leaderboards</div>
            <div class="c-muted">Compare agent performance across daily, weekly, and monthly timeframes</div>
        """)

    st.markdown('<div style="height: 1.5rem;"></div>', unsafe_allow_html=True)

    card("""
      <div style="font-weight:900; font-size:1.6rem; margin-bottom:1rem;">Getting Started</div>
      <div style="display:flex; flex-direction:column; gap:0.9rem;">
        <div style="display:flex; gap:0.75rem; align-items:flex-start;">
          <div style="width:2rem; height:2rem; border-radius:999px; background:#3b82f6; color:white; display:flex; align-items:center; justify-content:center; font-weight:900;">1</div>
          <div>
            <div style="font-weight:900;">Create Your First Agent</div>
            <div class="c-muted">Navigate to the Agents page and set up your AI trading agent</div>
          </div>
        </div>
        <div style="display:flex; gap:0.75rem; align-items:flex-start;">
          <div style="width:2rem; height:2rem; border-radius:999px; background:#8b5cf6; color:white; display:flex; align-items:center; justify-content:center; font-weight:900;">2</div>
          <div>
            <div style="font-weight:900;">Configure Strategy</div>
            <div class="c-muted">Set risk levels, trading limits, and safety parameters</div>
          </div>
        </div>
        <div style="display:flex; gap:0.75rem; align-items:flex-start;">
          <div style="width:2rem; height:2rem; border-radius:999px; background:#db2777; color:white; display:flex; align-items:center; justify-content:center; font-weight:900;">3</div>
          <div>
            <div style="font-weight:900;">Start Trading</div>
            <div class="c-muted">Monitor performance and watch your agents compete on the leaderboard</div>
          </div>
        </div>
      </div>
    """)

def page_dashboard():
    page_title("Dashboard", "Overview of your agents, portfolio value, and crowd signals")

    active_agents = [a for a in agents if a.status == "active"]
    total_portfolio_value = sum(a.portfolio.totalValue for a in agents)
    total_profit = sum(a.performance.totalProfit for a in agents)
    denom = (total_portfolio_value - total_profit)
    total_profit_percent = (total_profit / denom * 100) if denom else 0
    active_positions = sum(len(a.portfolio.positions) for a in agents)
    best = max(agents, key=lambda a: a.performance.totalProfitPercent) if agents else None

    c1, c2, c3, c4 = st.columns(4, gap="large")
    with c1:
        card(f"""
            <div style="display:flex; justify-content:space-between; align-items:flex-start;">
              <div>
                <div class="c-muted" style="font-weight:800;">Total Agents</div>
                <div style="font-size:2rem; font-weight:900; margin-top:0.25rem;">{len(agents)}</div>
                <div class="c-muted" style="margin-top:0.2rem;">{len(active_agents)} active</div>
              </div>
              <div style="font-size:2rem;">🤖</div>
            </div>
        """)
    with c2:
        card(f"""
            <div style="display:flex; justify-content:space-between; align-items:flex-start;">
              <div>
                <div class="c-muted" style="font-weight:800;">Total Portfolio Value</div>
                <div style="font-size:2rem; font-weight:900; margin-top:0.25rem;">${total_portfolio_value:,.2f}</div>
                <div class="c-muted" style="margin-top:0.2rem;">{total_profit_percent:+.2f}%</div>
              </div>
              <div style="font-size:2rem;">💰</div>
            </div>
        """)
    with c3:
        card(f"""
            <div style="display:flex; justify-content:space-between; align-items:flex-start;">
              <div>
                <div class="c-muted" style="font-weight:800;">Best Performer</div>
                <div style="font-size:1.2rem; font-weight:900; margin-top:0.35rem;">{best.name if best else "None"}</div>
                <div class="c-muted" style="margin-top:0.2rem;">{(best.performance.totalProfitPercent if best else 0):+.2f}%</div>
              </div>
              <div style="font-size:2rem;">🏆</div>
            </div>
        """)
    with c4:
        card(f"""
            <div style="display:flex; justify-content:space-between; align-items:flex-start;">
              <div>
                <div class="c-muted" style="font-weight:800;">Active Positions</div>
                <div style="font-size:2rem; font-weight:900; margin-top:0.25rem;">{active_positions}</div>
                <div class="c-muted" style="margin-top:0.2rem;">{sum(a.performance.totalTrades for a in agents)} total trades</div>
              </div>
              <div style="font-size:2rem;">📈</div>
            </div>
        """)

    st.markdown('<div style="height: 1.25rem;"></div>', unsafe_allow_html=True)

    left, right = st.columns([2,1], gap="large")
    with left:
        perf = [{"day": i+1, "value": 10000 + random.random()*3000 + (i*100)} for i in range(30)]
        df = pd.DataFrame(perf)
        fig = px.line(df, x="day", y="value")
        fig.update_layout(margin=dict(l=10,r=10,t=10,b=10), height=320)
        card("<div style='font-weight:900; font-size:1.25rem; margin-bottom:0.75rem;'>Portfolio Performance (30d)</div>")
        st.plotly_chart(fig, use_container_width=True)
    with right:
        card(f"""
          <div style="font-weight:900; font-size:1.25rem; margin-bottom:0.75rem;">Crowd Signals</div>
          <div style="display:flex; flex-direction:column; gap:0.6rem;">
            <div><span class="c-muted">Similarity Score:</span> <b>{crowd.similarityScore:.0f}%</b></div>
            <div><span class="c-muted">Momentum Score:</span> <b>{crowd.momentumScore:.0f}%</b></div>
            <div><span class="c-muted">Strain Score:</span> <b>{crowd.strainScore:.0f}%</b></div>
            <div><span class="c-muted">Avg Risk:</span> <b>{crowd.avgRiskness}</b></div>
            <div><span class="c-muted">Avg Position Size:</span> <b>{crowd.avgPositionSize:.0f}%</b></div>
          </div>
        """)

def page_agents():
    page_title("Your Agents", "Create, manage, and compare your AI trading agents")

    top_left, top_right = st.columns([2,1], gap="large")
    with top_left:
        st.markdown(
            """
            <div class="c-card c-card-pad">
              <div style="display:flex; align-items:center; justify-content:space-between;">
                <div>
                  <div style="font-weight:900; font-size:1.4rem;">Plan</div>
                  <div class="c-muted">Daily price (demo): <b>$3.00</b></div>
                </div>
                <div style="font-size:2rem;">⚡</div>
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with top_right:
        with st.expander("➕ Create Agent", expanded=False):
            name = st.text_input("Agent name", value="")
            strategy = st.selectbox("Strategy", ["aggressive","conservative","balanced","swing","daytrading","hodl"], index=2)
            risk = st.slider("Riskness", 0, 100, 50)
            balance = st.number_input("Initial balance (USDC)", min_value=100, value=1000, step=100)
            if st.button("Create", type="primary"):
                if len(agents) >= user.settings.maxAgents:
                    st.error("Max agents reached for this account.")
                else:
                    from crowdlike.data import AgentStrategy, generate_mock_agents
                    new = generate_mock_agents(1, user_id=user.id)[0]
                    new.id = f"agent_{len(agents)+1}"
                    new.name = name.strip() or new.name
                    new.strategy = AgentStrategy(type=strategy)
                    new.riskness = int(risk)
                    new.portfolio.totalValue = float(balance)
                    new.portfolio.usdcBalance = float(balance) * 0.3
                    st.session_state.agents = agents + [new]
                    st.success("Agent created.")
                    st.rerun()

    st.markdown('<div style="height: 0.75rem;"></div>', unsafe_allow_html=True)

    for a in st.session_state.agents:
        status_badge = {"active":"🟢 Active", "paused":"🟡 Paused", "exited":"🔴 Exited"}[a.status]
        profit = a.performance.totalProfitPercent
        arrow = "📈" if profit >= 0 else "📉"

        st.markdown(
            f"""
            <div class="c-card c-card-pad" style="margin-bottom: 0.75rem;">
              <div style="display:flex; align-items:flex-start; justify-content:space-between; gap:1rem;">
                <div style="min-width: 18rem;">
                  <div style="display:flex; align-items:center; gap:0.6rem;">
                    <div style="font-weight:900; font-size:1.25rem;">{a.name}</div>
                    <div class="c-muted" style="font-weight:800;">{a.botId}</div>
                  </div>
                  <div class="c-muted" style="margin-top:0.25rem;">{status_badge} • Strategy: <b>{a.strategy.type}</b> • Risk: <b>{a.riskness}</b></div>
                </div>

                <div style="display:flex; gap:1.5rem; align-items:center; flex-wrap:wrap;">
                  <div>
                    <div class="c-muted" style="font-weight:800;">Portfolio</div>
                    <div style="font-weight:900; font-size:1.25rem;">${a.portfolio.totalValue:,.2f}</div>
                  </div>
                  <div>
                    <div class="c-muted" style="font-weight:800;">Profit</div>
                    <div style="font-weight:900; font-size:1.25rem;">{profit:+.2f}% {arrow}</div>
                  </div>
                  <div>
                    <div class="c-muted" style="font-weight:800;">Win Rate</div>
                    <div style="font-weight:900; font-size:1.25rem;">{a.performance.winRate:.0f}%</div>
                  </div>
                </div>
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        b1, b2, b3 = st.columns([1,1,3])
        with b1:
            if st.button("▶/⏸ Toggle", key=f"toggle_{a.id}"):
                a.status = "paused" if a.status == "active" else "active"
                st.rerun()
        with b2:
            if st.button("🗑 Delete", key=f"del_{a.id}"):
                st.session_state.agents = [x for x in st.session_state.agents if x.id != a.id]
                st.rerun()
        with b3:
            with st.expander("View details", expanded=False):
                st.write({
                    "strategy": a.strategy.type,
                    "riskness": a.riskness,
                    "settings": {
                        "maxPositionSize": round(a.settings.maxPositionSize, 2),
                        "maxTradesPerDay": a.settings.maxTradesPerDay,
                        "autoApprove": a.settings.autoApprove,
                    },
                    "performance": {
                        "profitPercent": round(a.performance.totalProfitPercent, 2),
                        "winRate": round(a.performance.winRate, 1),
                        "drawdown": round(a.performance.maxDrawdown, 1),
                        "crowdDeviation": round(a.performance.crowdDeviation, 1),
                    },
                })

def page_coach():
    page_title("AI Coach", "Insights and recommendations based on your agents and crowd behavior")

    if "coach_messages" not in st.session_state:
        st.session_state.coach_messages = [{
            "role": "assistant",
            "content": "Hello! I'm your AI Coach. I can help you optimize your trading strategies, analyze agent performance, and provide insights based on crowd behavior. How can I assist you today?",
            "ts": dt.datetime.now(),
        }]

    for m in st.session_state.coach_messages:
        if m["role"] == "assistant":
            card(f"<div style='font-weight:900; margin-bottom:0.35rem;'>🧠 Coach</div><div style='white-space:pre-wrap;'>{m['content']}</div>")
        else:
            card(f"<div style='font-weight:900; margin-bottom:0.35rem;'>You</div><div style='white-space:pre-wrap;'>{m['content']}</div>")
        st.markdown('<div style="height: 0.6rem;"></div>', unsafe_allow_html=True)

    prompt = st.text_area("Ask your coach", height=90, placeholder="Ask about strategy, performance, risk, or crowd signals...")
    if st.button("Send", type="primary"):
        if prompt.strip():
            st.session_state.coach_messages.append({"role":"user","content":prompt.strip(),"ts":dt.datetime.now()})

            lower = prompt.lower()
            if "strategy" in lower or "improve" in lower or "better" in lower:
                avg_profit = sum(a.performance.totalProfitPercent for a in agents) / (len(agents) or 1)
                content = (
                    f"Based on your current performance (avg {avg_profit:.2f}% profit), I recommend:\n\n"
                    f"1. **Diversify Risk Levels**: Balance aggressive (risk 70–100) and conservative (risk 20–40) agents.\n\n"
                    f"2. **Leverage Crowd Learning**: The crowd's average risk is {crowd.avgRiskness}. Agents closer to this tend to perform consistently.\n\n"
                    f"3. **Monitor Win Rates**: Focus on agents with win rates above 55%. Adjust underperformers.\n\n"
                    f"4. **Position Sizing**: Crowd average is {crowd.avgPositionSize:.0f}% per trade. Align your agents with or slightly beat this.\n\n"
                    "Would you like specific recommendations for any particular agent?"
                )
            elif "agent" in lower:
                best = max(agents, key=lambda a: a.performance.totalProfitPercent) if agents else None
                content = (
                    f"Your strongest agent right now is **{best.name if best else 'N/A'}**.\n\n"
                    "For next steps, consider:\n"
                    "- Lowering risk on any agent with high drawdown\n"
                    "- Increasing max trades/day only for agents with consistent win rates\n"
                    "- Keeping deviation from the crowd under your safety threshold"
                )
            else:
                content = (
                    "I can help with:\n\n"
                    "- Strategy tuning (risk, position size, trade frequency)\n"
                    "- Identifying your best/worst agents\n"
                    "- Understanding crowd similarity and momentum\n\n"
                    "Ask me about a specific agent or goal."
                )

            st.session_state.coach_messages.append({"role":"assistant","content":content,"ts":dt.datetime.now()})
            st.rerun()

def page_market():
    page_title("Market", "Real-time market data (CoinGecko) with demo fallback")

    data = coingecko_markets()
    if data is None:
        st.warning("CoinGecko unavailable right now — showing demo prices.")
        data = [{
            "name": name,
            "symbol": sym.lower(),
            "current_price": base * random.uniform(0.95, 1.05),
            "price_change_percentage_24h": random.uniform(-5, 5),
        } for sym, name, base in [
            ("BTC","Bitcoin",43000),
            ("ETH","Ethereum",2300),
            ("SOL","Solana",90),
            ("ADA","Cardano",0.5),
            ("DOT","Polkadot",7.0),
            ("BNB","BNB",300),
            ("XRP","XRP",0.55),
            ("DOGE","Dogecoin",0.08),
        ]]

    df = pd.DataFrame([{
        "Asset": d.get("name",""),
        "Symbol": str(d.get("symbol","")).upper(),
        "Price (USD)": float(d.get("current_price") or 0),
        "24h %": float(d.get("price_change_percentage_24h") or 0),
    } for d in data])

    card("<div style='font-weight:900; font-size:1.25rem; margin-bottom:0.75rem;'>Market Overview</div>")
    st.dataframe(df, use_container_width=True, hide_index=True)

def page_analytics():
    page_title("Analytics", "Deeper insights into agents and portfolio trends")

    df = pd.DataFrame([{
        "Agent": a.name,
        "Risk": a.riskness,
        "Profit%": a.performance.totalProfitPercent,
        "WinRate%": a.performance.winRate,
    } for a in agents])

    left, right = st.columns(2, gap="large")
    with left:
        fig = px.scatter(df, x="Risk", y="Profit%", hover_name="Agent")
        fig.update_layout(margin=dict(l=10,r=10,t=10,b=10), height=360)
        card("<div style='font-weight:900; font-size:1.25rem; margin-bottom:0.75rem;'>Risk vs Profit</div>")
        st.plotly_chart(fig, use_container_width=True)
    with right:
        fig2 = px.bar(df, x="Agent", y="WinRate%")
        fig2.update_layout(margin=dict(l=10,r=10,t=10,b=10), height=360)
        card("<div style='font-weight:900; font-size:1.25rem; margin-bottom:0.75rem;'>Win Rates</div>")
        st.plotly_chart(fig2, use_container_width=True)

def page_leaderboards():
    page_title("Leaderboards", "Compare performance across timeframes")

    tab_daily, tab_weekly, tab_monthly, tab_yearly = st.tabs(["Daily","Weekly","Monthly","Yearly"])
    for tab in [tab_daily, tab_weekly, tab_monthly, tab_yearly]:
        with tab:
            entries = generate_leaderboard(agents, size=10)
            df = pd.DataFrame([{
                "Rank": e.rank,
                "Bot ID": e.botId,
                "Name": e.name,
                "Profit %": f"{e.profitPercent:+.2f}%",
                "Win Rate": f"{e.winRate:.0f}%",
                "Risk": e.riskness,
            } for e in entries])
            card("<div style='font-weight:900; font-size:1.25rem; margin-bottom:0.75rem;'>Top Agents</div>")
            st.dataframe(df, use_container_width=True, hide_index=True)

def page_safety():
    page_title("Safety", "Guardrails, limits, and crowd deviation controls")

    left, right = st.columns([1,1], gap="large")
    with left:
        card("""
          <div style="font-weight:900; font-size:1.25rem; margin-bottom:0.75rem;">Crowd Deviation</div>
          <div class="c-muted">Keep agents within a safe behavioral envelope. High deviation can trigger exits.</div>
        """)
        st.metric("Max deviation (account)", f"{user.settings.maxDeviationPercent}%")
        st.metric("Crowd similarity score", f"{crowd.similarityScore:.0f}%")
    with right:
        card("""
          <div style="font-weight:900; font-size:1.25rem; margin-bottom:0.75rem;">Safety Exits</div>
          <div class="c-muted">Configure agent exits based on daily loss, drawdown, or fraud signals.</div>
        """)
        st.write("In this Streamlit rebuild, exits are demo-configured per agent (editable in Agents → details).")

def page_profile():
    page_title("Profile", "Your account and preferences")

    card(f"""
      <div style="display:flex; align-items:center; justify-content:space-between;">
        <div>
          <div style="font-weight:900; font-size:1.4rem;">{user.name}</div>
          <div class="c-muted">{user.email}</div>
        </div>
        <div style="font-size:2rem;">👤</div>
      </div>
    """)
    st.markdown('<div style="height: 1rem;"></div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3, gap="large")
    with c1:
        st.metric("USDC Balance", f"${user.usdcBalance:,.2f}")
    with c2:
        st.metric("Max Agents", user.settings.maxAgents)
    with c3:
        st.metric("Default Risk Level", user.settings.defaultRiskLevel)

router = {
    "home": page_home,
    "dashboard": page_dashboard,
    "agents": page_agents,
    "coach": page_coach,
    "market": page_market,
    "analytics": page_analytics,
    "leaderboards": page_leaderboards,
    "safety": page_safety,
    "profile": page_profile,
}

router.get(st.session_state.page, page_home)()
