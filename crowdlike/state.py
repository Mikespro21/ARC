from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List

import streamlit as st

from .mock import (
    generate_mock_user,
    generate_mock_agents,
    calculate_crowd_metrics,
    generate_leaderboard,
)

STATE_VERSION = "optionA_v1"


def ensure_state() -> None:
    """Initialize Streamlit session state with demo data."""
    if st.session_state.get("_cl_state_version") != STATE_VERSION:
        st.session_state.clear()
        st.session_state["_cl_state_version"] = STATE_VERSION

    if "user" not in st.session_state:
        st.session_state["user"] = generate_mock_user()

    if "agents" not in st.session_state:
        st.session_state["agents"] = generate_mock_agents(4, user_id=st.session_state["user"]["id"])

    # crowd baseline (separate pool)
    if "crowd_agents" not in st.session_state:
        st.session_state["crowd_agents"] = generate_mock_agents(96, user_id="crowd")

    recompute_metrics()


def recompute_metrics() -> None:
    agents: List[Dict[str, Any]] = st.session_state.get("agents", [])
    crowd_agents: List[Dict[str, Any]] = st.session_state.get("crowd_agents", [])
    all_agents = list(agents) + list(crowd_agents)

    st.session_state["crowdMetrics"] = calculate_crowd_metrics(all_agents)
    st.session_state["leaderboards"] = {
        "daily": generate_leaderboard(all_agents, "daily"),
        "weekly": generate_leaderboard(all_agents, "weekly"),
        "monthly": generate_leaderboard(all_agents, "monthly"),
        "yearly": generate_leaderboard(all_agents, "yearly"),
    }
