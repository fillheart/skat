#include <GyverHX711.h>
#include <Servo.h>
GyverHX711 sensor(3, 2, HX_GAIN64_A);
// HX_GAIN128_A - канал А усиление 128
// HX_GAIN32_B - канал B усиление 32
// HX_GAIN64_A - канал А усиление 64
Servo esc;

#define LPF_K 0.025

long data;

void setup() {
  Serial.begin(115200);
  Serial1.begin(19200);

  esc.attach(7);
  esc.writeMicroseconds(2000);
  delay(2000);
  esc.writeMicroseconds(1000);
  delay(5000);

  // если тарирование при первом запуске -
  // нужно выждать готовность датчика
  sensor.tare();  // калибровка нуля

  //sensor.sleepMode(true);		// выключить датчик
  //sensor.sleepMode(false);	// включить датчик
}

uint16_t pwm = 950;
uint32_t time;
uint8_t esc_data[9];

void loop() {
  // чтение только по доступности! if available
  if (sensor.available()) {
    data += (sensor.read() - data) * LPF_K;
    /*Serial.print(-50000);  // To freeze the lower limit
    Serial.print(" ");
    Serial.print(50000);  // To freeze the upper limit
    Serial.print(" ");
    Serial.println(map(data, 0, 2650, 0, 100));*/
  }

  if (Serial1.read() == 0x9B) {
    delay(5);
    for (int i = 0; i < 9; i++) {
      esc_data[i] = Serial1.read();
    }
  }

  uint16_t e_cycle_time = esc_data[7] << 8 | esc_data[8];
  float rpm = 1000000.f / e_cycle_time / 7 * 60;

  if (millis() - time > 1500) {
    Serial.println(String(pwm) + '\t' + String(map(data, 0, 2650, 0, 100)) + '\t' + String(rpm));
    if(pwm == 2000){
      esc.detach();
      while(true);
    }
    time = millis();
    pwm += 50;
    esc.writeMicroseconds(pwm);
  }
}