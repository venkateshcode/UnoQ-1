// UNO Q: receive prompts from the Linux/Python side via RouterBridge.
// Telegram messages are forwarded by python/main.py using Bridge.call().

#include "Arduino_RouterBridge.h"

bool ledOn = false;
String lastPrompt = "";

bool waitForLinux(int timeoutSec = 30) {
  bool started = false;
  unsigned long startMs = millis();
  while (!started && (millis() - startMs) < (unsigned long)timeoutSec * 1000UL) {
    if (Bridge.call("linux_started").result(started) && started) {
      return true;
    }
    delay(100);
  }
  return false;
}

String process_prompt(String prompt) {
  lastPrompt = prompt;
  Monitor.print("Prompt from Linux: ");
  Monitor.println(prompt);

  // Pulse the LED to show the MCU received the prompt (no delay in callbacks).
  ledOn = true;
  digitalWrite(LED_BUILTIN, HIGH);
  digitalWrite(LED_BUILTIN, LOW);
  ledOn = false;

  return String("MCU received: ") + prompt;
}

String get_status(String arg) {
  String status = String("LED=") + (ledOn ? "ON" : "OFF");
  if (lastPrompt.length() > 0) {
    status += String(", last_prompt=") + lastPrompt;
  } else {
    status += ", last_prompt=(none)";
  }
  return status;
}

String toggle_led(String arg) {
  ledOn = !ledOn;
  digitalWrite(LED_BUILTIN, ledOn ? HIGH : LOW);
  return ledOn ? "ON" : "OFF";
}

void setup() {
  pinMode(LED_BUILTIN, OUTPUT);
  digitalWrite(LED_BUILTIN, LOW);

  Monitor.begin();
  Bridge.begin();
  Bridge.provide_safe("process_prompt", process_prompt);
  Bridge.provide_safe("get_status", get_status);
  Bridge.provide_safe("toggle_led", toggle_led);

  if (waitForLinux()) {
    Monitor.println("Bridge ready — Python/Telegram side is up");
  } else {
    Monitor.println("Warning: Python not ready (timeout)");
  }
}

void loop() {}
