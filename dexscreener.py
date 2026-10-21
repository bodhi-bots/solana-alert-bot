"""Small DexScreener client (public API, no key). Docs: https://docs.dexscreener.com/api/reference"""
import time
import requests

BASE = "https://api.dexscreener.com"
_session = requests.Session()
_session.headers["User-Agent"] = "solana-alert-bot/1.0"

def _get(path, retries=3):
    for i in range(retries):
        try:
            r = _session.get(BASE + path, timeout=15)
            if r.status_code == 429:
                time.sleep(2 + 2 * i)
                continue
            r.raise_for_status()
            return r.json()
        except requests.RequestException:
            time.sleep(1 + i)
    return None

def latest_profiles(chain="solana"):
    """Newest tokens that got a DexScreener profile (fresh launches)."""
    data = _get("/token-profiles/latest/v1") or []
    return [d["tokenAddress"] for d in data if d.get("chainId") == chain]

def pairs_for_tokens(addresses, chain="solana"):
    """Best pair (highest liquidity) per token, up to 30 tokens per call."""
    best = {}
    for i in range(0, len(addresses), 30):
        data = _get(f"/tokens/v1/{chain}/" + ",".join(addresses[i:i + 30])) or []
        for p in data:
            t = p["baseToken"]["address"]
            liq = (p.get("liquidity") or {}).get("usd") or 0
            if t not in best or liq > ((best[t].get("liquidity") or {}).get("usd") or 0):
                best[t] = p
    return best

def price_usd(address, chain="solana"):
    p = pairs_for_tokens([address], chain).get(address)
    return float(p["priceUsd"]) if p and p.get("priceUsd") else None
