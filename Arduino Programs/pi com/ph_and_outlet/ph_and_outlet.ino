#include <Arduino.h>
#include <math.h>

bool heating = false;

void setup() {
  Serial.begin(9600);
  pinMode(4, OUTPUT);
  pinMode(5, OUTPUT);

  digitalWrite(4, LOW);
  digitalWrite(5, LOW);
}

void loop() {
  //get data from rasp pi
  if(Serial.available() > 0) {
    String data = Serial.readStringUntil('\n');
    if(data.compareTo("high") == 0)
    {
      Serial.print("high signal recieved\n");
      //set pins 4 and 5 to high
      digitalWrite(4, HIGH);
      digitalWrite(5, HIGH);
    }
    else if(data.compareTo("low") == 0)
    {
      Serial.print("low signal recieved\n");
      //set pins 4 and 5 to low
      digitalWrite(4, LOW);
      digitalWrite(5, LOW);
    }
    else {
      Serial.print("No signal received\n");
    }

    delay(100);

    //get and calculate ph
    int adcValue = analogRead(A0);
    float pHVoltage = (float)adcValue * 5 / 1024;
    float pH = 2.8*pHVoltage;
    Serial.print("pH:"); Serial.println(pH, 3);

    //calculate co2
    int dKH = 6; //CHANGE THIS BASED OFF MEASURED VALUE
    float CO2 = 12.839 * dKH * pow(10, (6.37 - pH));
    Serial.print("CO2:"); Serial.println(CO2, 3);
    delay(100);
  }

  
}