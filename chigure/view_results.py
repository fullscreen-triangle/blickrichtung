"""
View saved experimental results

Run this to see your saved thought library:
    python view_results.py
"""

import numpy as np
from pathlib import Path
import json

def find_latest_results():
    """Find the most recent results files."""
    data_dir = Path("data/experiments")
    
    if not data_dir.exists():
        print("No data directory found!")
        return None, None
    
    # Find thought libraries
    libraries = sorted(data_dir.glob("thought_library_*.npz"))
    
    # Find validation results
    validations = sorted(data_dir.glob("validation_*.json"))
    
    return libraries[-1] if libraries else None, validations[-1] if validations else None


def view_thought_library(filepath):
    """Display thought library contents."""
    print("\n" + "="*80)
    print(f"THOUGHT LIBRARY: {filepath.name}")
    print("="*80 + "\n")
    
    data = np.load(filepath)
    
    # Count thoughts
    thought_ids = set()
    for key in data.keys():
        if key.startswith('thought_'):
            thought_id = int(key.split('_')[1])
            thought_ids.add(thought_id)
    
    n_thoughts = len(thought_ids)
    print(f"✓ Total thoughts captured: {n_thoughts}\n")
    
    # Display each thought
    for i in sorted(thought_ids):
        print(f"Thought {i}:")
        
        if f'thought_{i}_o2_positions' in data:
            o2_pos = data[f'thought_{i}_o2_positions']
            print(f"  - O₂ molecules: {len(o2_pos)}")
            print(f"  - Spatial extent: {np.max(np.abs(o2_pos)):.3f} m")
        
        if f'thought_{i}_hole_center' in data:
            hole_center = data[f'thought_{i}_hole_center']
            print(f"  - Hole center: {hole_center}")
        
        if f'thought_{i}_electron_position' in data:
            electron_pos = data[f'thought_{i}_electron_position']
            print(f"  - Electron position: {electron_pos}")
        
        if f'thought_{i}_energy' in data:
            energy = data[f'thought_{i}_energy']
            print(f"  - Energy: {energy:.1f} eV")
        
        if f'thought_{i}_signature' in data:
            signature = data[f'thought_{i}_signature']
            print(f"  - Signature features: {len(signature)}")
        
        print()
    
    print(f"✓ All {n_thoughts} thoughts successfully saved!")
    print(f"✓ File: {filepath}")


def view_validation_results(filepath):
    """Display validation results."""
    print("\n" + "="*80)
    print(f"VALIDATION RESULTS: {filepath.name}")
    print("="*80 + "\n")
    
    with open(filepath, 'r') as f:
        results = json.load(f)
    
    print(f"Thoughts captured: {results.get('n_thoughts_captured', 'N/A')}")
    
    if 'similarity' in results:
        sim = results['similarity']
        print(f"\nSimilarity analysis:")
        print(f"  - Comparisons: {sim.get('n_comparisons', 'N/A')}")
        print(f"  - Mean similarity: {sim.get('mean_similarity', 0):.3f}")
        print(f"  - Std similarity: {sim.get('std_similarity', 0):.3f}")
    
    if 'navigation' in results:
        nav = results['navigation']
        print(f"\nNavigation:")
        print(f"  - Steps: {nav.get('n_steps', 'N/A')}")
        print(f"  - Mean adjacent similarity: {nav.get('mean_adjacent_similarity', 0):.3f}")
        print(f"  - Continuity validated: {nav.get('continuity_validated', False)}")
    
    if 'frequency' in results:
        freq = results['frequency']
        print(f"\nFrequency analysis:")
        print(f"  - Mean rate: {freq.get('mean_completion_rate_hz', 0):.2f} Hz")
        print(f"  - In expected range: {freq.get('in_expected_range', False)}")
    
    if 'overall_validated' in results:
        status = "✓ VALIDATED" if results['overall_validated'] else "✗ INCOMPLETE"
        print(f"\nOverall status: {status}")


def main():
    print("="*80)
    print("CHIGURE EXPERIMENTAL RESULTS VIEWER")
    print("="*80)
    
    library_file, validation_file = find_latest_results()
    
    if library_file:
        view_thought_library(library_file)
    else:
        print("\n✗ No thought library found!")
        print("  Run: python run_experiment.py")
    
    if validation_file:
        view_validation_results(validation_file)
    else:
        print("\n✗ No validation results found (this is expected after the JSON error)")
        print("  Your thought library is saved, just not the summary.")
    
    print("\n" + "="*80)
    print("SUMMARY")
    print("="*80)
    
    if library_file:
        print(f"\n✓ Your experimental data is safe!")
        print(f"\n  Thought library: {library_file}")
        if validation_file:
            print(f"  Validation results: {validation_file}")
        
        print(f"\n  To load in Python:")
        print(f"  >>> import numpy as np")
        print(f"  >>> data = np.load('{library_file}')")
        print(f"  >>> print(data.files)  # See all saved arrays")
    else:
        print("\n✗ No experimental data found yet.")
        print("  Run: python run_experiment.py")
    
    print()


if __name__ == "__main__":
    main()

