#include <Arduino.h>
#include <Wire.h>
#include "BoardIO.h"
#include "SensorManager.h"
#include "ConfigStore.h"
#include "SelfTest.h"
#include "ModbusRtuServer.h"
#include "RegisterMap.h"
#include "HostServer.h"

BoardIO board;
SensorManager sensor;
ConfigStore config;
CalibrationManager calibration;
ModbusRtuServer modbus;
HostServer host;
AlarmManager alarms;
ProcessState process;
OperatingMode mode=OperatingMode::Test;
bool service=false, acknowledge=false;
uint8_t manualRelays=0;
uint32_t serviceUntil=0;
constexpr uint32_t SERVICE_DURATION_MS=15UL*60UL*1000UL;
char input[160]={};
size_t inputLength=0;
bool inputOverflow=false;
char serviceKey[33]={};
char lastCommand[120]="Noch kein Servicebefehl";

void result(const char* message) {
  strlcpy(lastCommand,message,sizeof(lastCommand));
  Serial.printf("[SYS] %s\n",message);
}

void status() {
  const auto& s=sensor.sample();
  Serial.printf("[SYS] mode=%s service=%u alarm=%u fault=%u ready=%u faults=0x%04X DI=0x%02X relay=0x%02X uptime=%lus\n",
    mode==OperatingMode::Test?"TEST_MODE":"HCHO_MODE",service,process.alarm,process.fault,process.ready,
    process.faults,board.inputs(),board.outputs(),millis()/1000UL);
  Serial.printf("[SENSOR] valid=%u T=%.2f RH=%.2f age=%lums error=%u\n",s.valid,s.temperature,s.humidity,millis()-s.time,s.error);
  auto net=host.network();
  Serial.printf("[HOST] W5500=%u link=%u online=%u IP=%s | [MODBUS] requests=%lu rejected=%lu\n",net.hardware,net.link,net.online,net.ip,(unsigned long)modbus.requests,(unsigned long)modbus.rejected);
  Serial.printf("[MODBUS] TCP port=502 requests=%lu rejected=%lu network=%s\n",(unsigned long)net.tcpRequests,(unsigned long)net.tcpRejected,net.dhcp?"DHCP":"statisch");
}
void handleCommand(const char* text,bool remote=false) {
  if(!strcmp(text,"status")) { status(); return; }
  if(!strcmp(text,"selftest")) { Serial.printf("[SYS] Logik-Selbsttest %s\n",coreSelfTest()?"PASS":"FAIL"); return; }
  if(!strncmp(text,"network ",8)) {
    if(remote) { result("Netzkonfiguration nur ueber USB erlaubt"); return; }
    NetworkConfig next; char ip[16]={},mask[16]={},gateway[16]={},tail;
    if(!strcmp(text,"network dhcp")) next.dhcp=1;
    else if(sscanf(text,"network static %15s %15s %15s %c",ip,mask,gateway,&tail)==3 &&
        parseIpv4(ip,next.ip) && parseIpv4(mask,next.mask) && parseIpv4(gateway,next.gateway)) next.dhcp=0;
    else { result("Syntax: network dhcp | network static IP MASKE GATEWAY"); return; }
    result(host.configure(next)?"Netzkonfiguration angefordert; Ergebnis im HOST-Log":"Ungueltige Netzkonfiguration"); return;
  }
  if(!strcmp(text,"service on")) {
    if(remote) { result("Service nur am USB-Terminal oeffnen oder verlaengern"); return; }
    service=true; manualRelays=0; serviceUntil=millis()+SERVICE_DURATION_MS;
    snprintf(serviceKey,sizeof(serviceKey),"%08lx%08lx%08lx%08lx",(unsigned long)esp_random(),(unsigned long)esp_random(),(unsigned long)esp_random(),(unsigned long)esp_random());
    result("Service aktiv fuer 15 Minuten; manuelle Relaismaske AUS");
    Serial.printf("[HOST] Serviceschluessel: %s\n",serviceKey); return;
  }
  if(!strcmp(text,"service off")) { service=false; manualRelays=0; calibration.cancel(); serviceKey[0]=0; result("Automatik aktiv"); return; }
  if(!strcmp(text,"ack")) { acknowledge=true; return; }
  if(!strcmp(text,"help")) {
    Serial.println("[SYS] status | selftest | registers | service on/off | relay 1..8 on/off | limits Tmin Tmax RHmin RHmax | hysteresis T RH | latch on/off | mode test/hcho | cal zero/span/reset/confirm | ack");
    Serial.println("[HOST] network dhcp | network static IP MASKE GATEWAY (nur USB, ohne Relais-Service)"); return;
  }
  if(!strcmp(text,"registers")) { for(uint8_t i=0;i<64;i++) Serial.printf("[MODBUS] %u=0x%04X\n",40001+i,modbus.registers[i]); return; }
  if(!service) { result("Befehl nur im Servicebetrieb erlaubt"); return; }
  if(!strcmp(text,"cal zero") || !strcmp(text,"cal span") || !strcmp(text,"cal reset")) {
    uint8_t kind=!strcmp(text,"cal zero")?1:!strcmp(text,"cal span")?2:3;
    result(calibration.propose(kind,sensor.sample(),mode,service,millis())?"Kalibrierung vorgemerkt; cal confirm erforderlich":"Kalibrierung abgelehnt: gueltiger HCHO-Sensor erforderlich");
    return;
  }
  if(!strcmp(text,"cal confirm")) { result(calibration.confirm(sensor.sample(),mode,service,millis())?"Kalibrierung gespeichert":"Kalibrierung abgelehnt"); return; }
  unsigned number; char state[8]={}, trailing=0;
  if(sscanf(text,"relay %u %7s %c",&number,state,&trailing)==2 && number>=1 && number<=8 &&
      (!strcmp(state,"on") || !strcmp(state,"off"))) {
    uint8_t bit=1<<(number-1);
    if(!strcmp(state,"on")) manualRelays|=bit; else manualRelays&=~bit;
    Serial.printf("[RELAY] Serviceanforderung=0x%02X\n",manualRelays); result("Relaisanforderung angenommen"); return;
  }
  Settings next=config.settings;
  if(sscanf(text,"limits %f %f %f %f %c",&next.tMin,&next.tMax,&next.rhMin,&next.rhMax,&trailing)==4) {
    result(config.save(next)?"Grenzwerte gespeichert":"Grenzwerte abgelehnt"); return;
  }
  if(sscanf(text,"hysteresis %f %f %c",&next.tHysteresis,&next.rhHysteresis,&trailing)==2) { result(config.save(next)?"Hysterese gespeichert":"Hysterese abgelehnt"); return; }
  if(!strcmp(text,"latch on") || !strcmp(text,"latch off")) { next.latchAlarm=!strcmp(text,"latch on"); result(config.save(next)?"Ruecksetzstrategie gespeichert":"Speichern fehlgeschlagen"); return; }
  if(!strcmp(text,"mode test")) { mode=OperatingMode::Test; calibration.cancel(); result("TEST_MODE"); return; }
  if(!strcmp(text,"mode hcho")) { mode=OperatingMode::Hcho; result("HCHO_MODE: SFA40 fehlt; Stoerung aktiv"); return; }
  result("Unbekannter Befehl; help");
}
void serialService() {
  unsigned budget=64;
  while(budget-- && Serial.available()) {
    char c=Serial.read();
    if(c=='\r') continue;
    if(c=='\n') {
      input[inputLength]=0;
      if(inputOverflow) Serial.println("[SYS] Befehl zu lang");
      else if(inputLength) handleCommand(input);
      inputLength=0; inputOverflow=false;
    } else if(inputLength<sizeof(input)-1 && !inputOverflow) input[inputLength++]=c;
    else inputOverflow=true;
  }
}
void setup() {
  Serial.begin(115200);
  Wire.begin(Pins::SDA,Pins::SCL); Wire.setClock(100000); Wire.setTimeOut(50);
  config.begin(); calibration.begin(); board.begin(); sensor.begin(); modbus.begin();
  if(!host.begin()) Serial.println("[HOST] Task konnte nicht gestartet werden; lokale Steuerung laeuft weiter");
  Serial.println("[SYS] ESP_Klima TEST_MODE; R1=Alarm R2=Stoerung R3=Bereit");
  Serial.printf("[SYS] Logik-Selbsttest %s\n",coreSelfTest()?"PASS":"FAIL");
}
void loop() {
  uint32_t now=millis();
  if(service && int32_t(now-serviceUntil)>=0) { service=false; manualRelays=0; serviceKey[0]=0; result("Servicezeit abgelaufen"); }
  serialService();
  HostCommand hostCommand;
  if(host.receive(hostCommand)) {
    if(service && !strcmp(hostCommand.key,serviceKey)) handleCommand(hostCommand.text,true);
    else result("Web-Befehl abgelehnt: Service inzwischen geschlossen");
  }
  calibration.update(now,service);
  sensor.update(now);
  process=alarms.update(sensor.sample(),config.settings,mode,service,board.healthy(),config.healthy && calibration.healthy,now,acknowledge);
  acknowledge=false;
  board.request(service?manualRelays:automaticRelays(process));
  board.update(now);
  uint8_t held=board.takeLongPress();
  if(held&3) {
    if((held&3)==3 || !calibration.propose((held&1)?1:2,sensor.sample(),mode,service,now))
      Serial.println("[CAL] Langdruck abgelehnt: Service/HCHO-Sensor pruefen");
  }
  Registers::fill(modbus.registers,sensor.sample(),config.settings,process,mode,service,calibration,
    board.inputs(),board.outputs(),board.healthy(),modbus.requests,now);
  modbus.update();
  static uint32_t published=0;
  if(uint32_t(now-published)>=200) {
    published=now; HostSnapshot snapshot;
    memcpy(snapshot.registers,modbus.registers,sizeof(snapshot.registers)); snapshot.publishedAt=now;
    snapshot.sample=sensor.sample(); snapshot.settings=config.settings; snapshot.process=process;
    snapshot.mode=mode; snapshot.service=service; snapshot.calibration=calibration.data.active;
    snapshot.calPending=calibration.pending(); snapshot.relayHealthy=board.healthy();
    snapshot.di=board.inputs(); snapshot.relays=board.outputs(); snapshot.uptime=now/1000;
    snapshot.requests=modbus.requests; snapshot.rejected=modbus.rejected; snapshot.lastRequest=modbus.lastRequest;
    snapshot.serviceRemaining=service?(serviceUntil-now)/1000:0;
    strlcpy(snapshot.key,serviceKey,sizeof(snapshot.key)); strlcpy(snapshot.lastCommand,lastCommand,sizeof(snapshot.lastCommand));
    host.publish(snapshot);
  }
  static uint16_t oldFlags=0xffff;
  uint16_t flags=(process.alarm?1:0)|(process.fault?2:0)|(process.ready?4:0)|(service?8:0);
  if(flags!=oldFlags) { oldFlags=flags; status(); }
  delay(1);
}
