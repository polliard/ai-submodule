#Requires -Version 5.1
<#
.SYNOPSIS
    Install servicenow-mcp
.DESCRIPTION
    Installs the Python package and Playwright browsers.
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
        Write-Host "==> python3 not found. Install Python 3.9+ from https://python.org" -ForegroundColor Red
        exit 1
    }
}

# Install package
Write-Host "==> Installing servicenow-mcp..." -ForegroundColor Green
& pip3 install -e . --quiet

# Install Playwright browsers
Write-Host "==> Installing Playwright browsers..." -ForegroundColor Green
& playwright install chromium

# Verify
try {
    & servicenow-mcp --help 2>&1 | Out-Null
    Write-Host "==> Installation complete!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Usage:"
    Write-Host "  servicenow-mcp serve"
    Write-Host ""
    Write-Host "Required environment variables:"
    Write-Host "  SERVICENOW_INSTANCE  - Your ServiceNow instance (e.g., mycompany.service-now.com)"
    Write-Host ""
    Write-Host "Authentication:"
    Write-Host "  Uses browser-based SSO. A browser window will open for authentication."
    Write-Host "  Sessions are cached at ~/.config/servicenow-mcp/ (8-hour expiry)."
} catch {
    Write-Host "==> Installation may have issues - servicenow-mcp not found in PATH" -ForegroundColor Yellow
    Write-Host "    Try: pip3 install -e ."
}
