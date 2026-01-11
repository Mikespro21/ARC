from __future__ import annotations

import streamlit as st
import streamlit.components.v1 as components

# Enforced by background gradient stops:
# Blue = 0-30% (30)
# White = 30-90% (60)
# Purple = 90-100% (10)
_BG_RATIO = {"blue": 30, "white": 60, "purple": 10}


def apply_ui() -> None:
    """Global UI skin: premium glass cards, soft gradient, consistent pills/badges/steppers."""
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

        --green: #16A34A;
        --red: #EF4444;
        --amber: #F59E0B;

        --r-card: 12px;
        --r-hero: 14px;
        --r-btn: 14px;

        --border: rgba(148,163,184,0.16);
        --shadow: 0 14px 34px rgba(15, 23, 42, 0.10);
        --shadow-soft: 0 10px 22px rgba(15,23,42,0.06);
        --focus: 0 0 0 3px rgba(14,165,233,0.20);
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
            rgba(255,255,255,0.997) 0%,
            rgba(255,255,255,0.997) 58%,
            rgba(14,165,233,0.035) 100%
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

    /* Typography tightening (subtle) */
    h1,h2,h3{ letter-spacing: -0.015em; }
    h2{ margin-top: 0.2rem; }
    .stCaption, .stMarkdown small{ color: var(--muted); }

    /* Hero */
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
    .hero-title{ font-size: 1.42rem; font-weight: 820; letter-spacing: -0.02em; margin: 0; }
    .hero-subtitle{ margin-top: 0.20rem; font-size: 0.96rem; color: var(--muted); }
    .hero-badge{
        display:inline-flex;
        align-items:center;
        justify-content:center;
        padding: 0.36rem 0.62rem;
        border-radius: 999px;
        border: 1px solid rgba(167,139,250,0.26);
        background: rgba(167,139,250,0.10);
        color: rgba(15,23,42,0.92);
        font-weight: 760;
        font-size: 0.86rem;
        white-space: nowrap;
    }

    /* Cards */
    .card{
        border-radius: var(--r-card);
        padding: 0.95rem 1.05rem;
        border: 1px solid rgba(148,163,184,0.16);
        background: rgba(255,255,255,0.88);
        box-shadow: var(--shadow-soft);
        backdrop-filter: blur(14px);
        animation: fadeUp 220ms ease both;
    }
    .card:hover{
        border-color: rgba(14,165,233,0.20);
        box-shadow: 0 14px 30px rgba(2,6,23,0.08);
        transform: translateY(-1px);
        transition: 160ms ease;
    }
    .card-strong{ background: rgba(255,255,255,0.94); }

    .divider-soft{
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(148,163,184,0.22), transparent);
        margin: 0.85rem 0;
    }

    /* Pills / badges */
    .pill-row{ display:flex; gap:0.45rem; flex-wrap:wrap; margin: 0.15rem 0 0.65rem; }
    .pill{
        display:inline-flex;
        align-items:center;
        gap:0.45rem;
        padding: 0.32rem 0.58rem;
        border-radius: 999px;
        border: 1px solid rgba(148,163,184,0.18);
        background: rgba(255,255,255,0.86);
        font-weight: 680;
        font-size: 0.86rem;
        color: rgba(15,23,42,0.92);
    }
    .pill .k{ color: var(--muted); font-weight: 720; }
    .pill.info{ border-color: rgba(14,165,233,0.20); background: rgba(14,165,233,0.06); }
    .pill.good{ border-color: rgba(22,163,74,0.20); background: rgba(22,163,74,0.06); }
    .pill.warn{ border-color: rgba(245,158,11,0.22); background: rgba(245,158,11,0.07); }
    .pill.bad{ border-color: rgba(239,68,68,0.18); background: rgba(239,68,68,0.06); }

    .badge{
        display:inline-flex;
        align-items:center;
        gap:0.35rem;
        padding: 0.28rem 0.50rem;
        border-radius: 999px;
        border: 1px solid rgba(148,163,184,0.18);
        background: rgba(255,255,255,0.86);
        color: rgba(15,23,42,0.90);
        font-size: 0.84rem;
        font-weight: 740;
    }
    .badge-dot{
        width: 8px; height: 8px; border-radius: 999px;
        background: rgba(14,165,233,0.55);
        box-shadow: 0 0 0 3px rgba(14,165,233,0.12);
    }

    /* Callouts */
    .callout{
        border-radius: 12px;
        border: 1px solid rgba(148,163,184,0.18);
        background: rgba(255,255,255,0.90);
        padding: 0.78rem 0.92rem;
        box-shadow: var(--shadow-soft);
    }
    .callout .t{ font-weight: 820; }
    .callout .b{ color: var(--muted); margin-top: 0.22rem; }
    .callout.info{ border-color: rgba(14,165,233,0.20); background: rgba(14,165,233,0.06); }
    .callout.warn{ border-color: rgba(245,158,11,0.22); background: rgba(245,158,11,0.07); }
    .callout.bad{ border-color: rgba(239,68,68,0.18); background: rgba(239,68,68,0.06); }
    .callout.good{ border-color: rgba(22,163,74,0.20); background: rgba(22,163,74,0.06); }

    /* XP bar */
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
        background: linear-gradient(90deg, rgba(14,165,233,0.75), rgba(167,139,250,0.25));
    }

    /* Stepper */
    .stepper{
        display:flex;
        gap: 0.55rem;
        flex-wrap:wrap;
        margin: 0.05rem 0 0.55rem;
    }
    .step{
        display:inline-flex;
        align-items:center;
        gap: 0.45rem;
        padding: 0.35rem 0.62rem;
        border-radius: 999px;
        border: 1px solid rgba(148,163,184,0.18);
        background: rgba(255,255,255,0.88);
        font-weight: 760;
        font-size: 0.86rem;
        color: rgba(15,23,42,0.92);
    }
    .step .n{
        width: 18px; height: 18px; border-radius: 999px;
        display:inline-flex; align-items:center; justify-content:center;
        font-size: 0.80rem;
        background: rgba(148,163,184,0.14);
        border: 1px solid rgba(148,163,184,0.18);
        color: rgba(15,23,42,0.82);
    }
    .step.active{ border-color: rgba(167,139,250,0.26); background: rgba(167,139,250,0.10); }
    .step.active .n{ border-color: rgba(167,139,250,0.30); background: rgba(167,139,250,0.12); }
    .step.done{ border-color: rgba(22,163,74,0.22); background: rgba(22,163,74,0.06); }
    .step.done .n{ border-color: rgba(22,163,74,0.22); background: rgba(22,163,74,0.10); }

    /* Links */
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

    /* Buttons: glassy but not loud; purple only for highlighted CTAs */
    .main div[data-testid="stButton"] button,
    section[data-testid="stSidebar"] div[data-testid="stButton"] button{
        border-radius: var(--r-btn) !important;
        border: 1px solid rgba(14,165,233,0.20) !important;
        background: linear-gradient(135deg, rgba(14,165,233,0.11), rgba(255,255,255,0.86)) !important;
        color: rgba(15,23,42,0.95) !important;
        font-weight: 670 !important;
    }
    .main div[data-testid="stButton"] button:hover,
    section[data-testid="stSidebar"] div[data-testid="stButton"] button:hover{
        transform: translateY(-1px);
        box-shadow: 0 0 0 3px rgba(167,139,250,0.22), 0 12px 26px rgba(2,6,23,0.10);
    }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)


def hero(title: str, subtitle: str = "", badge: str | None = None) -> None:
    """Top hero banner used across pages."""
    badge_html = f'<div class="hero-badge">{badge}</div>' if badge else ""
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


def pills(items: list[tuple[str, str, str]]) -> None:
    """Render a compact row of pills: [(key, value, kind)]. kind in info|good|warn|bad."""
    html = ['<div class="pill-row">']
    for k, v, kind in items:
        kind = kind if kind in ("info", "good", "warn", "bad") else "info"
        html.append(f'<div class="pill {kind}"><span class="k">{k}</span><span>{v}</span></div>')
    html.append("</div>")
    st.markdown("".join(html), unsafe_allow_html=True)


def status_bar(
    *,
    wallet_set: bool,
    demo_mode: bool,
    crowd_score: float | None = None,
    network_label: str = "Arc testnet",
) -> None:
    """Small status strip to reduce confusion during demos."""
    crowd_score = float(crowd_score) if crowd_score is not None else None
    items: list[tuple[str, str, str]] = []
    items.append(("Network", network_label, "info"))
    items.append(("Demo", "ON" if demo_mode else "OFF", "good" if demo_mode else "warn"))
    items.append(("Wallet", "Connected" if wallet_set else "Missing", "good" if wallet_set else "bad"))
    if crowd_score is not None:
        kind = "good" if crowd_score >= 70 else ("warn" if crowd_score < 40 else "info")
        items.append(("Crowd", f"{crowd_score:.0f}", kind))
    pills(items)


def callout(kind: str, title: str, body: str) -> None:
    kind = kind if kind in ("info", "good", "warn", "bad") else "info"
    st.markdown(
        f'<div class="callout {kind}"><div class="t">{title}</div><div class="b">{body}</div></div>',
        unsafe_allow_html=True,
    )


def stepper(current: int, labels: list[str]) -> None:
    """Visual stepper (display-only). Use alongside radio/flow state."""
    current = int(current or 1)
    html = ['<div class="stepper">']
    for i, lab in enumerate(labels, start=1):
        cls = "step"
        if i < current:
            cls += " done"
        elif i == current:
            cls += " active"
        html.append(f'<div class="{cls}"><span class="n">{i}</span><span>{lab}</span></div>')
    html.append("</div>")
    st.markdown("".join(html), unsafe_allow_html=True)


def toast(msg: str, kind: str = "info") -> None:
    """Nice feedback without breaking older Streamlit versions."""
    try:
        # Newer Streamlit
        st.toast(msg, icon="✅" if kind == "good" else "⚠️" if kind == "warn" else "ℹ️")
        return
    except Exception:
        pass
    if kind == "good":
        st.success(msg)
    elif kind == "warn":
        st.warning(msg)
    elif kind == "bad":
        st.error(msg)
    else:
        st.info(msg)


def copy_to_clipboard(text: str, key: str, label: str = "Copy") -> None:
    """Small inline copy-to-clipboard button (uses browser clipboard API)."""
    # Use JSON encoding so newlines/quotes/backticks can't break the JS string.
    import json as _json  # local import to keep ui.py lightweight

    payload = _json.dumps(text or "")

    html = f"""
    <div style="display:flex; gap:10px; align-items:center; margin-top: 0.35rem;">
      <button id="btn_{key}" style="
        cursor:pointer; padding: 8px 12px; border-radius: 12px;
        border: 1px solid rgba(14,165,233,0.22);
        background: rgba(255,255,255,0.86);
        font-weight: 700;
      ">{label}</button>
      <span id="msg_{key}" style="color: rgba(100,116,139,0.95); font-size: 0.88rem;"></span>
    </div>
    <script>
      const payload = {payload};
      const btn = document.getElementById("btn_{key}");
      const msg = document.getElementById("msg_{key}");
      btn.addEventListener("click", async () => {{
        try {{
          await navigator.clipboard.writeText(payload);
          msg.textContent = "Copied ✓";
          setTimeout(() => msg.textContent = "", 1200);
        }} catch (e) {{
          msg.textContent = "Copy failed (browser blocked)";
          setTimeout(() => msg.textContent = "", 1600);
        }}
      }});
    </script>
    """
    components.html(html, height=46)


def metric_card(title: str, value: str, caption: str = "", *, accent: str = "blue") -> None:
    accents = {
        "blue": "rgba(14,165,233,0.18)",
        "purple": "rgba(167,139,250,0.22)",
        "none": "rgba(148,163,184,0.16)",
    }
    border = accents.get(accent, accents["blue"])
    cap_html = f'<div style="color:var(--muted);font-size:0.9rem">{caption}</div>' if caption else ""
    st.markdown(
        '<div class="card card-strong" style="border:1px solid ' + border + '; background: rgba(255,255,255,0.94);">'
        f'<div style="font-weight:780">{title}</div>'
        f'<div style="font-size:1.45rem;font-weight:900;margin-top:4px">{value}</div>'
        f'{cap_html}'
        '</div>',
        unsafe_allow_html=True,
    )


def button_style(key: str, variant: str) -> None:
    """
    Style ONE Streamlit button by key using #st-key-<key>.
    Keep palette aligned with 60/30/10 (white/blue/purple).
    """
    palette = {
        # Neutral / nav
        "white": ("rgba(255,255,255,0.92)", "rgba(255,255,255,0.92)", "rgba(148,163,184,0.18)"),
        # Primary
        "blue": ("rgba(14,165,233,0.16)", "rgba(255,255,255,0.86)", "rgba(14,165,233,0.28)"),
        # Accent (use sparingly)
        "purple": ("rgba(167,139,250,0.14)", "rgba(255,255,255,0.86)", "rgba(167,139,250,0.28)"),
        # Subtle flavors (still within palette)
        "teal": ("rgba(14,165,233,0.10)", "rgba(255,255,255,0.92)", "rgba(14,165,233,0.22)"),
        "slate": ("rgba(148,163,184,0.12)", "rgba(255,255,255,0.92)", "rgba(148,163,184,0.22)"),
        "rose": ("rgba(167,139,250,0.10)", "rgba(255,255,255,0.92)", "rgba(167,139,250,0.22)"),
        "active": ("rgba(167,139,250,0.16)", "rgba(255,255,255,0.90)", "rgba(167,139,250,0.32)"),
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
        unsafe_allow_html=True,
    )


def nav(active: str = "Home") -> None:
    """Top nav split into 2 rows to keep it readable."""
    row1 = [
        ("Home", "app.py", "nav_home"),
        ("Agent", "pages/coach.py", "nav_agent"),
        ("Market", "pages/market.py", "nav_market"),
        ("Profile", "pages/profile.py", "nav_profile"),
    ]
    row2 = [
        ("Quests", "pages/quests.py", "nav_quests"),
        ("Shop", "pages/shop.py", "nav_shop"),
        ("Social", "pages/social.py", "nav_social"),
    ]

    cols = st.columns(len(row1))
    for i, (label, path, k) in enumerate(row1):
        with cols[i]:
            button_style(k, "active" if label == active else "white")
            if st.button(label, key=k, use_container_width=True):
                st.switch_page(path)

    cols2 = st.columns(len(row2))
    for i, (label, path, k) in enumerate(row2):
        with cols2[i]:
            button_style(k, "active" if label == active else "white")
            if st.button(label, key=k, use_container_width=True):
                st.switch_page(path)

    st.markdown('<div class="divider-soft" style="margin-top:0.65rem;margin-bottom:0.55rem;"></div>', unsafe_allow_html=True)


def bg_ratio() -> dict:
    return dict(_BG_RATIO)
