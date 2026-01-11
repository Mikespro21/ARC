import streamlit as st

from crowdlike.ui import apply_ui, hero, nav, soft_divider
from crowdlike.tour import maybe_run_tour, tour_complete_step
from crowdlike.auth import require_login, save_current_user
from crowdlike.game import ensure_user_schema, record_visit, grant_xp, add_notification, log_activity, compute_streak, xp_progress

st.set_page_config(page_title="Coach", page_icon="🤖", layout="wide")
apply_ui()

user = require_login(app_name="Crowdlike")

maybe_run_tour(user, current_page="coach")
ensure_user_schema(user)
record_visit(user, "coach")

nav(active="Coach")
hero("🤖 Coach", "Your friendly concierge for quests, market moves, and next steps.", badge="AI Demo")

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
