import streamlit as st

from crowdlike.ui import apply_ui, hero, nav, soft_divider, status_bar, callout, event_feed, metric_card
from crowdlike.settings import bool_setting
from crowdlike.tour import maybe_run_tour
from crowdlike.auth import require_login, save_current_user
from crowdlike.game import ensure_user_schema, record_visit, grant_xp, log_activity
from crowdlike.agents import get_active_agent, agent_label, get_agents
from crowdlike.layout import render_sidebar
from crowdlike.events import log_event, recent_events
from crowdlike.orchestrator import propose_next_action, decide_auto_execute
from crowdlike.crowd_deviation import cohort_for_agent, deviation_pct
from crowdlike.copying import apply_copy
from crowdlike.audit import log_audit
from crowdlike.market_data import get_markets


st.set_page_config(page_title="Coach", page_icon="🤖", layout="wide")
apply_ui()

user = require_login(app_name="Crowdlike")
ensure_user_schema(user)
record_visit(user, "coach")

render_sidebar(user, active_page="coach")

_demo = bool_setting("DEMO_MODE", True)
wallet = (user.get("wallet") or {}) if isinstance(user.get("wallet"), dict) else {}
_wallet_set = bool((wallet.get("address") or "").strip())
_crowd = user.get("crowd") if isinstance(user.get("crowd"), dict) else {}
status_bar(wallet_set=_wallet_set, demo_mode=_demo, crowd_score=float(_crowd.get("score", 50.0) or 50.0))

nav(active="Coach")
active_agent = get_active_agent(user)

hero("🤖 Coach", "Generate proposals, approve actions, and keep a trustless audit trail.", badge=agent_label(active_agent))

maybe_run_tour(user, "coach")

# Prices (best-effort; improves realistic mirroring)
WATCHLIST = ["bitcoin","ethereum","solana","matic-network","usd-coin","tether"]
try:
    rows = get_markets("usd", WATCHLIST)
    price_map = {r.id: float(r.current_price) for r in rows}
except Exception:
    price_map = {}

# --- Autonomy mode ---
mode = str(active_agent.get("mode") or "assist")
mode = st.select_slider(
    "Autonomy mode",
    options=["off", "assist", "auto"],
    value=mode if mode in ("off", "assist", "auto") else "assist",
    help="assist = proposes actions that require approval. auto = may auto-execute *practice trades* when within constraints.",
)
active_agent["mode"] = mode

soft_divider()

# --- Crowd deviation constraint (spec) ---
pol = user.get("policy") if isinstance(user.get("policy"), dict) else {}
try:
    max_dev = float(pol.get("max_deviation_pct", 20.0) or 20.0)
except Exception:
    max_dev = 20.0
max_dev = st.slider("Max crowd deviation (%)", min_value=0.0, max_value=50.0, value=float(max_dev), step=1.0, help="Actions beyond this deviation are constrained by safety/approval logic.")
pol["max_deviation_pct"] = float(max_dev)
user["policy"] = pol

cohort = cohort_for_agent(user, active_agent)
dev, metrics, perc = deviation_pct(user, active_agent, cohort_agents=cohort, price_map=price_map)

c1, c2, c3 = st.columns(3)
with c1:
    metric_card("Current deviation", f"{dev:.1f}%", "Average distance from cohort medians (percentile-based)")
with c2:
    metric_card("Riskness", f"{metrics['riskness']:.0f}/100", f"Percentile: {perc['riskness']:.0f}")
with c3:
    metric_card("Trades/day", f"{metrics['trades_per_day']:.2f}", f"Percentile: {perc['trades_per_day']:.0f}")

if dev > max_dev:
    callout(
        "warn",
        "Out of bounds",
        "This agent is deviating beyond your configured maximum. Auto-execution is blocked; approvals are required.",
    )

soft_divider()

# --- Proposal generator ---
st.markdown("### Proposals")
st.caption("Proposals are queued for approval. Payments always require manual confirmation in the demo.")

colA, colB = st.columns([1.0, 1.0])
with colA:
    if st.button("Generate proposal", type="primary", use_container_width=True):
        p = propose_next_action(user, active_agent)
        log_event(user, kind="agent", title="New proposal", details=str(p.get("title","")), severity="info", agent_id=str(active_agent.get("id")))
        grant_xp(user, 20, "Coach", "Generated proposal")
        st.success(f"Queued: {p.get('title')}")
        # Auto-execute if permitted
        if decide_auto_execute(user, active_agent, p):
            # emulate clicking approve for trades
            p["status"] = "approved"
            _run_auto = True
        else:
            _run_auto = False

        save_current_user(user)
        if _run_auto:
            st.rerun()

with colB:
    st.write("")
    st.write("")

# Auto-exec path: if agent is in auto and last proposal is trade and allowed, execute it immediately.
if mode == "auto" and isinstance(active_agent.get("approvals"), list) and active_agent["approvals"]:
    latest = active_agent["approvals"][0]
    if isinstance(latest, dict) and latest.get("status") == "approved" and latest.get("type") == "trade":
        # execute trade and then remove
        payload = latest.get("payload") or {}
        asset = str(payload.get("asset") or "").strip()
        side = str(payload.get("side","BUY")).upper()
        try:
            qty = float(payload.get("qty", 0.0) or 0.0)
        except Exception:
            qty = 0.0
        px = float(price_map.get(asset, 0.0) or 0.0) or 100.0
        notional = qty * px

        port = active_agent.get("portfolio") if isinstance(active_agent.get("portfolio"), dict) else {}
        port.setdefault("cash_usdc", 1000.0)
        port.setdefault("positions", {})
        port.setdefault("trades", [])

        cash = float(port.get("cash_usdc") or 0.0)
        positions = port.get("positions") if isinstance(port.get("positions"), dict) else {}
        cur_qty = float(positions.get(asset, 0.0) or 0.0)

        ok = False
        if side == "BUY":
            if cash >= notional:
                cash -= notional
                cur_qty += qty
                ok = True
        else:
            if cur_qty >= qty:
                cash += notional
                cur_qty -= qty
                ok = True

        if ok:
            positions[asset] = cur_qty
            port["positions"] = {k: v for k, v in positions.items() if abs(float(v or 0.0)) > 1e-12}
            port["cash_usdc"] = float(cash)
            trades = port.get("trades") if isinstance(port.get("trades"), list) else []
            trades.insert(0, {"ts": latest.get("ts"), "asset": asset, "side": side, "qty": qty, "price": px, "notional": round(notional,2), "auto": True})
            port["trades"] = trades[:200]
            active_agent["portfolio"] = port

            log_event(user, kind="trade", title=f"Auto trade executed", details=f"{side} {qty} {asset} @ ${px:.2f}", severity="success", agent_id=str(active_agent.get("id")))
            log_audit(user, kind="auto_execute", msg=f"Auto-executed trade {side} {asset} qty={qty}", agent_id=str(active_agent.get("id")), proposal_id=str(latest.get("id")))
            log_activity(user, f"Auto trade {side} {asset}", icon="🤖")
        else:
            log_event(user, kind="agent", title="Auto trade blocked", details="Insufficient balance/position.", severity="warn", agent_id=str(active_agent.get("id")))
            log_audit(user, kind="auto_block", msg="Auto trade blocked due to balance/position.", agent_id=str(active_agent.get("id")), proposal_id=str(latest.get("id")), severity="warn")

        # remove proposal regardless to prevent loops
        try:
            active_agent["approvals"].remove(latest)
        except Exception:
            pass
        save_current_user(user)
        st.rerun()

soft_divider()

# --- Pending approvals ---
st.markdown("### Pending approvals")
approvals = active_agent.get("approvals") if isinstance(active_agent.get("approvals"), list) else []
if not approvals:
    st.info("No pending approvals yet. Generate a proposal above.")
else:
    for i, p in enumerate(list(approvals)[:12]):
        if not isinstance(p, dict):
            continue
        with st.container(border=True):
            st.markdown(f"**{p.get('title','Proposal')}**")
            st.caption(f"Type: {p.get('type')} · ID: {p.get('id')}")

            cons = p.get("constraints") if isinstance(p.get("constraints"), dict) else {}
            if cons:
                st.caption(f"Deviation: {float(cons.get('deviation_pct',0.0)):.1f}% (max {float(cons.get('max_deviation_pct',0.0)):.1f}%)")

            cols = st.columns([1.0, 1.0])
            with cols[0]:
                if st.button("Approve", key=f"appr_yes_{i}", use_container_width=True, type="primary"):
                    typ = str(p.get("type") or "")
                    payload = p.get("payload") or {}

                    if typ == "trade":
                        asset = str(payload.get("asset") or "").strip()
                        side = str(payload.get("side","BUY")).upper()
                        qty = float(payload.get("qty", 0.0) or 0.0)
                        px = float(price_map.get(asset, 0.0) or 0.0) or 100.0
                        notional = qty * px

                        port = active_agent.get("portfolio") if isinstance(active_agent.get("portfolio"), dict) else {}
                        port.setdefault("cash_usdc", 1000.0)
                        port.setdefault("positions", {})
                        port.setdefault("trades", [])

                        cash = float(port.get("cash_usdc") or 0.0)
                        positions = port.get("positions") if isinstance(port.get("positions"), dict) else {}
                        cur_qty = float(positions.get(asset, 0.0) or 0.0)

                        ok = False
                        if side == "BUY":
                            if cash >= notional:
                                cash -= notional
                                cur_qty += qty
                                ok = True
                        else:
                            if cur_qty >= qty:
                                cash += notional
                                cur_qty -= qty
                                ok = True

                        if ok:
                            positions[asset] = cur_qty
                            port["positions"] = {k: v for k, v in positions.items() if abs(float(v or 0.0)) > 1e-12}
                            port["cash_usdc"] = float(cash)
                            trades = port.get("trades") if isinstance(port.get("trades"), list) else []
                            trades.insert(0, {"ts": p.get("ts"), "asset": asset, "side": side, "qty": qty, "price": px, "notional": round(notional,2)})
                            port["trades"] = trades[:200]
                            active_agent["portfolio"] = port

                            log_event(user, kind="trade", title="Approved trade (demo)", details=f"{side} {qty} {asset} @ ${px:.2f}", severity="success", agent_id=str(active_agent.get("id")))
                            log_audit(user, kind="approve", msg=f"Approved trade {side} {asset} qty={qty}", agent_id=str(active_agent.get("id")), proposal_id=str(p.get("id")))
                            grant_xp(user, 35, "Coach", "Approved trade")
                        else:
                            log_event(user, kind="agent", title="Trade blocked", details="Insufficient balance/position.", severity="warn", agent_id=str(active_agent.get("id")))
                            log_audit(user, kind="approve_block", msg="Trade approval blocked due to balance/position.", agent_id=str(active_agent.get("id")), proposal_id=str(p.get("id")), severity="warn")

                    elif typ == "payment":
                        amt = float(((payload or {}).get("amount_usdc")) or 0.0)
                        log_event(user, kind="payment", title="Payment approved (demo)", details=f"Approved intent for {amt:.2f} USDC. Use Market → Testnet checkout to execute on-chain.", severity="warn", agent_id=str(active_agent.get("id")))
                        log_audit(user, kind="approve", msg=f"Approved payment intent {amt:.2f} USDC", agent_id=str(active_agent.get("id")), proposal_id=str(p.get("id")))
                        grant_xp(user, 20, "Coach", "Approved payment intent")

                    elif typ == "copy":
                        src_id = str((payload or {}).get("source_agent_id") or "")
                        mode2 = str((payload or {}).get("mode") or "")
                        src_agent = None
                        for a in get_agents(user):
                            if str(a.get("id")) == src_id:
                                src_agent = a
                                break
                        if not src_agent:
                            log_event(user, kind="agent", title="Copy failed", details="Source agent not found.", severity="warn", agent_id=str(active_agent.get("id")))
                            log_audit(user, kind="approve_block", msg="Copy approval failed: source not found.", agent_id=str(active_agent.get("id")), proposal_id=str(p.get("id")), severity="warn")
                        else:
                            ok, msg = apply_copy(user, dest_agent=active_agent, source_agent=src_agent, mode=mode2, price_map=price_map)
                            if ok:
                                log_audit(user, kind="approve", msg=f"Approved copy: {mode2} from {src_agent.get('bot_id','')}", agent_id=str(active_agent.get("id")), proposal_id=str(p.get("id")))
                                grant_xp(user, 25, "Coach", "Approved copy")
                            else:
                                log_audit(user, kind="approve_block", msg=f"Copy blocked: {msg}", agent_id=str(active_agent.get("id")), proposal_id=str(p.get("id")), severity="warn")
                                st.warning(msg)
                    else:
                        log_event(user, kind="agent", title="Approved proposal", details=str(p.get("title","")), severity="success", agent_id=str(active_agent.get("id")))
                        log_audit(user, kind="approve", msg=f"Approved proposal {p.get('title','')}", agent_id=str(active_agent.get("id")), proposal_id=str(p.get("id")))

                    # remove proposal
                    try:
                        active_agent["approvals"].remove(p)
                    except Exception:
                        pass
                    save_current_user(user)
                    st.rerun()

            with cols[1]:
                if st.button("Reject", key=f"appr_no_{i}", use_container_width=True):
                    try:
                        active_agent["approvals"].remove(p)
                    except Exception:
                        pass
                    log_event(user, kind="agent", title="Rejected proposal", details=str(p.get("title","")), severity="info", agent_id=str(active_agent.get("id")))
                    log_audit(user, kind="reject", msg=f"Rejected proposal {p.get('title','')}", agent_id=str(active_agent.get("id")), proposal_id=str(p.get("id")))
                    save_current_user(user)
                    st.rerun()

soft_divider()

st.markdown("### Recent events")
ev = recent_events(user, limit=12)
event_feed(ev)

save_current_user()
