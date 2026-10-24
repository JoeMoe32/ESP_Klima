#pragma once
#include <Arduino.h>
static const char WEB_PAGE[] PROGMEM = R"HTML(<!doctype html>
<html lang="de"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Waveshare Sensorstation</title><style>
:root{color-scheme:light;font:16px system-ui;color:#163d42;background:#eef4f3}*{box-sizing:border-box}body{margin:0}main{max-width:1020px;margin:auto;padding:28px 22px}h1{font-size:30px;margin:8px 0}h2{font-size:19px}p{line-height:1.5}header{border-bottom:1px solid #c4d8d6;padding-bottom:20px}.eyebrow{font-size:12px;letter-spacing:2px;text-transform:uppercase}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:16px;margin:20px 0}.card,section{background:white;border:1px solid #cee0dd;border-radius:14px;padding:20px;margin-bottom:16px}.value{font-size:36px;font-weight:650;margin:12px 0}small{color:#536d70}.badge{display:inline-block;padding:6px 12px;background:#e2f2ed;border-radius:7px;margin:4px}.warn{background:#ffe2c3}.bad{background:#f9d4d1}button,input,select{font:inherit;border:1px solid #9bbcb7;border-radius:7px;padding:9px;margin:4px}button{background:#165e58;color:white;cursor:pointer}button:disabled{opacity:.5;cursor:default}label{display:inline-block;margin:5px}input[type=number]{width:100px}input[type=password]{width:min(330px,100%)}.io{display:flex;flex-wrap:wrap;gap:7px}.channel{border:1px solid #d0dfdc;border-radius:8px;padding:10px;min-width:80px}.on{background:#d4f0e4}.notice{border-left:4px solid #df9f44;padding-left:14px}#message{min-height:25px;white-space:pre-wrap}details{margin-top:12px}footer{color:#536d70;font-size:13px}</style>
<main><header><div class="eyebrow">Waveshare · ESP32-S3 · lokaler Prototyp</div><h1>Sensorstation</h1><span id="mode" class="badge">Verbindung wird aufgebaut</span><span id="connection"></span></header>
<p class="notice">TEST_MODE verwendet Temperatur und Feuchte als Testsignal. HCHO ist erst mit integriertem und geprüftem SFA40 verfügbar.</p>
<div class="grid"><div class="card">Temperatur<div class="value" id="temperature">—</div><small>Testsignal</small></div><div class="card">Relative Feuchte<div class="value" id="humidity">—</div><small>Testsignal</small></div><div class="card">Formaldehyd<div class="value" id="hcho">—</div><small id="hchoRaw">Noch keine gültige HCHO-Messung</small></div></div>
<section><h2>Betriebszustand</h2><div id="states"></div><p id="diagnostics"></p><p id="network"></p></section>
<section><h2>Digitale Eingänge</h2><div class="io" id="di"></div><small>DI1: ZERO · DI2: SPAN · DI3–8: Reserve</small></section>
<section><h2>Relais</h2><div class="io" id="relays"></div><p><small>R1: Alarm · R2: Störung · R3: Bereit · R4–8: Reserve. Anzeige des bestätigten Ausgangsregisters; keine Kontakt-Rückmeldung.</small></p></section>
<style>
[hidden]{display:none!important}
.service-access{display:flex;align-items:center;flex-wrap:wrap;gap:8px}
#serviceLogin{display:flex;align-items:center;flex-wrap:wrap;margin:0}
#serviceSend,.service-indicator{min-width:90px;min-height:42px;font:inherit;line-height:22px;padding:9px 14px;margin:4px;border:1px solid;border-radius:7px;text-align:center}
#serviceSend{border-color:#165e58}.service-indicator{display:inline-block;background:#f6cc45;border-color:#d4a719;color:#423300;font-weight:600}
#serviceMessage{min-height:24px;margin:8px 4px;color:#536d70}#serviceMessage.error{color:#9b2c20}
</style>
<section><h2>Service</h2><p>Service am USB-Terminal mit <code>service on</code> öffnen. Schlüssel eingeben und <strong>Senden</strong> drücken. Nach 15 Minuten endet der Service automatisch.</p>
<div class="service-access"><form id="serviceLogin" onsubmit="unlockService(event)"><input id="key" type="password" autocomplete="off" aria-label="Serviceschlüssel" placeholder="Serviceschlüssel" required><button id="serviceSend" type="submit" disabled>Senden</button></form><span id="serviceIndicator" class="service-indicator" role="status" hidden>Service</span><span id="remaining"></span></div>
<p id="serviceMessage" role="status" aria-live="polite"></p>
<p>Manuelle Tests setzen die Relaisautomatik während des Servicebetriebs aus.</p><div><label>Relais <select id="relayNumber"></select></label><button class="action" onclick="sendServiceCommand('relay '+el('relayNumber').value+' on')">Einschalten</button><button class="action" onclick="sendServiceCommand('relay '+el('relayNumber').value+' off')">Ausschalten</button></div>
<h2>Testgrenzen</h2><label>Temperatur min <input id="tmin" type="number" step="0.1"></label><label>max <input id="tmax" type="number" step="0.1"></label><label>Feuchte min <input id="rhmin" type="number" step="0.1"></label><label>max <input id="rhmax" type="number" step="0.1"></label><button class="action" onclick="sendServiceCommand('limits '+['tmin','tmax','rhmin','rhmax'].map(x=>el(x).value).join(' '))">Speichern</button>
<details><summary>Hysterese und Rücksetzen</summary><label>Temperatur <input id="thyst" type="number" step="0.1"></label><label>Feuchte <input id="rhhyst" type="number" step="0.1"></label><button class="action" onclick="sendServiceCommand('hysteresis '+el('thyst').value+' '+el('rhhyst').value)">Hysterese speichern</button><button class="action" onclick="sendServiceCommand('latch on')">Alarm speichern</button><button class="action" onclick="sendServiceCommand('latch off')">Automatisch zurücksetzen</button><button class="action" onclick="sendServiceCommand('ack')">Alarm quittieren</button></details>
<details><summary>HCHO und Kalibrierung</summary><p>Ohne SFA40 führt HCHO_MODE zu Störung und Bereit=AUS. Kalibrieraktionen werden ohne gültige HCHO-Daten abgelehnt.</p><button class="action" onclick="sendServiceCommand('mode test')">TEST_MODE</button><button class="action" onclick="sendServiceCommand('mode hcho')">HCHO_MODE</button><button class="action" onclick="sendServiceCommand('cal zero')">ZERO vormerken</button><button class="action" onclick="sendServiceCommand('cal span')">SPAN 300 vormerken</button><button class="action" onclick="sendServiceCommand('cal confirm')">Kalibrierung bestätigen</button><button class="action" onclick="sendServiceCommand('cal reset')">Reset vormerken</button></details>
<p><button class="action" onclick="sendServiceCommand('service off')">Service beenden</button></p><div id="message" role="status"></div><small id="lastCommand"></small></section><footer>Lokale Alarmsteuerung läuft unabhängig von Ethernet und Browser weiter.</footer></main>
<script>
const el=id=>document.getElementById(id);
let initial=true,online=false,serviceOpen=false,unlocked=false,checking=false,serviceKey='';
function serviceMessage(text,error=false){el('serviceMessage').textContent=text;el('serviceMessage').classList.toggle('error',error)}
function renderService(){
  const active=online&&serviceOpen&&unlocked;
  el('serviceLogin').hidden=active;el('serviceIndicator').hidden=!active;
  el('serviceSend').disabled=checking||!online||!serviceOpen;
  el('serviceSend').textContent=checking?'Prüfen…':'Senden';
  document.querySelectorAll('.action').forEach(b=>b.disabled=!active);
}
function lockService(){unlocked=false;serviceKey='';renderService()}
async function unlockService(event){
  event.preventDefault();
  const key=el('key').value.trim();
  if(!key){serviceMessage('Bitte den Serviceschlüssel eingeben.',true);return}
  if(!online||!serviceOpen){serviceMessage('Service zuerst über USB öffnen.',true);return}
  checking=true;serviceMessage('Schlüssel wird geprüft…');renderService();
  try{
    const r=await fetch('/api/service/unlock',{method:'POST',headers:{'X-Service-Key':key},signal:AbortSignal.timeout(4000)});
    if(!r.ok){lockService();serviceMessage(r.status===403?'Schlüssel ungültig oder Service abgelaufen.':'Schlüssel konnte nicht geprüft werden.',true);return}
    const s=await r.json();
    if(!s.authorized)throw Error();
    serviceKey=key;unlocked=true;online=true;serviceOpen=true;el('key').value='';
    serviceMessage('Service freigegeben.');
  }catch(e){lockService();serviceMessage('Keine Bestätigung vom ESP. Bitte erneut senden.',true)}
  finally{checking=false;renderService()}
}
for(let n=1;n<=8;n++){let o=document.createElement('option');o.value=n;o.textContent=n;el('relayNumber').append(o)}
function channels(id,mask,prefix){el(id).replaceChildren();for(let i=0;i<8;i++){let d=document.createElement('div');d.className='channel'+((mask>>i&1)?' on':'');d.textContent=prefix+(i+1)+': '+((mask>>i&1)?'EIN':'AUS');el(id).append(d)}}
async function sendServiceCommand(text){
  if(!online||!serviceOpen||!unlocked){el('message').textContent='Zuerst den Serviceschlüssel mit Senden bestätigen.';return}
  try{
    let r=await fetch('/api/command',{method:'POST',headers:{'Content-Type':'text/plain','X-Service-Key':serviceKey},body:text,signal:AbortSignal.timeout(4000)});
    el('message').textContent=await r.text();
    if(r.status===403){lockService();serviceMessage('Service abgelaufen oder Schlüssel nicht mehr gültig.',true)}
    if(r.ok&&text==='service off'){serviceOpen=false;lockService();serviceMessage('Service beendet.')}
  }catch(e){online=false;renderService();el('message').textContent='Befehl nicht übertragen'}
}
async function refresh(){
  const requestedKey=serviceKey;
  try{
    let r=await fetch('/api/status',{cache:'no-store',headers:requestedKey?{'X-Service-Key':requestedKey}:{},signal:AbortSignal.timeout(3000)});
    if(!r.ok)throw Error();let s=await r.json();online=true;serviceOpen=s.service;
    if(!s.service){if(unlocked)serviceMessage('Service beendet. Für eine neue Freigabe Service über USB öffnen.');lockService()}
    else if(requestedKey&&requestedKey===serviceKey){
      unlocked=s.authorized===true;
      if(!unlocked){serviceKey='';serviceMessage('Schlüssel nicht mehr gültig. Bitte erneut senden.',true)}
    }
    el('connection').textContent='Live';el('mode').textContent=s.mode;
    el('temperature').textContent=s.temperature===null?'—':s.temperature.toFixed(2)+' °C';
    el('humidity').textContent=s.humidity===null?'—':s.humidity.toFixed(2)+' %';
    el('hcho').textContent=s.hcho===null?'—':s.hcho.toFixed(1)+' ppb';
    el('hchoRaw').textContent=s.hchoRaw===null?'Keine gültige HCHO-Messung':'Rohwert: '+s.hchoRaw+' ppb';
    el('states').replaceChildren();
    for(let [label,on,cls] of [['Bereit',s.ready,''],['Alarm',s.alarm,'warn'],['Störung',s.fault,'bad'],['Service',s.service,'warn'],['Kalibrierung aktiv',s.calibration,'']]){
      let d=document.createElement('span');d.className='badge '+(on?cls:'');d.textContent=label+': '+(on?'EIN':'AUS');el('states').append(d)
    }
    el('diagnostics').textContent='Laufzeit '+s.uptime+' s · Fehlerbits '+s.faults+' · Sensorfehler '+s.sensorError+' · Modbus-Anfragen '+s.modbusRequests+' · Empfang verworfen '+s.modbusRejected;
    el('network').textContent='Ethernet '+s.ip+' · Relaistreiber '+(s.relayHealthy?'erreichbar':'nicht erreichbar');
    channels('di',s.di,'DI');channels('relays',s.relays,'R');
    el('remaining').textContent=s.service?'Noch '+Math.floor(s.serviceRemaining/60)+':'+String(s.serviceRemaining%60).padStart(2,'0')+' min':'Service geschlossen';
    el('lastCommand').textContent=s.lastCommand;renderService();
    if(initial){for(let k of ['tmin','tmax','rhmin','rhmax','thyst','rhhyst'])el(k).value=s[k];initial=false}
  }catch(e){online=false;el('connection').textContent='Verbindung unterbrochen';renderService()}
  finally{setTimeout(refresh,1500)}
}
renderService();refresh();
</script></html>)HTML";
