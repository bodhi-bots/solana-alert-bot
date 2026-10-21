import os, sys, tempfile
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
os.environ["DATA_DIR"] = tempfile.mkdtemp()
import paper

def test_trailing_stop_locks_profit():
    b = paper.Paper(stake=100, trail_pct=25, stop_pct=15)
    b.buy("X", "TEST", 1.0)
    assert b.update("X", 2.0) is None          # new peak, no exit
    t = b.update("X", 1.49)                     # 25.5% below peak -> trailing stop
    assert t["reason"] == "trailing stop" and t["pnl_pct"] == 49.0

def test_stop_loss():
    b = paper.Paper(stake=100, trail_pct=25, stop_pct=15)
    b.buy("Y", "TEST", 1.0)
    t = b.update("Y", 0.84)
    assert t["reason"] == "stop-loss" and t["pnl_usd"] == -16.0

if __name__ == "__main__":
    test_trailing_stop_locks_profit(); test_stop_loss(); print("all tests passed")
