//MQTT Client based on PubSubClient by Nick O'Leary 
//CCS811 Device Library by DFRobot_CCS881
//Communications and Networking libraries by espressif and Arduino

#include <Wire.h>
#include <SPI.h>
#include <Adafruit_Sensor.h>

#include <WiFi.h>
#include <PubSubClient.h>
#include <DHT11.h>
#include <CCS811.h>

CCS811 CCS811;

#define SEALEVELPRESSURE_HPA (1013.25)
#define TOKEN ""
#define DEVICEID ""

const char* ssid = "mqttserver";
const char* password = "";
const char* mqtt_server = "192.168.97.182";

WiFiClient espClient;
PubSubClient client(espClient);
long last = 0;
char msg[50];
int value = 0;

DHT11 dht11(33);
int temperature = 0;
int humidity = 0;
float VOC = 0;
float CO2 = 0;
char tempString[8];
char humString[8];
char VOCString[8];
char CO2String[8];
char PIRString[8];

const int pir_pin = 4;
const int echo_pin = 26;
const int trig_pin = 27;

void setup() {
  Serial.begin(115200);
  
  while (!Serial);

  Serial.println(F("CCS811 test"));
  while(CCS811.begin() != 0);
  Serial.println(F("CCS811 connected"));
  
  Serial.println(F("WiFi test"));
  setup_wifi();
  Serial.println(F("WiFi connected"));
  client.setServer(mqtt_server, 1883);

  pinMode(pir_pin, INPUT);
}

void setup_wifi() {
  delay(10);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED);
  Serial.println(WiFi.localIP());
}

void reconnect() {
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    if (client.connect("ESP32Client")) {
      Serial.println("connected");
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 1 second");
      delay(1000);
    }
  }
}

void loop() {
  if (!client.connected()) {
    reconnect();
  }

  int result = dht11.readTemperatureHumidity(temperature, humidity);

  dtostrf(temperature, 1, 2, tempString);
  Serial.print("Temperature: ");
  Serial.println(tempString);
  client.publish("esp32/temperature", tempString);

  dtostrf(humidity, 1, 2, humString);
  Serial.print("Temperature: ");
  Serial.println(humString);
  client.publish("esp32/humidity", humString);
  
  Serial.print("PIR: ");
  if (digitalRead(pir_pin)) {
    Serial.println("Motion detected");
    strcpy(PIRString, "True");
  } else {
    Serial.println("No motion");
    strcpy(PIRString, "False");
  }
  client.publish("esp32/PIR", PIRString);

  if((CCS811.checkDataReady()==true)){


      VOC = CCS811.getTVOCPPB();
      dtostrf(VOC, 1, 2, VOCString);
      Serial.print("VOC: ");
      Serial.println(VOCString);
      client.publish("esp32/VOC", VOCString);

      CO2 = CCS811.getCO2PPM();
      dtostrf(CO2, 1, 2, CO2String);
      Serial.print("CO2: ");
      Serial.println(CO2String);
      client.publish("esp32/CO2", CO2String);

      Serial.println();
  }
  delay(500);
}