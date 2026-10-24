#pragma once
#include "EthernetServerCompat.h"
#include "ModbusProtocol.h"

// All W5500 access remains on the Ethernet task. Two independent TCP sessions.
class ModbusTcpServer {
  struct Session {
    EthernetClient client;
    uint8_t frame[260]={};
    size_t used=0;
    uint32_t lastByte=0, started=0;
  } sessions_[2];
  FixedPortEthernetServer server_{502};
public:
  uint32_t requests=0, rejected=0;
  void begin() { server_.begin(); }
  void stop() { for(auto& s:sessions_) { s.client.stop(); s.used=0; } }
  void update(const uint16_t* registers,bool fresh) {
    for(auto& s:sessions_) {
      if(s.client && !s.client.connected() && !s.client.available()) { s.client.stop(); s.used=0; }
    }
    EthernetClient incoming=server_.accept();
    if(incoming) {
      bool accepted=false;
      for(auto& s:sessions_) if(!s.client) {
        s.client=incoming; s.client.setConnectionTimeout(100); s.used=0; s.lastByte=millis(); accepted=true; break;
      }
      if(!accepted) incoming.stop();
    }
    for(auto& s:sessions_) {
      unsigned budget=260;
      while(s.client && s.client.available() && budget--) {
        if(!s.used) s.started=millis();
        s.frame[s.used++]=s.client.read(); s.lastByte=millis();
        int expected=ModbusProtocol::tcpFrameLength(s.frame,s.used);
        if(expected<0) { rejected++; s.client.stop(); s.used=0; break; }
        if(expected && s.used==size_t(expected)) {
          uint8_t response[260];
          size_t n=ModbusProtocol::replyTcp(s.frame,s.used,registers,64,response,sizeof(response),fresh);
          if(n) {
            // A client that stops reading must not block the Ethernet task.
            if(s.client.availableForWrite()<int(n)) { rejected++; s.client.stop(); }
            else { if(s.client.write(response,n)!=n) s.client.stop(); requests++; }
          } else rejected++;
          s.used=0;
        }
      }
      if(s.client && ((s.used && uint32_t(millis()-s.started)>3000) || uint32_t(millis()-s.lastByte)>60000)) {
        if(s.used) rejected++;
        s.client.stop(); s.used=0;
      }
    }
  }
};
