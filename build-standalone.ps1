# art/*.png をすべて data URI として埋め込み、1ファイルで動く公開版を作る
$dir  = $PSScriptRoot
$src  = Join-Path $dir "index.html"
$art  = Join-Path $dir "art"
$out  = Join-Path $dir "arena-card-tactics.html"

$html = [System.IO.File]::ReadAllText($src, [System.Text.Encoding]::UTF8)

# 画像を base64 の対応表としてページ先頭に注入し、art/xxx.png の参照をそれに差し替える
$sb = New-Object System.Text.StringBuilder
[void]$sb.Append("<script>window.__ART__={")
$first = $true
Get-ChildItem $art -Filter *.png | ForEach-Object {
  $b64 = [Convert]::ToBase64String([System.IO.File]::ReadAllBytes($_.FullName))
  if (-not $first) { [void]$sb.Append(",") }
  [void]$sb.Append('"' + $_.Name + '":"data:image/png;base64,' + $b64 + '"')
  $first = $false
}
[void]$sb.Append("};</script>`n")

# 画像パス解決を差し替える（埋め込みがあればそれを使う）
$html = $html.Replace(
  'return `<img src="art/${f}"',
  'const _s=(window.__ART__&&window.__ART__[f])||("art/"+f);' + "`n" + '  return `<img src="${_s}"'
)
$html = $html.Replace(
  'im.src="art/"+f;',
  'im.src=(window.__ART__&&window.__ART__[f])||("art/"+f);'
)

# <head> の直後に注入
$idx = $html.IndexOf("<head>") + 6
$html = $html.Substring(0, $idx) + "`n" + $sb.ToString() + $html.Substring($idx)

[System.IO.File]::WriteAllText($out, $html, (New-Object System.Text.UTF8Encoding $false))
"出力: $out"
"サイズ: {0:N1} MB" -f ((Get-Item $out).Length / 1MB)
