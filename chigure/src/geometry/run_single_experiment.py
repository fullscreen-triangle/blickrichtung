#!/usr/bin/env python3
"""
Single Experiment Runner - Memory-Efficient Version

Run one validator experiment at a time to avoid memory crashes.

Usage:
  python run_single_experiment.py --validator quantum_ion --experiment 1
  python run_single_experiment.py --validator bmd_frame --experiment 2
  python run_single_experiment.py --validator multiscale --experiment all

Author: Kundai Farai Sachikonye
Date: November 2025
"""

import os
import sys
import json
import argparse
from pathlib import Path
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Add parent directory to path
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))
sys.path.insert(0, str(current_dir.parent.parent))


def run_quantum_ion_experiment(experiment_num, results_dir="single_experiment_results"):
    """Run specific quantum ion experiment"""
    from quantum_ion_consciousness_validator import QuantumIonConsciousnessValidator
    
    print("\n" + "="*80)
    print("QUANTUM ION CONSCIOUSNESS VALIDATOR")
    print("="*80)
    
    validator = QuantumIonConsciousnessValidator(results_dir=f"{results_dir}/quantum_ion")
    
    experiments = {
        1: validator.experiment_1_ion_tunneling_dynamics,
        2: validator.experiment_2_collective_coherence_fields,
        3: validator.experiment_3_consciousness_timescale_coupling,
        4: validator.experiment_4_decoherence_resistance,
        5: validator.experiment_5_consciousness_state_transitions
    }
    
    if experiment_num == 'all':
        return validator.run_all_experiments()
    elif experiment_num in experiments:
        return experiments[experiment_num]()
    else:
        print(f"❌ Invalid experiment number: {experiment_num}")
        return None


def run_bmd_frame_experiment(experiment_num, results_dir="single_experiment_results"):
    """Run specific BMD frame selection experiment"""
    from bmd_frame_selection_validator import BMDFrameSelectionValidator
    
    print("\n" + "="*80)
    print("BMD FRAME SELECTION VALIDATOR")
    print("="*80)
    
    validator = BMDFrameSelectionValidator(results_dir=f"{results_dir}/bmd_frame")
    
    experiments = {
        1: validator.experiment_1_frame_selection_probability_dynamics,
        2: validator.experiment_2_counterfactual_selection_bias,
        3: validator.experiment_3_reality_frame_fusion_dynamics,
        4: validator.experiment_4_predetermined_landscape_navigation,
        5: validator.experiment_5_temporal_consistency_constraints
    }
    
    if experiment_num == 'all':
        return validator.run_all_experiments()
    elif experiment_num in experiments:
        return experiments[experiment_num]()
    else:
        print(f"❌ Invalid experiment number: {experiment_num}")
        return None


def run_multiscale_experiment(experiment_num, results_dir="single_experiment_results"):
    """Run specific multi-scale oscillatory experiment"""
    from multiscale_oscillatory_consciousness_validator import MultiScaleOscillatoryConsciousnessValidator
    
    print("\n" + "="*80)
    print("MULTI-SCALE OSCILLATORY CONSCIOUSNESS VALIDATOR")
    print("="*80)
    
    validator = MultiScaleOscillatoryConsciousnessValidator(results_dir=f"{results_dir}/multiscale")
    
    experiments = {
        1: validator.experiment_1_hierarchical_scale_synchronization,
        2: validator.experiment_2_cross_scale_coupling_validation,
        3: validator.experiment_3_consciousness_frequency_resonance,
        4: validator.experiment_4_oscillatory_coherence_windows,
        5: validator.experiment_5_consciousness_scale_integration
    }
    
    if experiment_num == 'all':
        return validator.run_all_experiments()
    elif experiment_num in experiments:
        return experiments[experiment_num]()
    else:
        print(f"❌ Invalid experiment number: {experiment_num}")
        return None


def main():
    parser = argparse.ArgumentParser(
        description="Run single validator experiments to avoid memory crashes"
    )
    parser.add_argument(
        '--validator',
        type=str,
        required=True,
        choices=['quantum_ion', 'bmd_frame', 'multiscale'],
        help='Which validator to run'
    )
    parser.add_argument(
        '--experiment',
        type=str,
        default='1',
        help='Which experiment to run (1-5 or "all")'
    )
    parser.add_argument(
        '--output-dir',
        type=str,
        default='single_experiment_results',
        help='Output directory for results'
    )
    
    args = parser.parse_args()
    
    # Parse experiment number
    if args.experiment == 'all':
        experiment_num = 'all'
    else:
        try:
            experiment_num = int(args.experiment)
            if not 1 <= experiment_num <= 5:
                print("❌ Experiment number must be between 1 and 5")
                return
        except ValueError:
            print("❌ Invalid experiment number. Use 1-5 or 'all'")
            return
    
    # Create output directory
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"\n🔬 Running {args.validator} - Experiment {experiment_num}")
    print(f"📁 Results directory: {output_dir}")
    print("="*80)
    
    # Run selected validator
    try:
        if args.validator == 'quantum_ion':
            results = run_quantum_ion_experiment(experiment_num, args.output_dir)
        elif args.validator == 'bmd_frame':
            results = run_bmd_frame_experiment(experiment_num, args.output_dir)
        elif args.validator == 'multiscale':
            results = run_multiscale_experiment(experiment_num, args.output_dir)
        
        if results:
            print("\n✅ EXPERIMENT COMPLETED SUCCESSFULLY!")
            print(f"📊 Results saved to: {output_dir}")
            
            # Save summary
            summary_file = output_dir / f"{args.validator}_exp_{experiment_num}_summary.json"
            with open(summary_file, 'w') as f:
                json.dump({
                    'validator': args.validator,
                    'experiment': experiment_num,
                    'timestamp': datetime.now().isoformat(),
                    'success': True,
                    'results_summary': str(results.get('validation_success', 'N/A'))
                }, f, indent=2)
            
            print(f"📝 Summary saved to: {summary_file}")
        else:
            print("\n❌ EXPERIMENT FAILED")
    
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())

