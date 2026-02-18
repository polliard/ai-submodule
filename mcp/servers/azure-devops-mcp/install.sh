#!/bin/bash
#
# Install azure-devops-mcp
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

# Check Node.js
if ! command -v node &>/dev/null; then
    fail "node not found. Install Node.js 18+ from https://nodejs.org"
fi

NODE_VERSION=$(node --version)
info "Found Node.js $NODE_VERSION"

# Check npx
if ! command -v npx &>/dev/null; then
    fail "npx not found. It should ship with Node.js/npm."
fi

info "Found npx $(npx --version)"

# Verify package downloads
info "Verifying @azure-devops/mcp package..."
if npx -y @azure-devops/mcp --help &>/dev/null; then
    info "Package downloaded and verified."
else
    warn "Package download check returned non-zero (may still work — some MCP servers don't support --help)."
fi

info "Installation complete!"
echo
echo "Usage:"
echo "  npx -y @azure-devops/mcp <org-name>"
echo
echo "No local install needed — npx downloads on demand."
echo "Pass your Azure DevOps organization name as the argument."
