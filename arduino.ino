#include <Arduino.h>

void setup() {
  Serial.begin(9600);
  pinMode(4, OUTPUT);
  pinMode(5, OUTPUT);
}

void loop() {
  //get data from rasp pi
  if(Serial.available() > 0) {
    String data = Serial.readStringUntil('\n');
    if(data.compareTo("high") == 0)
    {
      Serial.print("high signal recieved");
      //set pins 4 and 5 to high
      digitalWrite(4, HIGH);
      digitalWrite(5, HIGH);
    }
    else if(data.compareTo("low") == 0)
    {
      Serial.print("low signal recieved");
      //set pins 4 and 5 to low
      digitalWrite(4, LOW);
      digitalWrite(5, LOW);
    }
  }

  //get ph
  int adcValue = analogRead(adcPin);
  float phVoltage = (float)adcValue * 5 / 1024;
  float ph = 2.8*phVoltage;
  Serial.print("pH = "); Serial.println(ph, 3);

  delay(1000);
}