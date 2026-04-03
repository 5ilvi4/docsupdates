/*
 * MotionMind IMU Diagnostic
 * Shows raw accelerometer values + detected gesture on screen
 * No BLE — pure sensor test
 */

#include <M5StickCPlus2.h>

void setup() {
  auto cfg = M5.config();
  StickCP2.begin(cfg);
  StickCP2.Display.setRotation(3);
  StickCP2.Display.setTextColor(WHITE, BLACK);
  StickCP2.Display.fillScreen(BLACK);
  Serial.begin(115200);
}

// Gesture latch — holds detected gesture on screen briefly
String latchedGesture = "NEUTRAL";
uint16_t latchedColor = WHITE;
unsigned long latchUntil = 0;
#define LATCH_MS 600

void loop() {
  StickCP2.update();

  float accX, accY, accZ;
  float gyroX, gyroY, gyroZ;
  StickCP2.Imu.getAccel(&accX, &accY, &accZ);
  StickCP2.Imu.getGyro(&gyroX, &gyroY, &gyroZ);

  // Y accel for left/right tilt (held position)
  // gyroX for jump/squat (rate of wrist flick — deg/s)
  String gesture = "NEUTRAL";
  uint16_t color = WHITE;

  if      (accY > 0.4f)    { gesture = "<< LEFT";  color = GREEN;  }
  else if (accY < -0.4f)   { gesture = "RIGHT >>"; color = CYAN;   }
  else if (gyroX < -200.0f){ gesture = "^ JUMP";   color = YELLOW; }
  else if (gyroX > 200.0f) { gesture = "v SQUAT";  color = ORANGE; }

  // Latch gesture so it stays readable
  if (gesture != "NEUTRAL") {
    latchedGesture = gesture;
    latchedColor = color;
    latchUntil = millis() + LATCH_MS;
  }
  if (millis() > latchUntil) {
    latchedGesture = "NEUTRAL";
    latchedColor = WHITE;
  }

  // Display
  StickCP2.Display.fillScreen(BLACK);
  StickCP2.Display.setTextSize(1);
  StickCP2.Display.setTextColor(WHITE, BLACK);

  StickCP2.Display.setCursor(5, 5);
  StickCP2.Display.printf("accY:%.2f accZ:%.2f", accY, accZ);
  StickCP2.Display.setCursor(5, 18);
  StickCP2.Display.printf("gyrX:%.0f gyrY:%.0f", gyroX, gyroY);

  StickCP2.Display.setTextSize(2);
  StickCP2.Display.setTextColor(latchedColor, BLACK);
  StickCP2.Display.setCursor(5, 55);
  StickCP2.Display.println(latchedGesture);
  StickCP2.Display.setTextColor(WHITE, BLACK);

  // Serial output
  Serial.printf("accY:%.2f gyrX:%.0f -> %s\n", accY, gyroX, latchedGesture.c_str());

  delay(30);
}
