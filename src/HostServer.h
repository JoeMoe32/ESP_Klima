#pragma once
#include <Arduino.h>
#include <freertos/FreeRTOS.h>
#include <freertos/queue.h>
#include "Core.h"
#include "NetworkConfig.h"
struct HostSnapshot {
  Sample sample;
  Settings settings;
  ProcessState process;
  OperatingMode mode=OperatingMode::Test;
  bool service=false, calibration=false, calPending=false, relayHealthy=false;
  uint8_t di=0, relays=0;
  uint32_t uptime=0, requests=0, rejected=0, lastRequest=0, serviceRemaining=0;
  char key[33]={};
  char lastCommand[120]={};
  uint16_t registers[64]={};
  uint32_t publishedAt=0;
};
struct HostCommand { char text[160]={}; char key[33]={}; };
struct NetworkState {
  bool hardware=false, link=false, online=false, dhcp=true;
  char ip[16]="0.0.0.0";
  uint32_t tcpRequests=0, tcpRejected=0;
};
class HostServer {
  QueueHandle_t snapshots_=nullptr, commands_=nullptr, network_=nullptr, netCommands_=nullptr;
  static void task(void* context);
  void run();
public:
  bool begin();
  bool configure(const NetworkConfig& c) { return validNetworkConfig(c) && netCommands_ && xQueueOverwrite(netCommands_,&c)==pdTRUE; }
  void publish(const HostSnapshot& s) { if(snapshots_) xQueueOverwrite(snapshots_,&s); }
  bool receive(HostCommand& c) { return commands_ && xQueueReceive(commands_,&c,0)==pdTRUE; }
  NetworkState network() { NetworkState s; if(network_) xQueuePeek(network_,&s,0); return s; }
};
