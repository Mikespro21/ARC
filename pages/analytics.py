import streamlit as st

from crowdlike.ui import apply_ui, hero, nav, soft_divider, status_bar, metric_card, callout
from crowdlike.auth import require_login, save_current_user
from crowdlike.game import ensure_user_schema, record_visit
from crowdlike.layout import render_sidebar
from crowdlike.agents import get_agents, get_active_agent, set_active_agent, agent_label
from crowdlike.market_data import get_markets
from crowdlike.analytics import agents_table, compute_agent_metrics


st.set_page_config(page_title="Analytics • Crowdlike", page_icon="📊", layout="wide")
apply_ui()

user = require_login()
ensure_user_schema(user)
record_visit(user, "analytics")

render_sidebar(active="Analytics")
nav(active="Analytics")
hero("Analytics", "Portfolio metrics, autonomy behavior, and run reports that make the app feel real.")

agents = get_agents(user)
active_agent = get_active_agent(user)

# --- price map for all coins we hold (best effort) ---
coin_ids = set()
for a in agents:
    port = a.get("portfolio") if isinstance(a.get("portfolio"), dict) else {}
    pos = port.get("positions") if isinstance(port.get("positions"), dict) else {}
    for cid, qty in pos.items():
        try:
            if float(qty or 0.0) > 1e-12:
                coin_ids.add(str(cid))
        except Exception:
            continue

price_map = {}
try:
    if coin_ids:
        rows = get_markets("usd", list(coin_ids))
        price_map = {r.id: float(r.current_price) for r in rows}
except Exception:
    price_map = {}

# --- Agent selector ---
with st.container():
    cols = st.columns([1.2, 2.2, 1.0])
    with cols[0]:
        st.subheader("Selected agent")
    with cols[1]:
        labels = [agent_label(a) for a in agents]
        ids = [str(a.get("id")) for a in agents]
        cur = str(active_agent.get("id"))
        try:
            idx = ids.index(cur)
        except Exception:
            idx = 0
        pick = st.selectbox("Agent", options=list(range(len(ids))), format_func=lambda i: labels[i], index=idx, label_visibility="collapsed")
        if ids[pick] != cur:
            set_active_agent(user, ids[pick])
            save_current_user()
            st.rerun()
    with cols[2]:
        st.caption("Tip: Run cycles from Coach to generate Run Reports.")

soft_divider()

# --- Overview table (all agents) ---
st.subheader("All agents snapshot")
rows = agents_table(user, agents, price_map)
if rows:
    st.dataframe(rows, use_container_width=True, hide_index=True)
else:
    callout("No agents yet. Create one in Agents.", tone="warning")

soft_divider()

# --- Selected agent analytics ---
st.subheader(f"Agent details • {agent_label(active_agent)}")
m = compute_agent_metrics(user, active_agent, price_map)

c1, c2, c3, c4 = st.columns(4)
with c1:
    metric_card("Value", f"${m['value_usdc']:.2f}", "Current portfolio value (cash + spot)")
with c2:
    metric_card("Profit", f"${(m['since'] or {}).get('profit', 0.0):.2f}", "Since inception (demo)")
with c3:
    metric_card("Return", f"{(m['since'] or {}).get('return_pct', 0.0):.2f}%", "Since inception (demo)")
with c4:
    metric_card("Deviation", f"{m['deviation_pct']:.1f}%", "Crowd deviation (lower = closer to cohort)")

c5, c6, c7, c8 = st.columns(4)
with c5:
    metric_card("Max drawdown", f"{m['max_drawdown_pct']:.2f}%", "Worst peak→trough from snapshots")
with c6:
    metric_card("Volatility", f"{m['volatility_proxy_pct']:.2f}%", "Std-dev of daily returns (proxy)")
with c7:
    metric_card("Runs", str(m["runs_total"]), "Run cycles generated")
with c8:
    metric_card("Pending approvals", str(m["approvals_pending"]), "Items waiting in Coach")

soft_divider()

# Charts & timelines
left, right = st.columns([1.2, 1.0])
with left:
    st.markdown("### Value history")
    hist = active_agent.get("value_history") if isinstance(active_agent.get("value_history"), list) else []
    if hist:
        # hist is newest-first; plot oldest-first
        xs = list(reversed(hist))
        chart = {"date": [r.get("d") for r in xs], "value": [r.get("v") for r in xs]}
        st.line_chart(chart, x="date", y="value", height=260)
    else:
        callout("No value history yet. Make a practice trade or run a cycle.", tone="muted")

with right:
    st.markdown("### Window returns")
    w = m.get("windows") or {}
    for k in ["daily", "weekly", "monthly", "yearly"]:
        row = w.get(k) or {}
        st.write(f"**{k.title()}**  •  ${row.get('profit', 0.0):.2f}  ({row.get('return_pct', 0.0):.2f}%)")

soft_divider()

st.subheader("Run reports (last 25)")
runs = active_agent.get("runs") if isinstance(active_agent.get("runs"), list) else []
if not runs:
    callout("No runs yet. Go to Coach → Run agent cycle.", tone="muted")
else:
    filt = st.selectbox("Filter", options=["All", "Executed", "Queued"], index=0)
    show = []
    for r in runs[:60]:
        if not isinstance(r, dict):
            continue
        if filt == "Executed" and not r.get("executed"):
            continue
        if filt == "Queued" and not r.get("queued"):
            continue
        show.append({
            "ts": r.get("ts"),
            "autonomy": (r.get("autonomy") or {}).get("effective"),
            "proposal": (r.get("proposal") or {}).get("title") if isinstance(r.get("proposal"), dict) else "",
            "decision": (r.get("decision") or {}).get("reason") if isinstance(r.get("decision"), dict) else "",
        })
        if len(show) >= 25:
            break
    st.dataframe(show, use_container_width=True, hide_index=True)

status_bar(user)
save_current_user()
