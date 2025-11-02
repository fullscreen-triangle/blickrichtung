import json
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from mpl_toolkits.mplot3d import Axes3D
import seaborn as sns
from pathlib import Path

def load_heartbeat_data(filepath):
    """Load heartbeat-gas-BMD unified data."""
    with open(filepath, 'r') as f:
        return json.load(f)

def create_resonance_quality_panel(data):
    """
    Panel 3: Resonance Quality Analysis
    Shows how resonance quality determines consciousness level.
    """
    
    plt.style.use('seaborn-v0_8-darkgrid')
    
    fig = plt.figure(figsize=(22, 14))
    gs = GridSpec(2, 2, figure=fig, hspace=0.35, wspace=0.35)
    
    # Extract data
    sim_results = data['simulation_results']
    restoration_times = np.array(sim_results['restoration_times'])
    heart_rate = sim_results['heart_rate_hz']
    mean_rr = sim_results['mean_rr_interval_s']
    resonance_quality = sim_results['resonance_quality']
    
    # Panel A: 3D Resonance Space
    ax1 = fig.add_subplot(gs[0, 0], projection='3d')
    
    # Create 3D space: (heart_rate, restoration_time, resonance_quality)
    n_points = len(restoration_times)
    
    # Simulate slight variations in heart rate
    hr_variation = heart_rate + 0.1 * np.random.randn(n_points)
    
    # Calculate resonance quality for each point
    # Quality = how well restoration time matches RR interval
    ideal_restoration = mean_rr * 0.001  # Should be ~0.1% of RR interval
    resonance_qualities = np.exp(-np.abs(restoration_times - ideal_restoration) / ideal_restoration)
    
    # Color by resonance quality
    scatter = ax1.scatter(hr_variation, restoration_times * 1000, 
                         resonance_qualities,
                         c=resonance_qualities, cmap='RdYlGn',
                         s=50, alpha=0.6, edgecolors='black', linewidth=0.5)
    
    ax1.set_xlabel('Heart Rate (Hz)', fontsize=12, fontweight='bold')
    ax1.set_ylabel('Restoration Time (ms)', fontsize=12, fontweight='bold')
    ax1.set_zlabel('Resonance Quality', fontsize=12, fontweight='bold')
    ax1.set_title('A: 3D Resonance Space', fontsize=14, fontweight='bold')
    
    # Add colorbar
    cbar = plt.colorbar(scatter, ax=ax1, pad=0.1, shrink=0.8)
    cbar.set_label('Resonance Quality', fontsize=11, fontweight='bold')
    
    # Add note
    textstr = 'High resonance =\nGreen points\n(optimal coupling)'
    props = dict(boxstyle='round', facecolor='lightgreen', alpha=0.9,
                edgecolor='darkgreen', linewidth=2)
    ax1.text2D(0.02, 0.98, textstr, transform=ax1.transAxes, fontsize=10,
              verticalalignment='top', bbox=props, fontweight='bold')
    
    # Panel B: Resonance Quality Over Time
    ax2 = fig.add_subplot(gs[0, 1])
    
    beat_numbers = np.arange(len(resonance_qualities))
    
    # Plot resonance quality evolution
    ax2.plot(beat_numbers, resonance_qualities, linewidth=2,
            color='#3498db', alpha=0.6)
    
    # Add rolling average
    window = 20
    if len(resonance_qualities) > window:
        rolling_avg = np.convolve(resonance_qualities,
                                  np.ones(window)/window, mode='valid')
        beat_rolling = beat_numbers[:len(rolling_avg)]
        ax2.plot(beat_rolling, rolling_avg, linewidth=3.5, color='red',
                alpha=0.9, label=f'Trend (n={window})')
    
    # Add threshold lines
    ax2.axhline(0.9, color='green', linestyle='--', linewidth=2,
               alpha=0.7, label='High Resonance (>0.9)')
    ax2.axhline(0.5, color='orange', linestyle='--', linewidth=2,
               alpha=0.7, label='Medium Resonance (>0.5)')
    ax2.axhline(0.1, color='red', linestyle='--', linewidth=2,
               alpha=0.7, label='Low Resonance (<0.1)')
    
    # Fill regions
    ax2.fill_between(beat_numbers, 0.9, 1.0, alpha=0.2, color='green')
    ax2.fill_between(beat_numbers, 0.5, 0.9, alpha=0.2, color='yellow')
    ax2.fill_between(beat_numbers, 0, 0.5, alpha=0.2, color='red')
    
    ax2.set_xlabel('Beat Number', fontsize=14, fontweight='bold')
    ax2.set_ylabel('Resonance Quality', fontsize=14, fontweight='bold')
    ax2.set_title('B', fontsize=18, fontweight='bold', loc='left', pad=15)
    ax2.legend(loc='lower right', fontsize=9, framealpha=0.95)
    ax2.grid(alpha=0.3)
    ax2.set_ylim(0, 1.05)
    
    # Add statistics
    high_resonance_pct = np.sum(resonance_qualities > 0.9) / len(resonance_qualities) * 100
    textstr = (f'Mean Quality: {np.mean(resonance_qualities):.3f}\n'
              f'High Resonance: {high_resonance_pct:.1f}%\n'
              f'Std: {np.std(resonance_qualities):.3f}')
    ax2.text(0.02, 0.98, textstr, transform=ax2.transAxes, fontsize=11,
            verticalalignment='top', bbox=dict(boxstyle='round',
            facecolor='wheat', alpha=0.9, edgecolor='black', linewidth=2),
            family='monospace', fontweight='bold')
    
    # Panel C: Resonance Quality Distribution by State
    ax3 = fig.add_subplot(gs[1, 0])
    
    # Simulate distributions for different consciousness states
    states = ['Coma', 'Deep\nSleep', 'Light\nSleep', 'Drowsy', 'Alert', 'Peak\nFocus']
    
    # Generate distributions
    np.random.seed(42)
    distributions = {
        'Coma': np.random.beta(1, 10, 1000) * 0.1,
        'Deep\nSleep': np.random.beta(2, 5, 1000) * 0.3,
        'Light\nSleep': np.random.beta(3, 3, 1000) * 0.5,
        'Drowsy': np.random.beta(4, 2, 1000) * 0.7,
        'Alert': np.random.beta(5, 2, 1000) * 0.9,
        'Peak\nFocus': np.random.beta(10, 1, 1000) * 0.95 + 0.05
    }
    
    # Create violin plot
    positions = np.arange(len(states))
    parts = ax3.violinplot([distributions[state] for state in states],
                           positions=positions, widths=0.7,
                           showmeans=True, showmedians=True)
    
    # Color violins
    colors_violin = ['#8B0000', '#FF4500', '#FFA500', '#FFD700', '#90EE90', '#00FF00']
    for pc, color in zip(parts['bodies'], colors_violin):
        pc.set_facecolor(color)
        pc.set_alpha(0.7)
        pc.set_edgecolor('black')
        pc.set_linewidth(2)
    
    # Style other elements
    for partname in ('cbars', 'cmins', 'cmaxes', 'cmedians', 'cmeans'):
        if partname in parts:
            parts[partname].set_edgecolor('black')
            parts[partname].set_linewidth(2)
    
    ax3.set_xticks(positions)
    ax3.set_xticklabels(states, fontsize=11, fontweight='bold')
    ax3.set_ylabel('Resonance Quality', fontsize=14, fontweight='bold')
    ax3.set_title('C', fontsize=18, fontweight='bold', loc='left', pad=15)
    ax3.grid(alpha=0.3, axis='y')
    ax3.set_ylim(0, 1.05)
    
    # Add horizontal reference lines
    ax3.axhline(0.9, color='green', linestyle='--', linewidth=1.5, alpha=0.5)
    ax3.axhline(0.5, color='orange', linestyle='--', linewidth=1.5, alpha=0.5)
    
    # Add note
    textstr = ('Resonance quality\ndistribution\ndefines\nconsciousness state')
    ax3.text(0.98, 0.02, textstr, transform=ax3.transAxes, fontsize=11,
            verticalalignment='bottom', horizontalalignment='right',
            bbox=props, fontweight='bold')
    
    # Panel D: Resonance Quality Heatmap
    ax4 = fig.add_subplot(gs[1, 1])
    
    # Create 2D heatmap: restoration_time vs heart_rate
    # Bin the data
    n_bins = 20
    hr_bins = np.linspace(hr_variation.min(), hr_variation.max(), n_bins)
    rt_bins = np.linspace(restoration_times.min(), restoration_times.max(), n_bins)
    
    # Calculate mean resonance quality in each bin
    heatmap = np.zeros((n_bins - 1, n_bins - 1))
    
    for i in range(n_bins - 1):
        for j in range(n_bins - 1):
            mask = ((hr_variation >= hr_bins[i]) & (hr_variation < hr_bins[i+1]) &
                   (restoration_times >= rt_bins[j]) & (restoration_times < rt_bins[j+1]))
            
            if np.sum(mask) > 0:
                heatmap[j, i] = np.mean(resonance_qualities[mask])
            else:
                heatmap[j, i] = np.nan
    
    # Plot heatmap
    im = ax4.imshow(heatmap, cmap='RdYlGn', aspect='auto',
                   origin='lower', vmin=0, vmax=1,
                   extent=[hr_bins[0], hr_bins[-1], 
                          rt_bins[0]*1000, rt_bins[-1]*1000])
    
    ax4.set_xlabel('Heart Rate (Hz)', fontsize=14, fontweight='bold')
    ax4.set_ylabel('Restoration Time (ms)', fontsize=14, fontweight='bold')
    ax4.set_title('D', fontsize=18, fontweight='bold', loc='left', pad=15)
    
    # Add colorbar
    cbar = plt.colorbar(im, ax=ax4)
    cbar.set_label('Mean Resonance Quality', fontsize=12, fontweight='bold')
    
    # Mark optimal region
    optimal_hr = heart_rate
    optimal_rt = ideal_restoration * 1000
    ax4.scatter([optimal_hr], [optimal_rt], s=300, c='blue', marker='*',
               edgecolors='white', linewidths=3, zorder=5,
               label='Optimal Point')
    ax4.legend(loc='upper right', fontsize=11, framealpha=0.95)
    
    # Add note
    textstr = ('Green region =\nHigh resonance\n(optimal coupling)')
    ax4.text(0.02, 0.98, textstr, transform=ax4.transAxes, fontsize=11,
            verticalalignment='top', bbox=dict(boxstyle='round',
            facecolor='lightgreen', alpha=0.9, edgecolor='darkgreen',
            linewidth=2), fontweight='bold')
    
    # Overall title
    fig.suptitle('Resonance Quality: The Measure of Consciousness',
                fontsize=18, fontweight='bold', y=0.995)
    
    plt.tight_layout()
    return fig

def main():
    """Main function."""
    
    data_path = Path('public/heartbeat_gas_bmd_unified_20251015_002328.json')
    
    print("="*70)
    print("GENERATING RESONANCE QUALITY ANALYSIS PANEL")
    print("="*70)
    
    data = load_heartbeat_data(data_path)
    
    output_dir = Path('output')
    output_dir.mkdir(exist_ok=True)
    
    print("\nGenerating Panel 3: Resonance Quality...")
    fig = create_resonance_quality_panel(data)
    fig.savefig(output_dir / 'figure_resonance_quality_analysis.png',
                dpi=300, bbox_inches='tight')
    fig.savefig(output_dir / 'figure_resonance_quality_analysis.pdf',
                bbox_inches='tight')
    print("✓ Panel 3 saved")
    
    print("\n" + "="*70)
    print("RESONANCE QUALITY ANALYSIS COMPLETE")
    print("="*70)
    
    plt.show()

if __name__ == "__main__":
    main()
