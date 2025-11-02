import json
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from mpl_toolkits.mplot3d import Axes3D
import seaborn as sns
from pathlib import Path
from scipy.interpolate import interp1d
from scipy.spatial import ConvexHull

def load_geojson_data(filepath):
    """Load GeoJSON data."""
    with open(filepath, 'r') as f:
        return json.load(f)

def extract_precision_data(geojson):
    """Extract precision levels and point data."""
    metadata = geojson['metadata']
    precision_levels = metadata['precision_levels']
    features = geojson['features']
    
    points = [f for f in features if f['geometry']['type'] == 'Point']
    
    return metadata, precision_levels, points

def calculate_thought_manifold(points, precision_level='raw_gps'):
    """
    Calculate thought manifold from GPS trajectory.
    Thought = planning + prediction + decision-making
    Represented by: acceleration (planning), jerk (prediction), position shifts (decisions)
    """
    
    level_points = [p for p in points if p['properties']['precision_level'] == precision_level
                   and p['properties']['watch'] == 'Watch 1 (93 points)']
    
    # Extract coordinates
    lons = np.array([p['geometry']['coordinates'][0] for p in level_points])
    lats = np.array([p['geometry']['coordinates'][1] for p in level_points])
    velocities = np.array([p['properties']['velocity_ms'] for p in level_points])
    
    # Calculate acceleration (thought as planning)
    accelerations = np.gradient(velocities)
    
    # Calculate jerk (thought as prediction)
    jerks = np.gradient(accelerations)
    
    # Calculate directional changes (thought as decision)
    dx = np.gradient(lons)
    dy = np.gradient(lats)
    direction_changes = np.abs(np.gradient(np.arctan2(dy, dx)))
    
    # Normalize
    accel_norm = (accelerations - accelerations.min()) / (accelerations.max() - accelerations.min() + 1e-10)
    jerk_norm = (jerks - jerks.min()) / (jerks.max() - jerks.min() + 1e-10)
    dirchange_norm = direction_changes / (direction_changes.max() + 1e-10)
    
    # Thought coordinates: (planning, prediction, decision)
    thought_coords = np.column_stack([accel_norm, jerk_norm, dirchange_norm])
    
    return thought_coords, accelerations, jerks, direction_changes, lons, lats

def create_thought_geometry_panel(metadata, precision_levels, points):
    """
    Panel 5: Thought Geometry - How thought manifests in movement planning.
    Shows the cognitive manifold at different precision scales.
    """
    
    plt.style.use('seaborn-v0_8-white')
    
    fig = plt.figure(figsize=(22, 14))
    gs = GridSpec(2, 2, figure=fig, hspace=0.35, wspace=0.35)
    
    # Panel A: 3D Thought Manifold (GPS Level)
    ax1 = fig.add_subplot(gs[0, 0], projection='3d')
    
    thought_coords_gps, accels_gps, jerks_gps, dirchanges_gps, lons_gps, lats_gps = \
        calculate_thought_manifold(points, 'raw_gps')
    
    # Color by jerk (prediction intensity)
    scatter = ax1.scatter(thought_coords_gps[:, 0], thought_coords_gps[:, 1], 
                         thought_coords_gps[:, 2],
                         c=jerks_gps, cmap='coolwarm', s=100, alpha=0.7,
                         edgecolors='black', linewidth=1)
    
    # Connect points
    ax1.plot(thought_coords_gps[:, 0], thought_coords_gps[:, 1], thought_coords_gps[:, 2],
            'k-', linewidth=1.5, alpha=0.3)
    
    ax1.set_xlabel('Planning (acceleration)', fontsize=12, fontweight='bold')
    ax1.set_ylabel('Prediction (jerk)', fontsize=12, fontweight='bold')
    ax1.set_zlabel('Decision (direction change)', fontsize=12, fontweight='bold')
    ax1.set_title('A: Thought Manifold (GPS)', fontsize=14, fontweight='bold')
    
    cbar = plt.colorbar(scatter, ax=ax1, pad=0.1, shrink=0.8)
    cbar.set_label('Jerk (prediction intensity)', fontsize=11, fontweight='bold')
    
    textstr = 'Thought =\nPlanning\n+ Prediction\n+ Decision'
    props = dict(boxstyle='round', facecolor='lightyellow', alpha=0.9,
                edgecolor='black', linewidth=2)
    ax1.text2D(0.02, 0.98, textstr, transform=ax1.transAxes, fontsize=10,
              verticalalignment='top', bbox=props, fontweight='bold')
    
    # Panel B: Thought Manifold at Attosecond Level
    ax2 = fig.add_subplot(gs[0, 1], projection='3d')
    
    thought_coords_as, accels_as, jerks_as, dirchanges_as, lons_as, lats_as = \
        calculate_thought_manifold(points, 'attosecond')
    
    if len(thought_coords_as) > 0:
        scatter2 = ax2.scatter(thought_coords_as[:, 0], thought_coords_as[:, 1], 
                              thought_coords_as[:, 2],
                              c=jerks_as, cmap='twilight', s=100, alpha=0.7,
                              edgecolors='black', linewidth=1)
        
        ax2.plot(thought_coords_as[:, 0], thought_coords_as[:, 1], thought_coords_as[:, 2],
                'k-', linewidth=1.5, alpha=0.3)
        
        cbar2 = plt.colorbar(scatter2, ax=ax2, pad=0.1, shrink=0.8)
        cbar2.set_label('Jerk (prediction intensity)', fontsize=11, fontweight='bold')
    
    ax2.set_xlabel('Planning (acceleration)', fontsize=12, fontweight='bold')
    ax2.set_ylabel('Prediction (jerk)', fontsize=12, fontweight='bold')
    ax2.set_zlabel('Decision (direction change)', fontsize=12, fontweight='bold')
    ax2.set_title('B: Thought Manifold (Attosecond)', fontsize=14, fontweight='bold')
    
    textstr = 'Attosecond precision\nreveals quantum\nthought structure'
    props2 = dict(boxstyle='round', facecolor='#00FF00', alpha=0.7,
                 edgecolor='black', linewidth=2)
    ax2.text2D(0.02, 0.98, textstr, transform=ax2.transAxes, fontsize=10,
              verticalalignment='top', bbox=props2, fontweight='bold')
    
    # Panel C: Thought Complexity Evolution
    ax3 = fig.add_subplot(gs[1, 0])
    
    # Calculate thought complexity as combination of all three dimensions
    thought_complexity = np.sqrt(thought_coords_gps[:, 0]**2 + 
                                thought_coords_gps[:, 1]**2 + 
                                thought_coords_gps[:, 2]**2)
    
    # Time axis (normalized)
    t = np.linspace(0, 1, len(thought_complexity))
    
    ax3.plot(t, thought_complexity, linewidth=2.5, color='#9b59b6', alpha=0.8)
    ax3.fill_between(t, 0, thought_complexity, alpha=0.3, color='#9b59b6')
    
    # Add rolling average
    window = 5
    if len(thought_complexity) > window:
        rolling_avg = np.convolve(thought_complexity, np.ones(window)/window, mode='valid')
        t_rolling = t[:len(rolling_avg)]
        ax3.plot(t_rolling, rolling_avg, linewidth=3.5, color='red',
                label='Trend', alpha=0.9)
    
    ax3.set_xlabel('Normalized Time', fontsize=14, fontweight='bold')
    ax3.set_ylabel('Thought Complexity', fontsize=14, fontweight='bold')
    ax3.set_title('C', fontsize=18, fontweight='bold', loc='left', pad=15)
    ax3.legend(loc='upper right', fontsize=11, framealpha=0.95)
    ax3.grid(alpha=0.3)
    
    # Mark complexity peaks (decision points)
    threshold = np.percentile(thought_complexity, 80)
    peaks_idx = thought_complexity > threshold
    ax3.scatter(t[peaks_idx], thought_complexity[peaks_idx],
               s=150, c='red', marker='*', edgecolors='black', linewidth=2,
               label='Decision Points', zorder=5)
    
    textstr = (f'Complexity peaks =\nDecision moments\n\n'
              f'Mean: {np.mean(thought_complexity):.3f}\n'
              f'Max: {np.max(thought_complexity):.3f}\n'
              f'Decisions: {np.sum(peaks_idx)}')
    ax3.text(0.02, 0.98, textstr, transform=ax3.transAxes, fontsize=10,
            verticalalignment='top', bbox=props, fontweight='bold')
    
    # Panel D: Thought Volume Across Scales
    ax4 = fig.add_subplot(gs[1, 1])
    
    # Calculate thought volume at each precision level
    precision_names = ['raw_gps', 'nanosecond', 'picosecond', 'femtosecond',
                      'attosecond', 'zeptosecond', 'planck', 'trans_planckian']
    
    volumes = []
    complexity_means = []
    
    for prec_name in precision_names:
        thought_coords, _, _, _, _, _ = calculate_thought_manifold(points, prec_name)
        
        if len(thought_coords) > 3:
            try:
                hull = ConvexHull(thought_coords)
                volume = hull.volume
            except:
                volume = 0
            
            complexity = np.sqrt(np.sum(thought_coords**2, axis=1))
            complexity_mean = np.mean(complexity)
        else:
            volume = 0
            complexity_mean = 0
        
        volumes.append(volume)
        complexity_means.append(complexity_mean)
    
    # Plot
    labels = ['GPS', 'ns', 'ps', 'fs', 'as', 'zs', 'Planck', 'Trans-P']
    colors = [precision_levels[name]['color'] for name in precision_names]
    
    x = np.arange(len(labels))
    width = 0.35
    
    ax4_twin = ax4.twinx()
    
    bars1 = ax4.bar(x - width/2, volumes, width, label='Volume',
                   color=colors, alpha=0.8, edgecolor='black', linewidth=2)
    bars2 = ax4_twin.bar(x + width/2, complexity_means, width, label='Complexity',
                        color='gray', alpha=0.6, edgecolor='black', linewidth=2)
    
    ax4.set_ylabel('Thought Volume', fontsize=13, fontweight='bold', color='black')
    ax4_twin.set_ylabel('Mean Complexity', fontsize=13, fontweight='bold', color='gray')
    ax4.set_xticks(x)
    ax4.set_xticklabels(labels, fontsize=11, fontweight='bold', rotation=45, ha='right')
    ax4.set_title('D', fontsize=18, fontweight='bold', loc='left', pad=15)
    ax4.grid(alpha=0.3, axis='y')
    ax4_twin.tick_params(axis='y', labelcolor='gray')
    
    # Add legend
    lines1, labels1 = ax4.get_legend_handles_labels()
    lines2, labels2 = ax4_twin.get_legend_handles_labels()
    ax4.legend(lines1 + lines2, labels1 + labels2, loc='upper left', 
              fontsize=10, framealpha=0.95)
    
    textstr = ('Thought volume\nexpands with\nprecision\n\n'
              'More precision =\nRicher cognitive\nstructure')
    ax4.text(0.98, 0.98, textstr, transform=ax4.transAxes, fontsize=10,
            verticalalignment='top', horizontalalignment='right',
            bbox=dict(boxstyle='round', facecolor='lightcoral',
                     alpha=0.9, edgecolor='darkred', linewidth=2),
            fontweight='bold')
    
    # Overall title
    fig.suptitle('Paper 2: The Geometry of Thought', fontsize=20, fontweight='bold', y=0.995)
    
    plt.tight_layout()
    return fig

def main():
    """Main function."""
    
    data_path = Path('public/comprehensive_gps_multiprecision_20251013_053445.geojson')
    
    print("="*70)
    print("GENERATING THOUGHT GEOMETRY PANEL")
    print("="*70)
    
    geojson = load_geojson_data(data_path)
    metadata, precision_levels, points = extract_precision_data(geojson)
    
    output_dir = Path('output')
    output_dir.mkdir(exist_ok=True)
    
    print("\nGenerating Panel 5: Thought Geometry...")
    fig = create_thought_geometry_panel(metadata, precision_levels, points)
    fig.savefig(output_dir / 'figure_gps_thought_geometry.png',
                dpi=300, bbox_inches='tight')
    fig.savefig(output_dir / 'figure_gps_thought_geometry.pdf',
                bbox_inches='tight')
    print("✓ Thought Geometry panel saved")
    
    print("\n" + "="*70)
    print("THOUGHT GEOMETRY COMPLETE")
    print("="*70)
    
    plt.show()

if __name__ == "__main__":
    main()
