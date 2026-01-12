# Crowdlike v0.31 (UX-first multi-agent demo)


## New in 0.31

- Always-on sidebar: **active agent switcher**, **readiness checklist**, and **quick actions** (Checkout / Coach).
- Safer UX: **confirmations** for destructive actions (panic sell, manual exit, delete agent).
- Navigation upgrade: **Coach** is now first-class in the top nav.
- Comparison dashboard ranks agents by **profit** and **% return** across daily/weekly/monthly/yearly.
- Safety UX: **panic sell**, **fraud alert**, and **auto drawdown exit** (demo converts holdings to “cash”).
- Pricing UX: pay-per-day estimator with exponential scaling by agents/risk/autonomy.
- Market + Checkout now run under the **active agent** (purchases are still mirrored into user history for convenience).

Crowdlike is a Streamlit demo exploring **agentic commerce with safety rails** on **Arc (EVM L1)** using **USDC testnet**.
It focuses on a clear “money moment” for hackathon judging:

**Profile → Market → Checkout → Verify receipt**

## Quickstart

### 1) Install
```bash
python -m venv .venv
source .venv/Scripts/activate   # Git Bash on Windows
pip install -U pip
pip install -r requirements.txt
```

### 2) Run
```bash
streamlit run app.py
```

## Demo flow (recommended for judges)

1. **Profile**: set your wallet address (MetaMask/Rabby works).
2. **Market**: try the practice simulator, then pick an offer.
3. **Checkout**: generate a payment command (or use your wallet if you adapt it).
4. **Verify**: paste the transaction hash and verify the USDC transfer on-chain.

## Safety rails (policy)

In **Profile → Autonomy & Limits**, you can set:
- **Max per transaction (USDC)**
- **Daily cap (USDC)**
- **Cooldown (seconds)**

These are enforced before generating payment actions.

## Demo mode (recommended)

By default, `DEMO_MODE` is treated as **on** and locks network settings to Arc testnet:
- RPC: https://rpc.testnet.arc.network
- Explorer: https://testnet.arcscan.app
- USDC interface: 0x3600000000000000000000000000000000000000
- Decimals: 6

If you want to customize networks locally, set `DEMO_MODE=false` in Streamlit secrets.

## Notes

- This demo stores profiles **locally** in `.crowdlike_data/` (created at runtime). Do not ship that directory in releases.
- Never commit `.env` or private keys. Use Streamlit secrets or local untracked environment variables.

## Release

To create a clean zip:
```bash
./scripts/build_release.sh v1.1.0
```

MIT licensed — see `LICENSE`.
