import json
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.gridspec import GridSpec
from scipy import signal, stats
from scipy.interpolate import interp1d
import pandas as pd
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

matplotlib.use('Agg')  # Non-interactive backend
sns.set_style("whitegrid")

def load_all_data():
    """Load comprehensive sleep and activity data"""
    print("Loading 24/7 metabolic data...")
    
    with open('public/infraredSleep.json', 'r') as f:
        infrared_sleep = json.load(f)
    
    with open('public/sleep_summary.json', 'r') as f:
        sleep_summary = json.load(f)
    
    with open('public/sleepRecords.json', 'r') as f:
        sleep_records = json.load(f)
    
    with open('public/activity.json', 'r') as f:
        activity = json.load(f)
    
    with open('public/readiness_records.json', 'r') as f:
        readiness_records = json.load(f)
    
    with open('public/readinessDataRecords.json', 'r') as f:
        readiness_data = json.load(f)
    
    return {
        'infrared_sleep': infrared_sleep,
        'sleep_summary': sleep_summary,
        'sleep_records': sleep_records,
        'activity': activity,
        'readiness_records': readiness_records,
        'readiness_data': readiness_data
    }

def safe_mean(data):
    """Safely calculate mean, handling NaN values"""
    try:
        if isinstance(data, list):
            values = [x for x in data if x is not None and np.isfinite(x) and x > 0]
        else:
            values = [data] if data is not None and np.isfinite(data) and data > 0 else []
        return np.mean(values) if len(values) > 0 else np.nan
    except:
        return np.nan

def safe_std(data):
    """Safely calculate std, handling NaN values"""
    try:
        if isinstance(data, list):
            values = [x for x in data if x is not None and np.isfinite(x) and x > 0]
        else:
            values = [data] if data is not None and np.isfinite(data) and data > 0 else []
        return np.std(values) if len(values) > 1 else np.nan
    except:
        return np.nan

def extract_rem_periods(data):
    """Extract REM sleep periods from Oura sleep data"""
    print("\nExtracting REM dream signature...")
    
    rem_periods = []
    
    # Process infraredSleep data (most detailed)
    if 'infrared_sleep' in data and data['infrared_sleep']:
        for sleep_session in data['infrared_sleep']:
            # Get time series data
            hr_5min = sleep_session.get('hr_5min', [])
            hrv_5min = sleep_session.get('hrv_5min', [])
            hypnogram_5min = sleep_session.get('hypnogram_5min', [])
            
            # Oura hypnogram codes: 1=deep, 2=light, 3=REM, 4=awake
            for i, sleep_stage in enumerate(hypnogram_5min):
                if sleep_stage == 3:  # REM sleep
                    # Get corresponding HR and HRV
                    if i < len(hr_5min) and i < len(hrv_5min):
                        hr = hr_5min[i]
                        hrv = hrv_5min[i]
                        
                        if hr and hr > 0 and hrv and hrv > 0:
                            rem_periods.append({
                                'hr': hr,
                                'hrv': hrv,
                                'timestamp': i * 300,  # 5-minute intervals
                                'metabolic': hr * 1.2 + hrv * 0.5,
                                'date': sleep_session.get('date', 'unknown')
                            })
    
    if len(rem_periods) == 0:
        print("⚠ No REM periods found in infraredSleep data")
        return []
    
    print(f"✓ Extracted {len(rem_periods)} REM periods")
    
    # Calculate statistics
    hr_values = [p['hr'] for p in rem_periods]
    hrv_values = [p['hrv'] for p in rem_periods]
    met_values = [p['metabolic'] for p in rem_periods]
    
    print(f"  - Mean REM HR: {safe_mean(hr_values):.1f} bpm")
    print(f"  - Mean REM HRV: {safe_mean(hrv_values):.1f} ms")
    print(f"  - Mean REM Metabolic: {safe_mean(met_values):.1f}")
    
    return rem_periods

def extract_waking_periods(data):
    """Extract waking periods from Oura activity data"""
    print("\nExtracting waking metabolic states...")
    
    waking_periods = []
    
    # Process activity data
    if 'activity' in data and data['activity']:
        for day_activity in data['activity']:
            # Get MET (Metabolic Equivalent) data
            met_1min = day_activity.get('met_1min', [])
            
            # Get activity classification (5-min intervals)
            # '0'=non-wear, '1'=rest, '2'=inactive, '3'=low, '4'=medium, '5'=high
            class_5min = day_activity.get('class_5min', '')
            
            # Estimate HR from MET (rough approximation)
            # Resting HR ≈ 60 bpm, each MET unit adds ~10 bpm
            for i, met_value in enumerate(met_1min):
                if met_value and met_value > 0:
                    # Estimate HR from MET
                    estimated_hr = 60 + (met_value - 1) * 10
                    
                    # Estimate HRV (inversely related to HR)
                    estimated_hrv = max(20, 100 - (estimated_hr - 60))
                    
                    # Get activity class for this minute
                    class_idx = i // 5  # Convert 1-min to 5-min index
                    activity_class = class_5min[class_idx] if class_idx < len(class_5min) else '0'
                    
                    # Only include awake periods (not rest/sleep)
                    if activity_class not in ['0', '1'] and met_value > 1.0:
                        waking_periods.append({
                            'hr': estimated_hr,
                            'hrv': estimated_hrv,
                            'met': met_value,
                            'timestamp': i * 60,  # Minutes to seconds
                            'metabolic': estimated_hr * 1.2 + estimated_hrv * 0.5,
                            'activity_class': activity_class,
                            'date': day_activity.get('date', 'unknown')
                        })
    
    # Also extract from readiness data (resting HR during day)
    if 'readiness_data' in data and data['readiness_data']:
        for readiness in data['readiness_data']:
            resting_hr = readiness.get('resting_heart_rate.bpm')
            
            if resting_hr and resting_hr > 0:
                # Estimate HRV for resting state
                estimated_hrv = 60.0  # Typical resting HRV
                
                waking_periods.append({
                    'hr': resting_hr,
                    'hrv': estimated_hrv,
                    'met': 1.0,
                    'timestamp': 0,
                    'metabolic': resting_hr * 1.2 + estimated_hrv * 0.5,
                    'activity_class': 'resting',
                    'date': readiness.get('date', 'unknown')
                })
    
    if len(waking_periods) == 0:
        print("⚠ No waking periods found")
        return []
    
    print(f"✓ Extracted {len(waking_periods)} waking periods")
    
    # Calculate statistics
    hr_values = [p['hr'] for p in waking_periods]
    hrv_values = [p['hrv'] for p in waking_periods]
    
    print(f"  - Mean Waking HR: {safe_mean(hr_values):.1f} bpm")
    print(f"  - Mean Waking HRV: {safe_mean(hrv_values):.1f} ms")
    print(f"  - HR range: {min(hr_values):.1f} - {max(hr_values):.1f} bpm")
    
    return waking_periods

def find_rem_cognates(rem_periods, waking_periods, tolerance=0.2):
    """Find waking periods that match REM signature (deep thought periods)"""
    print("\nSearching for waking REM cognates (thought periods)...")
    
    if len(rem_periods) == 0 or len(waking_periods) == 0:
        print("⚠ Cannot find cognates - missing REM or waking data")
        return []
    
    # Calculate REM signature ranges
    rem_hr = [p['hr'] for p in rem_periods]
    rem_hrv = [p['hrv'] for p in rem_periods]
    rem_met = [p['metabolic'] for p in rem_periods]
    
    rem_hr_mean = safe_mean(rem_hr)
    rem_hr_std = safe_std(rem_hr)
    rem_hrv_mean = safe_mean(rem_hrv)
    rem_hrv_std = safe_std(rem_hrv)
    rem_met_mean = safe_mean(rem_met)
    rem_met_std = safe_std(rem_met)
    
    print(f"\nREM Signature Ranges:")
    print(f"  HR: {rem_hr_mean:.1f} ± {rem_hr_std:.1f} bpm")
    print(f"  HRV: {rem_hrv_mean:.1f} ± {rem_hrv_std:.1f} ms")
    print(f"  Metabolic: {rem_met_mean:.1f} ± {rem_met_std:.1f}")
    
    # Find matching waking periods
    cognates = []
    
    for wp in waking_periods:
        # Calculate match score (normalized distance)
        hr_match = abs(wp['hr'] - rem_hr_mean) / (rem_hr_std + 1e-6)
        hrv_match = abs(wp['hrv'] - rem_hrv_mean) / (rem_hrv_std + 1e-6)
        met_match = abs(wp['metabolic'] - rem_met_mean) / (rem_met_std + 1e-6)
        
        # Combined match score (lower is better)
        match_score = (hr_match + hrv_match + met_match) / 3.0
        
        # Accept if within tolerance
        if match_score < tolerance:
            cognates.append({
                **wp,
                'match_score': match_score,
                'rem_hr_mean': rem_hr_mean,
                'rem_hrv_mean': rem_hrv_mean
            })
    
    print(f"\n✓ Found {len(cognates)} waking REM cognates")
    
    if len(cognates) > 0:
        match_scores = [c['match_score'] for c in cognates]
        print(f"  - Mean match score: {safe_mean(match_scores):.3f}")
        print(f"  - These are likely 'deep thought' periods!")
    else:
        print(f"  - No matches found with tolerance={tolerance}")
        print(f"  - Try increasing tolerance or check data quality")
    
    return cognates

def calculate_thought_signature(rem_periods, cognates):
    """Calculate thought-specific metabolic signature"""
    print("\nCalculating thought signature (subtraction method)...")
    
    if len(rem_periods) == 0:
        print("⚠ Cannot calculate signature - no REM data")
        return {
            'delta_hr': np.nan,
            'delta_hrv': np.nan,
            'delta_metabolic': np.nan,
            'cognitive_intensity': np.nan,
            'rem_baseline': np.nan,
            'waking_cognitive': np.nan,
            'status': 'no_rem_data'
        }
    
    # Calculate REM baseline
    rem_hr = safe_mean([p['hr'] for p in rem_periods])
    rem_hrv = safe_mean([p['hrv'] for p in rem_periods])
    rem_met = safe_mean([p['metabolic'] for p in rem_periods])
    
    if len(cognates) == 0:
        print("⚠ No waking cognates found")
        print("  Returning REM baseline only")
        
        return {
            'delta_hr': np.nan,
            'delta_hrv': np.nan,
            'delta_metabolic': np.nan,
            'cognitive_intensity': np.nan,
            'rem_baseline': rem_met,
            'waking_cognitive': np.nan,
            'rem_hr': rem_hr,
            'rem_hrv': rem_hrv,
            'status': 'no_cognates'
        }
    
    # Calculate waking cognitive baseline
    cog_hr = safe_mean([c['hr'] for c in cognates])
    cog_hrv = safe_mean([c['hrv'] for c in cognates])
    cog_met = safe_mean([c['metabolic'] for c in cognates])
    
    # Calculate differences
    delta_hr = cog_hr - rem_hr
    delta_hrv = cog_hrv - rem_hrv
    delta_met = cog_met - rem_met
    
    # Cognitive intensity (percentage increase)
    cognitive_intensity = (delta_met / rem_met) * 100 if rem_met > 0 else 0
    
    print(f"✓ Calculated thought signature")
    print(f"  - Mean ΔHR: {delta_hr:.1f} bpm")
    print(f"  - Mean ΔHRV: {delta_hrv:.1f} ms")
    print(f"  - Mean ΔMetabolic: {delta_met:.1f}")
    print(f"  - Cognitive intensity: {cognitive_intensity:.1f}% above REM baseline")
    
    return {
        'delta_hr': delta_hr,
        'delta_hrv': delta_hrv,
        'delta_metabolic': delta_met,
        'cognitive_intensity': cognitive_intensity,
        'rem_baseline': rem_met,
        'waking_cognitive': cog_met,
        'rem_hr': rem_hr,
        'rem_hrv': rem_hrv,
        'cog_hr': cog_hr,
        'cog_hrv': cog_hrv,
        'status': 'success'
    }

def calculate_energy_costs(data, rem_periods, waking_periods, cognates):
    """Calculate metabolic costs of perception, thought, and consciousness"""
    print("\n" + "="*70)
    print("CALCULATING METABOLIC COSTS")
    print("="*70)
    
    results = {
        'perception_cost': np.nan,
        'thought_cost': np.nan,
        'consciousness_cost': np.nan,
        'baseline_cost': np.nan
    }
    
    # 1. Baseline metabolic cost (deep sleep)
    deep_sleep_hr = []
    for sleep_session in data['infrared_sleep']:
        hr_5min = sleep_session.get('hr_5min', [])
        hypnogram_5min = sleep_session.get('hypnogram_5min', [])
        
        for i, stage in enumerate(hypnogram_5min):
            if stage == 1 and i < len(hr_5min):  # Deep sleep
                if hr_5min[i] and hr_5min[i] > 0:
                    deep_sleep_hr.append(hr_5min[i])
    
    baseline_hr = safe_mean(deep_sleep_hr) if deep_sleep_hr else 55.0
    baseline_met = baseline_hr * 1.2  # Proxy metabolic rate
    results['baseline_cost'] = baseline_met
    
    print(f"\n1. Baseline (Deep Sleep):")
    print(f"   HR: {baseline_hr:.1f} bpm")
    print(f"   Metabolic: {baseline_met:.1f} units")
    
    # 2. Thought cost (REM - Baseline)
    if rem_periods:
        rem_met = safe_mean([p['metabolic'] for p in rem_periods])
        thought_cost = rem_met - baseline_met
        results['thought_cost'] = thought_cost
        
        print(f"\n2. Thought (REM - Deep Sleep):")
        print(f"   REM Metabolic: {rem_met:.1f} units")
        print(f"   Thought Cost: {thought_cost:.1f} units ({(thought_cost/baseline_met)*100:.1f}% above baseline)")
    
    # 3. Perception cost (Waking Cognate - REM)
    if cognates and rem_periods:
        cognate_met = safe_mean([c['metabolic'] for c in cognates])
        rem_met = safe_mean([p['metabolic'] for p in rem_periods])
        perception_cost = cognate_met - rem_met
        results['perception_cost'] = perception_cost
        
        print(f"\n3. Perception (Waking Cognate - REM):")
        print(f"   Waking Cognate Metabolic: {cognate_met:.1f} units")
        print(f"   Perception Cost: {perception_cost:.1f} units ({(perception_cost/rem_met)*100:.1f}% above REM)")
    
    # 4. Consciousness cost (Waking Cognate - Baseline)
    if cognates:
        cognate_met = safe_mean([c['metabolic'] for c in cognates])
        consciousness_cost = cognate_met - baseline_met
        results['consciousness_cost'] = consciousness_cost
        
        print(f"\n4. Consciousness (Waking Cognate - Deep Sleep):")
        print(f"   Consciousness Cost: {consciousness_cost:.1f} units ({(consciousness_cost/baseline_met)*100:.1f}% above baseline)")
    
    # Convert to kcal/day estimates
    # Assuming metabolic units correlate with brain energy (20W baseline = 400 kcal/day)
    if not np.isnan(results['baseline_cost']):
        scaling_factor = 400 / results['baseline_cost']  # kcal/day per metabolic unit
        
        print(f"\n" + "="*70)
        print("ESTIMATED DAILY ENERGY COSTS (kcal/day)")
        print("="*70)
        print(f"Baseline (Deep Sleep): {results['baseline_cost'] * scaling_factor:.1f} kcal/day")
        
        if not np.isnan(results['thought_cost']):
            print(f"Thought (REM dreams): {results['thought_cost'] * scaling_factor:.1f} kcal/day")
        
        if not np.isnan(results['perception_cost']):
            print(f"Perception (sensory): {results['perception_cost'] * scaling_factor:.1f} kcal/day")
        
        if not np.isnan(results['consciousness_cost']):
            print(f"Consciousness (total): {results['consciousness_cost'] * scaling_factor:.1f} kcal/day")
            print(f"\nThis represents {(results['consciousness_cost']/results['baseline_cost'])*100:.1f}% increase over baseline!")
    
    return results

def save_results_json(rem_periods, waking_periods, cognates, signature, energy_costs):
    """Save comprehensive results to JSON"""
    
    def clean_for_json(obj):
        """Convert NaN to None for JSON serialization"""
        if isinstance(obj, dict):
            return {k: clean_for_json(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [clean_for_json(item) for item in obj]
        elif isinstance(obj, float) and np.isnan(obj):
            return None
        else:
            return obj
    
    results = {
        'analysis_timestamp': datetime.now().isoformat(),
        'sample_sizes': {
            'n_rem_periods': len(rem_periods),
            'n_waking_periods': len(waking_periods),
            'n_cognates': len(cognates)
        },
        'rem_summary': {
            'mean_hr': safe_mean([p['hr'] for p in rem_periods]) if rem_periods else None,
            'mean_hrv': safe_mean([p['hrv'] for p in rem_periods]) if rem_periods else None,
            'mean_metabolic': safe_mean([p['metabolic'] for p in rem_periods]) if rem_periods else None
        },
        'waking_summary': {
            'mean_hr': safe_mean([p['hr'] for p in waking_periods]) if waking_periods else None,
            'mean_hrv': safe_mean([p['hrv'] for p in waking_periods]) if waking_periods else None,
            'mean_metabolic': safe_mean([p['metabolic'] for p in waking_periods]) if waking_periods else None
        } if waking_periods else None,
        'thought_signature': clean_for_json(signature),
        'energy_costs': clean_for_json(energy_costs)
    }
    
    with open('metabolic_mirror_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print("\n✓ Results saved to metabolic_mirror_results.json")
    return results

def main():
    """Main analysis pipeline"""
    print("="*70)
    print("METABOLIC MIRROR HYPOTHESIS: EXTRACTING THOUGHTS FROM DREAMS")
    print("="*70)
    print("\nTheoretical Foundation:")
    print("  If oscillatory coupling is continuous (no wake/sleep boundary),")
    print("  then REM (dreams) must have a waking cognate (thoughts).")
    print("  By subtracting dream baseline, we isolate conscious thought!")
    print("="*70)
    
    try:
        # Load data
        data = load_all_data()
        
        # Extract REM periods
        rem_periods = extract_rem_periods(data)
        
        # Extract waking periods
        waking_periods = extract_waking_periods(data)
        
        # Find waking REM cognates
        cognates = find_rem_cognates(rem_periods, waking_periods, tolerance=0.2)
        
        # Calculate thought signature
        signature = calculate_thought_signature(rem_periods, cognates)
        
        # Calculate energy costs
        energy_costs = calculate_energy_costs(data, rem_periods, waking_periods, cognates)
        
        # Save results
        results = save_results_json(rem_periods, waking_periods, cognates, signature, energy_costs)
        
        print("\n" + "="*70)
        print("ANALYSIS COMPLETE!")
        print("="*70)
        
        return results
        
    except Exception as e:
        print(f"\n❌ Error in analysis pipeline: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    results = main()
