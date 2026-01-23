from __future__ import annotations

import streamlit as st
from typing import List, Tuple

PAGES: List[Tuple[str, str, str]] = [
    ("home", "Home", "🏠"),
    ("dashboard", "Dashboard", "📊"),
    ("agents", "Agents", "🤖"),
    ("coach", "Coach", "🧠"),
    ("market", "Market", "📈"),
    ("analytics", "Analytics", "📉"),
    ("leaderboards", "Leaderboards", "🏆"),
    ("safety", "Safety", "🛡️"),
    ("profile", "Profile", "👤"),
]

def inject_global_css() -> None:
    st.markdown(
        """
<style>
#MainMenu { visibility: hidden; }
header { visibility: hidden; }
footer { visibility: hidden; }
[data-testid="stToolbar"] { visibility: hidden; height: 0px; }

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');

html, body, [class*="css"]  {
  font-family: 'Inter', system-ui, -apple-system, Segoe UI, Roboto, Helvetica, Arial, sans-serif !important;
}

.stApp {
  background: linear-gradient(135deg, #eff6ff 0%, #ffffff 45%, #f5f3ff 100%);
}

.block-container {
  max-width: 80rem;
  padding-top: 2.25rem;
  padding-bottom: 2.25rem;
  transition: margin-left 250ms ease;
  margin-left: 0.5rem;
}

/* Hover-reveal sidebar */
:root {
  --c-sidebar-width: 18rem;       /* 288px */
  --c-sidebar-edge: 16px;
  --c-sidebar-z: 10010;
}

.c-hoverzone {
  position: fixed;
  left: 0;
  top: 0;
  width: var(--c-sidebar-edge);
  height: 100vh;
  z-index: calc(var(--c-sidebar-z) - 1);
  background: transparent;
}

section[data-testid="stSidebar"] {
  position: fixed !important;
  top: 0;
  left: 0;
  height: 100vh !important;
  width: var(--c-sidebar-width) !important;
  background: rgba(255,255,255,0.95) !important;
  backdrop-filter: blur(10px) !important;
  border-right: 1px solid rgba(0,0,0,0.08) !important;
  box-shadow: 0 10px 30px rgba(0,0,0,0.10) !important;
  z-index: var(--c-sidebar-z) !important;
  transform: translateX(calc(-1 * var(--c-sidebar-width) + var(--c-sidebar-edge)));
  transition: transform 250ms ease;
}

section[data-testid="stSidebar"]:hover {
  transform: translateX(0);
}

/* :has() is supported by modern Chromium, which Streamlit Cloud uses */
body:has(.c-hoverzone:hover) section[data-testid="stSidebar"] {
  transform: translateX(0);
}

body:has(section[data-testid="stSidebar"]:hover) .block-container,
body:has(.c-hoverzone:hover) .block-container {
  margin-left: calc(var(--c-sidebar-width) + 1rem);
}

section[data-testid="stSidebar"] [data-testid="stSidebarNav"] { display: none; }

/* Cards */
.c-card {
  background: #ffffff;
  border-radius: 0.75rem;
  box-shadow: 0 10px 25px rgba(0,0,0,0.08);
  border: 1px solid rgba(0,0,0,0.05);
}
.c-card:hover { box-shadow: 0 14px 30px rgba(0,0,0,0.10); }
.c-card-pad { padding: 1.5rem; }

/* Title gradient */
.c-title-gradient {
  background: linear-gradient(90deg, #2563eb 0%, #7c3aed 50%, #db2777 100%);
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
}

.c-muted { color: #6b7280; }

/* Buttons */
.stButton>button {
  border-radius: 0.75rem;
  padding: 0.6rem 0.9rem;
  font-weight: 700;
  border: 1px solid rgba(0,0,0,0.08);
  background: rgba(255,255,255,0.9);
}
.stButton>button:hover {
  border-color: rgba(37,99,235,0.35);
  box-shadow: 0 10px 18px rgba(37,99,235,0.12);
}

/* Sidebar nav buttons */
.c-nav button {
  width: 100% !important;
  justify-content: flex-start !important;
  gap: 0.6rem !important;
  background: transparent !important;
  border: none !important;
  box-shadow: none !important;
  padding: 0.55rem 0.6rem !important;
  border-radius: 0.75rem !important;
  font-weight: 700 !important;
  color: #111827 !important;
}
.c-nav button:hover {
  background: rgba(243,244,246, 0.9) !important;
}
.c-nav-active button {
  background: rgba(59,130,246,0.10) !important;
  border: 1px solid rgba(59,130,246,0.18) !important;
}

[data-testid="stMetricValue"] { font-weight: 900; }


/* Mobile: no hover, keep sidebar visible */
@media (max-width: 768px) {
  .c-hoverzone { display: none; }
  section[data-testid="stSidebar"] { transform: translateX(0) !important; }
  .block-container { margin-left: 0.5rem !important; }
}

section[data-testid="stSidebar"] > div {
  padding-top: 1.25rem;
}
</style>
<div class="c-hoverzone"></div>
        """,
        unsafe_allow_html=True,
    )

def sidebar_nav(current: str) -> str:
    with st.sidebar:
        st.markdown(
            """
            <div style="padding:0.75rem 1rem 1rem 1rem;">
              <div style="display:flex; align-items:center; justify-content:space-between; gap:0.75rem;">
                <div style="font-size:1.4rem; font-weight:900;" class="c-title-gradient">Crowdlike</div>
              </div>
              <div class="c-muted" style="margin-top:0.25rem; font-size:0.95rem;">
                Personal finance, agentic trading, and crowd feedback.
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        query = st.text_input("Search", value="", placeholder="Search pages...")
        st.markdown('<div class="c-nav">', unsafe_allow_html=True)

        chosen = current
        for page_id, label, emoji in PAGES:
            if query and query.lower() not in label.lower():
                continue

            st.markdown(f'<div class="{ "c-nav-active" if page_id == current else "" }">', unsafe_allow_html=True)
            if st.button(f"{emoji}  {label}", key=f"nav_{page_id}"):
                chosen = page_id
            st.markdown('</div>', unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown(
            """
            <div style="padding: 0.75rem 1rem; border-top: 1px solid rgba(0,0,0,0.06); margin-top: 0.75rem;">
              <div class="c-muted" style="font-size:0.85rem;">
                Tip: hover near the left edge to reveal the sidebar.
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    return chosen

def page_title(title: str, subtitle: str | None = None) -> None:
    st.markdown(
        f"""
        <div style="margin-bottom: 1.25rem;">
          <div style="font-size: 2.25rem; font-weight: 900;">{title}</div>
          {f'<div class="c-muted" style="margin-top:0.25rem; font-size:1.05rem;">{subtitle}</div>' if subtitle else ''}
        </div>
        """,
        unsafe_allow_html=True,
    )

def hero_title(title: str, subtitle: str) -> None:
    st.markdown(
        f"""
        <div style="text-align:center; padding: 3rem 0 1.5rem 0;">
          <div class="c-title-gradient" style="font-size:3.5rem; font-weight: 900; line-height:1.05; margin-bottom: 0.75rem;">
            {title}
          </div>
          <div class="c-muted" style="font-size:1.25rem; margin-bottom: 2rem;">
            {subtitle}
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

def card(html: str) -> None:
    st.markdown(f'<div class="c-card c-card-pad">{html}</div>', unsafe_allow_html=True)
