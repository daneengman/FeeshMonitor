void setup() {
  Serial.begin(9600);
}

void loop() {
  //get data from rasp pi
  if(Serial.available() > 0) {
    String data = Serial.readStringUntil('\n');
    Serial.print("rasp pi sent:");
    Serial.println(data);
  }

  //send data to rasp pi
  Serial.println("hello from ardunio");
  delay(1000);
}