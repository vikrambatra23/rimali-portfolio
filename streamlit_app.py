"""Streamlit wrapper for Rimali_Portfolio.html.

Streamlit embeds HTML in a sandboxed iframe, so the service worker / manifest
won't register on the parent page — PWA "Install app" won't work from here.
For real PWA install, host the static files (Rimali_Portfolio.html, trades_inline.js,
manifest.webmanifest, sw.js, icon.svg) on Netlify / GitHub Pages / Vercel instead.
"""

from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Rimali · Portfolio",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Strip Streamlit chrome so the dashboard fills the viewport
st.markdown(
    """
    <style>
      #MainMenu, footer, header {visibility: hidden;}
      .block-container { padding: 0 !important; max-width: 100% !important; }
      [data-testid="stAppViewContainer"] { background: #0a0e1a; }
      [data-testid="stHeader"] { display: none; }
    </style>
    """,
    unsafe_allow_html=True,
)

base = Path(__file__).parent
html = (base / "index.html").read_text(encoding="utf-8")
trades = (base / "trades_inline.js").read_text(encoding="utf-8")

# Inline the trades script — the iframe can't fetch sibling files
html = html.replace(
    '<script src="trades_inline.js"></script>',
    f"<script>\n{trades}\n</script>",
)
# Drop the manifest + SW registration since they're no-ops inside a Streamlit iframe
html = html.replace(
    '<link rel="manifest" href="manifest.webmanifest">',
    "",
)

components.html(html, height=1600, scrolling=True)
