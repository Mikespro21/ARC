from __future__ import annotations

import streamlit as st

from crowdlike.ui import button_style


def site_header(active: str = "Home") -> None:
    """Sticky website header with simple nav + primary CTA."""
    st.markdown('<div class="site-header">', unsafe_allow_html=True)
    a, b, c = st.columns([1.2, 2.2, 1.2], gap="large")

    with a:
        st.markdown('<div class="site-logo">🫧 <span>Crowdlike</span></div>', unsafe_allow_html=True)
        st.markdown('<div class="site-tag">Official demo build</div>', unsafe_allow_html=True)

    with b:
        # Keep this light; the real nav highlighting is handled by ui.nav
        st.markdown('<div class="site-links">Home · Product · Pricing · Docs</div>', unsafe_allow_html=True)

    with c:
        button_style("site_launch", "purple")
        if st.button("Launch App", key="site_launch", use_container_width=True):
            st.switch_page("pages/dashboard.py")
        button_style("site_journey", "ghost")
        if st.button("Journey", key="site_journey", use_container_width=True):
            st.switch_page("pages/journey.py")

    st.markdown("</div>", unsafe_allow_html=True)


def site_hero(*, kicker: str, title: str, subtitle: str) -> None:
    st.markdown(
        f'''
        <div class="site-hero">
          <div class="site-kicker">{kicker}</div>
          <div class="site-title">{title}</div>
          <div class="site-subtitle">{subtitle}</div>
        </div>
        ''',
        unsafe_allow_html=True,
    )


def site_section(*, icon: str, title: str, body: str, full_width: bool = False) -> None:
    cls = "site-section site-section-full" if full_width else "site-section"
    st.markdown(
        f'''
        <div class="{cls}">
          <div class="site-section-icon">{icon}</div>
          <div class="site-section-title">{title}</div>
          <div class="site-section-body">{body}</div>
        </div>
        ''',
        unsafe_allow_html=True,
    )


def site_footer() -> None:
    st.markdown(
        '''
        <div class="site-footer">
          <div class="site-footer-grid">
            <div>
              <div class="site-footer-title">Crowdlike</div>
              <div class="site-footer-muted">Agentic commerce with crowd-aware guardrails.</div>
            </div>
            <div>
              <div class="site-footer-title">Links</div>
              <div class="site-footer-links">Product · Pricing · Docs · Launch App</div>
            </div>
            <div>
              <div class="site-footer-title">Status</div>
              <div class="site-footer-muted">Local-first demo. No keys are stored by default.</div>
            </div>
          </div>
          <div class="site-footer-bottom">© Crowdlike — Demo build</div>
        </div>
        ''',
        unsafe_allow_html=True,
    )
