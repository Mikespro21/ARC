from __future__ import annotations

import streamlit as st

from crowdlike.state import ensure_state
from crowdlike.style import apply, card_start, card_end
from crowdlike.ui import df_from_leaderboard

st.set_page_config(page_title="Leaderboards • Crowdlike", page_icon="🏆", layout="wide")
apply()
ensure_state()

st.markdown("# Leaderboards")
st.caption("Compare agent performance across timeframes. (Demo: scores derived from profit and streaks.)")

tabs = st.tabs(["Daily","Weekly","Monthly","Yearly"])
lb = st.session_state["leaderboards"]

for tab, key in zip(tabs, ["daily","weekly","monthly","yearly"]):
    with tab:
        card_start(f"{key.capitalize()} Leaderboard")
        df = df_from_leaderboard(lb[key])
        st.dataframe(df, use_container_width=True, hide_index=True)
        card_end()
