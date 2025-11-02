import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from mpl_toolkits.mplot3d import Axes3D
import seaborn as sns
from pathlib import Path

def create_multiscale_atlas_figure():
    """
    Master Figure 4: Multi-Scale Consciousness Atlas
    Shows consciousness geometry from GPS to Planck scale.
    """
    
    plt.style.use('seaborn-v0_8-darkgrid')
    
    fig = plt.figure(figsize=(24, 18))
    gs = GridSpec(3, 2, figure=fig, hspace=0.35, wspace=0.3)
    
    # Define scales
    scales = {
        'GPS (5m)': {'precision': 5, 'color': '#e74c3c', 'complexity': 1},
        'Millimeter (1mm)': {'precision': 1e-3, 'color': '#f39c12', 'complexity': 10},
        'Micrometer (1μm)': {'precision': 1e-6, 'color': '#f1c40f', 'complexity': 100},
        'Nanometer (1nm)': {'precision': 1e-9, 'color': '#2ecc71', 'complexity': 1000},
        'Picometer (1pm)': {'precision': 1e-12, 'color': '#3498db', 'complexity': 10000},
        'Planck (10⁻³⁵m)': {'precision': 1.6e-35, 'color': '#9b59b6', 'complexity': 1e10}
    }
    
    scale_names = list(scales.keys())
    
    # Panel A: GPS Scale (Macro Consciousness)
    ax1 = fig.add_subplot(gs[0, 0])
    
    # Simulate GPS trajectory with consciousness signatures
    t = np.linspace(0, 100, 1000)
    x = 4 * t + 2 * np.sin(0.1 * t)  # Forward motion with decisions
    y = 0.5 * np.sin(0.2 * t) + 0.3 * np.cos(0.15 * t)
    
    # Consciousness intensity (from trajectory complexity)
    dx = np.gradient(x)
    dy = np.gradient(y)
    consciousness_gps = np.sqrt(dx**2 + dy**2)
    consciousness_gps = (consciousness_gps - consciousness_gps.min()) / \
                        (consciousness_gps.max() - consciousness_gps.min())
    
    scatter = ax1.scatter(x, y, c=consciousness_gps, cmap='plasma',
                         s=30, alpha=0.7, edgecolors='black', linewidth=0.3)
    ax1.plot(x, y, 'k-', linewidth=1, alpha=0.3)
    
    ax1.set_xlabel('X Position (m)', fontsize=11, fontweight='bold')
    ax1.set_ylabel('Y Position (m)', fontsize=11, fontweight='bold')
    ax1.set_title('A: GPS Scale (5m precision)\nMacro Consciousness - Decisions & Attention',
                 fontsize=13, fontweight='bold', pad=15)
    ax1.grid(alpha=0.3)
    ax1.set_aspect('equal')
    
    cbar = plt.colorbar(scatter, ax=ax1)
    cbar.set_label('Consciousness\nIntensity', fontsize=10, fontweight='bold')
    
    # Panel B: Nanosecond Scale (Neural Consciousness)
    ax2 = fig.add_subplot(gs[0, 1])
    
    # Simulate neural spike timing
    t_nano = np.linspace(0, 1e-6, 10000)  # 1 microsecond window
    
    # Multiple neurons firing
    n_neurons = 5
    spike_trains = []
    
    for i in range(n_neurons):
        # Random spike times
        n_spikes = np.random.randint(5, 15)
        spike_times = np.sort(np.random.uniform(0, 1e-6, n_spikes))
        spike_trains.append(spike_times)
        
        # Plot raster
        ax2.scatter(spike_times * 1e9, [i] * len(spike_times), s=100,
                   c='red', marker='|', linewidths=2)
    
    # Calculate consciousness from spike synchrony
    # Bin spikes
    bins = np.linspace(0, 1e-6, 100)
    spike_counts = np.zeros(len(bins) - 1)
    
    for spike_times in spike_trains:
        counts, _ = np.histogram(spike_times, bins=bins)
        spike_counts += counts
    
    # Plot synchrony
    ax2_twin = ax2.twinx()
    bin_centers = (bins[:-1] + bins[1:]) / 2 * 1e9
    ax2_twin.plot(bin_centers, spike_counts, linewidth=2, color='blue',
                 alpha=0.7, label='Spike Synchrony')
    ax2_twin.fill_between(bin_centers, 0, spike_counts, alpha=0.3, color='blue')
    
    ax2.set_xlabel('Time (nanoseconds)', fontsize=11, fontweight='bold')
    ax2.set_ylabel('Neuron ID', fontsize=11, fontweight='bold')
    ax2_twin.set_ylabel('Spike Synchrony\n(Consciousness)', fontsize=10,
                       fontweight='bold', color='blue')
    ax2.set_title('B: Nanosecond Scale (Neural)\nConsciousness from Spike Timing',
                 fontsize=13, fontweight='bold', pad=15)
    ax2.set_yticks(range(n_neurons))
    ax2.grid(alpha=0.3, axis='x')
    ax2_twin.tick_params(axis='y', labelcolor='blue')
    
    # Panel C: Femtosecond Scale (Molecular Consciousness)
    ax3 = fig.add_subplot(gs[1, 0], projection='3d')
    
    # Simulate molecular dynamics
    n_molecules = 100
    
    # Initial positions
    theta = np.random.uniform(0, 2*np.pi, n_molecules)
    phi = np.random.uniform(0, np.pi, n_molecules)
    r = np.random.uniform(0.5, 1.5, n_molecules)
    
    x_mol = r * np.sin(phi) * np.cos(theta)
    y_mol = r * np.sin(phi) * np.sin(theta)
    z_mol = r * np.cos(phi)
    
    # Consciousness from molecular coherence
    # Distance from center
    distances = np.sqrt(x_mol**2 + y_mol**2 + z_mol**2)
    coherence = np.exp(-distances)  # Higher coherence near center
    
    scatter = ax3.scatter(x_mol, y_mol, z_mol, c=coherence, cmap='viridis',
                         s=50, alpha=0.7, edgecolors='black', linewidth=0.5)
    
    ax3.set_xlabel('X (nm)', fontsize=10, fontweight='bold')
    ax3.set_ylabel('Y (nm)', fontsize=10, fontweight='bold')
    ax3.set_zlabel('Z (nm)', fontsize=10, fontweight='bold')
    ax3.set_title('C: Femtosecond Scale (Molecular)\nQuantum Coherence = Consciousness',
                 fontsize=13, fontweight='bold', pad=20)
    
    cbar = plt.colorbar(scatter, ax=ax3, pad=0.1, shrink=0.8)
    cbar.set_label('Quantum\nCoherence', fontsize=10, fontweight='bold')
    
    # Panel D: Planck Scale (Fundamental Consciousness)
    ax4 = fig.add_subplot(gs[1, 1])
    
    # Simulate spacetime foam at Planck scale
    x_planck = np.linspace(-5, 5, 100)
    y_planck = np.linspace(-5, 5, 100)
    X_planck, Y_planck = np.meshgrid(x_planck, y_planck)
    
    # Consciousness = spacetime curvature fluctuations
    Z_planck = np.sin(X_planck) * np.cos(Y_planck) + \
               0.5 * np.sin(2*X_planck) * np.sin(2*Y_planck) + \
               0.2 * np.random.randn(*X_planck.shape)
    
    im = ax4.contourf(X_planck, Y_planck, Z_planck, levels=20,
                     cmap='twilight', alpha=0.8)
    ax4.contour(X_planck, Y_planck, Z_planck, levels=20,
               colors='black', alpha=0.3, linewidths=0.5)
    
    ax4.set_xlabel('Planck Length Units', fontsize=11, fontweight='bold')
    ax4.set_ylabel('Planck Length Units', fontsize=11, fontweight='bold')
    ax4.set_title('D: Planck Scale (10⁻³⁵m)\nSpacetime Geometry = Consciousness',
                 fontsize=13, fontweight='bold', pad=15)
    ax4.set_aspect('equal')
    
    cbar = plt.colorbar(im, ax=ax4)
    cbar.set_label('Spacetime\nCurvature', fontsize=10, fontweight='bold')
    
    # Panel E: Scale Comparison (All Scales)
    ax5 = fig.add_subplot(gs[2, 0])
    
    scale_values = [scales[name]['precision'] for name in scale_names]
    complexity_values = [scales[name]['complexity'] for name in scale_names]
    colors_scale = [scales[name]['color'] for name in scale_names]
    
    # Create log-log plot
    ax5.loglog(scale_values, complexity_values, 'o-', linewidth=3, markersize=15,
              color='black', markerfacecolor='none', markeredgewidth=2)
    
    # Color each point
    for i, (sv, cv, color, name) in enumerate(zip(scale_values, complexity_values,
                                                    colors_scale, scale_names)):
        ax5.scatter([sv], [cv], s=300, c=color, edgecolors='black',
                   linewidth=3, zorder=5)
        
        # Add labels
        if i % 2 == 0:
            xytext = (20, 20)
        else:
            xytext = (20, -20)
        
        ax5.annotate(name.split('(')[0].strip(), xy=(sv, cv), xytext=xytext,
                    textcoords='offset points', fontsize=10, fontweight='bold',
                    bbox=dict(boxstyle='round', facecolor=color, alpha=0.7,
                             edgecolor='black', linewidth=2),
                    arrowprops=dict(arrowstyle='->', lw=2, color='black'))
    
    ax5.set_xlabel('Spatial Precision (meters)', fontsize=12, fontweight='bold')
    ax5.set_ylabel('Consciousness Complexity\n(Information Bits)', fontsize=12, fontweight='bold')
    ax5.set_title('E: Multi-Scale Consciousness Complexity\nSame Geometry, Increasing Information',
                 fontsize=13, fontweight='bold', pad=15)
    ax5.grid(True, alpha=0.3, which='both')
    
    # Add power law fit
    log_scale = np.log10(scale_values)
    log_complexity = np.log10(complexity_values)
    coeffs = np.polyfit(log_scale, log_complexity, 1)
    
    x_fit = np.logspace(np.log10(min(scale_values)), np.log10(max(scale_values)), 100)
    y_fit = 10**(coeffs[0] * np.log10(x_fit) + coeffs[1])
    
    ax5.plot(x_fit, y_fit, 'r--', linewidth=2, alpha=0.7,
            label=f'Power Law: C ∝ L^{coeffs[0]:.2f}')
    ax5.legend(loc='upper right', fontsize=11, framealpha=0.95)
    
    # Annotation
    textstr = ('Consciousness complexity\nscales as power law\n\n'
              'Finer precision =\nRicher structure')
    props = dict(boxstyle='round', facecolor='yellow', alpha=0.9,
                edgecolor='black', linewidth=2)
    ax5.text(0.02, 0.02, textstr, transform=ax5.transAxes, fontsize=10,
            verticalalignment='bottom', bbox=props, fontweight='bold')
    
    # Panel F: Unified Consciousness Equation
    ax6 = fig.add_subplot(gs[2, 1])
    ax6.axis('off')
    
    # Create equation display
    equations = [
        r'$\mathbf{Consciousness\ Framework}$',
        '',
        r'$\mathcal{C}(x, t, \epsilon) = ||\mathcal{P}(x, t, \epsilon) - \mathcal{T}(x, t, \epsilon)||$',
        '',
        r'$\mathbf{where:}$',
        r'$\mathcal{P}$ = Perception manifold',
        r'$\mathcal{T}$ = Thought manifold',
        r'$\epsilon$ = Precision scale',
        r'$x$ = Spatial coordinates',
        r'$t$ = Time',
        '',
        r'$\mathbf{Scale\ Invariance:}$',
        r'$\mathcal{C}(x, t, \epsilon) \sim \mathcal{C}(x, t, \lambda\epsilon)$',
        '',
        r'$\mathbf{Complexity\ Scaling:}$',
        r'$I(\epsilon) = -\log_2(\epsilon) + C_0$',
        '',
        r'$\mathbf{Heartbeat\ Quantization:}$',
        r'$\Delta t = RR_{interval}$',
        r'$f_{perception} = 1/\tau_{restoration}$',
        '',
        r'$\mathbf{Consciousness\ Measure:}$',
        r'$Q = \frac{|f_{heart} - f_{perception}|}{f_{heart}}$',
        r'$\mathcal{C}_{level} = Q \times HRV$'
    ]
    
    y_pos = 0.95
    for eq in equations:
        if eq == '':
            y_pos -= 0.02
        elif eq.startswith(r'$\mathbf{'):
            # Bold headers
            ax6.text(0.5, y_pos, eq, transform=ax6.transAxes,
                    fontsize=14, ha='center', va='top',
                    bbox=dict(boxstyle='round', facecolor='lightblue',
                             alpha=0.8, edgecolor='black', linewidth=2))
            y_pos -= 0.05
        else:
            # Regular equations
            ax6.text(0.5, y_pos, eq, transform=ax6.transAxes,
                    fontsize=12, ha='center', va='top')
            y_pos -= 0.04
    
    # Add border
    from matplotlib.patches import Rectangle
    rect = Rectangle((0.05, 0.05), 0.9, 0.9, transform=ax6.transAxes,
                     linewidth=3, edgecolor='purple', facecolor='none')
    ax6.add_patch(rect)
    
    ax6.set_title('F: Unified Multi-Scale Consciousness Equations',
                 fontsize=13, fontweight='bold', pad=15)
    
    # Overall title
    fig.suptitle('Multi-Scale Consciousness Atlas: From GPS to Planck Scale',
                fontsize=22, fontweight='bold', y=0.995)
    
    plt.tight_layout()
    return fig

def main():
    print("="*80)
    print("GENERATING MASTER FIGURE 4: MULTI-SCALE CONSCIOUSNESS ATLAS")
    print("="*80)
    
    output_dir = Path('output/master_figures')
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print("\nCreating multi-scale atlas figure...")
    fig = create_multiscale_atlas_figure()
    
    fig.savefig(output_dir / 'master_figure_4_multiscale_atlas.png',
                dpi=300, bbox_inches='tight')
    fig.savefig(output_dir / 'master_figure_4_multiscale_atlas.pdf',
                bbox_inches='tight')
    
    print("✓ Master Figure 4 saved")
    print(f"\nOutput location: {output_dir.absolute()}")
    
    plt.show()

if __name__ == "__main__":
    main()

