# 📦 Required Packages for thought_validation.py

## TL;DR - Quick Install

```bash
cd chigure/src/standing
pip install -r requirements_thought_validation.txt
```

---

## Core Requirements (MUST HAVE)

```bash
pip install numpy>=1.21.0 pandas>=1.3.0 scipy>=1.7.0
```

| Package | Version | Used For |
|---------|---------|----------|
| **numpy** | >= 1.21.0 | Arrays, FFT, linear algebra |
| **pandas** | >= 1.3.0 | DataFrames, CSV export |
| **scipy** | >= 1.7.0 | Statistics, regression (`stats.linregress`) |

---

## Optional (Nice to Have)

```bash
pip install matplotlib>=3.4.0 scikit-learn>=1.0.0 tqdm>=4.62.0
```

| Package | Version | Used For |
|---------|---------|----------|
| matplotlib | >= 3.4.0 | Custom plotting |
| scikit-learn | >= 1.0.0 | Clustering in imported modules |
| tqdm | >= 4.62.0 | Progress bars |

---

## Python Version

```
Minimum: Python 3.8
Reason: Uses dataclasses (Python 3.7+) and modern type hints
```

Check your version:
```bash
python --version
```

---

## Local Modules (Already in codebase - no install needed)

These are imported from `chigure/src/standing/`:
- `mimo_signal_amplification.py`
- `precise_clock_apis.py`
- `satellite_temporal_gps.py`
- `signal_fusion.py`
- `signal_latencies.py`
- `temporal_information_architecture.py`
- `heartbeat_gas_bmd_unified_theory.py`
- `cardiac_harmonic_hierarchy_analysis.py`
- `reality_perception_reconstruction.py`
- `body_segmentation.py`
- `muscle_model.py`
- `s_entropy_validation.py`
- `bmd_equivalence.py`

**Make sure all these files are present in the `standing/` directory!**

---

## Verification

```bash
# Test imports
python -c "import numpy, pandas, scipy; print('✅ All required packages installed')"

# Test scipy.stats (used in code)
python -c "from scipy import stats; print('✅ scipy.stats available')"
```

---

## Installation Options

### Option 1: Requirements file (Recommended)
```bash
cd chigure/src/standing
pip install -r requirements_thought_validation.txt
```

### Option 2: Parent project
```bash
cd chigure
pip install -e .
```

### Option 3: Manual minimal
```bash
pip install numpy pandas scipy
```

---

## Common Issues

**"No module named 'numpy'"**
→ Run: `pip install numpy pandas scipy`

**"ImportError: cannot import name 'create_mimo_signal_amplification_system'"**
→ Make sure you're in `chigure/src/standing/` directory
→ Or set PYTHONPATH: `export PYTHONPATH="${PYTHONPATH}:$(pwd)"`

**"SyntaxError" with type hints**
→ Upgrade to Python 3.8+

---

## File Locations

```
chigure/
├── pyproject.toml                    # Parent project dependencies
└── src/
    └── standing/
        ├── thought_validation.py     # Main script
        ├── requirements_thought_validation.txt  # THIS FILE lists all packages
        ├── INSTALLATION.md           # Detailed installation guide
        ├── RUN_THOUGHT_VALIDATION.md # How to run the script
        ├── PACKAGES_REQUIRED.md      # This quick reference
        └── *.py                      # All local modules (no install needed)
```

---

## Ready to Run

After installation:
```bash
cd chigure/src/standing
python thought_validation.py
```

Results saved to: `results/thought_validation/`

---

**Questions?** See `INSTALLATION.md` for detailed troubleshooting.

