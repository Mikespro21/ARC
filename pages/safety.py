import streamlit as st

from crowdlike.ui import apply_ui, hero, nav, soft_divider, status_bar, callout, metric_card, button_style
from crowdlike.settings import bool_setting
from crowdlike.auth import require_login, save_current_user
from crowdlike.game import ensure_user_schema, record_visit, grant_xp, add_notification
from crowdlike.agents import get_active_agent, agent_label
from crowdlike.market_data import get_markets
from crowdlike.performance import portfolio_value
from crowdlike.safety import trigger_panic, set_fraud_alert, check_safety_triggers, safety_exit
from crowdlike.layout import render_sidebar


st.set_page_config(page_title="Safety", page_icon="🛡️", layout="wide")
apply_ui()

user = require_login(app_name="Crowdlike")
ensure_user_schema(user)
record_visit(user, "safety")

render_sidebar(user, active_page="safety")

_demo = bool_setting("DEMO_MODE", True)
wallet = (user.get("wallet") or {}) if isinstance(user.get("wallet"), dict) else {}
_wallet_set = bool((wallet.get("address") or "").strip())
crowd = user.get("crowd") if isinstance(user.get("crowd"), dict) else {}
status_bar(wallet_set=_wallet_set, demo_mode=_demo, crowd_score=float(crowd.get("score", 50.0) or 50.0))

nav(active="Safety")
active = get_active_agent(user)

hero("🛡️ Safety", "One-click exits + automatic safety triggers. In production this would sell to USDC on-chain; here it updates the demo portfolio.", badge=agent_label(active))

# Prices for current holdings
coin_ids = []
port = active.get("portfolio") if isinstance(active.get("portfolio"), dict) else {}
pos = port.get("positions") if isinstance(port.get("positions"), dict) else {}
for cid, qty in pos.items():
    try:
        if abs(float(qty or 0.0)) > 1e-12:
            coin_ids.append(str(cid))
    except Exception:
        continue

price_map = {}
try:
    if coin_ids:
        rows = get_markets("usd", coin_ids[:45])
        price_map = {r.id: float(r.current_price) for r in rows}
except Exception:
    price_map = {}

value_now = portfolio_value(port, price_map)

# --- Overview ---
c1, c2, c3, c4 = st.columns(4)
with c1:
    metric_card("Agent", agent_label(active), "Safety scope", accent="blue")
with c2:
    metric_card("Value", f"${value_now:,.2f}", "Spot-priced", accent="purple")
with c3:
    s = active.get("safety") if isinstance(active.get("safety"), dict) else {}
    metric_card("Fraud alert", "ON" if s.get("fraud_alert") else "OFF", "Immediate exit", accent="none")
with c4:
    metric_card("Drawdown cap", f"{float((active.get('safety') or {}).get('max_drawdown_pct',25.0) or 25.0):.0f}%", "Auto exit", accent="none")

soft_divider()

# --- Controls ---
left, right = st.columns([1.15, 1.0])

with left:
    st.subheader("Safety controls")
    st.caption("These settings act on the active agent only.")

    s = active.setdefault("safety", {})
    if not isinstance(s, dict):
        s = {}
        active["safety"] = s

    max_dd = st.slider("Max drawdown before auto exit", min_value=5, max_value=80, value=int(float(s.get("max_drawdown_pct", 25.0) or 25.0)), step=1)
    s["max_drawdown_pct"] = float(max_dd)

    fraud = st.toggle("Fraud alert (forces immediate exit)", value=bool(s.get("fraud_alert")))
    set_fraud_alert(active, fraud)

    st.write("")

    b1, b2, b3 = st.columns(3)
    with b1:
        button_style("panic_btn", "bad")
        if st.button("Panic sell", key="panic_btn", use_container_width=True):
            st.session_state["safety_confirm_action"] = "panic"
    with b2:
        if st.button("Run safety check", use_container_width=True):
            ok, msg = check_safety_triggers(active, price_map)
            save_current_user()
            st.success(msg) if ok else st.info(msg)
    with b3:
        if st.button("Manual exit now", use_container_width=True):
            st.session_state["safety_confirm_action"] = "exit"

    # Confirm destructive actions (avoids mis-clicks during demos)
    act = str(st.session_state.get("safety_confirm_action") or "")
    if act in ("panic", "exit"):
        soft_divider()
        if act == "panic":
            callout(
                "warn",
                "Confirm: Panic sell",
                "This converts the agent's positions back to USDC in the demo. In production it would place sell orders on-chain.",
            )
        else:
            callout(
                "warn",
                "Confirm: Manual safety exit",
                "This immediately exits to USDC for the active agent (demo).",
            )
        c1, c2 = st.columns(2)
        with c1:
            button_style("safety_confirm_yes", "bad")
            if st.button("Confirm", key="safety_confirm_yes", use_container_width=True):
                if act == "panic":
                    trigger_panic(active)
                    ok, msg = check_safety_triggers(active, price_map)
                    if ok:
                        grant_xp(user, 20, "Safety", "Panic sell")
                        add_notification(user, "Panic sell executed", kind="warning")
                else:
                    ok, msg = safety_exit(active, price_map, "Manual safety exit")
                    if ok:
                        grant_xp(user, 20, "Safety", "Manual exit")
                        add_notification(user, "Exited to USDC", kind="success")

                st.session_state["safety_confirm_action"] = ""
                save_current_user()
                (st.success(msg) if ok else st.warning(msg))
                st.rerun()
        with c2:
            if st.button("Cancel", key="safety_confirm_no", use_container_width=True):
                st.session_state["safety_confirm_action"] = ""
                st.rerun()

    soft_divider()
    st.subheader("Recent safety events")
    last = (active.get("safety") or {}).get("last_exit")
    if last:
        st.markdown(
            '<div class="card">'
            f'<div style="font-weight:850">{last.get("reason","Exit")}</div>'
            f'<div style="color:var(--muted);margin-top:4px">{last.get("ts","")}</div>'
            f'<div style="margin-top:0.55rem">Value at exit: <b>${float(last.get("value",0.0) or 0.0):,.2f}</b> · Sold assets: <b>{int(last.get("sold_assets",0) or 0)}</b></div>'
            '</div>',
            unsafe_allow_html=True,
        )
    else:
        callout("info", "No exits yet", "When a trigger fires, you'll see an exit record here.")

with right:
    st.subheader("What happens in production")
    st.markdown(
        '<div class="card">'
        '<div style="font-weight:850">USDC safety exit</div>'
        '<div style="color:var(--muted);margin-top:6px">'
        'The vision calls for <b>selling positions into USDC immediately</b> and surfacing <b>panic sell</b> and <b>fraud alerts</b>. '
        'This demo keeps the UX but performs a local portfolio conversion.'
        '</div>'
        '<div style="margin-top:0.65rem">Suggested hard rails:</div>'
        '<ul style="margin-top:0.35rem;color:var(--muted)">'
        '<li>Per-agent limits + global daily caps</li>'
        '<li>Spend cadence limits (cooldown)</li>'
        '<li>Dual-confirm for high-risk settings</li>'
        '</ul>'
        '</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="card" style="margin-top:0.75rem">'
        '<div style="font-weight:850">Crowd influence</div>'
        '<div style="color:var(--muted);margin-top:6px">'
        'Crowd signals should <b>nudge</b> behavior, not remove safety. Keep adjustments gentle and auditable.'
        '</div>'
        '</div>',
        unsafe_allow_html=True,
    )

save_current_user()
