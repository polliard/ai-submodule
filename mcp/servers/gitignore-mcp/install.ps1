#Requires -Version 5.1
<#
.SYNOPSIS
    Install gitignore MCP server
.DESCRIPTION
    Downloads the gitignore binary for Windows or falls back to go install.
#>

$ErrorActionPreference = "Stop"

$repo = "polliard/gitignore"
$tarball = "gitignore-windows-amd64.tar.gz"
$url = "https://github.com/$repo/releases/latest/download/$tarball"
$installDir = "$env:LOCALAPPDATA\Programs"

# Ensure install directory exists
if (-not (Test-Path $installDir)) {
    New-Item -ItemType Directory -Path $installDir -Force | Out-Null
}

function Install-FromBinary {
    Write-Host "==> Downloading $tarball..." -ForegroundColor Green
    $tempFile = Join-Path $env:TEMP $tarball
    try {
        Invoke-WebRequest -Uri $url -OutFile $tempFile -UseBasicParsing
        Write-Host "==> Extracting..." -ForegroundColor Green
        tar xzf $tempFile -C $env:TEMP
        $exePath = Join-Path $env:TEMP "gitignore.exe"
        if (Test-Path $exePath) {
            Move-Item -Force $exePath (Join-Path $installDir "gitignore.exe")
            Remove-Item -Force $tempFile -ErrorAction SilentlyContinue
            return $true
        }
        Remove-Item -Force $tempFile -ErrorAction SilentlyContinue
        return $false
    } catch {
        Write-Host "==> Binary download failed: $_" -ForegroundColor Yellow
        Remove-Item -Force $tempFile -ErrorAction SilentlyContinue
        return $false
    }
}

function Install-FromSource {
    try {
        $goVersion = & go version 2>&1
        Write-Host "==> Found $goVersion" -ForegroundColor Green
    } catch {
        Write-Host "==> Neither binary download nor Go are available." -ForegroundColor Red
        Write-Host "    Install Go 1.23+ or download the binary manually." -ForegroundColor Red
        exit 1
    }
    Write-Host "==> Installing from source via go install..." -ForegroundColor Green
    & go install "github.com/$repo/src/cmd/gitignore@latest"
}

# Try binary first, fall back to source
if (-not (Install-FromBinary)) {
    Write-Host "==> Falling back to go install..." -ForegroundColor Yellow
    Install-FromSource
}

# Add to PATH if needed
$destExe = Join-Path $installDir "gitignore.exe"
if (Test-Path $destExe) {
    $userPath = [Environment]::GetEnvironmentVariable("Path", "User")
    if ($userPath -notlike "*$installDir*") {
        Write-Host "==> Adding $installDir to user PATH..." -ForegroundColor Green
        [Environment]::SetEnvironmentVariable("Path", "$userPath;$installDir", "User")
        $env:Path = "$env:Path;$installDir"
    }
}

# Verify
try {
    $version = & gitignore --version 2>&1
    Write-Host "==> Installation complete!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Version: $version"
    Write-Host ""
    Write-Host "Usage:"
    Write-Host "  gitignore serve    # Start MCP server"
    Write-Host "  gitignore list     # List templates"
    Write-Host "  gitignore add go   # Add a template"
} catch {
    Write-Host "==> gitignore not found in PATH." -ForegroundColor Yellow
    Write-Host "    If installed via 'go install', ensure GOPATH\bin is in your PATH."
}
