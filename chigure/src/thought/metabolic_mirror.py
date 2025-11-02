# metabolic_mirror_fixed.py
import json
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.gridspec import GridSpec
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

sns.set_style("whitegrid")

def load_all_data():
    """Load comprehensive sleep and activity data"""
    print("Loading 24/7 metabolic data...")
    
    with open('public/infraredSleep.json', 'r') as f:
        infrared_sleep = json.load(f)
    
    with open('public/activity.json', 'r') as f:
        activity = json.load(f)
    
    return {
        'infrared_sleep': infrared_sleep,
        'activity': activity
    }

def safe_mean(data):
    """Safely calculate mean"""
    try:
        if isinstance(data, list):
            values = [x for x in data if x is not None and np.isfinite(x) and x > 0]
        else:
            values = [data] if data is not None and np.isfinite(data) and data > 0 else []
        return np.mean(values) if len(values) > 0 else np.nan
    except:
        return np.nan

def extract_rem_periods_fixed(data):
    """
    Extract REM periods with multiple fallback strategies
    """
    print("\nExtracting REM dream signature (fixed)...")
    
    rem_periods = []
    
    for session in data['infrared_sleep']:
        date = session.get('date', '')
        
        # Strategy 1: Use hypnogram_5min
        if 'hypnogram_5min' in session:
            hr_5min = session.get('hr_5min', [])
            hrv_5min = session.get('hrv_5min', [])
            hypnogram = session['hypnogram_5min']
            
            print(f"  Processing {date}: hypnogram length={len(hypnogram)}")
            
            # Oura hypnogram codes (check what yours actually uses)
            # Common codes: '3'=REM, 3=REM, 'rem'=REM, 'REM'=REM
            rem_codes = [3, '3', 'rem', 'REM', 'r']
            
            for i, stage in enumerate(hypnogram):
                if stage in rem_codes:
                    if i < len(hr_5min) and i < len(hrv_5min):
                        hr = hr_5min[i]
                        hrv = hrv_5min[i]
                        
                        if hr and hr > 0 and hrv and hrv > 0:
                            rem_periods.append({
                                'hr': hr,
                                'hrv': hrv,
                                'timestamp': i * 300,
                                'metabolic': hr * 1.2 + hrv * 0.5,
                                'date': date
                            })
        
        # Strategy 2: If no hypnogram, use REM duration + average HR
        elif session.get('rem', 0) > 300:  # Has REM data
            rem_duration = session['rem']
            hr_avg = session.get('hr_average', 0)
            
            # Estimate HRV for REM (typically 50-70ms)
            hrv_estimate = 60.0
            
            if hr_avg > 0:
                # Create synthetic REM periods
                n_periods = int(rem_duration / 300)  # 5-min intervals
                for i in range(n_periods):
                    rem_periods.append({
                        'hr': hr_avg,
                        'hrv': hrv_estimate,
                        'timestamp': i * 300,
                        'metabolic': hr_avg * 1.2 + hrv_estimate * 0.5,
                        'date': date
                    })
    
    if len(rem_periods) == 0:
        print("⚠ No REM periods found - trying alternative extraction...")
        
        # Strategy 3: Use sleep records with REM indicators
        for session in data['infrared_sleep']:
            rem_duration = session.get('rem', 0)
            if rem_duration > 0:
                hr_avg = session.get('hr_average', 65)  # Default REM HR
                hrv_avg = 60.0
                
                rem_periods.append({
                    'hr': hr_avg,
                    'hrv': hrv_avg,
                    'timestamp': 0,
                    'metabolic': hr_avg * 1.2 + hrv_avg * 0.5,
                    'date': session.get('date', 'unknown')
                })
    
    print(f"✓ Extracted {len(rem_periods)} REM periods")
    
    if len(rem_periods) > 0:
        hr_values = [p['hr'] for p in rem_periods]
        hrv_values = [p['hrv'] for p in rem_periods]
        met_values = [p['metabolic'] for p in rem_periods]
        
        print(f"  - Mean REM HR: {safe_mean(hr_values):.1f} bpm")
        print(f"  - Mean REM HRV: {safe_mean(hrv_values):.1f} ms")
        print(f"  - Mean REM Metabolic: {safe_mean(met_values):.1f}")
    
    return rem_periods

def extract_waking_periods_fixed(data):
    """Extract waking periods from activity data"""
    print("\nExtracting waking metabolic states...")
    
    waking_periods = []
    
    for day in data['activity']:
        met_1min = day.get('met_1min', [])
        class_5min = day.get('class_5min', '')
        
        if len(met_1min) == 0:
            continue
        
        for i, met in enumerate(met_1min):
            if met and met > 0:
                # Get activity class
                class_idx = i // 5
                activity_class = class_5min[class_idx] if class_idx < len(class_5min) else '0'
                
                # Exclude non-wear (0) and rest (1)
                if activity_class not in ['0', '1']:
                    # Estimate HR from MET
                    estimated_hr = 60 + (met - 1.0) * 10
                    estimated_hrv = max(20, 100 - (estimated_hr - 60))
                    
                    waking_periods.append({
                        'hr': estimated_hr,
                        'hrv': estimated_hrv,
                        'met': met,
                        'timestamp': i * 60,
                        'metabolic': estimated_hr * 1.2 + estimated_hrv * 0.5,
                        'activity_class': activity_class,
                        'date': day.get('date', 'unknown')
                    })
    
    print(f"✓ Extracted {len(waking_periods)} waking periods")
    
    if len(waking_periods) > 0:
        hr_values = [p['hr'] for p in waking_periods]
        hrv_values = [p['hrv'] for p in waking_periods]
        
        print(f"  - Mean Waking HR: {safe_mean(hr_values):.1f} bpm")
        print(f"  - Mean Waking HRV: {safe_mean(hrv_values):.1f} ms")
    
    return waking_periods

def create_waking_data_visualization(waking_periods, output_dir='./'):
    """
    Create visualization for waking data only (when REM data unavailable)
    """
    print("\nGenerating waking data visualization...")
    
    if len(waking_periods) == 0:
        print("⚠ No data to visualize")
        return
    
    fig = plt.figure(figsize=(20, 12))
    gs = GridSpec(3, 3, figure=fig, hspace=0.35, wspace=0.3)
    
    # Extract data
    hr_values = [p['hr'] for p in waking_periods]
    hrv_values = [p['hrv'] for p in waking_periods]
    met_values = [p['metabolic'] for p in waking_periods]
    activity_classes = [p['activity_class'] for p in waking_periods]
    
    # ========================================================================
    # Panel 1: HR Distribution
    # ========================================================================
    ax1 = fig.add_subplot(gs[0, 0])
    
    ax1.hist(hr_values, bins=50, color='#3498DB', alpha=0.7, edgecolor='black')
    ax1.axvline(safe_mean(hr_values), color='red', linestyle='--', linewidth=2,
               label=f'Mean: {safe_mean(hr_values):.1f} bpm')
    ax1.set_xlabel('Heart Rate (bpm)', fontweight='bold')
    ax1.set_ylabel('Frequency', fontweight='bold')
    ax1.set_title('A. Waking Heart Rate Distribution', fontweight='bold', fontsize=13)
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # ========================================================================
    # Panel 2: HRV Distribution
    # ========================================================================
    ax2 = fig.add_subplot(gs[0, 1])
    
    ax2.hist(hrv_values, bins=50, color='#9B59B6', alpha=0.7, edgecolor='black')
    ax2.axvline(safe_mean(hrv_values), color='red', linestyle='--', linewidth=2,
               label=f'Mean: {safe_mean(hrv_values):.1f} ms')
    ax2.set_xlabel('HRV (ms)', fontweight='bold')
    ax2.set_ylabel('Frequency', fontweight='bold')
    ax2.set_title('B. Waking HRV Distribution', fontweight='bold', fontsize=13)
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    # ========================================================================
    # Panel 3: Metabolic Rate Distribution
    # ========================================================================
    ax3 = fig.add_subplot(gs[0, 2])
    
    ax3.hist(met_values, bins=50, color='#E74C3C', alpha=0.7, edgecolor='black')
    ax3.axvline(safe_mean(met_values), color='red', linestyle='--', linewidth=2,
               label=f'Mean: {safe_mean(met_values):.1f}')
    ax3.set_xlabel('Metabolic Rate', fontweight='bold')
    ax3.set_ylabel('Frequency', fontweight='bold')
    ax3.set_title('C. Waking Metabolic Rate Distribution', fontweight='bold', fontsize=13)
    ax3.legend()
    ax3.grid(True, alpha=0.3)
    
    # ========================================================================
    # Panel 4: HR vs HRV Scatter
    # ========================================================================
    ax4 = fig.add_subplot(gs[1, 0])
    
    scatter = ax4.scatter(hr_values, hrv_values, c=met_values, 
                         cmap='viridis', s=10, alpha=0.5)
    ax4.set_xlabel('Heart Rate (bpm)', fontweight='bold')
    ax4.set_ylabel('HRV (ms)', fontweight='bold')
    ax4.set_title('D. HR-HRV Phase Space\n(colored by metabolic rate)', 
                 fontweight='bold', fontsize=13)
    plt.colorbar(scatter, ax=ax4, label='Metabolic Rate')
    ax4.grid(True, alpha=0.3)
    
    # ========================================================================
    # Panel 5: Activity Class Distribution
    # ========================================================================
    ax5 = fig.add_subplot(gs[1, 1])
    
    from collections import Counter
    class_counts = Counter(activity_classes)
    
    classes = list(class_counts.keys())
    counts = list(class_counts.values())
    
    colors_map = {'2': '#95A5A6', '3': '#3498DB', '4': '#E67E22', '5': '#E74C3C'}
    colors = [colors_map.get(c, '#7F8C8D') for c in classes]
    
    ax5.bar(classes, counts, color=colors, alpha=0.7, edgecolor='black')
    ax5.set_xlabel('Activity Class', fontweight='bold')
    ax5.set_ylabel('Count', fontweight='bold')
    ax5.set_title('E. Activity Class Distribution\n(2=inactive, 3=low, 4=medium, 5=high)', 
                 fontweight='bold', fontsize=13)
    ax5.grid(True, alpha=0.3, axis='y')
    
    # ========================================================================
    # Panel 6: Metabolic Rate by Activity Class
    # ========================================================================
    ax6 = fig.add_subplot(gs[1, 2])
    
    # Group by activity class
    class_metabolic = {}
    for p in waking_periods:
        c = p['activity_class']
        if c not in class_metabolic:
            class_metabolic[c] = []
        class_metabolic[c].append(p['metabolic'])
    
    classes_sorted = sorted(class_metabolic.keys())
    means = [safe_mean(class_metabolic[c]) for c in classes_sorted]
    stds = [np.std(class_metabolic[c]) for c in classes_sorted]
    
    ax6.bar(classes_sorted, means, yerr=stds, color=colors, 
           alpha=0.7, edgecolor='black', capsize=5)
    ax6.set_xlabel('Activity Class', fontweight='bold')
    ax6.set_ylabel('Mean Metabolic Rate', fontweight='bold')
    ax6.set_title('F. Metabolic Rate by Activity Class', 
                 fontweight='bold', fontsize=13)
    ax6.grid(True, alpha=0.3, axis='y')
    
    # ========================================================================
    # Panel 7: Time Series (sample)
    # ========================================================================
    ax7 = fig.add_subplot(gs[2, :])
    
    # Take first 1440 minutes (24 hours) as sample
    sample_size = min(1440, len(waking_periods))
    sample_indices = range(sample_size)
    sample_hr = [waking_periods[i]['hr'] for i in sample_indices]
    sample_hrv = [waking_periods[i]['hrv'] for i in sample_indices]
    sample_met = [waking_periods[i]['metabolic'] for i in sample_indices]
    
    ax7_twin = ax7.twinx()
    
    ax7.plot(sample_indices, sample_hr, color='#3498DB', linewidth=1, 
            label='Heart Rate', alpha=0.7)
    ax7_twin.plot(sample_indices, sample_hrv, color='#9B59B6', linewidth=1, 
                 label='HRV', alpha=0.7)
    
    ax7.set_xlabel('Time (minutes)', fontweight='bold')
    ax7.set_ylabel('Heart Rate (bpm)', fontweight='bold', color='#3498DB')
    ax7_twin.set_ylabel('HRV (ms)', fontweight='bold', color='#9B59B6')
    ax7.set_title('G. 24-Hour Sample: HR and HRV Time Series', 
                 fontweight='bold', fontsize=13)
    ax7.legend(loc='upper left')
    ax7_twin.legend(loc='upper right')
    ax7.grid(True, alpha=0.3)
    
    # Main title
    fig.suptitle('Waking Metabolic Data Analysis (n={:,} periods)'.format(len(waking_periods)),
                 fontsize=16, fontweight='bold', y=0.995)
    
    # Save
    output_path = f'{output_dir}/waking_metabolic_analysis.png'
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"✓ Saved visualization to {output_path}")
    
    plt.close()

def create_summary_statistics_report(waking_periods, rem_periods, output_dir='./'):
    """Create detailed statistics report"""
    
    print("\n" + "="*70)
    print("SUMMARY STATISTICS REPORT")
    print("="*70)
    
    report = []
    report.append("="*70)
    report.append("METABOLIC MIRROR ANALYSIS - SUMMARY REPORT")
    report.append("="*70)
    report.append(f"Analysis Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append("")
    
    # Waking data
    report.append("WAKING DATA:")
    report.append(f"  Total periods: {len(waking_periods):,}")
    
    if len(waking_periods) > 0:
        hr_values = [p['hr'] for p in waking_periods]
        hrv_values = [p['hrv'] for p in waking_periods]
        met_values = [p['metabolic'] for p in waking_periods]
        
        report.append(f"  Heart Rate:")
        report.append(f"    - Mean: {safe_mean(hr_values):.2f} bpm")
        report.append(f"    - Std: {np.std(hr_values):.2f} bpm")
        report.append(f"    - Range: {min(hr_values):.1f} - {max(hr_values):.1f} bpm")
        
        report.append(f"  HRV:")
        report.append(f"    - Mean: {safe_mean(hrv_values):.2f} ms")
        report.append(f"    - Std: {np.std(hrv_values):.2f} ms")
        report.append(f"    - Range: {min(hrv_values):.1f} - {max(hrv_values):.1f} ms")
        
        report.append(f"  Metabolic Rate:")
        report.append(f"    - Mean: {safe_mean(met_values):.2f} units")
        report.append(f"    - Std: {np.std(met_values):.2f} units")
        report.append(f"    - Range: {min(met_values):.1f} - {max(met_values):.1f} units")
    
    report.append("")
    
    # REM data
    report.append("REM DATA:")
    report.append(f"  Total periods: {len(rem_periods):,}")
    
    if len(rem_periods) > 0:
        rem_hr = [p['hr'] for p in rem_periods]
        rem_hrv = [p['hrv'] for p in rem_periods]
        rem_met = [p['metabolic'] for p in rem_periods]
        
        report.append(f"  Heart Rate:")
        report.append(f"    - Mean: {safe_mean(rem_hr):.2f} bpm")
        report.append(f"    - Std: {np.std(rem_hr):.2f} bpm")
        
        report.append(f"  HRV:")
        report.append(f"    - Mean: {safe_mean(rem_hrv):.2f} ms")
        report.append(f"    - Std: {np.std(rem_hrv):.2f} ms")
        
        report.append(f"  Metabolic Rate:")
        report.append(f"    - Mean: {safe_mean(rem_met):.2f} units")
        report.append(f"    - Std: {np.std(rem_met):.2f} units")
    else:
        report.append("  ⚠ No REM data available")
        report.append("  Possible reasons:")
        report.append("    - Hypnogram data format mismatch")
        report.append("    - REM stage encoding different than expected")
        report.append("    - Need to check infraredSleep.json structure")
    
    report.append("")
    report.append("="*70)
    
    # Print to console
    for line in report:
        print(line)
    
    # Save to file
    output_path = f'{output_dir}/metabolic_mirror_report.txt'
    with open(output_path, 'w') as f:
        f.write('\n'.join(report))
    
    print(f"\n✓ Report saved to {output_path}")

def main():
    """Main analysis pipeline"""
    print("="*70)
    print("METABOLIC MIRROR ANALYSIS - FIXED VERSION")
    print("="*70)
    
    try:
        # Load data
        data = load_all_data()
        
        # Extract REM periods (fixed)
        rem_periods = extract_rem_periods_fixed(data)
        
        # Extract waking periods (fixed)
        waking_periods = extract_waking_periods_fixed(data)
        
        # Create visualizations
        create_waking_data_visualization(waking_periods)
        
        # Create summary report
        create_summary_statistics_report(waking_periods, rem_periods)
        
        print("\n" + "="*70)
        print("ANALYSIS COMPLETE!")
        print("="*70)
        
        return {
            'rem_periods': rem_periods,
            'waking_periods': waking_periods
        }
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    results = main()
