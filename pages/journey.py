import streamlit as st

from crowdlike.auth import require_login, save_current_user
from crowdlike.game import ensure_user_schema, record_visit
from crowdlike.layout import render_sidebar
from crowdlike.ui import apply_ui, hero, nav, soft_divider, callout, button_style
from crowdlike.flow import FLOW_STEPS, progress, next_step
from crowdlike.agents import get_agents, create_agent, get_active_agent, agent_label
from crowdlike.version import VERSION


st.set_page_config(page_title="Journey • Crowdlike", page_icon="🧭", layout="wide")
apply_ui()

user = require_login(app_name="Crowdlike")
ensure_user_schema(user)
record_visit(user, "journey")
save_current_user()

render_sidebar(user, active_page="journey")
nav(active="Journey")

hero("🧭 Journey", f"Your guided setup path · Crowdlike v{VERSION}", badge="Product flow wizard")

done, total, rows = progress(user)
ns = next_step(user)

st.markdown(
    '<div class="card card-strong">'
    f'<div style="font-weight:860; font-size:1.05rem">Setup progress</div>'
    f'<div style="color:var(--muted); margin-top:4px">{done}/{total} complete · finish this once, then live in Coach + Analytics.</div>'
    '</div>',
    unsafe_allow_html=True,
)

soft_divider()

# If user has no agents, offer an instant seed
agents = get_agents(user)
if not agents:
    callout("You have no agents yet. Create a starter agent to begin.", tone="warning")
    button_style("create_starter", "purple")
    if st.button("Create starter agent", key="create_starter"):
        create_agent(user, "Starter", "🤖")
        save_current_user()
        st.rerun()

active_agent = get_active_agent(user)
st.markdown(f"**Active agent:** {agent_label(active_agent) if active_agent else 'None'}")

soft_divider()

for step, ok in rows:
    with st.expander(f"{'✅' if ok else '⬜'} {step.label}", expanded=not ok):
        st.write(step.desc)
        st.caption(f"Destination: `{step.page}`")
        button_style(f"go_{step.id}", "purple" if not ok else "ghost")
        if st.button(("Go" if not ok else "Review") + f" → {step.label}", key=f"go_{step.id}", use_container_width=True):
            st.switch_page(step.page)

soft_divider()

if ns:
    callout(f"**Next recommended:** {ns.label}\n\n{ns.desc}", tone="muted")
    button_style("continue", "purple")
    if st.button(f"Continue → {ns.label}", key="continue", use_container_width=True):
        st.switch_page(ns.page)
else:
    callout("Setup complete. Your core loop now is: run cycles → approve → review analytics → iterate.", tone="success")
