import time
import streamlit as st

from crowdlike.ui import apply_ui, hero, nav, soft_divider
from crowdlike.tour import maybe_run_tour
from crowdlike.auth import require_login, save_current_user
from crowdlike.game import ensure_user_schema, record_visit, grant_xp, add_notification, log_activity

st.set_page_config(page_title="Quests", page_icon="🧭", layout="wide")
apply_ui()

user = require_login(app_name="Crowdlike")
maybe_run_tour(user, current_page="quests")
ensure_user_schema(user)
record_visit(user, "quests")
save_current_user()

nav(active="Home")
hero("🧭 Quests", "Quick tasks that boost your Crowd Score and unlock more autonomy safely.", badge="Quests")

today = time.strftime("%Y-%m-%d")
claimed = user.setdefault("quests_claimed", {}).setdefault(today, [])

quests = [
    {"id": "q_wallet", "title": "Set your wallet address", "desc": "Add your wallet address in Profile.", "xp": 20, "coins": 50},
    {"id": "q_limits", "title": "Set safety limits", "desc": "Pick a risk level and limits in Profile → Autonomy & Limits.", "xp": 20, "coins": 50},
    {"id": "q_market", "title": "Run a practice trade", "desc": "Use Practice buy/sell to place a trade.", "xp": 15, "coins": 30},
    {"id": "q_social", "title": "Give 3 likes", "desc": "Like 3 posts in Social.", "xp": 15, "coins": 30},
    {"id": "q_receipt", "title": "Verify a receipt", "desc": "Complete a testnet checkout and verify the tx hash.", "xp": 35, "coins": 70},
]

# Auto-check completion hints (best-effort)
wallet_ok = bool((user.get("wallet") or {}).get("address"))
limits_ok = isinstance(user.get("policy"), dict)
has_trade = bool((user.get("portfolio") or {}).get("trades"))
likes_given = int((user.get("crowd") or {}).get("likes_given", 0) or 0)
has_verified = any((p or {}).get("status") == "verified" for p in (user.get("purchases") or []))

completion = {
    "q_wallet": wallet_ok,
    "q_limits": limits_ok,
    "q_market": has_trade,
    "q_social": likes_given >= 3,
    "q_receipt": has_verified,
}

st.subheader("Today’s quests")
for q in quests:
    done = completion.get(q["id"], False)
    already = q["id"] in claimed
    cols = st.columns([3, 1])
    with cols[0]:
        st.markdown(
            '<div class="card">'
            f'<div style="font-weight:820">{q["title"]} {"✅" if already else ""}</div>'
            f'<div style="color:var(--muted);margin-top:4px">{q["desc"]}</div>'
            f'<div style="margin-top:0.6rem;font-weight:800">Reward: +{q["xp"]} XP · +{q["coins"]} coins</div>'
            '</div>',
            unsafe_allow_html=True,
        )
        if done and not already:
            st.caption("Looks completed — you can claim.")
        elif not done and not already:
            st.caption("Not completed yet.")
    with cols[1]:
        if already:
            st.button("Claimed", key=f"claimed_{q['id']}", disabled=True, use_container_width=True)
        else:
            can_claim = bool(done)
            if st.button("Claim", key=f"claim_{q['id']}", disabled=not can_claim, use_container_width=True, type="primary" if can_claim else "secondary"):
                claimed.append(q["id"])
                user["coins"] = int(user.get("coins", 0) or 0) + int(q["coins"])
                grant_xp(user, int(q["xp"]), "Quest", q["title"])
                # Small crowd score bump for completing quests
                crowd = user.setdefault("crowd", {"score": 50.0, "likes_received": 0, "likes_given": 0})
                crowd["score"] = float(crowd.get("score", 50.0)) + 1.5
                add_notification(user, "Quest complete", q["title"])
                log_activity(user, f"Completed quest: {q['title']}", icon="🧭")
                save_current_user()
                st.rerun()

soft_divider()
st.subheader("Why quests matter")
st.markdown(
    '<div class="card card-strong">'
    '<div style="font-weight:760">Crowd Score → autonomy</div>'
    '<div style="color:var(--muted);margin-top:4px">'
    'In Crowdlike 0.2, your Crowd Score gently boosts your payment limits (±20%). '
    'You still stay inside your safety rails, but “more trusted” behavior earns smoother flows.'
    '</div>'
    '</div>',
    unsafe_allow_html=True,
)
