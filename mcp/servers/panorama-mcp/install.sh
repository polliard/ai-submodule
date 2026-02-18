#!/bin/bash
#
# Install panorama-mcp
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

# Check Python version (require 3.10+)
if ! command -v python3 &>/dev/null; then
    fail "python3 not found. Install Python 3.10+ from https://python.org"
fi

PYTHON_VERSION=$(python3 --version)
PYTHON_MINOR=$(python3 -c "import sys; print(sys.version_info.minor)")
if [ "$PYTHON_MINOR" -lt 10 ]; then
    fail "Python 3.10+ required, found $PYTHON_VERSION"
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

# Install package using the venv's pip directly (avoids activate issues)
info "Installing panorama-mcp..."
.venv/bin/pip install -e . --quiet

# Install Playwright browsers
info "Installing Playwright browsers..."
.venv/bin/playwright install chromium

# Verify installation
if .venv/bin/panorama-mcp --help &>/dev/null; then
    info "Installation complete!"
    echo
    echo "Usage:"
    echo "  .venv/bin/panorama-mcp serve"
    echo
    echo "Required environment variables:"
    echo "  PANORAMA_URLS         - Comma-separated Panorama URLs"
    echo "  PANORAMA_SSO_ACCOUNT  - SSO account for auto-fill (optional)"
    echo "  PANORAMA_HEADLESS     - Set to 'false' for visible browser (optional)"
    echo
    echo "VS Code / Copilot (add to .vscode/mcp.json):"
    echo "  {"
    echo "    \"servers\": {"
    echo "      \"panorama\": {"
    echo "        \"type\": \"stdio\","
    echo "        \"command\": \"${SCRIPT_DIR}/.venv/bin/python\","
    echo "        \"args\": [\"-m\", \"panorama_mcp\", \"serve\", \"--no-preauth\"],"
    echo "        \"env\": {"
    echo "          \"PANORAMA_URLS\": \"https://panoramav2.corp.example.com\","
    echo "          \"PANORAMA_SSO_ACCOUNT\": \"user@company.com\","
    echo "          \"PANORAMA_HEADLESS\": \"false\""
    echo "        }"
    echo "      }"
    echo "    }"
    echo "  }"
else
    fail "Installation failed — panorama-mcp not found in .venv/bin/"
fi
