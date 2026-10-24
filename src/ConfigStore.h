#pragma once
#include <Preferences.h>
#include "Core.h"
class ConfigStore {
  Preferences prefs_;
  bool open_=false;
  struct Record { uint32_t version=1; Settings values; };
public:
  bool healthy=false;
  Settings settings;
  void begin() {
    open_=prefs_.begin("hcho-proto",false); healthy=open_;
    if(!open_) return;
    if(!prefs_.isKey("settings")) return;
    Record r;
    if(prefs_.getBytesLength("settings")!=sizeof(r) || prefs_.getBytes("settings",&r,sizeof(r))!=sizeof(r)
        || r.version!=1 || !validSettings(r.values)) { healthy=false; return; }
    settings=r.values;
  }
  bool save(const Settings& values) {
    if(!open_ || !validSettings(values)) return false;
    Record r; r.values=values;
    if(prefs_.putBytes("settings",&r,sizeof(r))!=sizeof(r)) { healthy=false; return false; }
    settings=values; healthy=true; return true;
  }
};
