#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>
#include "Adafruit_HTU21DF.h"
#include <WiFi.h>
#include <Wire.h>
#include <math.h>

#define AO_PIN 36

Adafruit_MPU6050 mpu;
Adafruit_HTU21DF htu = Adafruit_HTU21DF();
const char* ssid = "Redmi Note 12";
const char* password = "13131313";
const char* host = "192.168.221.172";
bool danger = 0;
char  send_data[40] = {'\0'};
bool volatile blinker = 0;

char dng_cntr = 0;
bool dng_flag = 0;

bool buzzer_flag = 0;
char buzzer_cntr = 0;

WiFiClient client;

void setup(void) {
  pinMode(12,OUTPUT);
  pinMode(13,OUTPUT);
  pinMode(15,OUTPUT);
  pinMode(19, INPUT);
  
  Serial.begin(115200);
  while (!Serial)
    delay(10); // will pause Zero, Leonardo, etc until serial console opens
  Serial.print("start\n");
  
  // Connencting to Server:
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);
  Serial.print("connecting to WiFi...\n");
  while(1){
    if(WiFi.status() == WL_CONNECTED){
        Serial.println("[WiFi] WiFi is connected!\n");
        Serial.print("[WiFi] IP address: ");
        Serial.println(WiFi.localIP());
        Serial.print("\n");
        break;
    }
  }
  while(!client.connect(host, 2222)){
  Serial.println("Connection to host failed\n");
  }
  Serial.println("Connected to host!\n");
  
  // Initializing MPU6050:
  if (!mpu.begin()) {
    Serial.println("Failed to find MPU6050 chip\n");}
  mpu.setAccelerometerRange(MPU6050_RANGE_8_G);
  mpu.setGyroRange(MPU6050_RANGE_500_DEG);
  mpu.setFilterBandwidth(MPU6050_BAND_21_HZ);

  // temp:
  if (!htu.begin()) {
    Serial.println("Check circuit. HTU21D not found!");
  }
  
  //delay(20000);
}

void loop() {
  
  /* MPU6050 */
  sensors_event_t a, g, temp;
  mpu.getEvent(&a, &g, &temp);
  float acc = pow((pow(a.acceleration.x, 2) + pow(a.acceleration.y, 2) + pow(a.acceleration.z, 2)), 0.5);
  if (acc >= 25) {
    danger = 1;
    Serial.print("Dangerrrrrrrrr!!!!!!!!!!! accelaration is: ");
    Serial.print(acc);
    Serial.print("\n");
  }

  /* Heart Rate */

  /* Gas Detection */
  int gasValue = analogRead(AO_PIN);
  if(gasValue>1000){
    danger = 1;
    Serial.println("Gas Detected!");
  }
  else{
    Serial.println("Gas Not Detected!");
  }
  /* Tempreture */
  float tempreture = htu.readTemperature();
  /* LED Alarm */
  
  sprintf(send_data, "10_%f_%f_%f_%d",100 - acc, tempreture, acc, gasValue);
//  client.print(acc);
  client.print(send_data);
  delay(1000);

/* LED Status */
if(danger == 1)
  dng_flag = 1;

danger = 0;
 
if(dng_flag){
  digitalWrite(13, HIGH);
  digitalWrite(12, LOW);
  if(dng_cntr > 5){
    dng_cntr = 0;
    dng_flag = 0;
    digitalWrite(13, LOW);
  }
  dng_cntr++;
  }
else{
  if(blinker == 1){
    
    digitalWrite(12, HIGH);
    blinker = 0;
  }else{
    digitalWrite(12, LOW);
    blinker = 1;
  }
}

if(digitalRead(19))
  buzzer_flag = 1;

if(buzzer_flag){
  if(buzzer_cntr > 2){
    buzzer_flag = 0;
    buzzer_cntr = 0;
    digitalWrite(15, LOW);
  }
  else{
    buzzer_cntr++;
    digitalWrite(15, HIGH);
  }
}
}
