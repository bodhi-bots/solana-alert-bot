"""Solana alert + paper-trading bot. Run:  python main.py            (uses .env, sends to Telegram)
                                             python main.py --dry-run  (prints alerts, never needs a token)
                                             python main.py --once     (one scan, then exit)"""
import sys, time
import config, dexscreener, scanner, telegram_bot as tg, dashboard
from paper import Paper, history

def scan_once(book, dry, seen):
    tokens = dexscreener.latest_profiles()
    pairs = dexscreener.pairs_for_tokens(tokens)
    for addr, pair in pairs.items():
        if addr in seen:
            continue
        seen.add(addr)
        ok, reasons, s = scanner.evaluate(pair)
        if ok:
            tg.send(scanner.format_alert(s, reasons), dry)
            if book.buy(addr, s["symbol"], s["price"]):
                tg.send(f"📝 Paper buy {s['symbol']} at ${s['price']:.8g}", dry)
    # update open paper positions
    if book.open:
        live = dexscreener.pairs_for_tokens(list(book.open))
        for addr, pair in live.items():
            t = book.update(addr, float(pair.get("priceUsd") or 0))
            if t:
                tg.send(f"✅ Paper sell {t['symbol']}: {t['pnl_pct']:+.1f}% (${t['pnl_usd']:+.2f}) after {t['minutes']} min — {t['reason']}", dry)
    return len(tokens), len(pairs)

def handle(cmd, book, dry):
    if cmd == "/start":
        tg.send("Bot running. Commands: /status /open /history", dry)
    elif cmd == "/status":
        h = history(); tot = sum(float(r["pnl_usd"]) for r in h)
        tg.send(f"Open: {len(book.open)} · closed: {len(h)} · paper P&L ${tot:+.2f}", dry)
    elif cmd == "/open":
        tg.send("\n".join(f"{p['symbol']} entry ${p['entry']:.8g} peak ${p['peak']:.8g}" for p in book.open.values()) or "No open positions", dry)
    elif cmd == "/history":
        tg.send("Report written to " + dashboard.build(), dry)

def main():
    dry = "--dry-run" in sys.argv or not tg.enabled()
    once = "--once" in sys.argv
    book, seen = Paper(), set()
    print(f"started ({'dry-run' if dry else 'telegram'}) — paper trading only, no real orders")
    while True:
        try:
            n_tok, n_pairs = scan_once(book, dry, seen)
            print(f"scan: {n_tok} new profiles, {n_pairs} pairs, {len(book.open)} open paper positions")
            for cmd in tg.poll_commands():
                handle(cmd, book, dry)
            dashboard.build()
        except Exception as e:
            print("loop error:", e)
        if once:
            break
        time.sleep(config.SCAN_INTERVAL_SEC)

if __name__ == "__main__":
    main()
