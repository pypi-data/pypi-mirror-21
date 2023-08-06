trap { Write-Error $_; Exit 1 }

Import-Module .\install-utils.ps1 -Force

$downloadDir = "C:/Downloads"

Download-URL 'https://download.microsoft.com/download/7/9/6/796EF2E4-801B-4FC4-AB28-B59FBF6D907B/VCForPython27.msi' $downloadDir

$filePath = Join-Path $downloadDir "VCForPython27.msi"

Start-Process msiexec -ArgumentList "/a `"$filePath`" ALLUSERS=1 /qb" -NoNewWindow -Wait
