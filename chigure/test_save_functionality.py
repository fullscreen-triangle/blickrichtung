"""
Test script to verify all save functionality works correctly.

This script runs a quick test of each module's save functionality
and reports success/failure.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

def test_hardware_signatures():
    """Test hardware signature saving."""
    print("\n" + "="*80)
    print("Testing Hardware Signatures")
    print("="*80)
    
    try:
        from signatures.hardware_signature import demonstrate_hardware_signatures
        demonstrate_hardware_signatures()
        
        # Verify files exist
        expected_files = [
            'results/hardware_signatures/hardware_signatures.json',
            'results/hardware_signatures/combined_signature.json',
            'results/hardware_signatures/molecular_scale_signature.json'
        ]
        
        for f in expected_files:
            if not Path(f).exists():
                print(f"✗ Missing: {f}")
                return False
        
        print("✓ All hardware signature files created")
        return True
    except Exception as e:
        print(f"✗ Hardware signatures failed: {e}")
        return False

def test_molecular_signatures():
    """Test molecular signature saving."""
    print("\n" + "="*80)
    print("Testing Molecular Signatures")
    print("="*80)
    
    try:
        from signatures.molecular_signature import demonstrate_molecular_signatures
        demonstrate_molecular_signatures()
        
        # Verify files exist
        expected_files = [
            'results/molecular_signatures/molecular_signatures.json',
            'results/molecular_signatures/similarity_matrix.json'
        ]
        
        for f in expected_files:
            if not Path(f).exists():
                print(f"✗ Missing: {f}")
                return False
        
        print("✓ All molecular signature files created")
        return True
    except Exception as e:
        print(f"✗ Molecular signatures failed: {e}")
        return False

def test_bond_analysis():
    """Test bond analysis saving."""
    print("\n" + "="*80)
    print("Testing Bond Analysis")
    print("="*80)
    
    try:
        from molecular.bond_analyzer import demonstrate_bond_analysis
        demonstrate_bond_analysis()
        
        # Verify files exist
        expected_files = [
            'results/bond_analysis/vanillin_bonds.json'
        ]
        
        for f in expected_files:
            if not Path(f).exists():
                print(f"✗ Missing: {f}")
                return False
        
        print("✓ All bond analysis files created")
        return True
    except Exception as e:
        print(f"✗ Bond analysis failed: {e}")
        return False

def test_mass_properties():
    """Test mass properties saving."""
    print("\n" + "="*80)
    print("Testing Mass Properties")
    print("="*80)
    
    try:
        from molecular.mass_properties import demonstrate_mass_properties
        demonstrate_mass_properties()
        
        # Verify files exist
        expected_files = [
            'results/mass_properties/benzene_h_mass.json',
            'results/mass_properties/benzene_d_mass.json',
            'results/mass_properties/isotope_comparison.json'
        ]
        
        for f in expected_files:
            if not Path(f).exists():
                print(f"✗ Missing: {f}")
                return False
        
        print("✓ All mass property files created")
        return True
    except Exception as e:
        print(f"✗ Mass properties failed: {e}")
        return False

def test_structure_encoding():
    """Test structure encoding saving."""
    print("\n" + "="*80)
    print("Testing Structure Encoding")
    print("="*80)
    
    try:
        from molecular.structure_encoder import demonstrate_encoding
        demonstrate_encoding()
        
        # Verify files exist
        expected_files = [
            'results/structure_encoding/molecular_features.json'
        ]
        
        for f in expected_files:
            if not Path(f).exists():
                print(f"✗ Missing: {f}")
                return False
        
        print("✓ All structure encoding files created")
        return True
    except Exception as e:
        print(f"✗ Structure encoding failed: {e}")
        return False

def test_geometry_calculation():
    """Test geometry calculation saving."""
    print("\n" + "="*80)
    print("Testing Geometry Calculation")
    print("="*80)
    
    try:
        from molecular.geometry_calculator import demonstrate_geometry_calculation
        demonstrate_geometry_calculation()
        
        # Verify files exist
        expected_files = [
            'results/geometry/molecular_geometries.json'
        ]
        
        for f in expected_files:
            if not Path(f).exists():
                print(f"✗ Missing: {f}")
                return False
        
        print("✓ All geometry files created")
        return True
    except Exception as e:
        print(f"✗ Geometry calculation failed: {e}")
        return False

def main():
    """Run all tests."""
    print("\n" + "="*80)
    print("TESTING ALL SAVE FUNCTIONALITY")
    print("="*80)
    
    results = {
        'Hardware Signatures': test_hardware_signatures(),
        'Molecular Signatures': test_molecular_signatures(),
        'Bond Analysis': test_bond_analysis(),
        'Mass Properties': test_mass_properties(),
        'Structure Encoding': test_structure_encoding(),
        'Geometry Calculation': test_geometry_calculation()
    }
    
    # Summary
    print("\n" + "="*80)
    print("TEST SUMMARY")
    print("="*80)
    
    passed = sum(results.values())
    total = len(results)
    
    for test_name, passed_test in results.items():
        status = "✓ PASS" if passed_test else "✗ FAIL"
        print(f"{status}: {test_name}")
    
    print("\n" + "="*80)
    print(f"Results: {passed}/{total} tests passed")
    print("="*80)
    
    if passed == total:
        print("\n✓ All save functionality working correctly!")
        print("\nResults saved to:")
        print("  - results/hardware_signatures/")
        print("  - results/molecular_signatures/")
        print("  - results/bond_analysis/")
        print("  - results/mass_properties/")
        print("  - results/structure_encoding/")
        print("  - results/geometry/")
        return 0
    else:
        print("\n✗ Some tests failed. Check output above for details.")
        return 1

if __name__ == "__main__":
    sys.exit(main())

