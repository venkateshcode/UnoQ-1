# UnoQ-1

Starter [Arduino App Lab](https://docs.arduino.cc/software/app-lab/) project for the Arduino UNO Q.

## Layout

- `app.yaml` — App Lab metadata
- `sketch/` — MCU firmware (`arduino:zephyr:unoq`)
- `python/` — Linux-side Python entrypoint
- `scripts/cloud-agent-install.sh` — Cloud Agent toolchain bootstrap

## Local / Cloud Agent (no board)

```bash
./scripts/cloud-agent-install.sh
arduino-cli compile -b arduino:zephyr:unoq ./sketch
```

## On the UNO Q (App Lab / SSH)

Copy this repo to `~/ArduinoApps/UnoQ-1` on the board, then:

```bash
arduino-app-cli app start ~/ArduinoApps/UnoQ-1
arduino-app-cli app logs ~/ArduinoApps/UnoQ-1
arduino-app-cli app stop ~/ArduinoApps/UnoQ-1
```

Board SSH / USB connection is optional for Cloud Agent compile checks and is not configured in this environment.
