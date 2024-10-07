#include <ArduinoBLE.h>

// BLE Service UUID
BLEService customService("12345678-1234-5678-1234-56789abcdef0");

// BLE Characteristic UUIDs (RX/TX)
BLECharacteristic rxCharacteristic("12345678-1234-5678-1234-56789abcdef1", BLEWrite, 20); // RX (Write)
BLECharacteristic txCharacteristic("12345678-1234-5678-1234-56789abcdef2", BLERead | BLENotify, 20); // TX (Notify)

// Function to handle when data is received
void onReceive(BLEDevice central, BLECharacteristic characteristic) {
  // Get the length of the received value
  int length = characteristic.valueLength();
  
  // Allocate a buffer to hold the received data
  char receivedData[length + 1];
  
  // Copy the data into the buffer
  memcpy(receivedData, characteristic.value(), length);
  
  // Null-terminate the string
  receivedData[length] = '\0';
  
  // Print the received data to the serial monitor
  Serial.print("Received from central: ");
  Serial.println(receivedData);

  // Echo the received data back to the central
  txCharacteristic.writeValue((const uint8_t*)receivedData, length);
  Serial.print("Sent back to central: ");
  Serial.println(receivedData);
}

void setup() {
  Serial.begin(115200);

  // Begin BLE initialization
  if (!BLE.begin()) {
    Serial.println("Starting BLE failed!");
    while (1);
  }

  // Set advertised device name and service
  BLE.setLocalName("Nano-ESP32-BLE");
  BLE.setAdvertisedService(customService);

  // Add characteristics to the service
  customService.addCharacteristic(rxCharacteristic);
  customService.addCharacteristic(txCharacteristic);

  // Add service to BLE
  BLE.addService(customService);

  // Set initial values for characteristics
  txCharacteristic.writeValue("Hello Central!");

  // Start advertising
  BLE.advertise();
  Serial.println("BLE device active, waiting for connections...");
}

void loop() {
  // Wait for a BLE central to connect
  BLEDevice central = BLE.central();
  
  if (central) {
    // Keep processing while central is connected
    while (central.connected()) {
      // Check if the RX characteristic has been written to
      if (rxCharacteristic.written()) {
        // Read the incoming data
        int length = rxCharacteristic.valueLength();
        char receivedData[length + 1];
        memcpy(receivedData, rxCharacteristic.value(), length);
        receivedData[length] = '\0'; // Null terminate the string

        // Print the received data to the serial monitor
        Serial.println(receivedData);

        // Reset the characteristic to avoid reprinting the same data
        rxCharacteristic.writeValue(""); // Reset the value or clear the characteristic

        // Optionally, clear or reset the characteristic's internal state here if needed
      }
    }

    // Central disconnected
    Serial.println("Central disconnected");
  }
}
