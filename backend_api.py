"""
Minimal FastAPI backend intended to be used by the React app *without changing React code*.

You can point the frontend's VITE_COINGECKO_API_URL to this server, and it will proxy the
small subset of CoinGecko endpoints used by the current UI:

- GET /coins/markets
- GET /simple/price
- GET /search
- GET /search/trending

This enables:
- consistent demo behavior
- optional caching
- future extension (agents, trades, Qubic/Arc integration, etc.)
"""

from __future__ import annotations

import os
import time
from typing import Any, Dict, Optional

import requests
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

COINGECKO_BASE = os.environ.get("CROWDLIKE_COINGECKO_BASE", "https://api.coingecko.com/api/v3")
CACHE_TTL_SECONDS = int(os.environ.get("CROWDLIKE_CACHE_TTL", "30"))
REQUEST_TIMEOUT = float(os.environ.get("CROWDLIKE_REQUEST_TIMEOUT", "10"))

app = FastAPI(title="Crowdlike Backend API", version="0.1.0")

# Broad CORS to keep local dev friction low.
# Tighten this later for production.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

_cache: Dict[str, tuple[float, Any]] = {}


def _cache_get(key: str) -> Optional[Any]:
    item = _cache.get(key)
    if not item:
        return None
    ts, data = item
    if time.time() - ts <= CACHE_TTL_SECONDS:
        return data
    return None


def _cache_set(key: str, data: Any) -> None:
    _cache[key] = (time.time(), data)


def _proxy(path: str, params: Dict[str, Any]) -> Any:
    key = f"{path}?{sorted(params.items())}"
    cached = _cache_get(key)
    if cached is not None:
        return cached

    url = f"{COINGECKO_BASE}{path}"
    resp = requests.get(url, params=params, timeout=REQUEST_TIMEOUT)
    resp.raise_for_status()
    data = resp.json()

    _cache_set(key, data)
    return data


@app.get("/health")
def health():
    return {"ok": True, "service": "crowdlike-backend"}


@app.get("/coins/markets")
def coins_markets(
    vs_currency: str = Query("usd"),
    ids: str = Query(..., description="Comma-separated coin ids (e.g. bitcoin,ethereum)"),
    order: str = Query("market_cap_desc"),
    sparkline: str = Query("false"),
    price_change_percentage: str = Query("24h"),
):
    params = {
        "vs_currency": vs_currency,
        "ids": ids,
        "order": order,
        "sparkline": sparkline,
        "price_change_percentage": price_change_percentage,
    }

    try:
        data = _proxy("/coins/markets", params)
        return JSONResponse(content=data)
    except Exception:
        # Minimal fallback in case CoinGecko is unavailable.
        # Shape matches CoinGecko response (list of coins).
        fallback = []
        for coin_id in ids.split(","):
            fallback.append(
                {
                    "id": coin_id,
                    "symbol": coin_id[:3],
                    "name": coin_id.capitalize(),
                    "current_price": 1,
                    "price_change_24h": 0,
                    "price_change_percentage_24h": 0,
                    "market_cap": 0,
                    "total_volume": 0,
                    "high_24h": 1,
                    "low_24h": 1,
                    "image": None,
                }
            )
        return JSONResponse(content=fallback)


@app.get("/simple/price")
def simple_price(
    ids: str = Query(..., description="Coin id (or comma-separated ids)"),
    vs_currencies: str = Query("usd"),
):
    params = {"ids": ids, "vs_currencies": vs_currencies}
    try:
        data = _proxy("/simple/price", params)
        return JSONResponse(content=data)
    except Exception:
        # CoinGecko returns an object: { "<id>": { "<vs>": number } }
        out: Dict[str, Dict[str, float]] = {}
        for coin_id in ids.split(","):
            out[coin_id] = {vs: 1.0 for vs in vs_currencies.split(",")}
        return JSONResponse(content=out)


@app.get("/search")
def search(query: str = Query(...)):
    params = {"query": query}
    try:
        data = _proxy("/search", params)
        return JSONResponse(content=data)
    except Exception:
        # Minimal shape: { coins: [...] }
        return JSONResponse(
            content={
                "coins": [
                    {"id": "bitcoin", "name": "Bitcoin", "symbol": "btc", "thumb": None, "large": None},
                    {"id": "ethereum", "name": "Ethereum", "symbol": "eth", "thumb": None, "large": None},
                ]
            }
        )


@app.get("/search/trending")
def trending():
    try:
        data = _proxy("/search/trending", {})
        return JSONResponse(content=data)
    except Exception:
        # Minimal shape: { coins: [ { item: { id, ... } } ] }
        return JSONResponse(
            content={
                "coins": [
                    {"item": {"id": "bitcoin", "name": "Bitcoin", "symbol": "BTC", "thumb": None, "large": None}},
                    {"item": {"id": "ethereum", "name": "Ethereum", "symbol": "ETH", "thumb": None, "large": None}},
                    {"item": {"id": "solana", "name": "Solana", "symbol": "SOL", "thumb": None, "large": None}},
                ]
            }
        )
