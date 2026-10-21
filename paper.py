"""Paper trading: no real money. Stop-loss + trailing stop, results logged to CSV."""
import csv, json, os, time
import config

STATE = os.path.join(config.DATA_DIR, "paper_state.json")
LOG = os.path.join(config.DATA_DIR, "paper_trades.csv")

class Paper:
    def __init__(self, stake=None, trail_pct=None, stop_pct=None):
        self.stake = stake or config.PAPER_STAKE_USD
        self.trail = (trail_pct or config.TRAIL_PCT) / 100
        self.stop = (stop_pct or config.STOP_LOSS_PCT) / 100
        self.open = json.load(open(STATE)) if os.path.exists(STATE) else {}

    def save(self):
        json.dump(self.open, open(STATE, "w"), indent=1)

    def buy(self, address, symbol, price):
        if address in self.open or not price:
            return False
        self.open[address] = dict(symbol=symbol, entry=price, peak=price, t=time.time())
        self.save()
        return True

    def update(self, address, price):
        """Returns a closed-trade dict if an exit rule fired, else None."""
        p = self.open.get(address)
        if not p or not price:
            return None
        p["peak"] = max(p["peak"], price)
        reason = None
        if price <= p["entry"] * (1 - self.stop):
            reason = "stop-loss"
        elif p["peak"] > p["entry"] and price <= p["peak"] * (1 - self.trail):
            reason = "trailing stop"
        if not reason:
            self.save()
            return None
        trade = dict(symbol=p["symbol"], address=address, entry=p["entry"], exit=price, peak=p["peak"],
                     pnl_pct=round((price / p["entry"] - 1) * 100, 2), pnl_usd=round(self.stake * (price / p["entry"] - 1), 2),
                     minutes=round((time.time() - p["t"]) / 60, 1), reason=reason)
        del self.open[address]
        self.save()
        new = not os.path.exists(LOG)
        with open(LOG, "a", newline="") as f:
            w = csv.DictWriter(f, fieldnames=list(trade))
            if new:
                w.writeheader()
            w.writerow(trade)
        return trade

def history():
    if not os.path.exists(LOG):
        return []
    return list(csv.DictReader(open(LOG)))
