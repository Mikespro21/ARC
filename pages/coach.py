import streamlit as st

from crowdlike.ui import apply_ui, hero, nav, soft_divider, status_bar, callout, event_feed
from crowdlike.settings import bool_setting
from crowdlike.tour import maybe_run_tour, tour_complete_step
from crowdlike.auth import require_login, save_current_user
from crowdlike.game import ensure_user_schema, record_visit, grant_xp, add_notification, log_activity, compute_streak, xp_progress
from crowdlike.agents import get_active_agent, agent_label
from crowdlike.layout import render_sidebar
from crowdlike.events import log_event, recent_events
from crowdlike.orchestrator import propose_next_action, decide_auto_execute


st.set_page_config(page_title="Coach", page_icon="🤖", layout="wide")
apply_ui()

user = require_login(app_name="Crowdlike")

maybe_run_tour(user, current_page="coach")
ensure_user_schema(user)
record_visit(user, "coach")

render_sidebar(user, active_page="coach")

nav(active="Coach")
active_agent = get_active_agent(user)
hero("🤖 Coach", "A friendly concierge for quests, market moves, and safe testnet checkout.", badge=agent_label(active_agent))

# Reduce demo confusion with a tiny status strip
_demo = bool_setting("DEMO_MODE", True)
_wallet_set = bool(((user.get("wallet") or {}) if isinstance(user.get("wallet"), dict) else {}).get("address"))
_crowd = user.get("crowd") if isinstance(user.get("crowd"), dict) else {}
status_bar(wallet_set=_wallet_set, demo_mode=_demo, crowd_score=float(_crowd.get("score", 50.0) or 50.0))


# --- Agent Command Console ---
st.markdown("## Agent command console")
st.caption("Generate proposals, approve actions, and keep a clean audit trail. Payments always require confirmation.")

# Agent mode (per-agent, overrides user-level)
mode = str(active_agent.get("mode") or "assist")
mode = st.select_slider(
    "Autonomy mode",
    options=["off", "assist", "auto"],
    value=mode if mode in ("off","assist","auto") else "assist",
    help="assist = proposes actions requiring approval. auto = can auto-execute *trades* only (payments still require confirmation).",
)
active_agent["mode"] = mode

cA, cB, cC = st.columns([1,1,2])
with cA:
    if st.button("Generate next action", type="primary", use_container_width=True, disabled=(mode=="off")):
        p = propose_next_action(user, active_agent)
        if p:
            log_event(user, kind="agent", title="Agent proposed an action", details=p.get("title",""), severity="info", agent_id=str(active_agent.get("id")))
            st.toast("Proposal generated.", icon="🧠")
        else:
            st.toast("Nothing to propose right now.", icon="✅")
        save_current_user(user)
        st.rerun()

with cB:
    if st.button("Clear pending", use_container_width=True):
        active_agent["approvals"] = []
        log_event(user, kind="agent", title="Cleared pending proposals", details="", severity="warn", agent_id=str(active_agent.get("id")))
        save_current_user(user)
        st.rerun()

with cC:
    st.caption("Tip: in demos, generate 1 proposal, approve it, then show the Activity feed on Home.")

pending = active_agent.get("approvals") if isinstance(active_agent.get("approvals"), list) else []
if pending:
    st.markdown("### Pending approvals")
    for i, p in enumerate(list(pending)):
        with st.container():
            st.markdown(f"**{p.get('title','(proposal)')}**")
            st.caption(f"{p.get('type','')} · {p.get('ts','')}")
            col1, col2, col3 = st.columns([1,1,3])
            with col1:
                if st.button("Approve", key=f"appr_ok_{i}", use_container_width=True):
                    # Demo execution
                    typ = p.get("type")
                    port = active_agent.get("portfolio") if isinstance(active_agent.get("portfolio"), dict) else {}
                    cash = float(port.get("cash_usdc", 0.0) or 0.0)
                    if typ == "trade":
                        payload = p.get("payload") or {}
                        asset = payload.get("asset","BTC")
                        side = payload.get("side","BUY")
                        qty = float(payload.get("qty", 0.0) or 0.0)
                        px = 100.0  # placeholder demo price index
                        notional = qty * px
                        pos = port.get("positions") if isinstance(port.get("positions"), dict) else {}
                        cur_qty = float((pos.get(asset) or {}).get("qty", 0.0) or 0.0)
                        if side == "BUY":
                            if cash >= notional:
                                cash -= notional
                                cur_qty += qty
                            else:
                                st.warning("Not enough demo cash for this trade.")
                        else:
                            sell_qty = min(cur_qty, qty)
                            cur_qty -= sell_qty
                            cash += sell_qty * px
                        pos[asset] = {"qty": round(cur_qty, 6), "avg": px}
                        port["positions"] = pos
                        port["cash_usdc"] = round(cash, 2)
                        trades = port.get("trades") if isinstance(port.get("trades"), list) else []
                        trades.insert(0, {"ts": p.get("ts"), "asset": asset, "side": side, "qty": qty, "price": px, "notional": round(notional,2)})
                        port["trades"] = trades[:200]
                        active_agent["portfolio"] = port
                        log_event(user, kind="trade", title=f"Approved {side} {qty} {asset}", details=f"~${notional:.2f} (demo)", severity="success", agent_id=str(active_agent.get("id")))
                    elif typ == "payment":
                        amt = float(((p.get("payload") or {}).get("amount_usdc")) or 0.0)
                        log_event(user, kind="payment", title="Payment requires manual checkout", details=f"Proposed ${amt:.2f} USDC — go to Market → Checkout.", severity="warn", agent_id=str(active_agent.get("id")))
                    else:
                        log_event(user, kind="agent", title="Approved proposal", details=str(p.get("title","")), severity="success", agent_id=str(active_agent.get("id")))
                    # remove proposal
                    try:
                        active_agent["approvals"].remove(p)
                    except Exception:
                        pass
                    save_current_user(user)
                    st.rerun()
            with col2:
                if st.button("Reject", key=f"appr_no_{i}", use_container_width=True):
                    try:
                        active_agent["approvals"].remove(p)
                    except Exception:
                        pass
                    log_event(user, kind="agent", title="Rejected proposal", details=str(p.get("title","")), severity="info", agent_id=str(active_agent.get("id")))
                    save_current_user(user)
                    st.rerun()
            with col3:
                st.caption("Approving trades executes a demo portfolio change. Payments route you to Checkout.")
            soft_divider()
else:
    st.caption("No pending proposals. Generate one to show the full agent loop.")

soft_divider()
event_feed(recent_events(user, agent_id=str(active_agent.get("id")), limit=12), title="Agent activity")




# Simple chat state
if "coach_messages" not in st.session_state:
    st.session_state.coach_messages = [
        {"role": "assistant", "content": "Hey! I’m your Coach. Tell me what you want to do: earn XP, buy a drop, or set up wallet checkout."}
    ]

for m in st.session_state.coach_messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

suggest_cols = st.columns(4)
with suggest_cols[0]:
    if st.button("Earn XP fast", key="coach_s1"):
        st.session_state.coach_messages.append({"role":"user","content":"How do I earn XP fast?"})
with suggest_cols[1]:
    if st.button("Set up wallet", key="coach_s2"):
        st.session_state.coach_messages.append({"role":"user","content":"Help me set up my wallet."})
with suggest_cols[2]:
    if st.button("What to buy?", key="coach_s3"):
        st.session_state.coach_messages.append({"role":"user","content":"What should I buy in the shop?"})
with suggest_cols[3]:
    if st.button("Explain testnet", key="coach_s4"):
        st.session_state.coach_messages.append({"role":"user","content":"What is testnet?"})

prompt = st.chat_input("Message Coach…")
if prompt:
    st.session_state.coach_messages.append({"role":"user","content":prompt})

# Generate responses for any new user messages without a following assistant message
def _answer(text: str) -> str:
    t = (text or "").lower()

    wallet = (user.get("wallet") or {}).get("address","")
    streak = compute_streak(user.get("active_days") or [])
    lvl, xp_in, xp_to_next, pct = xp_progress(int(user.get("xp", 0)))
    friends = user.get("friends") or []
    trades = (user.get("portfolio") or {}).get("trades") or []
    verified = [p for p in (user.get("purchases") or []) if p.get("status") == "verified"]

    if "xp" in t or "earn" in t:
        return (
            f"Fast XP plan (today):\n"
            f"1) Open **Market** (quest)\n"
            f"2) Do **1 practice trade** (quest)\n"
            f"3) Add **1 friend** (quest)\n"
            f"4) Set up your **wallet** (quest)\n"
            f"5) Verify **1 testnet receipt** for the big XP\n\n"
            f"You’re Level **{lvl}**, and need **{xp_to_next - xp_in} XP** to level up."
        )

    if "wallet" in t or "address" in t:
        if wallet:
            return (
                "You’re already connected ✅\n"
                f"Wallet: `{wallet[:6]}…{wallet[-4:]}`\n\n"
                "Next: go to **Shop** → pick a USDC item → generate a payment command → paste the receipt ID."
            )
        return (
            "Wallet setup (1 minute):\n"
            "1) Open **Profile**\n"
            "2) Paste your **public** address (starts with 0x…)\n"
            "3) Save\n\n"
            "Then you can use testnet checkout in Market/Shop."
        )

    if "testnet" in t:
        return (
            "Testnet = practice money, real blockchain.\n"
            "✅ You can send transactions and get receipts.\n"
            "❌ The tokens have no real-world value.\n\n"
            "In Crowdlike we use testnet USDC so you can demo the full checkout + proof flow safely."
        )

    if "buy" in t or "shop" in t:
        return (
            "If you want the clean demo moment: buy a **VIP Drop Ticket (USDC testnet)** in Shop.\n"
            "It shows: checkout command → receipt → verification → item unlocked.\n\n"
            "If you just want fast progress: grab a **Neon Profile Badge** with coins."
        )

    if "stats" in t or "money" in t or "balance" in t:
        return (
            f"Here’s your snapshot:\n"
            f"- Cash (testnet): **${float(user.get('cash_usdc',0.0)):.2f}**\n"
            f"- Coins: **{int(user.get('coins',0))}**\n"
            f"- Gems: **{int(user.get('gems',0))}**\n"
            f"- Friends: **{len(friends)}**\n"
            f"- Trades: **{len(trades)}**\n"
            f"- Verified receipts: **{len(verified)}**\n"
            f"- Streak: **{streak} days**"
        )

    return (
        "Got it. Here are the best next clicks:\n"
        "• **Quests** to earn XP\n"
        "• **Market** to practice buy/sell\n"
        "• **Shop** for drops\n"
        "• **Profile** for wallet + personalization\n\n"
        "Tell me what vibe you want: speedrun XP, premium checkout demo, or social growth?"
    )


# If last message is user, add assistant response
msgs = st.session_state.coach_messages
if msgs and msgs[-1]["role"] == "user":
    ans = _answer(msgs[-1]["content"])
    msgs.append({"role":"assistant","content":ans})
    with st.chat_message("assistant"):
        st.markdown(ans)
    grant_xp(user, 15, "Coach", "Asked for guidance")
    add_notification(user, "Coach gave you a new plan.", "info")
    log_activity(user, "Chatted with Coach", icon="🤖")
    save_current_user()

save_current_user()

# Guided tutorial (spotlight tour)
# --- Guided actions (goal-focused) ---
cols = st.columns(2)
with cols[0]:
    if st.button("Generate a plan", key="coach_plan", use_container_width=True):
        tour_complete_step(2)
        try:
            st.session_state.coach_messages.append({"role":"user","content":"Create a clear plan for investing + workflow automation."})
        except Exception:
            pass
with cols[1]:
    if st.button("Go to Market", key="coach_to_market", use_container_width=True):
        tour_complete_step(3)
        tour_complete_step(3)
        st.switch_page("pages/market.py")
