// UNO Q starter sketch: blink the built-in LED.
// Deploy on-device with: arduino-app-cli app start .

void setup() {
  pinMode(LED_BUILTIN, OUTPUT);
}

void loop() {
  digitalWrite(LED_BUILTIN, HIGH);
  delay(500);
  digitalWrite(LED_BUILTIN, LOW);
  delay(500);
}
