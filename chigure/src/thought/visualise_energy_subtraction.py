# visualize_energy_subtraction.py
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

def load_results():
    """Load energy subtraction results"""
    with open('energy_subtraction_results.json', 'r') as f:
        results = json.load(f)
    return results

def safe_mean(data):
    """Safely calculate mean"""
    try:
        if isinstance(data, list):
            values = [x for x in data if x is not None and np.isfinite(x)]
        else:
            values = [data] if data is not None and np.isfinite(data) else []
        return np.mean(values) if len(values) > 0 else np.nan
    except:
        return np.nan

def create_daytime_metabolism_visualization(results, output_dir='./'):
    """
    Create comprehensive visualization of daytime metabolism
    """
    print("\nGenerating daytime metabolism visualization...")
    
    daytime_data = results['raw_data']['daytime_metabolism']
    
    if len(daytime_data) == 0:
        print("⚠ No daytime data to visualize")
        return
    
    fig = plt.figure(figsize=(20, 14))
    gs = GridSpec(4, 3, figure=fig, hspace=0.4, wspace=0.35)
    
    # Extract data arrays
    hr_avg = [d['hr_avg'] for d in daytime_data]
    hrv = [d['hrv'] for d in daytime_data]
    met_avg = [d['met_avg'] for d in daytime_data]
    steps = [d['steps'] for d in daytime_data]
    cal_active = [d['cal_active'] for d in daytime_data]
    cal_total = [d['cal_total'] for d in daytime_data]
    activity_score = [d['activity_score'] for d in daytime_data]
    base_metabolic = [d['base_metabolic_rate'] for d in daytime_data]
    perception_load = [d['perception_load'] for d in daytime_data]
    total_metabolism = [d['total_metabolism'] for d in daytime_data]
    
    # Colors
    color_hr = '#E74C3C'
    color_hrv = '#9B59B6'
    color_met = '#3498DB'
    color_steps = '#2ECC71'
    color_cal = '#F39C12'
    
    # ========================================================================
    # Panel 1: Heart Rate Distribution
    # ========================================================================
    ax1 = fig.add_subplot(gs[0, 0])
    
    ax1.hist(hr_avg, bins=30, color=color_hr, alpha=0.7, edgecolor='black')
    ax1.axvline(safe_mean(hr_avg), color='darkred', linestyle='--', linewidth=2,
               label=f'Mean: {safe_mean(hr_avg):.1f} bpm')
    ax1.set_xlabel('Heart Rate (bpm)', fontweight='bold', fontsize=11)
    ax1.set_ylabel('Frequency', fontweight='bold', fontsize=11)
    ax1.set_title('A. Daytime Heart Rate Distribution', fontweight='bold', fontsize=13)
    ax1.legend(fontsize=10)
    ax1.grid(True, alpha=0.3)
    
    # ========================================================================
    # Panel 2: HRV Distribution
    # ========================================================================
    ax2 = fig.add_subplot(gs[0, 1])
    
    ax2.hist(hrv, bins=30, color=color_hrv, alpha=0.7, edgecolor='black')
    ax2.axvline(safe_mean(hrv), color='darkviolet', linestyle='--', linewidth=2,
               label=f'Mean: {safe_mean(hrv):.1f} ms')
    ax2.set_xlabel('HRV (ms)', fontweight='bold', fontsize=11)
    ax2.set_ylabel('Frequency', fontweight='bold', fontsize=11)
    ax2.set_title('B. Daytime HRV Distribution', fontweight='bold', fontsize=13)
    ax2.legend(fontsize=10)
    ax2.grid(True, alpha=0.3)
    
    # ========================================================================
    # Panel 3: MET Distribution
    # ========================================================================
    ax3 = fig.add_subplot(gs[0, 2])
    
    ax3.hist(met_avg, bins=30, color=color_met, alpha=0.7, edgecolor='black')
    ax3.axvline(safe_mean(met_avg), color='darkblue', linestyle='--', linewidth=2,
               label=f'Mean: {safe_mean(met_avg):.2f} MET')
    ax3.set_xlabel('Average MET', fontweight='bold', fontsize=11)
    ax3.set_ylabel('Frequency', fontweight='bold', fontsize=11)
    ax3.set_title('C. Metabolic Equivalent (MET) Distribution', fontweight='bold', fontsize=13)
    ax3.legend(fontsize=10)
    ax3.grid(True, alpha=0.3)
    
    # ========================================================================
    # Panel 4: Steps Distribution
    # ========================================================================
    ax4 = fig.add_subplot(gs[1, 0])
    
    ax4.hist(steps, bins=30, color=color_steps, alpha=0.7, edgecolor='black')
    ax4.axvline(safe_mean(steps), color='darkgreen', linestyle='--', linewidth=2,
               label=f'Mean: {safe_mean(steps):.0f} steps')
    ax4.set_xlabel('Daily Steps', fontweight='bold', fontsize=11)
    ax4.set_ylabel('Frequency', fontweight='bold', fontsize=11)
    ax4.set_title('D. Daily Step Count Distribution', fontweight='bold', fontsize=13)
    ax4.legend(fontsize=10)
    ax4.grid(True, alpha=0.3)
    
    # ========================================================================
    # Panel 5: Active Calories Distribution
    # ========================================================================
    ax5 = fig.add_subplot(gs[1, 1])
    
    ax5.hist(cal_active, bins=30, color=color_cal, alpha=0.7, edgecolor='black')
    ax5.axvline(safe_mean(cal_active), color='darkorange', linestyle='--', linewidth=2,
               label=f'Mean: {safe_mean(cal_active):.0f} kcal')
    ax5.set_xlabel('Active Calories (kcal)', fontweight='bold', fontsize=11)
    ax5.set_ylabel('Frequency', fontweight='bold', fontsize=11)
    ax5.set_title('E. Active Calorie Expenditure', fontweight='bold', fontsize=13)
    ax5.legend(fontsize=10)
    ax5.grid(True, alpha=0.3)
    
    # ========================================================================
    # Panel 6: Total Metabolism Distribution
    # ========================================================================
    ax6 = fig.add_subplot(gs[1, 2])
    
    ax6.hist(total_metabolism, bins=30, color='#34495E', alpha=0.7, edgecolor='black')
    ax6.axvline(safe_mean(total_metabolism), color='red', linestyle='--', linewidth=2,
               label=f'Mean: {safe_mean(total_metabolism):.1f}')
    ax6.set_xlabel('Total Metabolism', fontweight='bold', fontsize=11)
    ax6.set_ylabel('Frequency', fontweight='bold', fontsize=11)
    ax6.set_title('F. Total Metabolic Rate Distribution', fontweight='bold', fontsize=13)
    ax6.legend(fontsize=10)
    ax6.grid(True, alpha=0.3)
    
    # ========================================================================
    # Panel 7: HR vs HRV Scatter (colored by activity)
    # ========================================================================
    ax7 = fig.add_subplot(gs[2, 0])
    
    scatter = ax7.scatter(hr_avg, hrv, c=activity_score, cmap='viridis',
                         s=100, alpha=0.7, edgecolors='black', linewidth=0.5)
    ax7.set_xlabel('Heart Rate (bpm)', fontweight='bold', fontsize=11)
    ax7.set_ylabel('HRV (ms)', fontweight='bold', fontsize=11)
    ax7.set_title('G. HR-HRV Phase Space\n(colored by activity score)', 
                 fontweight='bold', fontsize=13)
    cbar = plt.colorbar(scatter, ax=ax7)
    cbar.set_label('Activity Score', fontweight='bold')
    ax7.grid(True, alpha=0.3)
    
    # ========================================================================
    # Panel 8: Steps vs Metabolism
    # ========================================================================
    ax8 = fig.add_subplot(gs[2, 1])
    
    scatter2 = ax8.scatter(steps, total_metabolism, c=hr_avg, cmap='coolwarm',
                          s=100, alpha=0.7, edgecolors='black', linewidth=0.5)
    ax8.set_xlabel('Daily Steps', fontweight='bold', fontsize=11)
    ax8.set_ylabel('Total Metabolism', fontweight='bold', fontsize=11)
    ax8.set_title('H. Steps vs Metabolic Rate\n(colored by HR)', 
                 fontweight='bold', fontsize=13)
    cbar2 = plt.colorbar(scatter2, ax=ax8)
    cbar2.set_label('HR (bpm)', fontweight='bold')
    ax8.grid(True, alpha=0.3)
    
    # ========================================================================
    # Panel 9: Metabolic Components Breakdown
    # ========================================================================
    ax9 = fig.add_subplot(gs[2, 2])
    
    avg_base = safe_mean(base_metabolic)
    avg_perception = safe_mean(perception_load)
    
    components = ['Base\nMetabolism', 'Perception\nLoad']
    values = [avg_base, avg_perception]
    colors = ['#3498DB', '#E74C3C']
    
    bars = ax9.bar(components, values, color=colors, alpha=0.7, 
                   edgecolor='black', linewidth=2)
    
    # Add value labels
    for bar, val in zip(bars, values):
        height = bar.get_height()
        percentage = val / (avg_base + avg_perception) * 100
        ax9.text(bar.get_x() + bar.get_width()/2., height,
                f'{val:.1f}\n({percentage:.1f}%)',
                ha='center', va='bottom', fontweight='bold', fontsize=11)
    
    ax9.set_ylabel('Metabolic Rate', fontweight='bold', fontsize=11)
    ax9.set_title('I. Average Metabolic Components', fontweight='bold', fontsize=13)
    ax9.grid(True, alpha=0.3, axis='y')
    
    # ========================================================================
    # Panel 10: Time Series - HR and Steps
    # ========================================================================
    ax10 = fig.add_subplot(gs[3, :2])
    
    days = np.arange(len(hr_avg))
    
    ax10_twin = ax10.twinx()
    
    line1 = ax10.plot(days, hr_avg, color=color_hr, linewidth=2, 
                     marker='o', markersize=4, label='Heart Rate', alpha=0.8)
    line2 = ax10_twin.plot(days, steps, color=color_steps, linewidth=2, 
                          marker='s', markersize=4, label='Steps', alpha=0.8)
    
    ax10.set_xlabel('Day', fontweight='bold', fontsize=11)
    ax10.set_ylabel('Heart Rate (bpm)', fontweight='bold', fontsize=11, color=color_hr)
    ax10_twin.set_ylabel('Steps', fontweight='bold', fontsize=11, color=color_steps)
    ax10.set_title('J. Time Series: Heart Rate and Daily Steps', fontweight='bold', fontsize=13)
    
    ax10.tick_params(axis='y', labelcolor=color_hr)
    ax10_twin.tick_params(axis='y', labelcolor=color_steps)
    
    # Combine legends
    lines = line1 + line2
    labels = [l.get_label() for l in lines]
    ax10.legend(lines, labels, loc='upper left', fontsize=10)
    
    ax10.grid(True, alpha=0.3)
    
    # ========================================================================
    # Panel 11: Summary Statistics Box
    # ========================================================================
    ax11 = fig.add_subplot(gs[3, 2])
    ax11.axis('off')
    
    summary_text = f"""
╔═══════════════════════════════════╗
║   DAYTIME METABOLISM SUMMARY      ║
╚═══════════════════════════════════╝

SAMPLE SIZE:
  • Days analyzed: {len(daytime_data)}
  • Total data points: {sum([d['n_waking_minutes'] for d in daytime_data]):,} min

CARDIOVASCULAR:
  • Mean HR: {safe_mean(hr_avg):.1f} bpm
  • HR range: {min(hr_avg):.1f} - {max(hr_avg):.1f}
  • Mean HRV: {safe_mean(hrv):.1f} ms
  • HRV range: {min(hrv):.1f} - {max(hrv):.1f}

ACTIVITY:
  • Mean steps: {safe_mean(steps):.0f} /day
  • Mean MET: {safe_mean(met_avg):.2f}
  • Mean activity score: {safe_mean(activity_score):.2f}

ENERGY:
  • Mean active cal: {safe_mean(cal_active):.0f} kcal
  • Mean total cal: {safe_mean(cal_total):.0f} kcal

METABOLISM:
  • Base rate: {safe_mean(base_metabolic):.1f}
  • Perception load: {safe_mean(perception_load):.1f}
  • Total: {safe_mean(total_metabolism):.1f}
  
  Perception = {safe_mean(perception_load)/safe_mean(total_metabolism)*100:.1f}% of total

⚠ NOTE: Dream data not available
   Cannot decompose thought component
   Need REM sleep data for full analysis
"""
    
    ax11.text(0.05, 0.95, summary_text, transform=ax11.transAxes,
             fontsize=9, verticalalignment='top', fontfamily='monospace',
             bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.3))
    
    # Main title
    fig.suptitle('Daytime Metabolism Analysis: Activity, Heart Rate, and Energy Expenditure',
                 fontsize=16, fontweight='bold', y=0.998)
    
    # Save
    output_path = f'{output_dir}/daytime_metabolism_visualization.png'
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"✓ Saved to {output_path}")
    
    plt.close()

def create_activity_correlation_heatmap(results, output_dir='./'):
    """
    Create correlation heatmap of all metabolic variables
    """
    print("\nGenerating correlation heatmap...")
    
    daytime_data = results['raw_data']['daytime_metabolism']
    
    if len(daytime_data) == 0:
        return
    
    # Create DataFrame
    import pandas as pd
    
    df = pd.DataFrame({
        'HR': [d['hr_avg'] for d in daytime_data],
        'HRV': [d['hrv'] for d in daytime_data],
        'MET': [d['met_avg'] for d in daytime_data],
        'Steps': [d['steps'] for d in daytime_data],
        'Active Cal': [d['cal_active'] for d in daytime_data],
        'Total Cal': [d['cal_total'] for d in daytime_data],
        'Activity Score': [d['activity_score'] for d in daytime_data],
        'Base Metabolism': [d['base_metabolic_rate'] for d in daytime_data],
        'Perception Load': [d['perception_load'] for d in daytime_data],
        'Total Metabolism': [d['total_metabolism'] for d in daytime_data]
    })
    
    # Calculate correlations
    corr = df.corr()
    
    # Create figure
    fig, ax = plt.subplots(figsize=(12, 10))
    
    # Create heatmap
    sns.heatmap(corr, annot=True, fmt='.2f', cmap='coolwarm', center=0,
                square=True, linewidths=1, cbar_kws={"shrink": 0.8},
                ax=ax, vmin=-1, vmax=1)
    
    ax.set_title('Metabolic Variables Correlation Matrix', 
                fontweight='bold', fontsize=14, pad=20)
    
    plt.tight_layout()
    
    output_path = f'{output_dir}/metabolic_correlations.png'
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"✓ Saved to {output_path}")
    
    plt.close()

def create_activity_intensity_breakdown(results, output_dir='./'):
    """
    Create breakdown by activity intensity levels
    """
    print("\nGenerating activity intensity breakdown...")
    
    daytime_data = results['raw_data']['daytime_metabolism']
    
    if len(daytime_data) == 0:
        return
    
    # Categorize by activity score
    low_activity = [d for d in daytime_data if d['activity_score'] < 0.3]
    medium_activity = [d for d in daytime_data if 0.3 <= d['activity_score'] < 0.7]
    high_activity = [d for d in daytime_data if d['activity_score'] >= 0.7]
    
    fig, axes = plt.subplots(2, 3, figsize=(18, 10))
    
    categories = [
        ('Low Activity\n(score < 0.3)', low_activity, '#95A5A6'),
        ('Medium Activity\n(0.3 ≤ score < 0.7)', medium_activity, '#3498DB'),
        ('High Activity\n(score ≥ 0.7)', high_activity, '#E74C3C')
    ]
    
    metrics = [
        ('HR (bpm)', 'hr_avg'),
        ('HRV (ms)', 'hrv'),
        ('MET', 'met_avg'),
        ('Steps', 'steps'),
        ('Active Cal', 'cal_active'),
        ('Total Metabolism', 'total_metabolism')
    ]
    
    for idx, (metric_name, metric_key) in enumerate(metrics):
        ax = axes[idx // 3, idx % 3]
        
        data_to_plot = []
        labels = []
        colors = []
        
        for cat_name, cat_data, color in categories:
            if len(cat_data) > 0:
                values = [d[metric_key] for d in cat_data]
                data_to_plot.append(values)
                labels.append(f"{cat_name}\n(n={len(cat_data)})")
                colors.append(color)
        
        if len(data_to_plot) > 0:
            bp = ax.boxplot(data_to_plot, labels=labels, patch_artist=True,
                           showmeans=True, meanline=True)
            
            for patch, color in zip(bp['boxes'], colors):
                patch.set_facecolor(color)
                patch.set_alpha(0.7)
            
            ax.set_ylabel(metric_name, fontweight='bold')
            ax.set_title(f'{metric_name} by Activity Level', fontweight='bold')
            ax.grid(True, alpha=0.3, axis='y')
    
    plt.suptitle('Metabolic Metrics by Activity Intensity', 
                fontsize=16, fontweight='bold', y=0.995)
    plt.tight_layout()
    
    output_path = f'{output_dir}/activity_intensity_breakdown.png'
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"✓ Saved to {output_path}")
    
    plt.close()

def create_energy_expenditure_analysis(results, output_dir='./'):
    """
    Create detailed energy expenditure analysis
    """
    print("\nGenerating energy expenditure analysis...")
    
    daytime_data = results['raw_data']['daytime_metabolism']
    
    if len(daytime_data) == 0:
        return
    
    fig = plt.figure(figsize=(16, 10))
    gs = GridSpec(2, 2, figure=fig, hspace=0.3, wspace=0.3)
    
    # Extract data
    cal_active = np.array([d['cal_active'] for d in daytime_data])
    cal_total = np.array([d['cal_total'] for d in daytime_data])
    steps = np.array([d['steps'] for d in daytime_data])
    met_avg = np.array([d['met_avg'] for d in daytime_data])
    
    # ========================================================================
    # Panel 1: Active vs Total Calories
    # ========================================================================
    ax1 = fig.add_subplot(gs[0, 0])
    
    ax1.scatter(cal_total, cal_active, s=100, alpha=0.6, 
               c=steps, cmap='viridis', edgecolors='black', linewidth=0.5)
    
    # Add regression line
    z = np.polyfit(cal_total, cal_active, 1)
    p = np.poly1d(z)
    ax1.plot(cal_total, p(cal_total), "r--", linewidth=2, alpha=0.8,
            label=f'y = {z[0]:.2f}x + {z[1]:.0f}')
    
    ax1.set_xlabel('Total Calories (kcal)', fontweight='bold', fontsize=11)
    ax1.set_ylabel('Active Calories (kcal)', fontweight='bold', fontsize=11)
    ax1.set_title('Active vs Total Calorie Expenditure', fontweight='bold', fontsize=13)
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # ========================================================================
    # Panel 2: Steps vs Active Calories
    # ========================================================================
    ax2 = fig.add_subplot(gs[0, 1])
    
    ax2.scatter(steps, cal_active, s=100, alpha=0.6,
               c=met_avg, cmap='plasma', edgecolors='black', linewidth=0.5)
    
    # Add regression line
    z2 = np.polyfit(steps, cal_active, 1)
    p2 = np.poly1d(z2)
    ax2.plot(steps, p2(steps), "r--", linewidth=2, alpha=0.8,
            label=f'y = {z2[0]:.3f}x + {z2[1]:.0f}')
    
    ax2.set_xlabel('Daily Steps', fontweight='bold', fontsize=11)
    ax2.set_ylabel('Active Calories (kcal)', fontweight='bold', fontsize=11)
    ax2.set_title('Steps vs Active Calorie Expenditure', fontweight='bold', fontsize=13)
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    # ========================================================================
    # Panel 3: Calorie Efficiency (cal/step)
    # ========================================================================
    ax3 = fig.add_subplot(gs[1, 0])
    
    cal_per_step = cal_active / (steps + 1)  # Avoid division by zero
    
    ax3.hist(cal_per_step, bins=30, color='#E67E22', alpha=0.7, edgecolor='black')
    ax3.axvline(safe_mean(cal_per_step), color='red', linestyle='--', linewidth=2,
               label=f'Mean: {safe_mean(cal_per_step):.3f} kcal/step')
    
    ax3.set_xlabel('Calories per Step (kcal/step)', fontweight='bold', fontsize=11)
    ax3.set_ylabel('Frequency', fontweight='bold', fontsize=11)
    ax3.set_title('Caloric Efficiency Distribution', fontweight='bold', fontsize=13)
    ax3.legend()
    ax3.grid(True, alpha=0.3)
    
    # ========================================================================
    # Panel 4: Summary Statistics
    # ========================================================================
    ax4 = fig.add_subplot(gs[1, 1])
    ax4.axis('off')
    
    # Calculate statistics
    total_days = len(daytime_data)
    total_steps = sum(steps)
    total_active_cal = sum(cal_active)
    total_cal = sum(cal_total)
    avg_cal_per_step = safe_mean(cal_per_step)
    
    # Correlation
    corr_steps_cal = np.corrcoef(steps, cal_active)[0, 1]
    corr_total_active = np.corrcoef(cal_total, cal_active)[0, 1]
    
    summary_text = f"""
╔════════════════════════════════════════╗
║   ENERGY EXPENDITURE SUMMARY           ║
╚════════════════════════════════════════╝

TOTALS (over {total_days} days):
  • Total steps: {total_steps:,}
  • Total active cal: {total_active_cal:,.0f} kcal
  • Total calories: {total_cal:,.0f} kcal

DAILY AVERAGES:
  • Steps: {safe_mean(steps):.0f} /day
  • Active cal: {safe_mean(cal_active):.0f} kcal/day
  • Total cal: {safe_mean(cal_total):.0f} kcal/day
  • MET: {safe_mean(met_avg):.2f}

EFFICIENCY:
  • Avg cal/step: {avg_cal_per_step:.3f} kcal/step
  • Active/Total ratio: {safe_mean(cal_active)/safe_mean(cal_total):.2%}

CORRELATIONS:
  • Steps ↔ Active cal: {corr_steps_cal:.3f}
  • Total ↔ Active cal: {corr_total_active:.3f}

INTERPRETATION:
  • Higher correlation indicates consistent
    energy expenditure patterns
  • Avg {avg_cal_per_step*1000:.1f} cal per 1000 steps
  • Active calories represent
    {safe_mean(cal_active)/safe_mean(cal_total)*100:.1f}% of total expenditure
"""
    
    ax4.text(0.05, 0.95, summary_text, transform=ax4.transAxes,
            fontsize=10, verticalalignment='top', fontfamily='monospace',
            bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.3))
    
    plt.suptitle('Energy Expenditure Analysis: Calories, Steps, and Efficiency',
                fontsize=16, fontweight='bold', y=0.995)
    
    output_path = f'{output_dir}/energy_expenditure_analysis.png'
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"✓ Saved to {output_path}")
    
    plt.close()

def main():
    """Main visualization pipeline"""
    print("="*70)
    print("ENERGY SUBTRACTION RESULTS VISUALIZATION")
    print("="*70)
    
    try:
        # Load results
        results = load_results()
        
        print(f"\nLoaded results:")
        print(f"  • Dream episodes: {results['sample_sizes']['n_dream_episodes']}")
        print(f"  • Daytime periods: {results['sample_sizes']['n_daytime_periods']}")
        print(f"  • Decomposed periods: {results['sample_sizes']['n_decomposed_periods']}")
        
        # Create visualizations
        create_daytime_metabolism_visualization(results)
        create_activity_correlation_heatmap(results)
        create_activity_intensity_breakdown(results)
        create_energy_expenditure_analysis(results)
        
        print("\n" + "="*70)
        print("VISUALIZATION COMPLETE!")
        print("="*70)
        print("\nGenerated files:")
        print("  1. daytime_metabolism_visualization.png")
        print("  2. metabolic_correlations.png")
        print("  3. activity_intensity_breakdown.png")
        print("  4. energy_expenditure_analysis.png")
        
        print("\n⚠ NOTE: Dream data not available")
        print("  Cannot create consciousness decomposition charts")
        print("  Need to fix REM detection in infraredSleep.json")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
