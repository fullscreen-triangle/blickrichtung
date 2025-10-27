# Quick start script for Megaphrenia (PowerShell)
# Run this to set up and test the package

$ErrorActionPreference = "Stop"

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "Megaphrenia Quick Start" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

# Check Python version
Write-Host "Checking Python version..." -ForegroundColor Yellow
$pythonVersion = python --version 2>&1 | Select-String -Pattern '\d+\.\d+' | ForEach-Object { $_.Matches.Value }
Write-Host "Python version: $pythonVersion" -ForegroundColor Green

$versionParts = $pythonVersion.Split('.')
$major = [int]$versionParts[0]
$minor = [int]$versionParts[1]

if ($major -lt 3 -or ($major -eq 3 -and $minor -lt 8)) {
    Write-Host "❌ Error: Python 3.8 or higher required" -ForegroundColor Red
    exit 1
}
Write-Host "✅ Python version OK" -ForegroundColor Green
Write-Host ""

# Create virtual environment if it doesn't exist
if (-not (Test-Path "venv")) {
    Write-Host "Creating virtual environment..." -ForegroundColor Yellow
    python -m venv venv
    Write-Host "✅ Virtual environment created" -ForegroundColor Green
} else {
    Write-Host "✅ Virtual environment already exists" -ForegroundColor Green
}
Write-Host ""

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
& .\venv\Scripts\Activate.ps1
Write-Host "✅ Virtual environment activated" -ForegroundColor Green
Write-Host ""

# Upgrade pip
Write-Host "Upgrading pip..." -ForegroundColor Yellow
pip install --upgrade pip --quiet
Write-Host "✅ pip upgraded" -ForegroundColor Green
Write-Host ""

# Install package in editable mode
Write-Host "Installing megaphrenia in editable mode..." -ForegroundColor Yellow
pip install -e . --quiet
Write-Host "✅ Package installed" -ForegroundColor Green
Write-Host ""

# Install dev dependencies
Write-Host "Installing development dependencies..." -ForegroundColor Yellow
pip install -r requirements-dev.txt --quiet
Write-Host "✅ Dev dependencies installed" -ForegroundColor Green
Write-Host ""

# Verify installation
Write-Host "Verifying installation..." -ForegroundColor Yellow
python -c "from megaphrenia.core import Psychon; print('✅ Core module working')"
python -c "from megaphrenia.circuits import HalfAdder; print('✅ Circuits module working')"
python -c "from megaphrenia.integration import SEntropyNavigator; print('✅ Integration module working')"
Write-Host ""

# Run a quick demo
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "Running Quick Demo: Moon Landing" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""
python -m megaphrenia.integration.moon_landing

Write-Host ""
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "Setup Complete! 🚀" -ForegroundColor Green
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "  1. Activate venv: .\venv\Scripts\Activate.ps1"
Write-Host "  2. Run demos: python -m megaphrenia.integration.moon_landing"
Write-Host "  3. Run tests: pytest"
Write-Host "  4. Start coding!"
Write-Host ""
Write-Host "Documentation:" -ForegroundColor Yellow
Write-Host "  - README.md"
Write-Host "  - INSTALL.md"
Write-Host "  - docs/INTEGRATION_COMPLETE.md"
Write-Host ""

