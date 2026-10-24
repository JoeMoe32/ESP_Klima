#pragma once
#include <Ethernet.h>

// ESP32 Arduino 2.x uses begin(uint16_t); Ethernet 2.0.2 uses begin().
class FixedPortEthernetServer : public EthernetServer {
public:
  explicit FixedPortEthernetServer(uint16_t port):EthernetServer(port) {}
  void begin(uint16_t=0) override {
    // Ethernet.begin() does not close existing listening sockets. Reuse them
    // after link recovery or IP changes instead of consuming another socket.
    if(!static_cast<bool>(*this)) EthernetServer::begin();
  }
};
