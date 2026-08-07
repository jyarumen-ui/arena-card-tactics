# -*- coding: utf-8 -*-
"""盤面を本家どおりの「2列×3段・前列後列は左右」に戻す"""
import io

p = "index.html"
s = io.open(p, encoding="utf-8").read()

# ---------- 1) HTML: 盤面を左右対面に ----------
old_field = '''  <!-- 盤面: 敵が上・自分が下（上下対面） -->
  <div id="field">
    <div class="rowLabel">相手 ─ 後衛</div>
    <div class="fieldRow" id="gridEB"></div>
    <div class="rowLabel">相手 ─ 前衛</div>
    <div class="fieldRow" id="gridEF"></div>
    <div id="centerLine"></div>
    <div class="rowLabel">自分 ─ 前衛</div>
    <div class="fieldRow" id="gridPF"></div>
    <div class="rowLabel">自分 ─ 後衛</div>
    <div class="fieldRow" id="gridPB"></div>
  </div>'''
new_field = '''  <!-- 盤面: 本家と同じ「2列×3段」。前列・後列は左右の関係 -->
  <div id="field">
    <div class="sideWrap">
      <div class="laneHead"><span>自分 後列</span><span>自分 前列</span></div>
      <div class="sideGrid" id="gridP"></div>
    </div>
    <div id="centerLine"></div>
    <div class="sideWrap">
      <div class="laneHead"><span>相手 前列</span><span>相手 後列</span></div>
      <div class="sideGrid" id="gridE"></div>
    </div>
  </div>'''
if old_field not in s:
    raise SystemExit("盤面HTMLが見つかりません")
s = s.replace(old_field, new_field, 1)

# ---------- 2) CSS ----------
old_css = '''  /* 盤面: 敵が上・自分が下（本家の上下対面） */
  #field { display:flex; flex-direction:column; align-items:center; gap:3px;
    transform:perspective(1500px) rotateX(9deg); }
  .fieldRow { display:grid; grid-template-columns:repeat(3,124px); gap:8px; }
  .rowLabel { font-size:9.5px; color:#f5e2b0; font-weight:bold; letter-spacing:3px; opacity:.62;
    text-shadow:0 2px 3px rgba(0,0,0,.9); }'''
new_css = '''  /* 盤面: 2列×3段が左右で向かい合う（本家準拠） */
  #field { display:flex; align-items:center; gap:14px;
    transform:perspective(1400px) rotateX(10deg); }
  .sideWrap { display:flex; flex-direction:column; align-items:center; gap:4px; }
  .sideGrid { display:grid; grid-template-columns:repeat(2,116px); grid-template-rows:repeat(3,96px); gap:8px; }
  .laneHead { display:flex; gap:8px; font-size:9.5px; color:#f5e2b0; font-weight:bold;
    letter-spacing:2px; opacity:.66; text-shadow:0 2px 3px rgba(0,0,0,.9); }
  .laneHead span { width:116px; text-align:center; }'''
if old_css not in s:
    raise SystemExit("盤面CSSが見つかりません")
s = s.replace(old_css, new_css, 1)

# 中央線を縦に戻す
old_line = '''  #centerLine { width:420px; height:5px; border-radius:3px; margin:4px 0;
    background:linear-gradient(90deg, transparent, #ffe9a0 18%, #d9b24a 50%, #ffe9a0 82%, transparent);
    box-shadow:0 0 14px #d9b24a88; }'''
new_line = '''  #centerLine { width:5px; height:320px; border-radius:3px;
    background:linear-gradient(180deg, transparent, #ffe9a0 18%, #d9b24a 50%, #ffe9a0 82%, transparent);
    box-shadow:0 0 14px #d9b24a88; }'''
if old_line not in s:
    raise SystemExit("中央線CSSが見つかりません")
s = s.replace(old_line, new_line, 1)

# ---------- 3) render(): 描画順を左右に ----------
old_render = '''  // 自陣: 前衛(0-2)を中央線側、後衛(3-5)を手前に
  [["gridPF",[0,1,2]],["gridPB",[3,4,5]]].forEach(([id,idxs])=>{
    const g=document.getElementById(id); g.innerHTML="";
    idxs.forEach(i=>{
      const slot=document.createElement("div"); slot.className="slot"; slot.dataset.cell="p-"+i;
      const u=S.p.board[i];
      if(u){
        const d=unitDiv(u,true,i);
        d.onclick=()=>{ if(!DRAG||!DRAG.moved) onMySlotClick(i); };
        if(u.ready&&!busy) attachDrag(d, {kind:"unit", slot:i});
        slot.appendChild(d);
      }
      else if(placing&&!busy){ slot.classList.add("placeable"); slot.onclick=()=>onMySlotClick(i); }
      g.appendChild(slot);
    });
  });
  // 敵陣: 後衛(3-5)を奥、前衛(0-2)を中央線側に
  [["gridEB",[3,4,5]],["gridEF",[0,1,2]]].forEach(([id,idxs])=>{
    const g=document.getElementById(id); g.innerHTML="";
    idxs.forEach(i=>{
      const slot=document.createElement("div"); slot.className="slot"; slot.dataset.cell="e-"+i;
      const u=S.e.board[i];
      if(u){
        const d=unitDiv(u,false,i);
        let ok=false;
        if(attacking&&atg.units.includes(i)) ok=true;
        if(spelling&&stg.includes(i)) ok=true;
        if(ok&&!busy){ d.classList.add("targetable"); d.onclick=()=>onEnemyTarget(i); }
        else {
          d.onclick=()=>{ showUnitDetail(u); if(attacking) coach(whyCantAttack(i)); };
          if(attacking){ d.classList.add("protected"); d.dataset.why=whyLabel(i); }
        }
        // 前衛が真下の後衛を守っていることを線で示す
        if(i<3&&S.e.board[i+3]&&!u.stealth) slot.classList.add("guarding");
        slot.appendChild(d);
      }
      g.appendChild(slot);
    });
  });'''
new_render = '''  // 自陣（左）: 各段は 後列(3+r) → 前列(r) の順。前列が中央線側
  const gP=document.getElementById("gridP"); gP.innerHTML="";
  for(let r=0;r<3;r++) [3+r, r].forEach(i=>{
    const slot=document.createElement("div"); slot.className="slot"; slot.dataset.cell="p-"+i;
    const u=S.p.board[i];
    if(u){
      const d=unitDiv(u,true,i);
      d.onclick=()=>{ if(!DRAG||!DRAG.moved) onMySlotClick(i); };
      if(u.ready&&!busy) attachDrag(d, {kind:"unit", slot:i});
      slot.appendChild(d);
    }
    else if(placing&&!busy){ slot.classList.add("placeable"); slot.onclick=()=>onMySlotClick(i); }
    gP.appendChild(slot);
  });
  // 敵陣（右）: 各段は 前列(r) → 後列(3+r) の順。前列が中央線側
  const gE=document.getElementById("gridE"); gE.innerHTML="";
  for(let r=0;r<3;r++) [r, 3+r].forEach(i=>{
    const slot=document.createElement("div"); slot.className="slot"; slot.dataset.cell="e-"+i;
    const u=S.e.board[i];
    if(u){
      const d=unitDiv(u,false,i);
      let ok=false;
      if(attacking&&atg.units.includes(i)) ok=true;
      if(spelling&&stg.includes(i)) ok=true;
      if(ok&&!busy){ d.classList.add("targetable"); d.onclick=()=>onEnemyTarget(i); }
      else {
        d.onclick=()=>{ showUnitDetail(u); if(attacking) coach(whyCantAttack(i)); };
        if(attacking){ d.classList.add("protected"); d.dataset.why=whyLabel(i); }
      }
      // 前列が同じ段の後列を守っていることを示す
      if(i<3&&S.e.board[i+3]&&!u.stealth) slot.classList.add("guarding");
      slot.appendChild(d);
    }
    gE.appendChild(slot);
  });'''
if old_render not in s:
    raise SystemExit("render の盤面描画が見つかりません")
s = s.replace(old_render, new_render, 1)

# ---------- 4) ドラッグのドロップ候補も新IDに ----------
s = s.replace('document.querySelectorAll("#gridPF .slot,#gridPB .slot")',
              'document.querySelectorAll("#gridP .slot")', 1)

# ---------- 5) 守りの線を横向きに ----------
old_guard = '''  .slot.guarding::after { content:""; position:absolute; left:50%; bottom:-11px; width:2px; height:11px;
    background:linear-gradient(#8dff2e,rgba(141,255,46,0)); transform:translateX(-50%); }'''
new_guard = '''  .slot.guarding::after { content:""; position:absolute; top:50%; right:-11px; width:11px; height:2px;
    background:linear-gradient(90deg,#8dff2e,rgba(141,255,46,0)); transform:translateY(-50%); }'''
if old_guard in s:
    s = s.replace(old_guard, new_guard, 1)

# ---------- 6) 説明文の言い回しを合わせる ----------
s = s.replace("自分の陣地は<b>前衛3マス・後衛3マス</b>。<br>",
              "自分の陣地は<b>2列×3段</b>。中央寄りが<b>前列</b>、リーダー寄りが<b>後列</b>。<br>", 1)
s = s.replace("同じ段の<b>前衛がいる間、その後ろの後衛は攻撃されません</b>。<br>",
              "同じ段の<b>前列にユニットがいる間、その後ろの後列は攻撃されません</b>。<br>", 1)
s = s.replace("相手の<b>前衛3マスが全部埋まると、リーダーを攻撃できません</b>（ウォール）。",
              "相手の<b>前列3マスが全部埋まると、リーダーを攻撃できません</b>（ウォール）。", 1)

io.open(p, "w", encoding="utf-8").write(s)
print("盤面を2列×3段の左右対面に戻しました")
