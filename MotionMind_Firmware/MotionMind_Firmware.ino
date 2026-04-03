/*
 * MotionMind Firmware for M5StickC PLUS2
 * ----------------------------------------
 * Architecture: PS Controller HID Model
 *   IMU Tilt/Motion → GestureDetector → BLE HID Keyboard
 *   (Standard HID keys — no game knowledge needed)
 *
 * Gesture → Key Mapping (mirrors GestureClassifier.swift):
 *   Lean Left   → LEFT ARROW
 *   Lean Right  → RIGHT ARROW
 *   Jump (up)   → SPACE BAR
 *   Squat (down)→ DOWN ARROW
 *   Hoverboard  → Button A double-tap → 'H' key
 *
 * Hardware: M5StickC PLUS2 (ESP32-PICO-V3-02, IMU: MPU6886)
 */

#include <M5StickCPlus2.h>
#include <BleKeyboard.h>

// ── BLE HID Keyboard ──────────────────────────────────────────────
// Changed name to force fresh pairing (old "MotionMind" was keyboard too,
// but iPad may have cached wrong profile — new name = clean slate)
BleKeyboard bleKeyboard("MotionMind2", "MCIM", 100);

// ── Gesture Thresholds ────────────────────────────────────────────
// Tilt angle in degrees
#define LEAN_LEFT_THRESHOLD   -20.0f   // pitch < -20 → lean left
#define LEAN_RIGHT_THRESHOLD   20.0f   // pitch >  20 → lean right
#define JUMP_THRESHOLD         -2.5f   // accel Z spike (upward liftoff)
#define SQUAT_THRESHOLD         2.5f   // accel Z dip (downward squat)

// Timing
#define GESTURE_COOLDOWN_MS    400     // 400ms between gestures (matches Swift)
#define JUMP_DETECT_WINDOW_MS  200     // look for jump peak within 200ms
#define HOVERBOARD_WINDOW_MS   500     // two wrist-like shakes within 500ms (use button A as proxy)

// ── State ─────────────────────────────────────────────────────────
unsigned long lastGestureTime = 0;
unsigned long lastShakeTime   = 0;
int           shakeCount      = 0;

float prevAccZ = 0;
bool  inJump   = false;

enum Gesture {
  NONE,
  LEAN_LEFT,
  LEAN_RIGHT,
  JUMP,
  SQUAT,
  HOVERBOARD
};

// ── Helpers ───────────────────────────────────────────────────────
bool cooldownExpired() {
  return (millis() - lastGestureTime) >= GESTURE_COOLDOWN_MS;
}

void sendKey(uint8_t key, const char* label) {
  if (!bleKeyboard.isConnected()) return;
  bleKeyboard.press(key);
  delay(50);
  bleKeyboard.releaseAll();
  lastGestureTime = millis();

  StickCP2.Display.fillScreen(BLACK);
  StickCP2.Display.setCursor(10, 50);
  StickCP2.Display.setTextSize(2);
  StickCP2.Display.println(label);
  Serial.println(label);
}

// ── IMU-Based Gesture Detection ───────────────────────────────────
Gesture detectGesture(float accX, float accY, float accZ, float gyroX, float gyroY, float gyroZ) {
  // Use Y axis for left/right (wrist-worn orientation)
  float tilt = accY;

  if (tilt > 0.4f)    return LEAN_LEFT;
  if (tilt < -0.4f)   return LEAN_RIGHT;

  // Jump: Z goes negative (upward lift)
  if (accZ < -0.5f && !inJump) {
    inJump = true;
    return JUMP;
  }
  if (inJump && accZ > 0.5f) inJump = false;

  // Squat: Z increases beyond resting gravity
  if (accZ > 1.5f && !inJump) return SQUAT;

  return NONE;
}

// ── Setup ─────────────────────────────────────────────────────────
void setup() {
  auto cfg = M5.config();
  StickCP2.begin(cfg);

  StickCP2.Display.setRotation(3);  // landscape
  StickCP2.Display.setTextColor(WHITE, BLACK);
  StickCP2.Display.setTextSize(1);
  StickCP2.Display.fillScreen(BLACK);

  // Splash screen
  StickCP2.Display.setCursor(5, 20);
  StickCP2.Display.setTextSize(2);
  StickCP2.Display.println("MotionMind");
  StickCP2.Display.setTextSize(1);
  StickCP2.Display.setCursor(5, 50);
  StickCP2.Display.println("Starting BLE...");

  // Start BLE HID keyboard
  bleKeyboard.begin();

  delay(1000);
}

// ── Main Loop ─────────────────────────────────────────────────────
void loop() {
  StickCP2.update();  // read buttons + IMU

  // ── BLE Connection Status ────────────────────────────────────────
  bool connected = bleKeyboard.isConnected();

  // ── Read IMU ────────────────────────────────────────────────────
  float accX, accY, accZ;
  float gyroX, gyroY, gyroZ;
  StickCP2.Imu.getAccel(&accX, &accY, &accZ);
  StickCP2.Imu.getGyro(&gyroX, &gyroY, &gyroZ);

  // ── Screen Header (live IMU values) ─────────────────────────────
  static unsigned long lastDisplay = 0;
  if (millis() - lastDisplay > 200) {
    lastDisplay = millis();
    StickCP2.Display.fillRect(0, 0, 240, 40, BLACK);
    StickCP2.Display.setCursor(5, 5);
    StickCP2.Display.setTextSize(1);
    StickCP2.Display.printf("BLE: %s", connected ? "CONNECTED" : "waiting...");
    StickCP2.Display.setCursor(5, 18);
    StickCP2.Display.printf("X:%.2f Y:%.2f Z:%.2f", accX, accY, accZ);
  }

  // ── Button A → Hoverboard (wrist-cross proxy) ───────────────────
  if (StickCP2.BtnA.wasPressed()) {
    unsigned long now = millis();
    if (now - lastShakeTime < HOVERBOARD_WINDOW_MS) {
      shakeCount++;
    } else {
      shakeCount = 1;
    }
    lastShakeTime = now;

    if (shakeCount >= 2 && cooldownExpired()) {
      shakeCount = 0;
      sendKey('h', "HOVERBOARD");
      return;
    }
  }

  if (!cooldownExpired()) {
    delay(10);
    return;
  }

  Gesture g = detectGesture(accX, accY, accZ, gyroX, gyroY, gyroZ);

  switch (g) {
    case LEAN_LEFT:
      sendKey(KEY_LEFT_ARROW, "<< LEFT");
      break;
    case LEAN_RIGHT:
      sendKey(KEY_RIGHT_ARROW, "RIGHT >>");
      break;
    case JUMP:
      sendKey(' ', "^ JUMP");
      break;
    case SQUAT:
      sendKey(KEY_DOWN_ARROW, "v SQUAT");
      break;
    default:
      break;
  }

  delay(10);
}
