#include <MPU9250.h>

#include "madgwick.h"

#define GYRO_CALIB_THRESH 10
#define GYRO_CALIB_AVG_NUM 30

MPU9250 IMU;

int16_t ax, ay, az, gx, gy, gz, ogx, ogy, ogz;
float fax, fay, faz, fgx, fgy, fgz;

uint32_t timer;

void setup() {
  Wire.begin();
  Serial.begin(115200);

  IMU.initialize();
  IMU.setFullScaleAccelRange(MPU9250_ACCEL_FS_16);
  IMU.setFullScaleGyroRange(MPU9250_GYRO_FS_2000);
  IMU.setDLPFMode(MPU9250_DLPF_BW_42);

  delay(1000);

  calibrateGyro();
}

void loop() {
  IMU.getMotion6(&ax, &ay, &az, &gx, &gy, &gz);
  trimGyroValues();
  calcActualAccelGyro();

  /*Serial.print(String(ax) + "\t" + String(ay) + "\t" + String(az) + "\t" + String(gx) + "\t" + String(gy) + "\t" + String(gz));
  Serial.print("\t");
  Serial.println(String(fax) + "\t" + String(fay) + "\t" + String(faz) + "\t" + String(fgx) + "\t" + String(fgy) + "\t" + String(fgz));*/

  if (millis() - timer > 10) {
    uint32_t microtimer = micros();
    MadgwickAHRSupdateIMU(fgx, fgy, fgz, fax, fay, faz);
    getYawPitchRoll();
    Serial.println(micros() - microtimer);
    timer = millis();
  }
}

void trimGyroValues() {
  gx -= ogx;
  gy -= ogy;
  gz -= ogz;
}

void getYawPitchRoll() {

  float gravx, gravy, gravz;
  float y, p, r;

  gravx = 2 * (q1 * q3 - q0 * q2);
  gravy = 2 * (q0 * q1 + q2 * q3);
  gravz = q0 * q0 - q1 * q1 - q2 * q2 + q3 * q3;

  y = atan2(2 * q1 * q2 - 2 * q0 * q3, 2 * q0 * q0 + 2 * q1 * q1 - 1);
  p = atan2(gravx, sqrt(gravy * gravy + gravz * gravz));
  r = atan2(gravy, gravz);
  if (gravz < 0) {
    if (p > 0) {
      p = PI - p;
    } else {
      p = -PI - p;
    }
  }

  y *= 180 / M_PI;
  p *= 180 / M_PI;
  r *= 180 / M_PI;
}

void calcActualAccelGyro() {
  fax = ax / 2048.f;
  fay = ay / 2048.f;
  faz = az / 2048.f;

  fgx = gx * 2000.f / 32768.f;
  fgy = gy * 2000.f / 32768.f;
  fgz = gz * 2000.f / 32768.f;

  fgx *= M_PI / 180;
  fgy *= M_PI / 180;
  fgz *= M_PI / 180;
}

void calibrateGyro() {
  int minX = -1000, maxX = 1000;
  int minY = -1000, maxY = 1000;
  int minZ = -1000, maxZ = 1000;

  Serial.println("Waiting for no motion...");

  while ((maxX - minX > GYRO_CALIB_THRESH) || (maxY - minY > GYRO_CALIB_THRESH) || (maxZ - minZ > GYRO_CALIB_THRESH)) {
    IMU.getRotation(&gx, &gy, &gz);
    minX++;
    minY++;
    minZ++;
    maxX--;
    maxY--;
    maxZ--;

    if (gx < minX) minX = gx;
    if (gy < minY) minY = gy;
    if (gz < minZ) minZ = gz;
    if (gx > maxX) maxX = gx;
    if (gy > maxY) maxY = gy;
    if (gz > maxZ) maxZ = gz;

    delay(2);
  }

  Serial.println("Calibrating gyro...");

  for (int i = 0; i < GYRO_CALIB_AVG_NUM; i++) {
    IMU.getRotation(&gx, &gy, &gz);
    ogx += gx;
    ogy += gy;
    ogz += gz;
  }

  Serial.println("New gyro offsets: " + String(ogx) + "\t" + String(ogy) + "\t" + String(ogz));
  ogx /= GYRO_CALIB_AVG_NUM;
  ogy /= GYRO_CALIB_AVG_NUM;
  ogz /= GYRO_CALIB_AVG_NUM;
}