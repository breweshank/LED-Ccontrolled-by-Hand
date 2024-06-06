const int ledPin = 9;

void setup() {
  pinMode(ledPin, OUTPUT);
  Serial.begin(9600);
}

void loop() {
  if (Serial.available() > 0) {
    int brightness = Serial.parseInt();
    analogWrite(ledPin, brightness);
  }
}
