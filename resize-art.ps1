# 生成イラストをゲーム用サイズ(320px)に縮小して軽量化する
# 元画像は art\orig\ に退避してから処理するので、失敗しても元に戻せる
Add-Type -AssemblyName System.Drawing
$dir  = Join-Path $PSScriptRoot "art"
$orig = Join-Path $dir "orig"
New-Item -ItemType Directory -Force $orig | Out-Null
$size = 320

Get-ChildItem $dir -Filter *.png | ForEach-Object {
  $name = $_.Name
  $src  = $_.FullName
  $before = $_.Length
  $backup = Join-Path $orig $name

  try {
    # 先に元画像を退避
    if (-not (Test-Path $backup)) { Copy-Item $src $backup -Force }

    $img = [System.Drawing.Image]::FromFile($backup)
    if ($img.Width -le $size -and $img.Height -le $size) { $img.Dispose(); return }

    $bmp = New-Object System.Drawing.Bitmap($size, $size, [System.Drawing.Imaging.PixelFormat]::Format32bppArgb)
    $g   = [System.Drawing.Graphics]::FromImage($bmp)
    $g.InterpolationMode = [System.Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic
    $g.PixelOffsetMode   = [System.Drawing.Drawing2D.PixelOffsetMode]::HighQuality
    $g.SmoothingMode     = [System.Drawing.Drawing2D.SmoothingMode]::AntiAlias
    $g.CompositingQuality= [System.Drawing.Drawing2D.CompositingQuality]::HighQuality
    $g.Clear([System.Drawing.Color]::Transparent)

    $scale = [Math]::Min($size / $img.Width, $size / $img.Height)
    $w = [int]($img.Width * $scale); $h = [int]($img.Height * $scale)
    $g.DrawImage($img, [int](($size-$w)/2), [int](($size-$h)/2), $w, $h)
    $g.Flush()
    $g.Dispose()
    $img.Dispose()

    $tmp = Join-Path $env:TEMP ("rz_" + $name)
    $bmp.Save($tmp, [System.Drawing.Imaging.ImageFormat]::Png)
    $bmp.Dispose()

    $newLen = (Get-Item $tmp).Length
    if ($newLen -lt 4096) { throw "出力が壊れています ($newLen bytes)" }   # 保険: 小さすぎたら書き戻さない

    Copy-Item $tmp $src -Force
    Remove-Item $tmp -Force
    "{0}: {1:N0}KB -> {2:N0}KB" -f $name, ($before/1KB), ($newLen/1KB)
  } catch {
    if (Test-Path $backup) { Copy-Item $backup $src -Force }              # 失敗したら元に戻す
    "SKIP $name : $($_.Exception.Message)"
  }
}
"--- 完了 ---"
Get-ChildItem $dir -Filter *.png | ForEach-Object { "{0} : {1:N0}KB" -f $_.Name, ($_.Length/1KB) }
