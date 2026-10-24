#pragma once
#include <Arduino.h>
#include <Wire.h>
#include <DFRobot_SCD4X.h>
#include "Core.h"

// Bewaehrter SCD4x-I2C-Test, ausschliesslich Temperatur und Feuchte.
// Fuer SFA40 spaeter einen eigenen Treiber hinter Sample ergaenzen.
class SensorManager {
  enum Stage { Stop, Stopping, Starting, Poll, ReadyReply, MeasurementReply, Retry } stage_=Stop;
  uint32_t deadline_=0;
  Sample sample_;
  bool command(uint16_t cmd) {
    Wire.beginTransmission(SCD4X_I2C_ADDR);
    Wire.write(uint8_t(cmd>>8)); Wire.write(uint8_t(cmd));
    uint8_t error=Wire.endTransmission();
    if (error) { fail(100+error); return false; }
    return true;
  }
  void fail(uint16_t error) {
    if (sample_.error != error) Serial.printf("[SENSOR] Fehler=%u\n",error);
    sample_.valid=false; sample_.hchoValid=false; sample_.error=error;
    stage_=Retry; deadline_=millis()+10000;
  }
  bool readWords(uint16_t* words,uint8_t count) {
    uint8_t expected=count*3;
    uint8_t received=Wire.requestFrom(SCD4X_I2C_ADDR,expected);
    if (received!=expected) { while(Wire.available()) Wire.read(); fail(200+received); return false; }
    for(uint8_t i=0;i<count;i++) {
      uint8_t bytes[2]={uint8_t(Wire.read()),uint8_t(Wire.read())};
      uint8_t responseCrc=Wire.read(), crc=0xff;
      for(auto b:bytes) { crc^=b; for(uint8_t bit=0;bit<8;bit++) crc=(crc&0x80)?(crc<<1)^0x31:crc<<1; }
      if(crc!=responseCrc) { while(Wire.available()) Wire.read(); fail(300+i); return false; }
      words[i]=(uint16_t(bytes[0])<<8)|bytes[1];
    }
    return true;
  }
public:
  void begin() { stage_=Stop; deadline_=millis(); }
  const Sample& sample() const { return sample_; }
  void update(uint32_t now) {
    if(int32_t(now-deadline_)<0) return;
    uint16_t words[3]={};
    switch(stage_) {
      case Stop: case Retry:
        if(command(SCD4X_STOP_PERIODIC_MEASURE)) { stage_=Stopping; deadline_=now+500; }
        break;
      case Stopping:
        if(command(SCD4X_START_PERIODIC_MEASURE)) { stage_=Starting; deadline_=now+5000; }
        break;
      case Starting: case Poll:
        if(command(SCD4X_GET_DATA_READY_STATUS)) { stage_=ReadyReply; deadline_=now+2; }
        break;
      case ReadyReply:
        if(!readWords(words,1)) break;
        if(!(words[0]&0x7ff)) { stage_=Poll; deadline_=now+500; break; }
        if(command(SCD4X_READ_MEASUREMENT)) { stage_=MeasurementReply; deadline_=millis()+2; }
        break;
      case MeasurementReply:
        if(!readWords(words,3)) break;
        // Das erste Datenwort wird absichtlich nicht als Prozesswert verwendet.
        sample_.temperature=-45.0f+175.0f*words[1]/65535.0f;
        sample_.humidity=100.0f*words[2]/65535.0f;
        sample_.time=now; sample_.valid=true; sample_.error=0;
        stage_=Poll; deadline_=now+5000;
        Serial.printf("[SENSOR] TEST_MODE T=%.2f C RH=%.2f %%\n",sample_.temperature,sample_.humidity);
        break;
    }
  }
};
