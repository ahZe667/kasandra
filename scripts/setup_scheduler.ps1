# Kasandra — jednorazowa konfiguracja Windows Task Scheduler.
# Uruchom raz z PowerShell (nie wymaga admina jezeli dla biezacego uzytkownika):
#
#   .\scripts\setup_scheduler.ps1
#
# Po konfiguracji scheduler odpala run_krs.ps1 automatycznie w dni robocze o 07:00.
# Komputer musi byc wlaczony i zalogowany (lub: uruchom z opcja -RunWhenLoggedOff).

param(
    [string]$TaskName   = "Kasandra KRS Daily",
    [string]$Time       = "07:00",
    [switch]$Remove,
    [switch]$RunNow
)

$ProjectDir  = Split-Path -Parent $PSScriptRoot
$ScriptPath  = Join-Path $ProjectDir "scripts\run_krs.ps1"

if ($Remove) {
    Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false -ErrorAction SilentlyContinue
    Write-Host "Usunieto zadanie: $TaskName"
    exit 0
}

if ($RunNow) {
    Write-Host "Uruchamiam teraz: $ScriptPath"
    & powershell.exe -NonInteractive -ExecutionPolicy Bypass -File $ScriptPath
    exit $LASTEXITCODE
}

$Action = New-ScheduledTaskAction `
    -Execute  "powershell.exe" `
    -Argument "-NonInteractive -ExecutionPolicy Bypass -File `"$ScriptPath`""

$Trigger = New-ScheduledTaskTrigger `
    -Weekly `
    -DaysOfWeek Monday, Tuesday, Wednesday, Thursday, Friday `
    -At $Time

$Settings = New-ScheduledTaskSettingsSet `
    -ExecutionTimeLimit  (New-TimeSpan -Minutes 15) `
    -StartWhenAvailable `
    -RunOnlyIfNetworkAvailable

Register-ScheduledTask `
    -TaskName $TaskName `
    -Action   $Action `
    -Trigger  $Trigger `
    -Settings $Settings `
    -RunLevel Limited `
    -Force | Out-Null

Write-Host "Skonfigurowano: '$TaskName'"
Write-Host "  Harmonogram : pn-pt o $Time"
Write-Host "  Skrypt      : $ScriptPath"
Write-Host "  Logi        : $ProjectDir\var\logs\kasandra_YYYY-MM-DD.log"
Write-Host ""
Write-Host "Dostepne opcje:"
Write-Host "  .\scripts\setup_scheduler.ps1 -RunNow     # uruchom natychmiast (test)"
Write-Host "  .\scripts\setup_scheduler.ps1 -Remove     # usun zadanie"
