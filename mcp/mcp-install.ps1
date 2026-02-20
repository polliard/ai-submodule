#Requires -Version 5.1
<#
.SYNOPSIS
    mcp-install — unified installer for MCP servers
.DESCRIPTION
    Installs and configures MCP servers. Run without arguments to see available servers.
.PARAMETER Server
    The server to install (azure-devops-mcp, gitignore-mcp, panorama-mcp, servicenow-mcp)
.PARAMETER Org
    Azure DevOps organization name (azure-devops-mcp only)
.PARAMETER Urls
    Comma-separated Panorama URLs (panorama-mcp only)
.PARAMETER SsoAccount
    SSO account for auto-fill (panorama-mcp only, optional)
.PARAMETER Instance
    ServiceNow instance hostname (servicenow-mcp only)
.EXAMPLE
    .\mcp-install.ps1 azure-devops-mcp -Org contoso
.EXAMPLE
    .\mcp-install.ps1 servicenow-mcp -Instance mycompany.service-now.com
#>

param(
    [Parameter(Position = 0)]
    [string]$Server,

    [string]$Org,
    [string]$Urls,
    [string]$SsoAccount,
    [string]$Instance
)

$ErrorActionPreference = "Stop"
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$serversDir = Join-Path $scriptDir "servers"

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
function Write-Info  { param([string]$msg) Write-Host "==> $msg" -ForegroundColor Green }
function Write-Warn  { param([string]$msg) Write-Host "==> $msg" -ForegroundColor Yellow }
function Write-Fail  { param([string]$msg) Write-Host "==> $msg" -ForegroundColor Red; exit 1 }
function Write-Header { param([string]$msg) Write-Host "`n$msg" -ForegroundColor Cyan }

function Read-Required {
    param([string]$Prompt, [string]$Current)
    if ($Current) { return $Current }
    while ($true) {
        $input = Read-Host "? $Prompt"
        if ($input) { return $input }
        Write-Host "  This field is required." -ForegroundColor Red
    }
}

function Read-Optional {
    param([string]$Prompt, [string]$Current)
    if ($Current) { return $Current }
    $input = Read-Host "? $Prompt (optional, press Enter to skip)"
    return $input
}

# ---------------------------------------------------------------------------
# Usage
# ---------------------------------------------------------------------------
function Show-Usage {
    Write-Host "mcp-install" -ForegroundColor White -NoNewline
    Write-Host " - unified installer for MCP servers"
    Write-Host ""
    Write-Host "Usage:" -ForegroundColor White
    Write-Host "  .\mcp-install.ps1 <server> [options]"
    Write-Host ""
    Write-Host "Available servers:" -ForegroundColor White
    Write-Host ""
    Write-Host "  azure-devops-mcp" -ForegroundColor Cyan -NoNewline
    Write-Host "   Query Azure DevOps work items, repos, pipelines"
    Write-Host "    Prerequisites:   Node.js 18+"
    Write-Host "    Options:         " -NoNewline
    Write-Host "-Org" -ForegroundColor Green -NoNewline
    Write-Host " <name>        Azure DevOps organization " -NoNewline
    Write-Host "(prompted if omitted)" -ForegroundColor DarkGray
    Write-Host ""
    Write-Host "  gitignore-mcp" -ForegroundColor Cyan -NoNewline
    Write-Host "      Manage .gitignore files using templates"
    Write-Host "    Prerequisites:   Go 1.23+ or curl"
    Write-Host "    Options:         " -NoNewline
    Write-Host "(none)" -ForegroundColor DarkGray
    Write-Host ""
    Write-Host "  panorama-mcp" -ForegroundColor Cyan -NoNewline
    Write-Host "       Palo Alto Panorama management via browser SSO"
    Write-Host "    Prerequisites:   Python 3.10+, Microsoft Edge"
    Write-Host "    Options:         " -NoNewline
    Write-Host "-Urls" -ForegroundColor Green -NoNewline
    Write-Host " <urls>       Comma-separated Panorama URLs " -NoNewline
    Write-Host "(prompted if omitted)" -ForegroundColor DarkGray
    Write-Host "                     " -NoNewline
    Write-Host "-SsoAccount" -ForegroundColor Green -NoNewline
    Write-Host " <email>  SSO account for auto-fill " -NoNewline
    Write-Host "(optional)" -ForegroundColor DarkGray
    Write-Host ""
    Write-Host "  servicenow-mcp" -ForegroundColor Cyan -NoNewline
    Write-Host "     ServiceNow CMDB, incidents, changes via SSO"
    Write-Host "    Prerequisites:   Python 3.9+"
    Write-Host "    Options:         " -NoNewline
    Write-Host "-Instance" -ForegroundColor Green -NoNewline
    Write-Host " <host>   ServiceNow instance " -NoNewline
    Write-Host "(prompted if omitted)" -ForegroundColor DarkGray
    Write-Host ""
    Write-Host "Examples:" -ForegroundColor White
    Write-Host "  .\mcp-install.ps1 azure-devops-mcp -Org contoso"
    Write-Host "  .\mcp-install.ps1 gitignore-mcp"
    Write-Host "  .\mcp-install.ps1 panorama-mcp -Urls https://panoramav2.example.com"
    Write-Host "  .\mcp-install.ps1 servicenow-mcp -Instance mycompany.service-now.com"
    exit 0
}

# ---------------------------------------------------------------------------
# Server installers
# ---------------------------------------------------------------------------
function Install-AzureDevopsMcp {
    Write-Header "Installing azure-devops-mcp"

    $script:Org = Read-Required "Azure DevOps organization name (e.g. contoso)" $Org

    Write-Info "Running installer..."
    & (Join-Path $serversDir "azure-devops-mcp\install.ps1")

    Write-Header "Usage"
    Write-Host "  npx -y @azure-devops/mcp $($script:Org)"
    Write-Host ""

    Write-Header "VS Code setup"
    Write-Host "Merge this into .vscode\mcp.json:"
    Write-Host ""
    Write-Host @"
{
    "servers": {
        "ado": {
            "type": "stdio",
            "command": "npx",
            "args": ["-y", "@azure-devops/mcp", "$($script:Org)"]
        }
    }
}
"@
    Write-Host ""
}

function Install-GitignoreMcp {
    Write-Header "Installing gitignore-mcp"

    Write-Info "Running installer..."
    & (Join-Path $serversDir "gitignore-mcp\install.ps1")

    Write-Header "VS Code setup"
    Write-Host "Merge this into .vscode\mcp.json:"
    Write-Host ""
    Write-Host @"
{
    "servers": {
        "gitignore": {
            "type": "stdio",
            "command": "gitignore",
            "args": ["serve"]
        }
    }
}
"@
    Write-Host ""
}

function Install-PanoramaMcp {
    Write-Header "Installing panorama-mcp"

    $script:Urls = Read-Required "Panorama URL(s), comma-separated (e.g. https://panoramav2.example.com)" $Urls
    $script:SsoAccount = Read-Optional "SSO account for auto-fill (e.g. user@company.com)" $SsoAccount

    Write-Info "Running installer..."
    & (Join-Path $serversDir "panorama-mcp\install.ps1")

    Write-Header "Configuration"
    Write-Host "Add these to your environment:"
    Write-Host ""
    Write-Host "  `$env:PANORAMA_URLS = `"$($script:Urls)`""
    if ($script:SsoAccount) {
        Write-Host "  `$env:PANORAMA_SSO_ACCOUNT = `"$($script:SsoAccount)`""
    }
    Write-Host ""

    $ssoLine = ""
    if ($script:SsoAccount) {
        $ssoLine = "`n                `"PANORAMA_SSO_ACCOUNT`": `"$($script:SsoAccount)`","
    }

    Write-Header "VS Code setup"
    Write-Host "Merge this into .vscode\mcp.json:"
    Write-Host ""
    Write-Host @"
{
    "servers": {
        "panorama": {
            "command": "panorama-mcp",
            "args": ["serve", "--no-preauth"],
            "env": {
                "PANORAMA_URLS": "$($script:Urls)",$ssoLine
                "PANORAMA_HEADLESS": "false"
            }
        }
    }
}
"@
    Write-Host ""
}

function Install-ServicenowMcp {
    Write-Header "Installing servicenow-mcp"

    $script:Instance = Read-Required "ServiceNow instance hostname (e.g. mycompany.service-now.com)" $Instance

    Write-Info "Running installer..."
    & (Join-Path $serversDir "servicenow-mcp\install.ps1")

    Write-Header "Configuration"
    Write-Host "Add this to your environment:"
    Write-Host ""
    Write-Host "  `$env:SERVICENOW_INSTANCE = `"$($script:Instance)`""
    Write-Host ""

    Write-Header "VS Code setup"
    Write-Host "Merge this into .vscode\mcp.json:"
    Write-Host ""
    Write-Host @"
{
    "servers": {
        "servicenow": {
            "type": "stdio",
            "command": "servicenow-mcp",
            "args": ["serve"],
            "env": {
                "SERVICENOW_INSTANCE": "$($script:Instance)"
            }
        }
    }
}
"@
    Write-Host ""
}

# ===========================================================================
# Main
# ===========================================================================

if (-not $Server) {
    Show-Usage
}

switch ($Server) {
    "azure-devops-mcp" { Install-AzureDevopsMcp }
    "gitignore-mcp"    { Install-GitignoreMcp }
    "panorama-mcp"     { Install-PanoramaMcp }
    "servicenow-mcp"   { Install-ServicenowMcp }
    default {
        Write-Fail "Unknown server: $Server`nRun '.\mcp-install.ps1' with no arguments to see available servers."
    }
}
