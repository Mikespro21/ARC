from __future__ import annotations

import os
from datetime import datetime
from typing import Any, Dict, List, Optional

import requests
import streamlit as st


DEFAULT_IDS = ["bitcoin","ethereum","solana","cardano","polkadot","binancecoin","ripple","dogecoin"]


@st.cache_data(ttl=60, show_spinner=False)
def fetch_market_data(ids: List[str] | None = None, vs_currency: str = "usd") -> List[Dict[str, Any]]:
    ids = ids or DEFAULT_IDS
    # CoinGecko markets endpoint
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        "vs_currency": vs_currency,
        "ids": ",".join(ids),
        "order": "market_cap_desc",
        "per_page": len(ids),
        "page": 1,
        "sparkline": "false",
        "price_change_percentage": "24h",
    }
    r = requests.get(url, params=params, timeout=15)
    r.raise_for_status()
    data = r.json()

    out: List[Dict[str, Any]] = []
    for row in data:
        out.append({
            "id": row.get("id"),
            "symbol": (row.get("symbol") or "").upper(),
            "name": row.get("name"),
            "currentPrice": float(row.get("current_price") or 0.0),
            "priceChange24h": float(row.get("price_change_24h") or 0.0),
            "priceChangePercent24h": float(row.get("price_change_percentage_24h") or 0.0),
            "marketCap": float(row.get("market_cap") or 0.0),
            "volume24h": float(row.get("total_volume") or 0.0),
            "high24h": float(row.get("high_24h") or 0.0),
            "low24h": float(row.get("low_24h") or 0.0),
            "lastUpdated": datetime.utcnow(),
            "image": row.get("image"),
        })
    return out


def safe_market_data(ids: List[str] | None = None) -> List[Dict[str, Any]]:
    """Fetch market data with graceful fallback to demo values."""
    try:
        return fetch_market_data(ids=ids)
    except Exception:
        # Minimal demo fallback (stable, no external calls)
        demo = [
            {"id":"bitcoin","symbol":"BTC","name":"Bitcoin","currentPrice":45000.0,"priceChange24h":0.0,"priceChangePercent24h":0.0,"marketCap":0.0,"volume24h":0.0,"high24h":0.0,"low24h":0.0,"lastUpdated":datetime.utcnow(),"image":None},
            {"id":"ethereum","symbol":"ETH","name":"Ethereum","currentPrice":2500.0,"priceChange24h":0.0,"priceChangePercent24h":0.0,"marketCap":0.0,"volume24h":0.0,"high24h":0.0,"low24h":0.0,"lastUpdated":datetime.utcnow(),"image":None},
            {"id":"solana","symbol":"SOL","name":"Solana","currentPrice":100.0,"priceChange24h":0.0,"priceChangePercent24h":0.0,"marketCap":0.0,"volume24h":0.0,"high24h":0.0,"low24h":0.0,"lastUpdated":datetime.utcnow(),"image":None},
            {"id":"cardano","symbol":"ADA","name":"Cardano","currentPrice":0.5,"priceChange24h":0.0,"priceChangePercent24h":0.0,"marketCap":0.0,"volume24h":0.0,"high24h":0.0,"low24h":0.0,"lastUpdated":datetime.utcnow(),"image":None},
            {"id":"polkadot","symbol":"DOT","name":"Polkadot","currentPrice":7.0,"priceChange24h":0.0,"priceChangePercent24h":0.0,"marketCap":0.0,"volume24h":0.0,"high24h":0.0,"low24h":0.0,"lastUpdated":datetime.utcnow(),"image":None},
        ]
        return demo
