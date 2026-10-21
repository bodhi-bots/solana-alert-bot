"""Minimal Telegram client (long polling, no framework). Commands: /start /status /open /history"""
import requests
import config

API = f"https://api.telegram.org/bot{config.TELEGRAM_TOKEN}"

def enabled():
    return bool(config.TELEGRAM_TOKEN and config.TELEGRAM_CHAT_ID)

def send(text, dry_run=False):
    if dry_run or not enabled():
        print("[telegram]", text.replace("\n", " | "))
        return
    try:
        requests.post(API + "/sendMessage", json={"chat_id": config.TELEGRAM_CHAT_ID, "text": text, "disable_web_page_preview": True}, timeout=15)
    except requests.RequestException as e:
        print("telegram error:", e)

_offset = 0

def poll_commands():
    """Returns new command strings sent by the configured chat."""
    global _offset
    if not enabled():
        return []
    try:
        r = requests.get(API + "/getUpdates", params={"offset": _offset, "timeout": 0}, timeout=15).json()
    except requests.RequestException:
        return []
    cmds = []
    for u in r.get("result", []):
        _offset = u["update_id"] + 1
        msg = u.get("message") or {}
        if str(msg.get("chat", {}).get("id")) == str(config.TELEGRAM_CHAT_ID) and msg.get("text", "").startswith("/"):
            cmds.append(msg["text"].split()[0].lower())
    return cmds
