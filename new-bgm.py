# -*- coding: utf-8 -*-
"""BGMエンジンを本格的なものに差し替える（残響／ドラム／和音進行／複数楽器）"""
import io

p = "index.html"
s = io.open(p, encoding="utf-8").read()

NEW = r'''
// ============ BGM（WebAudio合成：残響・ドラム・和音進行つき） ============
const NOTE={C2:65.41,D2:73.42,E2:82.41,F2:87.31,G2:98,A2:110,Bb2:116.54,B2:123.47,
 C3:130.81,Db3:138.59,D3:146.83,Eb3:155.56,E3:164.81,F3:174.61,G3:196,A3:220,Bb3:233.08,B3:246.94,
 C4:261.63,Db4:277.18,D4:293.66,Eb4:311.13,E4:329.63,F4:349.23,G4:392,A4:440,Bb4:466.16,B4:493.88,
 C5:523.25,Db5:554.37,D5:587.33,Eb5:622.25,E5:659.25,F5:698.46,G5:783.99,A5:880,Bb5:932.33,C6:1046.5,D6:1174.7};

// 和音は実音で持つ
const CH={
 Dm:["D3","F3","A3"], Bb:["Bb2","D3","F3"], F:["F2","A2","C3"], C:["C3","E3","G3"],
 Gm:["G2","Bb2","D3"], Am:["A2","C3","E3"], A7:["A2","Db3","G3"], Eb:["Eb3","G3","Bb3"]
};

// prog=[コード名,小節数] / mel=[音名 or null, 拍数]（合計が4の倍数になるよう作る）
const TUNES={
 home:{ bpm:82, drums:"soft",
   prog:[["Dm",2],["Bb",2],["F",2],["C",2],["Bb",2],["Gm",2],["Am",2],["Dm",2]],
   mel:[["A4",1.5],["D5",.5],["F5",1],["E5",1],
        ["D5",1.5],["A4",.5],["Bb4",2],
        ["C5",1.5],["F5",.5],["A5",1],["G5",1],
        ["F5",2],["E5",2],
        ["D5",1],["C5",1],["Bb4",1],["A4",1],
        ["G4",2],[null,2],
        ["A4",1],["Bb4",1],["C5",1],["D5",1],
        ["A4",3],[null,1]] },
 battle:{ bpm:126, drums:"hard",
   prog:[["Dm",2],["Bb",2],["C",2],["Dm",2],["Gm",2],["Bb",2],["C",2],["A7",2]],
   mel:[["D5",.5],["A4",.5],["D5",.5],["F5",.5],["E5",1],["D5",1],
        ["Bb4",.5],["D5",.5],["F5",.5],["A5",.5],["G5",2],
        ["C5",.5],["E5",.5],["G5",.5],["C6",.5],["Bb5",1],["A5",1],
        ["D5",.5],["F5",.5],["A5",.5],["D6",.5],["A5",2],
        ["G4",.5],["Bb4",.5],["D5",.5],["G5",.5],["F5",1],["D5",1],
        ["Bb4",.5],["D5",.5],["F5",.5],["Bb5",.5],["A5",2],
        ["C5",.5],["G5",.5],["E5",.5],["C5",.5],["D5",1],["E5",1],
        ["F5",.5],["E5",.5],["D5",.5],["C5",.5],["A4",2]] },
 win:{ bpm:130, drums:"hard", once:true,
   prog:[["Dm",1],["Bb",1],["F",1],["C",1],["Dm",2]],
   mel:[["D5",.5],["F5",.5],["A5",1],
        ["G5",.5],["A5",.5],["C6",1],
        ["A5",.5],["F5",.5],["D5",1],
        ["A5",1],["D6",1],
        ["D6",4]] },
};

let BGM={on:true, timer:null, t:0, mi:0, bar:0, started:false, scene:"home",
         master:null, conv:null, buses:null};

// 残響用のインパルス応答をその場で合成する
function makeIR(sec, decay){
  const rate=AC.sampleRate, len=Math.floor(rate*sec), buf=AC.createBuffer(2,len,rate);
  for(let ch=0;ch<2;ch++){
    const d=buf.getChannelData(ch);
    for(let i=0;i<len;i++) d[i]=(Math.random()*2-1)*Math.pow(1-i/len,decay);
  }
  return buf;
}
// 送り量ごとに固定のバスを用意する（音ごとに作らないのでノードが溜まらない）
const SENDS=[0,0.1,0.25,0.4,0.6];
function bgmInit(){
  if(BGM.master) return;
  BGM.master=AC.createGain(); BGM.master.gain.value=0.34;
  const comp=AC.createDynamicsCompressor();
  comp.threshold.value=-15; comp.ratio.value=3.2; comp.attack.value=0.006; comp.release.value=0.2;
  BGM.master.connect(comp); comp.connect(MASTER||AC.destination);
  BGM.conv=AC.createConvolver(); BGM.conv.buffer=makeIR(2.8, 2.6);
  const wet=AC.createGain(); wet.gain.value=0.42;
  BGM.conv.connect(wet); wet.connect(BGM.master);
  BGM.buses=SENDS.map(v=>{
    const g=AC.createGain(); g.gain.value=1; g.connect(BGM.master);
    if(v>0){ const w=AC.createGain(); w.gain.value=v; g.connect(w); w.connect(BGM.conv); }
    return g;
  });
}
function bus(send){
  let best=0, diff=9;
  SENDS.forEach((v,i)=>{ const d=Math.abs(v-send); if(d<diff){ diff=d; best=i; } });
  return BGM.buses[best];
}
// 音色つきの1音
function tone(freq,start,dur,o){
  if(!freq||!BGM.buses) return;
  o=o||{};
  const f=AC.createBiquadFilter();
  f.type="lowpass"; f.frequency.value=o.cut||2600; f.Q.value=o.q||0.7;
  f.connect(bus(o.send===undefined?0.25:o.send));
  const g=AC.createGain(); g.connect(f);
  const peak=o.vol===undefined?0.2:o.vol;
  const atk=o.atk===undefined?0.012:o.atk, rel=o.rel===undefined?0.22:o.rel;
  g.gain.setValueAtTime(0.0001,start);
  g.gain.exponentialRampToValueAtTime(peak,start+atk);
  g.gain.setValueAtTime(peak,start+Math.max(atk+0.001,dur-rel));
  g.gain.exponentialRampToValueAtTime(0.0006,start+dur);
  if(o.sweep){
    f.frequency.setValueAtTime((o.cut||2600)*0.45,start);
    f.frequency.linearRampToValueAtTime(o.cut||2600,start+0.11);
  }
  // 少しずらした発振器を重ねて厚みを出す
  const det=o.detune||[0];
  let last=null;
  det.forEach(c=>{
    const osc=AC.createOscillator();
    osc.type=o.type||"triangle"; osc.frequency.value=freq; osc.detune.value=c;
    if(o.vib){
      const lfo=AC.createOscillator(), la=AC.createGain();
      lfo.frequency.value=5.4; la.gain.value=o.vib;
      lfo.connect(la); la.connect(osc.detune);
      lfo.start(start); lfo.stop(start+dur+0.05);
      osc.onended=()=>{ try{ lfo.disconnect(); la.disconnect(); }catch(e){} };
    }
    osc.connect(g); osc.start(start); osc.stop(start+dur+0.05);
    last=osc;
  });
  if(last) last.onended=()=>{ try{ g.disconnect(); f.disconnect(); }catch(e){} };
}
function noiseHit(t,hp,vol,decay,send){
  if(!BGM.buses) return;
  const s=AC.createBufferSource(); s.buffer=NOISEBUF;
  const f=AC.createBiquadFilter(); f.type="highpass"; f.frequency.value=hp;
  const g=AC.createGain();
  s.connect(f); f.connect(g); g.connect(bus(send));
  g.gain.setValueAtTime(vol,t); g.gain.exponentialRampToValueAtTime(0.0008,t+decay);
  s.start(t); s.stop(t+decay+0.02);
  s.onended=()=>{ try{ g.disconnect(); f.disconnect(); }catch(e){} };
}
function drumKick(t,vol){
  if(!BGM.buses) return;
  const o=AC.createOscillator(), g=AC.createGain();
  o.type="sine"; o.connect(g); g.connect(bus(0.1));
  o.frequency.setValueAtTime(155,t); o.frequency.exponentialRampToValueAtTime(44,t+0.1);
  g.gain.setValueAtTime(vol||0.5,t); g.gain.exponentialRampToValueAtTime(0.001,t+0.23);
  o.start(t); o.stop(t+0.25);
  o.onended=()=>{ try{ g.disconnect(); }catch(e){} };
}
function curTune(){ return TUNES[BGM.scene]||TUNES.battle; }
function bgmScene(name){
  if(!TUNES[name]||BGM.scene===name) return;
  BGM.scene=name; BGM.mi=0; BGM.bar=0;
  if(AC&&BGM.started) BGM.t=AC.currentTime+0.06;
}
function totalBars(T){ return T.prog.reduce((n,x)=>n+x[1],0); }
function chordAt(T,bar){
  let acc=0;
  for(const [name,len] of T.prog){ if(bar<acc+len) return CH[name]; acc+=len; }
  return CH[T.prog[0][0]];
}

function bgmSchedule(){
  if(!AC||!BGM.on||!BGM.master) return;
  const T=curTune(), beat=60/T.bpm, barLen=beat*4, ahead=1.6;
  while(BGM.t < AC.currentTime+ahead){
    if(BGM.t < AC.currentTime) BGM.t=AC.currentTime+0.05;
    if(T.once && BGM.bar>=totalBars(T)){ bgmScene("home"); return; }
    const t0=BGM.t, b=BGM.bar%totalBars(T), ch=chordAt(T,b), hard=T.drums==="hard";

    // 和音のパッド（長く伸ばして空気をつくる）
    ch.forEach(n=>tone(NOTE[n]*2,t0,barLen*0.99,
      {type:"sawtooth",vol:0.05,atk:0.4,rel:0.7,cut:820,send:0.6,detune:[-8,8]}));

    // ベース
    const root=NOTE[ch[0]];
    for(let k=0;k<4;k++)
      tone(k===2?root*1.5:root, t0+k*beat, beat*0.9,
        {type:"sawtooth",vol:0.21,atk:0.006,rel:0.1,cut:480,send:0.1,sweep:1});

    // 対旋律のアルペジオ（速い曲だけ）
    if(hard) for(let k=0;k<8;k++)
      tone(NOTE[ch[k%3]]*2, t0+k*beat/2, beat*0.42,
        {type:"triangle",vol:0.055,atk:0.004,rel:0.09,cut:3400,send:0.4});

    // ドラム
    drumKick(t0, hard?0.55:0.4);
    if(hard) drumKick(t0+beat*2.5,0.4);
    noiseHit(t0+beat,   1500, hard?0.22:0.13, 0.15, 0.25);
    noiseHit(t0+beat*3, 1500, hard?0.22:0.13, 0.15, 0.25);
    const div=hard?8:4;
    for(let k=0;k<div;k++) noiseHit(t0+k*barLen/div, 7500, hard?(k%2?0.035:0.07):0.045, 0.045, 0.1);

    // 主旋律（この小節ぶんを敷き詰める）
    let mt=t0, remain=4;
    while(remain>0.001){
      const [n,d]=T.mel[BGM.mi%T.mel.length];
      const use=Math.min(d,remain);
      if(n){
        tone(NOTE[n], mt, use*beat*0.96,
          {type:"triangle",vol:0.21,atk:0.014,rel:0.18,cut:4400,send:0.35,detune:[-6,6],vib:7});
        tone(NOTE[n]/2, mt, use*beat*0.9,
          {type:"sine",vol:0.06,atk:0.02,rel:0.18,cut:1600,send:0.25});
      }
      mt+=use*beat; remain-=use;
      if(use>=d) BGM.mi++; else break;
    }
    BGM.t+=barLen; BGM.bar++;
  }
}
function bgmStart(){
  if(!AC||BGM.started||!BGM.on) return;
  acInit(); bgmInit();
  BGM.started=true; BGM.t=AC.currentTime+0.15;
  bgmSchedule();
  BGM.timer=setInterval(bgmSchedule,430);
}
function bgmStop(){
  BGM.started=false;
  if(BGM.timer){ clearInterval(BGM.timer); BGM.timer=null; }
  if(BGM.master){ try{ BGM.master.gain.setTargetAtTime(0,AC.currentTime,0.1); }catch(e){} }
}
function bgmToggle(){
  BGM.on=!BGM.on;
  try{ localStorage.setItem("ct_bgm", BGM.on?"1":"0"); }catch(e){}
  if(BGM.on){
    if(BGM.master) BGM.master.gain.setTargetAtTime(0.34,AC.currentTime,0.12);
    BGM.started=false; bgmStart();
  } else bgmStop();
  const b=document.getElementById("bgmBtn"); if(b) b.textContent=BGM.on?"🔊":"🔇";
}
'''

start = s.index("// ============ RPG風BGM")
end = s.index("function sfx(kind){")
s = s[:start] + NEW.strip("\n") + "\n\n" + s[end:]

io.open(p, "w", encoding="utf-8").write(s)
print("BGMエンジンを差し替えました")
