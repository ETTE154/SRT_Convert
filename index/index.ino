#include <WiFiS3.h>
#include <Wire.h> 
#include <LiquidCrystal_I2C.h>

#include "arduino_secrets.h" 
char ssid[] = SECRET_SSID;
char pass[] = SECRET_PASS;

int status = WL_IDLE_STATUS;
WiFiServer server(23);

const int vibrationPin = 3;
boolean alreadyConnected = false;

LiquidCrystal_I2C lcd(0x27,20,4);  // set the LCD address to 0x27 for a 16 chars and 2 line display

void setup() {
  startSerial();
  checkWifiModule();
  connectToWifi();
  startServer();
  setPinModes();
  initLCD();
}

void loop() {
  checkForClient();
}

void startSerial() {
  Serial.begin(9600);
  while (!Serial) {
    ; // wait for serial port to connect. Needed for native USB port only
  }
}

void checkWifiModule() {
  if (WiFi.status() == WL_NO_MODULE) {
    Serial.println("Communication with WiFi module failed!");
    while (true);
  }

  String fv = WiFi.firmwareVersion();
  if (fv < WIFI_FIRMWARE_LATEST_VERSION) {
    Serial.println("Please upgrade the firmware");
  }
}

void connectToWifi() {
  while (status != WL_CONNECTED) {
    Serial.print("Attempting to connect to SSID: ");
    Serial.println(ssid);
    status = WiFi.begin(ssid, pass);
    delay(10000);
  }
  printWifiStatus();
}

void startServer() {
  server.begin();
}

void setPinModes() {
  pinMode(vibrationPin, OUTPUT);
}

void initLCD() {
  lcd.init();                      // initialize the lcd 
  lcd.init();
  lcd.backlight();
}

void checkForClient() {
  WiFiClient client = server.available();

  if (client) {
    if (!alreadyConnected) {
      client.flush();
      String newClientMessage = "New client";
      Serial.println(newClientMessage);
      lcd.clear();  // clear the LCD
      lcd.setCursor(0,0);
      lcd.print(newClientMessage);
      client.println("Hello, client!");
      alreadyConnected = true;
    }

    if (client.available() > 0) {
      String clientInput = client.readStringUntil('\n');
      processClientInput(clientInput);
      Serial.println(clientInput);
    }
  }
}

void processClientInput(String clientInput) {
  int value = clientInput.toInt(); // convert the received string to an integer

  // 입력받은 0~5 사이의 값을 0~255 로 변환
  if (value >= 0 && value <= 5) {
    int outputValue = map(value, 0, 5, 0, 255);
    analogWrite(vibrationPin, outputValue);
  }
  
  lcd.clear();  // clear the LCD
  lcd.setCursor(0,0);
  lcd.print("Receive Value: ");
  lcd.setCursor(0,1);
  lcd.print(value);
}


void printWifiStatus() {
  Serial.print("SSID: ");
  Serial.println(WiFi.SSID());

  IPAddress ip = WiFi.localIP();
  Serial.print("IP Address: ");
  Serial.println(ip);

  long rssi = WiFi.RSSI();
  Serial.print("signal strength (RSSI):");
  Serial.print(rssi);
  Serial.println(" dBm");
}
