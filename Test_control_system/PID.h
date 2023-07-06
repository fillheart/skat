class PID {
private:
  float _value;
  float _err;
  float _integral;
  uint32_t _cycleTime;
  uint32_t _timer;

public:

  PID(int32_t cycleTime, int32_t integralLimit = 32767) {
    _cycleTime = cycleTime;
  }

  float calc(float err, float kP, float kI, float kD) {
    if (micros() - _timer > _cycleTime) {
      _integral += kI * err * _cycleTime;
      _value = kP * err + kI * _integral + kD * (err - _err) / _cycleTime;
      _timer = micros();
    }
    return _value;
  }
};