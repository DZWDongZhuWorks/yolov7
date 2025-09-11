# COCO 2017 dataset http://cocodataset.org
# 下載指令：在 PowerShell 中執行 .\get_coco.ps1

# 注意：請確保系統使用 PowerShell 5.1 或更新版本，並可使用 Expand-Archive 解壓縮

# 下載並解壓 labels
$d = ".\"             # 解壓縮目的目錄
$url = "https://github.com/ultralytics/yolov5/releases/download/v1.0/"
$f = "coco2017labels-segments.zip"  # 可改為 "coco2017labels.zip"
Write-Output "Downloading $url$f ..."
Start-Job -ScriptBlock {
    param($url, $f, $d)
    Invoke-WebRequest -Uri "$url$f" -OutFile $f
    Expand-Archive -Path $f -DestinationPath $d -Force
    Remove-Item $f
} -ArgumentList $url, $f, $d

# 下載並解壓 images
$d = ".\coco\images"  # 解壓縮目的目錄
# 若目錄不存在，則建立之
if (-Not (Test-Path $d)) {
    New-Item -ItemType Directory -Path $d | Out-Null
}
$url = "http://images.cocodataset.org/zips/"
$f1 = "train2017.zip"  # 約 19G, 118k 張圖片
$f2 = "val2017.zip"    # 約 1G, 5k 張圖片
$f3 = "test2017.zip"   # 約 7G, 41k 張圖片（選擇性下載）

foreach ($f in @($f1, $f2, $f3)) {
    Write-Output "Downloading $url$f ..."
    Start-Job -ScriptBlock {
        param($url, $f, $d)
        Invoke-WebRequest -Uri "$url$f" -OutFile $f
        Expand-Archive -Path $f -DestinationPath $d -Force
        Remove-Item $f
    } -ArgumentList $url, $f, $d
}

# 等待所有背景工作完成
Get-Job | Wait-Job | Out-Null
Get-Job | Remove-Job | Out-Null
Write-Output "全部下載與解壓縮完成！"
