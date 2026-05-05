# Kasandra — dzienny fetch KRS.
# Uruchamiany przez Windows Task Scheduler; logguje do var/logs/kasandra_YYYY-MM-DD.log.
# Nie wymaga recznego uruchomienia po pierwszej konfiguracji (setup_scheduler.ps1).

$ProjectDir = Split-Path -Parent $PSScriptRoot
Set-Location $ProjectDir

$env:PYTHONUTF8 = "1"
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

$LogDate  = Get-Date -Format "yyyy-MM-dd"
$LogFile  = Join-Path $ProjectDir "var\logs\kasandra_$LogDate.log"
$Start    = Get-Date -Format "yyyy-MM-dd HH:mm:ss"

"[$Start] === kasandra run --source all ===" | Add-Content -Path $LogFile -Encoding UTF8

uv run kasandra run --source all 2>&1 | ForEach-Object {
    $_ | Add-Content -Path $LogFile -Encoding UTF8
}

$End = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
"[$End] === koniec (exit $LASTEXITCODE) ===" | Add-Content -Path $LogFile -Encoding UTF8
""                                           | Add-Content -Path $LogFile -Encoding UTF8
