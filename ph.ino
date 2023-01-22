#include <Arduino.h>

const int adcPin = A0;

void setup() {
  Serial.begin(115200);
}

void loop() {
  int adcValue = analogRead(adcPin);
  float phVoltage = (float)adcValue * 5 / 1024;
  //Serial.print("ADC = "); Serial.print(adcValue);
  //Serial.print("; Po = "); Serial.println(phVoltage, 3);

  float ph = 2.8*phVoltage;
  Serial.print("pH = "); Serial.println(ph, 3);
  delay(1000);
}