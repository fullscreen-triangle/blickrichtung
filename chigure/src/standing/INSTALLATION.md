# Installation Guide for Thought Validation Pipeline

## Quick Reference

### Required Packages

| Package | Minimum Version | Purpose |
|---------|----------------|---------|
| **numpy** | >= 1.21.0 | Numerical arrays and computations |
| **pandas** | >= 1.3.0 | Data structures and CSV export |
| **scipy** | >= 1.7.0 | Statistical analysis and regression |
| **matplotlib** | >= 3.4.0 | Optional: Plotting (for custom visualizations) |
| **scikit-learn** | >= 1.0.0 | Optional: Clustering in imported modules |
| **tqdm** | >= 4.62.0 | Optional: Progress bars |

### Python Version
- **Minimum**: Python 3.8
- **Recommended**: Python 3.9 or 3.10
- **Reason**: Requires `dataclasses` (Python 3.7+) and modern type hints

---

## Installation Methods

### Method 1: Using requirements.txt (Fastest)

```bash
cd chigure/src/standing
pip install -r requirements_thought_validation.txt
```

**Installs:**
- All required packages (numpy, pandas, scipy)
- All optional packages (matplotlib, scikit-learn, tqdm)

---

### Method 2: Parent Project Installation (Recommended)

```bash
cd chigure
pip install -e .
```

**Benefits:**
- Installs chigure as editable package
- Makes all modules importable from anywhere
- Includes all dependencies from `pyproject.toml`

**To include optional dependencies:**
```bash
pip install -e ".[all]"  # Includes dev, hardware, visualization extras
```

---

### Method 3: Manual Installation

**Minimal (only required packages):**
```bash
pip install numpy>=1.21.0 pandas>=1.3.0 scipy>=1.7.0
```

**Full (all packages):**
```bash
pip install numpy>=1.21.0 pandas>=1.3.0 scipy>=1.7.0 matplotlib>=3.4.0 scikit-learn>=1.0.0 tqdm>=4.62.0
```

---

### Method 4: Conda/Mamba (Alternative)

```bash
conda create -n thought_validation python=3.10
conda activate thought_validation
conda install numpy pandas scipy matplotlib scikit-learn tqdm
```

Or with mamba (faster):
```bash
mamba create -n thought_validation python=3.10 numpy pandas scipy matplotlib scikit-learn tqdm
mamba activate thought_validation
```

---

## Verification

### Check Python Version
```bash
python --version
# Should show: Python 3.8.x or higher
```

### Verify Package Installation
```bash
python -c "import numpy, pandas, scipy; print('✅ Core packages OK')"
python -c "import matplotlib, sklearn, tqdm; print('✅ Optional packages OK')"
```

### Check Package Versions
```python
python << EOF
import numpy as np
import pandas as pd
import scipy

print(f"numpy:  {np.__version__}")
print(f"pandas: {pd.__version__}")
print(f"scipy:  {scipy.__version__}")
EOF
```

---

## Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'numpy'"

**Solution:**
```bash
pip install numpy pandas scipy
```

### Issue: "ImportError: cannot import name 'create_mimo_signal_amplification_system'"

**Cause:** Local modules not in path

**Solution:**
```bash
# Make sure you're in the correct directory
cd chigure/src/standing

# Or set PYTHONPATH (Linux/Mac)
export PYTHONPATH="${PYTHONPATH}:$(pwd)"

# Or set PYTHONPATH (Windows)
set PYTHONPATH=%PYTHONPATH%;%CD%
```

### Issue: "SyntaxError" related to type hints

**Cause:** Python version too old

**Solution:** Upgrade to Python 3.8+
```bash
# Check version
python --version

# If < 3.8, install newer Python
# Linux: use apt/yum
# Mac: use homebrew
# Windows: download from python.org
```

### Issue: pip install fails with "Permission denied"

**Solution:** Use `--user` flag
```bash
pip install --user -r requirements_thought_validation.txt
```

Or use a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows

pip install -r requirements_thought_validation.txt
```

---

## Virtual Environment Setup (Best Practice)

### Create Virtual Environment
```bash
# Navigate to project root
cd chigure

# Create venv
python -m venv venv

# Activate (Linux/Mac)
source venv/bin/activate

# Activate (Windows)
venv\Scripts\activate
```

### Install Packages
```bash
# Install parent project (recommended)
pip install -e .

# Or install just requirements
cd src/standing
pip install -r requirements_thought_validation.txt
```

### Deactivate When Done
```bash
deactivate
```

---

## Dependencies Explained

### Why Each Package?

**numpy** (Required)
- Multi-dimensional arrays for oscillatory data
- Fast vectorized computations
- Fourier transforms (FFT) for frequency analysis
- Linear algebra operations

**pandas** (Required)
- DataFrame structures for tabular results
- CSV export for summary statistics
- Time series data handling
- Easy aggregation and grouping

**scipy** (Required)
- Statistical functions (`scipy.stats`)
  - Linear regression (`stats.linregress`)
  - Statistical tests (t-tests, correlations)
- Signal processing (`scipy.signal`)
- Optimization algorithms

**matplotlib** (Optional)
- Only needed if creating custom plots
- Not used by `thought_validation.py` directly
- Required by some imported modules

**scikit-learn** (Optional)
- Clustering algorithms (hierarchical, k-means)
- Used in harmonic network analysis
- Not critical for basic validation

**tqdm** (Optional)
- Progress bars for long operations
- Improves user experience
- Not required for core functionality

---

## What About Local Modules?

The following imports are **local modules** from `chigure/src/standing/`:
- `mimo_signal_amplification`
- `precise_clock_apis`
- `satellite_temporal_gps`
- `signal_fusion`
- `signal_latencies`
- `temporal_information_architecture`
- `heartbeat_gas_bmd_unified_theory`
- `cardiac_harmonic_hierarchy_analysis`
- `reality_perception_reconstruction`
- `body_segmentation`
- `muscle_model`
- `s_entropy_validation`
- `bmd_equivalence`

**These do NOT need separate installation** — they're part of the codebase.

**Important:** Make sure all `.py` files in `chigure/src/standing/` are present!

---

## Platform-Specific Notes

### Linux
- Use system package manager for Python if needed: `sudo apt install python3.10`
- pip usually works out of the box

### macOS
- Use Homebrew: `brew install python@3.10`
- May need to use `python3` and `pip3` commands

### Windows
- Download from python.org
- Make sure to check "Add Python to PATH" during installation
- Use `py` launcher: `py -m pip install ...`

---

## Docker (Optional - Advanced)

Create a `Dockerfile`:
```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements_thought_validation.txt .
RUN pip install -r requirements_thought_validation.txt

COPY . .

CMD ["python", "thought_validation.py"]
```

Build and run:
```bash
docker build -t thought-validation .
docker run -v $(pwd)/results:/app/results thought-validation
```

---

## Summary: Recommended Installation

**For most users:**
```bash
# 1. Navigate to project
cd chigure

# 2. Create virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# 3. Install project
pip install -e .

# 4. Navigate to standing directory
cd src/standing

# 5. Run validation
python thought_validation.py

# 6. Check results
ls results/thought_validation/
```

**Minimal installation (if above fails):**
```bash
cd chigure/src/standing
pip install numpy pandas scipy
python thought_validation.py
```

---

## Still Having Issues?

**Check these common problems:**

1. ✅ Python version >= 3.8
2. ✅ pip is up to date: `pip install --upgrade pip`
3. ✅ You're in the correct directory: `chigure/src/standing`
4. ✅ All local `.py` modules are present in `standing/`
5. ✅ No conflicting Python installations

**If all else fails:**
- Create a fresh virtual environment
- Install only core packages (numpy, pandas, scipy)
- Run with verbose output: `python -v thought_validation.py`

