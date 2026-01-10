import streamlit as st
from streamlit_cookies_manager import EncryptedCookieManager

from crowdlike.db import init_db
from crowdlike.auth import get_user_by_session

def init_app_context():
    init_db()

    cookie_pw = st.secrets.get("COOKIE_PASSWORD", "change-me")
    cookies = EncryptedCookieManager(prefix="crowdlike/", password=cookie_pw)
    if not cookies.ready():
        st.stop()

    # Load once per session
    if "user" not in st.session_state:
        token = cookies.get("session", "")
        user = get_user_by_session(token) if token else None
        st.session_state.user = user
        st.session_state.session_token = token if user else ""

    return cookies, st.session_state.get("user")
