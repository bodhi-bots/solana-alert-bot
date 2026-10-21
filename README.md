# Solana Alert & Paper-Trading Bot

A lightweight Telegram bot that scans fresh Solana tokens on DexScreener, filters them with simple, explainable rules,
sends alerts to Telegram and **paper-trades** every alert with a stop-loss and trailing stop.
No real orders, no wallet, no private keys: it is built to *test* a strategy safely before any money is involved.

> Built by **bodhi-bots**. This is a public demo of the tooling I use in my own research bot
> (multi-strategy paper testing, live dashboards, automated daily reports). Need something like this? See the bottom of this page.

## Features
- 🔎 **Scanner**: newest Solana token profiles from DexScreener, best pair per token
- 🧮 **Explainable filters**: liquidity, pair age, buys/sells ratio, 5-minute volume (all configurable in `.env`)
- 🚨 **Telegram alerts** with the reasons each check passed or failed
- 📝 **Paper trading**: automatic paper buy on each alert, exit on stop-loss or trailing stop, results in CSV
- 📊 **HTML report**: `data/report.html` with all closed paper trades and total P&L
- 💬 **Commands**: `/start`, `/status`, `/open`, `/history`
- 🧪 **Dry-run mode**: runs without any Telegram token and prints everything to the console
- ✅ **Tests** for the exit logic (`python tests/test_paper.py`)

## Quick start
```bash
pip install -r requirements.txt
cp .env.example .env            # add your bot token (from @BotFather) and chat id
python main.py --dry-run --once # try one scan without Telegram
python main.py                  # run continuously
```

## How it works
```
DexScreener API ──> scanner.py (filters) ──> telegram_bot.py (alert)
                                  └──────> paper.py (paper buy / stop-loss / trailing stop) ──> data/paper_trades.csv
                                                                                    └──> dashboard.py ──> data/report.html
```

| File | What it does |
|---|---|
| `dexscreener.py` | Small API client with retries and rate-limit handling |
| `scanner.py` | Filters and alert formatting |
| `paper.py` | Paper positions, exit rules, trade log |
| `telegram_bot.py` | Sending messages and reading commands (long polling, no framework) |
| `dashboard.py` | Self-contained HTML report |
| `main.py` | Main loop |

## Lessons from my own research (why paper-test first)
In my private research bot I tested hundreds of thousands of strategy variants on real executable prices.
Strategies that looked great in a backtest often failed on newer data. Testing on paper, with real costs and a
separate control period, is the only honest way to know if something works. This demo follows the same idea.

## Disclaimer
Paper trading only. Not financial advice. Crypto, and especially new tokens, are extremely risky.

## Hire me
I build custom Telegram/Discord bots, alert systems, dashboards and paper-trading/backtesting tools.
Contact: GitHub **bodhi-bots**.

MIT License.
