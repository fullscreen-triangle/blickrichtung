"""
Test script to verify Chigure installation

Run this to check if everything is working:
    python test_installation.py
"""

import sys

def test_imports():
    """Test that all modules can be imported."""
    print("Testing module imports...")
    
    tests = []
    
    # Test 1: Basic imports
    try:
        import numpy as np
        import scipy
        import matplotlib
        print("  ✓ Core scientific libraries (numpy, scipy, matplotlib)")
        tests.append(True)
    except ImportError as e:
        print(f"  ✗ Core libraries failed: {e}")
        tests.append(False)
    
    # Test 2: Experimental module
    try:
        from experimental import ConsciousnessDetectionSystem
        print("  ✓ Experimental module (ConsciousnessDetectionSystem)")
        tests.append(True)
    except ImportError as e:
        print(f"  ✗ Experimental module failed: {e}")
        print("     Try: pip install -e .")
        tests.append(False)
    
    # Test 3: Hardware module
    try:
        from experimental import IntegratedSystem
        print("  ✓ Hardware module (IntegratedSystem)")
        tests.append(True)
    except ImportError as e:
        print(f"  ✗ Hardware module failed: {e}")
        tests.append(False)
    
    # Test 4: Thought geometry
    try:
        from experimental import ThoughtGeometry
        print("  ✓ Thought geometry module")
        tests.append(True)
    except ImportError as e:
        print(f"  ✗ Thought geometry failed: {e}")
        tests.append(False)
    
    # Test 5: Oscillatory hole detector
    try:
        from experimental import OscillatoryHoleDetector
        print("  ✓ Oscillatory hole detector")
        tests.append(True)
    except ImportError as e:
        print(f"  ✗ Oscillatory hole detector failed: {e}")
        tests.append(False)
    
    return all(tests)


def test_basic_functionality():
    """Test basic functionality."""
    print("\nTesting basic functionality...")
    
    try:
        from experimental import ConsciousnessDetectionSystem
        import numpy as np
        
        # Initialize system
        system = ConsciousnessDetectionSystem(simulation_mode=True)
        print("  ✓ System initialization")
        
        # Check attributes
        assert system.simulation_mode == True
        assert system.hardware is not None
        print("  ✓ System attributes")
        
        return True
    except Exception as e:
        print(f"  ✗ Functionality test failed: {e}")
        return False


def test_quick_demo():
    """Run a quick mini demo."""
    print("\nRunning quick demo (5 seconds)...")
    
    try:
        from experimental.hardware_setup import IntegratedSystem
        import time
        
        # Initialize hardware
        system = IntegratedSystem(simulation_mode=True)
        print("  ✓ Hardware initialized")
        
        # Test gas chamber
        system.chamber.set_o2_concentration(0.005)
        print("  ✓ Gas chamber control")
        
        # Test electron positioning
        import numpy as np
        system.circuit.move_electron(np.array([0.01, 0.01, 0.1]))
        print("  ✓ Electron positioning")
        
        # Test sensor array
        system.sensors.start_acquisition()
        time.sleep(0.5)
        data = system.sensors.get_latest_data(max_samples=10)
        system.sensors.stop_acquisition()
        print(f"  ✓ Sensor acquisition ({len(data)} readings)")
        
        return True
    except Exception as e:
        print(f"  ✗ Demo failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all tests."""
    print("=" * 70)
    print("CHIGURE INSTALLATION TEST")
    print("=" * 70)
    print()
    
    results = []
    
    # Test imports
    results.append(test_imports())
    
    # Test functionality
    if results[0]:  # Only if imports worked
        results.append(test_basic_functionality())
        results.append(test_quick_demo())
    
    # Summary
    print("\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    
    if all(results):
        print("\n✅ ALL TESTS PASSED!")
        print("\nChigure is installed and working correctly.")
        print("\nNext steps:")
        print("  - Run complete experiment: python run_experiment.py")
        print("  - Or use command: chigure-experiment")
        print("  - Read QUICKSTART.md for more options")
        return 0
    else:
        print("\n❌ SOME TESTS FAILED")
        print("\nTroubleshooting:")
        print("  1. Make sure you're in the chigure directory")
        print("  2. Install the package: pip install -e .")
        print("  3. Check dependencies: pip install -r requirements.txt")
        print("  4. See INSTALL.md for detailed instructions")
        return 1


if __name__ == "__main__":
    sys.exit(main())

