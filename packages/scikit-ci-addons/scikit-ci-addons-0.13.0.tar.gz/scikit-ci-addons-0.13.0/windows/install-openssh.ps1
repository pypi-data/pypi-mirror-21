trap { Write-Error $_; Exit 1 }

Import-Module .\install-utils.ps1 -Force

$downloadDir = "C:/Downloads"

# See https://winscp.net/eng/docs/guide_windows_openssh_server
# Must also open up the port in the firewall

$version = "0.0.9.0"
$archiveName = "OpenSSH-Win64"

Download-URL "https://github.com/PowerShell/Win32-OpenSSH/releases/download/v$version/$archiveName.zip" $downloadDir

$unpackDir = Join-Path "D:\" "Support\openssh"
Extract-Zip (Join-Path $downloadDir "$archiveName.zip") "$unpackDir"

$extractDir = Join-Path "$unpackDir" "$archiveName"
cd "$extractDir"
.\install-sshd.ps1
.\ssh-keygen.exe -A
.\install-sshlsa.ps1
