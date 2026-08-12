# UnoQ-1

[Arduino App Lab](https://docs.arduino.cc/software/app-lab/) project for the Arduino UNO Q with **Telegram integration**. Send a message to your Telegram bot and it is forwarded to the MCU sketch over RouterBridge.

## Layout

- `app.yaml` — App Lab metadata
- `sketch/` — MCU firmware (`arduino:zephyr:unoq`) with RouterBridge handlers
- `python/` — Linux-side Telegram bot + RouterBridge client
- `scripts/cloud-agent-install.sh` — Cloud Agent toolchain bootstrap

## Telegram setup

1. Create a bot with [@BotFather](https://t.me/BotFather) and copy the token.
2. On the UNO Q, copy `python/telegram_config.example.py` to `python/telegram_config.py` and set:
   - `TELEGRAM_BOT_TOKEN`
   - `TELEGRAM_ALLOWED_USER_IDS` (recommended — your Telegram user ID from [@userinfobot](https://t.me/userinfobot))
3. Alternatively, set environment variables `TELEGRAM_BOT_TOKEN` and `TELEGRAM_ALLOWED_USER_IDS`.

### Bot commands

| Command | Action |
| --- | --- |
| Any text | Forwarded to MCU as a prompt (`process_prompt`) |
| `/status` | Read MCU status |
| `/led` | Toggle the built-in LED |
| `/help` | Show help |

## Local / Cloud Agent (no board)

```bash
./scripts/cloud-agent-install.sh
arduino-cli compile -b arduino:zephyr:unoq ./sketch
python3 python/main.py   # mock MCU demo when Telegram token is unset
```

With `TELEGRAM_BOT_TOKEN` set, `python3 python/main.py` starts long-polling Telegram (requires network access to `api.telegram.org`).

## On the UNO Q (App Lab / SSH)

Copy this repo to `~/ArduinoApps/UnoQ-1` on the board, configure `python/telegram_config.py`, then:

```bash
arduino-app-cli app start ~/ArduinoApps/UnoQ-1
arduino-app-cli app logs ~/ArduinoApps/UnoQ-1
arduino-app-cli app stop ~/ArduinoApps/UnoQ-1
```

The board needs WiFi for Telegram API access. MCU ↔ Linux communication uses the built-in RouterBridge (no extra wiring).
