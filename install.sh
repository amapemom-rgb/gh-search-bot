#!/bin/bash
set -e

echo ""
echo "========================================"
echo "   GH-najdi Bot -- Installer"
echo "========================================"
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "ERROR: python3 not found. Please install Python 3.9+."
    exit 1
fi

# Check git
if ! command -v git &> /dev/null; then
    echo "ERROR: git not found. Please install git."
    exit 1
fi

INSTALL_DIR="$HOME/gh-search-bot"

if [ -d "$INSTALL_DIR" ]; then
    echo "Directory $INSTALL_DIR already exists. Updating..."
    cd "$INSTALL_DIR"
    git pull
else
    echo "Cloning repository..."
    git clone https://github.com/amapemom-rgb/gh-search-bot "$INSTALL_DIR"
    cd "$INSTALL_DIR"
fi

echo ""
echo "Running setup wizard..."
echo ""
exec python3 setup.py < /dev/tty
