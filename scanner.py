"""Turns raw DexScreener pairs into alerts using simple, explainable filters."""
import time
import config

def pair_age_min(pair):
    created = pair.get("pairCreatedAt")
    return (time.time() * 1000 - created) / 60000 if created else None

def evaluate(pair):
    """Returns (passed: bool, reasons: list[str], summary: dict)."""
    liq = (pair.get("liquidity") or {}).get("usd") or 0
    tx5 = (pair.get("txns") or {}).get("m5") or {}
    buys, sells = tx5.get("buys", 0), tx5.get("sells", 0)
    ratio = buys / max(sells, 1)
    vol5 = (pair.get("volume") or {}).get("m5") or 0
    age = pair_age_min(pair)
    checks = [
        (liq >= config.MIN_LIQUIDITY_USD, f"liquidity ${liq:,.0f}"),
        (age is not None and age <= config.MAX_PAIR_AGE_MIN, f"age {age:.0f} min" if age is not None else "age unknown"),
        (ratio >= config.MIN_BUY_SELL_RATIO, f"buys/sells 5m {buys}/{sells}"),
        (vol5 >= config.MIN_VOLUME_5M_USD, f"volume 5m ${vol5:,.0f}"),
    ]
    passed = all(ok for ok, _ in checks)
    summary = dict(symbol=pair["baseToken"]["symbol"], address=pair["baseToken"]["address"], price=float(pair.get("priceUsd") or 0),
                   mcap=pair.get("marketCap") or pair.get("fdv"), liquidity=liq, url=pair.get("url"))
    return passed, [("✅ " if ok else "❌ ") + txt for ok, txt in checks], summary

def format_alert(summary, reasons):
    mc = summary["mcap"]
    return (f"🚨 {summary['symbol']} passed the filters\n"
            f"MC: ${mc:,.0f}\n" if mc else f"🚨 {summary['symbol']} passed the filters\n") + "\n".join(reasons) + f"\n{summary['url']}"
