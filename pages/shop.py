import datetime as dt
import streamlit as st

from crowdlike.ui import apply_ui, hero, nav, soft_divider, link_button
from crowdlike.auth import require_login, save_current_user
from crowdlike.game import record_visit, ensure_user_schema, grant_xp, add_notification, log_activity
from crowdlike.arc import (
    cast_usdc_transfer_cmd,
    get_tx_receipt,
    verify_erc20_transfer,
    to_base_units,
    is_address,
    is_tx_hash,
    DEFAULT_EXPLORER,
    DEFAULT_RPC_URL,
)

st.set_page_config(page_title="Shop", page_icon="🛍️", layout="wide")
apply_ui()

user = require_login(app_name="Crowdlike")
ensure_user_schema(user)
record_visit(user, "shop")

nav(active="Shop")
hero("🛍️ Shop", "Drops, upgrades, and premium vibes.", badge="Store")

wallet = user.setdefault("wallet", {})
rpc_url = wallet.get("rpc_url", DEFAULT_RPC_URL)
explorer = wallet.get("explorer", DEFAULT_EXPLORER)
usdc_erc20 = wallet.get("usdc_erc20")
usdc_decimals = int(wallet.get("usdc_decimals", 6))

# ---- Catalog ----
ITEMS = [
    {"id":"neon_badge","name":"Neon Profile Badge","cat":"Cosmetics","desc":"A glowing badge next to your name.","price":150,"cur":"COINS","tag":"NEW"},
    {"id":"aura_theme","name":"Aura Theme Pack","cat":"Cosmetics","desc":"Extra UI accents + gradients.","price":220,"cur":"COINS","tag":"HOT"},
    {"id":"boost_xp","name":"XP Booster","cat":"Upgrades","desc":"+25% XP for the next 5 actions.","price":12,"cur":"GEMS","tag":"PRO"},
    {"id":"vip_drop","name":"VIP Drop Ticket","cat":"VIP","desc":"Access limited drops and exclusive offers.","price":"1.00","cur":"USDC","tag":"VIP"},
    {"id":"priority_list","name":"Priority Marketplace Listing","cat":"VIP","desc":"Your listing floats to the top (demo).","price":"0.25","cur":"USDC","tag":"FAST"},
    {"id":"creator_tip","name":"Creator Tip Jar","cat":"Community","desc":"Support the community treasury (demo).","price":"0.10","cur":"USDC","tag":"LOVE"},
    {"id":"mystery_box","name":"Mystery Box","cat":"Drops","desc":"Random reward (coins, gems, badge).","price":300,"cur":"COINS","tag":"DROP"},
]

cats = ["All"] + sorted({x["cat"] for x in ITEMS})
curs = ["All", "COINS", "GEMS", "USDC"]

top1, top2, top3 = st.columns([1.2, 0.9, 0.9])
with top1:
    cat = st.selectbox("Category", cats, key="shop_cat")
with top2:
    cur = st.selectbox("Currency", curs, key="shop_cur")
with top3:
    sort = st.selectbox("Sort", ["Featured", "Price: low → high", "Price: high → low"], key="shop_sort")

def _filter(items):
    out = []
    for it in items:
        if cat != "All" and it["cat"] != cat:
            continue
        if cur != "All" and it["cur"] != cur:
            continue
        out.append(it)
    return out

items = _filter(ITEMS)

def _price_key(it):
    p = it["price"]
    try:
        return float(p)
    except Exception:
        return 0.0

if sort == "Price: low → high":
    items = sorted(items, key=_price_key)
elif sort == "Price: high → low":
    items = sorted(items, key=_price_key, reverse=True)

# ---- Balances ----
st.markdown(
    f'<div style="display:flex;gap:0.5rem;flex-wrap:wrap">'
    f'<span class="chip">💵 Cash <b>${float(user.get("cash_usdc",0.0)):.2f}</b></span>'
    f'<span class="chip">🪙 Coins <b>{int(user.get("coins",0))}</b></span>'
    f'<span class="chip">💎 Gems <b>{int(user.get("gems",0))}</b></span>'
    f'</div>',
    unsafe_allow_html=True,
)

st.write("")
st.subheader("Storefront")

# Keep selection in session
st.session_state.setdefault("shop_selected", None)
selected = st.session_state.get("shop_selected")

cols = st.columns(3)
for i, it in enumerate(items):
    with cols[i % 3]:
        price = it["price"]
        if it["cur"] == "USDC":
            price_txt = f"${price} USDC (testnet)"
        elif it["cur"] == "COINS":
            price_txt = f"{price} coins"
        else:
            price_txt = f"{price} gems"

        st.markdown(
            f'''
            <div class="card" style="margin-bottom:0.75rem">
              <div style="display:flex;justify-content:space-between;align-items:center;gap:10px">
                <div style="font-weight:900">{it["name"]}</div>
                <div class="badge"><span class="badge-dot"></span>{it["tag"]}</div>
              </div>
              <div style="color:var(--muted);margin-top:0.35rem;min-height:44px">{it["desc"]}</div>
              <div style="margin-top:0.6rem;font-size:1.15rem;font-weight:900">{price_txt}</div>
              <div style="color:var(--muted);font-size:0.82rem;margin-top:0.25rem">Category: {it["cat"]}</div>
            </div>
            ''',
            unsafe_allow_html=True,
        )

        if st.button("Buy", type="primary", key=f"shop_buy_{it['id']}"):
            st.session_state["shop_selected"] = it["id"]
            selected = it["id"]
            st.rerun()

soft_divider()

# ---- Checkout or instant purchase ----
sel_item = next((x for x in ITEMS if x["id"] == selected), None)
if sel_item:
    st.subheader(f"Checkout • {sel_item['name']}")
    if sel_item["cur"] in ("COINS", "GEMS"):
        cur_key = "coins" if sel_item["cur"] == "COINS" else "gems"
        have = int(user.get(cur_key, 0))
        cost = int(sel_item["price"])
        st.markdown(
            f'<div class="card card-strong"><b>Instant purchase</b><br/>'
            f'<span style="color:var(--muted)">This uses your in-app balance (no blockchain needed).</span></div>',
            unsafe_allow_html=True,
        )
        st.write("")
        if have < cost:
            st.error(f"Not enough {cur_key}. You have {have}, need {cost}.")
        else:
            c1, c2 = st.columns([1, 1])
            with c1:
                if st.button("Confirm purchase", type="primary", key="shop_confirm_inapp"):
                    user[cur_key] = have - cost
                    user.setdefault("inventory", []).append(sel_item["id"])
                    grant_xp(user, 90, "Shop", f"Bought {sel_item['name']}")
                    add_notification(user, f"Purchased: {sel_item['name']} ✔️", "success")
                    log_activity(user, f"Bought {sel_item['name']} ({sel_item['price']} {sel_item['cur']})", icon="🛍️")
                    save_current_user()
                    st.success("Purchased ✅")
                    st.session_state["shop_selected"] = None
                    st.rerun()
            with c2:
                if st.button("Cancel", key="shop_cancel_inapp"):
                    st.session_state["shop_selected"] = None
                    st.rerun()

    else:
        st.markdown(
            '<div class="card card-strong"><b>Testnet checkout</b><br/>'
            '<span style="color:var(--muted)">You’ll generate a safe command, run it locally, then paste the receipt ID.</span>'
            '</div>',
            unsafe_allow_html=True,
        )
        st.write("")
        if not wallet.get("address"):
            st.warning("Set your wallet address in **Profile** first.")
            st.page_link("pages/profile.py", label="Go to Profile")
        else:
            treasury = st.text_input(
                "Treasury address (where payments go)",
                value=wallet.get("treasury_address", ""),
                placeholder="0x…",
                key="shop_treasury",
            )
            wallet["treasury_address"] = treasury.strip()

            price_usdc = str(sel_item["price"])
            if st.button("Generate payment command", type="primary", key="shop_gen_cmd"):
                if not is_address(treasury.strip()):
                    st.error("Enter a valid treasury address.")
                else:
                    cmd = cast_usdc_transfer_cmd(
                        to_address=treasury.strip(),
                        amount_usdc=price_usdc,
                        rpc_url=rpc_url,
                        usdc_erc20=usdc_erc20,
                        usdc_decimals=usdc_decimals,
                        private_key_env="$PRIVATE_KEY",
                    )
                    st.code(cmd, language="bash")
                    st.caption("Run it in your terminal. It outputs a tx hash (receipt ID).")

            tx = st.text_input("Receipt ID (tx hash)", placeholder="0x + 64 hex", key="shop_tx")
            if tx and is_tx_hash(tx.strip()):
                link_button("View receipt on ArcScan", f"{explorer}/tx/{tx.strip()}")

            if st.button("Verify receipt", key="shop_verify_btn"):
                if not is_tx_hash(tx.strip()):
                    st.error("Paste a valid receipt ID first.")
                elif not is_address(treasury.strip()):
                    st.error("Treasury address is missing.")
                else:
                    try:
                        rcpt = get_tx_receipt(rpc_url, tx.strip())
                        if not rcpt:
                            st.info("Receipt not found yet. Try again in a moment.")
                        else:
                            ok, msg = verify_erc20_transfer(
                                rcpt,
                                token_address=usdc_erc20,
                                to_address=treasury.strip(),
                                min_amount_base_units=to_base_units(price_usdc, usdc_decimals),
                            )
                            if ok:
                                user.setdefault("inventory", []).append(sel_item["id"])
                                user.setdefault("purchases", []).insert(
                                    0,
                                    {
                                        "ts": dt.datetime.utcnow().isoformat(timespec="seconds")+"Z",
                                        "item_id": sel_item["id"],
                                        "name": sel_item["name"],
                                        "price": price_usdc,
                                        "currency": "USDC(testnet)",
                                        "tx_hash": tx.strip(),
                                        "status": "verified",
                                    },
                                )
                                grant_xp(user, 180, "Shop", f"Bought {sel_item['name']}")
                                add_notification(user, f"Payment verified: {sel_item['name']} ✔️", "success")
                                log_activity(user, f"Paid ${price_usdc} for {sel_item['name']} (testnet)", icon="🧾")
                                save_current_user()
                                st.success("Verified ✅ (added to inventory)")
                                st.session_state["shop_selected"] = None
                                st.rerun()
                            else:
                                st.warning("Not verified yet.")
                                st.caption(msg)
                    except Exception as e:
                        st.error("Couldn’t verify via RPC. ArcScan link still works as proof.")
                        with st.expander("Details"):
                            st.exception(e)

soft_divider()

st.subheader("🎒 Your inventory")
inv = user.get("inventory") or []
if not inv:
    st.caption("No items yet. Buy something to see it here.")
else:
    for item_id in inv[-30:][::-1]:
        it = next((x for x in ITEMS if x["id"] == item_id), None)
        st.markdown(f'<div class="chip">✅ {it["name"] if it else item_id}</div>', unsafe_allow_html=True)

save_current_user()
