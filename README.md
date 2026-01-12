# Crowdlike v0.50 (Vision-aligned demo)

Crowdlike is a Streamlit multi-agent demo exploring **agentic payments** and **crowd-influenced autonomy** on Arc (USDC-centric). This release focuses on the **Master Context** vision: safety-first autonomy, crowd deviation constraints, copy mechanics, and trustless logging.

## What’s new in 0.50 (major)

- **Leaderboards (Daily/Weekly/Monthly/Yearly)** using anonymous **Bot IDs**.
  - Profit is **rounded to 2 decimals before scoring**.
  - Score formula: **score = (profit * 100) + streaks**.
- **Crowd deviation constraint (percentile-based)**
  - Metrics: **riskness**, **trades/day**, **position size (% portfolio per trade)**.
  - Deviation% = average(|percentile - 50|) across metrics.
  - If deviation exceeds your configured max, **auto execution is blocked** and approvals are required.
- **Copy modes (crowd learning)**
  - `mirror_trades`, `copy_settings`, `copy_strategy` proposals can be generated and approved.
- **Pricing model updated to spec**
  - `price = (agentCount^2) * (risk / 100)` per day.
- **Safety exits expanded**
  - Configurable **max daily loss (USDC)** + **max drawdown (%)**, plus fraud/anomaly and panic.
- **Trustless AI audit log (bot/admin-only)**
  - Proposals and approvals are logged for transparency.

## Run locally

### 1) Create venv + install deps
```bash
python -m venv .venv
source .venv/Scripts/activate
pip install -r requirements.txt
```

### 2) Run Streamlit
From the repo root (same folder as `app.py`):
```bash
streamlit run app.py
```

## Notes

- This is a demo: trades and payments are mocked or practice-mode unless you wire a real Arc/Circle flow.
- Keep secrets out of git. If you need them, use `.streamlit/secrets.toml` locally.
