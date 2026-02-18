#!/bin/bash
#
# Install gitignore MCP server
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

REPO="polliard/gitignore"
INSTALL_DIR="/usr/local/bin"

# Detect OS and architecture
OS="$(uname -s | tr '[:upper:]' '[:lower:]')"
ARCH="$(uname -m)"

case "$ARCH" in
    x86_64)  ARCH="amd64" ;;
    aarch64|arm64) ARCH="arm64" ;;
    *) ARCH="amd64" ;;
esac

info "Detected platform: ${OS}-${ARCH}"

# Try binary download first
TARBALL="gitignore-${OS}-${ARCH}.tar.gz"
URL="https://github.com/${REPO}/releases/latest/download/${TARBALL}"

download_binary() {
    info "Downloading ${TARBALL}..."
    if curl -fsSL "$URL" -o "/tmp/${TARBALL}"; then
        info "Extracting..."
        tar xzf "/tmp/${TARBALL}" -C /tmp
        info "Installing to ${INSTALL_DIR} (may require sudo)..."
        if [ -w "$INSTALL_DIR" ]; then
            mv /tmp/gitignore "$INSTALL_DIR/gitignore"
        else
            sudo mv /tmp/gitignore "$INSTALL_DIR/gitignore"
        fi
        rm -f "/tmp/${TARBALL}"
        return 0
    else
        warn "Binary download failed for ${OS}-${ARCH}."
        rm -f "/tmp/${TARBALL}"
        return 1
    fi
}

install_from_source() {
    if ! command -v go &>/dev/null; then
        fail "Neither binary download nor Go are available. Install Go 1.23+ or download the binary manually."
    fi
    info "Installing from source via go install..."
    go install "github.com/${REPO}/src/cmd/gitignore@latest"
}

# Try binary first, fall back to source
if ! download_binary; then
    warn "Falling back to go install..."
    install_from_source
fi

# Verify
if command -v gitignore &>/dev/null; then
    info "Installation complete!"
    echo
    echo "Version: $(gitignore --version 2>&1 || echo 'unknown')"
    echo
    echo "Usage:"
    echo "  gitignore serve    # Start MCP server"
    echo "  gitignore list     # List templates"
    echo "  gitignore add go   # Add a template"
else
    warn "gitignore binary not found in PATH."
    echo "If installed via 'go install', ensure \$GOPATH/bin is in your PATH."
fi
