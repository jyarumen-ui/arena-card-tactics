# art/*.png をすべて data URI で埋め込み、1ファイルで動く公開版を作る
import base64, io, os, json

d = os.path.dirname(os.path.abspath(__file__))
src = os.path.join(d, "index.html")
art = os.path.join(d, "art")
out = os.path.join(d, "arena-card-tactics.html")

html = io.open(src, encoding="utf-8").read()

# 画像を名前→data URI の対応表にする
table = {}
for f in sorted(os.listdir(art)):
    if not f.lower().endswith(".png"):
        continue
    with open(os.path.join(art, f), "rb") as fp:
        table[f] = "data:image/png;base64," + base64.b64encode(fp.read()).decode("ascii")

inject = "<script>window.__ART__=" + json.dumps(table) + ";</script>\n"

# 画像パスの解決を「埋め込みがあればそれを使う」に差し替え
a = 'return `<img src="art/${f}"'
b = ('const _s=(window.__ART__&&window.__ART__[f])||("art/"+f);\n'
     '  return `<img src="${_s}"')
assert a in html, "img src の差し替え箇所が見つかりません"
html = html.replace(a, b, 1)

a2 = 'im.src="art/"+f;'
b2 = 'im.src=(window.__ART__&&window.__ART__[f])||("art/"+f);'
assert a2 in html, "preload の差し替え箇所が見つかりません"
html = html.replace(a2, b2, 1)

# 開発用のスナップショット起動フックは公開版では外す
for marker in ['if(location.search.includes("shot=gacha")){ showGacha(openPack(10)); }',
               'if(location.search.includes("shot=deck")){ showDeckEdit("sword"); }']:
    html = html.replace(marker, "")

i = html.index("<head>") + len("<head>")
html = html[:i] + "\n" + inject + html[i:]

io.open(out, "w", encoding="utf-8").write(html)
print("出力:", out)
print("画像:", len(table), "枚")
print("サイズ: %.1f MB" % (os.path.getsize(out) / 1024 / 1024))
