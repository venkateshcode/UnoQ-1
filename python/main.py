"""UNO Q App Lab entrypoint: Telegram bot -> RouterBridge -> MCU sketch."""

from __future__ import annotations

from bridge_client import get_bridge, run_app
from telegram_bot import create_bot

bridge = get_bridge()
bridge.provide("linux_started", lambda: True)

_bot = create_bot(bridge)


def _demo_without_telegram() -> None:
    demo_prompt = "hello from cloud agent"
    print(f"Demo prompt -> MCU: {demo_prompt!r}")
    reply = bridge.call("process_prompt", demo_prompt)
    print(f"MCU reply: {reply}")
    status = bridge.call("get_status", "")
    print(f"MCU status: {status}")


def loop() -> None:
    if _bot is None:
        raise RuntimeError("Telegram bot is not configured")
    _bot.poll_once()


if __name__ == "__main__":
    if _bot is None:
        _demo_without_telegram()
    else:
        print("Telegram bot started. Send a message to your bot to reach the UNO Q MCU.")
        run_app(loop)
