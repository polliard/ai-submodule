# gitignore MCP — Install Guide

## Prerequisites

One of:

- **Go 1.23+** (to install from source)
- **curl + tar** (to download a pre-built release binary)

## Manual Install

### Option A: From source (Go required)

```bash
go install github.com/polliard/gitignore/src/cmd/gitignore@latest
```

### Option B: Pre-built binary

```bash
# macOS (Apple Silicon)
curl -L https://github.com/polliard/gitignore/releases/latest/download/gitignore-darwin-arm64.tar.gz | tar xz
sudo mv gitignore /usr/local/bin/

# macOS (Intel)
curl -L https://github.com/polliard/gitignore/releases/latest/download/gitignore-darwin-amd64.tar.gz | tar xz
sudo mv gitignore /usr/local/bin/

# Linux (amd64)
curl -L https://github.com/polliard/gitignore/releases/latest/download/gitignore-linux-amd64.tar.gz | tar xz
sudo mv gitignore /usr/local/bin/
```

### Windows

```powershell
# Download and extract
Invoke-WebRequest -Uri "https://github.com/polliard/gitignore/releases/latest/download/gitignore-windows-amd64.tar.gz" -OutFile gitignore.tar.gz
tar xzf gitignore.tar.gz
Move-Item gitignore.exe "$env:LOCALAPPDATA\Programs\gitignore.exe"
# Add $env:LOCALAPPDATA\Programs to PATH if not already present
```

## Automated Install

```bash
# macOS / Linux
./install.sh

# Windows (PowerShell)
.\install.ps1
```

## Verify

```bash
gitignore --version
gitignore serve   # should start MCP server on stdio
```

## Configuration

### VS Code / Cursor

Add to `.vscode/mcp.json`:

```json
{
    "servers": {
        "gitignore": {
            "type": "stdio",
            "command": "gitignore",
            "args": ["serve"]
        }
    }
}
```

### Optional: `~/.gitignorerc`

```ini
gitignore.template.url = https://github.com/github/gitignore
enable.toptal.gitignore = true
gitignore.default-types = github/go, github/global/macos, github/global/visualstudiocode
```

See [README.md](README.md) for full configuration and tool documentation.
