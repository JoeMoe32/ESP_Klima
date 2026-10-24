#pragma once
#include <Preferences.h>
#include "Core.h"
struct Calibration {
  uint32_t version=1;
  float zeroRaw=0, spanRaw=300;
  bool haveZero=false, active=false;
};
inline bool validCalibration(const Calibration& c) {
  return c.version==1 && isfinite(c.zeroRaw) && isfinite(c.spanRaw)
    && (!c.active || (c.haveZero && c.spanRaw-c.zeroRaw>1));
}
inline float correctHcho(float raw,const Calibration& c) {
  return c.active && validCalibration(c)?300.0f*(raw-c.zeroRaw)/(c.spanRaw-c.zeroRaw):raw;
}
class CalibrationManager {
  Preferences prefs_; bool open_=false;
  uint8_t pending_=0; float proposed_=0; uint32_t requested_=0;
public:
  Calibration data;
  bool healthy=true;
  void begin() {
    open_=prefs_.begin("hcho-cal",false); healthy=open_;
    if(!open_ || !prefs_.isKey("record")) return;
    if(prefs_.getBytesLength("record")!=sizeof(data) || prefs_.getBytes("record",&data,sizeof(data))!=sizeof(data)
        || !validCalibration(data)) { data=Calibration{}; healthy=false; }
  }
  bool pending() const { return pending_!=0; }
  void cancel() { pending_=0; }
  void update(uint32_t now,bool service) { if(!service || uint32_t(now-requested_)>30000) cancel(); }
  bool propose(uint8_t kind,const Sample& s,OperatingMode mode,bool service,uint32_t now) {
    cancel();
    if(!service || mode!=OperatingMode::Hcho || !s.valid || !s.hchoValid || !isfinite(s.rawHcho)
       || uint32_t(now-s.time)>15000 || kind<1 || kind>3) return false;
    if(kind==2 && (!data.haveZero || s.rawHcho-data.zeroRaw<=1)) return false;
    pending_=kind; proposed_=s.rawHcho; requested_=now;
    Serial.printf("[CAL] Vorschlag %s raw=%.2f; innerhalb 30 s mit 'cal confirm' bestaetigen\n",kind==1?"ZERO":kind==2?"SPAN 300":"RESET",proposed_);
    return true;
  }
  bool confirm(const Sample& s,OperatingMode mode,bool service,uint32_t now) {
    if(!pending_ || !service || mode!=OperatingMode::Hcho || uint32_t(now-requested_)>30000 ||
       !s.valid || !s.hchoValid || uint32_t(now-s.time)>15000) { cancel(); return false; }
    Calibration next=data;
    if(pending_==1) { next.zeroRaw=proposed_; next.haveZero=true; next.active=false; }
    if(pending_==2) { next.spanRaw=proposed_; next.active=true; }
    if(pending_==3) next=Calibration{};
    cancel();
    if(!open_ || !validCalibration(next)) return false;
    healthy=prefs_.putBytes("record",&next,sizeof(next))==sizeof(next);
    if(healthy) data=next;
    return healthy;
  }
};
