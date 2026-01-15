import streamlit as st

from crowdlike.ui import apply_ui, soft_divider, callout
from crowdlike.site import site_hero, site_section, site_footer, site_header
from crowdlike.version import VERSION


st.set_page_config(page_title="Crowdlike", page_icon="🫧", layout="wide")
apply_ui()

# Website Home (no login required)
site_header(active="home")

site_hero(
    kicker=f"Crowdlike v{VERSION}",
    title="Agentic commerce that stays inside the crowd.",
    subtitle=(
        "Crowdlike helps multiple AI agents transact safely on-chain with user-set risk, limits, "
        "and an explicit crowd-deviation constraint—so autonomy feels powerful without feeling reckless."
    ),
)

soft_divider()

c1, c2, c3 = st.columns(3, gap="large")
with c1:
    site_section(
        icon="🧠",
        title="Many agents, separate portfolios",
        body="Run multiple specialized agents in parallel. Each agent has its own portfolio, activity, and run reports.",
    )
with c2:
    site_section(
        icon="🛡️",
        title="Safety and deviation guardrails",
        body="Max deviation, max daily loss, drawdown exits, and approvals make the autonomy ladder predictable and controllable.",
    )
with c3:
    site_section(
        icon="🏁",
        title="Leaderboards with streak scoring",
        body="Track daily/weekly/monthly/yearly performance with a simple score that rewards profit and consistency.",
    )

soft_divider()

left, right = st.columns([1.2, 1.0], gap="large")
with left:
    callout(
        "How it works",
        "**Launch the app**, create agents, set a wallet and limits, then run cycles from Coach. "
        "Crowdlike produces run reports and analytics, while enforcing your safety and crowd-deviation constraints.",
        tone="muted",
    )
with right:
    st.markdown("### Start here")
    st.write("If you're demoing or evaluating, the fastest path is the guided Journey.")
    # No navigation buttons: use page links and the left nav rail.
    st.page_link("pages/dashboard.py", label="🚀 Dashboard", use_container_width=True)
    st.page_link("pages/journey.py", label="🧭 Guided Journey", use_container_width=True)
    st.page_link("pages/docs.py", label="📚 Docs", use_container_width=True)

soft_divider()

site_section(
    icon="✨",
    title="Built for competition demos",
    body=(
        "A crisp user flow, clear risk controls, and a mission-control Coach page "
        "let judges understand the product in minutes."
    ),
    full_width=True,
)

site_footer()
