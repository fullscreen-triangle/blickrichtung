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

def load_all_data():
    """Load comprehensive sleep and activity data"""
    print("Loading metabolic decomposition data...")
    
    with open('public/infraredSleep.json', 'r') as f:
        infrared_sleep = json.load(f)
    
    with open('public/sleep_summary.json', 'r') as f:
        sleep_summary = json.load(f)
    
    with open('public/sleepRecords.json', 'r') as f:
        sleep_records = json.load(f)
    
    with open('public/actigram.json', 'r') as f:
        actigram = json.load(f)
    
    with open('public/activity.json', 'r') as f:
        activity = json.load(f)
    
    with open('public/activityPPG.json', 'r') as f:
        activity_ppg = json.load(f)
    
    print(f"✓ Loaded {len(sleep_records)} sleep records")
    print(f"✓ Loaded {len(actigram)} actigram points")
    print(f"✓ Loaded {len(activity)} activity days")
    
    return {
        'infrared_sleep': infrared_sleep,
        'sleep_summary': sleep_summary,
        'sleep_records': sleep_records,
        'actigram': actigram,
        'activity': activity,
        'activity_ppg': activity_ppg
    }

def identify_dream_episodes(data):
    """
    Identify dream episodes: REM periods after deep sleep followed by wakefulness
    These represent pure thought metabolism
    """
    print("\nIdentifying dream episodes (pure thought metabolism)...")
    
    dream_episodes = []
    
    for record in data['sleep_records']:
        date = record.get('date', '')
        
        # Extract sleep stages (in seconds)
        deep_sleep = record.get('deep', 0)
        rem_sleep = record.get('rem', 0)
        awake = record.get('awake', 0)
        light_sleep = record.get('light', 0)
        total_duration = record.get('duration', 0)
        
        # Get physiological metrics
        hr_avg = record.get('hr_average', 0)
        hr_min = record.get('hr_lowest', 0)
        hr_max = record.get('hr_5min_high', 0)
        hrv = record.get('rmssd', 0)
        breath_avg = record.get('breath_average', 0)
        
        # Calculate metabolic intensity
        if hr_avg and breath_avg:
            metabolic_intensity = hr_avg * breath_avg
        else:
            metabolic_intensity = hr_avg * 17  # Default breath rate
        
        # Criteria for dream episode:
        # 1. Has significant REM (> 5 minutes)
        # 2. Has preceding deep sleep (> 10 minutes)
        # 3. Has some wakefulness after (metabolic cost indicator)
        if rem_sleep > 300 and deep_sleep > 600 and awake > 60:
            # Calculate REM metabolic cost
            rem_percentage = rem_sleep / total_duration if total_duration > 0 else 0
            
            # Metabolic cost = intensity * duration * efficiency factor
            dream_metabolic_cost = metabolic_intensity * (rem_sleep / 3600) * rem_percentage
            
            # Wake metabolic cost (clearing cost)
            wake_metabolic_cost = metabolic_intensity * (awake / 3600) * 1.2  # Higher rate during wake
            
            dream_episodes.append({
                'date': date,
                'deep_sleep_min': deep_sleep / 60,
                'rem_sleep_min': rem_sleep / 60,
                'awake_min': awake / 60,
                'hr_avg': hr_avg,
                'hr_range': hr_max - hr_min,
                'hrv': hrv,
                'breath_avg': breath_avg,
                'metabolic_intensity': metabolic_intensity,
                'dream_metabolic_cost': dream_metabolic_cost,
                'wake_metabolic_cost': wake_metabolic_cost,
                'total_thought_cost': dream_metabolic_cost + wake_metabolic_cost,
                'rem_percentage': rem_percentage * 100
            })
    
    print(f"✓ Identified {len(dream_episodes)} dream episodes")
    
    if len(dream_episodes) > 0:
        avg_cost = np.mean([ep['total_thought_cost'] for ep in dream_episodes])
        print(f"  - Average thought metabolic cost: {avg_cost:.2f}")
        print(f"  - Average REM duration: {np.mean([ep['rem_sleep_min'] for ep in dream_episodes]):.1f} min")
    
    return dream_episodes

def extract_daytime_metabolism(data):
    """
    Extract daytime metabolic activity (thought + perception)
    """
    print("\nExtracting daytime metabolism (thought + perception)...")
    
    daytime_metabolism = []
    
    for record in data['activity_ppg']:
        date = record.get('date', '')
        
        # Get physiological metrics
        hr_avg = record.get('average_heart_rate', 0)
        hr_max = record.get('max_heart_rate', 0)
        hr_min = record.get('min_heart_rate', 0)
        hrv = record.get('hrv', 0)
        
        # Activity score (proxy for perception load)
        activity_score = record.get('score', 50) / 100.0
        
        if hr_avg > 0:
            # Estimate metabolic rate
            # Higher activity = more perception
            # Base metabolism includes both thought and perception
            base_metabolic_rate = hr_avg * 17  # Assuming 17 breaths/min
            
            # Activity modulation (perception load)
            perception_load = activity_score * base_metabolic_rate * 0.3
            
            # Total daytime metabolism
            total_daytime = base_metabolic_rate + perception_load
            
            daytime_metabolism.append({
                'date': date,
                'hr_avg': hr_avg,
                'hr_range': hr_max - hr_min,
                'hrv': hrv,
                'activity_score': activity_score,
                'base_metabolic_rate': base_metabolic_rate,
                'perception_load': perception_load,
                'total_metabolism': total_daytime
            })
    
    print(f"✓ Extracted {len(daytime_metabolism)} daytime periods")
    
    if len(daytime_metabolism) > 0:
        avg_total = np.mean([d['total_metabolism'] for d in daytime_metabolism])
        print(f"  - Average total daytime metabolism: {avg_total:.2f}")
    
    return daytime_metabolism

def decompose_consciousness_metabolism(dream_episodes, daytime_metabolism):
    """
    Decompose consciousness into thought and perception components
    
    Consciousness = Thought + Perception
    
    Where:
    - Thought metabolism = measured from dream episodes
    - Perception metabolism = daytime - thought baseline
    """
    print("\nDecomposing consciousness metabolism...")
    
    if len(dream_episodes) == 0 or len(daytime_metabolism) == 0:
        print("⚠ Insufficient data for decomposition")
        return None
    
    # Calculate average thought metabolic rate from dreams
    avg_thought_cost = np.mean([ep['total_thought_cost'] for ep in dream_episodes])
    avg_dream_hr = np.mean([ep['hr_avg'] for ep in dream_episodes])
    
    # Normalize to per-hour rate
    avg_rem_duration_hrs = np.mean([ep['rem_sleep_min'] / 60 for ep in dream_episodes])
    thought_metabolic_rate = avg_thought_cost / avg_rem_duration_hrs if avg_rem_duration_hrs > 0 else 0
    
    print(f"\nThought Metabolism Baseline:")
    print(f"  - Rate: {thought_metabolic_rate:.2f} units/hour")
    print(f"  - Average dream HR: {avg_dream_hr:.1f} bpm")
    
    # Decompose each daytime period
    decomposed = []
    
    for day in daytime_metabolism:
        # Total daytime metabolism
        total = day['total_metabolism']
        
        # Estimate thought component (scale by HR ratio)
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
            'total_metabolism': total,
            'thought_component': thought_component,
            'perception_component': perception_component,
            'consciousness_metabolism': consciousness_metabolism,
            'thought_ratio': thought_ratio,
            'perception_ratio': perception_ratio
        })
    
    print(f"\n✓ Decomposed {len(decomposed)} periods")
    
    if len(decomposed) > 0:
        avg_thought = np.mean([d['thought_component'] for d in decomposed])
        avg_perception = np.mean([d['perception_component'] for d in decomposed])
        avg_consciousness = np.mean([d['consciousness_metabolism'] for d in decomposed])
        
        print(f"\nAverage Components:")
        print(f"  - Thought: {avg_thought:.2f} ({avg_thought/avg_consciousness*100:.1f}%)")
        print(f"  - Perception: {avg_perception:.2f} ({avg_perception/avg_consciousness*100:.1f}%)")
        print(f"  - Consciousness: {avg_consciousness:.2f}")
    
    return decomposed

def create_consciousness_decomposition_visualization(dream_episodes, daytime_metabolism, 
                                                     decomposed, output_dir='./'):
    """
    Create comprehensive visualization of consciousness metabolic decomposition
    """
    print("\nGenerating consciousness decomposition visualization...")
    
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
        ax1.bar(dream_indices, deep_durations, label='Deep Sleep (Clearing)', 
                color=color_deep, alpha=0.7, edgecolor='black')
        ax1.bar(dream_indices, rem_durations, bottom=deep_durations,
                label='REM (Dream/Thought)', color=color_dream, alpha=0.7, edgecolor='black')
        ax1.bar(dream_indices, wake_durations, 
                bottom=np.array(deep_durations) + np.array(rem_durations),
                label='Wake (Metabolic Cost)', color='orange', alpha=0.7, edgecolor='black')
        
        ax1.set_xlabel('Dream Episode', fontweight='bold', fontsize=12)
        ax1.set_ylabel('Duration (minutes)', fontweight='bold', fontsize=12)
        ax1.set_title('A. Dream Episodes: Deep Sleep → REM → Wake Pattern\n(Pure Thought Metabolism)', 
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
        ax2.axvline(np.mean(dream_costs), color='red', linestyle='--', linewidth=2,
                   label=f'Mean: {np.mean(dream_costs):.2f}')
        
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
                label='Dream HR', edgecolor='black')
        ax3.hist(day_hrs, bins=20, alpha=0.4, color=color_perception, 
                label='Day HR', edgecolor='black')
        
        ax3.axvline(np.mean(dream_hrs), color=color_dream, linestyle='--', linewidth=2)
        ax3.axvline(np.mean(day_hrs), color=color_perception, linestyle='--', linewidth=2)
        
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
        ax4.axvline(np.mean(total_metabolism), color='red', linestyle='--', 
                   linewidth=2, label=f'Mean: {np.mean(total_metabolism):.1f}')
        
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
        thought_ratios = [d['thought_ratio'] * 100 for d in decomposed]
        perception_ratios = [d['perception_ratio'] * 100 for d in decomposed]
        
        ax6.scatter(thought_ratios, perception_ratios, 
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
    
    # ========================================================================
    # Panel 7: Average Component Breakdown
    # ========================================================================
    ax7 = fig.add_subplot(gs[3, 1])
    
    if decomposed and len(decomposed) > 0:
        avg_thought = np.mean([d['thought_component'] for d in decomposed])
        avg_perception = np.mean([d['perception_component'] for d in decomposed])
        
        components = ['Thought\n(Fabricated\nReality)', 'Perception\n(Sensory\nInput)']
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
        avg_thought = np.mean([d['thought_component'] for d in decomposed])
        avg_perception = np.mean([d['perception_component'] for d in decomposed])
        avg_consciousness = avg_thought + avg_perception
        
        thought_pct = avg_thought / avg_consciousness * 100
        perception_pct = avg_perception / avg_consciousness * 100
        
        avg_dream_cost = np.mean([ep['total_thought_cost'] for ep in dream_episodes])
        avg_rem_duration = np.mean([ep['rem_sleep_min'] for ep in dream_episodes])
        
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
│   └─ {thought_pct:.1f}% of consciousness
├─ Perception (Sensory): {avg_perception:.2f}
│   └─ {perception_pct:.1f}% of consciousness
└─ Total Consciousness: {avg_consciousness:.2f}

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
"""
        
        ax8.text(0.05, 0.95, summary_text, transform=ax8.transAxes,
                fontsize=8, verticalalignment='top', fontfamily='monospace',
                bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.9))
    
    fig.suptitle('METABOLIC DECOMPOSITION OF CONSCIOUSNESS\n' +
                 'Thought (Dreams) + Perception (Sensory) = Consciousness (Agency)',
                 fontsize=16, fontweight='bold', y=0.99)
    
    output_path = f'{output_dir}/consciousness_metabolic_decomposition.png'
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"✓ Saved: {output_path}")
    plt.close()

def create_metabolic_flow_diagram(dream_episodes, decomposed, output_dir='./'):
    """
    Create Sankey-style flow diagram showing metabolic pathways
    """
    print("\nGenerating metabolic flow diagram...")
    
    fig, ax = plt.subplots(figsize=(16, 10))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')
    
    color_dream = '#9B59B6'
    color_perception = '#3498DB'
    color_consciousness = '#E74C3C'
    
    # Draw boxes
    from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
    
    # Night pathway
    box1 = FancyBboxPatch((0.5, 7), 1.5, 1.5, boxstyle="round,pad=0.1",
                          facecolor=color_dream, edgecolor='black', linewidth=3, alpha=0.7)
    ax.add_patch(box1)
    ax.text(1.25, 7.75, 'REM Sleep\n(Dreams)', ha='center', va='center',
           fontsize=12, fontweight='bold')
    
    box2 = FancyBboxPatch((3, 7), 1.5, 1.5, boxstyle="round,pad=0.1",
                          facecolor=color_dream, edgecolor='black', linewidth=3, alpha=0.7)
    ax.add_patch(box2)
    ax.text(3.75, 7.75, 'Thought\nMetabolism', ha='center', va='center',
           fontsize=12, fontweight='bold')
    
    # Day pathway
    box3 = FancyBboxPatch((0.5, 4), 1.5, 1.5, boxstyle="round,pad=0.1",
                          facecolor=color_perception, edgecolor='black', linewidth=3, alpha=0.7)
    ax.add_patch(box3)
    ax.text(1.25, 4.75, 'Daytime\nActivity', ha='center', va='center',
           fontsize=12, fontweight='bold')
    
    box4 = FancyBboxPatch((3, 4), 1.5, 1.5, boxstyle="round,pad=0.1",
                          facecolor=color_perception, edgecolor='black', linewidth=3, alpha=0.7)
    ax.add_patch(box4)
    ax.text(3.75, 4.75, 'Thought +\nPerception', ha='center', va='center',
           fontsize=12, fontweight='bold')
    
    # Subtraction
    box5 = FancyBboxPatch((6, 5.5), 1.5, 1.5, boxstyle="round,pad=0.1",
                          facecolor='yellow', edgecolor='black', linewidth=3, alpha=0.7)
    ax.add_patch(box5)
    ax.text(6.75, 6.25, 'Subtract\nThought', ha='center', va='center',
           fontsize=12, fontweight='bold')
    
    # Result
    box6 = FancyBboxPatch((8.5, 4), 1.2, 1.5, boxstyle="round,pad=0.1",
                          facecolor=color_perception, edgecolor='black', linewidth=3, alpha=0.7)
    ax.add_patch(box6)
    ax.text(9.1, 4.75, 'Pure\nPerception', ha='center', va='center',
           fontsize=11, fontweight='bold')
    
    # Consciousness
    box7 = FancyBboxPatch((8.5, 7), 1.2, 1.5, boxstyle="round,pad=0.1",
                          facecolor=color_consciousness, edgecolor='black', linewidth=3, alpha=0.7)
    ax.add_patch(box7)
    ax.text(9.1, 7.75, 'Conscious-\nness', ha='center', va='center',
           fontsize=11, fontweight='bold')
    
    # Arrows
    arrows = [
        ((2, 7.75), (3, 7.75), color_dream),
        ((2, 4.75), (3, 4.75), color_perception),
        ((4.5, 7.75), (6, 6.5), color_dream),
        ((4.5, 4.75), (6, 6), color_perception),
        ((7.5, 6.25), (8.5, 4.75), color_perception),
        ((7.5, 6.25), (8.5, 7.75), color_consciousness),
    ]
    
    for start, end, color in arrows:
        arrow = FancyArrowPatch(start, end, arrowstyle='->', mutation_scale=40,
                               linewidth=4, color=color, alpha=0.7)
        ax.add_patch(arrow)
    
    # Labels
    ax.text(5, 9.5, 'METABOLIC DECOMPOSITION OF CONSCIOUSNESS', 
           ha='center', fontsize=16, fontweight='bold')
    
    ax.text(1.25, 9, 'NIGHT', ha='center', fontsize=14, fontweight='bold',
           bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.7))
    ax.text(1.25, 3, 'DAY', ha='center', fontsize=14, fontweight='bold',
           bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.7))
    
    ax.text(5, 2, 'Consciousness = Thought + Perception = "Coherent thoughts with agency"',
           ha='center', fontsize=13, fontweight='bold', style='italic',
           bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
    
    output_path = f'{output_dir}/metabolic_flow_diagram.png'
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"✓ Saved: {output_path}")
    plt.close()

def main():
    """Main analysis pipeline"""
    print("="*70)
    print("METABOLIC DECOMPOSITION OF CONSCIOUSNESS")
    print("="*70)
    print("\nTheoretical Framework:")
    print("  Night: REM (dreams) = Pure thought metabolism")
    print("  Day: Activity = Thought + Perception metabolism")
    print("  Subtraction: Day - Night = Pure perception metabolism")
    print("  Consciousness = Thought + Perception = Agency")
    print("="*70)
    
    # Set style
    plt.style.use('seaborn-v0_8-darkgrid')
    sns.set_palette("husl")
    
    # Load data
    data = load_all_data()
    
    # Identify dream episodes (pure thought)
    dream_episodes = identify_dream_episodes(data)
    
    # Extract daytime metabolism (thought + perception)
    daytime_metabolism = extract_daytime_metabolism(data)
    
    # Decompose consciousness
    decomposed = decompose_consciousness_metabolism(dream_episodes, daytime_metabolism)
    
    # Generate visualizations
    if decomposed:
        create_consciousness_decomposition_visualization(dream_episodes, daytime_metabolism, 
                                                        decomposed)
        create_metabolic_flow_diagram(dream_episodes, decomposed)
    
    print("\n" + "="*70)
    print("ANALYSIS COMPLETE!")
    print("="*70)
    print("\nGenerated files:")
    print("  1. consciousness_metabolic_decomposition.png")
    print("  2. metabolic_flow_diagram.png")
    print("\nKEY DISCOVERY:")
    print("  Consciousness = Thought (dreams) + Perception (sensory)")
    print("  Dreams reveal the metabolic cost of pure thought!")
    print("="*70)

if __name__ == "__main__":
    main()
