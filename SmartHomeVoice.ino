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
}

void loop() {
  if (Serial.available()) {
    char cmd = Serial.read();

    switch (cmd) {
      case 'A':
        digitalWrite(lightPin, HIGH);
        break;
      case 'a':
        digitalWrite(lightPin, LOW);
        break;
      case 'B':
        digitalWrite(fanPin, HIGH);
        break;
      case 'b':
        digitalWrite(fanPin, LOW);
        break;
      case 'C':
        doorServo.write(90);
        break;
      case 'c':
        doorServo.write(0);
        break;
      case 'D':
        digitalWrite(securityPin, HIGH);
        break;
      case 'd':
        digitalWrite(securityPin, LOW);
        break;
    }
  }
}
