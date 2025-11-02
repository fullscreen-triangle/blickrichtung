#!/usr/bin/env python3
"""
Comprehensive Experimental Framework for Oscillatory Consciousness Validators

This script runs all available validators systematically and generates
comprehensive results for validating the complete theoretical framework.

Author: Kundai Farai Sachikonye
Date: November 2025
"""

import os
import sys
import json
import time
from pathlib import Path
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Add parent directory to path for imports
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))
sys.path.insert(0, str(current_dir.parent.parent))  # project root

class ComprehensiveExperimentalFramework:
    """
    Master framework for running all oscillatory validators and
    collecting comprehensive experimental results.
    """
    
    def __init__(self, results_dir="comprehensive_validation_results"):
        """Initialize the experimental framework."""
        self.results_dir = Path(results_dir)
        self.results_dir.mkdir(parents=True, exist_ok=True)
        
        self.results = {
            'start_time': datetime.now().isoformat(),
            'validators': {},
            'summary': {},
            'errors': []
        }
        
        print("="*80)
        print("COMPREHENSIVE OSCILLATORY CONSCIOUSNESS EXPERIMENTAL FRAMEWORK")
        print("="*80)
        print(f"Results directory: {self.results_dir}")
        print(f"Start time: {self.results['start_time']}")
        print("="*80 + "\n")
    
    def run_comprehensive_consciousness_validator(self):
        """Run the master comprehensive consciousness validator."""
        print("\n" + "="*80)
        print("1. COMPREHENSIVE CONSCIOUSNESS VALIDATOR")
        print("="*80)
        
        try:
            from comprehensive_consciousness_validator import ComprehensiveConsciousnessValidator
            
            print("Initializing ComprehensiveConsciousnessValidator...")
            validator = ComprehensiveConsciousnessValidator(
                results_dir=str(self.results_dir / "comprehensive_consciousness")
            )
            
            print("Running comprehensive validation...")
            start_time = time.time()
            results = validator.run_comprehensive_validation()
            elapsed_time = time.time() - start_time
            
            self.results['validators']['comprehensive_consciousness'] = {
                'status': 'success',
                'elapsed_time': elapsed_time,
                'results_summary': self._extract_summary(results),
                'results_path': str(self.results_dir / "comprehensive_consciousness")
            }
            
            print(f"✓ Comprehensive consciousness validation complete ({elapsed_time:.2f}s)")
            return results
            
        except Exception as e:
            print(f"❌ Error in comprehensive consciousness validator: {e}")
            self.results['errors'].append({
                'validator': 'comprehensive_consciousness',
                'error': str(e)
            })
            return None
    
    def run_multiscale_validator(self):
        """Run the multi-scale oscillatory consciousness validator."""
        print("\n" + "="*80)
        print("2. MULTI-SCALE OSCILLATORY CONSCIOUSNESS VALIDATOR")
        print("="*80)
        
        try:
            from multiscale_oscillatory_consciousness_validator import MultiScaleOscillatoryConsciousnessValidator
            
            print("Initializing MultiScaleOscillatoryConsciousnessValidator...")
            validator = MultiScaleOscillatoryConsciousnessValidator(
                results_dir=str(self.results_dir / "multiscale_oscillatory")
            )
            
            print("Running all experiments...")
            start_time = time.time()
            results = validator.run_all_experiments()
            elapsed_time = time.time() - start_time
            
            self.results['validators']['multiscale_oscillatory'] = {
                'status': 'success',
                'elapsed_time': elapsed_time,
                'results_summary': self._extract_summary(results),
                'results_path': str(self.results_dir / "multiscale_oscillatory")
            }
            
            print(f"✓ Multi-scale validation complete ({elapsed_time:.2f}s)")
            return results
            
        except Exception as e:
            print(f"❌ Error in multi-scale validator: {e}")
            self.results['errors'].append({
                'validator': 'multiscale_oscillatory',
                'error': str(e)
            })
            return None
    
    def run_activity_sleep_mirror_validator(self, activity_path=None, sleep_path=None):
        """Run the activity-sleep oscillatory mirror validator."""
        print("\n" + "="*80)
        print("3. ACTIVITY-SLEEP OSCILLATORY MIRROR VALIDATOR")
        print("="*80)
        
        try:
            from sleep_activity_oscillatory_mirror_validator import ActivitySleepOscillatoryMirrorValidator
            
            print("Initializing ActivitySleepOscillatoryMirrorValidator...")
            validator = ActivitySleepOscillatoryMirrorValidator(
                results_dir=str(self.results_dir / "activity_sleep_mirror")
            )
            
            # Set default paths if not provided
            if activity_path is None:
                activity_path = Path(__file__).parent.parent.parent.parent / "public" / "activity.json"
            if sleep_path is None:
                sleep_path = Path(__file__).parent.parent.parent.parent / "public" / "sleep_summary.json"
            
            print(f"Activity data: {activity_path}")
            print(f"Sleep data: {sleep_path}")
            
            # Check if files exist
            if not Path(activity_path).exists():
                print(f"⚠ Activity file not found: {activity_path}")
                print("  Running with synthetic data...")
                activity_path = None
            
            if not Path(sleep_path).exists():
                print(f"⚠ Sleep file not found: {sleep_path}")
                print("  Running with synthetic data...")
                sleep_path = None
            
            print("Running comprehensive validation...")
            start_time = time.time()
            results = validator.run_comprehensive_validation(
                activity_json_path=str(activity_path) if activity_path else None,
                sleep_json_path=str(sleep_path) if sleep_path else None
            )
            elapsed_time = time.time() - start_time
            
            self.results['validators']['activity_sleep_mirror'] = {
                'status': 'success',
                'elapsed_time': elapsed_time,
                'results_summary': self._extract_summary(results),
                'results_path': str(self.results_dir / "activity_sleep_mirror"),
                'data_source': 'real' if activity_path and sleep_path else 'synthetic'
            }
            
            print(f"✓ Activity-sleep mirror validation complete ({elapsed_time:.2f}s)")
            return results
            
        except Exception as e:
            print(f"❌ Error in activity-sleep mirror validator: {e}")
            import traceback
            traceback.print_exc()
            self.results['errors'].append({
                'validator': 'activity_sleep_mirror',
                'error': str(e)
            })
            return None
    
    def run_bmd_frame_validator(self):
        """Run the BMD frame selection validator."""
        print("\n" + "="*80)
        print("4. BMD FRAME SELECTION VALIDATOR")
        print("="*80)
        
        try:
            from bmd_frame_selection_validator import BMDFrameSelectionValidator
            
            print("Initializing BMDFrameSelectionValidator...")
            validator = BMDFrameSelectionValidator(
                results_dir=str(self.results_dir / "bmd_frame_selection")
            )
            
            print("Running all experiments...")
            start_time = time.time()
            results = validator.run_all_experiments()
            elapsed_time = time.time() - start_time
            
            self.results['validators']['bmd_frame_selection'] = {
                'status': 'success',
                'elapsed_time': elapsed_time,
                'results_summary': self._extract_summary(results),
                'results_path': str(self.results_dir / "bmd_frame_selection")
            }
            
            print(f"✓ BMD frame selection validation complete ({elapsed_time:.2f}s)")
            return results
            
        except Exception as e:
            print(f"❌ Error in BMD frame validator: {e}")
            self.results['errors'].append({
                'validator': 'bmd_frame_selection',
                'error': str(e)
            })
            return None
    
    def run_fire_consciousness_validator(self):
        """Run the fire-consciousness coupling validator."""
        print("\n" + "="*80)
        print("5. FIRE-CONSCIOUSNESS COUPLING VALIDATOR")
        print("="*80)
        
        try:
            from fire_consciousness_coupling_validator import FireConsciousnessCouplingValidator
            
            print("Initializing FireConsciousnessCouplingValidator...")
            validator = FireConsciousnessCouplingValidator(
                results_dir=str(self.results_dir / "fire_consciousness")
            )
            
            print("Running all experiments...")
            start_time = time.time()
            results = validator.run_all_experiments()
            elapsed_time = time.time() - start_time
            
            self.results['validators']['fire_consciousness'] = {
                'status': 'success',
                'elapsed_time': elapsed_time,
                'results_summary': self._extract_summary(results),
                'results_path': str(self.results_dir / "fire_consciousness")
            }
            
            print(f"✓ Fire-consciousness validation complete ({elapsed_time:.2f}s)")
            return results
            
        except Exception as e:
            print(f"❌ Error in fire-consciousness validator: {e}")
            self.results['errors'].append({
                'validator': 'fire_consciousness',
                'error': str(e)
            })
            return None
    
    def run_quantum_ion_validator(self):
        """Run the quantum ion consciousness validator."""
        print("\n" + "="*80)
        print("6. QUANTUM ION CONSCIOUSNESS VALIDATOR")
        print("="*80)
        
        try:
            from quantum_ion_consciousness_validator import QuantumIonConsciousnessValidator
            
            print("Initializing QuantumIonConsciousnessValidator...")
            validator = QuantumIonConsciousnessValidator(
                results_dir=str(self.results_dir / "quantum_ion")
            )
            
            print("Running all experiments...")
            start_time = time.time()
            results = validator.run_all_experiments()
            elapsed_time = time.time() - start_time
            
            self.results['validators']['quantum_ion'] = {
                'status': 'success',
                'elapsed_time': elapsed_time,
                'results_summary': self._extract_summary(results),
                'results_path': str(self.results_dir / "quantum_ion")
            }
            
            print(f"✓ Quantum ion validation complete ({elapsed_time:.2f}s)")
            return results
            
        except Exception as e:
            print(f"❌ Error in quantum ion validator: {e}")
            self.results['errors'].append({
                'validator': 'quantum_ion',
                'error': str(e)
            })
            return None
    
    def _extract_summary(self, results):
        """Extract key summary statistics from results."""
        if not results:
            return None
        
        summary = {}
        
        # Try to extract common patterns
        if isinstance(results, dict):
            for key, value in results.items():
                if isinstance(value, dict):
                    # Look for common result patterns
                    if 'success' in value:
                        summary[key] = {'success': value['success']}
                    elif 'mean' in value or 'std' in value:
                        summary[key] = {
                            k: v for k, v in value.items() 
                            if k in ['mean', 'std', 'min', 'max', 'count']
                        }
        
        return summary if summary else {'note': 'See full results in directory'}
    
    def generate_comprehensive_report(self):
        """Generate comprehensive experimental report."""
        print("\n" + "="*80)
        print("GENERATING COMPREHENSIVE REPORT")
        print("="*80)
        
        self.results['end_time'] = datetime.now().isoformat()
        
        # Calculate totals
        successful = sum(1 for v in self.results['validators'].values() if v['status'] == 'success')
        failed = len(self.results['errors'])
        total_time = sum(v.get('elapsed_time', 0) for v in self.results['validators'].values())
        
        self.results['summary'] = {
            'total_validators_run': successful + failed,
            'successful': successful,
            'failed': failed,
            'total_elapsed_time': total_time
        }
        
        # Save results
        results_path = self.results_dir / "comprehensive_experimental_results.json"
        with open(results_path, 'w') as f:
            json.dump(self.results, f, indent=2, default=str)
        
        # Print summary
        print(f"\n{'='*80}")
        print("EXPERIMENTAL RESULTS SUMMARY")
        print(f"{'='*80}")
        print(f"Total validators run: {successful + failed}")
        print(f"Successful: {successful}")
        print(f"Failed: {failed}")
        print(f"Total time: {total_time:.2f} seconds ({total_time/60:.2f} minutes)")
        print(f"\nResults saved to: {results_path}")
        print(f"{'='*80}\n")
        
        return self.results
    
    def run_all_experiments(self, use_real_data=True):
        """Run all experimental validators."""
        print("Starting comprehensive experimental validation...")
        print("This will run all available validators systematically.\n")
        
        # 1. Comprehensive Consciousness Validator (master integrator)
        self.run_comprehensive_consciousness_validator()
        
        # 2. Multi-Scale Oscillatory Validator
        self.run_multiscale_validator()
        
        # 3. Activity-Sleep Mirror Validator (with real data if available)
        if use_real_data:
            self.run_activity_sleep_mirror_validator()
        else:
            self.run_activity_sleep_mirror_validator(activity_path=None, sleep_path=None)
        
        # 4. BMD Frame Selection Validator
        self.run_bmd_frame_validator()
        
        # 5. Fire-Consciousness Coupling Validator
        self.run_fire_consciousness_validator()
        
        # 6. Quantum Ion Consciousness Validator
        self.run_quantum_ion_validator()
        
        # Generate comprehensive report
        final_results = self.generate_comprehensive_report()
        
        return final_results


def main():
    """Main execution function."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Run comprehensive oscillatory consciousness experiments"
    )
    parser.add_argument(
        '--output-dir',
        type=str,
        default='comprehensive_validation_results',
        help='Output directory for results (default: comprehensive_validation_results)'
    )
    parser.add_argument(
        '--synthetic-data',
        action='store_true',
        help='Use synthetic data instead of real biometric data'
    )
    parser.add_argument(
        '--quick',
        action='store_true',
        help='Run quick tests (reduced iterations)'
    )
    
    args = parser.parse_args()
    
    # Initialize framework
    framework = ComprehensiveExperimentalFramework(results_dir=args.output_dir)
    
    # Run all experiments
    use_real_data = not args.synthetic_data
    results = framework.run_all_experiments(use_real_data=use_real_data)
    
    print("\n🎊 COMPREHENSIVE EXPERIMENTAL VALIDATION COMPLETE! 🎊\n")
    
    if results['summary']['failed'] == 0:
        print("✓ All validators completed successfully!")
    else:
        print(f"⚠ {results['summary']['failed']} validator(s) encountered errors")
        print("  Check the errors section in the results file for details")
    
    print(f"\nFull results: {framework.results_dir}/comprehensive_experimental_results.json")
    print("\nNext steps:")
    print("1. Review individual validator results in subdirectories")
    print("2. Analyze generated figures and visualizations")
    print("3. Compare results against theoretical predictions")
    print("4. Integrate findings into research papers")
    
    return results


if __name__ == "__main__":
    results = main()

