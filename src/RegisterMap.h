#pragma once
#include "Core.h"
#include "CalibrationManager.h"
namespace Registers {
constexpr uint16_t Status=0, Mode=1, Faults=2, Temperature=9, Humidity=10,
  HchoRaw=19, HchoCorrected=20, HchoLimit=21, Inputs=29, Relays=30,
  Alarm=39, Fault=40, Ready=41, CalActive=49, Zero=50, Span=51, SpanReference=52,
  Valid=53, HchoValid=54, UptimeHigh=55, UptimeLow=56, SensorError=57, Requests=58, RelayHealthy=59;
inline uint16_t signedValue(float value) {
  if(!isfinite(value) || value < -32767 || value > 32767) return 0x8000;
  return uint16_t(int16_t(lroundf(value)));
}
inline void fill(uint16_t* r,const Sample& sample,const Settings& cfg,const ProcessState& s,
    OperatingMode mode,bool service,const CalibrationManager& cal,uint8_t di,uint8_t relays,
    bool relayHealthy,uint32_t requests,uint32_t now) {
  for(uint8_t i=0;i<64;i++) r[i]=0xffff;
  bool valid=sample.valid && uint32_t(now-sample.time)<=15000;
  bool hchoValid=valid && sample.hchoValid && mode==OperatingMode::Hcho;
  r[Status]=(s.ready?1:0)|(s.alarm?2:0)|(s.fault?4:0)|(service?8:0)|(cal.pending()?16:0)|(mode==OperatingMode::Test?32:0);
  r[Mode]=uint16_t(mode); r[Faults]=s.faults;
  r[Temperature]=valid?signedValue(sample.temperature*100):0x8000;
  r[Humidity]=valid?uint16_t(lroundf(sample.humidity*100)):0xffff;
  r[HchoRaw]=hchoValid?signedValue(sample.rawHcho):0x8000;
  r[HchoCorrected]=hchoValid?signedValue(sample.correctedHcho):0x8000;
  r[HchoLimit]=uint16_t(lroundf(cfg.hchoThreshold));
  r[Inputs]=di; r[Relays]=relays; r[Alarm]=s.alarm; r[Fault]=s.fault; r[Ready]=s.ready;
  r[CalActive]=cal.data.active; r[Zero]=cal.data.haveZero?signedValue(cal.data.zeroRaw):0x8000;
  r[Span]=cal.data.active?signedValue(cal.data.spanRaw):0x8000; r[SpanReference]=300;
  r[Valid]=valid; r[HchoValid]=hchoValid; r[UptimeHigh]=(now/1000)>>16; r[UptimeLow]=now/1000;
  r[SensorError]=sample.error; r[Requests]=requests; r[RelayHealthy]=relayHealthy;
}
}
