# -*- coding: utf-8 -*-
"""拡張セット「種族の目覚め」87枚をPOOLに追加する"""
import io

p = "index.html"
s = io.open(p, encoding="utf-8").read()

CARDS = """
 // ================= 拡張セット「種族の目覚め」 =================
 {n:"こだまスライム",  t:"unit", c:1, a:0, h:2, kw:"crydraw",  r:"R", gen:{b:"slime",g:"gBlue",l:"#10508c",mouth:1}},
 {n:"マナのつぼみ",    t:"unit", c:1, a:0, h:2, kw:"crymp",    r:"R", gen:{b:"plant",g:"gGreen",l:"#14611f",one:1}},
 {n:"ミニドラゴン",    t:"unit", c:1, a:1, h:1, kw:"racesolo", race:"ドラゴン", r:"R", gen:{b:"dragon",g:"gRed",l:"#70140a"}},
 {n:"わかばウルフ",    t:"unit", c:1, a:1, h:1, kw:"racesolo", race:"けもの",   r:"N", gen:{b:"beast",g:"gOlive",l:"#2b3b0d",fang:1}},
 {n:"かけらゴーレム",  t:"unit", c:1, a:0, h:2, kw:"nio",      r:"N", gen:{b:"golem",g:"gStone",l:"#3b4049"}},
 {n:"したっぱゾンビ",  t:"unit", c:1, a:1, h:1, kw:"lastdraw", r:"N", gen:{b:"undead",g:"gBone",l:"#8d8672"}},
 {n:"ちいさな火の玉",  t:"unit", c:1, a:1, h:1, kw:"cryburn",  r:"R", gen:{b:"elem",g:"gFlame",l:"#8f2403",one:1}},
 {n:"すばやいツバメ",  t:"unit", c:1, a:1, h:1, kw:"onatk",    r:"N", gen:{b:"bird",g:"gCream",l:"#6b5c3d"}},
 {n:"せいれいのたまご",t:"unit", c:1, a:0, h:2, kw:"growth",   r:"R", gen:{b:"elem",g:"gCream",l:"#6b5c3d",one:1}},
 {n:"こわれかけロボ",  t:"unit", c:1, a:1, h:1, kw:"metal",    r:"SR",gen:{b:"golem",g:"gSteel",l:"#12305a"}},
 {n:"マナクリスタル",  t:"unit", c:2, a:1, h:2, kw:"crymp",    r:"R", gen:{b:"elem",g:"gCobalt",l:"#132356",one:1}},
 {n:"ぬすっとカラス",  t:"unit", c:2, a:2, h:2, kw:"crydraw",  r:"R", gen:{b:"bird",g:"gDark",l:"#07080d"}},
 {n:"とげネズミ",      t:"unit", c:2, a:1, h:3, kw:"enrage",   r:"N", gen:{b:"beast",g:"gBrown",l:"#4a3014",fang:1}},
 {n:"火花の精",        t:"unit", c:2, a:2, h:2, kw:"cryburn",  r:"R", gen:{b:"elem",g:"gFlame",l:"#8f2403",one:1}},
 {n:"群狼のアルファ",  t:"unit", c:3, a:3, h:3, kw:"racebuff", race:"けもの",     r:"SR",gen:{b:"beast",g:"gBrown",l:"#4a3014",fang:1}},
 {n:"大空の先導者",    t:"unit", c:3, a:3, h:3, kw:"racebuff", race:"とり",       r:"SR",gen:{b:"bird",g:"gYellow",l:"#95700a",wing:1}},
 {n:"世界樹のなえ",    t:"unit", c:3, a:2, h:4, kw:"racebuff", race:"しょくぶつ", r:"SR",gen:{b:"plant",g:"gGreen",l:"#14611f",one:1}},
 {n:"精霊の導き手",    t:"unit", c:3, a:3, h:3, kw:"racebuff", race:"エレメント", r:"SR",gen:{b:"elem",g:"gPurple",l:"#3d1c78",one:1}},
 {n:"沈黙の司祭",      t:"unit", c:3, a:2, h:3, kw:"crysilence", r:"R", gen:{b:"humanoid",g:"gBone",l:"#8d8672"}},
 {n:"マナの番人",      t:"unit", c:3, a:2, h:3, kw:"crymp",      r:"R", gen:{b:"golem",g:"gCobalt",l:"#132356"}},
 {n:"スライムキング",  t:"unit", c:4, a:3, h:5, kw:"racebuff", race:"スライム",   r:"SR",gen:{b:"slime",g:"gBlue",l:"#10508c",crown:1,mouth:1}},
 {n:"傭兵団の隊長",    t:"unit", c:4, a:4, h:4, kw:"racebuff", race:"にんげん",   r:"SR",gen:{b:"humanoid",g:"gSteel",l:"#12305a"}},
 {n:"女王アリ",        t:"unit", c:4, a:3, h:5, kw:"racebuff", race:"むし",       r:"SR",gen:{b:"insect",g:"gOlive",l:"#2b3b0d",crown:1}},
 {n:"墓守の司教",      t:"unit", c:4, a:3, h:5, kw:"racebuff", race:"アンデッド", r:"SR",gen:{b:"undead",g:"gMaroon",l:"#200d12"}},
 {n:"深海の歌姫",      t:"unit", c:4, a:3, h:5, kw:"racebuff", race:"すいせい",   r:"SR",gen:{b:"fish",g:"gCobalt",l:"#132356",mouth:1}},
 {n:"魔導の技師",      t:"unit", c:4, a:3, h:5, kw:"racebuff", race:"ぶっしつ",   r:"SR",gen:{b:"humanoid",g:"gStone",l:"#3b4049"}},
 {n:"鋼のかかし",      t:"unit", c:4, a:0, h:8, kw:"nio",      r:"R", gen:{b:"golem",g:"gBrown",l:"#4a3014"}},
 {n:"竜騎士ガイア",    t:"unit", c:5, a:4, h:5, kw:"racebuff", race:"ドラゴン",   r:"SR",gen:{b:"humanoid",g:"gRed",l:"#70140a",horn:1}},
 {n:"氷結のゴーレム",  t:"unit", c:5, a:4, h:5, kw:"shield",   r:"R", gen:{b:"golem",g:"gSteel",l:"#12305a"}},
 {n:"復讐の亡霊",      t:"unit", c:5, a:6, h:3, kw:"enrage",   r:"R", gen:{b:"undead",g:"gMaroon",l:"#200d12"}},
 {n:"永久機関ゴーレム",t:"unit", c:6, a:4, h:7, kw:"crymp",      r:"SR",gen:{b:"golem",g:"gGold",l:"#7a5010"}},
 {n:"大鎌の死神",      t:"unit", c:6, a:6, h:4, kw:"crysilence", r:"SR",gen:{b:"undead",g:"gDark",l:"#07080d"}},
 {n:"竜王の末裔",      t:"unit", c:6, a:5, h:6, kw:"racebuff", race:"ドラゴン", r:"SR",gen:{b:"dragon",g:"gGold",l:"#7a5010",horn:1}},
 {n:"深淵のクラーケン",t:"unit", c:7, a:5, h:9, kw:"nio",        r:"SR",gen:{b:"fish",g:"gCobalt",l:"#132356",one:1}},
 {n:"業火竜イグニス",  t:"unit", c:7, a:7, h:5, kw:"two",        r:"SR",gen:{b:"dragon",g:"gFlame",l:"#8f2403",horn:1,fang:1}},
 {n:"星喰らいの巨鳥",  t:"unit", c:8, a:6, h:9, kw:"growth",     r:"SR",gen:{b:"bird",g:"gCloud",l:"#1e2431",wing:1}},
 {n:"冥王ベルゼグ",    t:"unit", c:9, a:8, h:8, kw:"crydestroy", r:"L", gen:{b:"undead",g:"gDark",l:"#07080d",crown:1}},
 {n:"創世の巨神",      t:"unit", c:10,a:9, h:10,kw:"nio",        r:"L", gen:{b:"golem",g:"gGold",l:"#7a5010",crown:1}},
 {n:"だいちのめぐみ",  t:"spell", c:2, spell:"mpup",       r:"R"},
 {n:"追い打ちの矢",    t:"spell", c:2, spell:"dmg2draw",   r:"N"},
 {n:"英雄の一撃",      t:"spell", c:3, spell:"face5",      r:"R"},
 {n:"やまびこの号令",  t:"spell", c:4, spell:"token3",     r:"R"},
 {n:"粛清の光",        t:"spell", c:5, spell:"destroybig", r:"SR"},
 {n:"忘却の呪い",      t:"spell", c:5, spell:"silenceall", r:"R"},
 {n:"きりさきの短剣",  t:"weapon",c:1, a:1, dur:2,         r:"N"},
 {n:"雷神のヤリ",      t:"weapon",c:6, a:5, dur:3,         r:"SR"},
 {n:"刃研ぎの弟子",  t:"unit", c:1, a:1, h:1, kw:"crybladed", cls:"sword", r:"N", gen:{b:"humanoid",g:"gSteel",l:"#12305a"}},
 {n:"疾風の剣士",    t:"unit", c:2, a:3, h:1, kw:"charge",    cls:"sword", r:"N", gen:{b:"humanoid",g:"gSteel",l:"#12305a"}},
 {n:"武器商の剣士",  t:"unit", c:3, a:2, h:3, kw:"cryweapon", cls:"sword", r:"R", gen:{b:"humanoid",g:"gGold",l:"#7a5010"}},
 {n:"研ぎ澄まし",    t:"spell",c:2, spell:"weaponup",         cls:"sword", r:"R"},
 {n:"鋼刃の剣聖",    t:"unit", c:6, a:5, h:6, kw:"crybladed", cls:"sword", r:"SR",gen:{b:"humanoid",g:"gSteel",l:"#12305a",crown:1}},
 {n:"剣聖リオン",    t:"unit", c:7, a:6, h:6, kw:"two",       cls:"sword", r:"L", gen:{b:"humanoid",g:"gGold",l:"#7a5010",crown:1}},
 {n:"石割りの拳士",  t:"unit", c:1, a:1, h:1, kw:"charge", cls:"monk", r:"N", gen:{b:"humanoid",g:"gRed",l:"#70140a"}},
 {n:"円陣の武僧",    t:"unit", c:3, a:3, h:3, kw:"cheer",  cls:"monk", r:"R", gen:{b:"humanoid",g:"gRed",l:"#70140a"}},
 {n:"荒行の求道者",  t:"unit", c:4, a:3, h:5, kw:"enrage", cls:"monk", r:"R", gen:{b:"humanoid",g:"gBrown",l:"#4a3014"}},
 {n:"気合の一喝",    t:"spell",c:3, spell:"buffcharge",    cls:"monk", r:"R"},
 {n:"闘気の化身",    t:"unit", c:6, a:6, h:5, kw:"growth", cls:"monk", r:"SR",gen:{b:"humanoid",g:"gFlame",l:"#8f2403",horn:1}},
 {n:"荷運びの丁稚",  t:"unit", c:1, a:1, h:1, kw:"crymp",   cls:"merchant", r:"R", gen:{b:"humanoid",g:"gGold",l:"#7a5010"}},
 {n:"競りの仕切り屋",t:"unit", c:3, a:3, h:2, kw:"crydraw", cls:"merchant", r:"R", gen:{b:"humanoid",g:"gGold",l:"#7a5010"}},
 {n:"隊商の護衛",    t:"unit", c:4, a:3, h:5, kw:"shield",  cls:"merchant", r:"R", gen:{b:"humanoid",g:"gBrown",l:"#4a3014"}},
 {n:"金貨の雨",      t:"spell",c:5, spell:"draw3heal",      cls:"merchant", r:"R"},
 {n:"豪商ゴルドー",  t:"unit", c:7, a:5, h:8, kw:"crymp",   cls:"merchant", r:"L", gen:{b:"humanoid",g:"gGold",l:"#7a5010",crown:1}},
 {n:"星見のみならい",  t:"unit", c:1, a:1, h:1, kw:"tlink",      cls:"oracle", r:"N", gen:{b:"humanoid",g:"gCobalt",l:"#132356"}},
 {n:"予言のかがみ",    t:"unit", c:2, a:1, h:3, kw:"crydraw",    cls:"oracle", r:"R", gen:{b:"golem",g:"gCobalt",l:"#132356"}},
 {n:"月光の占星術師",  t:"unit", c:4, a:3, h:4, kw:"crytension", cls:"oracle", r:"R", gen:{b:"humanoid",g:"gPurple",l:"#2b0d4d"}},
 {n:"天啓のとばり",    t:"spell",c:3, spell:"scry2",             cls:"oracle", r:"R"},
 {n:"運命神アストラ",  t:"unit", c:7, a:5, h:7, kw:"tlink",      cls:"oracle", r:"L", gen:{b:"humanoid",g:"gCobalt",l:"#132356",crown:1,wing:1}},
 {n:"血啜りコウモリ",t:"unit", c:1, a:1, h:1, kw:"drain",    cls:"dark", r:"N", gen:{b:"beast",g:"gMaroon",l:"#200d12",wing:1}},
 {n:"骸の従僕",      t:"unit", c:2, a:2, h:2, kw:"lastdraw", cls:"dark", r:"N", gen:{b:"undead",g:"gMaroon",l:"#200d12"}},
 {n:"生贄の祭壇",    t:"unit", c:3, a:3, h:2, kw:"cryburn",  cls:"dark", r:"R", gen:{b:"undead",g:"gDark",l:"#07080d"}},
 {n:"呪いの反噬",    t:"spell",c:3, spell:"selfdraw",        cls:"dark", r:"R"},
 {n:"魔剣公ヴェイン",t:"unit", c:6, a:6, h:5, kw:"drain",    cls:"dark", r:"SR",gen:{b:"humanoid",g:"gDark",l:"#07080d",horn:1}},
 {n:"路地のスリ",    t:"unit", c:1, a:1, h:1, kw:"stealth", cls:"thief", r:"N", gen:{b:"humanoid",g:"gGreen",l:"#14611f"}},
 {n:"毒刃の忍び",    t:"unit", c:3, a:3, h:2, kw:"poison",  cls:"thief", r:"N", gen:{b:"humanoid",g:"gOlive",l:"#2b3b0d"}},
 {n:"影渡りの盗賊",  t:"unit", c:4, a:4, h:3, kw:"onatk",   cls:"thief", r:"R", gen:{b:"humanoid",g:"gDark",l:"#07080d"}},
 {n:"けむり玉",      t:"spell",c:2, spell:"stealthall",      cls:"thief", r:"R"},
 {n:"闇夜の首領",    t:"unit", c:6, a:6, h:5, kw:"stealth", cls:"thief", r:"SR",gen:{b:"humanoid",g:"gDark",l:"#07080d",crown:1}},
 {n:"呪文の写し手",  t:"unit", c:1, a:1, h:1, kw:"crydraw",  cls:"mage", r:"N", gen:{b:"humanoid",g:"gPurple",l:"#2b0d4d"}},
 {n:"氷結の魔導書",  t:"unit", c:2, a:1, h:3, kw:"seal",     cls:"mage", r:"R", gen:{b:"golem",g:"gCobalt",l:"#132356"}},
 {n:"業火の魔女",    t:"unit", c:4, a:3, h:4, kw:"cryaoe2",  cls:"mage", r:"R", gen:{b:"humanoid",g:"gFlame",l:"#8f2403"}},
 {n:"炎獄の轟き",    t:"spell",c:6, spell:"aoeface3",        cls:"mage", r:"SR"},
 {n:"大賢者メルヴィン",t:"unit",c:8, a:6, h:8, kw:"cryaoe4", cls:"mage", r:"L", gen:{b:"humanoid",g:"gPurple",l:"#2b0d4d",crown:1}},
 {n:"見習い侍祭",    t:"unit", c:1, a:0, h:2, kw:"cryheal", cls:"priest", r:"N", gen:{b:"humanoid",g:"gBone",l:"#8d8672"}},
 {n:"癒しの泉",      t:"unit", c:3, a:1, h:5, kw:"regen",   cls:"priest", r:"R", gen:{b:"elem",g:"gCobalt",l:"#132356",one:1}},
 {n:"守護の光",      t:"unit", c:4, a:2, h:6, kw:"shield",  cls:"priest", r:"R", gen:{b:"humanoid",g:"gBone",l:"#8d8672",wing:1}},
 {n:"再生の秘跡",    t:"spell",c:4, spell:"healall",         cls:"priest", r:"R"},
 {n:"聖女アルテア",  t:"unit", c:7, a:5, h:8, kw:"cheer",   cls:"priest", r:"L", gen:{b:"humanoid",g:"gBone",l:"#8d8672",crown:1,wing:1}},
"""

NEW_ART = """ "だいちのめぐみ":{i:"rocks",g:"gGreen",l:"#12652f"},
 "追い打ちの矢":{i:"bolt",g:"gSteel",l:"#12305a"},
 "英雄の一撃":{i:"sword",g:"gRed",l:"#70140a"},
 "やまびこの号令":{i:"fist",g:"gCream",l:"#6b5c3d"},
 "粛清の光":{i:"cross",g:"gYellow",l:"#95700a"},
 "忘却の呪い":{i:"rain",g:"gPurple",l:"#3d1c78"},
 "きりさきの短剣":{i:"sword",g:"gSteel",l:"#12305a"},
 "雷神のヤリ":{i:"bolt",g:"gGold",l:"#7a5010"},
 "研ぎ澄まし":{i:"sword",g:"gGold",l:"#7a5010"},
 "気合の一喝":{i:"fist",g:"gRed",l:"#70140a"},
 "金貨の雨":{i:"rain",g:"gGold",l:"#7a5010"},
 "天啓のとばり":{i:"wheel",g:"gCobalt",l:"#132356"},
 "呪いの反噬":{i:"blood",g:"gMaroon",l:"#200d12"},
 "けむり玉":{i:"rain",g:"gDark",l:"#07080d"},
 "炎獄の轟き":{i:"burst",g:"gFlame",l:"#8f2403"},
 "再生の秘跡":{i:"cross",g:"gBone",l:"#8d8672"},
"""

marker = ' {n:"終焉のラグナロク",t:"spell",c:8, spell:"wipe",   r:"L"},'
if marker not in s:
    raise SystemExit("挿入位置が見つかりません")
s = s.replace(marker, marker + "\n" + CARDS.strip("\n"), 1)

art_marker = ' "一閃":{i:"sword",g:"gSteel",l:"#12305a"},'
if art_marker not in s:
    raise SystemExit("アイコン挿入位置が見つかりません")
s = s.replace(art_marker, NEW_ART + art_marker, 1)

io.open(p, "w", encoding="utf-8").write(s)
print("87枚のカードと16のアイコンを追加しました")
