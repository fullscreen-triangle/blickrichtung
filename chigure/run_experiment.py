"""
Quick runner for Chigure experiments

Run this from the chigure root directory:
    python run_experiment.py
"""

import sys
from pathlib import Path

# Add src to path
src_path = Path(__file__).parent / 'src'
sys.path.insert(0, str(src_path))

# Now import and run
from experimental.complete_system import run_complete_experiment

if __name__ == "__main__":
    print("Starting complete consciousness detection experiment...")
    print("=" * 80)
    
    try:
        results = run_complete_experiment()
        print("\n" + "=" * 80)
        print("Experiment completed successfully!")
        print("=" * 80)
    except Exception as e:
        print(f"\nError running experiment: {e}")
        import traceback
        traceback.print_exc()

