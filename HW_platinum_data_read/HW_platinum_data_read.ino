#include <Servo.h>

Servo esc;

void setup() {
  Serial1.begin(19200);
  Serial.begin(115200);
  esc.attach(7);
  esc.writeMicroseconds(1000);
}

void loop() {
  while(Serial1.read() != 0x9B);
  delay(10);
  uint8_t data[9];
  for(int i = 0; i < 9; i++){
    data[i] = Serial1.read();
  }

  for(uint8_t byte : data) Serial.print(String(byte, HEX) + '\t');
  uint16_t e_cycle_time = data[7] << 8 | data[8];
  Serial.println();

  Serial.println(1000000.f/e_cycle_time/7*60);
}
