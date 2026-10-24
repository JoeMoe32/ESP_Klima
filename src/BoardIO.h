#pragma once
#include <Arduino.h>
#include <Wire.h>
namespace Pins {
constexpr uint8_t SDA=42, SCL=41, TCA=0x20;
constexpr uint8_t DI[8]={4,5,6,7,8,9,10,11};
constexpr uint8_t TX=17, RX=18, ETH_INT=12, MOSI=13, MISO=14, SCLK=15, CS=16;
}
class BoardIO {
  uint8_t actual_=0, desired_=0, stable_=0, candidate_=0, longSent_=0, longEvents_=0;
  uint32_t changed_[8]={}, pressed_[8]={}, lastAttempt_=0;
  bool configured_=false, healthy_=false;
  bool write(uint8_t reg, uint8_t value) {
    Wire.beginTransmission(Pins::TCA); Wire.write(reg); Wire.write(value);
    return Wire.endTransmission()==0;
  }
public:
  void begin() {
    for (auto pin: Pins::DI) pinMode(pin,INPUT_PULLUP);
    lastAttempt_=millis()-1000;
  }
  void request(uint8_t outputs) { desired_=outputs; }
  void update(uint32_t now) {
    for (uint8_t i=0;i<8;i++) {
      const uint8_t bit=1<<i;
      const bool raw=digitalRead(Pins::DI[i])==LOW;
      if (raw != bool(candidate_&bit)) { candidate_^=bit; changed_[i]=now; }
      if (raw != bool(stable_&bit) && uint32_t(now-changed_[i])>=30) {
        stable_^=bit; pressed_[i]=now; longSent_ &= ~bit;
        Serial.printf("[DI] DI%u=%u\n",i+1,raw);
      }
      if ((stable_&bit) && !(longSent_&bit) && uint32_t(now-pressed_[i])>=5000) {
        longSent_|=bit; longEvents_|=bit;
      }
    }
    if (healthy_ && actual_==desired_) return;
    if (uint32_t(now-lastAttempt_)<1000) return;
    lastAttempt_=now;
    if (!configured_) {
      if (!write(0x01,0) || !write(0x03,0)) { healthy_=false; return; }
      configured_=true; actual_=0;
    }
    if (!write(0x01,desired_)) { healthy_=false; configured_=false;
      Serial.println("[FAULT] TCA9554 Schreibfehler"); return; }
    if (!healthy_ || actual_!=desired_) Serial.printf("[RELAY] Maske=0x%02X\n",desired_);
    actual_=desired_; healthy_=true;
  }
  bool healthy() const { return healthy_; }
  uint8_t outputs() const { return actual_; }
  uint8_t inputs() const { return stable_; }
  uint8_t takeLongPress() { auto v=longEvents_; longEvents_=0; return v; }
};
