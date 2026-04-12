$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent $PSScriptRoot
Set-Location $repoRoot

if (-not (Get-Command uv -ErrorAction SilentlyContinue)) {
  Write-Host "uv not found. Skipping changed-file checks."
  exit 0
}

if (-not (Test-Path ".venv")) {
  Write-Host ".venv not found. Run scripts/bootstrap.ps1 to enable changed-file checks."
  exit 0
}

$files = New-Object System.Collections.Generic.HashSet[string]

$previousErrorActionPreference = $ErrorActionPreference
$ErrorActionPreference = "Continue"
git rev-parse --verify HEAD *> $null
$hasHead = $LASTEXITCODE -eq 0
$ErrorActionPreference = $previousErrorActionPreference

if ($hasHead) {
  $changed = @(
    git diff --name-only HEAD
    git diff --name-only --cached HEAD
    git ls-files --others --exclude-standard
  )
} else {
  $changed = @(git ls-files --modified --others --exclude-standard)
}

foreach ($file in $changed) {
  if ($file -and (Test-Path $file)) {
    [void]$files.Add($file)
  }
}

$fileList = @($files) | Sort-Object
if ($fileList.Count -eq 0) {
  Write-Host "No changed files detected. Skipping pre-commit."
  exit 0
}

uv tool run pre-commit run --files $fileList
