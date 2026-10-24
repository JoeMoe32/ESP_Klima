#pragma once
#include <stdint.h>
#include <math.h>

enum class OperatingMode : uint8_t { Test = 0, Hcho = 1 };
enum Fault : uint16_t { NoFault=0, SensorFault=1, SensorStale=2, RelayFault=4,
  HchoUnavailable=8, StorageFault=16 };
struct Settings {
  float tMin=15, tMax=23, rhMin=30, rhMax=50;
  float tHysteresis=0.3f, rhHysteresis=2;
  float hchoThreshold=300, hchoHysteresis=10;
  bool latchAlarm=false;
};
inline bool validSettings(const Settings& s) {
  return isfinite(s.tMin) && isfinite(s.tMax) && isfinite(s.rhMin) && isfinite(s.rhMax)
    && isfinite(s.tHysteresis) && isfinite(s.rhHysteresis)
    && isfinite(s.hchoThreshold) && isfinite(s.hchoHysteresis)
    && s.tMin >= -45 && s.tMax <= 130 && s.tMin < s.tMax
    && s.rhMin >= 0 && s.rhMax <= 100 && s.rhMin < s.rhMax
    && s.tHysteresis >= 0 && s.tHysteresis*2 < s.tMax-s.tMin
    && s.rhHysteresis >= 0 && s.rhHysteresis*2 < s.rhMax-s.rhMin
    && s.hchoThreshold > 0 && s.hchoThreshold < 65000
    && s.hchoHysteresis >= 0 && s.hchoHysteresis < s.hchoThreshold;
}
struct Sample {
  float temperature=NAN, humidity=NAN, rawHcho=NAN, correctedHcho=NAN;
  uint32_t time=0;
  uint16_t error=0;
  bool valid=false, hchoValid=false;
};
struct ProcessState { bool alarm=false, fault=true, ready=false; uint16_t faults=SensorFault; };
inline int8_t rangeAlarm(float value, float low, float high, float hysteresis, int8_t previous) {
  if (value < low) return -1;
  if (value > high) return 1;
  if (previous == -1 && value < low+hysteresis) return -1;
  if (previous == 1 && value > high-hysteresis) return 1;
  return 0;
}
class AlarmManager {
  int8_t temperatureState_=0, humidityState_=0;
  bool hchoAlarm_=false, latched_=false;
public:
  ProcessState update(const Sample& sample, const Settings& cfg, OperatingMode mode,
      bool service, bool relayOk, bool storageOk, uint32_t now, bool acknowledge=false) {
    ProcessState s;
    s.faults = NoFault;
    if (!sample.valid) s.faults |= SensorFault;
    else if (uint32_t(now-sample.time)>15000) s.faults |= SensorStale;
    if (!relayOk) s.faults |= RelayFault;
    if (!storageOk) s.faults |= StorageFault;
    if (mode == OperatingMode::Hcho && !sample.hchoValid) s.faults |= HchoUnavailable;
    s.fault = s.faults != 0;
    bool current = false;
    if (!(s.faults & (SensorFault|SensorStale|HchoUnavailable))) {
      if (mode == OperatingMode::Test) {
        temperatureState_=rangeAlarm(sample.temperature,cfg.tMin,cfg.tMax,cfg.tHysteresis,temperatureState_);
        humidityState_=rangeAlarm(sample.humidity,cfg.rhMin,cfg.rhMax,cfg.rhHysteresis,humidityState_);
        current=temperatureState_ || humidityState_;
      } else {
        hchoAlarm_=sample.correctedHcho >= cfg.hchoThreshold ||
          (hchoAlarm_ && sample.correctedHcho > cfg.hchoThreshold-cfg.hchoHysteresis);
        current=hchoAlarm_;
      }
    }
    if (!cfg.latchAlarm || (acknowledge && !current && !s.fault)) latched_=false;
    if (cfg.latchAlarm && current) latched_=true;
    s.alarm=current || latched_;
    s.ready=!s.fault && !service;
    return s;
  }
};
inline uint8_t automaticRelays(const ProcessState& s) {
  return (s.alarm ? 1:0) | (s.fault ? 2:0) | (s.ready ? 4:0);
}
