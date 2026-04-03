/*
 * MotionMind v3 — NimBLE HID Keyboard (proper iOS bonding)
 * Y-axis gesture detection, wrist-worn orientation
 */

#include <M5StickCPlus2.h>
#include <NimBLEDevice.h>
#include <NimBLEHIDDevice.h>
#include <HIDTypes.h>

#define KEY_LEFT_ARROW  0x50
#define KEY_RIGHT_ARROW 0x4F
#define KEY_SPACE       0x2C
#define KEY_DOWN_ARROW  0x51
#define COOLDOWN_MS     400

static const uint8_t hidReportDescriptor[] = {
  USAGE_PAGE(1),0x01, USAGE(1),0x06, COLLECTION(1),0x01,
  REPORT_ID(1),0x01,
  USAGE_PAGE(1),0x07, USAGE_MINIMUM(1),0xE0, USAGE_MAXIMUM(1),0xE7,
  LOGICAL_MINIMUM(1),0x00, LOGICAL_MAXIMUM(1),0x01,
  REPORT_SIZE(1),0x01, REPORT_COUNT(1),0x08, HIDINPUT(1),0x02,
  REPORT_COUNT(1),0x01, REPORT_SIZE(1),0x08, HIDINPUT(1),0x01,
  REPORT_COUNT(1),0x06, REPORT_SIZE(1),0x08,
  LOGICAL_MINIMUM(1),0x00, LOGICAL_MAXIMUM(1),0x65,
  USAGE_MINIMUM(1),0x00, USAGE_MAXIMUM(1),0x65, HIDINPUT(1),0x00,
  REPORT_COUNT(1),0x05, REPORT_SIZE(1),0x01,
  USAGE_PAGE(1),0x08, USAGE_MINIMUM(1),0x01, USAGE_MAXIMUM(1),0x05,
  LOGICAL_MINIMUM(1),0x00, LOGICAL_MAXIMUM(1),0x01,
  HIDOUTPUT(1),0x02, REPORT_COUNT(1),0x01, REPORT_SIZE(1),0x03,
  HIDOUTPUT(1),0x01, END_COLLECTION(0)
};

NimBLEHIDDevice* hid;
NimBLECharacteristic* inputKeyboard;
bool deviceConnected = false;
unsigned long lastGestureTime = 0;

class ServerCallbacks : public NimBLEServerCallbacks {
  void onConnect(NimBLEServer* pServer) {
    deviceConnected = true;
    StickCP2.Display.fillScreen(BLACK);
    StickCP2.Display.setCursor(5, 50);
    StickCP2.Display.setTextSize(2);
    StickCP2.Display.setTextColor(GREEN, BLACK);
    StickCP2.Display.println("CONNECTED!");
    StickCP2.Display.setTextColor(WHITE, BLACK);
    Serial.println("Connected");
  }
  void onDisconnect(NimBLEServer* pServer) {
    deviceConnected = false;
    NimBLEDevice::startAdvertising();
    Serial.println("Disconnected - advertising");
  }
};

void sendKey(uint8_t keycode, const char* label, uint16_t color) {
  if (!deviceConnected) return;
  uint8_t report[8] = {0, 0, keycode, 0, 0, 0, 0, 0};
  inputKeyboard->setValue(report, sizeof(report));
  inputKeyboard->notify();
  delay(50);
  memset(report, 0, sizeof(report));
  inputKeyboard->setValue(report, sizeof(report));
  inputKeyboard->notify();
  lastGestureTime = millis();
  StickCP2.Display.fillScreen(BLACK);
  StickCP2.Display.setCursor(5, 50);
  StickCP2.Display.setTextSize(2);
  StickCP2.Display.setTextColor(color, BLACK);
  StickCP2.Display.println(label);
  StickCP2.Display.setTextColor(WHITE, BLACK);
  Serial.println(label);
}

void setup() {
  auto cfg = M5.config();
  StickCP2.begin(cfg);
  StickCP2.Display.setRotation(3);
  StickCP2.Display.setTextColor(WHITE, BLACK);
  StickCP2.Display.fillScreen(BLACK);
  Serial.begin(115200);

  NimBLEDevice::init("MotionMind3");
  NimBLEDevice::setSecurityAuth(true, true, true);
  NimBLEDevice::setPower(ESP_PWR_LVL_P9);

  NimBLEServer* pServer = NimBLEDevice::createServer();
  pServer->setCallbacks(new ServerCallbacks());

  hid = new NimBLEHIDDevice(pServer);
  inputKeyboard = hid->getInputReport(1);
  hid->setManufacturer("MCIM");
  hid->setPnp(0x02, 0xe502, 0xa111, 0x0210);
  hid->setHidInfo(0x00, 0x01);
  hid->setReportMap((uint8_t*)hidReportDescriptor, sizeof(hidReportDescriptor));
  hid->startServices();

  NimBLEAdvertising* pAdvertising = NimBLEDevice::getAdvertising();
  pAdvertising->setAppearance(HID_KEYBOARD);
  pAdvertising->addServiceUUID(hid->getHidService()->getUUID());
  pAdvertising->start();

  StickCP2.Display.setCursor(5, 20);
  StickCP2.Display.setTextSize(2);
  StickCP2.Display.println("MotionMind3");
  StickCP2.Display.setTextSize(1);
  StickCP2.Display.setCursor(5, 50);
  StickCP2.Display.println("BLE: waiting...");
  Serial.println("Advertising...");
}

void loop() {
  StickCP2.update();
  float accX, accY, accZ;
  StickCP2.Imu.getAccel(&accX, &accY, &accZ);

  static unsigned long lastDisplay = 0;
  if (!deviceConnected && millis() - lastDisplay > 300) {
    lastDisplay = millis();
    StickCP2.Display.fillRect(0, 40, 240, 30, BLACK);
    StickCP2.Display.setCursor(5, 42);
    StickCP2.Display.setTextSize(1);
    StickCP2.Display.printf("Y:%.2f Z:%.2f", accY, accZ);
  }

  if ((millis() - lastGestureTime) < COOLDOWN_MS) { delay(10); return; }

  if      (accY >  0.4f) sendKey(KEY_LEFT_ARROW,  "<< LEFT",  GREEN);
  else if (accY < -0.4f) sendKey(KEY_RIGHT_ARROW, "RIGHT >>", 0x07FF);
  else if (accZ < -0.5f) sendKey(KEY_SPACE,        "^ JUMP",   YELLOW);
  else if (accZ >  1.5f) sendKey(KEY_DOWN_ARROW,   "v SQUAT",  ORANGE);

  if (StickCP2.BtnA.wasPressed()) sendKey(0x0B, "HOVERBOARD", PURPLE);

  delay(10);
}
