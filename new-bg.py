# -*- coding: utf-8 -*-
"""CSSグラデーションの背景を、実際の背景画像＋光の演出に差し替える"""
import io

p = "index.html"
s = io.open(p, encoding="utf-8").read()

# ---------- 1) CSS ----------
old_css_start = s.index("  /* ===== アリーナ背景（壁＋奥行きのある石床＋松明） ===== */")
old_css_end = s.index("  /* ===== 上部バー ===== */")

NEW_CSS = '''  /* ===== アリーナ背景（描き込んだ背景画＋光の演出） ===== */
  #bg { position:fixed; inset:0; z-index:-2; overflow:hidden; background:#0b0906; }
  /* 背景画は2枚を重ね、切り替え時にクロスフェードさせる */
  .bgLayer { position:absolute; inset:0; background-size:cover; background-position:center 42%;
    opacity:0; transition:opacity .9s ease; transform:scale(1.04);
    animation:bgDrift 46s ease-in-out infinite alternate; }
  .bgLayer.on { opacity:1; }
  @keyframes bgDrift {
    from { transform:scale(1.04) translate(0,0); }
    to   { transform:scale(1.09) translate(0,-1.4%); }
  }
  /* 空気中の塵（奥行きを出す） */
  #bgDust { position:fixed; inset:0; z-index:-1; pointer-events:none; opacity:.5;
    background:
      radial-gradient(circle at 12% 30%, rgba(255,230,180,.55) 0 1.1px, transparent 1.6px),
      radial-gradient(circle at 34% 68%, rgba(255,230,180,.42) 0 1.4px, transparent 2px),
      radial-gradient(circle at 58% 22%, rgba(255,230,180,.5) 0 1px, transparent 1.5px),
      radial-gradient(circle at 77% 55%, rgba(255,230,180,.38) 0 1.3px, transparent 1.9px),
      radial-gradient(circle at 91% 34%, rgba(255,230,180,.46) 0 1.1px, transparent 1.6px);
    background-size:340px 300px, 420px 380px, 300px 340px, 460px 400px, 380px 320px;
    animation:dust 34s linear infinite; }
  @keyframes dust {
    from { background-position:0 0, 0 0, 0 0, 0 0, 0 0; }
    to   { background-position:0 -300px, 0 -380px, 0 -340px, 0 -400px, 0 -320px; }
  }
  /* 明暗の調整。UIを読みやすくしつつ雰囲気を残す */
  #bgVig { position:fixed; inset:0; z-index:-1; pointer-events:none;
    background:
      radial-gradient(ellipse 34% 40% at 6% 30%, rgba(255,158,58,.20), transparent 70%),
      radial-gradient(ellipse 34% 40% at 94% 30%, rgba(255,158,58,.20), transparent 70%),
      linear-gradient(rgba(0,0,0,.52), rgba(0,0,0,.10) 22%, rgba(0,0,0,.12) 62%, rgba(0,0,0,.66)),
      radial-gradient(ellipse 88% 74% at 50% 48%, transparent 34%, rgba(0,0,0,.62) 100%);
    animation:ember 5.5s ease-in-out infinite; }
  @keyframes ember { 0%,100%{ opacity:1; } 50%{ opacity:.9; } }
  /* 盤面のうしろに敷く舞台の敷物。カードの視認性を上げる */
  #stageGlow { position:fixed; left:50%; top:52%; width:760px; height:390px; z-index:-1;
    transform:translate(-50%,-50%); pointer-events:none; filter:blur(26px); opacity:.5;
    background:radial-gradient(ellipse at center, rgba(0,0,0,.72) 0%, rgba(0,0,0,.42) 55%, transparent 78%); }
'''

s = s[:old_css_start] + NEW_CSS + s[old_css_end:]

# ---------- 2) HTML ----------
old_html = '''<div id="bg">
  <div id="bgWall"><div id="bgArches"></div></div>
  <div id="bgFloor"><div id="bgGrid"></div></div>
  <div id="bgHorizon"></div>'''
new_html = '''<div id="bg">
  <div class="bgLayer" id="bgA"></div>
  <div class="bgLayer" id="bgB"></div>'''
if old_html not in s:
    raise SystemExit("背景HTMLが見つかりません")
s = s.replace(old_html, new_html, 1)

# 松明のspanを塵と舞台の影に置き換える
old_torch = '''<div id="bgVig"></div>
<span class="torch" style="left:52px; top:126px;"></span>
<span class="torch" style="right:52px; top:126px;"></span>
<span class="torch" style="left:212px; top:104px;"></span>
<span class="torch" style="right:212px; top:104px;"></span>'''
new_torch = '''<div id="bgVig"></div>
<div id="bgDust"></div>
<div id="stageGlow"></div>'''
if old_torch not in s:
    raise SystemExit("松明HTMLが見つかりません")
s = s.replace(old_torch, new_torch, 1)

# ---------- 3) 背景切り替えのJS ----------
BG_JS = '''
// ============ 背景の切り替え（クロスフェード） ============
const BG_SET={
  arena:{ file:"bg-arena.jpg",  tint:"warm" },
  ice:  { file:"bg-arena2.jpg", tint:"cold" }
};
let BG_CUR=null, BG_FLIP=false;
function bgUrl(file){
  if(window.__ART__ && window.__ART__[file]) return window.__ART__[file];
  return "art/"+file;
}
function setBg(name){
  const def=BG_SET[name]||BG_SET.arena;
  if(BG_CUR===name) return;
  BG_CUR=name;
  const show=document.getElementById(BG_FLIP?"bgA":"bgB");
  const hide=document.getElementById(BG_FLIP?"bgB":"bgA");
  BG_FLIP=!BG_FLIP;
  show.style.backgroundImage='url("'+bgUrl(def.file)+'")';
  // 画像が読めてから切り替える（黒画面をはさまない）
  const img=new Image();
  img.onload=img.onerror=()=>{ show.classList.add("on"); hide.classList.remove("on"); };
  img.src=bgUrl(def.file);
  // 光の色みを場所に合わせる
  const v=document.getElementById("bgVig");
  v.style.filter = def.tint==="cold" ? "hue-rotate(172deg) saturate(.85)" : "none";
}
function preloadBg(){ Object.values(BG_SET).forEach(d=>{ const i=new Image(); i.src=bgUrl(d.file); }); }
'''

anchor = "// ============ BGM（WebAudio合成"
if anchor not in s:
    raise SystemExit("JS挿入位置が見つかりません")
s = s.replace(anchor, BG_JS.strip("\n") + "\n\n" + anchor, 1)

io.open(p, "w", encoding="utf-8").write(s)
print("背景を画像ベースに差し替えました")
