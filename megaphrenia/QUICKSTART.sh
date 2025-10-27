#!/bin/bash
# Quick start script for Megaphrenia
# Run this to set up and test the package

set -e  # Exit on error

echo "=========================================="
echo "Megaphrenia Quick Start"
echo "=========================================="
echo ""

# Check Python version
echo "Checking Python version..."
python_version=$(python3 --version 2>&1 | grep -oP '\d+\.\d+' | head -1)
echo "Python version: $python_version"

if [ $(echo "$python_version < 3.8" | bc) -eq 1 ]; then
    echo "❌ Error: Python 3.8 or higher required"
    exit 1
fi
echo "✅ Python version OK"
echo ""

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo "✅ Virtual environment created"
else
    echo "✅ Virtual environment already exists"
fi
echo ""

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate
echo "✅ Virtual environment activated"
echo ""

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip -q
echo "✅ pip upgraded"
echo ""

# Install package in editable mode
echo "Installing megaphrenia in editable mode..."
pip install -e . -q
echo "✅ Package installed"
echo ""

# Install dev dependencies
echo "Installing development dependencies..."
pip install -r requirements-dev.txt -q
echo "✅ Dev dependencies installed"
echo ""

# Verify installation
echo "Verifying installation..."
python -c "from megaphrenia.core import Psychon; print('✅ Core module working')"
python -c "from megaphrenia.circuits import HalfAdder; print('✅ Circuits module working')"
python -c "from megaphrenia.integration import SEntropyNavigator; print('✅ Integration module working')"
echo ""

# Run a quick demo
echo "=========================================="
echo "Running Quick Demo: Moon Landing"
echo "=========================================="
echo ""
python -m megaphrenia.integration.moon_landing

echo ""
echo "=========================================="
echo "Setup Complete! 🚀"
echo "=========================================="
echo ""
echo "Next steps:"
echo "  1. Activate venv: source venv/bin/activate"
echo "  2. Run demos: python -m megaphrenia.integration.moon_landing"
echo "  3. Run tests: pytest"
echo "  4. Start coding!"
echo ""
echo "Documentation:"
echo "  - README.md"
echo "  - INSTALL.md"
echo "  - docs/INTEGRATION_COMPLETE.md"
echo ""

