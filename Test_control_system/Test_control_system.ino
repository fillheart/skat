#include <Wire.h>
#include <Servo.h>
#include <I2Cdev.h>
#include <MPU6050.h>
#include <SpektrumSerialReceiver.h>

#include "PID.h"

#define GYRO_CALIB_THRESH 10
#define GYRO_CALIB_AVG_NUM 30

#define ROLL_KP 0.15
#define ROLL_KI 0.0001
#define ROLL_KD 0.3

#define PITCH_KP 0.15
#define PITCH_KI 0.0001
#define PITCH_KD 0.3

#define YAW_KP 0.4
#define YAW_KI 0.001
#define YAW_KD 0.7

#define MOTOR_IDLE 1050

#define TILT_R_MIN 2000
#define TILT_L_MIN 960
#define TILT_R_MAXHOV 1500
#define TILT_L_MAXHOV 1530
#define TILT_R_MAX 1100
#define TILT_L_MAX 2100

MPU6050 IMU;

SpektrumSerialReceiver RX(1);

Servo esc1;
Servo esc2;
Servo esc3;

Servo tiltR;
Servo tiltL;

PID rollPID(1000, 32768);
PID pitchPID(1000, 32768);
PID yawPID(1000, 32768);

int gx, gy, gz, ogx, ogy, ogz;

void setup() {
  Wire.begin();
  RX.begin(Serial);

  IMU.initialize();
  IMU.setFullScaleGyroRange(MPU6050_IMU::MPU6050_GYRO_FS_2000);
  IMU.setDLPFMode(MPU6050_IMU::MPU6050_DLPF_BW_42);

  calibrateGyro();

  esc1.attach(2);
  esc2.attach(3);
  esc3.attach(4);
  tiltR.attach(5);
  tiltL.attach(6);

  esc1.writeMicroseconds(1000);
  esc2.writeMicroseconds(1000);
  esc3.writeMicroseconds(1000);

  tiltR.writeMicroseconds(TILT_R_MIN);
  tiltL.writeMicroseconds(TILT_L_MIN);

  tiltR.writeMicroseconds(TILT_R_MAX);
  tiltL.writeMicroseconds(TILT_L_MAX);
  delay(2000);
  tiltR.writeMicroseconds(TILT_R_MAXHOV);
  tiltL.writeMicroseconds(TILT_L_MAXHOV);
  delay(2000);
  tiltR.writeMicroseconds(TILT_R_MIN);
  tiltL.writeMicroseconds(TILT_L_MIN);
  delay(10000);
}

void loop() {
  RX.update();
  IMU.getRotation(&gx, &gy, &gz);
  trimGyroValues();

  int thr, roll, pitch, yaw, fr, fl, r, y;

  thr = map(RX.getChannel(0), 0, 2047, 0, 2000 - MOTOR_IDLE);
  roll = map(RX.getChannel(1), 0, 2047, -5000, 5000);
  pitch = map(RX.getChannel(2), 0, 2047, 5000, -5000);
  yaw = map(RX.getChannel(3), 0, 2047, -5000, 5000);

  fr = -rollPID.calc(gx - roll, ROLL_KP, ROLL_KI, ROLL_KD) - pitchPID.calc(gy - pitch, PITCH_KP, PITCH_KI, PITCH_KD) / 2;
  fl = rollPID.calc(gx - roll, ROLL_KP, ROLL_KI, ROLL_KD) - pitchPID.calc(gy - pitch, PITCH_KP, PITCH_KI, PITCH_KD) / 2;
  r = pitchPID.calc(gy - pitch, PITCH_KP, PITCH_KI, PITCH_KD);
  y = yawPID.calc(gz - yaw, YAW_KP, YAW_KI, YAW_KD);

  tiltR.writeMicroseconds(constrain(map(-y, 0, 1000, TILT_R_MIN, TILT_R_MAXHOV), min(TILT_R_MIN, TILT_R_MAXHOV), max(TILT_R_MIN, TILT_R_MAXHOV)));
  tiltL.writeMicroseconds(constrain(map(y, 0, 1000, TILT_L_MIN, TILT_L_MAXHOV), min(TILT_L_MIN, TILT_L_MAXHOV), max(TILT_L_MIN, TILT_L_MAXHOV)));

  if (RX.getChannel(5) < 1024) {  // arm / disarm motors on CH6
    esc1.writeMicroseconds(constrain(thr + fr + MOTOR_IDLE, MOTOR_IDLE, 2000));
    esc2.writeMicroseconds(constrain(thr + fl + MOTOR_IDLE, MOTOR_IDLE, 2000));
    esc3.writeMicroseconds(constrain(thr + r + MOTOR_IDLE, MOTOR_IDLE, 2000));
  } else {
    esc1.writeMicroseconds(1000);
    esc2.writeMicroseconds(1000);
    esc3.writeMicroseconds(1000);
  }
}

void trimGyroValues() {
  gx -= ogx;
  gy -= ogy;
  gz -= ogz;
}

void calibrateGyro() {
  int minX = -1000, maxX = 1000;
  int minY = -1000, maxY = 1000;
  int minZ = -1000, maxZ = 1000;

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

  for (int i = 0; i < GYRO_CALIB_AVG_NUM; i++) {
    IMU.getRotation(&gx, &gy, &gz);
    ogx += gx;
    ogy += gy;
    ogz += gz;
  }
  ogx /= GYRO_CALIB_AVG_NUM;
  ogy /= GYRO_CALIB_AVG_NUM;
  ogz /= GYRO_CALIB_AVG_NUM;
}