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
NC='\033[0m'

info() { echo -e "${GREEN}==>${NC} $1"; }
warn() { echo -e "${YELLOW}==>${NC} $1"; }

# Check Python
if ! command -v python3 &>/dev/null; then
    echo "Error: python3 not found"
    exit 1
fi

info "Installing servicenow-mcp..."

# Install package
pip3 install -e . --quiet

# Install Playwright browsers
info "Installing Playwright browsers..."
playwright install chromium

# Verify installation
if command -v servicenow-mcp &>/dev/null; then
    info "Installation complete!"
    echo
    echo "Usage:"
    echo "  servicenow-mcp serve"
    echo
    echo "Required environment variables:"
    echo "  SERVICENOW_INSTANCE  - Your ServiceNow instance (e.g., mycompany.service-now.com)"
    echo
    echo "Authentication:"
    echo "  Uses browser-based SSO. A browser window will open for authentication."
    echo "  Sessions are cached at ~/.config/servicenow-mcp/ (8-hour expiry)."
else
    warn "Installation may have issues - servicenow-mcp not found in PATH"
    echo "Try: pip3 install -e ."
fi
