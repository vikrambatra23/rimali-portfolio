"""Read all tradebook CSVs, dedupe by trade_id, filter to last 3 years from today,
and emit a compact JS array for inlining into Rimali_Portfolio.html.

Output format per trade: [date, symbol, type, qty, price]
  type: 'b' (buy) or 's' (sell)
"""

import csv
import json
import sys
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).parent
CSV_DIR = ROOT / "rimali-pf-static" / "tradebooks"
OUT = ROOT / "trades_inline.js"

# Include everything in the CSVs (no cutoff). FIFO needs early buys to match later sells.
CUTOFF = date(1900, 1, 1)

seen = set()
trades = []

for csv_path in sorted(CSV_DIR.glob("*.csv")):
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            tid = row.get("trade_id")
            if not tid or tid in seen:
                continue
            seen.add(tid)
            tt = row.get("trade_type")
            if tt not in ("buy", "sell"):
                continue
            try:
                d = date.fromisoformat(row["trade_date"])
            except Exception:
                continue
            if d < CUTOFF:
                continue
            qty = float(row["quantity"])
            px = float(row["price"])
            trades.append([row["trade_date"], row["symbol"], "b" if tt == "buy" else "s", qty, px])

trades.sort(key=lambda t: (t[0], t[1]))

print(f"Wrote {len(trades)} trades from {trades[0][0]} to {trades[-1][0]}", file=sys.stderr)

# Compact JSON one-per-line so the HTML stays diff-friendly
lines = ["[\n"]
for t in trades:
    # Round qty/price to keep file small
    qty = t[3]
    px = t[4]
    qty_s = f"{qty:.6f}".rstrip("0").rstrip(".")
    px_s = f"{px:.6f}".rstrip("0").rstrip(".")
    lines.append(f'  ["{t[0]}","{t[1]}","{t[2]}",{qty_s},{px_s}],\n')
lines.append("]")

OUT.write_text("const TRADES_INLINE = " + "".join(lines) + ";\n", encoding="utf-8")
print(f"Wrote {OUT}", file=sys.stderr)
