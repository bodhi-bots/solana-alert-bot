"""Settings from .env (simple parser, no extra dependency)."""
import os

def _load_env(path=".env"):
    if not os.path.exists(path):
        return
    for line in open(path, encoding="utf-8"):
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            os.environ.setdefault(k.strip(), v.strip())

_load_env()

def _f(name, default):
    return float(os.environ.get(name, default))

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN", "")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", "")
MIN_LIQUIDITY_USD = _f("MIN_LIQUIDITY_USD", 20000)
MAX_PAIR_AGE_MIN = _f("MAX_PAIR_AGE_MIN", 120)
MIN_BUY_SELL_RATIO = _f("MIN_BUY_SELL_RATIO", 1.5)
MIN_VOLUME_5M_USD = _f("MIN_VOLUME_5M_USD", 5000)
PAPER_STAKE_USD = _f("PAPER_STAKE_USD", 100)
TRAIL_PCT = _f("TRAIL_PCT", 25)
STOP_LOSS_PCT = _f("STOP_LOSS_PCT", 15)
SCAN_INTERVAL_SEC = _f("SCAN_INTERVAL_SEC", 60)
DATA_DIR = os.environ.get("DATA_DIR", "data")
os.makedirs(DATA_DIR, exist_ok=True)
