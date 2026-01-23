from __future__ import annotations

from typing import Any, Dict

import pandas as pd
import streamlit as st

from .style import pill


def fmt_usd(x: float) -> str:
    try:
        return f"${x:,.2f}"
    except Exception:
        return "$0.00"


def status_chip(status: str) -> str:
    cls = "cl-chip-active" if status == "active" else ("cl-chip-paused" if status == "paused" else "cl-chip-exited")
    label = status.capitalize()
    return f"<span class='cl-chip {cls}'>{label}</span>"


def strategy_pill(strategy_type: str) -> str:
    return pill(f"Strategy: {strategy_type}")


def risk_pill(risk: int) -> str:
    return pill(f"Risk: {int(risk)}/100")


def df_from_leaderboard(entries: list[dict]) -> pd.DataFrame:
    if not entries:
        return pd.DataFrame(columns=["rank","botId","agentName","score","profit","profitPercent","streaks","totalTrades","winRate"])
    df = pd.DataFrame(entries)
    cols = ["rank","botId","agentName","score","profit","profitPercent","streaks","totalTrades","winRate"]
    df = df[[c for c in cols if c in df.columns]]
    return df
