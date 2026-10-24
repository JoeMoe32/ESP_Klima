#pragma once
#include "Core.h"
#include "ModbusProtocol.h"
#include "CalibrationManager.h"
#include "NetworkConfig.h"
inline bool coreSelfTest() {
  Settings cfg;
  if(!validSettings(cfg)) return false;
  if(rangeAlarm(24,15,23,0.3f,0)!=1 || rangeAlarm(22.9f,15,23,0.3f,1)!=1
      || rangeAlarm(22.6f,15,23,0.3f,1)!=0) return false;
  AlarmManager alarms;
  Sample sample; sample.valid=true; sample.time=100; sample.temperature=20; sample.humidity=40;
  auto s=alarms.update(sample,cfg,OperatingMode::Test,false,true,true,100);
  if(!s.ready || s.alarm || s.fault || automaticRelays(s)!=4) return false;
  s=alarms.update(sample,cfg,OperatingMode::Test,false,true,true,15101);
  if(!s.fault || s.ready || !(s.faults&SensorStale)) return false;
  s=alarms.update(sample,cfg,OperatingMode::Hcho,false,true,true,100);
  if(!s.fault || !(s.faults&HchoUnavailable)) return false;
  cfg.latchAlarm=true; sample.temperature=24;
  s=alarms.update(sample,cfg,OperatingMode::Test,false,true,true,100);
  if(!s.alarm) return false;
  sample.temperature=20;
  s=alarms.update(sample,cfg,OperatingMode::Test,false,true,true,100);
  if(!s.alarm) return false;
  s=alarms.update(sample,cfg,OperatingMode::Test,false,true,true,100,true);
  if(s.alarm) return false;
  sample.time=0xfffffff0U;
  s=alarms.update(sample,cfg,OperatingMode::Test,false,true,true,0x10);
  if(!s.ready) return false;
  Calibration cal; cal.haveZero=true; cal.active=true; cal.zeroRaw=10; cal.spanRaw=310;
  if(correctHcho(10,cal)!=0 || correctHcho(310,cal)!=300 || correctHcho(160,cal)!=150) return false;
  cal.spanRaw=cal.zeroRaw;
  if(validCalibration(cal)) return false;
  uint16_t regs[64]={}; regs[9]=2300;
  uint8_t request[8]={1,3,0,9,0,1,0,0}, response[256]={};
  ModbusProtocol::appendCrc(request,6);
  auto n=ModbusProtocol::reply(request,8,regs,64,response,sizeof(response));
  if(n!=7 || response[2]!=2 || response[3]!=8 || response[4]!=252 || ModbusProtocol::crc(response,n)!=0) return false;
  request[0]=0; ModbusProtocol::appendCrc(request,6);
  if(ModbusProtocol::reply(request,8,regs,64,response,sizeof(response))) return false;
  request[0]=1; request[3]=63; request[5]=2; ModbusProtocol::appendCrc(request,6);
  if(ModbusProtocol::reply(request,8,regs,64,response,sizeof(response))!=5 || response[2]!=2) return false;
  request[3]=0; request[5]=0; ModbusProtocol::appendCrc(request,6);
  if(ModbusProtocol::reply(request,8,regs,64,response,sizeof(response))!=5 || response[2]!=3) return false;
  request[1]=6; ModbusProtocol::appendCrc(request,6);
  if(ModbusProtocol::reply(request,8,regs,64,response,sizeof(response))!=5 || response[2]!=1) return false;
  request[7]^=1;
  if(ModbusProtocol::reply(request,8,regs,64,response,sizeof(response))!=0) return false;
  uint8_t tcp[12]={0x12,0x34,0,0,0,6,1,3,0,9,0,1};
  n=ModbusProtocol::replyTcp(tcp,sizeof(tcp),regs,64,response,sizeof(response));
  if(n!=11 || response[0]!=0x12 || response[1]!=0x34 || response[5]!=5 || response[6]!=1 || response[9]!=8 || response[10]!=252) return false;
  tcp[6]=255;
  if(ModbusProtocol::replyTcp(tcp,12,regs,64,response,sizeof(response))!=11 || response[6]!=255) return false;
  if(ModbusProtocol::replyTcp(tcp,12,regs,64,response,sizeof(response),false)!=9 || response[8]!=4) return false;
  tcp[6]=2;
  if(ModbusProtocol::replyTcp(tcp,12,regs,64,response,sizeof(response))) return false;
  tcp[6]=1; tcp[3]=1;
  if(ModbusProtocol::tcpFrameLength(tcp,6)!=-1 || ModbusProtocol::replyTcp(tcp,12,regs,64,response,sizeof(response))) return false;
  tcp[3]=0; tcp[4]=1; tcp[5]=0;
  if(ModbusProtocol::tcpFrameLength(tcp,6)!=-1 || ModbusProtocol::tcpFrameLength(tcp,5)!=0) return false;
  NetworkConfig net; net.dhcp=0;
  if(!validNetworkConfig(net)) return false;
  net.ip[3]=0; if(validNetworkConfig(net)) return false;
  net.ip[3]=2; net.mask[1]=254; if(validNetworkConfig(net)) return false;
  return !parseIpv4("192.168.77.256",net.ip) && parseIpv4("192.168.77.2",net.ip);
}
