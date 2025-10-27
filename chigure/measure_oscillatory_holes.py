"""
MEASURE OSCILLATORY HOLES

This is the "meat" of the argument - the actual validation of:
  "Consciousness is generalized olfaction through oscillatory hole-filling"

Run this to execute the core validation experiments.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from validation.core_hypothesis_validation import CoreHypothesisValidator

if __name__ == "__main__":
    print("\n" + "="*80)
    print("MEASURING OSCILLATORY HOLES")
    print("Core Hypothesis Validation")
    print("="*80)
    
    print("\nThis will test the fundamental predictions:")
    print("  1. Similar oscillatory signatures → similar smells")
    print("  2. H/D isotope substitution → different smells (CRITICAL TEST)")
    print("  3. Oscillatory holes are physically detectable")
    print("\nPress Enter to begin...")
    input()
    
    # Run validation
    validator = CoreHypothesisValidator()
    results = validator.run_all_experiments()
    
    print("\n\n" + "="*80)
    print("VALIDATION COMPLETE!")
    print("="*80)
    print("\nResults saved to: results/core_validation/")
    print("\nKey files:")
    print("  - experiment_1_odorant_similarity.json")
    print("  - experiment_2_isotope_discrimination.json")
    print("  - experiment_3_hole_detection.json")
    print("  - validation_summary.json")

