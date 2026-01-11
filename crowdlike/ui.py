from __future__ import annotations
import streamlit as st

# Enforced by background gradient stops:
# Blue = 0-30% (30)
# White = 30-90% (60)
# Purple = 90-100% (10)
_BG_RATIO = {"blue": 30, "white": 60, "purple": 10}

def apply_ui() -> None:
    css = r"""
    <style>
    :root{
        --white: #FFFFFF;
        --blue: #0EA5E9;
        --blue-soft: rgba(14,165,233,0.10);
        --purple: #A78BFA;
        --purple-soft: rgba(167,139,250,0.10);

        --text: #0F172A;
        --muted: #64748B;

        --r-card: 10px;
        --r-hero: 12px;
        --r-btn: 14px;

        --border: rgba(148,163,184,0.16);
        --shadow: 0 14px 34px rgba(15, 23, 42, 0.10);
    }

    @keyframes fadeUp {
      from { opacity: 0; transform: translateY(6px); }
      to   { opacity: 1; transform: translateY(0); }
    }
    @media (prefers-reduced-motion: reduce){
      *{ animation: none !important; transition: none !important; }
    }

    
    /* Mostly-white background with soft blue + minimal purple */
    .stApp{
        background:
          radial-gradient(900px 360px at 16% 6%, rgba(14,165,233,0.10) 0%, rgba(14,165,233,0.00) 62%),
          radial-gradient(780px 320px at 86% 10%, rgba(167,139,250,0.06) 0%, rgba(167,139,250,0.00) 60%),
          linear-gradient(135deg,
            rgba(255,255,255,0.995) 0%,
            rgba(255,255,255,0.995) 58%,
            rgba(14,165,233,0.04) 100%
          );
        color: var(--text);
        font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    }

    header[data-testid="stHeader"]{ background: transparent; }
    footer{ visibility:hidden; }

    .main .block-container{
        padding-top: 0.85rem;
        padding-bottom: 2.4rem;
        max-width: 1080px;
    }

    section[data-testid="stSidebar"]{
        background: rgba(255,255,255,0.92);
        border-right: 1px solid rgba(148,163,184,0.14);
    }

    .hero{
        border-radius: var(--r-hero);
        padding: 1.0rem 1.1rem;
        border: 1px solid rgba(14,165,233,0.18);
        background: rgba(255,255,255,0.90);
        box-shadow: var(--shadow);
        backdrop-filter: blur(14px);
        margin-bottom: 0.8rem;
        animation: fadeUp 220ms ease both;
    }
    .hero-title{ font-size: 1.42rem; font-weight: 780; letter-spacing: -0.02em; margin: 0; }
    .hero-subtitle{ margin-top: 0.20rem; font-size: 0.96rem; color: var(--muted); }

    .card{
        border-radius: var(--r-card);
        padding: 0.95rem 1.05rem;
        border: 1px solid rgba(148,163,184,0.16);
        background: rgba(255,255,255,0.88);
        box-shadow: 0 10px 22px rgba(15,23,42,0.06);
        backdrop-filter: blur(14px);
        animation: fadeUp 220ms ease both;
    }
    .card-strong{ background: rgba(255,255,255,0.94); }

    .divider-soft{
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(148,163,184,0.22), transparent);
        margin: 0.85rem 0;
    }

    .xp-track{
        width: 100%;
        height: 10px;
        border-radius: 999px;
        background: rgba(148,163,184,0.14);
        overflow: hidden;
        border: 1px solid rgba(148,163,184,0.14);
    }
    .xp-fill{
        height: 100%;
        border-radius: 999px;
        background: linear-gradient(90deg, rgba(14,165,233,0.70), rgba(167,139,250,0.22));
    }

    /* buttons: glassy but not loud; purple only on hover */
    .main div[data-testid="stButton"] button,
    section[data-testid="stSidebar"] div[data-testid="stButton"] button{
        border-radius: var(--r-btn) !important;
        border: 1px solid rgba(14,165,233,0.20) !important;
        background: linear-gradient(135deg, rgba(14,165,233,0.11), rgba(255,255,255,0.86)) !important;
        color: rgba(15,23,42,0.95) !important;
        font-weight: 650 !important;
    }
    .main div[data-testid="stButton"] button:hover,
    section[data-testid="stSidebar"] div[data-testid="stButton"] button:hover{
        transform: translateY(-1px);
        box-shadow: 0 0 0 3px rgba(167,139,250,0.22), 0 12px 26px rgba(2,6,23,0.10);
    }

    .btn-link{
        display:inline-flex;
        align-items:center;
        justify-content:center;
        gap:0.5rem;
        padding: 0.54rem 0.86rem;
        border-radius: var(--r-btn);
        border: 1px solid rgba(14,165,233,0.22);
        background: rgba(255,255,255,0.86);
        color: var(--text);
        text-decoration:none !important;
        font-weight: 650;
    }
    .btn-link:hover{
        border-color: rgba(167,139,250,0.22);
        box-shadow: 0 0 0 3px rgba(167,139,250,0.18), 0 12px 26px rgba(2,6,23,0.10);
        transform: translateY(-1px);
    }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

def hero(title: str, subtitle: str = "", badge: str | None = None) -> None:
    """Top hero banner used across pages."""
    badge_html = ""
    if badge:
        badge_html = f'<div class="hero-badge">{badge}</div>'

    st.markdown(
        f"""
        <div class="hero">
          <div style="display:flex; align-items:flex-start; justify-content:space-between; gap:12px;">
            <div>
              <div class="hero-title">{title}</div>
              <div class="hero-subtitle">{subtitle}</div>
            </div>
            {badge_html}
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
def soft_divider() -> None:
    st.markdown('<div class="divider-soft"></div>', unsafe_allow_html=True)

def xp_bar(pct: float, left: str, right: str) -> None:
    pct = max(0.0, min(1.0, float(pct or 0.0)))
    st.markdown(
        f"""
        <div style="margin-top:0.15rem; margin-bottom:0.1rem;">
          <div class="xp-track"><div class="xp-fill" style="width:{pct*100:.1f}%"></div></div>
          <div style="display:flex; justify-content:space-between; color: var(--muted); font-size: 0.85rem; margin-top: 0.32rem;">
            <span>{left}</span><span>{right}</span>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

def link_button(label: str, url: str) -> None:
    st.markdown(
        f'<a class="btn-link" href="{url}" target="_blank" rel="noopener noreferrer">{label} ↗</a>',
        unsafe_allow_html=True,
    )
def button_style(key: str, variant: str) -> None:
    """
    Style ONE Streamlit button by key using #st-key-<key>.
    Purple only for key CTAs (10% accent).
    """
    palette = {
        "blue":   ("rgba(14,165,233,0.16)", "rgba(255,255,255,0.86)", "rgba(14,165,233,0.28)"),
        "white":  ("rgba(255,255,255,0.92)", "rgba(255,255,255,0.92)", "rgba(148,163,184,0.18)"),
        "purple": ("rgba(167,139,250,0.14)", "rgba(255,255,255,0.86)", "rgba(167,139,250,0.28)"),
    }
    a, b, border = palette.get(variant, palette["blue"])
    st.markdown(
        f"""
        <style>
        #st-key-{key} button {{
            border: 1px solid {border} !important;
            background: linear-gradient(135deg, {a}, {b}) !important;
        }}
        #st-key-{key} button:hover {{
            box-shadow: 0 0 0 3px rgba(167,139,250,0.22), 0 12px 26px rgba(2,6,23,0.10) !important;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

def nav(active: str = "Home") -> None:
    # Only the pages that actively guide the user to the goal:
    # Agent -> Market buy/sell -> Profile wallet
    cols = st.columns(4)
    items = [
        ("Home", "app.py", "nav_home"),
        ("Agent", "pages/coach.py", "nav_agent"),
        ("Market", "pages/market.py", "nav_market"),
        ("Profile", "pages/profile.py", "nav_profile"),
    ]
    for i, (label, path, k) in enumerate(items):
        with cols[i]:
            if st.button(label, key=k, use_container_width=True):
                st.switch_page(path)

def bg_ratio() -> dict:
    return dict(_BG_RATIO)
