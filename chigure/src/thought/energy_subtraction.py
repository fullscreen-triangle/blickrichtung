import json
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.gridspec import GridSpec
from scipy import signal, stats
from scipy.interpolate import interp1d
from datetime import datetime, timedelta
import pandas as pd
import warnings
warnings.filterwarnings('ignore')

matplotlib.use('Agg')  # Non-interactive backend
sns.set_style("whitegrid")

def load_all_data():
    """Load comprehensive sleep and activity data"""
    print("Loading metabolic decomposition data...")
    
    with open('public/infraredSleep.json', 'r') as f:
        infrared_sleep = json.load(f)
    
    with open('public/sleep_summary.json', 'r') as f:
        sleep_summary = json.load(f)
    
    with open('public/sleepRecords.json', 'r') as f:
        sleep_records = json.load(f)
    
    with open('public/activity.json', 'r') as f:
        activity = json.load(f)
    
    print(f"✓ Loaded {len(sleep_records)} sleep records")
    print(f"✓ Loaded {len(infrared_sleep)} infrared sleep sessions")
    print(f"✓ Loaded {len(activity)} activity days")
    
    return {
        'infrared_sleep': infrared_sleep,
        'sleep_summary': sleep_summary,
        'sleep_records': sleep_records,
        'activity': activity
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

def identify_dream_episodes(data):
    """
    Identify dream episodes: REM periods with metabolic measurements
    These represent pure thought metabolism
    """
    print("\nIdentifying dream episodes (pure thought metabolism)...")
    
    dream_episodes = []
    
    # Use infraredSleep for detailed time-series data
    for session in data['infrared_sleep']:
        date = session.get('date', '')
        
        # Get time series data
        hr_5min = session.get('hr_5min', [])
        hrv_5min = session.get('hrv_5min', [])
        hypnogram_5min = session.get('hypnogram_5min', [])
        
        # Get summary stats
        duration = session.get('duration', 0)
        rem_duration = session.get('rem', 0)
        deep_duration = session.get('deep', 0)
        awake_duration = session.get('awake', 0)
        
        hr_avg = session.get('hr_average', 0)
        hr_lowest = session.get('hr_lowest', 0)
        
        # Skip if insufficient REM
        if rem_duration < 300:  # Less than 5 minutes
            continue
        
        # Extract REM-specific metrics from time series
        rem_hr_values = []
        rem_hrv_values = []
        deep_hr_values = []
        
        for i, stage in enumerate(hypnogram_5min):
            if i < len(hr_5min):
                hr = hr_5min[i]
                hrv = hrv_5min[i] if i < len(hrv_5min) else None
                
                if hr and hr > 0:
                    if stage == 3:  # REM sleep
                        rem_hr_values.append(hr)
                        if hrv and hrv > 0:
                            rem_hrv_values.append(hrv)
                    elif stage == 1:  # Deep sleep
                        deep_hr_values.append(hr)
        
        # Calculate REM metabolic metrics
        if len(rem_hr_values) > 0:
            rem_hr_avg = safe_mean(rem_hr_values)
            rem_hrv_avg = safe_mean(rem_hrv_values) if rem_hrv_values else 50.0
            deep_hr_avg = safe_mean(deep_hr_values) if deep_hr_values else hr_lowest
            
            # Metabolic intensity (HR * breathing rate proxy)
            breath_rate = 17.0  # Average breathing rate
            rem_metabolic_intensity = rem_hr_avg * breath_rate
            
            # Calculate metabolic cost
            rem_duration_hrs = rem_duration / 3600
            dream_metabolic_cost = rem_metabolic_intensity * rem_duration_hrs
            
            # Wake metabolic cost (clearing/consolidation)
            wake_duration_hrs = awake_duration / 3600
            wake_metabolic_cost = rem_hr_avg * breath_rate * wake_duration_hrs * 1.2
            
            # Total thought cost
            total_thought_cost = dream_metabolic_cost + wake_metabolic_cost
            
            dream_episodes.append({
                'date': date,
                'deep_sleep_min': deep_duration / 60,
                'rem_sleep_min': rem_duration / 60,
                'awake_min': awake_duration / 60,
                'hr_avg': rem_hr_avg,
                'hr_lowest': deep_hr_avg,
                'hr_range': rem_hr_avg - deep_hr_avg,
                'hrv': rem_hrv_avg,
                'breath_avg': breath_rate,
                'metabolic_intensity': rem_metabolic_intensity,
                'dream_metabolic_cost': dream_metabolic_cost,
                'wake_metabolic_cost': wake_metabolic_cost,
                'total_thought_cost': total_thought_cost,
                'rem_percentage': (rem_duration / duration * 100) if duration > 0 else 0,
                'n_rem_periods': len(rem_hr_values)
            })
    
    print(f"✓ Identified {len(dream_episodes)} dream episodes")
    
    if len(dream_episodes) > 0:
        avg_cost = safe_mean([ep['total_thought_cost'] for ep in dream_episodes])
        avg_rem = safe_mean([ep['rem_sleep_min'] for ep in dream_episodes])
        avg_hr = safe_mean([ep['hr_avg'] for ep in dream_episodes])
        
        print(f"  - Average thought metabolic cost: {avg_cost:.2f} units")
        print(f"  - Average REM duration: {avg_rem:.1f} min")
        print(f"  - Average REM HR: {avg_hr:.1f} bpm")
    
    return dream_episodes

def extract_daytime_metabolism(data):
    """
    Extract daytime metabolic activity (thought + perception)
    """
    print("\nExtracting daytime metabolism (thought + perception)...")
    
    daytime_metabolism = []
    
    for day in data['activity']:
        date = day.get('date', '')
        
        # Get MET (Metabolic Equivalent) time series
        met_1min = day.get('met_1min', [])
        class_5min = day.get('class_5min', '')
        
        # Get summary metrics
        cal_active = day.get('cal_active', 0)
        cal_total = day.get('cal_total', 0)
        steps = day.get('steps', 0)
        average_met = day.get('average_met', 1.0)
        
        if len(met_1min) == 0:
            continue
        
        # Calculate average waking MET (exclude rest periods)
        waking_met_values = []
        for i, met in enumerate(met_1min):
            class_idx = i // 5
            activity_class = class_5min[class_idx] if class_idx < len(class_5min) else '0'
            
            # Exclude non-wear (0) and rest (1)
            if activity_class not in ['0', '1'] and met > 0:
                waking_met_values.append(met)
        
        if len(waking_met_values) == 0:
            continue
        
        avg_waking_met = safe_mean(waking_met_values)
        
        # Estimate HR from MET (empirical relationship)
        # Resting MET = 1.0 → ~60 bpm
        # Each MET unit adds ~10 bpm
        estimated_hr = 60 + (avg_waking_met - 1.0) * 10
        
        # Estimate HRV (inversely related to HR)
        estimated_hrv = max(20, 100 - (estimated_hr - 60))
        
        # Calculate metabolic rate
        breath_rate = 17.0
        base_metabolic_rate = estimated_hr * breath_rate
        
        # Activity score (proxy for perception load)
        # Higher activity = more sensory processing
        activity_score = min(1.0, steps / 10000) if steps > 0 else 0.3
        
        # Perception load (additional metabolic cost from sensory processing)
        perception_load = activity_score * base_metabolic_rate * 0.3
        
        # Total daytime metabolism
        total_metabolism = base_metabolic_rate + perception_load
        
        daytime_metabolism.append({
            'date': date,
            'hr_avg': estimated_hr,
            'hrv': estimated_hrv,
            'met_avg': avg_waking_met,
            'activity_score': activity_score,
            'steps': steps,
            'cal_active': cal_active,
            'cal_total': cal_total,
            'base_metabolic_rate': base_metabolic_rate,
            'perception_load': perception_load,
            'total_metabolism': total_metabolism,
            'n_waking_minutes': len(waking_met_values)
        })
    
    print(f"✓ Extracted {len(daytime_metabolism)} daytime periods")
    
    if len(daytime_metabolism) > 0:
        avg_total = safe_mean([d['total_metabolism'] for d in daytime_metabolism])
        avg_hr = safe_mean([d['hr_avg'] for d in daytime_metabolism])
        avg_steps = safe_mean([d['steps'] for d in daytime_metabolism])
        
        print(f"  - Average total daytime metabolism: {avg_total:.2f} units")
        print(f"  - Average daytime HR: {avg_hr:.1f} bpm")
        print(f"  - Average daily steps: {avg_steps:.0f}")
    
    return daytime_metabolism

def decompose_consciousness_metabolism(dream_episodes, daytime_metabolism):
    """
    Decompose consciousness into thought and perception components
    
    Consciousness = Thought + Perception
    
    Where:
    - Thought metabolism = measured from dream episodes (REM baseline)
    - Perception metabolism = daytime - thought baseline
    """
    print("\n" + "="*70)
    print("DECOMPOSING CONSCIOUSNESS METABOLISM")
    print("="*70)
    
    if len(dream_episodes) == 0 or len(daytime_metabolism) == 0:
        print("⚠ Insufficient data for decomposition")
        return None
    
    # Calculate average thought metabolic rate from dreams
    avg_thought_cost = safe_mean([ep['total_thought_cost'] for ep in dream_episodes])
    avg_dream_hr = safe_mean([ep['hr_avg'] for ep in dream_episodes])
    avg_rem_duration_hrs = safe_mean([ep['rem_sleep_min'] / 60 for ep in dream_episodes])
    
    # Thought metabolic rate (per hour)
    thought_metabolic_rate = avg_thought_cost / avg_rem_duration_hrs if avg_rem_duration_hrs > 0 else 0
    
    print(f"\nThought Metabolism Baseline (from dreams):")
    print(f"  - Rate: {thought_metabolic_rate:.2f} units/hour")
    print(f"  - Average dream HR: {avg_dream_hr:.1f} bpm")
    print(f"  - Average REM duration: {avg_rem_duration_hrs:.2f} hours")
    
    # Decompose each daytime period
    decomposed = []
    
    for day in daytime_metabolism:
        # Total daytime metabolism
        total = day['total_metabolism']
        
        # Estimate thought component (scale by HR ratio)
        # Assumption: thought metabolism scales with HR
        hr_ratio = day['hr_avg'] / avg_dream_hr if avg_dream_hr > 0 else 1.0
        thought_component = thought_metabolic_rate * hr_ratio
        
        # Perception component (residual)
        perception_component = total - thought_component
        
        # Ensure non-negative
        if perception_component < 0:
            perception_component = 0
            thought_component = total
        
        # Consciousness = thought + perception
        consciousness_metabolism = thought_component + perception_component
        
        # Ratios
        thought_ratio = thought_component / consciousness_metabolism if consciousness_metabolism > 0 else 0
        perception_ratio = perception_component / consciousness_metabolism if consciousness_metabolism > 0 else 0
        
        decomposed.append({
            'date': day['date'],
            'hr_avg': day['hr_avg'],
            'activity_score': day['activity_score'],
            'steps': day['steps'],
            'total_metabolism': total,
            'thought_component': thought_component,
            'perception_component': perception_component,
            'consciousness_metabolism': consciousness_metabolism,
            'thought_ratio': thought_ratio,
            'perception_ratio': perception_ratio,
            'thought_percentage': thought_ratio * 100,
            'perception_percentage': perception_ratio * 100
        })
    
    print(f"\n✓ Decomposed {len(decomposed)} periods")
    
    if len(decomposed) > 0:
        avg_thought = safe_mean([d['thought_component'] for d in decomposed])
        avg_perception = safe_mean([d['perception_component'] for d in decomposed])
        avg_consciousness = safe_mean([d['consciousness_metabolism'] for d in decomposed])
        
        thought_pct = (avg_thought / avg_consciousness * 100) if avg_consciousness > 0 else 0
        perception_pct = (avg_perception / avg_consciousness * 100) if avg_consciousness > 0 else 0
        
        print(f"\nAverage Metabolic Components:")
        print(f"  - Thought: {avg_thought:.2f} units ({thought_pct:.1f}%)")
        print(f"  - Perception: {avg_perception:.2f} units ({perception_pct:.1f}%)")
        print(f"  - Consciousness: {avg_consciousness:.2f} units (100%)")
        
        # Convert to kcal/day estimates
        # Brain baseline: ~20W = 400 kcal/day
        # Assume baseline deep sleep HR = 55 bpm → 935 metabolic units
        baseline_deep_sleep = 55 * 17  # HR * breath_rate
        scaling_factor = 400 / baseline_deep_sleep
        
        print(f"\nEstimated Daily Energy Costs (kcal/day):")
        print(f"  - Baseline (deep sleep): {baseline_deep_sleep * scaling_factor:.1f} kcal/day")
        print(f"  - Thought: {avg_thought * scaling_factor:.1f} kcal/day")
        print(f"  - Perception: {avg_perception * scaling_factor:.1f} kcal/day")
        print(f"  - Total Consciousness: {avg_consciousness * scaling_factor:.1f} kcal/day")
    
    return decomposed

def calculate_energy_costs_detailed(dream_episodes, daytime_metabolism, decomposed):
    """
    Calculate detailed energy costs for perception, thought, and consciousness
    """
    print("\n" + "="*70)
    print("DETAILED ENERGY COST ANALYSIS")
    print("="*70)
    
    results = {
        'baseline_cost': np.nan,
        'thought_cost': np.nan,
        'perception_cost': np.nan,
        'consciousness_cost': np.nan,
        'baseline_kcal_day': np.nan,
        'thought_kcal_day': np.nan,
        'perception_kcal_day': np.nan,
        'consciousness_kcal_day': np.nan
    }
    
    if not decomposed or len(decomposed) == 0:
        print("⚠ No decomposed data available")
        return results
    
    # Calculate baseline (deep sleep)
    baseline_hr = 55.0  # Typical deep sleep HR
    breath_rate = 17.0
    baseline_metabolic = baseline_hr * breath_rate
    
    # Average components from decomposition
    avg_thought = safe_mean([d['thought_component'] for d in decomposed])
    avg_perception = safe_mean([d['perception_component'] for d in decomposed])
    avg_consciousness = safe_mean([d['consciousness_metabolism'] for d in decomposed])
    
    # Metabolic costs (relative to baseline)
    thought_cost = avg_thought - baseline_metabolic
    perception_cost = avg_perception
    consciousness_cost = avg_consciousness - baseline_metabolic
    
    # Convert to kcal/day
    # Brain baseline: 400 kcal/day at rest
    scaling_factor = 400 / baseline_metabolic
    
    baseline_kcal = baseline_metabolic * scaling_factor
    thought_kcal = thought_cost * scaling_factor
    perception_kcal = perception_cost * scaling_factor
    consciousness_kcal = consciousness_cost * scaling_factor
    
    results = {
        'baseline_cost': baseline_metabolic,
        'thought_cost': thought_cost,
        'perception_cost': perception_cost,
        'consciousness_cost': consciousness_cost,
        'baseline_kcal_day': baseline_kcal,
        'thought_kcal_day': thought_kcal,
        'perception_kcal_day': perception_kcal,
        'consciousness_kcal_day': consciousness_kcal,
        'scaling_factor': scaling_factor
    }
    
    print(f"\nMetabolic Units:")
    print(f"  Baseline (deep sleep): {baseline_metabolic:.2f}")
    print(f"  Thought (above baseline): {thought_cost:.2f}")
    print(f"  Perception: {perception_cost:.2f}")
    print(f"  Consciousness (above baseline): {consciousness_cost:.2f}")
    
    print(f"\nDaily Energy Costs (kcal/day):")
    print(f"  Baseline: {baseline_kcal:.1f} kcal/day")
    print(f"  Thought: {thought_kcal:.1f} kcal/day")
    print(f"  Perception: {perception_kcal:.1f} kcal/day")
    print(f"  Total Consciousness: {consciousness_kcal:.1f} kcal/day")
    
    print(f"\nPercentage of Baseline:")
    print(f"  Thought: +{(thought_cost/baseline_metabolic)*100:.1f}%")
    print(f"  Perception: +{(perception_cost/baseline_metabolic)*100:.1f}%")
    print(f"  Consciousness: +{(consciousness_cost/baseline_metabolic)*100:.1f}%")
    
    return results

def create_consciousness_decomposition_visualization(dream_episodes, daytime_metabolism, 
                                                     decomposed, energy_costs, output_dir='./'):
    """
    Create comprehensive visualization of consciousness metabolic decomposition
    """
    print("\nGenerating consciousness decomposition visualization...")
    
    if not decomposed or len(decomposed) == 0:
        print("⚠ No data to visualize")
        return
    
    fig = plt.figure(figsize=(20, 14))
    gs = GridSpec(4, 3, figure=fig, hspace=0.4, wspace=0.35)
    
    # Colors
    color_dream = '#9B59B6'  # Purple for dreams/thought
    color_perception = '#3498DB'  # Blue for perception
    color_consciousness = '#E74C3C'  # Red for consciousness
    color_deep = '#2C3E50'  # Dark for deep sleep
    
    # ========================================================================
    # Panel 1: Dream Episode Timeline
    # ========================================================================
    ax1 = fig.add_subplot(gs[0, :])
    
    if len(dream_episodes) > 0:
        dream_indices = np.arange(len(dream_episodes))
        rem_durations = [ep['rem_sleep_min'] for ep in dream_episodes]
        deep_durations = [ep['deep_sleep_min'] for ep in dream_episodes]
        wake_durations = [ep['awake_min'] for ep in dream_episodes]
        
        # Stacked bar chart
        ax1.bar(dream_indices, deep_durations, label='Deep Sleep (Baseline)', 
                color=color_deep, alpha=0.7, edgecolor='black')
        ax1.bar(dream_indices, rem_durations, bottom=deep_durations,
                label='REM (Pure Thought)', color=color_dream, alpha=0.7, edgecolor='black')
        ax1.bar(dream_indices, wake_durations, 
                bottom=np.array(deep_durations) + np.array(rem_durations),
                label='Wake (Consolidation)', color='orange', alpha=0.7, edgecolor='black')
        
        ax1.set_xlabel('Dream Episode', fontweight='bold', fontsize=12)
        ax1.set_ylabel('Duration (minutes)', fontweight='bold', fontsize=12)
        ax1.set_title('A. Dream Episodes: Deep Sleep → REM → Wake Pattern\n(Pure Thought Metabolism Without Perception)', 
                      fontweight='bold', fontsize=14)
        ax1.legend(loc='upper right', fontsize=10)
        ax1.grid(True, alpha=0.3, axis='y')
    
    # ========================================================================
    # Panel 2: Dream Metabolic Cost Distribution
    # ========================================================================
    ax2 = fig.add_subplot(gs[1, 0])
    
    if len(dream_episodes) > 0:
        dream_costs = [ep['total_thought_cost'] for ep in dream_episodes]
        
        ax2.hist(dream_costs, bins=20, color=color_dream, alpha=0.7, edgecolor='black')
        ax2.axvline(safe_mean(dream_costs), color='red', linestyle='--', linewidth=2,
                   label=f'Mean: {safe_mean(dream_costs):.2f}')
        
        ax2.set_xlabel('Thought Metabolic Cost', fontweight='bold')
        ax2.set_ylabel('Frequency', fontweight='bold')
        ax2.set_title('B. Dream Metabolic Cost Distribution', fontweight='bold', fontsize=13)
        ax2.legend()
        ax2.grid(True, alpha=0.3)
    
    # ========================================================================
    # Panel 3: HR During Dreams vs Day
    # ========================================================================
    ax3 = fig.add_subplot(gs[1, 1])
    
    if len(dream_episodes) > 0 and len(daytime_metabolism) > 0:
        dream_hrs = [ep['hr_avg'] for ep in dream_episodes]
        day_hrs = [d['hr_avg'] for d in daytime_metabolism]
        
        ax3.hist(dream_hrs, bins=20, alpha=0.6, color=color_dream, 
                label=f'Dream HR (μ={safe_mean(dream_hrs):.1f})', edgecolor='black')
        ax3.hist(day_hrs, bins=20, alpha=0.4, color=color_perception, 
                label=f'Day HR (μ={safe_mean(day_hrs):.1f})', edgecolor='black')
        
        ax3.axvline(safe_mean(dream_hrs), color=color_dream, linestyle='--', linewidth=2)
        ax3.axvline(safe_mean(day_hrs), color=color_perception, linestyle='--', linewidth=2)
        
        ax3.set_xlabel('Heart Rate (bpm)', fontweight='bold')
        ax3.set_ylabel('Frequency', fontweight='bold')
        ax3.set_title('C. Heart Rate: Dreams vs Daytime', fontweight='bold', fontsize=13)
        ax3.legend()
        ax3.grid(True, alpha=0.3)
    
    # ========================================================================
    # Panel 4: Daytime Total Metabolism
    # ========================================================================
    ax4 = fig.add_subplot(gs[1, 2])
    
    if len(daytime_metabolism) > 0:
        total_metabolism = [d['total_metabolism'] for d in daytime_metabolism]
        
        ax4.hist(total_metabolism, bins=25, color=color_consciousness, 
                alpha=0.7, edgecolor='black')
        ax4.axvline(safe_mean(total_metabolism), color='red', linestyle='--', 
                   linewidth=2, label=f'Mean: {safe_mean(total_metabolism):.1f}')
        
        ax4.set_xlabel('Total Metabolism', fontweight='bold')
        ax4.set_ylabel('Frequency', fontweight='bold')
        ax4.set_title('D. Daytime Total Metabolism\n(Thought + Perception)', 
                     fontweight='bold', fontsize=13)
        ax4.legend()
        ax4.grid(True, alpha=0.3)
    
    # ========================================================================
    # Panel 5: Consciousness Decomposition (Stacked)
    # ========================================================================
    ax5 = fig.add_subplot(gs[2, :])
    
    if decomposed and len(decomposed) > 0:
        indices = np.arange(len(decomposed))
        thought_components = [d['thought_component'] for d in decomposed]
        perception_components = [d['perception_component'] for d in decomposed]
        
        ax5.bar(indices, thought_components, label='Thought Component', 
               color=color_dream, alpha=0.7, edgecolor='black')
        ax5.bar(indices, perception_components, bottom=thought_components,
               label='Perception Component', color=color_perception, alpha=0.7, 
               edgecolor='black')
        
        # Add total line
        consciousness_total = np.array(thought_components) + np.array(perception_components)
        ax5.plot(indices, consciousness_total, color=color_consciousness, 
                linewidth=2, marker='o', markersize=3, label='Total Consciousness')
        
        ax5.set_xlabel('Time Period', fontweight='bold', fontsize=12)
        ax5.set_ylabel('Metabolic Rate', fontweight='bold', fontsize=12)
        ax5.set_title('E. Consciousness Metabolic Decomposition: Thought + Perception = Consciousness',
                     fontweight='bold', fontsize=14)
        ax5.legend(loc='upper right', fontsize=10)
        ax5.grid(True, alpha=0.3, axis='y')
    
    # ========================================================================
    # Panel 6: Component Ratios
    # ========================================================================
    ax6 = fig.add_subplot(gs[3, 0])
    
    if decomposed and len(decomposed) > 0:
        thought_ratios = [d['thought_percentage'] for d in decomposed]
        perception_ratios = [d['perception_percentage'] for d in decomposed]
        
        scatter = ax6.scatter(thought_ratios, perception_ratios, 
                   c=range(len(decomposed)), cmap='viridis',
                   s=80, alpha=0.7, edgecolors='black', linewidth=0.5)
        
        # Add reference lines
        ax6.plot([0, 100], [100, 0], 'r--', linewidth=2, alpha=0.5, 
                label='Sum = 100%')
        
        ax6.set_xlabel('Thought %', fontweight='bold')
        ax6.set_ylabel('Perception %', fontweight='bold')
        ax6.set_title('F. Thought-Perception Ratio Space', fontweight='bold', fontsize=13)
        ax6.legend()
        ax6.grid(True, alpha=0.3)
        ax6.set_xlim(0, 100)
        ax6.set_ylim(0, 100)
        plt.colorbar(scatter, ax=ax6, label='Time')
    
    # ========================================================================
    # Panel 7: Average Component Breakdown
    # ========================================================================
    ax7 = fig.add_subplot(gs[3, 1])
    
    if decomposed and len(decomposed) > 0:
        avg_thought = safe_mean([d['thought_component'] for d in decomposed])
        avg_perception = safe_mean([d['perception_component'] for d in decomposed])
        
        components = ['Thought\n(Internal\nModel)', 'Perception\n(Sensory\nInput)']
        values = [avg_thought, avg_perception]
        colors = [color_dream, color_perception]
        
        bars = ax7.bar(components, values, color=colors, alpha=0.7, 
                      edgecolor='black', linewidth=2)
        
        # Add value labels
        for bar, val in zip(bars, values):
            height = bar.get_height()
            percentage = val / (avg_thought + avg_perception) * 100
            ax7.text(bar.get_x() + bar.get_width()/2., height,
                    f'{val:.1f}\n({percentage:.1f}%)',
                    ha='center', va='bottom', fontweight='bold', fontsize=11)
        
        ax7.set_ylabel('Average Metabolic Rate', fontweight='bold')
        ax7.set_title('G. Average Component Breakdown', fontweight='bold', fontsize=13)
        ax7.grid(True, alpha=0.3, axis='y')
        
        # Add consciousness total
        ax7.axhline(avg_thought + avg_perception, color=color_consciousness, 
                   linestyle='--', linewidth=2, label='Total Consciousness')
        ax7.legend()
    
    # ========================================================================
    # Panel 8: Summary Report
    # ========================================================================
    ax8 = fig.add_subplot(gs[3, 2])
    ax8.axis('off')
    
    if decomposed and len(decomposed) > 0 and len(dream_episodes) > 0:
        avg_thought = safe_mean([d['thought_component'] for d in decomposed])
        avg_perception = safe_mean([d['perception_component'] for d in decomposed])
        avg_consciousness = avg_thought + avg_perception
        
        thought_pct = avg_thought / avg_consciousness * 100
        perception_pct = avg_perception / avg_consciousness * 100
        
        avg_dream_cost = safe_mean([ep['total_thought_cost'] for ep in dream_episodes])
        avg_rem_duration = safe_mean([ep['rem_sleep_min'] for ep in dream_episodes])
        
        # Energy costs
        thought_kcal = energy_costs.get('thought_kcal_day', 0)
        perception_kcal = energy_costs.get('perception_kcal_day', 0)
        consciousness_kcal = energy_costs.get('consciousness_kcal_day', 0)
        
        summary_text = f"""
╔════════════════════════════════════╗
║  CONSCIOUSNESS DECOMPOSITION       ║
╚════════════════════════════════════╝

DREAM ANALYSIS (Pure Thought):
├─ Dream episodes: {len(dream_episodes)}
├─ Avg REM duration: {avg_rem_duration:.1f} min
├─ Avg metabolic cost: {avg_dream_cost:.2f}
└─ Thought baseline: {avg_thought:.2f}/hr

DAYTIME ANALYSIS (Thought + Perception):
├─ Periods analyzed: {len(decomposed)}
├─ Total metabolism: {avg_consciousness:.2f}
└─ Components:

CONSCIOUSNESS COMPONENTS:
├─ Thought (Fabrication): {avg_thought:.2f}
│   ├─ {thought_pct:.1f}% of consciousness
│   └─ {thought_kcal:.1f} kcal/day
├─ Perception (Sensory): {avg_perception:.2f}
│   ├─ {perception_pct:.1f}% of consciousness
│   └─ {perception_kcal:.1f} kcal/day
└─ Total Consciousness: {avg_consciousness:.2f}
    └─ {consciousness_kcal:.1f} kcal/day

KEY EQUATION:
  Consciousness = Thought + Perception
  
  Where:
  • Thought = Internal model fabrication
  • Perception = Sensory input processing
  • Agency = Coherent integration
  
INTERPRETATION:
  Your consciousness is ~{thought_pct:.0f}% internal
  thought and ~{perception_pct:.0f}% external
  perception. Dreams reveal the pure
  metabolic cost of thought without
  sensory input.
  
  Thought costs ~{thought_kcal:.0f} kcal/day
  Perception costs ~{perception_kcal:.0f} kcal/day
"""
        
        ax8.text(0.05, 0.95, summary_text, transform=ax8.transAxes,
                fontsize=8, verticalalignment='top', fontfamily='monospace',
                bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.3))
    
    # Main title
    fig.suptitle('Consciousness Metabolic Decomposition: Extracting Thought and Perception Components',
                 fontsize=16, fontweight='bold', y=0.995)
    
    # Save figure
    output_path = f'{output_dir}/consciousness_decomposition.png'
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"✓ Saved visualization to {output_path}")
    
    plt.close()

def save_results_json(dream_episodes, daytime_metabolism, decomposed, energy_costs, output_dir='./'):
    """Save comprehensive results to JSON"""
    
    def clean_for_json(obj):
        """Convert NaN to None for JSON serialization"""
        if isinstance(obj, dict):
            return {k: clean_for_json(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [clean_for_json(item) for item in obj]
        elif isinstance(obj, float) and np.isnan(obj):
            return None
        elif isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        else:
            return obj
    
    results = {
        'analysis_timestamp': datetime.now().isoformat(),
        'sample_sizes': {
            'n_dream_episodes': len(dream_episodes),
            'n_daytime_periods': len(daytime_metabolism),
            'n_decomposed_periods': len(decomposed) if decomposed else 0
        },
        'dream_summary': {
            'avg_rem_duration_min': safe_mean([ep['rem_sleep_min'] for ep in dream_episodes]) if dream_episodes else None,
            'avg_thought_cost': safe_mean([ep['total_thought_cost'] for ep in dream_episodes]) if dream_episodes else None,
            'avg_dream_hr': safe_mean([ep['hr_avg'] for ep in dream_episodes]) if dream_episodes else None
        },
        'daytime_summary': {
            'avg_total_metabolism': safe_mean([d['total_metabolism'] for d in daytime_metabolism]) if daytime_metabolism else None,
            'avg_hr': safe_mean([d['hr_avg'] for d in daytime_metabolism]) if daytime_metabolism else None,
            'avg_steps': safe_mean([d['steps'] for d in daytime_metabolism]) if daytime_metabolism else None
        },
        'consciousness_decomposition': {
            'avg_thought_component': safe_mean([d['thought_component'] for d in decomposed]) if decomposed else None,
            'avg_perception_component': safe_mean([d['perception_component'] for d in decomposed]) if decomposed else None,
            'avg_consciousness': safe_mean([d['consciousness_metabolism'] for d in decomposed]) if decomposed else None,
            'thought_percentage': safe_mean([d['thought_percentage'] for d in decomposed]) if decomposed else None,
            'perception_percentage': safe_mean([d['perception_percentage'] for d in decomposed]) if decomposed else None
        },
        'energy_costs': clean_for_json(energy_costs),
        'raw_data': {
            'dream_episodes': clean_for_json(dream_episodes),
            'daytime_metabolism': clean_for_json(daytime_metabolism),
            'decomposed': clean_for_json(decomposed) if decomposed else None
        }
    }
    
    output_path = f'{output_dir}/energy_subtraction_results.json'
    with open(output_path, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n✓ Results saved to {output_path}")
    return results

def main():
    """Main analysis pipeline"""
    print("="*70)
    print("CONSCIOUSNESS ENERGY DECOMPOSITION")
    print("Subtracting Dream Metabolism to Isolate Perception")
    print("="*70)
    
    try:
        # Load data
        data = load_all_data()
        
        # Identify dream episodes (pure thought)
        dream_episodes = identify_dream_episodes(data)
        
        # Extract daytime metabolism (thought + perception)
        daytime_metabolism = extract_daytime_metabolism(data)
        
        # Decompose consciousness
        decomposed = decompose_consciousness_metabolism(dream_episodes, daytime_metabolism)
        
        # Calculate detailed energy costs
        energy_costs = calculate_energy_costs_detailed(dream_episodes, daytime_metabolism, decomposed)
        
        # Create visualization
        create_consciousness_decomposition_visualization(
            dream_episodes, daytime_metabolism, decomposed, energy_costs
        )
        
        # Save results
        results = save_results_json(dream_episodes, daytime_metabolism, decomposed, energy_costs)
        
        print("\n" + "="*70)
        print("ANALYSIS COMPLETE!")
        print("="*70)
        print("\nKey Findings:")
        if decomposed and len(decomposed) > 0:
            avg_thought = safe_mean([d['thought_component'] for d in decomposed])
            avg_perception = safe_mean([d['perception_component'] for d in decomposed])
            avg_consciousness = avg_thought + avg_perception
            
            print(f"  • Thought: {avg_thought:.2f} units ({avg_thought/avg_consciousness*100:.1f}%)")
            print(f"  • Perception: {avg_perception:.2f} units ({avg_perception/avg_consciousness*100:.1f}%)")
            print(f"  • Consciousness: {avg_consciousness:.2f} units (100%)")
            
            if energy_costs:
                print(f"\n  • Thought energy: {energy_costs.get('thought_kcal_day', 0):.1f} kcal/day")
                print(f"  • Perception energy: {energy_costs.get('perception_kcal_day', 0):.1f} kcal/day")
                print(f"  • Total consciousness: {energy_costs.get('consciousness_kcal_day', 0):.1f} kcal/day")
        
        return results
        
    except Exception as e:
        print(f"\n❌ Error in analysis pipeline: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    results = main()
