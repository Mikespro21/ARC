import streamlit as st

from crowdlike.ui import apply_ui, hero, nav, soft_divider, status_bar, callout
from crowdlike.settings import bool_setting
from crowdlike.auth import require_login, save_current_user
from crowdlike.game import ensure_user_schema, record_visit
from crowdlike.agents import get_agents, get_active_agent, agent_label
from crowdlike.market_data import get_markets
from crowdlike.performance import portfolio_value, ensure_daily_snapshot, returns_windows, since_inception


st.set_page_config(page_title="Compare", page_icon="📊", layout="wide")
apply_ui()

user = require_login(app_name="Crowdlike")
ensure_user_schema(user)
record_visit(user, "compare")

_demo = bool_setting("DEMO_MODE", True)
wallet = (user.get("wallet") or {}) if isinstance(user.get("wallet"), dict) else {}
_wallet_set = bool((wallet.get("address") or "").strip())
crowd = user.get("crowd") if isinstance(user.get("crowd"), dict) else {}
status_bar(wallet_set=_wallet_set, demo_mode=_demo, crowd_score=float(crowd.get("score", 50.0) or 50.0))

nav(active="Compare")
hero("📊 Compare", "Rank agents by profit and percent return across daily / weekly / monthly / yearly — all at once.", badge="Performance")

agents = get_agents(user)
active = get_active_agent(user)

if not agents:
    callout("warn", "No agents", "Create at least one agent in the Agents page.")
    st.stop()

# Fetch prices for all holdings (best effort)
coin_ids = set()
for a in agents:
    port = a.get("portfolio") if isinstance(a.get("portfolio"), dict) else {}
    pos = port.get("positions") if isinstance(port.get("positions"), dict) else {}
    for cid, qty in pos.items():
        try:
            if abs(float(qty or 0.0)) > 1e-12:
                coin_ids.add(str(cid))
        except Exception:
            continue

ids_list = list(coin_ids)[:45]
price_map = {}
try:
    if ids_list:
        rows = get_markets("usd", ids_list)
        price_map = {r.id: float(r.current_price) for r in rows}
except Exception:
    price_map = {}

rows = []
for a in agents:
    port = a.get("portfolio") if isinstance(a.get("portfolio"), dict) else {}
    v = portfolio_value(port, price_map)
    ensure_daily_snapshot(a, v)
    inc = since_inception(a, v)
    win = returns_windows(a, v)
    rows.append(
        {
            "id": str(a.get("id")),
            "agent": agent_label(a),
            "value": v,
            "profit": inc["profit"],
            "return_pct": inc["return_pct"],
            "daily_profit": win["daily"]["profit"],
            "daily_return": win["daily"]["return_pct"],
            "weekly_profit": win["weekly"]["profit"],
            "weekly_return": win["weekly"]["return_pct"],
            "monthly_profit": win["monthly"]["profit"],
            "monthly_return": win["monthly"]["return_pct"],
            "yearly_profit": win["yearly"]["profit"],
            "yearly_return": win["yearly"]["return_pct"],
        }
    )

save_current_user()

# --- Simultaneous top rankings ---
colA, colB, colC, colD = st.columns(4)


def _top_by(key: str):
    return sorted(rows, key=lambda r: float(r.get(key, 0.0) or 0.0), reverse=True)[:1]


def _card(col, title, key_profit, key_ret):
    best = _top_by(key_profit)
    if not best:
        return
    b = best[0]
    with col:
        st.markdown(
            '<div class="card">'
            f'<div style="font-weight:860">{title}</div>'
            f'<div style="margin-top:0.35rem;font-weight:900;font-size:1.05rem">{b["agent"]}</div>'
            f'<div style="margin-top:0.55rem">'
            f'<span class="pill info"><span class="k">Profit</span><span>${float(b[key_profit]):,.2f}</span></span>'
            f'<span class="pill"><span class="k">Return</span><span>{float(b[key_ret]):+.2f}%</span></span>'
            f'</div>'
            '</div>',
            unsafe_allow_html=True,
        )


_card(colA, "Daily", "daily_profit", "daily_return")
_card(colB, "Weekly", "weekly_profit", "weekly_return")
_card(colC, "Monthly", "monthly_profit", "monthly_return")
_card(colD, "Yearly", "yearly_profit", "yearly_return")

soft_divider()

# --- Detailed tables ---

tabD, tabW, tabM, tabY, tabAll = st.tabs(["Daily", "Weekly", "Monthly", "Yearly", "Since inception"])


def _table(tab, profit_k: str, ret_k: str):
    with tab:
        items = sorted(rows, key=lambda r: float(r.get(profit_k, 0.0) or 0.0), reverse=True)
        # Compact table
        st.dataframe(
            [
                {
                    "Agent": r["agent"],
                    "Value ($)": round(float(r["value"]), 2),
                    "Profit ($)": round(float(r[profit_k]), 2),
                    "Return (%)": round(float(r[ret_k]), 2),
                }
                for r in items
            ],
            use_container_width=True,
            hide_index=True,
        )


_table(tabD, "daily_profit", "daily_return")
_table(tabW, "weekly_profit", "weekly_return")
_table(tabM, "monthly_profit", "monthly_return")
_table(tabY, "yearly_profit", "yearly_return")
_table(tabAll, "profit", "return_pct")

soft_divider()

# --- Active agent history ---
st.subheader("Active agent history")
st.caption("Value snapshots are recorded once per day (local demo storage).")

hist = active.get("value_history") if isinstance(active.get("value_history"), list) else []
pts = []
for row in reversed(hist[-60:]):
    if not isinstance(row, dict):
        continue
    try:
        pts.append(float(row.get("v")))
    except Exception:
        continue

if pts:
    st.line_chart(pts, height=240)
else:
    callout("info", "No history yet", "Make a practice trade or revisit tomorrow to build a history curve.")

st.caption("Tip: switch your active agent in Agents to view a different history.")

save_current_user()
