# Installation Guide for Megaphrenia

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- git (for development installation)

## Quick Install (User)

### Option 1: Install from source

```bash
# Navigate to the megaphrenia directory
cd megaphrenia

# Install the package
pip install .
```

### Option 2: Install with optional dependencies

```bash
# Install with visualization support
pip install .[viz]

# Install with development tools
pip install .[dev]

# Install everything
pip install .[all]
```

## Development Install (Recommended for Contributors)

### 1. Clone or navigate to the repository

```bash
cd megaphrenia
```

### 2. Create a virtual environment (recommended)

**On Windows:**
```powershell
python -m venv venv
.\venv\Scripts\activate
```

**On Linux/macOS:**
```bash
python -m venv venv
source venv/bin/activate
```

### 3. Install in editable mode with dev dependencies

```bash
# Editable install (changes reflect immediately)
pip install -e .

# Install development dependencies
pip install -r requirements-dev.txt
```

## Verify Installation

Test that the package is installed correctly:

```python
# Test imports
python -c "from megaphrenia.core import Psychon; print('✅ Core module working')"
python -c "from megaphrenia.circuits import HalfAdder; print('✅ Circuits module working')"
python -c "from megaphrenia.integration import SEntropyNavigator; print('✅ Integration module working')"
```

Or run the module demos:

```bash
# Test moon landing (S-entropy navigation)
python -m megaphrenia.integration.moon_landing

# Test harmonic analysis
python -m megaphrenia.integration.harmonic_analysis

# Test harmonic network graph
python -m megaphrenia.integration.harmonic_network_graph

# Test circuit configuration
python -m megaphrenia.integration.circuit_configuration
```

## Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=megaphrenia --cov-report=html

# Run specific test file
pytest tests/test_integration.py
```

## Dependencies

### Core Dependencies (required)

- **numpy** (≥1.21.0): Numerical computing
- **scipy** (≥1.7.0): Scientific computing
- **pyyaml** (≥5.4.0): YAML parsing for circuit configuration

### Optional Dependencies

**Visualization** (`pip install megaphrenia[viz]`):
- **matplotlib** (≥3.5.0): Plotting
- **seaborn** (≥0.11.0): Statistical visualization

**Development** (`pip install megaphrenia[dev]`):
- **pytest** (≥7.0.0): Testing framework
- **pytest-cov** (≥3.0.0): Coverage reporting
- **black** (≥22.0.0): Code formatting
- **flake8** (≥4.0.0): Linting
- **mypy** (≥0.950): Type checking

## Using the Package

### As a Module

```python
from megaphrenia.core import Psychon, create_psychon_from_signature
from megaphrenia.circuits import HalfAdder, FullAdder
from megaphrenia.integration import (
    SEntropyNavigator,
    HarmonicAnalyzer,
    build_circuit_harmonic_graph,
    create_half_adder_config
)

# Create a psychon
psychon = create_psychon_from_signature(frequency=7.07e13, amplitude=1.0)

# Create a circuit
half_adder = HalfAdder()
sum_bit, carry_bit = half_adder.add(True, True)

# Use integration modules
navigator = SEntropyNavigator()
analyzer = HarmonicAnalyzer()
```

### Running Standalone Demos

Each module has a `__main__` block for demonstration:

```bash
# From megaphrenia directory
cd src/megaphrenia

# Run individual modules
python -m integration.moon_landing
python -m integration.harmonic_analysis
python -m integration.harmonic_network_graph
python -m integration.circuit_configuration
```

## Troubleshooting

### Import Errors

If you get import errors:

```python
# Check installation
pip list | grep megaphrenia

# Reinstall
pip install --force-reinstall .
```

### Module Not Found

If Python can't find the module:

```bash
# Check PYTHONPATH
python -c "import sys; print('\n'.join(sys.path))"

# Add src to PYTHONPATH (temporary)
export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"  # Linux/macOS
$env:PYTHONPATH += ";$(pwd)\src"              # Windows PowerShell
```

### NumPy/SciPy Installation Issues

On some systems, you may need to install numpy/scipy separately:

```bash
# Windows: Use precompiled wheels
pip install numpy scipy --only-binary :all:

# Linux: May need build tools
sudo apt-get install python3-dev  # Debian/Ubuntu
sudo yum install python3-devel     # RedHat/CentOS

# macOS: Install via Homebrew (optional)
brew install numpy scipy
```

## Updating

### Update from source

```bash
cd megaphrenia
git pull  # If using git
pip install --upgrade .
```

### Update in editable mode

If installed with `pip install -e .`, changes to source code are reflected immediately (no need to reinstall).

## Uninstalling

```bash
pip uninstall megaphrenia
```

## Directory Structure After Installation

```
megaphrenia/
├── src/
│   └── megaphrenia/
│       ├── __init__.py
│       ├── core/           # Core modules (Psychon, BMD, S-entropy)
│       ├── circuits/       # Circuit components
│       ├── hardware/       # Hardware oscillation harvesters
│       ├── validation/     # Validation framework
│       └── integration/    # Shooting + harmonic balance
├── tests/                  # Test files
├── docs/                   # Documentation
├── pyproject.toml          # Modern package config
├── setup.py               # Traditional setup
├── requirements.txt       # Core dependencies
└── requirements-dev.txt   # Dev dependencies
```

## Next Steps

After installation:

1. **Read the documentation**: `README.md`, `docs/INTEGRATION_COMPLETE.md`
2. **Run the demos**: Try each module's `__main__` demo
3. **Run tests**: `pytest` to verify everything works
4. **Start building circuits**: See `docs/implementation.md`

## Getting Help

- Check the documentation in `docs/`
- Read module docstrings: `help(megaphrenia.integration.SEntropyNavigator)`
- Run demos to see usage examples
- Check test files in `tests/` for usage patterns

---

**Installation complete! 🚀**

You're ready to build biological integrated circuits with shooting + harmonic balance validation!

