from __future__ import annotations
import streamlit as st

CSS = """
<style>
/* Background */
.stApp {
  background: linear-gradient(135deg, #eff6ff 0%, #ffffff 42%, #f5f3ff 100%);
}

/* Reduce top padding a touch */
.block-container { padding-top: 2.2rem; }

/* Glass cards */
.cl-card {
  background: rgba(255,255,255,0.72);
  border: 1px solid rgba(255,255,255,0.55);
  border-radius: 18px;
  padding: 18px 18px;
  box-shadow: 0 12px 30px rgba(17,24,39,0.08);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  margin-bottom: 14px;
}

/* Small helper text */
.cl-muted { color: rgba(17,24,39,0.60); }

/* Pills */
.cl-pill {
  display: inline-block;
  padding: 4px 10px;
  border-radius: 999px;
  font-size: 12px;
  font-weight: 600;
  border: 1px solid rgba(124,58,237,0.20);
  background: rgba(124,58,237,0.08);
  color: rgba(88,28,135,0.95);
  margin-right: 6px;
  margin-top: 6px;
}

/* Status chips */
.cl-chip {
  display: inline-block;
  padding: 4px 10px;
  border-radius: 999px;
  font-size: 12px;
  font-weight: 700;
}
.cl-chip-active { background: rgba(34,197,94,0.12); color: rgba(22,101,52,1); border: 1px solid rgba(34,197,94,0.20); }
.cl-chip-paused { background: rgba(245,158,11,0.12); color: rgba(120,53,15,1); border: 1px solid rgba(245,158,11,0.20); }
.cl-chip-exited { background: rgba(239,68,68,0.10); color: rgba(127,29,29,1); border: 1px solid rgba(239,68,68,0.20); }

/* Buttons: keep Streamlit look but slightly rounder */
.stButton > button {
  border-radius: 14px !important;
  padding: 0.6rem 1rem !important;
}

/* Sidebar spacing */
section[data-testid="stSidebar"] .block-container { padding-top: 1.2rem; }

/* Tables */
[data-testid="stDataFrame"] {
  border-radius: 14px;
  overflow: hidden;
  border: 1px solid rgba(17,24,39,0.08);
}
</style>
"""


def apply() -> None:
    """Apply global CSS styling."""
    st.markdown(CSS, unsafe_allow_html=True)


def card_start(title: str | None = None, subtitle: str | None = None) -> None:
    st.markdown('<div class="cl-card">', unsafe_allow_html=True)
    if title:
        st.markdown(f"### {title}")
    if subtitle:
        st.markdown(f"<div class='cl-muted'>{subtitle}</div>", unsafe_allow_html=True)


def card_end() -> None:
    st.markdown('</div>', unsafe_allow_html=True)


def pill(text: str) -> str:
    return f"<span class='cl-pill'>{text}</span>"
