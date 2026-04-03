/*
 * MotionMind v4 — HijelHID_BLEKeyboard (iOS tested)
 * Y-axis gesture detection, wrist-worn orientation
 */

#include <M5StickCPlus2.h>
#include <HijelHID_BLEKeyboard.h>

HijelHID_BLEKeyboard keyboard("MotionMind", "MCIM", 100);

#define COOLDOWN_MS 400
unsigned long lastGestureTime = 0;

void sendGesture(uint8_t key, const char* label, uint16_t color) {
  keyboard.tap(key);
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

  keyboard.setDebugLevel(HIDLogLevel::Normal);
  keyboard.begin();

  StickCP2.Display.setCursor(5, 20);
  StickCP2.Display.setTextSize(2);
  StickCP2.Display.println("MotionMind");
  StickCP2.Display.setTextSize(1);
  StickCP2.Display.setCursor(5, 50);
  StickCP2.Display.println("BLE: waiting...");
  Serial.println("Advertising...");
}

void loop() {
  StickCP2.update();

  float accX, accY, accZ;
  StickCP2.Imu.getAccel(&accX, &accY, &accZ);

  // Update status
  static unsigned long lastDisplay = 0;
  if (millis() - lastDisplay > 300) {
    lastDisplay = millis();
    bool connected = keyboard.isConnected();
    StickCP2.Display.fillRect(0, 0, 240, 40, BLACK);
    StickCP2.Display.setCursor(5, 5);
    StickCP2.Display.setTextSize(1);
    StickCP2.Display.setTextColor(connected ? GREEN : WHITE, BLACK);
    StickCP2.Display.printf("BLE: %s", connected ? "CONNECTED" : "waiting...");
    StickCP2.Display.setTextColor(WHITE, BLACK);
    StickCP2.Display.setCursor(5, 18);
    StickCP2.Display.printf("Y:%.2f Z:%.2f", accY, accZ);
  }

  float gyroX, gyroY, gyroZ;
  StickCP2.Imu.getGyro(&gyroX, &gyroY, &gyroZ);

  if ((millis() - lastGestureTime) < COOLDOWN_MS) { delay(10); return; }
  if (!keyboard.isConnected()) { delay(10); return; }

  // Y accel: wrist tilt left/right (right arm)
  // gyroX: wrist flick speed for jump/squat
  if      (accY < -0.3f)    sendGesture(KEY_LEFT,  "<< LEFT",  GREEN);
  else if (accY >  0.3f)    sendGesture(KEY_RIGHT, "RIGHT >>", CYAN);
  else if (gyroX < -200.0f) sendGesture(KEY_SPACE, "^ JUMP",   YELLOW);
  else if (gyroX >  200.0f) sendGesture(KEY_DOWN,  "v SQUAT",  ORANGE);

  // Button A = hoverboard
  if (StickCP2.BtnA.wasPressed()) sendGesture(KEY_H, "HOVERBOARD", PURPLE);

  delay(10);
}
