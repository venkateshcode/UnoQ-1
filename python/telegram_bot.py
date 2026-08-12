"""Telegram long-polling bot that forwards prompts to the UNO Q MCU."""

from __future__ import annotations

import json
import urllib.error
import urllib.parse
import urllib.request
from typing import Any

from config import is_user_allowed, load_settings

class TelegramClient:
    def __init__(self, token: str, poll_timeout_sec: int = 25) -> None:
        self.api_base = f"https://api.telegram.org/bot{token}"
        self.poll_timeout_sec = poll_timeout_sec
        self.offset: int | None = None

    def _request(self, method: str, payload: dict[str, Any] | None = None) -> dict[str, Any]:
        url = f"{self.api_base}/{method}"
        data = None
        headers: dict[str, str] = {}
        if payload is not None:
            data = json.dumps(payload).encode("utf-8")
            headers["Content-Type"] = "application/json"
        request = urllib.request.Request(url, data=data, headers=headers, method="POST" if data else "GET")
        with urllib.request.urlopen(request, timeout=self.poll_timeout_sec + 10) as response:
            body = json.loads(response.read().decode("utf-8"))
        if not body.get("ok"):
            raise RuntimeError(f"Telegram API error for {method}: {body}")
        return body

    def get_updates(self) -> list[dict[str, Any]]:
        payload: dict[str, Any] = {
            "timeout": self.poll_timeout_sec,
            "allowed_updates": ["message"],
        }
        if self.offset is not None:
            payload["offset"] = self.offset
        result = self._request("getUpdates", payload)
        return result.get("result", [])

    def send_message(self, chat_id: int, text: str) -> None:
        self._request(
            "sendMessage",
            {
                "chat_id": chat_id,
                "text": text[:4096],
            },
        )


class TelegramPromptBot:
    HELP_TEXT = (
        "UnoQ-1 Telegram bridge\n\n"
        "Send any text to forward it to the UNO Q MCU.\n\n"
        "Commands:\n"
        "/help - show this message\n"
        "/status - MCU status\n"
        "/led - toggle the built-in LED"
    )

    def __init__(self, bridge: Any, client: TelegramClient, allowed_user_ids: set[int]) -> None:
        self.bridge = bridge
        self.client = client
        self.allowed_user_ids = allowed_user_ids

    def _call_mcu(self, method: str, arg: str = "") -> str:
        try:
            result = self.bridge.call(method, arg)
            return str(result)
        except Exception as exc:  # noqa: BLE001 - surface MCU/bridge errors to Telegram
            return f"MCU error: {exc}"

    def _handle_text(self, chat_id: int, user_id: int, text: str) -> None:
        if not is_user_allowed(user_id, self.allowed_user_ids):
            self.client.send_message(chat_id, "Unauthorized user.")
            return

        normalized = text.strip()
        if not normalized:
            return

        if normalized.startswith("/"):
            command = normalized.split()[0].split("@")[0].lower()
            if command == "/help":
                self.client.send_message(chat_id, self.HELP_TEXT)
                return
            if command == "/status":
                self.client.send_message(chat_id, self._call_mcu("get_status"))
                return
            if command == "/led":
                state = self._call_mcu("toggle_led")
                self.client.send_message(chat_id, f"LED is now {state}")
                return
            self.client.send_message(chat_id, "Unknown command. Send /help.")
            return

        reply = self._call_mcu("process_prompt", normalized)
        self.client.send_message(chat_id, reply)

    def poll_once(self) -> None:
        try:
            updates = self.client.get_updates()
        except urllib.error.URLError as exc:
            print(f"Telegram poll failed: {exc}")
            return

        for update in updates:
            update_id = update.get("update_id")
            if isinstance(update_id, int):
                self.offset = update_id + 1

            message = update.get("message") or {}
            chat = message.get("chat") or {}
            chat_id = chat.get("id")
            user = message.get("from") or {}
            user_id = user.get("id")
            text = message.get("text")

            if not isinstance(chat_id, int) or not isinstance(user_id, int) or not isinstance(text, str):
                continue

            self._handle_text(chat_id, user_id, text)


def create_bot(bridge: Any) -> TelegramPromptBot | None:
    settings = load_settings()
    token = str(settings["bot_token"])
    if not token:
        print(
            "TELEGRAM_BOT_TOKEN is not set. "
            "Copy python/telegram_config.example.py to python/telegram_config.py "
            "or export TELEGRAM_BOT_TOKEN."
        )
        return None

    allowed_user_ids = settings["allowed_user_ids"]
    if isinstance(allowed_user_ids, set):
        allowed = allowed_user_ids
    else:
        allowed = set(allowed_user_ids)

    client = TelegramClient(token, int(settings["poll_timeout_sec"]))
    bot = TelegramPromptBot(bridge, client, allowed)
    return bot
