"""Writes a self-contained HTML report of the paper results (open data/report.html in a browser)."""
import html, os
import config, paper

def build():
    rows = paper.history()
    total = sum(float(r["pnl_usd"]) for r in rows)
    wins = sum(1 for r in rows if float(r["pnl_usd"]) > 0)
    body = "".join(f"<tr><td>{html.escape(r['symbol'])}</td><td>{r['pnl_pct']}%</td><td>${r['pnl_usd']}</td><td>{r['minutes']} min</td><td>{r['reason']}</td></tr>" for r in reversed(rows[-50:]))
    page = f"""<!doctype html><meta charset="utf-8"><title>Paper results</title>
<style>body{{font-family:system-ui;margin:24px;background:#111;color:#eee}}td,th{{padding:6px 10px;border-bottom:1px solid #333}}</style>
<h1>Paper trading results</h1><p>{len(rows)} closed trades · {wins} winners · total ${total:,.2f} (stake ${config.PAPER_STAKE_USD:.0f} per trade)</p>
<table><tr><th>Token</th><th>Result</th><th>USD</th><th>Held</th><th>Exit</th></tr>{body}</table>"""
    path = os.path.join(config.DATA_DIR, "report.html")
    open(path, "w", encoding="utf-8").write(page)
    return path
