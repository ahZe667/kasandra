$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent $PSScriptRoot
Set-Location $repoRoot

if (-not (Get-Command uv -ErrorAction SilentlyContinue)) {
  throw "uv is required. Install uv first and rerun scripts/bootstrap.ps1."
}

if (-not (Get-Command npx -ErrorAction SilentlyContinue)) {
  throw "npx is required. Install Node.js first and rerun scripts/bootstrap.ps1."
}

Write-Host "Syncing Python environment with uv..."
if (Test-Path "uv.lock") {
  uv sync --dev --frozen
} else {
  uv sync --dev
}

Write-Host "Installing pre-commit hooks..."
uv tool run pre-commit install

Write-Host "Running initial repository checks..."
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/repo-check.ps1

if ((Test-Path ".env.example") -and -not (Test-Path ".env")) {
  Write-Host "Optional: copy .env.example to .env if you need local runtime overrides."
}

Write-Host "Bootstrap finished."
