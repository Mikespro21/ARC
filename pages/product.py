import streamlit as st
from crowdlike.ui import apply_ui, soft_divider, callout
from crowdlike.site import site_footer, site_header, site_hero, site_section
from crowdlike.version import VERSION

st.set_page_config(page_title="Crowdlike — Product", page_icon="✨", layout="wide")
apply_ui()

site_header(active="Product")


site_hero(kicker=f"Crowdlike v{VERSION}", title="Product", subtitle="A production-feel demo for agentic payments guided by crowd likability—designed for clarity, safety, and judged UX.")

soft_divider()

c1, c2 = st.columns([1.2, 1.0], gap="large")
with c1:
    callout(
        "Core loop",
        "Create agents → set autonomy and limits → run cycles → approve or auto-execute within guardrails → review analytics.",
        tone="muted",
    )
    site_section(icon="🧭", title="Guided onboarding", body="A Journey wizard keeps users from getting lost and reduces judge friction.", full_width=True)
with c2:
    site_section(icon="🔒", title="Trust signals", body="Verified receipts, stable deviation, and safe drawdown build confidence to unlock autonomy.", full_width=True)

soft_divider()

g1, g2, g3 = st.columns(3, gap="large")
with g1:
    site_section(icon="📈", title="Markets + checkout", body="Practice trades plus a testnet checkout flow for believable commerce demos.")
with g2:
    site_section(icon="🤖", title="Coach mission control", body="Run reports, approvals, and clear 'why' explanations for every proposal.")
with g3:
    site_section(icon="📊", title="Analytics", body="Portfolio metrics, drawdown, streak scoring, and timeline-driven auditing.")

site_footer()
