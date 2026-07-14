const int red = 8;
const int blue = 9;
const int green = 10;

void setup() {
  pinMode(red, OUTPUT);
  pinMode(blue, OUTPUT);
  pinMode(green, OUTPUT);

  Serial.begin(9600);
}

void allOff() {
  digitalWrite(red, LOW);
  digitalWrite(blue, LOW);
  digitalWrite(green, LOW);
}

void allOn() {
  digitalWrite(red, HIGH);
  digitalWrite(blue, HIGH);
  digitalWrite(green, HIGH);
}

void loop() {
  if (Serial.available()) {
    String cmd = Serial.readStringUntil('\n');
    cmd.trim();
    cmd.toLowerCase(); // Clean input to prevent case mismatches

    Serial.print("Received: ");
    Serial.println(cmd);

    if (cmd == "red on") {
      digitalWrite(red, HIGH);
    }
    else if (cmd == "red off") {
      digitalWrite(red, LOW);
    }
    else if (cmd == "blue on") {
      digitalWrite(blue, HIGH);
    }
    else if (cmd == "blue off") {
      digitalWrite(blue, LOW);
    }
    else if (cmd == "green on") {
      digitalWrite(green, HIGH);
    }
    else if (cmd == "green off") {
      digitalWrite(green, LOW);
    }
    else if (cmd == "all on") {
      allOn();
    }
    else if (cmd == "all off") {
      allOff();
    }
  }
}
