#!/usr/bin/env python3
"""
Proper Thought Metabolism Validation Using Existing Validator Framework

This script uses the existing activity_sleep_oscillatory_mirror_validator.py
to properly calculate thought metabolism with REAL mirror pairs.

Author: Blickrichtung Research Team
Date: November 2025
"""

import sys
import os
from pathlib import Path
import json

# Add geometry validators to path
geometry_path = Path(__file__).parent.parent / 'geometry'
sys.path.insert(0, str(geometry_path))

try:
    from sleep_activity_oscillatory_mirror_validator import ActivitySleepOscillatoryMirrorValidator
    print("✅ Successfully imported ActivitySleepOscillatoryMirrorValidator")
except ImportError as e:
    print(f"❌ Failed to import validator: {e}")
    print(f"   Tried path: {geometry_path}")
    sys.exit(1)

def run_proper_thought_metabolism_validation():
    """
    Run proper thought metabolism validation using the existing validator framework.
    """
    print("\n" + "="*80)
    print("🧠💡 PROPER THOUGHT METABOLISM VALIDATION 💡🧠")
    print("="*80)
    print("Using existing activity_sleep_oscillatory_mirror_validator.py")
    print("="*80 + "\n")
    
    # Set up paths
    project_root = Path(__file__).parent.parent.parent.parent
    public_dir = project_root / 'public'
    output_dir = Path(__file__).parent / 'output' / 'proper_validation'
    
    activity_path = public_dir / 'activity.json'
    sleep_path = public_dir / 'sleep_summary.json'
    
    # Verify files exist
    if not activity_path.exists():
        print(f"❌ Activity data not found: {activity_path}")
        return None
    
    if not sleep_path.exists():
        print(f"❌ Sleep data not found: {sleep_path}")
        return None
    
    print(f"✅ Found activity data: {activity_path}")
    print(f"✅ Found sleep data: {sleep_path}")
    print(f"📊 Results will be saved to: {output_dir}")
    print()
    
    # Create output directory
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Initialize validator
    print("🔧 Initializing Activity-Sleep Oscillatory Mirror Validator...")
    validator = ActivitySleepOscillatoryMirrorValidator(results_dir=str(output_dir))
    
    # Load data
    print("📁 Loading biometric data...")
    success_activity = validator.load_activity_data(str(activity_path))
    success_sleep = validator.load_sleep_data(str(sleep_path))
    
    if not (success_activity and success_sleep):
        print("❌ Failed to load data")
        return None
    
    print(f"✅ Loaded {len(validator.activity_data)} activity records")
    print(f"✅ Loaded {len(validator.sleep_data)} sleep records")
    print()
    
    # Run comprehensive validation
    print("🧪 Running comprehensive validation...")
    print("   This validates:")
    print("   1. Oscillatory Mirror Hypothesis")
    print("   2. Error Accumulation Model")
    print("   3. Sleep Cleanup Efficiency")
    print("   4. Circadian Coupling Analysis")
    print("   5. Mirror Pattern Recognition")
    print()
    
    try:
        results = validator.run_comprehensive_validation(
            activity_json_path=str(activity_path),
            sleep_json_path=str(sleep_path)
        )
        
        print("\n" + "="*80)
        print("✅ VALIDATION COMPLETE!")
        print("="*80)
        
        # Extract key results
        print("\n📊 KEY RESULTS:")
        print("-" * 60)
        
        if 'oscillatory_mirror_hypothesis' in results:
            mirror_results = results['oscillatory_mirror_hypothesis']
            
            # Mirror pairs
            cleanup_validation = mirror_results.get('cleanup_validation', [])
            num_mirror_pairs = len(cleanup_validation)
            print(f"🪞 Mirror Pairs Found: {num_mirror_pairs}")
            
            if num_mirror_pairs > 0:
                # Mirror pattern strength
                mirror_strength = mirror_results.get('mirror_pattern_strength', 0)
                print(f"💪 Mirror Pattern Strength: {mirror_strength:.3f}")
                
                # Statistical significance
                stats = mirror_results.get('statistical_significance', {})
                if stats:
                    correlation = stats.get('error_cleanup_correlation', 0)
                    p_value = stats.get('p_value', 1.0)
                    significance = stats.get('significance_level', 'unknown')
                    
                    print(f"📈 Error-Cleanup Correlation: {correlation:.3f}")
                    print(f"📊 P-value: {p_value:.4f}")
                    print(f"✨ Significance Level: {significance}")
                
                # Sample mirror pairs
                print(f"\n📋 First 5 Mirror Pairs:")
                for i, pair in enumerate(cleanup_validation[:5], 1):
                    date = pair.get('date', 'unknown')
                    error = pair.get('total_error', 0)
                    cleanup = pair.get('cleanup_effectiveness', 0)
                    ratio = pair.get('error_cleanup_ratio', 0)
                    
                    print(f"   Pair {i}: Error={error:.2f}, Cleanup={cleanup:.2f}, Ratio={ratio:.2f}")
            else:
                print("⚠️  No mirror pairs found. This may indicate:")
                print("    1. Timestamp matching issue")
                print("    2. Data format mismatch")
                print("    3. Need to adjust matching window")
        
        # Error accumulation model
        if 'error_accumulation_model' in results:
            error_results = results['error_accumulation_model']
            patterns = error_results.get('accumulation_patterns', [])
            print(f"\n📈 Error Accumulation Patterns: {len(patterns)} analyzed")
            
            if patterns:
                avg_error = sum(p.get('total_error', 0) for p in patterns) / len(patterns)
                print(f"   Average Daily Error: {avg_error:.2f}")
        
        # Sleep cleanup efficiency
        if 'sleep_cleanup_efficiency' in results:
            cleanup_results = results['sleep_cleanup_efficiency']
            efficiency = cleanup_results.get('efficiency_patterns', [])
            print(f"\n🛌 Sleep Cleanup Efficiency: {len(efficiency)} nights analyzed")
            
            if efficiency:
                avg_cleanup = sum(p.get('total_effectiveness', 0) for p in efficiency) / len(efficiency)
                print(f"   Average Cleanup Effectiveness: {avg_cleanup:.2f}")
        
        # Circadian coupling
        if 'circadian_coupling' in results:
            circadian_results = results['circadian_coupling']
            coupling_strength = circadian_results.get('coupling_strength', 0)
            print(f"\n🌙 Circadian Coupling Strength: {coupling_strength:.3f}")
        
        # Mirror pattern recognition
        if 'mirror_pattern_recognition' in results:
            pattern_results = results['mirror_pattern_recognition']
            pattern_strength = pattern_results.get('pattern_strength', 0)
            coefficients = pattern_results.get('mirror_coefficients', [])
            print(f"\n🔍 Mirror Pattern Recognition:")
            print(f"   Pattern Strength: {pattern_strength:.3f}")
            print(f"   Mirror Coefficients Calculated: {len(coefficients)}")
            if coefficients:
                avg_coeff = sum(coefficients) / len(coefficients)
                print(f"   Average Mirror Coefficient: {avg_coeff:.3f}")
        
        print("\n" + "-" * 60)
        print(f"📁 Complete results saved to: {output_dir}")
        print("="*80 + "\n")
        
        # Save summary
        summary_path = output_dir / 'validation_summary.json'
        with open(summary_path, 'w') as f:
            json.dump(results, f, indent=2, default=str)
        
        print(f"✅ Summary saved: {summary_path}")
        
        # Check if we got usable results
        if num_mirror_pairs > 0:
            print("\n🎉 SUCCESS! Found mirror pairs!")
            print("   Next steps:")
            print("   1. Review results in output directory")
            print("   2. Extract thought energy from error-cleanup differences")
            print("   3. Update metabolism paper with real numbers")
        else:
            print("\n⚠️  No mirror pairs found.")
            print("   Possible solutions:")
            print("   1. Check data timestamp formats")
            print("   2. Adjust matching window in validator")
            print("   3. Review data quality and completeness")
        
        return results
        
    except Exception as e:
        print(f"\n❌ Validation failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return None


def main():
    """Main execution"""
    results = run_proper_thought_metabolism_validation()
    
    if results:
        print("\n✅ Validation completed successfully!")
        return 0
    else:
        print("\n❌ Validation failed. Please check errors above.")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)

