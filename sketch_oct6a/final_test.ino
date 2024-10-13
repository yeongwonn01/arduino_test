#include <ArduinoBLE.h>

// BLE 서비스 UUID
BLEService customService("12345678-1234-5678-1234-56789abcdef0");

// BLE 특성 UUID (RX/TX)
BLECharacteristic rxCharacteristic("12345678-1234-5678-1234-56789abcdef1", BLEWrite, 20); // RX (쓰기)
BLECharacteristic txCharacteristic("12345678-1234-5678-1234-56789abcdef2", BLERead | BLENotify, 20); // TX (알림)

void setup() {
  Serial.begin(115200);

  // BLE 초기화 시작
  if (!BLE.begin()) {
    Serial.println("Starting BLE failed!");
    while (1);
  }

  // 광고할 장치 이름과 서비스를 설정
  BLE.setLocalName("Nano-ESP32-BLE");
  BLE.setAdvertisedService(customService);

  // 서비스에 특성을 추가
  customService.addCharacteristic(rxCharacteristic);
  customService.addCharacteristic(txCharacteristic);

  // BLE에 서비스 추가
  BLE.addService(customService);

  // 특성의 초기 값 설정
  txCharacteristic.writeValue("Hello Central!");

  // 광고 시작
  BLE.advertise();
  Serial.println("BLE device active, waiting for connections...");
}

void loop() {
  // BLE 중앙 장치가 연결될 때까지 대기
  BLEDevice central = BLE.central();
  
  if (central) {
    Serial.print("Connected to central: ");
    Serial.println(central.address());

    // 중앙 장치가 연결되어 있는지 계속 확인
    while (central.connected()) {
      // 시리얼 모니터에서 입력된 데이터 전송
      if (Serial.available()) {
        String inputData = Serial.readStringUntil('\n');
        txCharacteristic.writeValue(inputData.c_str(), inputData.length());
        Serial.print("Sent from Serial Monitor to central: ");
        Serial.println(inputData);
        String send_comp = ""
        txCharacteristic.writeValue()
      }
      // RX 특성에 데이터가 쓰여진 경우
      if (rxCharacteristic.written()) {
        // RX 특성 값이 변경된 후 처리를 완료한 뒤 초기화
         rxCharacteristic.readValue((uint8_t*)receivedData, length);

        // 수신된 값의 길이를 가져옴
        int length = rxCharacteristic.valueLength();
        
        // 수신된 데이터를 저장할 버퍼 할당
        char receivedData[length + 1];
        
        // 데이터를 버퍼에 복사
        memcpy(receivedData, rxCharacteristic.value(), length);
        
        // 문자열 끝에 널 문자를 추가
        receivedData[length] = '\0';
        
        // 수신된 데이터를 시리얼 모니터에 출력
        Serial.print("Received from central: ");
        Serial.println(receivedData);
      }
    }

    // 중앙 장치 연결 해제됨
    Serial.println("Central disconnected");
  }
}