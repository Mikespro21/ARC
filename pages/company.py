import streamlit as st
from crowdlike.ui import apply_ui, nav, soft_divider
from crowdlike.site import site_header, site_footer, site_section

st.set_page_config(page_title="Crowdlike — Company", page_icon="🏢", layout="wide")
apply_ui()

site_header(active="Company")
nav(active="Company")

st.markdown("## Company")
st.write("Crowdlike is a demo product concept focused on safe agentic commerce experiences.")

soft_divider()

site_section(icon="🎯", title="Mission", body="Make agent autonomy feel safe, legible, and user-controlled—without losing speed or fun.", full_width=True)
site_section(icon="🧩", title="Design principles", body="Clear next steps, guardrails first, explanations always, minimal clutter.", full_width=True)

site_footer()
