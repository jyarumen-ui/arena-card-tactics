Add-Type -AssemblyName System.Drawing
$dir  = "C:\Users\aio\card-tactics\art"
$orig = Join-Path $dir "orig"
$size = 320
New-Item -ItemType Directory -Force $orig | Out-Null

Get-ChildItem $dir -Filter *.png | Where-Object { $_.Length -gt 300KB } | ForEach-Object {
  $name = $_.Name
  $src  = $_.FullName
  $bk   = Join-Path $orig $name
  try {
    if (-not (Test-Path $bk)) { Copy-Item $src $bk -Force }
    $img = [System.Drawing.Image]::FromFile($bk)
    $bmp = New-Object System.Drawing.Bitmap($size, $size, [System.Drawing.Imaging.PixelFormat]::Format32bppArgb)
    $g   = [System.Drawing.Graphics]::FromImage($bmp)
    $g.InterpolationMode  = [System.Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic
    $g.CompositingQuality = [System.Drawing.Drawing2D.CompositingQuality]::HighQuality
    $g.Clear([System.Drawing.Color]::Transparent)
    $sc = [Math]::Min($size / $img.Width, $size / $img.Height)
    $w  = [int]($img.Width * $sc)
    $h  = [int]($img.Height * $sc)
    $x  = [int](($size - $w) / 2)
    $y  = [int](($size - $h) / 2)
    $g.DrawImage($img, $x, $y, $w, $h)
    $g.Dispose(); $img.Dispose()

    $tmp = Join-Path $env:TEMP ("rz_" + $name)
    $bmp.Save($tmp, [System.Drawing.Imaging.ImageFormat]::Png)
    $bmp.Dispose()

    if ((Get-Item $tmp).Length -gt 4096) {
      Copy-Item $tmp $src -Force
      "{0} : {1}KB" -f $name, [int]((Get-Item $src).Length / 1KB)
    } else {
      Copy-Item $bk $src -Force
      "{0} : 失敗のため元に戻しました" -f $name
    }
  } catch {
    if (Test-Path $bk) { Copy-Item $bk $src -Force }
    "{0} : SKIP {1}" -f $name, $_.Exception.Message
  }
}
$f = Get-ChildItem $dir -Filter *.png
"--- {0}枚 合計{1:N1}MB 最小{2}KB ---" -f $f.Count, (($f | Measure-Object Length -Sum).Sum / 1MB), [int](($f | Measure-Object Length -Minimum).Minimum / 1KB)
