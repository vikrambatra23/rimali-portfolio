RIMALI PORTFOLIO PWA — Setup guide (no coding required)
========================================================

This folder is a complete portfolio app. You don't need to install anything.
Total time to set up: ~10 minutes.

The app shows:
  • Live portfolio value (refreshed every hour from Google Finance)
  • Per-stock LTP and profit/loss
  • Full trade history with biggest winners/losers

There are two things to do:
  1. Set up the Google Sheet that feeds live prices.
  2. Put this folder online and install it on Rimali's phone.


STEP 1 — Set up the live-prices Google Sheet
---------------------------------------------

1. Go to https://sheets.new — this creates a fresh blank Google Sheet.

2. Type these in cell A1 and B1:
        A1:   symbol
        B1:   price

3. Starting from row 2 of column A, paste these tickers, one per row:
        AUROPHARMA
        CHENNPETRO
        CIEINDIA
        DATAPATTNS
        GLAXO
        HEG
        KTKBANK
        LIQUIDBEES
        MID150BEES
        NIFTYBEES
        OIL
        ONGC
        SBIN
        SOUTHBANK
        UJJIVANSFB

4. In cell B2, paste exactly:
        =GOOGLEFINANCE("NSE:"&A2,"price")

   Then click B2, hover over the small blue square at the bottom-right
   of the cell, and drag it down to row 16. All the prices will fill in.

5. Top menu: File → Share → Publish to web.

6. In the dialog:
        - "Link" tab (default)
        - First dropdown: choose your sheet (e.g. "Sheet1")
        - Second dropdown: change "Web page" to "Comma-separated values (.csv)"
        - Click Publish, then OK.

7. Copy the URL it shows. It looks like:
        https://docs.google.com/spreadsheets/d/e/.../pub?output=csv

   Save this URL — you'll paste it into the app later.


STEP 2 — Put the app online (free, takes 60 seconds)
-----------------------------------------------------

The easiest free host is Netlify Drop. No signup needed for a one-time deploy.

1. Open https://app.netlify.com/drop in your browser.

2. Drag this whole folder (rimali-pf-static) onto the page.
   Wait ~10 seconds while it uploads.

3. Netlify shows a URL like:  https://abc-xyz-123.netlify.app
   That's the app's permanent web address. Bookmark it.

NOTE: If you want a nicer URL or to keep it private, sign up for a free
Netlify account during step 2 — it'll let you rename the site
(e.g. rimali-pf.netlify.app) and add a password.


STEP 3 — Install on Rimali's phone
-----------------------------------

1. Open the Netlify URL in Chrome on her Android phone (or Safari on iPhone).

2. Tap the ⚙ tab at the bottom.

3. Paste the Google Sheet CSV URL from Step 1, tap Save.

4. Holdings tab will now show live prices.

5. Install as an app:
        Android Chrome:  three-dot menu → "Install app" → Add
        iPhone Safari:   Share button → "Add to Home Screen"

   The app icon appears on her home screen and opens fullscreen, just
   like a regular app. Prices auto-refresh every hour while it's open.


UPDATING HOLDINGS WHEN SHE BUYS/SELLS
--------------------------------------

Open index.html in a text editor (Notepad works). Near the top you'll see:

    const HOLDINGS = [
      { symbol: "AUROPHARMA",  qty: 235,   avgCost: 1383.90 },
      ...
    ];

Edit the qty / avgCost numbers, save the file, and re-deploy:
go back to https://app.netlify.com/drop and drag the folder again
(or use your Netlify dashboard if you signed up).


ADDING NEW TRADEBOOK CSVS
--------------------------

When she downloads a new tradebook from Zerodha:
  1. Drop the new .csv into the tradebooks/ subfolder.
  2. Open index.html in a text editor, find the TRADEBOOK_FILES list
     near the top, and add a line for the new file.
  3. Re-deploy as above.


THINGS TO KNOW
--------------

• If a holding shows "—" instead of a price, the symbol in the Google
  Sheet (column A) doesn't match. Check the spelling — Google Finance
  is case-sensitive for some tickers. Try BSE: prefix if NSE: doesn't
  resolve (e.g. BSE:GLAXO instead of NSE:GLAXO).

• The "EVENT" tag next to SBIN / SOUTHBANK / UJJIVANSFB is just a label
  copied from her Kite holdings — it means those shares came from a
  corporate event (dividend, bonus, split). The price feed uses the
  same ticker.

• The app saves the price-sheet URL in the phone's local storage, so
  you only enter it once.

• If you ever want to see exact files: Trades tab → "All trades"
  shows every buy/sell since 2023.
