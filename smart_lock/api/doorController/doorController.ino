#include<Servo.h>
const int doorPin = 9; // Replace 9 with the actual pin number for the door servo
const int indicatorPin = 13; // Replace 13 with the actual pin number for the indicator

Servo door;


void setup() {
  Serial.begin(9600);
  door.attach(doorPin);
  
}

void loop() {
  while (1){
    if (Serial.available() > 0) {
    char cmd = Serial.read();
    if (cmd == '1') {
      
      door.write(160);
      delay(15);
    } else if (cmd == '0') {
      
      door.write(0);
      delay(15);
    }
  }
  }
}
