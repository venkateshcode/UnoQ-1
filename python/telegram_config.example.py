"""Example Telegram config for the UNO Q board.

Copy to telegram_config.py and fill in your values:
  cp python/telegram_config.example.py python/telegram_config.py

Or set environment variables instead:
  TELEGRAM_BOT_TOKEN
  TELEGRAM_ALLOWED_USER_IDS  (comma-separated Telegram user IDs)
"""

TELEGRAM_BOT_TOKEN = "123456789:REPLACE_WITH_BOTFATHER_TOKEN"

# Restrict who can control the board. Leave empty to allow all users.
TELEGRAM_ALLOWED_USER_IDS = [
    # 123456789,
]
