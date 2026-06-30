#include <Servo.h>

Servo doorServo;

// Pins
const int lightPin = 8;
const int servoPin = 6;

/*
SERIAL COMMANDS FROM PYTHON
A = Light ON      a = Light OFF
B = Door OPEN     b = Door CLOSED
*/

void setup() {
  Serial.begin(9600);

  pinMode(lightPin, OUTPUT);

  doorServo.attach(servoPin);
  doorServo.write(0);

  // IMPORTANT: clear any garbage serial data at startup
  while (Serial.available()) {
    Serial.read();
  }

  Serial.println("SYSTEM READY");
}

void loop() {
  if (Serial.available()) {

    char cmd = Serial.read();

    switch (cmd) {

      case 'A':
        digitalWrite(lightPin, HIGH);
        Serial.println("LIGHT ON");
        break;

      case 'a':
        digitalWrite(lightPin, LOW);
        Serial.println("LIGHT OFF");
        break;

      case 'B':
        doorServo.write(90);
        Serial.println("DOOR OPEN");
        break;

      case 'b':
        doorServo.write(0);
        Serial.println("DOOR CLOSED");
        break;

      default:
        // Ignore unknown commands safely
        break;
    }
  }
}
