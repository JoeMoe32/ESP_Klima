#pragma once
#include <stdint.h>
#include <stddef.h>
namespace ModbusProtocol {
inline uint16_t crc(const uint8_t* bytes,size_t size) {
  uint16_t result=0xffff;
  for(size_t i=0;i<size;i++) {
    result^=bytes[i];
    for(uint8_t b=0;b<8;b++) result=(result&1)?(result>>1)^0xa001:result>>1;
  }
  return result;
}
inline size_t appendCrc(uint8_t* bytes,size_t size) {
  uint16_t c=crc(bytes,size); bytes[size++]=uint8_t(c); bytes[size++]=uint8_t(c>>8); return size;
}
// Shared read-only PDU for RTU and TCP. Transport headers are handled separately.
inline size_t replyPdu(const uint8_t* request,size_t length,const uint16_t* registers,
    size_t registerCount,uint8_t* response,size_t capacity) {
  if(!length || capacity<2) return 0;
  uint8_t error=0;
  uint16_t first=0,count=0;
  if(request[0]!=3 && request[0]!=4) error=1;
  else if(length!=5) error=3;
  else {
    first=(uint16_t(request[1])<<8)|request[2]; count=(uint16_t(request[3])<<8)|request[4];
    if(count<1 || count>125) error=3;
    else if(uint32_t(first)+count>registerCount) error=2;
  }
  response[0]=request[0];
  if(error) { response[0]|=0x80; response[1]=error; return 2; }
  if(capacity<2+size_t(count)*2) return 0;
  response[1]=count*2;
  for(uint16_t i=0;i<count;i++) { response[2+i*2]=uint8_t(registers[first+i]>>8); response[3+i*2]=uint8_t(registers[first+i]); }
  return 2+count*2;
}
// Invalid/broadcast/foreign RTU frames have no response.
inline size_t reply(const uint8_t* request,size_t length,const uint16_t* registers,
    size_t registerCount,uint8_t* response,size_t capacity) {
  if(length<4 || request[0]!=1 || crc(request,length)!=0 || capacity<5) return 0;
  size_t n=replyPdu(request+1,length-3,registers,registerCount,response+1,capacity-3);
  if(!n) return 0;
  response[0]=1;
  return appendCrc(response,n+1);
}
// MBAP length includes unit id + PDU. 0=incomplete header, -1=invalid header.
inline int tcpFrameLength(const uint8_t* request,size_t length) {
  if(length<6) return 0;
  uint16_t payload=(uint16_t(request[4])<<8)|request[5];
  if(request[2] || request[3] || payload<2 || payload>254) return -1;
  return 6+payload;
}
inline size_t replyTcp(const uint8_t* request,size_t length,const uint16_t* registers,
    size_t registerCount,uint8_t* response,size_t capacity,bool fresh=true) {
  if(length<8 || tcpFrameLength(request,length)!=int(length) || capacity<9) return 0;
  // Direct server, not a serial gateway. Support configured id 1 and TCP id 255.
  if(request[6]!=1 && request[6]!=255) return 0;
  size_t n;
  if(!fresh) { response[7]=request[7]|0x80; response[8]=4; n=2; }
  else n=replyPdu(request+7,length-7,registers,registerCount,response+7,capacity-7);
  if(!n) return 0;
  response[0]=request[0]; response[1]=request[1]; response[2]=0; response[3]=0;
  response[4]=uint8_t((n+1)>>8); response[5]=uint8_t(n+1); response[6]=request[6];
  return 7+n;
}
}
