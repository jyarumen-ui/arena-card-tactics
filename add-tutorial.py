# -*- coding: utf-8 -*-
"""対話式チュートリアル戦を組み込む"""
import io

p = "index.html"
s = io.open(p, encoding="utf-8").read()

TUTO_JS = r'''
// ================= 対話式チュートリアル =================
let TUTO={on:false, step:0};
const TUTO_ENEMY={   // 相手の行動は完全固定（AIを使わない）
  1:[],
  2:[{sum:"トゲガメ", slot:1}],
  3:[{sum:"カマイタチ", slot:0},{atk:0,tgt:1}],
  4:[{sum:"ガーディアン", slot:1}],
  5:[{sum:"サラマンドラ", slot:2}]
};
// 手札に配る順（先頭から配られる）
const TUTO_HAND=["ぷにまる","サラマンドラ","いかずちの矢"];
const TUTO_DRAW=["みならい魔導士","チビドラ","サンダーボルト","ヒーリング","ぷにまる","デスロード"];

function tutoCard(n){ const c=POOL.find(x=>x.n===n); return c?{...c}:{...POOL[0]}; }
function handHas(n){ return S.p.hand.some(c=>c.n===n); }
function boardHas(n){ return S.p.board.some(u=>u&&u.n===n); }
function myUnits(){ return S.p.board.filter(Boolean).length; }

const TUTO_STEPS=[
 {say:"ようこそ。<b>3分で1勝</b>できるよう案内します。\nまずは目的から。<b>相手リーダーのHPを0にすれば勝ち</b>です。いまは12。",
  hi:"#pedE", next:true},
 {say:"カードを出すには<b>MP</b>がいります。いまのMPは<b>1</b>。\nMPは毎ターン1ずつ増えて、最大10まで上がります。",
  hi:"#zoneP .mpnum, #zoneP .mpgems", next:true},
 {say:"手札の<b>ぷにまる</b>（コスト1）をタップしてみましょう。",
  hi:"#handArea .card", done:()=>S.pending&&S.pending.type==="place"},
 {say:"置ける場所が光りました。\n<b>前衛</b>は自分から殴られる盾、<b>後衛</b>は真上に前衛がいる間は守られます。\nいまは<b>前衛のまん中</b>に置いてみましょう。",
  hi:'[data-cell="p-1"]', done:()=>boardHas("ぷにまる")},
 {say:"出したばかりのユニットは<b>そのターンは攻撃できません</b>（😴の印）。\n「ターン終了」を押しましょう。",
  hi:"#endBtn", done:()=>S.turn>=2},
 {say:"MPが<b>2</b>になりました。\nぷにまるが緑に光っています。これが「動ける」印です。タップしてみましょう。",
  hi:'[data-cell="p-1"] .unit', done:()=>S.sel!==null},
 {say:"赤く光っているのが攻撃できる相手。\n相手の前衛が空いているので<b>リーダーを直接殴れます</b>。",
  hi:"#pedE", done:()=>S.e.hp<12},
 {say:"よくできました。残りMPで<b>サラマンドラ</b>を前衛に出して、ターンを終えましょう。",
  hi:"#handArea .card, #endBtn", done:()=>S.turn>=3},
 {say:"相手が <b>⛨におうだち</b> を出しました。\n<b>これがいる間、ほかのユニットもリーダーも攻撃できません</b>。",
  hi:'[data-cell="e-1"] .unit', next:true},
 {say:"正面から殴ると自分も傷つきます。\n先に特技<b>いかずちの矢</b>（3ダメージ）で削りましょう。",
  hi:"#handArea .card", done:()=>!handHas("いかずちの矢")},
 {say:"MPが余ったら<b>テンション</b>に変えておきましょう。\n1ターン1回ためられて、<b>3たまると職業ごとの必殺技</b>が使えます。",
  hi:"#tensionBtn", done:()=>S.p.tension>=1||S.turn>=4},
 {say:"ここからは自由に戦ってみましょう。\n・壁を壊してからリーダーを殴る\n・MPは余らせず使い切る\nこの2つを意識すれば勝てます。",
  hi:null, next:true, free:true}
];

function tutoEl(sel){ try{ return sel?document.querySelectorAll(sel):[]; }catch(e){ return []; } }
function tutoPaint(){
  if(!TUTO.on) return;
  const b=document.getElementById("tutoBubble"), m=document.getElementById("tutoMask");
  // 条件を満たしたステップを進める
  let guard=0;
  while(TUTO.step<TUTO_STEPS.length && TUTO_STEPS[TUTO.step].done && TUTO_STEPS[TUTO.step].done() && guard++<20) TUTO.step++;
  const st=TUTO_STEPS[TUTO.step];
  document.querySelectorAll(".tutoGlow").forEach(e=>e.classList.remove("tutoGlow"));
  if(!st){ b.classList.remove("on"); m.classList.remove("on"); return; }
  b.innerHTML=st.say+'<div class="row">'+
    (st.next?'<button id="tutoNext">つぎへ ▶</button>':'')+
    '<button class="skip" id="tutoSkip">説明をとばす</button></div>';
  b.classList.add("on");
  m.classList.toggle("on", !!st.hi);
  tutoEl(st.hi).forEach(e=>e.classList.add("tutoGlow"));
  const nx=document.getElementById("tutoNext");
  if(nx) nx.onclick=()=>{ TUTO.step++; render(); };
  document.getElementById("tutoSkip").onclick=()=>tutoEnd();
}
function tutoEnd(){
  TUTO.on=false;
  document.getElementById("tutoBubble").classList.remove("on");
  document.getElementById("tutoMask").classList.remove("on");
  document.querySelectorAll(".tutoGlow").forEach(e=>e.classList.remove("tutoGlow"));
}
// 相手の行動（固定台本）
function tutoEnemyTurn(){
  const gid=S.gid;
  const seq=(TUTO_ENEMY[S.turn]||[]).slice();
  (function next(){
    if(!S||S.gid!==gid) return;
    if(S.p.hp<=0||S.e.hp<=0){ render(); return; }
    const a=seq.shift();
    if(!a){
      S.turn++; startTurn("p"); busy=false;
      banner("あなたのターン"); render(); return;
    }
    if(a.sum){ const c=POOL.find(x=>x.n===a.sum); if(c) summon("e",c,a.slot); }
    if(a.atk!==undefined && S.e.board[a.atk] && S.p.board[a.tgt]) attack("e",a.atk,a.tgt);
    render(); setTimeout(next, 900);
  })();
}
'''

# 1) チュートリアルのコードを挿入
anchor = "// ================= バランス測定用シミュレータ ================="
if anchor not in s:
    raise SystemExit("挿入位置が見つかりません")
s = s.replace(anchor, TUTO_JS.strip("\n") + "\n\n" + anchor, 1)

# 2) startGame にチュートリアル分岐
old = '''function startGame(clsP, clsE){
  document.getElementById("classSel").style.display="none";
  document.getElementById("screen").classList.remove("on");'''
new = '''function startGame(clsP, clsE, opt){
  opt=opt||{};
  document.getElementById("classSel").style.display="none";
  document.getElementById("screen").classList.remove("on");
  tutoEnd();'''
if old not in s: raise SystemExit("startGame が見つかりません")
s = s.replace(old, new, 1)

# 3) チュートリアル用の初期化（デッキ・HP・手札を固定）
old2 = '''  labelSides();
  document.getElementById("log").innerHTML="";
  showDetail(null); restorePedestals(); render();'''
new2 = '''  if(opt.tuto){
    MODE="tuto"; TUTO.on=true; TUTO.step=0;
    S.e.hp=12; S.eMax=12;
    S.p.hand=TUTO_HAND.map(tutoCard);
    S.p.deck=TUTO_DRAW.slice().reverse().map(tutoCard)
      .concat(Array(12).fill(0).map(()=>tutoCard("ぷにまる")));
    S.e.hand=[]; S.e.tension=0; S.e.potion=false;
    document.getElementById("vsE").textContent="訓練相手";
  }
  labelSides();
  document.getElementById("log").innerHTML="";
  showDetail(null); restorePedestals(); render();'''
if old2 not in s: raise SystemExit("初期化位置が見つかりません")
s = s.replace(old2, new2, 1)

# 4) マリガンを飛ばす
old3 = '''  } else {
    showMulligan(()=>{ startTurn("p"); busy=false; banner("あなたのターン"); render(); });
  }
}'''
new3 = '''  } else if(opt.tuto){
    startTurn("p"); busy=false; banner("チュートリアル"); render();
  } else {
    showMulligan(()=>{ startTurn("p"); busy=false; banner("あなたのターン"); render(); });
  }
}'''
if old3 not in s: raise SystemExit("マリガン分岐が見つかりません")
s = s.replace(old3, new3, 1)

# 5) endTurn でチュートリアルの台本を回す
old4 = '''  banner("相手のターン");
  startTurn("e");
  render();
  const gid=S.gid;
  setTimeout(()=>{ if(S&&S.gid===gid) aiTurn(); }, 900);'''
new4 = '''  banner("相手のターン");
  startTurn("e");
  render();
  const gid=S.gid;
  setTimeout(()=>{ if(S&&S.gid===gid) (MODE==="tuto"?tutoEnemyTurn():aiTurn()); }, 900);'''
if old4 not in s: raise SystemExit("endTurn が見つかりません")
s = s.replace(old4, new4, 1)

# 6) render の末尾で吹き出しを更新
old5 = "  document.getElementById(\"enemyThink\").textContent = busy&&S.p.hp>0&&S.e.hp>0 ? \"考え中…\" : \"\";\n  flushFX();"
new5 = "  document.getElementById(\"enemyThink\").textContent = busy&&S.p.hp>0&&S.e.hp>0 ? \"考え中…\" : \"\";\n  if(TUTO.on) tutoPaint();\n  flushFX();"
if old5 not in s: raise SystemExit("render 末尾が見つかりません")
s = s.replace(old5, new5, 1)

# 7) 敵HPバーの分母をチュートリアルに合わせる
s = s.replace('document.getElementById("hpbarE").style.width=Math.max(0,S.e.hp/25*100)+"%";',
              'document.getElementById("hpbarE").style.width=Math.max(0,S.e.hp/(S.eMax||25)*100)+"%";', 1)

io.open(p, "w", encoding="utf-8").write(s)
print("チュートリアルを組み込みました")
