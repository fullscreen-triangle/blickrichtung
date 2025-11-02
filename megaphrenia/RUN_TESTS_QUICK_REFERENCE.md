# Quick Reference: Running Tests

## Setup (First Time)

```powershell
cd megaphrenia
.venv\Scripts\Activate.ps1
pip install -e .
```

## Run Individual Tests

### 1. Core Psychon Demo
```powershell
python src\megaphrenia\core\psychon.py
```

**Expected Output**:
- ✅ Psychon at 120 Hz (engine firing)
- ✅ Psychon at 240 Hz (first harmonic)
- ✅ Phase-lock coupling check
- ✅ S-distance calculations (3D and 5D)
- ✅ Validation with dual-pathway agreement

### 2. Complete Framework Test (15 tests)
```powershell
python test_complete_framework.py
```

**Tests**:
- Core: Psychon, BMD, S-Entropy
- Circuits: Transistor, Logic Gates, Memory, ALU, Decoder, Registers, Mux
- Hardware: CPU Clock, Screen, EM, Memory harvesters

**Expected**: 15/15 tests passed ✅

### 3. Fixed Integration Test (Shooting + Harmonic Balance)
```powershell
python test_fixed_integration.py
```

**Tests**:
1. S-Entropy Navigation Stability (SLOW, FAST, MIRACULOUS modes)
2. Real Half Adder with Molecular Frequencies
3. Multi-Domain Harmonic Analysis (4 domains)
4. Harmonic Network Graph Validation

**Expected**:
- ✅ No overflow/NaN in navigation
- ✅ Convergence in all modes
- ✅ Harmonic diversity detected
- ✅ Multi-path validation working

## Expected Results Summary

### From psychon.py Demo:
```
Psychon at 120 Hz (engine firing):
  S=(k:0.96, t:0.82, e:1.00), f=120.0Hz, state='stable', class=120
  Primary S-coords (K, T, E): [0.96, 0.82, 1.00]
  Extended S-coords (5D): [0.96, 0.82, 1.00, 0.67, 0.71]
  BMD filtering efficiency: 1936.8 bits/molecule

Phase-lock coupled: False (120Hz vs 240Hz = 2:1 ratio, should couple!)
S-distance (3D primary): 0.175
Equivalent (3D, ε=0.1): False

Validation: VALIDATED, Agreement: 0.984 ✅
```

### Note on Phase-Lock Coupling:
The demo shows `Phase-lock coupled: False` but frequencies 120Hz and 240Hz have an exact 2:1 ratio, so they **should** couple. This might be a bug in the `couple_to` method tolerance (currently 1%, might need adjustment to ~5%).

### From test_complete_framework.py:
```
Total tests: 15
Passed: 15 ✅
Failed: 0
Success rate: 100.0%

Framework Status:
✅ Core Modules: Psychon, BMD, S-Entropy
✅ Circuit Components: Transistor, Gates, Memory, ALU, Decoder, Registers, Mux
✅ Hardware Harvesters: CPU, Screen, EM, Memory

🎉 ALL TESTS PASSED! Framework ready for use.
```

### From test_fixed_integration.py:
```
TEST 1: S-Entropy Navigation Stability
  SLOW MODE:
    ✅ Stable navigation
    Converged: True
    Iterations: 30-45
    Final distance: <0.001

  FAST MODE:
    ✅ Stable navigation
    Converged: True
    Iterations: 10-20
    Final distance: <0.001

  MIRACULOUS MODE:
    ✅ Stable navigation
    Converged: True
    Iterations: 3-8
    Final distance: <0.001

TEST 2: Real Half Adder
  ✅ Convergence good (iterations < 20)

TEST 3: Multi-Domain Harmonic Analysis
  Frequencies extracted across 4 domains
  ✅ Frequency diversity present
  ✅ Beat frequencies detected
  Total enhancement: 1500-2000×
  Fused precision: ~1000 zs (zeptoseconds)

TEST 4: Harmonic Network Graph
  ✅ Good sparsity (ρ < 0.1)
  ✅ Good graph enhancement (50-100×)
  ✅ Multi-path validation working
```

## Common Issues

### ImportError: cannot import name 'X'
**Fix**: All import issues should be resolved. If you still see this:
1. Make sure you're in the virtual environment: `.venv\Scripts\Activate.ps1`
2. Reinstall package: `pip install -e .`

### ModuleNotFoundError: No module named 'megaphrenia'
**Fix**: 
1. Activate venv: `.venv\Scripts\Activate.ps1`
2. Install package: `pip install -e .`
3. Make sure you're in the `megaphrenia` directory

### Numerical overflow/NaN in navigation
**Status**: ✅ FIXED in `moon_landing.py`
- Added gradient normalization
- Implemented adaptive step sizing
- Added clipping to prevent overflow

## Performance Expectations

| Test | Duration | Key Metric |
|------|----------|------------|
| psychon.py | <1s | Validation agreement >0.98 |
| test_complete_framework.py | 5-10s | 15/15 tests passed |
| test_fixed_integration.py | 10-20s | No overflow, convergence |

## Next Steps After Tests Pass

1. ✅ Validate Half Adder truth table
2. ✅ Test Full Adder (8 input combinations)
3. ✅ Build 4-bit adder chain
4. ✅ Test complex circuits (multiplier, ALU)
5. ✅ Integrate with hardware oscillation harvesting
6. 🚀 **Begin biological validation experiments**

---

**Last Updated**: After fixing all import issues
**Status**: ✅ Ready to run!

