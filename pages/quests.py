import streamlit as st

from crowdlike.ui import apply_ui, hero, nav, soft_divider
from crowdlike.auth import require_login, save_current_user
from crowdlike.game import (
    ensure_user_schema,
    record_visit,
    today_str,
    grant_xp,
    add_notification,
    log_activity,
)

st.set_page_config(page_title="Quests", page_icon="🎯", layout="wide")
apply_ui()

user = require_login(app_name="Crowdlike")
ensure_user_schema(user)
record_visit(user, "quests")

nav(active="Quests")
hero("🎯 Quests", "Clear missions, earn XP, unlock drops.", badge="Daily")

today = today_str()
claimed = user.setdefault("quests_claimed", {}).setdefault(today, [])

wallet_addr = (user.get("wallet") or {}).get("address", "")
friends = user.get("friends") or []
trades = (user.get("portfolio") or {}).get("trades") or []
purchases = user.get("purchases") or []
verified_purchases = [p for p in purchases if p.get("status") == "verified"]

visits = user.get("visits") or {}

QUESTS = [
    {
        "id": "visit_market",
        "title": "Scout the Market",
        "desc": "Open the Market page once.",
        "xp": 80,
        "done": visits.get("market", 0) >= 1,
        "hint": "Go to Market → come back.",
    },
    {
        "id": "add_friend",
        "title": "Add a Friend",
        "desc": "Add at least 1 friend in Social.",
        "xp": 120,
        "done": len(friends) >= 1,
        "hint": "Social → Add friend.",
    },
    {
        "id": "first_trade",
        "title": "First Trade (Practice)",
        "desc": "Make 1 practice buy/sell.",
        "xp": 140,
        "done": len(trades) >= 1,
        "hint": "Market → Practice buy/sell.",
    },
    {
        "id": "setup_wallet",
        "title": "Wallet Ready",
        "desc": "Add your public wallet address.",
        "xp": 160,
        "done": bool(wallet_addr),
        "hint": "Profile → Wallet.",
    },
    {
        "id": "checkout_proof",
        "title": "Proof of Payment",
        "desc": "Verify 1 testnet receipt.",
        "xp": 220,
        "done": len(verified_purchases) >= 1,
        "hint": "Market or Shop → Testnet checkout.",
    },
]

st.subheader("Daily quests")
st.caption("Claim once per day. New quests refresh daily.")

for q in QUESTS:
    qid = q["id"]
    is_claimed = qid in claimed
    done = bool(q["done"])

    st.markdown(
        f'<div class="card" style="margin-bottom:0.65rem">'
        f'<div style="display:flex;justify-content:space-between;gap:12px;align-items:flex-start">'
        f'<div><div style="font-weight:900;font-size:1.05rem">{q["title"]}</div>'
        f'<div style="color:var(--muted)">{q["desc"]}</div>'
        f'<div style="margin-top:0.35rem" class="chip">⚡ {q["xp"]} XP</div></div>'
        f'<div class="badge"><span class="badge-dot"></span>{"DONE" if done else "IN PROGRESS"}</div>'
        f'</div>'
        f'</div>',
        unsafe_allow_html=True,
    )

    cols = st.columns([1, 1, 1])
    with cols[0]:
        if done and not is_claimed:
            if st.button("Claim", type="primary", key=f"quest_claim_{qid}"):
                claimed.append(qid)
                grant_xp(user, int(q["xp"]), "Quest", q["title"])
                add_notification(user, f"Quest cleared: {q['title']} +{q['xp']} XP", "success")
                log_activity(user, f"Cleared quest: {q['title']}", icon="🎯")
                save_current_user()
                st.rerun()
        elif is_claimed:
            st.success("Claimed ✅")
        else:
            st.info("Not done yet")

    with cols[1]:
        st.caption(f"Hint: {q['hint']}")
    with cols[2]:
        st.write("")

soft_divider()

# ---- Achievements ----
st.subheader("🏅 Achievements")
xp = int(user.get("xp", 0))
ach = [
    {"title":"Rookie", "desc":"Reach 500 XP", "done": xp >= 500},
    {"title":"Operator", "desc":"Reach 2,000 XP", "done": xp >= 2000},
    {"title":"Connector", "desc":"Add 5 friends", "done": len(friends) >= 5},
    {"title":"Trader", "desc":"Complete 10 practice trades", "done": len(trades) >= 10},
    {"title":"Collector", "desc":"Own 5 shop items", "done": len(user.get("inventory") or []) >= 5},
    {"title":"On‑chain Verified", "desc":"Verify 3 receipts", "done": len(verified_purchases) >= 3},
]

cols = st.columns(2)
for i, a in enumerate(ach):
    with cols[i % 2]:
        st.markdown(
            f'<div class="card" style="margin-bottom:0.65rem">'
            f'<div style="display:flex;justify-content:space-between;align-items:center;gap:10px">'
            f'<div><div style="font-weight:900">{a["title"]}</div>'
            f'<div style="color:var(--muted)">{a["desc"]}</div></div>'
            f'<div class="badge"><span class="badge-dot"></span>{"Unlocked" if a["done"] else "Locked"}</div>'
            f'</div></div>',
            unsafe_allow_html=True,
        )

save_current_user()
