# Crowdlike (Option A — Pure Streamlit)

This is a full rebuild of the Crowdlike UI using **Streamlit only** (no React, no Node/npm).  
It is designed to run cleanly for “average users” and to deploy on **Streamlit Community Cloud** without extra build steps.

## Run locally

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate

pip install -r requirements.txt
streamlit run app.py
```

## Deploy to Streamlit Community Cloud

1. Push this repo to GitHub.
2. In Streamlit Cloud, create a new app pointing to:
   - **Repository:** your GitHub repo
   - **Branch:** main
   - **Main file path:** `app.py`

That’s it — no frontend build required.

## Notes

- Market data is fetched from CoinGecko when available. If the request fails (offline/rate-limited), the app falls back to demo prices.
- All trading is **paper trading** (simulation) for UI/flow purposes.
