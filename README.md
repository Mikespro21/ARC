# Crowdlike v0.2 (Arc / USDC testnet demo)


## New in 0.2
- Fixed startup crash when no `secrets.toml` is present.
- Added missing pages: **Shop**, **Quests**, **Social** (Home buttons now work).
- Rebuilt **Testnet checkout** flow (Configure → Pay → Verify) and fixed the `treasury` NameError/indent bug.
- Added **Crowd Score** that gently boosts payment limits (±20%) while staying within safety rails.

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
