import streamlit as st
import pandas as pd

from crowdlike.ui import apply_ui, hero, nav, soft_divider
from crowdlike.auth import require_login, save_current_user
from crowdlike.game import record_visit, ensure_user_schema, grant_xp, add_notification, log_activity

st.set_page_config(page_title="Social", page_icon="👥", layout="wide")
apply_ui()

user = require_login(app_name="Crowdlike")
ensure_user_schema(user)
record_visit(user, "social")

nav(active="Social")
hero("👥 Social", "Friends, leaderboards, and community energy.", badge="Community")

friends = user.setdefault("friends", [])

c1, c2 = st.columns([1.2, 0.8])

with c1:
    st.markdown('<div class="card card-strong"><h3>🤝 Friends</h3><div style="color:var(--muted)">Add friends by username (local demo).</div></div>', unsafe_allow_html=True)
    st.write("")
    new_friend = st.text_input("Add friend", placeholder="e.g. vector01234", key="soc_add_friend")
    cols = st.columns([1, 1, 1])
    with cols[0]:
        if st.button("Add", type="primary", key="soc_add_btn"):
            f = (new_friend or "").strip()
            if not f:
                st.warning("Type a username first.")
            elif f.lower() == (user.get("username","").lower()):
                st.warning("That’s you 😄")
            elif f in friends:
                st.info("Already added.")
            else:
                friends.append(f)
                grant_xp(user, 80, "Social", "Added a friend")
                add_notification(user, f"Friend added: {f}", "success")
                log_activity(user, f"Added friend {f}", icon="🤝")
                save_current_user()
                st.rerun()

    with cols[1]:
        if st.button("Clear friends", key="soc_clear_btn"):
            friends.clear()
            add_notification(user, "Friends cleared (demo).", "warning")
            save_current_user()
            st.rerun()

    with cols[2]:
        st.write("")

    st.write("")
    if not friends:
        st.caption("No friends yet. Add one to unlock the leaderboard ✨")
    else:
        for f in friends[:20]:
            st.markdown(f'<div class="chip">👤 {f} <span style="opacity:0.6">• friend</span></div>', unsafe_allow_html=True)

with c2:
    st.markdown('<div class="card card-strong"><h3>🏆 Leaderboard</h3><div style="color:var(--muted)">This is a demo leaderboard using your stats.</div></div>', unsafe_allow_html=True)
    st.write("")
    # Demo leaderboard: you + friends with fake stats derived from name length (just for visuals)
    rows = []
    me_xp = int(user.get("xp", 0))
    me_coins = int(user.get("coins", 0))
    rows.append({"Player": f"{user.get('avatar','🧊')} {user.get('username','Me')}", "XP": me_xp, "Coins": me_coins})

    for f in friends[:8]:
        seed = sum(ord(c) for c in f) % 1000
        rows.append({"Player": f"👤 {f}", "XP": int(200 + seed), "Coins": int(100 + seed // 2)})

    df = pd.DataFrame(rows).sort_values("XP", ascending=False)
    st.dataframe(df, use_container_width=True, hide_index=True)

    # Colorful chart (Streamlit default palette)
    st.caption("XP (higher is better)")
    st.bar_chart(df.set_index("Player")["XP"])

soft_divider()

st.subheader("💬 Community feed (demo)")
st.markdown(
    '<div class="card">'
    '<b>What’s happening:</b> new drops, new teams, new wins.<br/>'
    '<span style="color:var(--muted)">For the hackathon demo, this is a local feed. Later we can connect it to a real backend.</span>'
    '</div>',
    unsafe_allow_html=True,
)

save_current_user()
