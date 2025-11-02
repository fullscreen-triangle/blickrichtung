import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from mpl_toolkits.mplot3d import Axes3D
import seaborn as sns
from pathlib import Path

def create_consciousness_geometry_figure():
    """
    Master Figure 2: Consciousness Geometry
    Shows the geometric structure of consciousness at multiple scales.
    """
    
    plt.style.use('seaborn-v0_8-white')
    
    fig = plt.figure(figsize=(24, 16))
    gs = GridSpec(2, 2, figure=fig, hspace=0.3, wspace=0.3)
    
    # Panel A: Consciousness Manifold (3D Visualization)
    ax1 = fig.add_subplot(gs[0, 0], projection='3d')
    
    # Create consciousness manifold as residual field
    x = np.linspace(-5, 5, 50)
    y = np.linspace(-5, 5, 50)
    X, Y = np.meshgrid(x, y)
    
    # Perception surface (smooth)
    Z_perception = 2 * np.exp(-(X**2 + Y**2) / 10) * np.cos(X) * np.sin(Y)
    
    # Thought surface (discrete, quantum)
    Z_thought = 1.5 * np.exp(-(X**2 + Y**2) / 8) * np.sin(X) * np.cos(Y) + 0.5
    
    # Consciousness = residual
    Z_consciousness = np.abs(Z_perception - Z_thought)
    
    # Plot
    surf = ax1.plot_surface(X, Y, Z_consciousness, cmap='plasma',
                           alpha=0.8, edgecolor='none', vmin=0, vmax=3)
    
    # Add contour lines
    ax1.contour(X, Y, Z_consciousness, levels=10, colors='black',
               alpha=0.3, linewidths=1)
    
    ax1.set_xlabel('Spatial Dimension 1', fontsize=11, fontweight='bold')
    ax1.set_ylabel('Spatial Dimension 2', fontsize=11, fontweight='bold')
    ax1.set_zlabel('Consciousness Intensity', fontsize=11, fontweight='bold')
    ax1.set_title('A: Consciousness Manifold\n|C(x,y)| = ||P(x,y) - T(x,y)||',
                 fontsize=14, fontweight='bold', pad=20)
    
    # Colorbar
    cbar = plt.colorbar(surf, ax=ax1, pad=0.1, shrink=0.8)
    cbar.set_label('Consciousness Intensity', fontsize=10, fontweight='bold')
    
        # Annotation
    ax1.text2D(0.02, 0.98, 'High intensity (red) = Large P-T separation = Strong consciousness',
              transform=ax1.transAxes, fontsize=10, verticalalignment='top',
              bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.8,
                       edgecolor='black', linewidth=2), fontweight='bold')
    
    # Panel B: Consciousness States in Phase Space
    ax2 = fig.add_subplot(gs[0, 1], projection='3d')
    
    # Define consciousness states
    states = {
        'Coma': (0.0, 0.0, 0.0),
        'Deep Sleep': (0.2, 0.3, 0.1),
        'Light Sleep': (0.4, 0.5, 0.3),
        'Drowsy': (0.6, 0.7, 0.5),
        'Alert': (0.8, 0.9, 0.8),
        'Peak Focus': (1.0, 1.0, 1.0)
    }
    
    colors_states = ['#8B0000', '#FF4500', '#FFA500', '#FFD700', '#90EE90', '#00FF00']
    
    # Plot states
    for (state_name, coords), color in zip(states.items(), colors_states):
        x, y, z = coords
        
        # Add some scatter around each state
        n_points = 100
        x_scatter = x + 0.05 * np.random.randn(n_points)
        y_scatter = y + 0.05 * np.random.randn(n_points)
        z_scatter = z + 0.05 * np.random.randn(n_points)
        
        ax2.scatter(x_scatter, y_scatter, z_scatter, c=color, s=30,
                   alpha=0.6, edgecolors='black', linewidth=0.3,
                   label=state_name)
        
        # Mark center
        ax2.scatter([x], [y], [z], c=color, s=300, marker='*',
                   edgecolors='black', linewidth=2, zorder=5)
        
        # Label
        ax2.text(x, y, z + 0.1, state_name, fontsize=9, fontweight='bold',
                ha='center', va='bottom')
    
    # Draw trajectory through states
    state_coords = np.array(list(states.values()))
    ax2.plot(state_coords[:, 0], state_coords[:, 1], state_coords[:, 2],
            'k--', linewidth=2, alpha=0.5, label='State Trajectory')
    
    ax2.set_xlabel('Resonance Quality', fontsize=11, fontweight='bold')
    ax2.set_ylabel('Manifold Distance', fontsize=11, fontweight='bold')
    ax2.set_zlabel('Heartbeat Variability', fontsize=11, fontweight='bold')
    ax2.set_title('B: Consciousness State Space\nFrom Coma to Peak Focus',
                 fontsize=14, fontweight='bold', pad=20)
    ax2.legend(loc='upper left', fontsize=9, framealpha=0.95)
    
    ax2.set_xlim(0, 1.1)
    ax2.set_ylim(0, 1.1)
    ax2.set_zlim(0, 1.1)
    
    # Panel C: Multi-Scale Consciousness Structure
    ax3 = fig.add_subplot(gs[1, 0])
    
    # Create multi-scale visualization
    scales = ['GPS\n(5m)', 'Millimeter\n(1mm)', 'Micrometer\n(1μm)',
             'Nanometer\n(1nm)', 'Picometer\n(1pm)', 'Femtometer\n(1fm)',
             'Planck\n(10⁻³⁵m)']
    
    scale_values = [5, 1e-3, 1e-6, 1e-9, 1e-12, 1e-15, 1.6e-35]
    
    # Consciousness complexity at each scale
    complexity = [1, 10, 100, 1000, 10000, 100000, 1e10]
    
    # Create log-log plot
    ax3.loglog(scale_values, complexity, 'o-', linewidth=3, markersize=12,
              color='#9b59b6', markerfacecolor='#e74c3c', markeredgecolor='black',
              markeredgewidth=2)
    
    # Add labels for each scale
    for i, (scale, sv, comp) in enumerate(zip(scales, scale_values, complexity)):
        ax3.annotate(scale, xy=(sv, comp), xytext=(10, 10),
                    textcoords='offset points', fontsize=9, fontweight='bold',
                    bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.7,
                             edgecolor='black', linewidth=1.5),
                    arrowprops=dict(arrowstyle='->', lw=1.5))
    
    ax3.set_xlabel('Spatial Scale (meters)', fontsize=12, fontweight='bold')
    ax3.set_ylabel('Consciousness Complexity\n(Information Content)', fontsize=12, fontweight='bold')
    ax3.set_title('C: Multi-Scale Consciousness Structure',
                 fontsize=14, fontweight='bold', pad=15)
    ax3.grid(True, alpha=0.3, which='both')
    
    # Add shaded regions
    ax3.axvspan(1e-35, 1e-15, alpha=0.2, color='purple', label='Quantum Scale')
    ax3.axvspan(1e-15, 1e-6, alpha=0.2, color='blue', label='Molecular Scale')
    ax3.axvspan(1e-6, 1, alpha=0.2, color='green', label='Macro Scale')
    
    ax3.legend(loc='upper right', fontsize=10, framealpha=0.95)
    
    # Annotation
    textstr = ('Same geometric structure\nat all scales\n\n'
              'Complexity increases\nwith precision')
    props = dict(boxstyle='round', facecolor='lightblue', alpha=0.9,
                edgecolor='black', linewidth=2)
    ax3.text(0.02, 0.02, textstr, transform=ax3.transAxes, fontsize=10,
            verticalalignment='bottom', bbox=props, fontweight='bold')
    
    # Panel D: Consciousness Topology (Betti Numbers)
    ax4 = fig.add_subplot(gs[1, 1])
    
    # Simulate topological features at different consciousness states
    states_topo = ['Coma', 'Deep\nSleep', 'Light\nSleep', 'Drowsy', 'Alert', 'Peak\nFocus']
    
    # Betti numbers (topological features)
    # β₀ = connected components
    # β₁ = loops/cycles
    # β₂ = voids/cavities
    
    beta_0 = [1, 2, 3, 5, 8, 12]  # Increasing connectivity
    beta_1 = [0, 1, 3, 8, 15, 25]  # Increasing loops
    beta_2 = [0, 0, 1, 3, 8, 15]   # Increasing voids
    
    x = np.arange(len(states_topo))
    width = 0.25
    
    bars1 = ax4.bar(x - width, beta_0, width, label='β₀ (Components)',
                   color='#e74c3c', alpha=0.8, edgecolor='black', linewidth=2)
    bars2 = ax4.bar(x, beta_1, width, label='β₁ (Loops)',
                   color='#3498db', alpha=0.8, edgecolor='black', linewidth=2)
    bars3 = ax4.bar(x + width, beta_2, width, label='β₂ (Voids)',
                   color='#2ecc71', alpha=0.8, edgecolor='black', linewidth=2)
    
    ax4.set_ylabel('Betti Number (Topological Features)', fontsize=12, fontweight='bold')
    ax4.set_xlabel('Consciousness State', fontsize=12, fontweight='bold')
    ax4.set_xticks(x)
    ax4.set_xticklabels(states_topo, fontsize=10, fontweight='bold')
    ax4.set_title('D: Consciousness Topology\nTopological Complexity Increases with Awareness',
                 fontsize=14, fontweight='bold', pad=15)
    ax4.legend(loc='upper left', fontsize=10, framealpha=0.95)
    ax4.grid(alpha=0.3, axis='y')
    
    # Add values on bars
    for bars in [bars1, bars2, bars3]:
        for bar in bars:
            height = bar.get_height()
            if height > 0:
                ax4.text(bar.get_x() + bar.get_width()/2., height + 0.5,
                        f'{int(height)}', ha='center', va='bottom',
                        fontsize=9, fontweight='bold')
    
    # Annotation
    textstr = ('β₀ = Connected components\nβ₁ = Loops/cycles\nβ₂ = Voids/cavities\n\n'
              'Higher consciousness =\nRicher topology')
    ax4.text(0.98, 0.98, textstr, transform=ax4.transAxes, fontsize=10,
            verticalalignment='top', horizontalalignment='right',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.9,
                     edgecolor='black', linewidth=2), fontweight='bold')
    
    # Overall title
    fig.suptitle('Consciousness Geometry: Structure, States, and Topology',
                fontsize=20, fontweight='bold', y=0.98)
    
    plt.tight_layout()
    return fig

def main():
    print("="*80)
    print("GENERATING MASTER FIGURE 2: CONSCIOUSNESS GEOMETRY")
    print("="*80)
    
    output_dir = Path('output/master_figures')
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print("\nCreating consciousness geometry figure...")
    fig = create_consciousness_geometry_figure()
    
    fig.savefig(output_dir / 'master_figure_2_consciousness_geometry.png',
                dpi=300, bbox_inches='tight')
    fig.savefig(output_dir / 'master_figure_2_consciousness_geometry.pdf',
                bbox_inches='tight')
    
    print("✓ Master Figure 2 saved")
    print(f"\nOutput location: {output_dir.absolute()}")
    
    plt.show()

if __name__ == "__main__":
    main()
