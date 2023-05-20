#include <SPI.h>
#include <MFRC522.h>

#define SS_PIN 10
#define RST_PIN 5
#define LED_PIN 9
#define DENIED_LED_PIN 8

MFRC522 rfid(SS_PIN, RST_PIN);

void setup() {
  Serial.begin(9600);
  while (!Serial); // wait for serial port to connect
  SPI.begin(); // init SPI bus
  rfid.PCD_Init(); // init MFRC522
  pinMode(LED_PIN, OUTPUT); // set LED pin as output
  pinMode(DENIED_LED_PIN, OUTPUT); // set denied LED pin as output
  digitalWrite(LED_PIN, LOW); // turn off LED initially
  digitalWrite(DENIED_LED_PIN, LOW); // turn off denied LED initially
}

void loop() {
  if (rfid.PICC_IsNewCardPresent()) { // new tag is available
    if (rfid.PICC_ReadCardSerial()) { // NUID has been read
      // send UID to computer via serial communication
      for (int i = 0; i < rfid.uid.size; i++) {
        Serial.print(rfid.uid.uidByte[i] < 0x10 ? "0" : "");
        Serial.print(rfid.uid.uidByte[i], HEX);
      }
      Serial.println();

      // wait for Python script to read serial data
      while (Serial.available() <= 0) {
        delay(1);
      }
      String response = Serial.readStringUntil('\n'); // read response from Python script
      if (response == "1") {
        digitalWrite(LED_PIN, HIGH); // turn on LED
        delay(2000); // keep LED on for 2 seconds
        digitalWrite(LED_PIN, LOW); // turn off LED
      } else if (response == "0") {
        digitalWrite(DENIED_LED_PIN, HIGH); // turn on denied LED
        delay(2000); // keep denied LED on for 2 seconds
        digitalWrite(DENIED_LED_PIN, LOW); // turn off denied LED
      }
      rfid.PICC_HaltA(); // halt PICC
      rfid.PCD_StopCrypto1(); // stop encryption on PCD
    }
  }
  delay(1000);
}
