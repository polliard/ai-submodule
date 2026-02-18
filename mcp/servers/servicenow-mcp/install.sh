#!/bin/bash
#
# Install servicenow-mcp
#

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

info() { echo -e "${GREEN}==>${NC} $1"; }
warn() { echo -e "${YELLOW}==>${NC} $1"; }
fail() { echo -e "${RED}==>${NC} $1"; exit 1; }

# Check Python version (require 3.9+)
if ! command -v python3 &>/dev/null; then
    fail "python3 not found. Install Python 3.9+ from https://python.org"
fi

PYTHON_VERSION=$(python3 --version)
PYTHON_MINOR=$(python3 -c "import sys; print(sys.version_info.minor)")
if [ "$PYTHON_MINOR" -lt 9 ]; then
    fail "Python 3.9+ required, found $PYTHON_VERSION"
fi
info "Found $PYTHON_VERSION"

# Create or recreate venv if broken
VENV_OK=false
if [ -d ".venv" ]; then
    if .venv/bin/python --version &>/dev/null; then
        VENV_OK=true
        info "Virtual environment OK."
    else
        warn "Virtual environment has a stale interpreter — recreating..."
        rm -rf .venv
    fi
fi

if [ "$VENV_OK" = false ]; then
    info "Creating virtual environment..."
    python3 -m venv .venv
fi

# Install package using the venv's pip directly (avoids externally-managed-environment errors)
info "Installing servicenow-mcp..."
.venv/bin/pip install -e . --quiet

# Install Playwright browsers
info "Installing Playwright browsers..."
.venv/bin/playwright install chromium

# Verify installation
if .venv/bin/servicenow-mcp --help &>/dev/null; then
    info "Installation complete!"
    echo
    echo "Usage:"
    echo "  .venv/bin/servicenow-mcp serve"
    echo
    echo "Required environment variables:"
    echo "  SERVICENOW_INSTANCE  - Your ServiceNow instance (e.g., mycompany.service-now.com)"
    echo
    echo "Authentication:"
    echo "  Uses browser-based SSO. A browser window will open for authentication."
    echo "  Sessions are cached at ~/.config/servicenow-mcp/ (8-hour expiry)."
    echo
    echo "VS Code / Copilot (add to .vscode/mcp.json):"
    echo "  {"
    echo "    \"servers\": {"
    echo "      \"servicenow\": {"
    echo "        \"type\": \"stdio\","
    echo "        \"command\": \"${SCRIPT_DIR}/.venv/bin/servicenow-mcp\","
    echo "        \"args\": [\"serve\", \"--no-preauth\"],"
    echo "        \"env\": {"
    echo "          \"SERVICENOW_INSTANCE\": \"mycompany.service-now.com\""
    echo "        }"
    echo "      }"
    echo "    }"
    echo "  }"
else
    fail "Installation failed — servicenow-mcp not found in .venv/bin/"
fi
