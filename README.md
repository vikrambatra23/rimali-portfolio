# Rimali · Portfolio

Single-file PWA showing live holdings, closed-trade P&L, and portfolio XIRR.

## Files

- `index.html` — the dashboard
- `trades_inline.js` — 1,603 trades from 2023-03-20 to 2026-04-20
- `manifest.webmanifest`, `sw.js`, `icon.svg` — PWA shell
- `build_trades_inline.py` — regenerator (reads `rimali-pf-static/tradebooks/*.csv`)
- `streamlit_app.py` — optional Streamlit wrapper

## Run locally

```
python -m http.server 8000
```

Open `http://localhost:8000`. PIN is `0000`.

## Refresh trades after new activity

Drop new Zerodha CSVs into `rimali-pf-static/tradebooks/` and run:

```
python build_trades_inline.py
```

## Deploy as a PWA

GitHub Pages serves this repo's root as a PWA. After enabling Pages, install on your phone via the browser's "Add to Home Screen" / "Install app" option.

> Privacy: portfolio data is plain JS. Use a private repo + Cloudflare Pages if you don't want public visibility.
