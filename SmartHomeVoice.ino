const int red = 8;
const int yellow = 9;
const int green = 10;

void setup() {
  pinMode(red, OUTPUT);
  pinMode(yellow, OUTPUT);
  pinMode(green, OUTPUT);

  Serial.begin(9600);
}

void allOff() {
  digitalWrite(red, LOW);
  digitalWrite(yellow, LOW);
  digitalWrite(green, LOW);
}

void loop() {

  if (Serial.available()) {

    String cmd = Serial.readStringUntil('\n');
    cmd.trim();

    Serial.print("Received: ");
    Serial.println(cmd);

    allOff();

    if (cmd == "red") {
      digitalWrite(red, HIGH);
    }
    else if (cmd == "yellow") {
      digitalWrite(yellow, HIGH);
    }
    else if (cmd == "green") {
      digitalWrite(green, HIGH);
    }
  }
}
