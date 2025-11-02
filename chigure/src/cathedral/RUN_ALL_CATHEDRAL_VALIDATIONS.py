#!/usr/bin/env python3
"""
Master Validation Script for Cathedral Framework
=================================================

Runs all validation experiments and generates comprehensive reports.

Usage:
    python RUN_ALL_CATHEDRAL_VALIDATIONS.py

This will:
1. Run all 13 validation modules
2. Generate 4+ chart panels for each
3. Save JSON results
4. Create comprehensive text reports
5. Compile master summary

Modules:
- oxygen_distinguishability: 10^33× bandwidth enhancement
- charge_dynamics: P-N junction, hole mobility
- membrane_computing: 240-BMD Turing-complete circuit
- circuit_pathway: Circuit-pathway duality theorem
- drug_membrane: Pharmaceutical sensing and delivery
- membrane_composition: Lipid formulation optimization
- circuit_integration: 7-component architecture
- topological_enhancements: Graph densification, Turing completeness
- membrane_performance: Response time, spatial resolution
- adverserial_robustness: Clinical robustness requirements
- bmd_equivalence: Cross-modal BMD equivalence
- s_entropy_validation: Predetermined solutions, complexity reduction
- statistical_reporting: Publication-ready statistics
"""

import sys
import time
from pathlib import Path
from datetime import datetime

def run_all_validations():
    """Run all cathedral validation modules"""
    
    print("\n" + "="*100)
    print(" " * 30 + "CATHEDRAL FRAMEWORK VALIDATION")
    print("=" * 100 + "\n")
    print("Running comprehensive validation of membrane computing interface...")
    print("This will generate 13 validation reports with 4+ chart panels each.\n")
    
    modules_to_run = [
        ('oxygen_distinguishability', 'Oxygen Categorical Distinguishability'),
        ('charge_dynamics', 'Charge Dynamics and P-N Junctions'),
        ('membrane_computing', 'Membrane Computing - 240-BMD Circuit'),
        ('circuit_pathway', 'Circuit-Pathway Duality Theorem'),
        ('drug_membrane', 'Pharmaceutical Sensing and Delivery'),
        ('membrane_composition', 'Membrane Composition Optimization'),
        ('circuit_integration', 'Circuit Integration - 7 Components'),
        ('topological_enhancements', 'Topological Graph Enhancement'),
        ('membrane_performance', 'Membrane Performance Metrics'),
        ('adverserial_robustness', 'Adversarial Robustness'),
        ('bmd_equivalence', 'BMD Cross-Modal Equivalence'),
        ('s_entropy_validation', 'S-Entropy Navigation'),
        ('statistical_reporting', 'Statistical Validation Summary')
    ]
    
    results_summary = {}
    start_time = time.time()
    
    for i, (module_name, description) in enumerate(modules_to_run, 1):
        print(f"\n[{i}/13] Running: {description}...")
        print("-" * 100)
        
        module_start = time.time()
        
        try:
            # Import and run module
            module = __import__(module_name)
            
            # Find validator class
            validator_class = None
            for attr_name in dir(module):
                if 'Validator' in attr_name and not attr_name.startswith('_'):
                    validator_class = getattr(module, attr_name)
                    break
            
            if validator_class:
                validator = validator_class()
                result = validator.save_comprehensive_results()
                
                results_summary[module_name] = {
                    'status': 'SUCCESS',
                    'description': description,
                    'duration_s': time.time() - module_start,
                    'result': result
                }
                print(f"✓ Completed in {time.time() - module_start:.2f}s")
            else:
                results_summary[module_name] = {
                    'status': 'SKIPPED',
                    'description': description,
                    'reason': 'No validator class found'
                }
                print(f"⊘ Skipped (no validator class)")
                
        except Exception as e:
            results_summary[module_name] = {
                'status': 'FAILED',
                'description': description,
                'error': str(e),
                'duration_s': time.time() - module_start
            }
            print(f"✗ Failed: {str(e)}")
    
    total_duration = time.time() - start_time
    
    # Generate master summary report
    print("\n" + "="*100)
    print("GENERATING MASTER SUMMARY REPORT")
    print("="*100 + "\n")
    
    results_dir = Path('results/cathedral')
    results_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    summary_path = results_dir / f'master_summary_{timestamp}.txt'
    with open(summary_path, 'w', encoding='utf-8') as f:
        f.write("=" * 100 + "\n")
        f.write(" " * 30 + "CATHEDRAL FRAMEWORK VALIDATION SUMMARY\n")
        f.write("=" * 100 + "\n\n")
        f.write(f"Generated: {timestamp}\n")
        f.write(f"Total Duration: {total_duration:.2f} seconds\n\n")
        
        f.write("MODULES RUN:\n")
        f.write("-" * 100 + "\n")
        
        success_count = 0
        failed_count = 0
        skipped_count = 0
        
        for module_name, result in results_summary.items():
            status_symbol = {
                'SUCCESS': '✓',
                'FAILED': '✗',
                'SKIPPED': '⊘'
            }.get(result['status'], '?')
            
            f.write(f"{status_symbol} {result['description']:<50} [{result['status']}]\n")
            
            if result['status'] == 'SUCCESS':
                success_count += 1
                f.write(f"   Duration: {result['duration_s']:.2f}s\n")
            elif result['status'] == 'FAILED':
                failed_count += 1
                f.write(f"   Error: {result.get('error', 'Unknown')}\n")
            elif result['status'] == 'SKIPPED':
                skipped_count += 1
                f.write(f"   Reason: {result.get('reason', 'Unknown')}\n")
            
            f.write("\n")
        
        f.write("=" * 100 + "\n")
        f.write("SUMMARY STATISTICS:\n")
        f.write("-" * 100 + "\n")
        f.write(f"Total Modules: {len(results_summary)}\n")
        f.write(f"Successful: {success_count}\n")
        f.write(f"Failed: {failed_count}\n")
        f.write(f"Skipped: {skipped_count}\n")
        f.write(f"Success Rate: {success_count/len(results_summary)*100:.1f}%\n")
        f.write("=" * 100 + "\n")
    
    print(f"✓ Master summary saved: {summary_path}")
    
    print("\n" + "="*100)
    print("CATHEDRAL FRAMEWORK VALIDATION COMPLETE")
    print("="*100)
    print(f"Total Duration: {total_duration:.2f} seconds")
    print(f"Successful: {success_count}/{len(results_summary)}")
    print(f"Results directory: {results_dir.absolute()}")
    print("="*100 + "\n")
    
    return results_summary

if __name__ == "__main__":
    try:
        results = run_all_validations()
        print("\n✓ All validations complete! Check results/cathedral/ for outputs.\n")
    except KeyboardInterrupt:
        print("\n\n⚠ Validation interrupted by user.\n")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n✗ Validation failed with error: {str(e)}\n")
        sys.exit(1)

