from __future__ import annotations

from datetime import datetime

import pandas as pd
import streamlit as st

from crowdlike.market import safe_market_data, DEFAULT_IDS
from crowdlike.state import ensure_state
from crowdlike.style import apply, card_start, card_end
from crowdlike.ui import fmt_usd

st.set_page_config(page_title="Market • Crowdlike", page_icon="💱", layout="wide")
apply()
ensure_state()

st.markdown("# Market")
st.caption("Paper trade with real market prices (CoinGecko) when available. Falls back to demo prices when offline.")

market = safe_market_data(DEFAULT_IDS)
mdf = pd.DataFrame(market)
mdf_display = mdf[["name","symbol","currentPrice","priceChangePercent24h","marketCap","volume24h"]].copy()
mdf_display.rename(columns={
    "name":"Asset",
    "symbol":"Symbol",
    "currentPrice":"Price (USD)",
    "priceChangePercent24h":"24h %",
    "marketCap":"Market Cap",
    "volume24h":"Volume 24h",
}, inplace=True)

card_start("Market Overview")
st.dataframe(mdf_display, use_container_width=True, hide_index=True)
card_end()

agents = st.session_state["agents"]
if not agents:
    st.info("Create an agent first (Agents page).")
    st.stop()

# Trading form
card_start("Paper Trade")
left, right = st.columns([1,1], gap="large")

with left:
    agent_name_to_id = {a["name"]: a["id"] for a in agents}
    agent_name = st.selectbox("Agent", list(agent_name_to_id.keys()))
    agent = next(a for a in agents if a["id"] == agent_name_to_id[agent_name])

with right:
    asset_name_to_id = {row["name"]: row["id"] for row in market}
    asset_name = st.selectbox("Asset", list(asset_name_to_id.keys()))
    asset_id = asset_name_to_id[asset_name]
    row = next(x for x in market if x["id"] == asset_id)
    price = float(row["currentPrice"])
    st.metric("Current Price", f"${price:,.6f}" if price < 1 else f"${price:,.2f}")

trade_type = st.radio("Type", ["buy","sell"], horizontal=True)
amount = st.number_input("Amount (units of asset)", min_value=0.0, value=0.01, step=0.01)

reason = st.text_input("Reason (optional)", placeholder="e.g., momentum, mean reversion, crowd signal…")
approved = st.checkbox("Approved", value=True)

if st.button("Execute paper trade"):
    if amount <= 0:
        st.warning("Amount must be > 0.")
    else:
        usdc_amount = amount * price
        portfolio = agent["portfolio"]

        # Buy
        if trade_type == "buy":
            if usdc_amount > portfolio["usdcBalance"]:
                st.warning("Insufficient USDC balance for this agent.")
            else:
                portfolio["usdcBalance"] -= usdc_amount
                pos = next((p for p in portfolio["positions"] if p["asset"] == asset_id), None)
                if pos:
                    total_amount = pos["amount"] + amount
                    total_cost = (pos["amount"] * pos["averagePrice"]) + usdc_amount
                    pos["amount"] = total_amount
                    pos["averagePrice"] = total_cost / total_amount if total_amount else pos["averagePrice"]
                    pos["currentPrice"] = price
                    pos["value"] = total_amount * price
                else:
                    portfolio["positions"].append({
                        "id": f"pos_{int(datetime.utcnow().timestamp()*1000)}",
                        "asset": asset_id,
                        "symbol": row["symbol"],
                        "amount": float(amount),
                        "averagePrice": float(price),
                        "currentPrice": float(price),
                        "value": float(amount * price),
                        "profitLoss": 0.0,
                        "profitLossPercent": 0.0,
                        "openedAt": datetime.utcnow(),
                    })

        # Sell
        else:
            pos = next((p for p in portfolio["positions"] if p["asset"] == asset_id), None)
            if not pos or pos["amount"] < amount:
                st.warning("Insufficient position size to sell.")
            else:
                portfolio["usdcBalance"] += usdc_amount
                if pos["amount"] == amount:
                    portfolio["positions"] = [p for p in portfolio["positions"] if p["asset"] != asset_id]
                else:
                    pos["amount"] -= amount
                    pos["value"] = pos["amount"] * price
                    pos["currentPrice"] = price

        # Update totals
        for p in portfolio["positions"]:
            p["currentPrice"] = float(next((x["currentPrice"] for x in market if x["id"] == p["asset"]), p["currentPrice"]))
            p["value"] = p["amount"] * p["currentPrice"]
            pnl = p["value"] - (p["amount"] * p["averagePrice"])
            p["profitLoss"] = pnl
            p["profitLossPercent"] = (pnl / (p["amount"] * p["averagePrice"]) * 100) if (p["amount"] * p["averagePrice"]) else 0.0

        positions_value = sum(p["value"] for p in portfolio["positions"])
        portfolio["totalValue"] = portfolio["usdcBalance"] + positions_value
        portfolio["lastUpdated"] = datetime.utcnow()

        # Trade record
        portfolio["trades"].append({
            "id": f"trade_{int(datetime.utcnow().timestamp()*1000)}",
            "agentId": agent["id"],
            "asset": asset_id,
            "symbol": row["symbol"],
            "type": trade_type,
            "amount": float(amount),
            "price": float(price),
            "usdcAmount": float(usdc_amount),
            "timestamp": datetime.utcnow(),
            "reason": reason or None,
            "approved": bool(approved),
            "executedAt": datetime.utcnow(),
        })
        agent["lastTradeAt"] = datetime.utcnow()

        # Performance (demo): profit relative to initial paper balance for that agent (approx)
        initial = 2000.0
        agent["performance"]["totalProfit"] = float(portfolio["totalValue"] - initial)
        agent["performance"]["totalProfitPercent"] = float((agent["performance"]["totalProfit"] / initial) * 100 if initial else 0.0)
        agent["performance"]["totalTrades"] = int(agent["performance"]["totalTrades"] + 1)

        st.success("Trade executed (paper).")
        from crowdlike.state import recompute_metrics
        recompute_metrics()
        st.rerun()

card_end()

# Show agent portfolio snapshot
card_start("Selected Agent Portfolio Snapshot")
st.write("USDC balance:", fmt_usd(agent["portfolio"]["usdcBalance"]))
st.write("Total value:", fmt_usd(agent["portfolio"]["totalValue"]))

if agent["portfolio"]["positions"]:
    pdf = pd.DataFrame(agent["portfolio"]["positions"])
    st.dataframe(pdf[["symbol","amount","averagePrice","currentPrice","value","profitLossPercent"]], use_container_width=True, hide_index=True)
else:
    st.caption("No open positions.")

if agent["portfolio"]["trades"]:
    tdf = pd.DataFrame(agent["portfolio"]["trades"][-10:]).copy()
    tdf["timestamp"] = tdf["timestamp"].astype(str)
    st.dataframe(tdf[["timestamp","type","symbol","amount","price","usdcAmount","approved"]], use_container_width=True, hide_index=True)
else:
    st.caption("No trades yet.")
card_end()
