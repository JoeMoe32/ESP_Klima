#include "HostServer.h"
#include <SPI.h>
#include <Ethernet.h>
#include "BoardIO.h"
#include "WebPage.h"
#include "ModbusTcpServer.h"
#include <Preferences.h>

bool HostServer::begin() {
  snapshots_=xQueueCreate(1,sizeof(HostSnapshot)); commands_=xQueueCreate(4,sizeof(HostCommand)); network_=xQueueCreate(1,sizeof(NetworkState));
  netCommands_=xQueueCreate(1,sizeof(NetworkConfig));
  if(!snapshots_ || !commands_ || !network_ || !netCommands_) return false;
  return xTaskCreatePinnedToCore(task,"ethernet-host",12288,this,1,nullptr,0)==pdPASS;
}
void HostServer::task(void* context) { static_cast<HostServer*>(context)->run(); }
static String number(float value,bool valid) { return valid && isfinite(value)?String(value,2):String("null"); }
static String json(const HostSnapshot& s,const NetworkState& net,bool authorized) {
  bool valid=s.sample.valid && uint32_t(millis()-s.sample.time)<=15000;
  bool hcho=valid && s.sample.hchoValid && s.mode==OperatingMode::Hcho;
  String out; out.reserve(1600);
  out="{\"mode\":\""; out+=s.mode==OperatingMode::Test?"TEST_MODE":"HCHO_MODE";
  out+="\",\"temperature\":"+number(s.sample.temperature,valid)+",\"humidity\":"+number(s.sample.humidity,valid);
  out+=",\"hcho\":"+number(s.sample.correctedHcho,hcho)+",\"hchoRaw\":"+number(s.sample.rawHcho,hcho);
  char fields[850];
  snprintf(fields,sizeof(fields),",\"alarm\":%s,\"fault\":%s,\"ready\":%s,\"service\":%s,\"calibration\":%s,\"calPending\":%s,\"relayHealthy\":%s,\"di\":%u,\"relays\":%u,\"faults\":%u,\"sensorError\":%u,\"uptime\":%lu,\"modbusRequests\":%lu,\"modbusRejected\":%lu,\"serviceRemaining\":%lu,\"tmin\":%.2f,\"tmax\":%.2f,\"rhmin\":%.2f,\"rhmax\":%.2f,\"thyst\":%.2f,\"rhhyst\":%.2f,\"latch\":%s,\"ip\":\"%s\",\"lastCommand\":\"",
    s.process.alarm?"true":"false",s.process.fault?"true":"false",s.process.ready?"true":"false",s.service?"true":"false",s.calibration?"true":"false",s.calPending?"true":"false",s.relayHealthy?"true":"false",s.di,s.relays,s.process.faults,s.sample.error,
    (unsigned long)s.uptime,(unsigned long)s.requests,(unsigned long)s.rejected,(unsigned long)s.serviceRemaining,
    s.settings.tMin,s.settings.tMax,s.settings.rhMin,s.settings.rhMax,s.settings.tHysteresis,s.settings.rhHysteresis,s.settings.latchAlarm?"true":"false",net.ip);
  out+=fields;
  for(const char* p=s.lastCommand;*p;p++) { if(*p=='"' || *p=='\\') out+='\\'; if(uint8_t(*p)>=32) out+=*p; }
  out+="\",\"tcpRequests\":"+String(net.tcpRequests)+",\"tcpRejected\":"+String(net.tcpRejected);
  out+=",\"authorized\":"; out+=authorized?"true":"false";
  out+=" ,\"dhcp\":"; out+=net.dhcp?"true":"false"; out+="}"; return out;
}
static bool sendBytes(EthernetClient& c,const char* data,size_t size,uint32_t started) {
  // Ethernet 2.0.2 silently truncates a single write above the W5500 TX buffer.
  while(size && c.connected() && uint32_t(millis()-started)<4000) {
    size_t chunk=size<512?size:512;
    if(c.availableForWrite()<int(chunk)) { vTaskDelay(pdMS_TO_TICKS(1)); continue; }
    if(c.write(reinterpret_cast<const uint8_t*>(data),chunk)!=chunk) return false;
    data+=chunk; size-=chunk;
  }
  return size==0;
}
static void respond(EthernetClient& c,int code,const char* type,const char* body) {
  char header[256];
  int n=snprintf(header,sizeof(header),"HTTP/1.1 %d %s\r\nConnection: close\r\nCache-Control: no-store\r\nX-Content-Type-Options: nosniff\r\nContent-Type: %s\r\nContent-Length: %u\r\n\r\n",
    code,code==200?"OK":code==202?"Accepted":"Error",type,unsigned(strlen(body)));
  uint32_t started=millis();
  if(n>0 && n<int(sizeof(header)) && sendBytes(c,header,n,started)) sendBytes(c,body,strlen(body),started);
  c.stop();
}
void HostServer::run() {
  SPI.begin(Pins::SCLK,Pins::MISO,Pins::MOSI,Pins::CS); Ethernet.init(Pins::CS);
  uint64_t chip=ESP.getEfuseMac(); uint8_t mac[6];
  for(uint8_t i=0;i<6;i++) mac[i]=chip>>(8*i);
  mac[0]=(mac[0]|2)&0xfe;
  FixedPortEthernetServer server(80); EthernetClient client;
  ModbusTcpServer tcp;
  HostSnapshot snapshot; NetworkState net;
  Preferences prefs; NetworkConfig config;
  bool storeOpen=prefs.begin("hcho-net",false);
  if(storeOpen && prefs.isKey("config")) {
    if(prefs.getBytesLength("config")!=sizeof(config) || prefs.getBytes("config",&config,sizeof(config))!=sizeof(config) || !validNetworkConfig(config)) {
      config=NetworkConfig{}; Serial.println("[HOST] Ungueltige Netzkonfiguration; DHCP verwendet");
    }
  }
  net.dhcp=config.dhcp;
  char request[1200]={}; size_t used=0, headerEnd=0, bodySize=0;
  uint32_t attempt=millis()-30000, connectedAt=0, maintained=0;
  for(;;) {
    xQueuePeek(snapshots_,&snapshot,0);
    NetworkConfig requested;
    if(xQueueReceive(netCommands_,&requested,0)==pdTRUE) {
      if(validNetworkConfig(requested) && storeOpen && prefs.putBytes("config",&requested,sizeof(requested))==sizeof(requested)) {
        config=requested; net.dhcp=config.dhcp; client.stop(); tcp.stop(); net.online=false;
        strlcpy(net.ip,"0.0.0.0",sizeof(net.ip)); attempt=millis()-30000;
        Serial.println("[HOST] Netzkonfiguration gespeichert; Verbindung wird neu aufgebaut");
      } else Serial.println("[HOST] Netzkonfiguration konnte nicht gespeichert werden");
    }
    if(net.hardware) {
      bool link=Ethernet.linkStatus()==LinkON;
      if(link && !net.link) attempt=millis()-30000;
      if(!link && net.online) { net.online=false; client.stop(); tcp.stop(); }
      net.link=link;
    }
    if(!net.online && uint32_t(millis()-attempt)>=30000) {
      attempt=millis();
      int ok=1;
      if(config.dhcp) ok=Ethernet.begin(mac,3000,750);
      else Ethernet.begin(mac,IPAddress(config.ip),IPAddress(0,0,0,0),IPAddress(config.gateway),IPAddress(config.mask));
      Ethernet.setRetransmissionTimeout(200); Ethernet.setRetransmissionCount(2);
      net.hardware=Ethernet.hardwareStatus()==EthernetW5500;
      net.link=Ethernet.linkStatus()==LinkON; net.online=ok && net.link && net.hardware;
      if(net.online) {
        auto ip=Ethernet.localIP(); snprintf(net.ip,sizeof(net.ip),"%u.%u.%u.%u",ip[0],ip[1],ip[2],ip[3]);
        server.begin(); tcp.begin();
      }
      Serial.printf("[HOST] W5500=%u link=%u online=%u IP=%s %s; HTTP=80 ModbusTCP=502\n",net.hardware,net.link,net.online,net.ip,config.dhcp?"DHCP":"statisch");
    }
    if(net.online) {
      if(config.dhcp && uint32_t(millis()-maintained)>1000) {
        maintained=millis(); int result=Ethernet.maintain();
        if(result==1 || result==3) { net.online=false; client.stop(); tcp.stop(); }
        else if(result==2 || result==4) {
          auto ip=Ethernet.localIP(); snprintf(net.ip,sizeof(net.ip),"%u.%u.%u.%u",ip[0],ip[1],ip[2],ip[3]);
        }
      }
      if(!net.online) { xQueueOverwrite(network_,&net); vTaskDelay(pdMS_TO_TICKS(5)); continue; }
      tcp.update(snapshot.registers,snapshot.publishedAt && uint32_t(millis()-snapshot.publishedAt)<=2000);
      if(!client) { client=server.accept(); if(client) { client.setConnectionTimeout(100); used=0; headerEnd=0; bodySize=0; connectedAt=millis(); } }
      unsigned budget=256;
      while(client && client.available() && budget--) {
        if(used>=sizeof(request)-1) { respond(client,413,"text/plain","Anfrage zu gross"); break; }
        request[used++]=client.read(); request[used]=0;
        if(!headerEnd && used>=4 && !memcmp(request+used-4,"\r\n\r\n",4)) {
          headerEnd=used;
          // Header names are case insensitive; request body remains untouched.
          String headers(request); String lower=headers; lower.toLowerCase();
          int cl=lower.indexOf("\r\ncontent-length:");
          if(cl>=0) {
            int end=lower.indexOf("\r\n",cl+2); String value=lower.substring(cl+17,end); value.trim();
            bool numeric=value.length()>0;
            for(unsigned i=0;i<value.length();i++) if(value[i]<'0'||value[i]>'9') numeric=false;
            if(!numeric || value.length()>3 || value.toInt()>=160) { respond(client,413,"text/plain","Ungueltige Befehlslaenge"); break; }
            bodySize=value.toInt();
          }
          if(lower.indexOf("\r\ntransfer-encoding:")>=0) { respond(client,400,"text/plain","Transfer-Encoding nicht unterstuetzt"); break; }
        }
        if(headerEnd && used>=headerEnd+bodySize) {
          char method[8]={},path[64]={}; sscanf(request,"%7s %63s",method,path);
          String headers=String(request).substring(0,headerEnd); String lower=headers; lower.toLowerCase();
          int pos=lower.indexOf("\r\nx-service-key:"); String key;
          if(pos>=0) { int end=lower.indexOf("\r\n",pos+2); key=headers.substring(pos+16,end); key.trim(); }
          bool fresh=snapshot.publishedAt && uint32_t(millis()-snapshot.publishedAt)<=2000;
          bool authorized=snapshot.service && fresh && snapshot.key[0] && key==snapshot.key;
          if(!strcmp(method,"GET") && !strcmp(path,"/")) respond(client,200,"text/html; charset=utf-8",WEB_PAGE);
          else if(!strcmp(method,"GET") && !strcmp(path,"/api/status")) { String result=json(snapshot,net,authorized); respond(client,200,"application/json",result.c_str()); }
          else if(!strcmp(method,"POST") && !strcmp(path,"/api/service/unlock")) {
            // Validate only: no output changes and no extension of the USB service window.
            if(authorized) respond(client,200,"application/json","{\"authorized\":true}");
            else respond(client,403,"text/plain","Serviceschluessel ungueltig oder Service abgelaufen.");
          }
          else if(!strcmp(method,"POST") && !strcmp(path,"/api/command")) {
            if(!authorized) respond(client,403,"text/plain","Service geschlossen oder Schluessel ungueltig");
            else {
              HostCommand command; memcpy(command.text,request+headerEnd,bodySize); command.text[bodySize]=0;
              strlcpy(command.key,snapshot.key,sizeof(command.key));
              if(!bodySize || strchr(command.text,'\n') || strchr(command.text,'\r')) respond(client,400,"text/plain","Ungueltiger Befehl");
              else if(xQueueSend(commands_,&command,0)!=pdTRUE) respond(client,503,"text/plain","Beschaeftigt");
              else respond(client,202,"text/plain","Befehl angenommen. Ergebnis im Status und USB-Log.");
            }
          } else respond(client,404,"text/plain","Nicht gefunden");
          break;
        }
      }
      if(client && uint32_t(millis()-connectedAt)>4000) client.stop();
    }
    net.tcpRequests=tcp.requests; net.tcpRejected=tcp.rejected;
    xQueueOverwrite(network_,&net);
    vTaskDelay(pdMS_TO_TICKS(5));
  }
}
