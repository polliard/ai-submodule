#!/bin/bash
#
# MCP Server Test Runner
#
# Usage:
#   ./run_tests.sh              # Run all tests
#   ./run_tests.sh gitignore    # Run gitignore tests only
#   ./run_tests.sh servicenow   # Run servicenow tests only
#

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

info() { echo -e "${GREEN}==>${NC} $1"; }
warn() { echo -e "${YELLOW}==>${NC} $1"; }
error() { echo -e "${RED}==>${NC} $1"; }

# Setup virtual environment
setup_venv() {
    if [[ ! -d .venv ]]; then
        info "Creating virtual environment..."
        python3 -m venv .venv
    fi

    source .venv/bin/activate

    # Check if pytest is installed
    if ! python -c "import pytest" 2>/dev/null; then
        info "Installing dependencies..."
        pip install -q -r requirements.txt
    fi
}

# Check server availability
check_server() {
    local server=$1
    case $server in
        gitignore)
            if ! command -v gitignore &>/dev/null; then
                warn "gitignore binary not found - tests will be skipped"
                return 1
            fi
            ;;
        servicenow)
            if ! command -v servicenow-mcp &>/dev/null; then
                warn "servicenow-mcp binary not found - tests will be skipped"
                return 1
            fi
            if [[ -z "$SERVICENOW_INSTANCE" ]]; then
                warn "SERVICENOW_INSTANCE not set - tests will be skipped"
                return 1
            fi
            ;;
    esac
    return 0
}

# Run tests
run_tests() {
    local target=${1:-}
    local pytest_args="-v --tb=short"

    if [[ -n "$target" ]]; then
        case $target in
            gitignore)
                pytest_args="$pytest_args test_gitignore.py"
                ;;
            servicenow)
                pytest_args="$pytest_args test_servicenow.py"
                ;;
            *)
                error "Unknown target: $target"
                echo "Usage: $0 [gitignore|servicenow]"
                exit 1
                ;;
        esac
    fi

    info "Running tests..."
    python -m pytest $pytest_args
}

# Main
main() {
    info "MCP Server Tests"
    echo

    setup_venv

    # Show server status
    echo "Server Status:"
    if check_server gitignore; then
        echo "  gitignore:   $(command -v gitignore)"
    else
        echo "  gitignore:   NOT FOUND"
    fi
    if check_server servicenow; then
        echo "  servicenow:  $(command -v servicenow-mcp)"
    else
        echo "  servicenow:  NOT FOUND"
    fi
    echo

    run_tests "$@"
}

main "$@"
