#pragma once
#include <stdint.h>
#include <stdio.h>

struct NetworkConfig {
  uint32_t version=1;
  uint8_t dhcp=1;
  uint8_t ip[4]={192,168,77,2};
  uint8_t mask[4]={255,255,255,0};
  uint8_t gateway[4]={0,0,0,0};
};
inline uint32_t ipv4Number(const uint8_t* ip) {
  return (uint32_t(ip[0])<<24)|(uint32_t(ip[1])<<16)|(uint32_t(ip[2])<<8)|ip[3];
}
inline bool parseIpv4(const char* text,uint8_t* out) {
  unsigned a,b,c,d; char tail;
  if(sscanf(text,"%u.%u.%u.%u%c",&a,&b,&c,&d,&tail)!=4 || a>255 || b>255 || c>255 || d>255) return false;
  out[0]=a; out[1]=b; out[2]=c; out[3]=d; return true;
}
inline bool validNetworkConfig(const NetworkConfig& c) {
  if(c.version!=1 || c.dhcp>1) return false;
  if(c.dhcp) return true;
  uint32_t ip=ipv4Number(c.ip), mask=ipv4Number(c.mask), gateway=ipv4Number(c.gateway), hostMask=~mask;
  if(!mask || hostMask<3 || (hostMask & (hostMask+1))) return false;
  if(!c.ip[0] || c.ip[0]==127 || c.ip[0]>=224 || !(ip&hostMask) || (ip&hostMask)==hostMask) return false;
  return !gateway || (gateway!=ip && (gateway&mask)==(ip&mask) && (gateway&hostMask) && (gateway&hostMask)!=hostMask);
}
