# Installation Guide

Comprehensive installation instructions for the Blickrichtung Consciousness Programming Framework.

---

## Table of Contents

1. [System Requirements](#system-requirements)
2. [Quick Installation](#quick-installation)
3. [Detailed Installation](#detailed-installation)
4. [Verification](#verification)
5. [Troubleshooting](#troubleshooting)
6. [Development Installation](#development-installation)
7. [Platform-Specific Notes](#platform-specific-notes)

---

## System Requirements

### Minimum Requirements
- **OS**: Windows 10+, macOS 10.15+, or Linux (Ubuntu 18.04+)
- **Python**: 3.8 or higher
- **RAM**: 4 GB
- **Storage**: 500 MB free space
- **CPU**: Any modern processor (2+ cores recommended)

### Recommended Requirements
- **OS**: Windows 11, macOS 12+, or Ubuntu 22.04 LTS
- **Python**: 3.10 or higher
- **RAM**: 8 GB or more
- **Storage**: 2 GB free space (for results and documentation)
- **CPU**: 4+ cores for faster simulations

### Optional (for documentation compilation)
- **LaTeX**: TeX Live 2020+ (Linux/Mac) or MiKTeX (Windows)
- **PDF viewer**: For viewing compiled manuscripts

---

## Quick Installation

### For Users (Package Installation)

```bash
# Install from source
git clone https://github.com/yourusername/blickrichtung.git
cd blickrichtung/chigure
pip install .

# Or install in development mode
pip install -e .

# Verify installation
blickrichtung-validate --help
```

### For Researchers (Full Repository)

```bash
# Clone repository
git clone https://github.com/yourusername/blickrichtung.git
cd blickrichtung

# Set up computational suite
cd chigure
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r src/computing/requirements.txt

# Run validation
cd src/computing
python run_all_validations.py
```

---

## Detailed Installation

### Step 1: Install Python

#### Windows
1. Download Python from [python.org](https://www.python.org/downloads/)
2. Run installer, **check "Add Python to PATH"**
3. Verify installation:
   ```cmd
   python --version
   ```

#### macOS
```bash
# Using Homebrew (recommended)
brew install python@3.10

# Or download from python.org
```

#### Linux (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install python3.10 python3.10-venv python3-pip
```

### Step 2: Install Git

#### Windows
- Download from [git-scm.com](https://git-scm.com/)
- Use default installation options

#### macOS
```bash
brew install git
```

#### Linux
```bash
sudo apt install git
```

### Step 3: Clone Repository

```bash
# HTTPS (recommended for most users)
git clone https://github.com/yourusername/blickrichtung.git

# Or SSH (if you have SSH keys configured)
git clone git@github.com:yourusername/blickrichtung.git

# Navigate to repository
cd blickrichtung
```

### Step 4: Set Up Virtual Environment

**Why use a virtual environment?**
- Isolates project dependencies
- Prevents conflicts with other Python projects
- Ensures reproducibility

```bash
# Navigate to computational suite
cd chigure

# Create virtual environment
python -m venv .venv

# Activate virtual environment
# On Windows (PowerShell):
.venv\Scripts\Activate.ps1

# On Windows (CMD):
.venv\Scripts\activate.bat

# On macOS/Linux:
source .venv/bin/activate

# Your prompt should now show (.venv)
```

### Step 5: Install Dependencies

```bash
# Ensure you're in chigure directory with activated venv
cd src/computing
pip install --upgrade pip
pip install -r requirements.txt
```

**Expected output:**
```
Successfully installed numpy-1.24.3 scipy-1.11.1 matplotlib-3.7.1 networkx-3.1
```

### Step 6: Verify Installation

```bash
# Run core validation suite
python run_all_validations.py
```

**Expected output:**
```
=== Blickrichtung Computational Validation Suite ===

[1/5] Electromagnetic Resonance Analysis...
  ✓ Lithium: Q = 47.3, Programming strength = 0.73
  ✓ Dopamine: Q = 31.2, Programming strength = 0.58
  ✓ Serotonin: Q = 28.5, Programming strength = 0.54

[2/5] Kuramoto Oscillator Network...
  ✓ Lithium: Order parameter = 0.847
  ...

All validations completed successfully!
Results saved to: results/
```

---

## Verification

### Test Core Functionality

```bash
# Test individual modules
cd chigure/src/computing

# Test electromagnetic resonance
python electromagnetic_resonance_calculator.py

# Test metabolic hierarchy
python metabolic_flux_hierarchy.py

# Test hierarchy mapper
python metabolic_hierarchy_mapper.py
```

### Run Extended Validation Suite

```bash
# Run all 10 modules
python run_extended_validations.py --all

# Run specific module
python run_extended_validations.py --module drug_properties

# List available modules
python run_extended_validations.py --list
```

### Check Package Installation (if installed via pip)

```bash
# Check installed version
pip show blickrichtung-computing

# Test console scripts
blickrichtung-validate --help
blickrichtung-flux --help
blickrichtung-mapper --help
```

---

## Troubleshooting

### Common Issues

#### 1. `python` command not found

**Solution**: Use `python3` instead:
```bash
python3 -m venv .venv
python3 -m pip install -r requirements.txt
```

#### 2. Permission errors during installation

**Solution**: Install in user directory:
```bash
pip install --user -r requirements.txt
```

#### 3. Virtual environment activation fails (Windows)

**Error**: "cannot be loaded because running scripts is disabled"

**Solution**: Change PowerShell execution policy:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

#### 4. NumPy/SciPy installation fails

**Solution**: Install from conda instead:
```bash
conda create -n blickrichtung python=3.10
conda activate blickrichtung
conda install numpy scipy matplotlib networkx
```

#### 5. ImportError: No module named 'computing'

**Cause**: Wrong directory or environment not activated

**Solution**:
```bash
# Ensure you're in the right directory
cd chigure/src

# Check if venv is activated (should see (.venv) in prompt)
# If not, activate it:
source ../.venv/bin/activate  # macOS/Linux
..\.venv\Scripts\activate     # Windows
```

#### 6. Matplotlib backend errors

**Error**: "Matplotlib is currently using agg, which is a non-GUI backend"

**Solution**: Install tkinter:
```bash
# Ubuntu/Debian
sudo apt-get install python3-tk

# macOS
brew install python-tk

# Or use non-interactive backend in scripts
import matplotlib
matplotlib.use('Agg')
```

### Getting Help

If problems persist:

1. **Check Python version**:
   ```bash
   python --version  # Should be 3.8 or higher
   ```

2. **Check pip version**:
   ```bash
   pip --version
   ```

3. **Reinstall in clean environment**:
   ```bash
   rm -rf .venv  # Delete old environment
   python -m venv .venv
   source .venv/bin/activate
   pip install --upgrade pip setuptools wheel
   pip install -r src/computing/requirements.txt
   ```

4. **Search existing issues**:
   https://github.com/yourusername/blickrichtung/issues

5. **Create new issue**:
   Include Python version, OS, and full error message

---

## Development Installation

For contributors and developers:

```bash
# Clone repository
git clone https://github.com/yourusername/blickrichtung.git
cd blickrichtung/chigure

# Create development environment
python -m venv .venv
source .venv/bin/activate

# Install in editable mode with dev dependencies
pip install -e ".[dev]"

# Install pre-commit hooks (optional)
pip install pre-commit
pre-commit install

# Run tests
pytest tests/

# Format code
black src/computing/

# Check linting
flake8 src/computing/
```

### Development Dependencies

The `[dev]` extra includes:
- `pytest` - Testing framework
- `pytest-cov` - Coverage reporting
- `black` - Code formatting
- `flake8` - Linting
- `mypy` - Type checking
- `sphinx` - Documentation generation

---

## Platform-Specific Notes

### Windows

**PowerShell vs CMD**:
- Use PowerShell for better experience
- If activation fails, see troubleshooting above

**Long path support**:
```powershell
# Enable long paths (Administrator)
New-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Control\FileSystem" `
-Name "LongPathsEnabled" -Value 1 -PropertyType DWORD -Force
```

**Windows Subsystem for Linux (WSL)**:
- Recommended for advanced users
- Follow Linux installation instructions inside WSL

### macOS

**Apple Silicon (M1/M2)**:
- Use native Python 3.10+ for best performance
- Some NumPy operations automatically use Apple Silicon acceleration

**Permissions**:
```bash
# If you get permission errors
sudo chown -R $USER /usr/local
```

### Linux

**Ubuntu/Debian**:
```bash
sudo apt install python3-dev python3-venv python3-tk
```

**Fedora/RHEL**:
```bash
sudo dnf install python3-devel python3-tkinter
```

**Arch Linux**:
```bash
sudo pacman -S python python-pip tk
```

---

## LaTeX Installation (Optional)

For compiling manuscripts:

### Windows
- Download MiKTeX: https://miktex.org/download
- Use MiKTeX Console to install missing packages automatically

### macOS
```bash
brew install --cask mactex
# Or BasicTeX for smaller installation:
brew install --cask basictex
```

### Linux
```bash
# Ubuntu/Debian
sudo apt install texlive-full

# Or minimal installation
sudo apt install texlive-latex-base texlive-latex-extra
```

### Compile Papers
```bash
cd docs/computing/oxygen-hydrogen-coupling/
pdflatex metabolic-hierarchy-computing.tex
bibtex metabolic-hierarchy-computing
pdflatex metabolic-hierarchy-computing.tex
pdflatex metabolic-hierarchy-computing.tex
```

---

## Post-Installation

### Configure Results Directory

```bash
# Create results directory for outputs
cd blickrichtung/chigure/src/computing
mkdir -p results
```

### Test Data Generation

```bash
# Generate test datasets
python metabolic_flux_hierarchy.py
python drug_properties.py
python therapeutic_window_calculator.py

# Check results
ls -lh results/
```

### Documentation Access

```bash
# View documentation
cd docs/computing
# Open README.md in your preferred markdown viewer
```

---

## Uninstallation

### Package Installation
```bash
pip uninstall blickrichtung-computing
```

### Full Repository
```bash
# Deactivate virtual environment
deactivate

# Remove repository
cd ..
rm -rf blickrichtung
```

---

## Next Steps

After installation:

1. **Read documentation**: [chigure/src/computing/README.md](chigure/src/computing/README.md)
2. **Run quick start**: [QUICK_START_GUIDE.md](chigure/src/computing/QUICK_START_GUIDE.md)
3. **Explore papers**: [docs/computing/](docs/computing/)
4. **Try examples**: Run validation modules individually
5. **Join discussions**: [GitHub Discussions](https://github.com/yourusername/blickrichtung/discussions)

---

## Support

- **Issues**: https://github.com/yourusername/blickrichtung/issues
- **Discussions**: https://github.com/yourusername/blickrichtung/discussions
- **Email**: your.email@example.com

---

*Last Updated: December 2025*

