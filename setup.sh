#!/bin/bash
# /Users/tef/Projects/cta/back/setup.sh

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'  # No Color

# Project Directories
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="${PROJECT_ROOT}/venv"

# Logging Function
log() {
    echo -e "${YELLOW}[CTA Backend Setup]${NC} $1"
}

# Error Handling Function
error_exit() {
    echo -e "${RED}Error: $1${NC}" >&2
    exit 1
}

# Prerequisite Checks
check_prerequisites() {
    log "Checking system prerequisites..."

    # Check Python Version
    if ! command -v python3 &> /dev/null; then
        error_exit "Python 3 is not installed. Please install Python 3.10+"
    fi

    PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
    if [[ "$(printf '%s\n' "3.10" "$PYTHON_VERSION" | sort -V | head -n1)" != "3.10" ]]; then
        error_exit "Python 3.10+ is required. Found version: $PYTHON_VERSION"
    fi

    # Check pip
    if ! command -v pip3 &> /dev/null; then
        error_exit "pip3 is not installed. Please install pip3"
    fi

    # Check virtualenv
    if ! command -v virtualenv &> /dev/null; then
        log "Installing virtualenv..."
        pip3 install virtualenv
    fi
}

# Create Virtual Environment
create_venv() {
    log "Creating virtual environment..."
    
    # Remove existing venv if it exists
    if [ -d "$VENV_DIR" ]; then
        rm -rf "$VENV_DIR"
    fi

    # Create new virtual environment
    python3 -m venv "$VENV_DIR"
    
    # Activate the virtual environment
    source "$VENV_DIR/bin/activate"

    # Upgrade pip and setuptools
    pip install --upgrade pip setuptools wheel
}

# Install Project Dependencies
install_dependencies() {
    log "Installing project dependencies..."
    pip install -r "${PROJECT_ROOT}/requirements.txt"
    
    # Development dependencies
    pip install -r "${PROJECT_ROOT}/requirements-dev.txt" || \
        log "No development requirements found."
}

# Configure Development Environment
configure_dev_env() {
    log "Configuring development environment..."
    
    # Copy .env.example to .env if not exists
    if [ ! -f "${PROJECT_ROOT}/.env" ]; then
        cp "${PROJECT_ROOT}/.env.example" "${PROJECT_ROOT}/.env"
        log "Created .env file from example. Please update with your configurations."
    fi
}

# Main Setup Function
main() {
    clear
    echo -e "${GREEN}CTA Backend Development Environment Setup${NC}"
    
    check_prerequisites
    create_venv
    install_dependencies
    configure_dev_env

    log "Setup complete! 🚀"
    echo -e "\n${GREEN}Virtual Environment is ready.${NC}"
    echo -e "${YELLOW}Activate with:${NC} source ${VENV_DIR}/bin/activate"
    echo -e "${YELLOW}Deactivate with:${NC} deactivate"
}

# Run the main setup function
main