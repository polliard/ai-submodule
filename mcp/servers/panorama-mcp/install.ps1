#Requires -Version 5.1
<#
.SYNOPSIS
    Install panorama-mcp
.DESCRIPTION
    Creates a Python venv, installs the package, and sets up Playwright.
#>

$ErrorActionPreference = "Stop"

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $scriptDir

# Check Python
try {
    $pythonVersion = & python3 --version 2>&1
    Write-Host "==> Found $pythonVersion" -ForegroundColor Green
} catch {
    try {
        $pythonVersion = & python --version 2>&1
        Write-Host "==> Found $pythonVersion" -ForegroundColor Green
        Set-Alias -Name python3 -Value python -Scope Script
    } catch {
        Write-Host "==> python3 not found. Install Python 3.10+ from https://python.org" -ForegroundColor Red
        exit 1
    }
}

# Create venv if it doesn't exist
if (-not (Test-Path ".venv")) {
    Write-Host "==> Creating virtual environment..." -ForegroundColor Green
    & python3 -m venv .venv
} else {
    Write-Host "==> Virtual environment already exists." -ForegroundColor Green
}

# Activate venv
& .venv\Scripts\Activate.ps1

# Install package
Write-Host "==> Installing panorama-mcp..." -ForegroundColor Green
& pip install -e . --quiet

# Install Playwright browsers
Write-Host "==> Installing Playwright browsers..." -ForegroundColor Green
& playwright install chromium

# Verify
try {
    & panorama-mcp --help 2>&1 | Out-Null
    Write-Host "==> Installation complete!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Usage:"
    Write-Host "  panorama-mcp serve"
    Write-Host ""
    Write-Host "Required environment variables:"
    Write-Host "  PANORAMA_URLS         - Comma-separated Panorama URLs"
    Write-Host "  PANORAMA_SSO_ACCOUNT  - SSO account for auto-fill (optional)"
} catch {
    Write-Host "==> Installation may have issues - panorama-mcp not found in PATH" -ForegroundColor Yellow
    Write-Host "    Try: .venv\Scripts\Activate.ps1; pip install -e ."
}
