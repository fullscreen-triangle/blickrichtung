#!/usr/bin/env python3
"""
Test script to verify all validator imports and basic functionality.

Run this first to ensure everything is set up correctly before
running the full experimental framework.
"""

import sys
from pathlib import Path

# Add current directory to path
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

print("="*80)
print("TESTING OSCILLATORY VALIDATOR IMPORTS")
print("="*80)

validators_status = {}

# Test 1: Comprehensive Consciousness Validator
print("\n1. Testing ComprehensiveConsciousnessValidator...")
try:
    from comprehensive_consciousness_validator import ComprehensiveConsciousnessValidator
    validator = ComprehensiveConsciousnessValidator(results_dir="test_results/comprehensive")
    print("   ✓ Import successful")
    print(f"   ✓ Initialized: {validator is not None}")
    validators_status['comprehensive_consciousness'] = True
except Exception as e:
    print(f"   ❌ Error: {e}")
    validators_status['comprehensive_consciousness'] = False

# Test 2: Multi-Scale Validator
print("\n2. Testing MultiScaleOscillatoryConsciousnessValidator...")
try:
    from multiscale_oscillatory_consciousness_validator import MultiScaleOscillatoryConsciousnessValidator
    validator = MultiScaleOscillatoryConsciousnessValidator(results_dir="test_results/multiscale")
    print("   ✓ Import successful")
    print(f"   ✓ Initialized with {len(validator.hierarchy)} scales")
    validators_status['multiscale_oscillatory'] = True
except Exception as e:
    print(f"   ❌ Error: {e}")
    validators_status['multiscale_oscillatory'] = False

# Test 3: Activity-Sleep Mirror Validator
print("\n3. Testing ActivitySleepOscillatoryMirrorValidator...")
try:
    from sleep_activity_oscillatory_mirror_validator import ActivitySleepOscillatoryMirrorValidator
    validator = ActivitySleepOscillatoryMirrorValidator(results_dir="test_results/mirror")
    print("   ✓ Import successful")
    print("   ✓ Initialized")
    validators_status['activity_sleep_mirror'] = True
except Exception as e:
    print(f"   ❌ Error: {e}")
    validators_status['activity_sleep_mirror'] = False

# Test 4: BMD Frame Selection Validator
print("\n4. Testing BMDFrameSelectionValidator...")
try:
    from bmd_frame_selection_validator import BMDFrameSelectionValidator
    validator = BMDFrameSelectionValidator(results_dir="test_results/bmd")
    print("   ✓ Import successful")
    print(f"   ✓ Initialized with memory size {validator.memory_size}")
    validators_status['bmd_frame_selection'] = True
except Exception as e:
    print(f"   ❌ Error: {e}")
    validators_status['bmd_frame_selection'] = False

# Test 5: Fire-Consciousness Validator
print("\n5. Testing FireConsciousnessCouplingValidator...")
try:
    from fire_consciousness_coupling_validator import FireConsciousnessCouplingValidator
    validator = FireConsciousnessCouplingValidator(results_dir="test_results/fire")
    print("   ✓ Import successful")
    print("   ✓ Initialized")
    validators_status['fire_consciousness'] = True
except Exception as e:
    print(f"   ❌ Error: {e}")
    validators_status['fire_consciousness'] = False

# Test 6: Quantum Ion Validator
print("\n6. Testing QuantumIonConsciousnessValidator...")
try:
    from quantum_ion_consciousness_validator import QuantumIonConsciousnessValidator
    validator = QuantumIonConsciousnessValidator(results_dir="test_results/quantum")
    print("   ✓ Import successful")
    print(f"   ✓ Initialized with {len(validator.ions)} ion types")
    validators_status['quantum_ion'] = True
except Exception as e:
    print(f"   ❌ Error: {e}")
    validators_status['quantum_ion'] = False

# Test 7: Package Import
print("\n7. Testing package-level import...")
try:
    import geometry
    print("   ✓ Package import successful")
    print(f"   ✓ Package version: {geometry.__version__}")
    print(f"   ✓ Available validators: {len(geometry.__all__)}")
    validators_status['package_import'] = True
except Exception as e:
    print(f"   ❌ Error: {e}")
    validators_status['package_import'] = False

# Test 8: Dependencies
print("\n8. Testing dependencies...")
try:
    import numpy as np
    print(f"   ✓ numpy {np.__version__}")
except ImportError:
    print("   ❌ numpy not found - run: pip install numpy")
    validators_status['dependencies'] = False

try:
    import scipy
    print(f"   ✓ scipy {scipy.__version__}")
except ImportError:
    print("   ⚠ scipy not found (optional) - run: pip install scipy")

try:
    import matplotlib
    print(f"   ✓ matplotlib {matplotlib.__version__}")
except ImportError:
    print("   ❌ matplotlib not found - run: pip install matplotlib")
    validators_status['dependencies'] = False

try:
    import seaborn
    print(f"   ✓ seaborn {seaborn.__version__}")
except ImportError:
    print("   ⚠ seaborn not found (optional) - run: pip install seaborn")

if 'dependencies' not in validators_status:
    validators_status['dependencies'] = True

# Summary
print("\n" + "="*80)
print("TEST SUMMARY")
print("="*80)

successful = sum(1 for v in validators_status.values() if v)
total = len(validators_status)

for name, status in validators_status.items():
    symbol = "✓" if status else "❌"
    print(f"{symbol} {name}")

print(f"\n{successful}/{total} tests passed")

if successful == total:
    print("\n🎊 All tests passed! Ready to run experiments! 🎊")
    print("\nNext steps:")
    print("1. Run: python run_comprehensive_experiments.py")
    print("2. Or check README_EXPERIMENTAL_FRAMEWORK.md for options")
else:
    print("\n⚠ Some tests failed. Please fix errors before running experiments.")
    print("\nCommon fixes:")
    print("- Install missing dependencies: pip install numpy scipy matplotlib seaborn")
    print("- Check that all validator files are present in this directory")
    print("- Ensure you're running from chigure/src/geometry/ directory")

# Clean up test results
print("\n" + "="*80)
try:
    import shutil
    test_dir = Path("test_results")
    if test_dir.exists():
        shutil.rmtree(test_dir)
        print("✓ Cleaned up test results directory")
except:
    pass

print("="*80)

