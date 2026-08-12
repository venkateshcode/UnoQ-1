"""RouterBridge access with a mock fallback for Cloud Agent / offline dev."""

from __future__ import annotations

import time
from typing import Any, Callable

ON_BOARD = False
Bridge: Any = None
App: Any = None

try:
    from arduino.app_utils import App as _App
    from arduino.app_utils import Bridge as _Bridge

    App = _App
    Bridge = _Bridge
    ON_BOARD = True
except ImportError:
    pass


class MockBridge:
    """Simulates MCU responses when arduino.app_utils is unavailable."""

    _handlers: dict[str, Callable[..., Any]] = {}
    _led_on = False
    _last_prompt = ""

    @classmethod
    def provide(cls, name: str, handler: Callable[..., Any]) -> None:
        cls._handlers[name] = handler

    @classmethod
    def call(cls, name: str, *args: Any, timeout: int = 10) -> Any:
        if name == "linux_started":
            return True
        if name == "process_prompt":
            prompt = str(args[0]) if args else ""
            cls._last_prompt = prompt
            return f"MCU received: {prompt}"
        if name == "get_status":
            led = "ON" if cls._led_on else "OFF"
            last = cls._last_prompt or "(none)"
            return f"LED={led}, last_prompt={last}"
        if name == "toggle_led":
            cls._led_on = not cls._led_on
            return "ON" if cls._led_on else "OFF"
        raise RuntimeError(f"Unknown mock bridge call: {name}")

    @classmethod
    def notify(cls, name: str, *args: Any) -> None:
        return None


def get_bridge() -> Any:
    return Bridge if ON_BOARD else MockBridge


def run_app(user_loop: Callable[[], None]) -> None:
    if ON_BOARD and App is not None:
        App.run(user_loop=user_loop)
        return

    print("Running in mock mode (no arduino.app_utils / UNO Q board).")
    while True:
        user_loop()
        time.sleep(0.5)
