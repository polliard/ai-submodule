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

# Check Python
if ! command -v python3 &>/dev/null; then
    fail "python3 not found. Install Python 3.10+ from https://python.org"
fi

PYTHON_VERSION=$(python3 --version)
info "Found $PYTHON_VERSION"

# Create venv if it doesn't exist
if [ ! -d ".venv" ]; then
    info "Creating virtual environment..."
    python3 -m venv .venv
else
    info "Virtual environment already exists."
fi

# Activate venv
source .venv/bin/activate

# Install package
info "Installing panorama-mcp..."
pip install -e . --quiet

# Install Playwright browsers
info "Installing Playwright browsers..."
playwright install chromium

# Verify installation
if command -v panorama-mcp &>/dev/null; then
    info "Installation complete!"
    echo
    echo "Usage:"
    echo "  panorama-mcp serve"
    echo
    echo "Required environment variables:"
    echo "  PANORAMA_URLS         - Comma-separated Panorama URLs"
    echo "  PANORAMA_SSO_ACCOUNT  - SSO account for auto-fill (optional)"
    echo
    echo "Quick start:"
    echo "  export PANORAMA_URLS=\"https://panoramav2.corp.example.com\""
    echo "  export PANORAMA_SSO_ACCOUNT=\"user@company.com\""
    echo "  panorama-mcp serve"
else
    warn "Installation may have issues - panorama-mcp not found in PATH"
    echo "Try: source .venv/bin/activate && pip install -e ."
fi
