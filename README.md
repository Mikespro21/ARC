# Crowdlike (Streamlit)

This repository is a **Streamlit port** that keeps the UI content and Tailwind class structure intact by rendering the app inside a single embedded HTML component.

## Run locally

```bash
pip install -r requirements.txt
streamlit run streamlit_app.py
```

## What this does

- Uses `streamlit.components.v1.html(...)` to render the Crowdlike UI.
- Loads Tailwind, Lucide, and canvas-confetti from CDNs so the original class names and icons behave as expected.
- Implements the same page switching, search, sidebar reveal/hide, and confetti behavior in vanilla JS (mirroring the original React logic).

## Tradeoffs

- This wrapper does **not** translate the UI into native Streamlit widgets; it preserves the markup/behavior by embedding HTML/JS.
- Because external CDNs are used, the app requires outbound internet access at runtime.
