from __future__ import annotations

import streamlit as st

_UI_KEY = "_crowdlike_ui_applied"


def apply_ui() -> None:
    """Apply the global Crowdlike UI (light-blue → white → light-purple)."""
    if st.session_state.get(_UI_KEY):
        return

    css = r"""
    <style>
    :root{
        --bg-1: #E0F2FE;           /* sky-100 */
        --bg-2: #FFFFFF;
        --bg-3: #F3E8FF;           /* purple-100 */
        --card: rgba(255,255,255,0.72);
        --card-2: rgba(255,255,255,0.86);
        --border: rgba(148,163,184,0.28);
        --text: #0F172A;
        --muted: #64748B;
        --blue: #0EA5E9;
        --blue-2: #38BDF8;
        --purple: #A78BFA;
        --purple-2: #8B5CF6;
        --green: #22C55E;
        --amber: #F59E0B;
        --red: #EF4444;
        --shadow: 0 22px 45px rgba(15, 23, 42, 0.18);
        --r-lg: 18px;
        --r-xl: 24px;
        --pill: 999px;
    }

    .stApp{
        background:
            radial-gradient(1000px 520px at 10% 0%, rgba(56,189,248,0.35), transparent 65%),
            radial-gradient(900px 520px at 90% 10%, rgba(167,139,250,0.26), transparent 60%),
            radial-gradient(circle at 55% 35%, #FFFFFF 0%, #FFFFFF 22%, rgba(255,255,255,0.65) 45%, transparent 70%),
            linear-gradient(135deg, var(--bg-1) 0%, var(--bg-2) 42%, var(--bg-3) 100%);
        color: var(--text);
        font-family: system-ui, -apple-system, BlinkMacSystemFont, "SF Pro Text", "Inter", "Segoe UI", sans-serif;
    }

    header[data-testid="stHeader"]{ background: transparent; }
    footer{ visibility:hidden; }

    .main .block-container{
        padding-top: 0.8rem;
        padding-bottom: 3rem;
        max-width: 1180px;
    }

    section[data-testid="stSidebar"]{
        background: linear-gradient(180deg, rgba(224,242,254,0.75) 0%, rgba(243,232,255,0.55) 100%);
        border-right: 1px solid rgba(148,163,184,0.22);
    }

    .hero{
        border-radius: var(--r-xl);
        padding: 1.25rem 1.35rem;
        border: 1px solid rgba(56,189,248,0.28);
        background:
            radial-gradient(600px 140px at 18% 25%, rgba(56,189,248,0.25), transparent 65%),
            radial-gradient(520px 160px at 82% 0%, rgba(167,139,250,0.22), transparent 55%),
            rgba(255,255,255,0.65);
        box-shadow: var(--shadow);
        backdrop-filter: blur(14px);
        margin-bottom: 0.9rem;
    }
    .hero-title{
        font-size: 1.55rem;
        font-weight: 750;
        letter-spacing: -0.02em;
        margin: 0;
    }
    .hero-subtitle{
        margin-top: 0.25rem;
        font-size: 0.98rem;
        color: var(--muted);
    }

    .card{
        border-radius: var(--r-lg);
        padding: 1.1rem 1.15rem;
        border: 1px solid var(--border);
        background: var(--card);
        box-shadow: 0 14px 34px rgba(15,23,42,0.10);
        backdrop-filter: blur(14px);
    }
    .card-strong{
        background: var(--card-2);
    }
    .card h3, .card h4{ margin-top: 0.1rem; }

    .badge{
        display:inline-flex;
        align-items:center;
        gap:0.45rem;
        padding: 0.28rem 0.65rem;
        border-radius: var(--pill);
        border: 1px solid rgba(148,163,184,0.25);
        background: rgba(255,255,255,0.75);
        font-size: 0.82rem;
        color: var(--text);
    }
    .badge-dot{
        width: 8px; height: 8px; border-radius: 999px;
        background: linear-gradient(135deg, var(--blue), var(--purple));
        box-shadow: 0 0 0 3px rgba(56,189,248,0.18);
    }

    .chip{
        display:inline-flex;
        align-items:center;
        justify-content:space-between;
        gap:0.6rem;
        padding: 0.42rem 0.75rem;
        border-radius: var(--pill);
        border: 1px solid rgba(148,163,184,0.24);
        background: rgba(255,255,255,0.70);
        font-size: 0.85rem;
        color: var(--text);
    }
    .chip b{ font-weight: 750; }

    .btn-link{
        display:inline-flex;
        align-items:center;
        justify-content:center;
        gap:0.5rem;
        padding: 0.56rem 0.9rem;
        border-radius: 14px;
        border: 1px solid rgba(56,189,248,0.38);
        background: linear-gradient(135deg, rgba(14,165,233,0.16), rgba(167,139,250,0.12));
        color: var(--text);
        text-decoration:none !important;
        font-weight: 650;
    }
    .btn-link:hover{
        border-color: rgba(139,92,246,0.55);
        box-shadow: 0 12px 30px rgba(139,92,246,0.18);
        transform: translateY(-1px);
    }

    .divider-soft{
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(148,163,184,0.35), transparent);
        margin: 0.9rem 0;
    }

    .xp-track{
        width: 100%;
        height: 10px;
        border-radius: 999px;
        background: rgba(148,163,184,0.18);
        overflow: hidden;
        border: 1px solid rgba(148,163,184,0.22);
    }
    .xp-fill{
        height: 100%;
        border-radius: 999px;
        background: linear-gradient(90deg, rgba(56,189,248,0.90), rgba(167,139,250,0.85));
    }

    /* Simple centered login overlay (fallback if st.dialog not available) */
    .overlay{
        position: fixed;
        inset: 0;
        display: flex;
        align-items: center;
        justify-content: center;
        background: rgba(2,6,23,0.35);
        z-index: 1000;
    }
    .overlay-inner{
        width: min(520px, 92vw);
        border-radius: 22px;
        padding: 1.1rem 1.1rem 0.9rem;
        background: rgba(255,255,255,0.92);
        border: 1px solid rgba(148,163,184,0.25);
        box-shadow: 0 26px 70px rgba(2,6,23,0.30);
        backdrop-filter: blur(16px);
    }
    .overlay-title{
        font-weight: 800;
        font-size: 1.25rem;
        margin-bottom: 0.35rem;
    }
    .overlay-subtitle{
        color: var(--muted);
        margin-bottom: 0.75rem;
    }
    </style>
    """

    st.markdown(css, unsafe_allow_html=True)
    st.session_state[_UI_KEY] = True


def hero(title: str, subtitle: str = "", badge: str | None = None) -> None:
    badge_html = "" if not badge else f'<span class="badge"><span class="badge-dot"></span>{badge}</span>'
    st.markdown(
        f"""
        <div class="hero">
          <div style="display:flex; align-items:center; justify-content:space-between; gap: 12px;">
            <div>
              <div class="hero-title">{title}</div>
              <div class="hero-subtitle">{subtitle}</div>
            </div>
            <div>{badge_html}</div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def link_button(label: str, url: str, icon: str = "↗") -> None:
    st.markdown(f'<a class="btn-link" href="{url}" target="_blank">{label} <span style="opacity:0.75">{icon}</span></a>', unsafe_allow_html=True)


def soft_divider() -> None:
    st.markdown('<div class="divider-soft"></div>', unsafe_allow_html=True)


def xp_bar(pct: float, left: str, right: str) -> None:
    pct = max(0.0, min(1.0, float(pct or 0.0)))
    st.markdown(
        f"""
        <div style="margin-top:0.2rem; margin-bottom:0.15rem;">
          <div class="xp-track"><div class="xp-fill" style="width:{pct*100:.1f}%"></div></div>
          <div style="display:flex; justify-content:space-between; color: var(--muted); font-size: 0.85rem; margin-top: 0.35rem;">
            <span>{left}</span><span>{right}</span>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def nav(active: str = "Home") -> None:
    """Top navigation row that connects all pages."""
    cols = st.columns(6)
    # Use page_link if available; fallback to text
    page_link = getattr(st, "page_link", None)

    items = [
        ("🏠 Home", "app.py"),
        ("📈 Market", "pages/market.py"),
        ("🛍️ Shop", "pages/shop.py"),
        ("👥 Social", "pages/social.py"),
        ("🎯 Quests", "pages/quests.py"),
        ("🧑‍🚀 Profile", "pages/profile.py"),
    ]

    for i, (label, path) in enumerate(items):
        with cols[i]:
            if callable(page_link):
                try:
                    page_link(path, label=label)
                except TypeError:
                    # Some Streamlit versions use different arg name
                    st.markdown(f"**{label}**")
            else:
                st.markdown(f"**{label}**")

