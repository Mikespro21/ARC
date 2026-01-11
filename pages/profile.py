import streamlit as st

from crowdlike.ui import apply_ui, hero, nav, link_button, soft_divider
from crowdlike.tour import maybe_run_tour, tour_complete_step
from crowdlike.auth import require_login, save_current_user, logout
from crowdlike.arc import (
    DEFAULT_RPC_URL,
    DEFAULT_EXPLORER,
    DEFAULT_USDC_ERC20,
    DEFAULT_USDC_DECIMALS,
    is_address,
)
from crowdlike.game import record_visit, ensure_user_schema, grant_xp, add_notification

st.set_page_config(page_title="Profile", page_icon="🧑‍🚀", layout="wide")
apply_ui()

user = require_login(app_name="Crowdlike")

maybe_run_tour(user, current_page="profile")
ensure_user_schema(user)
record_visit(user, "profile")

nav(active="Profile")
hero("🧑‍🚀 Profile", "Customize your identity, wallet, and app settings.", badge="Settings")

AVATARS = ["🧊","🦋","🧠","🛰️","🪙","🦊","🦄","🐉","🧿","🪐","🌊","⚡","🫧","🧑‍🚀","🤖","🦈","🐙","🦜"]

# ---- Profile basics ----
c1, c2 = st.columns([1, 1])

with c1:
    st.markdown('<div class="card card-strong"><h3>Identity</h3></div>', unsafe_allow_html=True)
    st.write("")
    current_avatar = user.get("avatar", "🧊")
    try:
        avatar_index = AVATARS.index(current_avatar)
    except ValueError:
        avatar_index = 0

    user["avatar"] = st.selectbox("Avatar", AVATARS, index=avatar_index, key="pf_avatar")
    user["username"] = st.text_input("Display name", value=user.get("username","Member"), key="pf_name")
    user["bio"] = st.text_area("Bio", value=user.get("bio",""), placeholder="What are you building?", key="pf_bio")

with c2:
    st.markdown(
        '<div class="card card-strong"><h3>Wallet</h3>'
        '<div style="color:var(--muted)">Only paste a public address (never a private key).</div></div>',
        unsafe_allow_html=True,
    )
    st.write("")
    wallet = user.setdefault("wallet", {})
    wallet_addr = st.text_input(
        "Wallet address (public)",
        value=wallet.get("address",""),
        placeholder="0x...",
        key="pf_wallet",
    )
    if wallet_addr and not is_address(wallet_addr.strip()):
        st.warning("That doesn’t look like a valid 0x address.")
    wallet["address"] = wallet_addr.strip()

    cols = st.columns([1, 1, 1])
    with cols[0]:
        if st.button("Save profile", type="primary", key="pf_save"):
            save_current_user()
            grant_xp(user, 60, "Profile", "Updated settings")
            add_notification(user, "Saved ✔️", "success")
            save_current_user()
            st.rerun()
    with cols[1]:
        if st.button("Log out", key="pf_logout"):
            logout()
            st.rerun()
    with cols[2]:
        st.write("")

    if wallet.get("address"):
        st.write("")
        explorer = wallet.get("explorer", DEFAULT_EXPLORER)
        link_button("Open wallet on ArcScan (testnet)", f"{explorer}/address/{wallet.get('address')}")
        st.caption("Tip: You can get a testnet wallet from any EVM wallet app (MetaMask, Rabby, etc.).")

soft_divider()

# ---- Advanced settings (keep clean by default) ----
st.subheader("Advanced")
adv = st.toggle("Show advanced network settings", value=False, key="pf_adv_toggle")

if adv:
    st.markdown(
        '<div class="card"><h3>Network</h3>'
        '<div style="color:var(--muted)">These defaults work for Arc testnet. Change only if you know why.</div></div>',
        unsafe_allow_html=True,
    )
    st.write("")
    wallet["rpc_url"] = st.text_input("RPC URL", value=wallet.get("rpc_url", DEFAULT_RPC_URL), key="pf_rpc")
    wallet["explorer"] = st.text_input("Explorer base", value=wallet.get("explorer", DEFAULT_EXPLORER), key="pf_explorer")
    wallet["usdc_erc20"] = st.text_input("USDC ERC-20 address", value=wallet.get("usdc_erc20", DEFAULT_USDC_ERC20), key="pf_usdc_addr")
    wallet["usdc_decimals"] = st.number_input(
        "USDC decimals",
        min_value=0,
        max_value=18,
        value=int(wallet.get("usdc_decimals", DEFAULT_USDC_DECIMALS)),
        key="pf_usdc_dec",
    )

    b1, b2 = st.columns([1, 1])
    with b1:
        if st.button("Reset to defaults", key="pf_reset_defaults"):
            wallet["rpc_url"] = DEFAULT_RPC_URL
            wallet["explorer"] = DEFAULT_EXPLORER
            wallet["usdc_erc20"] = DEFAULT_USDC_ERC20
            wallet["usdc_decimals"] = DEFAULT_USDC_DECIMALS
            save_current_user()
            st.rerun()
    with b2:
        if st.button("Save advanced settings", type="primary", key="pf_save_adv"):
            save_current_user()
            add_notification(user, "Advanced settings saved.", "success")
            save_current_user()
            st.rerun()

save_current_user()

# Guided tutorial (spotlight tour)