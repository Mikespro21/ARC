import time
import uuid
import streamlit as st

from crowdlike.ui import apply_ui, hero, nav, soft_divider
from crowdlike.tour import maybe_run_tour
from crowdlike.auth import require_login, save_current_user
from crowdlike.game import ensure_user_schema, record_visit, add_notification, log_activity

st.set_page_config(page_title="Social", page_icon="🫶", layout="wide")
apply_ui()

user = require_login(app_name="Crowdlike")
maybe_run_tour(user, current_page="social")
ensure_user_schema(user)
record_visit(user, "social")
save_current_user()

nav(active="Home")
hero("🫶 Social", "Crowd Score is the feedback engine — it nudges what your agent is allowed to do.", badge="Social")

crowd = user.setdefault("crowd", {"score": 50.0, "likes_received": 0, "likes_given": 0})
feed = user.setdefault("social_feed", [])

# Seed a few demo posts once
if not feed:
    feed.extend([
        {"id": "p1", "author": "Arc Builder", "text": "Tip: Start with low limits, then raise after your first verified receipt.", "likes": 3},
        {"id": "p2", "author": "Crowdlike", "text": "Crowd Score gently boosts your payment limits (±20%).", "likes": 5},
        {"id": "p3", "author": "Demo User", "text": "I verified my first checkout — smooth!", "likes": 2},
    ])
    save_current_user()

c1, c2, c3 = st.columns(3)
with c1:
    st.markdown(f'<div class="card"><div style="font-weight:800">Crowd Score</div><div style="font-size:2rem;font-weight:900;margin-top:0.25rem">{float(crowd.get("score",50.0)):.0f}</div></div>', unsafe_allow_html=True)
with c2:
    st.markdown(f'<div class="card"><div style="font-weight:800">Likes given</div><div style="font-size:2rem;font-weight:900;margin-top:0.25rem">{int(crowd.get("likes_given",0) or 0)}</div></div>', unsafe_allow_html=True)
with c3:
    st.markdown(f'<div class="card"><div style="font-weight:800">Likes received</div><div style="font-size:2rem;font-weight:900;margin-top:0.25rem">{int(crowd.get("likes_received",0) or 0)}</div></div>', unsafe_allow_html=True)

soft_divider()

st.subheader("Post an update")
with st.form("post_form", clear_on_submit=True):
    txt = st.text_area("What are you building?", placeholder="e.g., I just verified a checkout and raised my daily cap to $0.50", height=90)
    submitted = st.form_submit_button("Post")
    if submitted:
        msg = (txt or "").strip()
        if not msg:
            st.warning("Write something first.")
        else:
            feed.insert(0, {
                "id": str(uuid.uuid4()),
                "author": user.get("username","Member"),
                "text": msg[:280],
                "likes": 0,
            })
            log_activity(user, "Posted an update", icon="🫶")
            save_current_user()
            st.success("Posted.")

soft_divider()
st.subheader("Feed")

# Local-only likes (single-user demo)
for p in feed[:25]:
    cols = st.columns([6, 1])
    with cols[0]:
        st.markdown(
            '<div class="card">'
            f'<div style="font-weight:820">{p.get("author","")}</div>'
            f'<div style="color:var(--muted);margin-top:4px">{p.get("text","")}</div>'
            f'<div style="margin-top:0.6rem;color:var(--muted)">Likes: <b>{int(p.get("likes",0) or 0)}</b></div>'
            '</div>',
            unsafe_allow_html=True,
        )
    with cols[1]:
        if st.button("Like", key=f"like_{p.get('id')}"):
            p["likes"] = int(p.get("likes", 0) or 0) + 1
            crowd["likes_given"] = int(crowd.get("likes_given", 0) or 0) + 1

            # Gentle score gain from “participation”
            crowd["score"] = float(crowd.get("score", 50.0) or 50.0) + 0.3

            add_notification(user, "Liked", f"You liked {p.get('author','a post')}.")
            save_current_user()
            st.rerun()

soft_divider()
st.subheader("How Social affects autonomy")
st.markdown(
    '<div class="card card-strong">'
    '<div style="font-weight:760">Crowd Score → payment limits</div>'
    '<div style="color:var(--muted);margin-top:4px">'
    'Your Crowd Score gently boosts your payment limits by up to ±20%. '
    'It’s not “free money” — it only nudges within your safety rails. '
    'The goal is to make agentic payments feel earned and controllable.'
    '</div>'
    '</div>',
    unsafe_allow_html=True,
)
