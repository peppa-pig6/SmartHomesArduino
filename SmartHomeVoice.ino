#include <Servo.h>

Servo doorServo;

// Pins
const int livingRoomLightPin = 8;
const int kitchenLightPin = 7;
const int servoPin = 6;

/*
SERIAL COMMANDS FROM PYTHON

A = Living Room Light ON
a = Living Room Light OFF

K = Kitchen Light ON
k = Kitchen Light OFF

B = Door OPEN
b = Door CLOSED

G = Good Boy

P = Party Mode
*/

void setup() {

  Serial.begin(9600);

  pinMode(livingRoomLightPin, OUTPUT);
  pinMode(kitchenLightPin, OUTPUT);

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
        digitalWrite(livingRoomLightPin, HIGH);
        Serial.println("LIVING ROOM LIGHT ON");
        break;

      case 'a':
        digitalWrite(livingRoomLightPin, LOW);
        Serial.println("LIVING ROOM LIGHT OFF");
        break;

      case 'K':
        digitalWrite(kitchenLightPin, HIGH);
        Serial.println("KITCHEN LIGHT ON");
        break;

      case 'k':
        digitalWrite(kitchenLightPin, LOW);
        Serial.println("KITCHEN LIGHT OFF");
        break;

      case 'B':
        doorServo.write(90);
        Serial.println("DOOR OPEN");
        break;

      case 'b':
        doorServo.write(0);
        Serial.println("DOOR CLOSED");
        break;

      case 'G':

        for (int i = 0; i < 6; i++) {

          doorServo.write(60);
          delay(150);

          doorServo.write(120);
          delay(150);
        }

        doorServo.write(90);  // Stop in the open position
        Serial.println("HAPPY WAG");
        break;

      case 'P':

        for (int i = 0; i < 8; i++) {

          digitalWrite(livingRoomLightPin, HIGH);
          digitalWrite(kitchenLightPin, LOW);
          doorServo.write(40);
          delay(180);

          digitalWrite(livingRoomLightPin, LOW);
          digitalWrite(kitchenLightPin, HIGH);
          doorServo.write(140);
          delay(180);
        }

        // Finish with everything back to normal
        doorServo.write(0);
        digitalWrite(livingRoomLightPin, LOW);
        digitalWrite(kitchenLightPin, LOW);

        Serial.println("PARTY MODE");

        break;

      case 'L':
        digitalWrite(livingRoomLightPin, HIGH);
        digitalWrite(kitchenLightPin, HIGH);
        Serial.println("ALL LIGHTS ON");
        break;

      case 'l':
        digitalWrite(livingRoomLightPin, LOW);
        digitalWrite(kitchenLightPin, LOW);
        Serial.println("ALL LIGHTS OFF");
        break;

      default:
        // Ignore unknown commands safely
        break;
    }
  }
}

/*
==========================================
Declaration:

The overall project design, implementation, and integration were developed by AI. As this was my first time working with C++, I used AI to assist with generating this code and understanding concepts.

==========================================
*/
