#include <WiFi.h>
#include <HTTPClient.h>
#include <Adafruit_BMP280.h>
#include <Wire.h>


const char* ssid = "SSID";
const char* password = "PASSWORD";
const char* url = "http://SERVER_IP:PORT/heater";
int counter = 0;
int counter2 = 0;

// Adafruit_BMP280 bmp;

void setup() {
  pinMode(2, OUTPUT);  
  pinMode(5, OUTPUT);
  digitalWrite(2, LOW);
  digitalWrite(5, LOW);

  
  Serial.begin(115200); 


  // if (!bmp.begin(0x76)) {
  //   Serial.println("Could not find a valid BMP280 sensor, check wiring!");
  //   while (1);
  // }

  //   bmp.setSampling(Adafruit_BMP280::MODE_NORMAL,     /* Operating Mode. */
  //                 Adafruit_BMP280::SAMPLING_X2,     /* Temp. oversampling */
  //                 Adafruit_BMP280::SAMPLING_X16,    /* Pressure oversampling */
  //                 Adafruit_BMP280::FILTER_X16,      /* Filtering. */
  //                 Adafruit_BMP280::STANDBY_MS_500);

  connect();

}

void loop() {
  if(WiFi.status()== WL_CONNECTED) {
    HTTPClient http;

    http.begin(url);
    
    digitalWrite(2, HIGH);
    delay(100);
    int ResponseCode = http.GET();
    digitalWrite(2, LOW);


    if (ResponseCode>0) {
      Serial.print("HTTP Response code: ");
      Serial.println(ResponseCode);
      String payload = http.getString();
      Serial.println(payload);
      if (payload == "1") {
        Serial.println("ON");
        digitalWrite(5, LOW);
      }
      else {
        Serial.println("OFF");
        digitalWrite(5, HIGH);
      }
    }
    else {
      Serial.println("OFF");
      digitalWrite(5, HIGH);      
      Serial.print("Error code: ");
      Serial.println(ResponseCode);
    }

    http.end();
  }
  else {
    Serial.println("OFF");
    digitalWrite(5, HIGH);
    Serial.println("WiFi Disconnected");
    connect();
  }

  delay(300000);
  // delay(300000);
  // while (counter < 30000 && digitalRead(12) == HIGH) {
  //   delay(10);
  //   counter++;
  // }
  // counter = 0;
}

void connect() {
  WiFi.begin(ssid, password);

  Serial.print("Connecting");

  while (WiFi.status() != WL_CONNECTED) {
    digitalWrite(2, HIGH);
    delay(100);
    digitalWrite(2, LOW);
    delay(100);
    Serial.print(".");
    counter2++;
    if (counter2 >= 150) {
      Serial.println("");
      Serial.println("Failure,\nretrying in 10s");
      counter2 = 0;
      delay(10000);
      WiFi.begin(ssid, password);
      Serial.print("Connecting");
    }
  }
  counter2 = 0;

  Serial.println("");
  Serial.print("Connected to WiFi network with IP Address: ");
  Serial.println(WiFi.localIP());
  delay(500);
}