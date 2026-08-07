# Artifact 公開用: <!doctype>/<html>/<head>/<body> を外し、本文だけの断片にする
import io, os, re

d = os.path.dirname(os.path.abspath(__file__))
src = os.path.join(d, "arena-card-tactics.html")
out = os.path.join(d, "artifact.html")

s = io.open(src, encoding="utf-8").read()

# <head> の中身（title / style / 埋め込み画像スクリプト）を取り出す
head = s[s.index("<head>") + len("<head>"): s.index("</head>")]
body = s[s.index("<body>") + len("<body>"): s.rindex("</body>")]

# meta / doctype 相当は publish 時の骨組みが用意するので落とす
head = re.sub(r'<meta[^>]*>\s*', '', head)

frag = head.strip() + "\n" + body.strip() + "\n"

# 画面いっぱいに敷くため、artifact 側のページ余白を打ち消す
frag = frag.replace(
    "  * { margin:0; padding:0; box-sizing:border-box;",
    "  html,body { margin:0 !important; padding:0 !important; }\n"
    "  * { margin:0; padding:0; box-sizing:border-box;",
    1,
)

io.open(out, "w", encoding="utf-8").write(frag)
print("出力:", out)
print("サイズ: %.1f MB" % (os.path.getsize(out) / 1024 / 1024))
print("title あり:", "<title>" in frag)
