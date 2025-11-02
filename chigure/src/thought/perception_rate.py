import json
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import seaborn as sns
from scipy import stats
from pathlib import Path

def load_data(filepath):
    """Load JSON data from public folder."""
    with open(filepath, 'r') as f:
        return json.load(f)

def create_perception_rate_foundation_panel(data):
    """
    Create 4-panel figure establishing perception rate measurement.
    This is Figure 1 of the perception rate paper.
    """
    
    plt.style.use('seaborn-v0_8-whitegrid')
    
    fig = plt.figure(figsize=(16, 12))
    gs = GridSpec(2, 2, figure=fig, hspace=0.35, wspace=0.35)
    
    # Extract data
    restoration_times = np.array(data['simulation_results']['restoration_times'])
    heart_rate_hz = data['simulation_results']['heart_rate_hz']
    mean_rr_interval = data['simulation_results']['mean_rr_interval_s']
    mean_restoration = data['simulation_results']['mean_restoration_time_s']
    perception_rate = data['simulation_results']['perception_rate_hz']
    resonance_quality = data['simulation_results']['resonance_quality']
    
    # Panel A: The Core Measurement - Restoration Time Distribution
    ax1 = fig.add_subplot(gs[0, 0])
    
    # Histogram with KDE
    n, bins, patches = ax1.hist(restoration_times * 1e6, bins=35, 
                                 density=True, alpha=0.6, color='steelblue', 
                                 edgecolor='black', linewidth=1.5)
    
    # Add KDE
    from scipy.stats import gaussian_kde
    kde = gaussian_kde(restoration_times * 1e6)
    x_kde = np.linspace(restoration_times.min() * 1e6, 
                        restoration_times.max() * 1e6, 200)
    ax1.plot(x_kde, kde(x_kde), 'r-', linewidth=3, label='KDE')
    
    # Mark mean
    ax1.axvline(mean_restoration * 1e6, color='darkred', linestyle='--', 
                linewidth=3, label=f'μ = {mean_restoration*1e6:.1f} μs')
    
    ax1.set_xlabel('Restoration Time (μs)', fontsize=13, fontweight='bold')
    ax1.set_ylabel('Probability Density', fontsize=13, fontweight='bold')
    ax1.set_title('A', fontsize=16, fontweight='bold', loc='left', pad=10)
    ax1.legend(loc='upper right', fontsize=11, framealpha=0.9)
    ax1.grid(alpha=0.3)
    
    # Add n
    ax1.text(0.98, 0.95, f'n = {len(restoration_times)}', 
             transform=ax1.transAxes, fontsize=11, fontweight='bold',
             verticalalignment='top', horizontalalignment='right',
             bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
    
    # Panel B: The Calculation - From Restoration Time to Perception Rate
    ax2 = fig.add_subplot(gs[0, 1])
    
    # Create visual equation
    ax2.text(0.5, 0.75, 'Perception Rate Calculation', 
             transform=ax2.transAxes, fontsize=14, fontweight='bold',
             ha='center', va='center')
    
    # Equation
    equation_parts = [
        ('Perception Rate', 0.65),
        ('=', 0.55),
        ('1', 0.45),
        ('─────────────────', 0.42),
        ('Restoration Time', 0.35),
        ('', 0.25),
        (f'= 1 / {mean_restoration*1e6:.1f} μs', 0.15),
        (f'= {perception_rate:.1f} Hz', 0.05),
    ]
    
    for text, y_pos in equation_parts:
        if text:
            weight = 'bold' if '=' in text or 'Hz' in text else 'normal'
            size = 13 if '=' in text or 'Hz' in text else 12
            ax2.text(0.5, y_pos, text, transform=ax2.transAxes,
                    fontsize=size, fontweight=weight, ha='center', va='center',
                    family='monospace')
    
    # Highlight result
    ax2.add_patch(plt.Rectangle((0.15, 0.0), 0.7, 0.12, 
                                transform=ax2.transAxes,
                                facecolor='yellow', alpha=0.3, 
                                edgecolor='orange', linewidth=3))
    
    ax2.set_xlim(0, 1)
    ax2.set_ylim(0, 1)
    ax2.axis('off')
    ax2.set_title('B', fontsize=16, fontweight='bold', loc='left', pad=10)
    
    # Panel C: Comparison to Traditional Estimates
    ax3 = fig.add_subplot(gs[1, 0])
    
    # Traditional vs measured perception rates
    categories = ['Traditional\nEstimate\n(Neural)', 'Measured\n(Molecular)', 'Ratio']
    values = [60, perception_rate, perception_rate / 60]
    colors_bar = ['#95a5a6', '#2ecc71', '#e74c3c']
    
    # Use two y-axes
    ax3_twin = ax3.twinx()
    
    bars1 = ax3.bar([0, 1], values[:2], color=colors_bar[:2], 
                    alpha=0.8, edgecolor='black', linewidth=2, width=0.6)
    bars2 = ax3_twin.bar([2], [values[2]], color=colors_bar[2], 
                         alpha=0.8, edgecolor='black', linewidth=2, width=0.6)
    
    ax3.set_ylabel('Frequency (Hz)', fontsize=13, fontweight='bold')
    ax3_twin.set_ylabel('Fold Increase', fontsize=13, fontweight='bold', 
                        color=colors_bar[2])
    ax3_twin.tick_params(axis='y', labelcolor=colors_bar[2], labelsize=11)
    ax3.set_xticks([0, 1, 2])
    ax3.set_xticklabels(categories, fontsize=11, fontweight='bold')
    ax3.set_title('C', fontsize=16, fontweight='bold', loc='left', pad=10)
    ax3.grid(alpha=0.3, axis='y')
    ax3.set_yscale('log')
    ax3.tick_params(axis='both', labelsize=11)
    
    # Add values on bars
    for bar, val in zip(bars1, values[:2]):
        height = bar.get_height()
        ax3.text(bar.get_x() + bar.get_width()/2., height * 1.2,
                f'{val:.0f} Hz', ha='center', va='bottom', 
                fontsize=12, fontweight='bold')
    
    for bar in bars2:
        height = bar.get_height()
        ax3_twin.text(bar.get_x() + bar.get_width()/2., height * 1.1,
                     f'{values[2]:.1f}×', ha='center', va='bottom', 
                     fontsize=12, fontweight='bold', color=colors_bar[2])
    
    # Panel D: Experimental Validation - Running Without Falling
    ax4 = fig.add_subplot(gs[1, 1])
    
    # Create conceptual diagram
    ax4.text(0.5, 0.9, 'Experimental Validation', 
             transform=ax4.transAxes, fontsize=14, fontweight='bold',
             ha='center', va='top')
    
    # Logic flow
    logic = [
        ('Running requires:', 0.75, 'black', 12),
        ('Perception ⇄ Thought ⇄ Action', 0.68, 'darkblue', 11),
        ('', 0.60, 'black', 11),
        ('If desynchronized:', 0.52, 'black', 12),
        ('Perception ≠ Thought → Fall', 0.45, 'darkred', 11),
        ('', 0.37, 'black', 11),
        ('Observed:', 0.29, 'black', 12),
        ('No falls during 400m run', 0.22, 'darkgreen', 11),
        ('', 0.14, 'black', 11),
        ('∴ Perception = Thought', 0.06, 'darkgreen', 13),
    ]
    
    for text, y_pos, color, size in logic:
        if text:
            weight = 'bold' if '∴' in text or ':' in text else 'normal'
            ax4.text(0.5, y_pos, text, transform=ax4.transAxes,
                    fontsize=size, fontweight=weight, ha='center', va='center',
                    color=color)
    
    # Highlight conclusion
    ax4.add_patch(plt.Rectangle((0.1, 0.0), 0.8, 0.12, 
                                transform=ax4.transAxes,
                                facecolor='lightgreen', alpha=0.3, 
                                edgecolor='darkgreen', linewidth=3))
    
    # Add resonance quality
    ax4.text(0.5, 0.95, f'Resonance Quality: {resonance_quality:.2f}', 
             transform=ax4.transAxes, fontsize=10, fontweight='bold',
             ha='center', va='top',
             bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.7))
    
    ax4.set_xlim(0, 1)
    ax4.set_ylim(0, 1)
    ax4.axis('off')
    ax4.set_title('D', fontsize=16, fontweight='bold', loc='left', pad=10)
    
    plt.tight_layout()
    return fig

def main():
    """Main function to generate visualization."""
    data_path = Path('public/heartbeat_gas_bmd_unified_20251015_002328.json')
    data = load_data(data_path)
    
    fig = create_perception_rate_foundation_panel(data)
    
    output_path = Path('output/figure_1_perception_rate_foundation.png')
    output_path.parent.mkdir(exist_ok=True)
    fig.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"Figure 1 saved to {output_path}")
    
    fig.savefig(output_path.with_suffix('.pdf'), bbox_inches='tight')
    print(f"Figure 1 (PDF) saved to {output_path.with_suffix('.pdf')}")
    
    plt.show()

if __name__ == "__main__":
    main()
