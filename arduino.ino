void setup() {
  Serial.begin(9600);
  pinMode(4, OUTPUT);
  pinMode(5, OUTPUT);
}

void loop() {
  //get data from rasp pi
  if(Serial.available() > 0) {
    String data = Serial.readStringUntil('\n');
    String message = "dane sucks";
    if(data.compareTo(message) == 0);
    {
        Serial.print("signal recieved");
        //set pins 4 and 5 to high
        digitalWrite(4, HIGH);
        digitalWrite(5, HIGH);
        delay(1000);
        digitalWrite(4, LOW);
        digitalWrite(5, LOW);
        delay(1000);
    }
  }
}

// void loop() {
//   //get data from rasp pi
//   if(Serial.available() > 0) {
//     String data = Serial.readStringUntil('\n');
//     Serial.print("rasp pi sent:");
//     Serial.println(data);
//   }

//   //send data to rasp pi
//   Serial.println("hello from ardunio");
//   delay(1000);
// }