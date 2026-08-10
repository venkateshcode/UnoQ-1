#!/usr/bin/env bash
# Idempotent Cloud Agent bootstrap for Arduino UNO Q / App Lab development.
set -euo pipefail

BIN_DIR="${HOME}/.local/bin"
mkdir -p "${BIN_DIR}"
export PATH="${BIN_DIR}:${PATH}"

if ! command -v arduino-cli >/dev/null 2>&1; then
  curl -fsSL https://raw.githubusercontent.com/arduino/arduino-cli/master/install.sh \
    | BINDIR="${BIN_DIR}" sh
fi

# Keep CLI on PATH for subsequent agent shells.
if ! grep -q 'HOME/.local/bin' "${HOME}/.bashrc" 2>/dev/null; then
  echo 'export PATH="$HOME/.local/bin:$PATH"' >> "${HOME}/.bashrc"
fi

arduino-cli version
arduino-cli config init --overwrite >/dev/null
arduino-cli core update-index
arduino-cli core install arduino:zephyr

# Smoke-check: compile the starter sketch offline (no board required).
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
arduino-cli compile -b arduino:zephyr:unoq "${ROOT}/sketch"

echo "Arduino UNO Q toolchain ready (arduino:zephyr:unoq)."
