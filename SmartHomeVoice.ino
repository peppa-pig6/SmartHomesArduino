#include <Servo.h>

Servo doorServo;

// Pins
const int lightPin = 8;
const int fanPin = 9;
const int securityPin = 10;
const int servoPin = 6;

/*
SERIAL COMMANDS FROM PYTHON
A = Light ON      a = Light OFF
B = Fan ON        b = Fan OFF
C = Door OPEN     c = Door CLOSED
D = Security ON   d = Security OFF
*/

void setup() {
  Serial.begin(9600);

  pinMode(lightPin, OUTPUT);
  pinMode(fanPin, OUTPUT);
  pinMode(securityPin, OUTPUT);

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
        digitalWrite(fanPin, HIGH);
        Serial.println("FAN ON");
        break;

      case 'b':
        digitalWrite(fanPin, LOW);
        Serial.println("FAN OFF");
        break;

      case 'C':
        doorServo.write(90);
        Serial.println("DOOR OPEN");
        break;

      case 'c':
        doorServo.write(0);
        Serial.println("DOOR CLOSE");
        break;

      case 'D':
        digitalWrite(securityPin, HIGH);
        Serial.println("SECURITY ON");
        break;

      case 'd':
        digitalWrite(securityPin, LOW);
        Serial.println("SECURITY OFF");
        break;

      default:
        // ignore unknown commands safely
        break;
    }
  }
}
