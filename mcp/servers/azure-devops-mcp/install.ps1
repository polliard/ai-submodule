#Requires -Version 5.1
<#
.SYNOPSIS
    Install azure-devops-mcp
.DESCRIPTION
    Verifies Node.js/npx prerequisites and confirms the MCP package downloads.
#>

$ErrorActionPreference = "Stop"

# Check Node.js
try {
    $nodeVersion = & node --version 2>&1
    Write-Host "==> Found Node.js $nodeVersion" -ForegroundColor Green
} catch {
    Write-Host "==> node not found. Install Node.js 18+ from https://nodejs.org" -ForegroundColor Red
    exit 1
}

# Check npx
try {
    $npxVersion = & npx --version 2>&1
    Write-Host "==> Found npx $npxVersion" -ForegroundColor Green
} catch {
    Write-Host "==> npx not found. It should ship with Node.js/npm." -ForegroundColor Red
    exit 1
}

# Verify package downloads
Write-Host "==> Verifying @azure-devops/mcp package..." -ForegroundColor Green
try {
    & npx -y @azure-devops/mcp --help 2>&1 | Out-Null
    Write-Host "==> Package downloaded and verified." -ForegroundColor Green
} catch {
    Write-Host "==> Package download check returned non-zero (may still work)." -ForegroundColor Yellow
}

Write-Host "==> Installation complete!" -ForegroundColor Green
Write-Host ""
Write-Host "Usage:"
Write-Host "  npx -y @azure-devops/mcp <org-name>"
Write-Host ""
Write-Host "No local install needed - npx downloads on demand."
Write-Host "Pass your Azure DevOps organization name as the argument."
