import re
import streamlit as st

from crowdlike.ui import apply_ui, hero, nav, link_button, soft_divider
from crowdlike.tour import maybe_run_tour
from crowdlike.auth import require_login, save_current_user, logout
from crowdlike.arc import (
    DEFAULT_RPC_URL,
    DEFAULT_EXPLORER,
    DEFAULT_USDC_ERC20,
    DEFAULT_USDC_DECIMALS,
    is_address,
)
from crowdlike.game import record_visit, ensure_user_schema, grant_xp, add_notification


DEMO_MODE = str(st.secrets.get("DEMO_MODE", "true")).lower() not in ("0", "false", "no")

AVATARS = ["🧊","🦋","🧠","🛰️","🪙","🦊","🦄","🐉","🧿","🪐","🌊","⚡","🫧","🧑‍🚀","🤖","🦈","🐙","🦜"]


def _is_safe_public_https_url(url: str) -> bool:
    u = (url or "").strip().lower()
    if not u.startswith("https://"):
        return False
    if "localhost" in u or "127." in u or "0.0.0.0" in u:
        return False
    return True


st.set_page_config(page_title="Profile", page_icon="🧑‍🚀", layout="wide")
apply_ui()

user = require_login(app_name="Crowdlike")
maybe_run_tour(user, current_page="profile")
ensure_user_schema(user)
record_visit(user, "profile")
save_current_user()

nav(active="Profile")
hero("🧑‍🚀  Profile", "Your identity, wallet, and app settings.", badge="Settings")


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
    user["username"] = st.text_input("Display name", value=user.get("username", "Member"), key="pf_name")
    user["bio"] = st.text_area("Bio (optional)", value=user.get("bio", ""), placeholder="What are you building?", key="pf_bio")

with c2:
    st.markdown(
        '<div class="card card-strong"><h3>Wallet</h3>'
        '<div style="color:var(--muted)">Only paste a public address (never a private key).</div></div>',
        unsafe_allow_html=True,
    )
    st.write("")
    wallet = user.setdefault("wallet", {}) if isinstance(user.get("wallet"), dict) else {}
    user["wallet"] = wallet

    wallet_addr = st.text_input(
        "Wallet address (public)",
        value=wallet.get("address", ""),
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

# ---- Autonomy & limits (policy gates) ----
st.subheader("Autonomy & Limits")
policy = user.setdefault("policy", {}) if isinstance(user.get("policy"), dict) else {}
user["policy"] = policy

risk = int(policy.get("risk", 25) or 25)
risk = st.slider("Risk level", 0, 100, value=risk, help="Controls your max-per-transaction, daily cap, and cooldown.", key="pf_risk")
policy["risk"] = risk

if risk <= 33:
    tier, max_tx, daily_cap, cooldown = "Conservative", 0.05, 0.25, 30
elif risk <= 66:
    tier, max_tx, daily_cap, cooldown = "Balanced", 0.10, 0.50, 15
else:
    tier, max_tx, daily_cap, cooldown = "Aggressive", 0.25, 1.00, 10

st.caption(f"Tier: **{tier}** — suggested defaults below. These are enforced before generating a payment command.")

c1, c2, c3 = st.columns(3)
with c1:
    policy["max_per_tx_usdc"] = st.number_input(
        "Max per transaction (USDC)",
        min_value=0.0,
        value=float(policy.get("max_per_tx_usdc", max_tx) or max_tx),
        step=0.01,
        format="%.2f",
        key="pf_max_tx",
    )
with c2:
    policy["daily_cap_usdc"] = st.number_input(
        "Daily cap (USDC)",
        min_value=0.0,
        value=float(policy.get("daily_cap_usdc", daily_cap) or daily_cap),
        step=0.05,
        format="%.2f",
        key="pf_daily_cap",
    )
with c3:
    policy["cooldown_s"] = st.number_input(
        "Cooldown (seconds)",
        min_value=0,
        value=int(policy.get("cooldown_s", cooldown) or cooldown),
        step=1,
        key="pf_cooldown",
    )

if st.button("Save limits", type="primary", key="pf_save_policy"):
    save_current_user()
    add_notification(user, "Limits saved.", "success")
    save_current_user()
    st.rerun()

soft_divider()

# ---- Advanced settings (keep clean by default) ----
st.subheader("Advanced")
adv = st.toggle("Developer mode (advanced network)", value=False, key="pf_adv_toggle")

if adv:
    st.markdown(
        '<div class="card"><h3>Network</h3>'
        '<div style="color:var(--muted)">Demo mode locks these to Arc testnet for safety.</div></div>',
        unsafe_allow_html=True,
    )
    st.write("")

    if DEMO_MODE:
        wallet["rpc_url"] = DEFAULT_RPC_URL
        wallet["explorer"] = DEFAULT_EXPLORER
        wallet["usdc_erc20"] = DEFAULT_USDC_ERC20
        wallet["usdc_decimals"] = DEFAULT_USDC_DECIMALS

        st.info("Demo mode is ON: network settings are locked.")
        st.code(DEFAULT_RPC_URL); st.caption("RPC URL (locked)")
        st.code(DEFAULT_EXPLORER); st.caption("Explorer base (locked)")
        st.code(DEFAULT_USDC_ERC20); st.caption("USDC ERC-20 interface (locked)")
        st.caption(f"USDC decimals (locked): {DEFAULT_USDC_DECIMALS}")
    else:
        rpc_in = st.text_input("RPC URL (https only)", value=wallet.get("rpc_url", DEFAULT_RPC_URL), key="pf_rpc")
        exp_in = st.text_input("Explorer base (https only)", value=wallet.get("explorer", DEFAULT_EXPLORER), key="pf_explorer")
        usdc_in = st.text_input("USDC ERC-20 address", value=wallet.get("usdc_erc20", DEFAULT_USDC_ERC20), key="pf_usdc_addr")
        dec_in = st.number_input(
            "USDC decimals",
            min_value=0,
            max_value=18,
            value=int(wallet.get("usdc_decimals", DEFAULT_USDC_DECIMALS)),
            step=1,
            key="pf_usdc_dec",
        )

        if not _is_safe_public_https_url(rpc_in) or not _is_safe_public_https_url(exp_in):
            st.warning("RPC/Explorer must be public https URLs (no localhost).")

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
                if not _is_safe_public_https_url(rpc_in) or not _is_safe_public_https_url(exp_in):
                    st.error("Please provide safe public https URLs (no localhost).")
                elif usdc_in and not is_address(usdc_in.strip()):
                    st.error("USDC address must be a valid 0x address.")
                else:
                    wallet["rpc_url"] = rpc_in.strip()
                    wallet["explorer"] = exp_in.strip()
                    wallet["usdc_erc20"] = usdc_in.strip()
                    wallet["usdc_decimals"] = int(dec_in)
                    save_current_user()
                    add_notification(user, "Advanced settings saved.", "success")
                    save_current_user()
                    st.rerun()

save_current_user()
