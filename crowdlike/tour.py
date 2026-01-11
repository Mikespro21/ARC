from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, Any
import streamlit as st

@dataclass(frozen=True)
class Step:
    n: int
    title: str
    body: str
    page: str
    key: str

TOTAL = 7

# Steps are ONLY about the core goal: use agent -> go market -> execute -> set wallet
STEPS: Dict[int, Step] = {
    1: Step(1, "Welcome", "You’ll use an AI agent to plan a trade, then execute a testnet-safe buy/sell in Market.", "home", "cta_automate"),
    2: Step(2, "Agent", "Tap the highlighted starter to generate your first plan.", "coach", "coach_plan"),
    3: Step(3, "Market", "Go to Market to turn the plan into a buy/sell action.", "coach", "coach_to_market"),
    4: Step(4, "Pick an asset", "Select an asset you want to trade.", "market", "practice_coin"),
    5: Step(5, "Execute", "Execute a demo buy/sell so you understand the flow.", "market", "practice_exec"),
    6: Step(6, "Wallet", "Save your wallet so the app can link you to ArcScan proof.", "profile", "pf_save"),
    7: Step(7, "Done", "You’re ready: Agent → Market → Execute → Track.", "home", "nav_home"),
}

def _set_step(n: int) -> None:
    st.session_state["tour_step"] = max(1, min(TOTAL, int(n)))

def tour_complete_step(n: int) -> None:
    cur = int(st.session_state.get("tour_step", 1))
    if n == cur:
        if cur >= TOTAL:
            st.session_state["tour_done"] = True
        else:
            _set_step(cur + 1)
        st.rerun()

def _end(user: Dict[str, Any]) -> None:
    user["tutorial_done"] = True
    st.session_state["tour_done"] = True
    try:
        from crowdlike.auth import save_current_user
        save_current_user()
    except Exception:
        pass

def _css(target_key: str) -> None:
    st.markdown(
        f"""
        <style>
        .tour-scrim {{
            position: fixed; inset: 0;
            background: rgba(2,6,23,0.52);
            z-index: 10000;
        }}
        .tour-box {{
            position: fixed;
            left: 50%; top: 72px;
            transform: translateX(-50%);
            width: min(680px, calc(100vw - 28px));
            z-index: 10002;
            border-radius: 14px;
            border: 1px solid rgba(167,139,250,0.22);
            background: rgba(255,255,255,0.94);
            box-shadow: 0 24px 80px rgba(2,6,23,0.18);
            backdrop-filter: blur(12px);
            padding: 14px 14px 12px 14px;
        }}
        .tour-topline {{
            height: 3px;
            border-radius: 999px;
            background: linear-gradient(90deg, rgba(14,165,233,0.55), rgba(167,139,250,0.70));
            margin-bottom: 10px;
        }}
        .tour-kicker {{
            font-size: 0.78rem;
            letter-spacing: 0.08em;
            text-transform: uppercase;
            color: rgba(71,85,105,0.92);
            margin-bottom: 4px;
        }}
        .tour-title {{
            font-weight: 820;
            font-size: 1.05rem;
            margin-bottom: 6px;
            color: rgba(15,23,42,0.95);
        }}
        .tour-body {{
            color: rgba(51,65,85,0.95);
            line-height: 1.45;
            font-size: 0.96rem;
            margin-bottom: 10px;
        }}

        /* spotlight */
        #st-key-{target_key} {{
            position: relative !important;
            z-index: 10003 !important;
        }}
        #st-key-{target_key} button,
        #st-key-{target_key} input,
        #st-key-{target_key} textarea,
        #st-key-{target_key} a {{
            box-shadow: 0 0 0 3px rgba(167,139,250,0.22), 0 18px 50px rgba(2,6,23,0.22) !important;
        }}

        /* controls fixed */
        #st-key-tour_back, #st-key-tour_next, #st-key-tour_skip, #st-key-tour_finish {{
            position: fixed !important;
            z-index: 10004 !important;
            bottom: 22px;
        }}
        #st-key-tour_skip {{ left: 22px; }}
        #st-key-tour_back {{ right: 212px; }}
        #st-key-tour_next, #st-key-tour_finish {{ right: 22px; }}

        #st-key-tour_next button, #st-key-tour_finish button {{
            border: 1px solid rgba(167,139,250,0.28) !important;
            background: linear-gradient(135deg, rgba(167,139,250,0.14), rgba(255,255,255,0.86)) !important;
        }}
        </style>
        <div class="tour-scrim"></div>
        """,
        unsafe_allow_html=True
    )

def maybe_run_tour(user: Dict[str, Any], current_page: str) -> None:
    """7-step guided tour.

    Design goals:
    - Never crash the app (unique keys per-page).
    - Works across Streamlit multipage.
    - Can be advanced manually (Next) OR automatically when a page completes a step
      via `tour_complete_step(step_number)`.
    """
    if not user or user.get("tutorial_done") or st.session_state.get("tour_done"):
        return

    step = int(st.session_state.get("tour_step", 1))
    step = max(1, min(TOTAL, step))
    _set_step(step)

    s = STEPS[step]

    # If the user is on a different page than the step expects, show a simple "Go" helper.
    page_paths = {
        "home": "app.py",
        "coach": "pages/coach.py",
        "market": "pages/market.py",
        "profile": "pages/profile.py",
    }
    if current_page != s.page:
        _css("nav_home")  # keep nav visible, but don't attempt to spotlight a missing key
        st.markdown(
            f"""<div class="tour-box">
                <div class="tour-topline"></div>
                <div class="tour-kicker">Step {step} of {TOTAL}</div>
                <div class="tour-title">{s.title}</div>
                <div class="tour-body">Go to <b>{s.page.title()}</b> to continue the tutorial.</div>
            </div>""",
            unsafe_allow_html=True,
        )
        colA, colB, colC = st.columns([1,1,1])
        with colA:
            if st.button("Skip", key=f"tour_skip_{current_page}_{step}", use_container_width=True):
                _end(user); st.rerun()
        with colB:
            if st.button("Back", key=f"tour_back_{current_page}_{step}", use_container_width=True, disabled=(step==1)):
                _set_step(step - 1); st.rerun()
        with colC:
            if st.button(f"Go to {s.page.title()}", key=f"tour_goto_{current_page}_{step}", use_container_width=True):
                st.switch_page(page_paths.get(s.page, "app.py"))
        return

    # Normal render on the correct page: spotlight the correct target key.
    target = s.key
    _css(target)

    st.markdown(
        f"""<div class="tour-box">
            <div class="tour-topline"></div>
            <div class="tour-kicker">Step {step} of {TOTAL}</div>
            <div class="tour-title">{s.title}</div>
            <div class="tour-body">{s.body}</div>
        </div>""",
        unsafe_allow_html=True,
    )

    col1, col2, col3, col4 = st.columns([1,1,1,1])
    with col1:
        skip = st.button("Skip", key=f"tour_skip_{current_page}_{step}", use_container_width=True)
    with col2:
        back = st.button("Back", key=f"tour_back_{current_page}_{step}", use_container_width=True, disabled=(step==1))
    with col3:
        if step < TOTAL:
            nxt = st.button("Next", key=f"tour_next_{current_page}_{step}", use_container_width=True)
            fin = False
        else:
            nxt = False
            fin = st.button("Finish", key=f"tour_finish_{current_page}_{step}", use_container_width=True)
    with col4:
        # subtle indicator slot
        st.caption("")

    if skip:
        _end(user); st.rerun()
    if back:
        _set_step(step - 1); st.rerun()
    if nxt:
        _set_step(step + 1); st.rerun()
    if fin:
        _end(user); st.rerun()