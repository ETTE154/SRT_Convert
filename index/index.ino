#include <WiFiS3.h>
#include <Wire.h> 
#include <LiquidCrystal_I2C.h>

#include "arduino_secrets.h"  // 아두이노 비밀 정보를 저장하고 있는 헤더 파일
// WiFi 접속을 위한 SSID와 비밀번호를 선언
char ssid[] = SECRET_SSID; // WiFi SSID
char pass[] = SECRET_PASS; // WiFi 비밀번호

int status = WL_IDLE_STATUS; // WiFi 상태를 저장하는 변수
WiFiServer server(23); // WiFi 서버 객체

const int vibrationPin = 3; // 진동 모터가 연결된 핀 번호
boolean alreadyConnected = false; // 클라이언트가 연결되었는지 여부를 저장하는 변수

LiquidCrystal_I2C lcd(0x27,20,4);  // I2C 주소가 0x27인 20x4 LCD를 선언

void setup() {
  startSerial();     // 시리얼 통신 시작
  checkWifiModule(); // WiFi 모듈 체크
  connectToWifi();   // WiFi에 연결
  startServer();     // 서버 시작
  setPinModes();     // 핀 모드 설정
  initLCD();         // LCD 초기화
}

void loop() {
  checkForClient();  // 클라이언트 확인
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

// 클라이언트로부터 받은 입력을 처리하는 함수
void processClientInput(String clientInput) {
  int value = clientInput.toInt();

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
