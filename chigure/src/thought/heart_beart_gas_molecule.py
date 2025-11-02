import json
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import seaborn as sns
from pathlib import Path
from scipy import stats

def load_heartbeat_data(filepath):
    """Load heartbeat-gas-BMD unified data."""
    with open(filepath, 'r') as f:
        return json.load(f)

def create_heartbeat_unified_panel(data):
    """
    Panel 1: Heartbeat-Gas-BMD Unified Framework
    Shows how heartbeat perturbations drive perception through equilibrium restoration.
    """
    
    plt.style.use('seaborn-v0_8-whitegrid')
    
    fig = plt.figure(figsize=(22, 14))
    gs = GridSpec(2, 2, figure=fig, hspace=0.35, wspace=0.35)
    
    # Extract data
    sim_results = data['simulation_results']
    key_insights = data['key_insights']
    
    heart_rate = sim_results['heart_rate_hz']
    mean_rr = sim_results['mean_rr_interval_s']
    mean_restoration = sim_results['mean_restoration_time_s']
    perception_rate = sim_results['perception_rate_hz']
    resonance_quality = sim_results['resonance_quality']
    restoration_times = np.array(sim_results['restoration_times'])
    
    # Panel A: Heartbeat Perturbation Timeline
    ax1 = fig.add_subplot(gs[0, 0])
    
    # Create timeline
    n_beats = len(restoration_times)
    t_beats = np.cumsum([mean_rr] * n_beats)
    t_beats = np.concatenate([[0], t_beats])
    
    # Simulate equilibrium perturbation
    t_fine = np.linspace(0, t_beats[-1], 10000)
    equilibrium = np.ones(len(t_fine))
    
    # Add perturbations at each heartbeat
    for beat_time in t_beats[1:]:
        # Perturbation: sudden drop then exponential recovery
        mask = t_fine >= beat_time
        time_since_beat = t_fine[mask] - beat_time
        
        # Find restoration time for this beat
        beat_idx = np.argmin(np.abs(t_beats[1:] - beat_time))
        if beat_idx < len(restoration_times):
            tau = restoration_times[beat_idx]
        else:
            tau = mean_restoration
        
        # Exponential recovery
        recovery = 1 - 0.3 * np.exp(-time_since_beat / tau)
        equilibrium[mask] = np.minimum(equilibrium[mask], recovery)
    
    # Plot
    ax1.plot(t_fine, equilibrium, linewidth=2, color='#3498db', alpha=0.8)
    ax1.fill_between(t_fine, 0.7, equilibrium, alpha=0.3, color='#3498db')
    
    # Mark heartbeats
    for beat_time in t_beats[1:21]:  # First 20 beats
        ax1.axvline(beat_time, color='red', linestyle='--', 
                   linewidth=1.5, alpha=0.5)
    
    # Add equilibrium line
    ax1.axhline(1.0, color='green', linestyle='-', linewidth=2,
               alpha=0.7, label='Perfect Equilibrium')
    
    ax1.set_xlabel('Time (s)', fontsize=14, fontweight='bold')
    ax1.set_ylabel('Gas Molecular Equilibrium', fontsize=14, fontweight='bold')
    ax1.set_title('A', fontsize=18, fontweight='bold', loc='left', pad=15)
    ax1.legend(loc='lower right', fontsize=11, framealpha=0.95)
    ax1.grid(alpha=0.3)
    ax1.set_xlim(0, t_beats[20])
    ax1.set_ylim(0.65, 1.05)
    
    # Add metrics
    textstr = (f'Heart Rate: {heart_rate:.2f} Hz\n'
              f'RR Interval: {mean_rr*1000:.1f} ms\n'
              f'Restoration: {mean_restoration*1000:.3f} ms\n'
              f'Red lines = Heartbeats')
    props = dict(boxstyle='round', facecolor='wheat', alpha=0.9,
                edgecolor='black', linewidth=2)
    ax1.text(0.02, 0.02, textstr, transform=ax1.transAxes, fontsize=11,
            verticalalignment='bottom', bbox=props, family='monospace',
            fontweight='bold')
    
    # Panel B: Restoration Time Distribution
    ax2 = fig.add_subplot(gs[0, 1])
    
    # Histogram
    counts, bins, patches = ax2.hist(restoration_times * 1000, bins=30,
                                     color='#2ecc71', alpha=0.7,
                                     edgecolor='black', linewidth=1.5)
    
    # Add mean and median lines
    mean_rest_ms = mean_restoration * 1000
    median_rest_ms = np.median(restoration_times) * 1000
    
    ax2.axvline(mean_rest_ms, color='red', linestyle='--', linewidth=3,
               label=f'Mean: {mean_rest_ms:.3f} ms')
    ax2.axvline(median_rest_ms, color='blue', linestyle='--', linewidth=3,
               label=f'Median: {median_rest_ms:.3f} ms')
    
    # Fit Gaussian
    mu, sigma = stats.norm.fit(restoration_times * 1000)
    x_fit = np.linspace(restoration_times.min() * 1000, 
                        restoration_times.max() * 1000, 100)
    y_fit = stats.norm.pdf(x_fit, mu, sigma) * len(restoration_times) * \
            (bins[1] - bins[0])
    ax2.plot(x_fit, y_fit, 'k-', linewidth=2.5, alpha=0.8,
            label=f'Gaussian Fit\nμ={mu:.3f}, σ={sigma:.3f}')
    
    ax2.set_xlabel('Restoration Time (ms)', fontsize=14, fontweight='bold')
    ax2.set_ylabel('Frequency', fontsize=14, fontweight='bold')
    ax2.set_title('B', fontsize=18, fontweight='bold', loc='left', pad=15)
    ax2.legend(loc='upper right', fontsize=10, framealpha=0.95)
    ax2.grid(alpha=0.3, axis='y')
    
    # Add statistics
    textstr = (f'N = {len(restoration_times)}\n'
              f'Min: {restoration_times.min()*1000:.3f} ms\n'
              f'Max: {restoration_times.max()*1000:.3f} ms\n'
              f'Std: {restoration_times.std()*1000:.3f} ms')
    ax2.text(0.98, 0.98, textstr, transform=ax2.transAxes, fontsize=10,
            verticalalignment='top', horizontalalignment='right',
            bbox=props, family='monospace', fontweight='bold')
    
    # Panel C: Perception Rate vs Heart Rate Coupling
    ax3 = fig.add_subplot(gs[1, 0])
    
    # Calculate perception frames per heartbeat
    frames_per_beat = perception_rate / heart_rate
    
    # Create bar comparison
    categories = ['Heart Rate\n(Hz)', 'Perception Rate\n(Hz)', 
                 'Frames per\nHeartbeat']
    values = [heart_rate, perception_rate, frames_per_beat]
    colors = ['#e74c3c', '#3498db', '#9b59b6']
    
    # Use log scale for perception rate
    bars = ax3.bar(categories, values, color=colors, alpha=0.8,
                  edgecolor='black', linewidth=2, width=0.6)
    
    ax3.set_ylabel('Value (log scale)', fontsize=14, fontweight='bold')
    ax3.set_yscale('log')
    ax3.set_title('C', fontsize=18, fontweight='bold', loc='left', pad=15)
    ax3.grid(alpha=0.3, axis='y', which='both')
    
    # Add values on bars
    for bar, val in zip(bars, values):
        height = bar.get_height()
        if val >= 1000:
            label = f'{val:.0f}'
        elif val >= 10:
            label = f'{val:.1f}'
        else:
            label = f'{val:.2f}'
        
        ax3.text(bar.get_x() + bar.get_width()/2., height * 1.2,
                label, ha='center', va='bottom', fontsize=12, 
                fontweight='bold')
    
    # Add key insight
    textstr = (f'KEY INSIGHT:\n'
              f'{frames_per_beat:.0f} perception frames\n'
              f'between heartbeats\n\n'
              f'Resonance Quality:\n{resonance_quality:.3f}')
    ax3.text(0.98, 0.02, textstr, transform=ax3.transAxes, fontsize=11,
            verticalalignment='bottom', horizontalalignment='right',
            bbox=dict(boxstyle='round', facecolor='lightgreen',
                     alpha=0.9, edgecolor='darkgreen', linewidth=3),
            fontweight='bold')
    
    # Panel D: Restoration Time vs Beat Number
    ax4 = fig.add_subplot(gs[1, 1])
    
    beat_numbers = np.arange(len(restoration_times))
    
    # Scatter plot
    scatter = ax4.scatter(beat_numbers, restoration_times * 1000,
                         c=restoration_times * 1000, cmap='viridis',
                         s=50, alpha=0.6, edgecolors='black', linewidth=0.5)
    
    # Add rolling average
    window = 10
    if len(restoration_times) > window:
        rolling_avg = np.convolve(restoration_times * 1000, 
                                  np.ones(window)/window, mode='valid')
        beat_rolling = beat_numbers[:len(rolling_avg)]
        ax4.plot(beat_rolling, rolling_avg, linewidth=3, color='red',
                alpha=0.8, label=f'Rolling Avg (n={window})')
    
    # Add mean line
    ax4.axhline(mean_rest_ms, color='blue', linestyle='--', linewidth=2,
               alpha=0.7, label=f'Mean: {mean_rest_ms:.3f} ms')
    
    ax4.set_xlabel('Beat Number', fontsize=14, fontweight='bold')
    ax4.set_ylabel('Restoration Time (ms)', fontsize=14, fontweight='bold')
    ax4.set_title('D', fontsize=18, fontweight='bold', loc='left', pad=15)
    ax4.legend(loc='upper right', fontsize=11, framealpha=0.95)
    ax4.grid(alpha=0.3)
    
    # Add colorbar
    cbar = plt.colorbar(scatter, ax=ax4)
    cbar.set_label('Restoration Time (ms)', fontsize=11, fontweight='bold')
    
    # Add note
    textstr = 'Restoration time\nvaries with each\nheartbeat'
    ax4.text(0.02, 0.98, textstr, transform=ax4.transAxes, fontsize=11,
            verticalalignment='top', bbox=props, fontweight='bold')
    
    # Overall title
    fig.suptitle('Heartbeat-Gas-BMD Unified Framework: Equilibrium Restoration Drives Perception',
                fontsize=18, fontweight='bold', y=0.995)
    
    plt.tight_layout()
    return fig

def main():
    """Main function."""
    
    data_path = Path('public/heartbeat_gas_bmd_unified_20251015_002328.json')
    
    print("="*70)
    print("GENERATING HEARTBEAT-GAS-BMD UNIFIED FRAMEWORK PANEL")
    print("="*70)
    
    data = load_heartbeat_data(data_path)
    
    output_dir = Path('output')
    output_dir.mkdir(exist_ok=True)
    
    print("\nGenerating Panel 1: Heartbeat Unified Framework...")
    fig = create_heartbeat_unified_panel(data)
    fig.savefig(output_dir / 'figure_heartbeat_unified_framework.png',
                dpi=300, bbox_inches='tight')
    fig.savefig(output_dir / 'figure_heartbeat_unified_framework.pdf',
                bbox_inches='tight')
    print("✓ Panel 1 saved")
    
    print("\n" + "="*70)
    print("HEARTBEAT UNIFIED FRAMEWORK COMPLETE")
    print("="*70)
    
    plt.show()

if __name__ == "__main__":
    main()
