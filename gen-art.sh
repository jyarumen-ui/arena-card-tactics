#!/bin/bash
# カードイラストを順番に生成する（並列はネットワークエラーになるため必ず直列）
ART="C:/Users/aio/card-tactics/art"
SC='python "$env:CODEX_HOME/skills/.system/imagegen/scripts/remove_chroma_key.py" --input <元> --out <保存名> --auto-key border --soft-matte --transparent-threshold 12 --opaque-threshold 220 --despill'

COMMON='【全画像共通】用途=スマホ向けカードバトルゲームのカードイラスト。画風=日本のスマホカードゲーム風、厚塗りの3Dレンダリング調、劇的なリムライト、鮮やかで彩度の高い色、被写体1体のみを中央に全身で配置。背景=完全に均一な #00ff00 の単色（影・グラデーション・床・反射を入れない）。被写体に #00ff00 は使わない。文字ロゴ透かしは一切入れない。既存作品に似せず完全オリジナル。正方形1024x1024。
【必須の後処理】各画像を remove_chroma_key.py で透過してから指定名で保存すること:
'"$SC"'
【内容と保存名】'

run() {
  echo "=== $1 ==="
  codex exec --skip-git-repo-check -C "$ART" "GPT Image 2で画像を生成し、必ず背景を透過して指定名で $ART に保存してください。

$COMMON
$2" </dev/null 2>&1 | tail -3
}

run "リーダー" "leader-mage.png : 紫のローブと大きなとんがり帽子の若い女性魔法使い。手に光る宝珠の杖、周囲に魔法の光。
leader-priest.png : 白と金の法衣をまとった慈愛に満ちた女性僧侶。頭上に光の輪、手に聖なる錫杖。
leader-monk.png : 赤い道着に鉢巻きの筋骨たくましい格闘家。拳に闘気の炎、構えたポーズ。
leader-merchant.png : 金貨をあしらった豪華な衣装の商人。片手に金貨袋、にやりと笑う。"

run "リーダー2" "leader-oracle.png : 青い星柄のローブの占い師の女性。水晶玉を掲げ、周囲に星屑。
leader-dark.png : 黒い鎧の魔剣士。紫の禍々しいオーラ、大鎌を構える。顔は影に隠れ目だけが光る。
leader-thief.png : 緑のフードと口元を覆う布の軽装の盗賊。両手に短剣、身をかがめた俊敏な構え。"

run "低コスト" "koumorin.png : 紫色の小さなコウモリの魔物。大きな翼と丸い目、愛嬌のある顔。
togegame.png : 甲羅に黄色い鋭いトゲが並んだ緑色の大きな亀の魔物。硬そうな守りの姿勢。
salamandra.png : 赤いトカゲ型の魔物。背中に炎のたてがみ、鋭い爪。
bomster.png : 黒い球体の爆弾モンスター。頭に火のついた導火線、いたずらっぽい笑顔。"

run "中コスト" "flowerheal.png : ピンクの花の妖精モンスター。花びらの体、黄色い中心に優しい顔、緑の茎の脚。
rockgolem.png : 岩でできた重厚なゴーレム。四角い体、黄色く光る目、頑丈な腕。
kamaitachi.png : 白いイタチ型の疾風の魔物。鎌のような鋭い爪、風をまとった俊敏な姿。
minarai.png : 見習いの若い魔法使いの少年。とんがり帽子と杖、初々しい表情。"

run "中コスト2" "shadowcat.png : 影に溶ける黒猫の魔物。緑に光る目、しなやかな体、半透明の影のオーラ。
chibidora.png : 緑色の小さな子供のドラゴン。金色の角、丸い体、愛らしい顔。
guardian.png : 巨大な盾そのものが体になった守護者の魔物。青と金の装甲、堅牢な立ち姿。
arrowhunter.png : 弓を構えた獣人のハンター。茶色い毛皮、鋭い目、矢をつがえた姿。"

run "高コスト" "bloodwolf.png : 暗赤色の狼の魔物。赤く光る目、鋭い牙、獰猛な唸り声のポーズ。
griffon.png : 金色の鷲と獅子が合わさった魔獣グリフォン。大きな翼を広げた勇壮な姿。
lancebeetle.png : 青い甲殻の巨大カブトムシ。長く鋭い一本角、突進の構え。
deathlord.png : 金の王冠をかぶった骸骨の魔王。紫に光る眼窩、黒いマント、威圧的な姿。"

run "ボス級" "tyranobreaker.png : 緑色の巨大な肉食恐竜型モンスター。凶暴な牙と鋭い爪、咆哮。
titangolem.png : 灰色の巨石でできた超巨大ゴーレム。山のような体躯、圧倒的な存在感。
ryuoh.png : 紫と黒の鱗を持つ竜王。金の王冠と巨大な翼、最強のボスらしい荘厳な威容。
glacies.png : 氷でできた王のような魔物。透き通る青い氷の体、氷の王冠、冷気のオーラ。
thunderbird.png : 黄色く輝く巨大な雷鳥。雷をまとった翼、鋭い眼光。"

echo "=== 全バッチ完了 ==="
ls -1 "$ART"/*.png | wc -l
