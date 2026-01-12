import streamlit as st

from crowdlike.ui import apply_ui, hero, nav, soft_divider, status_bar, callout, metric_card
from crowdlike.settings import bool_setting
from crowdlike.auth import require_login, save_current_user
from crowdlike.game import ensure_user_schema, record_visit
from crowdlike.agents import get_agents
from crowdlike.pricing import quote_daily
from crowdlike.layout import render_sidebar


st.set_page_config(page_title="Pricing", page_icon="💳", layout="wide")
apply_ui()

user = require_login(app_name="Crowdlike")
ensure_user_schema(user)
record_visit(user, "pricing")

render_sidebar(user, active_page="pricing")

_demo = bool_setting("DEMO_MODE", True)
wallet = (user.get("wallet") or {}) if isinstance(user.get("wallet"), dict) else {}
_wallet_set = bool((wallet.get("address") or "").strip())
crowd = user.get("crowd") if isinstance(user.get("crowd"), dict) else {}
status_bar(wallet_set=_wallet_set, demo_mode=_demo, crowd_score=float(crowd.get("score", 50.0) or 50.0))

nav(active="Pricing")
hero("💳 Pricing", "Per-day billing that scales with agent count and risk (per Master Context).", badge="Pay-per-day")

callout(
    "info",
    "Pricing model (spec)",
    "Final formula: price = (agentCount^2) * (risk / 100), where risk is a 0–100 value.",
)

agents = get_agents(user)
c1, c2 = st.columns([1.0, 1.2])
with c1:
    n = st.number_input("Number of agents", min_value=1, max_value=200, value=max(1, len(agents)), step=1)
with c2:
    # Use user policy risk as default if present
    base_policy = user.get("policy") if isinstance(user.get("policy"), dict) else {}
    default_r = int(float(base_policy.get("risk", 25) or 25))
    risk = st.slider("Riskness (0–100)", min_value=0, max_value=100, value=max(0, min(100, default_r)))

q = quote_daily(int(n), float(risk))

soft_divider()

m1, m2, m3 = st.columns(3)
with m1:
    metric_card("Total per day", f"${q.total_per_day:,.2f}", "Daily total across all agents")
with m2:
    metric_card("Per agent per day", f"${q.per_agent_per_day:,.2f}", "Average per-agent daily cost")
with m3:
    metric_card("Risk", f"{q.risk:.0f}/100", "Risk influences constraints + price")

st.markdown("### Notes")
st.markdown(
    """- This is a transparent estimator for the demo (not an actual billing integration).
- Riskness also influences *crowd deviation constraints* (see Profile/Coach).
- As agentCount grows, price increases quadratically by design in the spec."""
)

save_current_user()
