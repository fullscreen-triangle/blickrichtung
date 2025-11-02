import json
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import seaborn as sns
from pathlib import Path

def load_reality_perception_data(filepath):
    """Load reality perception JSON data."""
    with open(filepath, 'r') as f:
        return json.load(f)

def create_garmin_atmospheric_panel(data):
    """
    GARMIN Watch Analysis: Focus on atmospheric dynamics and molecular coupling.
    Shows air displacement, molecular interactions, and energy transfer.
    """
    
    plt.style.use('seaborn-v0_8-white')
    
    fig = plt.figure(figsize=(20, 14))
    gs = GridSpec(2, 2, figure=fig, hspace=0.35, wspace=0.35)
    
    # Extract data
    atmospheric = data['atmospheric']
    metadata = data['metadata']
    
    # Panel A: Air Displacement & Mass Flow
    ax1 = fig.add_subplot(gs[0, 0])
    
    total_volume = atmospheric['total_displacement_volume_m3']
    total_mass = atmospheric['total_air_mass_displaced_kg']
    duration = atmospheric['total_duration_s']
    mean_velocity = atmospheric['mean_velocity_ms']
    
    # Create cumulative displacement over time
    t = np.linspace(0, duration, 100)
    
    # Assume constant velocity for simplicity
    cumulative_volume = (total_volume / duration) * t
    cumulative_mass = (total_mass / duration) * t
    
    # Plot both on dual axes
    ax1_twin = ax1.twinx()
    
    line1 = ax1.plot(t, cumulative_volume, linewidth=3, color='#3498db',
                    label='Volume', alpha=0.8)
    ax1.fill_between(t, 0, cumulative_volume, alpha=0.3, color='#3498db')
    
    line2 = ax1_twin.plot(t, cumulative_mass, linewidth=3, color='#e74c3c',
                         label='Mass', alpha=0.8, linestyle='--')
    
    ax1.set_xlabel('Time (s)', fontsize=14, fontweight='bold')
    ax1.set_ylabel('Cumulative Volume (m³)', fontsize=13, fontweight='bold',
                  color='#3498db')
    ax1_twin.set_ylabel('Cumulative Mass (kg)', fontsize=13, fontweight='bold',
                       color='#e74c3c')
    ax1.set_title('A', fontsize=18, fontweight='bold', loc='left', pad=15)
    ax1.grid(alpha=0.3)
    ax1.tick_params(axis='y', labelcolor='#3498db')
    ax1_twin.tick_params(axis='y', labelcolor='#e74c3c')
    
    # Add legend
    lines = line1 + line2
    labels = [l.get_label() for l in lines]
    ax1.legend(lines, labels, loc='upper left', fontsize=11, framealpha=0.95)
    
    # Add metrics
    textstr = (f'Total Volume: {total_volume:.2f} m³\n'
              f'Total Mass: {total_mass:.2f} kg\n'
              f'Mean Velocity: {mean_velocity:.2f} m/s\n'
              f'Duration: {duration:.1f} s')
    props = dict(boxstyle='round', facecolor='wheat', alpha=0.9,
                edgecolor='black', linewidth=2)
    ax1.text(0.98, 0.02, textstr, transform=ax1.transAxes, fontsize=11,
            verticalalignment='bottom', horizontalalignment='right',
            bbox=props, family='monospace', fontweight='bold')
    
    # Panel B: Molecular Interactions (Direct vs Coupled)
    ax2 = fig.add_subplot(gs[0, 1])
    
    molecules_direct = atmospheric['molecules_directly_displaced']
    molecules_coupled = atmospheric['molecules_coupled_influenced']
    coupling_factor = atmospheric['coupling_enhancement_factor']
    
    # Create comparison bars
    categories = ['Direct\nDisplacement', 'Coupled\nInfluence']
    values = [molecules_direct, molecules_coupled]
    colors = ['#2ecc71', '#9b59b6']
    
    # Use log scale
    log_values = [np.log10(v) for v in values]
    
    bars = ax2.bar(categories, log_values, color=colors, alpha=0.8,
                  edgecolor='black', linewidth=2, width=0.6)
    
    ax2.set_ylabel('log₁₀(Number of Molecules)', fontsize=13, fontweight='bold')
    ax2.set_title('B', fontsize=18, fontweight='bold', loc='left', pad=15)
    ax2.grid(alpha=0.3, axis='y')
    
    # Add values on bars
    for bar, val, log_val in zip(bars, values, log_values):
        height = bar.get_height()
        # Format in scientific notation
        exp = int(np.log10(val))
        mantissa = val / (10 ** exp)
        ax2.text(bar.get_x() + bar.get_width()/2., height + 0.5,
                f'{mantissa:.2f}×10$^{{{exp}}}$',
                ha='center', va='bottom', fontsize=11, fontweight='bold')
    
    # Add coupling factor annotation
    ax2.annotate('', xy=(1, log_values[1]), xytext=(0, log_values[0]),
                arrowprops=dict(arrowstyle='->', lw=3, color='red'))
    ax2.text(0.5, (log_values[0] + log_values[1])/2,
            f'{coupling_factor:.0f}× enhancement',
            ha='center', va='center', fontsize=12, fontweight='bold',
            bbox=dict(boxstyle='round', facecolor='yellow',
                     alpha=0.9, edgecolor='red', linewidth=2))
    
    # Panel C: Wake Dynamics & Vortex Shedding
    ax3 = fig.add_subplot(gs[1, 0])
    
    reynolds = atmospheric['reynolds_number']
    wake_length = atmospheric['wake_length_m']
    wake_volume = atmospheric['wake_volume_m3']
    vortex_freq = atmospheric['vortex_shedding_freq_hz']
    
    # Visualize wake structure
    x = np.linspace(0, wake_length, 1000)
    
    # Wake envelope (exponential decay)
    wake_width = 0.5 * np.exp(-x / (wake_length * 0.3))
    
    ax3.fill_between(x, -wake_width, wake_width, alpha=0.3, color='#3498db')
    ax3.plot(x, wake_width, 'b-', linewidth=2, alpha=0.7, label='Wake Boundary')
    ax3.plot(x, -wake_width, 'b-', linewidth=2, alpha=0.7)
    
    # Add vortex shedding visualization
    n_vortices = int(vortex_freq * duration)
    vortex_positions = np.linspace(0, wake_length, n_vortices)
    
    for i, xv in enumerate(vortex_positions[:20]):  # Show first 20
        sign = 1 if i % 2 == 0 else -1
        y_vortex = sign * 0.3 * np.exp(-xv / (wake_length * 0.3))
        ax3.plot(xv, y_vortex, 'ro', markersize=8, alpha=0.6,
                markeredgecolor='black', markeredgewidth=1)
    
    # Add runner silhouette at origin
    ax3.plot(0, 0, 'ks', markersize=20, markeredgecolor='black',
            markeredgewidth=2, label='Runner')
    
    ax3.set_xlabel('Distance Behind Runner (m)', fontsize=14, fontweight='bold')
    ax3.set_ylabel('Wake Width (m)', fontsize=14, fontweight='bold')
    ax3.set_title('C', fontsize=18, fontweight='bold', loc='left', pad=15)
    ax3.legend(loc='upper right', fontsize=11, framealpha=0.95)
    ax3.grid(alpha=0.3)
    ax3.set_ylim(-1, 1)
    
    # Add metrics
    textstr = (f'Reynolds: {reynolds:.0f}\n'
              f'Wake Length: {wake_length:.1f} m\n'
              f'Wake Volume: {wake_volume:.1f} m³\n'
              f'Vortex Freq: {vortex_freq:.3f} Hz')
    ax3.text(0.02, 0.98, textstr, transform=ax3.transAxes, fontsize=11,
            verticalalignment='top', bbox=props, family='monospace',
            fontweight='bold')
    
    # Panel D: Energy Transfer & Temperature Rise
    ax4 = fig.add_subplot(gs[1, 1])
    
    energy_transferred = atmospheric['energy_transferred_to_air_j']
    temp_rise = atmospheric['wake_temperature_rise_k']
    
    # Create energy flow diagram
    ax4.text(0.5, 0.9, 'Energy Transfer to Atmosphere',
            transform=ax4.transAxes, fontsize=16, fontweight='bold',
            ha='center', va='top')
    
    # Runner energy box
    ax4.add_patch(plt.Rectangle((0.1, 0.6), 0.3, 0.2,
                                transform=ax4.transAxes,
                                facecolor='#e74c3c', alpha=0.7,
                                edgecolor='black', linewidth=3))
    ax4.text(0.25, 0.7, 'Runner\nKinetic\nEnergy',
            transform=ax4.transAxes, fontsize=12, fontweight='bold',
            ha='center', va='center', color='white')
    
    # Arrow
    ax4.annotate('', xy=(0.6, 0.7), xytext=(0.4, 0.7),
                transform=ax4.transAxes,
                arrowprops=dict(arrowstyle='->', lw=5, color='orange'))
    ax4.text(0.5, 0.75, f'{energy_transferred:.1f} J',
            transform=ax4.transAxes, fontsize=13, fontweight='bold',
            ha='center', va='bottom',
            bbox=dict(boxstyle='round', facecolor='yellow',
                     alpha=0.9, edgecolor='black', linewidth=2))
    
    # Air heating box
    ax4.add_patch(plt.Rectangle((0.6, 0.6), 0.3, 0.2,
                                transform=ax4.transAxes,
                                facecolor='#3498db', alpha=0.7,
                                edgecolor='black', linewidth=3))
    ax4.text(0.75, 0.7, 'Air\nHeating',
            transform=ax4.transAxes, fontsize=12, fontweight='bold',
            ha='center', va='center', color='white')
    
    # Temperature rise display
    ax4.text(0.5, 0.4, f'ΔT = {temp_rise*1000:.2f} mK',
            transform=ax4.transAxes, fontsize=24, fontweight='bold',
            ha='center', va='center',
            bbox=dict(boxstyle='round', facecolor='lightcoral',
                     alpha=0.9, edgecolor='red', linewidth=3))
    
    # Additional metrics
    power = energy_transferred / duration
    textstr = (f'Total Energy: {energy_transferred:.1f} J\n'
              f'Average Power: {power:.2f} W\n'
              f'Duration: {duration:.1f} s\n'
              f'Temp Rise: {temp_rise*1000:.2f} mK')
    ax4.text(0.5, 0.15, textstr, transform=ax4.transAxes, fontsize=11,
            ha='center', va='center', bbox=props, family='monospace',
            fontweight='bold')
    
    ax4.text(0.5, 0.02, 'GARMIN Watch', fontsize=14,
            transform=ax4.transAxes, fontweight='bold', ha='center',
            bbox=dict(boxstyle='round', facecolor='lightgray',
                     alpha=0.8, edgecolor='black', linewidth=2))
    
    ax4.set_xlim(0, 1)
    ax4.set_ylim(0, 1)
    ax4.axis('off')
    ax4.set_title('D', fontsize=18, fontweight='bold', loc='left', pad=20)
    
    plt.tight_layout()
    return fig

def main():
    """Main function to generate GARMIN watch visualizations."""
    
    # Load data
    data_path = Path('public/reality_perception_garmin_cleaned_20251013_000747_20251014_234019.json')
    data = load_reality_perception_data(data_path)
    
    # Create output directory
    output_dir = Path('output')
    output_dir.mkdir(exist_ok=True)
    
    print("="*70)
    print("GENERATING GARMIN WATCH ANALYSIS - ATMOSPHERIC FOCUS")
    print("="*70)
    
    print("\nGenerating GARMIN Atmospheric Panel...")
    fig = create_garmin_atmospheric_panel(data)
    fig.savefig(output_dir / 'figure_garmin_atmospheric.png',
                dpi=300, bbox_inches='tight')
    fig.savefig(output_dir / 'figure_garmin_atmospheric.pdf',
                bbox_inches='tight')
    print("✓ GARMIN panel saved")
    
    print("\n" + "="*70)
    print("GARMIN ANALYSIS COMPLETE")
    print("="*70)
    print(f"\nOutput location: {output_dir.absolute()}")
    print("\nKey Findings:")
    atm = data['atmospheric']
    print(f"  • Air Displaced: {atm['total_air_mass_displaced_kg']:.2f} kg")
    print(f"  • Molecules Coupled: {atm['molecules_coupled_influenced']:.2e}")
    print(f"  • Reynolds Number: {atm['reynolds_number']:.0f}")
    print(f"  • Energy Transferred: {atm['energy_transferred_to_air_j']:.1f} J")
    
    plt.show()

if __name__ == "__main__":
    main()
