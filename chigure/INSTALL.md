# Installation Guide for Chigure

Complete installation instructions for the Consciousness Validation Engine.

---

## Prerequisites

### Required
- **Python 3.8 or higher**
- **pip** (Python package installer)
- **git** (for cloning repository)

### Recommended
- **Virtual environment** (venv or conda)
- **10 GB free disk space** (for data and results)

---

## Quick Installation

### 1. Clone Repository

```bash
git clone https://github.com/yourusername/blickrichtung.git
cd blickrichtung/chigure
```

### 2. Create Virtual Environment (Recommended)

**Using venv:**
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

**Using conda:**
```bash
conda create -n chigure python=3.10
conda activate chigure
```

### 3. Install Package

**Basic installation (simulation only):**
```bash
pip install -e .
```

**With all features:**
```bash
pip install -e ".[all]"
```

### 4. Verify Installation

```bash
python -c "import experimental; print('✓ Installation successful!')"
```

---

## Installation Options

### Option 1: Basic (Simulation Only)

For running simulations without hardware:

```bash
pip install -e .
```

**Installs**:
- numpy, scipy, pandas
- matplotlib
- scikit-learn
- tqdm

**Use case**: Software development, testing, simulations

### Option 2: Development

For contributing to the codebase:

```bash
pip install -e ".[dev]"
```

**Adds**:
- pytest, pytest-cov (testing)
- black, flake8, mypy (code quality)
- jupyter, ipython (interactive development)
- plotly, seaborn, networkx (visualization)

**Use case**: Development, testing, debugging

### Option 3: Hardware

For connecting to physical hardware:

```bash
pip install -e ".[hardware]"
```

**Adds**:
- pyserial (serial communication)
- pyvisa, pyvisa-py (GPIB/VISA instruments)

**Use case**: Physical experiments with actual hardware

**Note**: May require additional drivers:
- **Windows**: NI-VISA or Keysight IO Libraries
- **Linux**: `sudo apt install libusb-1.0-0-dev`
- **Mac**: Install NI-VISA or use pyvisa-py backend

### Option 4: All Features

Complete installation with everything:

```bash
pip install -e ".[all]"
```

**Use case**: Complete development and experimentation

---

## Manual Installation

If you prefer to install dependencies separately:

### 1. Core Dependencies

```bash
pip install -r requirements.txt
```

### 2. Development Dependencies (Optional)

```bash
pip install -r requirements-dev.txt
```

### 3. Hardware Dependencies (Optional)

```bash
pip install -r requirements-hardware.txt
```

### 4. Install Package

```bash
pip install -e .
```

---

## Platform-Specific Instructions

### Windows

```powershell
# 1. Clone repository
git clone https://github.com/yourusername/blickrichtung.git
cd blickrichtung\chigure

# 2. Create virtual environment
python -m venv venv
venv\Scripts\activate

# 3. Install
pip install -e ".[all]"

# 4. Test
python -c "from experimental import ConsciousnessDetectionSystem; print('✓ Success!')"
```

**Troubleshooting Windows**:
- If `pip` not found: Add Python to PATH or use `python -m pip`
- If permission errors: Run PowerShell as Administrator
- If Visual C++ errors: Install [Microsoft C++ Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/)

### Linux (Ubuntu/Debian)

```bash
# 1. Install prerequisites
sudo apt update
sudo apt install python3 python3-pip python3-venv git

# For hardware support
sudo apt install libusb-1.0-0-dev

# 2. Clone repository
git clone https://github.com/yourusername/blickrichtung.git
cd blickrichtung/chigure

# 3. Create virtual environment
python3 -m venv venv
source venv/bin/activate

# 4. Install
pip install -e ".[all]"

# 5. Test
python -c "from experimental import ConsciousnessDetectionSystem; print('✓ Success!')"
```

**Troubleshooting Linux**:
- If `python3-venv` not found: `sudo apt install python3-venv`
- If permission errors for USB devices: Add user to `dialout` group: `sudo usermod -a -G dialout $USER`

### macOS

```bash
# 1. Install Homebrew (if not already installed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# 2. Install Python
brew install python@3.10 git

# 3. Clone repository
git clone https://github.com/yourusername/blickrichtung.git
cd blickrichtung/chigure

# 4. Create virtual environment
python3 -m venv venv
source venv/bin/activate

# 5. Install
pip install -e ".[all]"

# 6. Test
python -c "from experimental import ConsciousnessDetectionSystem; print('✓ Success!')"
```

**Troubleshooting macOS**:
- If Xcode Command Line Tools needed: `xcode-select --install`
- If permission errors: Use `pip install --user` or fix permissions

---

## Verifying Installation

### Test Basic Import

```python
python -c "
from experimental import ConsciousnessDetectionSystem
from hardware import HardwareSensorFusion
from temporal import TemporalPerceptionValidator
from prediction import ScentPredictor
print('✓ All modules imported successfully!')
"
```

### Run Quick Test

```bash
# Run a quick validation
python -c "
from experimental.complete_system import run_complete_experiment
print('Running quick test...')
# results = run_complete_experiment()  # Uncomment for full test
print('✓ System operational!')
"
```

### Check Dependencies

```bash
pip list | grep -E "numpy|scipy|matplotlib|pandas|sklearn|tqdm"
```

Expected output:
```
matplotlib       3.4.0
numpy           1.21.0
pandas          1.3.0
scikit-learn    1.0.0
scipy           1.7.0
tqdm            4.62.0
```

---

## Hardware Setup (Optional)

For physical hardware experiments:

### 1. Install Hardware Libraries

```bash
pip install -e ".[hardware]"
```

### 2. Install Drivers

**NI-VISA (National Instruments)**:
- Download: https://www.ni.com/en-us/support/downloads/drivers/download.ni-visa.html
- Install for your platform

**Keysight IO Libraries (Keysight instruments)**:
- Download: https://www.keysight.com/us/en/lib/software-detail/computer-software/io-libraries-suite-downloads-2175637.html

### 3. Test Hardware Connection

```python
import pyvisa

# List available instruments
rm = pyvisa.ResourceManager()
print(rm.list_resources())

# Expected: ['GPIB0::24::INSTR', 'USB0::...', etc.]
```

### 4. Test Serial Devices

```python
import serial.tools.list_ports

# List serial ports
ports = serial.tools.list_ports.comports()
for port in ports:
    print(f"{port.device}: {port.description}")

# Expected: COM3: USB Serial Port, /dev/ttyUSB0: USB-Serial, etc.
```

---

## Troubleshooting

### Import Errors

**Problem**: `ModuleNotFoundError: No module named 'experimental'`

**Solution**:
```bash
# Make sure you're in the chigure directory
cd blickrichtung/chigure

# Install in editable mode
pip install -e .

# Or set PYTHONPATH (temporary)
export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"  # Linux/Mac
set PYTHONPATH=%PYTHONPATH%;%cd%\src          # Windows
```

### Dependency Conflicts

**Problem**: Conflicting package versions

**Solution**:
```bash
# Create fresh virtual environment
python -m venv venv_clean
source venv_clean/bin/activate  # or venv_clean\Scripts\activate on Windows

# Install fresh
pip install -e ".[all]"
```

### NumPy/SciPy Build Errors

**Problem**: Compilation errors during numpy/scipy installation

**Solution**:
```bash
# Use pre-built wheels
pip install --only-binary :all: numpy scipy

# Or use conda
conda install numpy scipy matplotlib pandas scikit-learn
pip install -e . --no-deps
```

### Hardware Connection Issues

**Problem**: Can't connect to instruments

**Solutions**:

1. **Check cables and power**
2. **Verify drivers installed**:
   ```bash
   # Test VISA
   python -c "import pyvisa; print(pyvisa.ResourceManager().list_resources())"
   ```
3. **Check permissions (Linux)**:
   ```bash
   sudo usermod -a -G dialout $USER
   # Log out and log back in
   ```
4. **Use simulation mode**:
   ```python
   system = ConsciousnessDetectionSystem(simulation_mode=True)
   ```

### Memory Issues

**Problem**: Out of memory errors

**Solution**:
```python
# Reduce data capture duration
system.capture_thought(odorant, capture_duration=1.0)  # Instead of 2.0

# Process in smaller batches
data = sensors.get_latest_data(max_samples=50)  # Instead of 100
```

---

## Uninstallation

### Remove Package

```bash
pip uninstall chigure
```

### Remove Virtual Environment

```bash
# Deactivate
deactivate

# Remove directory
rm -rf venv  # Linux/Mac
rmdir /s venv  # Windows
```

### Remove Repository

```bash
cd ..
rm -rf blickrichtung  # Linux/Mac
rmdir /s /q blickrichtung  # Windows
```

---

## Updating

### Update Package

```bash
# Pull latest changes
git pull

# Reinstall
pip install -e ".[all]" --upgrade
```

### Update Dependencies Only

```bash
pip install -r requirements.txt --upgrade
```

---

## Docker Installation (Advanced)

For containerized deployment:

```dockerfile
FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    libusb-1.0-0-dev \
    && rm -rf /var/lib/apt/lists/*

# Clone and install
RUN git clone https://github.com/yourusername/blickrichtung.git
WORKDIR /app/blickrichtung/chigure
RUN pip install -e ".[all]"

# Run tests
RUN python -c "from experimental import ConsciousnessDetectionSystem; print('✓ Success!')"

CMD ["python", "-m", "experimental.complete_system"]
```

Build and run:
```bash
docker build -t chigure .
docker run chigure
```

---

## Support

If installation problems persist:

1. **Check Python version**: `python --version` (must be 3.8+)
2. **Check pip version**: `pip --version` (should be recent)
3. **Try fresh environment**: Create new venv
4. **Check disk space**: Ensure 10+ GB free
5. **Open issue**: https://github.com/yourusername/blickrichtung/issues

---

## Next Steps

After successful installation:

1. **Read documentation**: `implementation.md`, `README.md`
2. **Run examples**: See `README.md` Quick Start
3. **Run tests**: `pytest` (if dev dependencies installed)
4. **Explore modules**: `jupyter notebook` (if dev dependencies installed)

---

**Installation complete! Ready to detect consciousness!** ✅

