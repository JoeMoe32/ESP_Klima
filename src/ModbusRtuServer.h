#pragma once
#include <Arduino.h>
#include "BoardIO.h"
#include "ModbusProtocol.h"
class ModbusRtuServer {
  uint8_t buffer_[256]={}; size_t length_=0; bool overflow_=false;
  uint32_t lastByte_=0;
public:
  uint32_t requests=0, rejected=0, lastRequest=0;
  uint16_t registers[64]={};
  void begin() {
    Serial1.setRxBufferSize(512); Serial1.setTxBufferSize(256);
    Serial1.begin(9600,SERIAL_8N1,Pins::RX,Pins::TX);
    Serial.println("[MODBUS] RTU Slave 1, 9600 8N1, TX17 RX18, FC03/04");
  }
  void update() {
    // 4 ms > 3.5 characters at 9600 baud, 8N1.
    // Drain bytes already received before deciding that an idle gap completed a frame.
    if(!Serial1.available() && (length_ || overflow_) && uint32_t(micros()-lastByte_)>=4000) {
      uint8_t response[256]; size_t n=overflow_?0:ModbusProtocol::reply(buffer_,length_,registers,64,response,sizeof(response));
      if(n) { Serial1.write(response,n); requests++; lastRequest=millis(); }
      else rejected++;
      length_=0; overflow_=false;
    }
    unsigned budget=256;
    while(budget-- && Serial1.available()) {
      uint8_t b=Serial1.read(); lastByte_=micros();
      if(length_<sizeof(buffer_) && !overflow_) buffer_[length_++]=b; else overflow_=true;
    }
  }
};
