"""
Run all core module demonstrations.

Executes complete demonstrations of:
1. Oxygen Categorical Clock
2. S-Entropy Coordinate System  
3. Biological Maxwell Demons
4. Oscillatory Signature Framework

All results saved to results/ directory in accessible formats (JSON + NPY).
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

def main():
    print("\n" + "="*80)
    print("CORE THEORETICAL FRAMEWORK DEMONSTRATIONS")
    print("="*80)
    print("\nThis will demonstrate all four core modules:")
    print("  1. Oxygen Categorical Clock (O₂ 25,110 states)")
    print("  2. S-Entropy Coordinate System")
    print("  3. Biological Maxwell Demons (BMDs)")
    print("  4. Oscillatory Signature Framework")
    print("\nAll results will be saved to results/ directory.")
    print("="*80 + "\n")
    
    input("Press Enter to continue...")
    
    # Module 1: Oxygen Categorical Clock
    print("\n" + "#"*80)
    print("# MODULE 1: OXYGEN CATEGORICAL CLOCK")
    print("#"*80 + "\n")
    
    from core.oxygen_categorical_clock import demonstrate_oxygen_clock
    demonstrate_oxygen_clock()
    
    input("\nPress Enter to continue to next module...")
    
    # Module 2: S-Entropy
    print("\n" + "#"*80)
    print("# MODULE 2: S-ENTROPY COORDINATE SYSTEM")
    print("#"*80 + "\n")
    
    from core.saint_entropy import demonstrate_sentropy
    demonstrate_sentropy()
    
    input("\nPress Enter to continue to next module...")
    
    # Module 3: Biological Maxwell Demons
    print("\n" + "#"*80)
    print("# MODULE 3: BIOLOGICAL MAXWELL DEMONS")
    print("#"*80 + "\n")
    
    from core.biological_maxwell_demon import demonstrate_bmd
    demonstrate_bmd()
    
    input("\nPress Enter to continue to next module...")
    
    # Module 4: Oscillatory Signatures
    print("\n" + "#"*80)
    print("# MODULE 4: OSCILLATORY SIGNATURE FRAMEWORK")
    print("#"*80 + "\n")
    
    from core.oscillatory_signature import demonstrate_signatures
    demonstrate_signatures()
    
    # Final summary
    print("\n" + "="*80)
    print("ALL DEMONSTRATIONS COMPLETE")
    print("="*80)
    print("\nResults saved to:")
    print("  - results/oxygen_clock/")
    print("  - results/sentropy/")
    print("  - results/bmds/")
    print("  - results/signatures/")
    print("\nFormats:")
    print("  - JSON: Human-readable, easily loaded")
    print("  - NPY: Binary NumPy arrays (efficient)")
    print("\nThese core modules provide the theoretical foundation for:")
    print("  ✓ Molecular perception (scent prediction)")
    print("  ✓ Drug effects (psychoactive similarity)")
    print("  ✓ Temporal perception (time estimation)")
    print("  ✓ Hardware consciousness (oscillatory hole detection)")
    print("  ✓ Thought geometry (3D thought navigation)")
    print("\n" + "="*80 + "\n")


if __name__ == "__main__":
    main()

