import streamlit as st

from crowdlike.ui import apply_ui, hero, nav, soft_divider, link_button
from crowdlike.tour import maybe_run_tour, tour_complete_step
from crowdlike.auth import require_login, save_current_user
from crowdlike.game import record_visit, ensure_user_schema, grant_xp, add_notification, log_activity
from crowdlike.market_data import get_markets, get_market_chart_7d
from crowdlike.policy import PaymentPolicy
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

st.set_page_config(page_title="Market", page_icon="📈", layout="wide")
apply_ui()

user = require_login(app_name="Crowdlike")

maybe_run_tour(user, current_page="market")
ensure_user_schema(user)
record_visit(user, "market")

nav(active="Market")
hero("📈 Market", "Live prices + easy buy/sell (practice) + testnet checkout.", badge="Market")

wallet = user.setdefault("wallet", {})
rpc_url = wallet.get("rpc_url", DEFAULT_RPC_URL)
explorer = wallet.get("explorer", DEFAULT_EXPLORER)
usdc_erc20 = wallet.get("usdc_erc20")
usdc_decimals = int(wallet.get("usdc_decimals", 6))

WATCHLIST = ["bitcoin", "ethereum", "solana", "avalanche-2", "chainlink", "polygon-ecosystem-token"]

tab_live, tab_practice, tab_checkout = st.tabs(["Live prices", "Practice buy/sell", "Testnet checkout"])

with tab_live:
    st.subheader("Live prices (CoinGecko)")
    try:
        rows = get_markets("usd", WATCHLIST)
    except Exception as e:
        rows = []
        st.error("Market data is unavailable right now.")
        with st.expander("Details"):
            st.exception(e)

    if rows:
        # Card grid
        cols = st.columns(3)
        for i, r in enumerate(rows):
            chg = r.price_change_percentage_24h
            chg_txt = "—" if chg is None else f"{chg:+.2f}%"
            chg_color = "var(--muted)"
            if chg is not None:
                if chg > 0:
                    chg_color = "var(--green)"
                elif chg < 0:
                    chg_color = "var(--red)"

            with cols[i % 3]:
                st.markdown(
                    f'''
                    <div class="card" style="margin-bottom:0.75rem">
                      <div style="display:flex;justify-content:space-between;align-items:flex-start;gap:10px">
                        <div>
                          <div style="font-weight:800">{r.name} <span style="color:var(--muted)">({r.symbol})</span></div>
                          <div style="font-size:1.35rem;font-weight:850">${r.current_price:,.2f}</div>
                        </div>
                        <div class="badge"><span class="badge-dot"></span>
                          <span style="font-weight:800;color:{chg_color}">{chg_txt}</span>
                        </div>
                      </div>
                      <div style="color:var(--muted);font-size:0.82rem;margin-top:0.45rem">
                        Rank #{r.market_cap_rank or "—"} · Volume {r.total_volume or 0:,.0f}
                      </div>
                    </div>
                    ''',
                    unsafe_allow_html=True,
                )

        soft_divider()
        coin_id = st.selectbox("View a 7‑day chart", [r.id for r in rows], key="mkt_chart_coin")
        try:
            pts = get_market_chart_7d(coin_id, "usd")
            if pts:
                st.line_chart([p[1] for p in pts], height=260)
        except Exception as e:
            st.warning("Chart unavailable right now.")
            with st.expander("Details"):
                st.exception(e)

    st.caption("Tip: Live prices are for the UI demo. Testnet checkout below is the on-chain part.")

with tab_practice:
    st.subheader("Practice buy/sell (simple + fun)")
    st.markdown(
        '<div class="card">This is a <b>practice</b> portfolio using live prices. '
        'It helps you demo trading UX without needing a DEX integration.</div>',
        unsafe_allow_html=True,
    )
    st.write("")



    portfolio = user.setdefault("portfolio", {"cash_usdc": 1000.0, "positions": {}, "trades": []})
    portfolio.setdefault("cash_usdc", 1000.0)
    portfolio.setdefault("positions", {})
    portfolio.setdefault("trades", [])

    try:
        rows = get_markets("usd", WATCHLIST)
    except Exception:
        rows = []
    price_map = {r.id: r.current_price for r in rows}

    if not rows:
        st.warning("Practice mode needs market prices. Try again later.")
    else:
        c1, c2, c3 = st.columns([1.2, 0.9, 0.9])
        with c1:
            coin = st.selectbox("Asset", [r.id for r in rows], format_func=lambda x: x, key="practice_coin")

        # Tutorial auto-advance: when the user *changes* the asset during step 4
        if st.session_state.get("tour_step") == 4:
            base = st.session_state.get("_tour_step4_base")
            if base is None:
                st.session_state["_tour_step4_base"] = coin
            elif coin != base:
                tour_complete_step(4)
        with c2:
            side = st.selectbox("Side", ["BUY", "SELL"], key="practice_side")
        with c3:
            amt = st.number_input("Amount (cash)", min_value=1.0, value=25.0, step=1.0, key="practice_amt")

        px = float(price_map.get(coin, 0.0) or 0.0)
        if px <= 0:
            st.error("Price missing.")
        else:
            qty = float(amt) / px
            st.write(f"Price: **${px:,.2f}** → Qty: **{qty:.6f}**")
            st.write("")

            m1, m2, m3 = st.columns(3)
            with m1:
                st.metric("Cash", f"${float(portfolio['cash_usdc']):.2f}")
            with m2:
                pos = float(portfolio["positions"].get(coin, 0.0))
                st.metric("Position", f"{pos:.6f}")
            with m3:
                st.metric("Pos value", f"${pos*px:.2f}")

            if st.button("Execute", type="primary", key="practice_exec"):
                if side == "BUY":
                    if float(portfolio["cash_usdc"]) < float(amt):
                        st.error("Not enough cash.")
                    else:
                        portfolio["cash_usdc"] = float(portfolio["cash_usdc"]) - float(amt)
                        portfolio["positions"][coin] = float(portfolio["positions"].get(coin, 0.0)) + qty
                        portfolio["trades"].insert(0, {"side": "BUY", "coin": coin, "cash": float(amt), "qty": qty, "price": px})
                        grant_xp(user, 45, "Market", "Practice BUY")
                        log_activity(user, f"Practice BUY {coin} (${amt:.2f})", icon="📈")
                        save_current_user()
                        st.success("Done ✅")
                        st.rerun()
                else:
                    pos = float(portfolio["positions"].get(coin, 0.0))
                    if pos < qty:
                        st.error("Not enough position to sell.")
                    else:
                        portfolio["cash_usdc"] = float(portfolio["cash_usdc"]) + float(amt)
                        portfolio["positions"][coin] = pos - qty
                        portfolio["trades"].insert(0, {"side": "SELL", "coin": coin, "cash": float(amt), "qty": qty, "price": px})
                        grant_xp(user, 45, "Market", "Practice SELL")
                        log_activity(user, f"Practice SELL {coin} (${amt:.2f})", icon="📉")
                        save_current_user()
                        st.success("Done ✅")
                        st.rerun()

            with st.expander("Portfolio & trade history", expanded=False):
                st.write("**Positions**")
                if not portfolio["positions"]:
                    st.caption("No positions yet.")
                else:
                    for k, v in portfolio["positions"].items():
                        if abs(float(v)) > 1e-12:
                            st.write(f"- {k}: {float(v):.6f}")

                st.write("**Trades**")
                if not portfolio["trades"]:
                    st.caption("No trades yet.")
                else:
                    st.dataframe(portfolio["trades"][:25], use_container_width=True, hide_index=True)

with tab_checkout:
    st.subheader("Testnet checkout (real on-chain receipt)")
    st.markdown(
        '<div class="card card-strong">'
        '<b>This is the on-chain part.</b> You pay using testnet USDC and we save a “receipt ID” (tx hash). '
        '<div style="color:var(--muted);margin-top:0.35rem">Private keys never enter the app — you run the command locally.</div>'
        '</div>',
        unsafe_allow_html=True,
    )
    st.write("")

    if not wallet.get("address"):
        st.warning("First: set your wallet address in **Profile**.")
        st.page_link("pages/profile.py", label="Go to Profile")
    else:
        # Choose a checkout item
        offers = [
            {"id": "vip_pass", "name": "VIP Pass", "desc": "Unlock VIP shop drops + flex badge.", "price": "1.00"},
            {"id": "api_credits", "name": "API Credits", "desc": "Pay-per-use credits (demo).", "price": "0.25"},
            {"id": "creator_tip", "name": "Creator Tip", "desc": "Tip the community treasury (demo).", "price": "0.10"},
        ]
        names = [f"{o['name']} — ${o['price']} (testnet)" for o in offers]
        idx = st.selectbox("What are you buying?", list(range(len(offers))), format_func=lambda i: names[i], key="checkout_offer")
        offer = offers[int(idx)]

        treasury = st.text_input(
            "Treasury address (where payments go)",
            value=wallet.get("treasury_address", ""),
            placeholder="0x…",
            key="checkout_treasury",
        )
        wallet["treasury_address"] = treasury.strip()

        c1, c2 = st.columns([1, 1])
        with c1:
            st.markdown(
                f'<div class="card"><h3>🧾 {offer["name"]}</h3>'
                f'<div style="color:var(--muted)">{offer["desc"]}</div>'
                f'<div style="margin-top:0.65rem;font-size:1.35rem;font-weight:900">${offer["price"]} USDC</div>'
                '</div>',
                unsafe_allow_html=True,
            )
        with c2:
            st.markdown(
                '<div class="card"><h3>✅ Steps</h3>'
                '<ol style="margin-left:1.2rem;color:var(--muted)">'
                '<li>Copy the payment command</li>'
                '<li>Run it in Git Bash / Terminal</li>'
                '<li>Paste the receipt ID here</li>'
                '</ol></div>',
                unsafe_allow_html=True,
            )

st.write("")
if st.button("Generate payment command", type="primary", key="checkout_gen_cmd"):
    if not is_address(treasury.strip()):
        st.error("Enter a valid treasury address.")
    else:
        policy = PaymentPolicy.from_user(user)
        ok_policy, why = policy.authorize_payment(user, offer["price"], commit=False)
        if not ok_policy:
            st.error(why)
        else:
            cmd = cast_usdc_transfer_cmd(
                to_address=treasury.strip(),
                amount_usdc=offer["price"],
                rpc_url=rpc_url,
                usdc_erc20=usdc_erc20,
                usdc_decimals=usdc_decimals,
                private_key_env="$PRIVATE_KEY",
            )
            st.code(cmd, language="bash")
            st.caption("Run this in your terminal. It will output a tx hash (receipt ID).")

receipt = st.text_input("Receipt ID (tx hash)", placeholder="0x + 64 hex", key="checkout_tx")
if receipt:
    if is_tx_hash(receipt.strip()):
        link_button("View receipt on ArcScan", f"{explorer}/tx/{receipt.strip()}")
    else:
        st.warning("This doesn’t look like a valid tx hash yet.")

st.write("")
if st.button("Verify receipt", type="primary", key="checkout_verify"):
    if not receipt or not is_tx_hash(receipt.strip()):
        st.error("Paste a valid receipt ID first.")
    elif not is_address(treasury.strip()):
        st.error("Treasury address is missing.")
    else:
        try:
            rcpt = get_tx_receipt(rpc_url, receipt.strip())
            if not rcpt:
                st.info("Receipt not found yet. Try again in a moment.")
            else:
                status = (rcpt.get("status") or "").lower()
                if status not in ("0x1", "1", 1):
                    st.error("Transaction failed (receipt status not successful).")
                    st.stop()

                # Verify at least the offer price
                ok, msg = verify_erc20_transfer(
                    rcpt,
                    token_address=usdc_erc20,
                    to_address=treasury.strip(),
                    min_amount_base_units=to_base_units(offer["price"], usdc_decimals),
                )
                if ok:
                    add_notification(user, f"Payment verified: {offer['name']} ✔️", "success")
                    grant_xp(user, 140, "Checkout", f"Bought {offer['name']}")
                    log_activity(user, f"Paid ${offer['price']} for {offer['name']} (testnet)", icon="🧾")

                    # Commit policy counters only after verification
                    PaymentPolicy.from_user(user).authorize_payment(user, offer["price"], commit=True)

                    # Save receipt idempotently (avoid duplicates on reruns)
                    txh = receipt.strip()
                    purchases = user.setdefault("purchases", [])
                    existing_i = None
                    for i, row in enumerate(purchases):
                        if isinstance(row, dict) and str(row.get("tx_hash", "")).lower() == txh.lower():
                            existing_i = i
                            break
                    rec = {
                        "ts": __import__("datetime").datetime.utcnow().isoformat(timespec="seconds") + "Z",
                        "item_id": offer["id"],
                        "name": offer["name"],
                        "price": offer["price"],
                        "currency": "USDC(testnet)",
                        "tx_hash": txh,
                        "status": "verified",
                    }
                    if existing_i is not None:
                        purchases.pop(existing_i)
                    purchases.insert(0, rec)

                    save_current_user()
                    st.success("Verified ✅ (saved to your profile)")
                else:
                    st.warning("Not verified yet.")
                    st.caption(msg)
        except Exception as e:
            st.error("Couldn’t verify via RPC. You can still use ArcScan as proof.")
            with st.expander("Details"):
                st.exception(e)

save_current_user()

# Guided tutorial (spotlight tour)
