"""Load Telegram credentials from env vars or a local config module."""

from __future__ import annotations

import os
from typing import Iterable

DEFAULT_POLL_TIMEOUT_SEC = 25


def _parse_allowed_user_ids(raw: str | None) -> set[int]:
    if not raw:
        return set()
    ids: set[int] = set()
    for part in raw.replace(";", ",").split(","):
        part = part.strip()
        if part:
            ids.add(int(part))
    return ids


def load_settings() -> dict[str, object]:
    token = os.environ.get("TELEGRAM_BOT_TOKEN", "").strip()
    allowed_raw = os.environ.get("TELEGRAM_ALLOWED_USER_IDS", "").strip()

    try:
        from telegram_config import TELEGRAM_ALLOWED_USER_IDS as file_ids
        from telegram_config import TELEGRAM_BOT_TOKEN as file_token

        if not token:
            token = str(file_token).strip()
        if not allowed_raw and file_ids:
            allowed_raw = ",".join(str(user_id) for user_id in file_ids)
    except ImportError:
        pass

    return {
        "bot_token": token,
        "allowed_user_ids": _parse_allowed_user_ids(allowed_raw),
        "poll_timeout_sec": DEFAULT_POLL_TIMEOUT_SEC,
    }


def is_user_allowed(user_id: int, allowed_user_ids: Iterable[int]) -> bool:
    allowed = set(allowed_user_ids)
    return not allowed or user_id in allowed
