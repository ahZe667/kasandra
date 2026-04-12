$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent $PSScriptRoot
Set-Location $repoRoot

if (-not (Get-Command uv -ErrorAction SilentlyContinue)) {
  throw "uv is required. Install uv first and rerun scripts/repo-check.ps1."
}

if ((Test-Path ".venv") -eq $false) {
  Write-Host "Virtual environment not found. Syncing with uv..."
  if (Test-Path "uv.lock") {
    uv sync --dev --frozen
  } else {
    uv sync --dev
  }
}

$files = @(git ls-files --cached --others --exclude-standard)
if ($files.Count -gt 0) {
  uv tool run pre-commit run --files $files
}

uv run ruff check src tests
uv run pytest
