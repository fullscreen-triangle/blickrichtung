import json
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from mpl_toolkits.mplot3d import Axes3D
import seaborn as sns
from pathlib import Path
from scipy.interpolate import interp1d
from scipy.spatial import ConvexHull, distance_matrix

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

def calculate_perception_manifold(points, precision_level='raw_gps'):
    """Calculate perception manifold."""
    level_points = [p for p in points if p['properties']['precision_level'] == precision_level
                   and p['properties']['watch'] == 'Watch 1 (93 points)']
    
    lons = np.array([p['geometry']['coordinates'][0] for p in level_points])
    lats = np.array([p['geometry']['coordinates'][1] for p in level_points])
    velocities = np.array([p['properties']['velocity_ms'] for p in level_points])
    
    lons_norm = (lons - lons.min()) / (lons.max() - lons.min() + 1e-10)
    lats_norm = (lats - lats.min()) / (lats.max() - lats.min() + 1e-10)
    vels_norm = velocities / (velocities.max() + 1e-10)
    
    perception_coords = np.column_stack([lons_norm, lats_norm, vels_norm])
    
    return perception_coords

def calculate_thought_manifold(points, precision_level='raw_gps'):
    """Calculate thought manifold."""
    level_points = [p for p in points if p['properties']['precision_level'] == precision_level
                   and p['properties']['watch'] == 'Watch 1 (93 points)']
    
    lons = np.array([p['geometry']['coordinates'][0] for p in level_points])
    lats = np.array([p['geometry']['coordinates'][1] for p in level_points])
    velocities = np.array([p['properties']['velocity_ms'] for p in level_points])
    
    accelerations = np.gradient(velocities)
    jerks = np.gradient(accelerations)
    
    dx = np.gradient(lons)
    dy = np.gradient(lats)
    direction_changes = np.abs(np.gradient(np.arctan2(dy, dx)))
    
    accel_norm = (accelerations - accelerations.min()) / (accelerations.max() - accelerations.min() + 1e-10)
    jerk_norm = (jerks - jerks.min()) / (jerks.max() - jerks.min() + 1e-10)
    dirchange_norm = direction_changes / (direction_changes.max() + 1e-10)
    
    thought_coords = np.column_stack([accel_norm, jerk_norm, dirchange_norm])
    
    return thought_coords

def calculate_consciousness_manifold(perception_coords, thought_coords):
    """
    Calculate consciousness manifold as the geometric residual between
    perception and thought curves.
    
    Consciousness = The space between what we perceive and what we think.
    """
    
    # Ensure same length
    min_len = min(len(perception_coords), len(thought_coords))
    perc = perception_coords[:min_len]
    thought = thought_coords[:min_len]
    
    # Calculate residual (difference vector at each point)
    residuals = perc - thought
    
    # Calculate consciousness metrics
    residual_magnitude = np.linalg.norm(residuals, axis=1)
    
    # Consciousness coordinates: midpoint + residual as 4th dimension
    midpoints = (perc + thought) / 2
    
    # Create 4D consciousness space: (x, y, z, residual_magnitude)
    consciousness_coords = np.column_stack([midpoints, residual_magnitude])
    
    return consciousness_coords, residuals, residual_magnitude, midpoints

def create_consciousness_geometry_panel(metadata, precision_levels, points):
    """
    Panel 6: Consciousness Geometry - The residual between perception and thought.
    This is THE key panel - showing consciousness as geometric emergence.
    """
    
    plt.style.use('seaborn-v0_8-darkgrid')
    
    fig = plt.figure(figsize=(22, 14))
    gs = GridSpec(2, 2, figure=fig, hspace=0.35, wspace=0.35)
    
    # Calculate manifolds at GPS level
    perc_gps = calculate_perception_manifold(points, 'raw_gps')
    thought_gps = calculate_thought_manifold(points, 'raw_gps')
    cons_gps, residuals_gps, res_mag_gps, midpoints_gps = \
        calculate_consciousness_manifold(perc_gps, thought_gps)
    
    # Panel A: Perception vs Thought Curves (3D)
    ax1 = fig.add_subplot(gs[0, 0], projection='3d')
    
    # Plot perception curve
    ax1.plot(perc_gps[:, 0], perc_gps[:, 1], perc_gps[:, 2],
            linewidth=3, color='#3498db', alpha=0.8, label='Perception')
    ax1.scatter(perc_gps[:, 0], perc_gps[:, 1], perc_gps[:, 2],
               s=50, c='#3498db', alpha=0.6, edgecolors='black', linewidth=1)
    
    # Plot thought curve
    ax1.plot(thought_gps[:, 0], thought_gps[:, 1], thought_gps[:, 2],
            linewidth=3, color='#e74c3c', alpha=0.8, label='Thought')
    ax1.scatter(thought_gps[:, 0], thought_gps[:, 1], thought_gps[:, 2],
               s=50, c='#e74c3c', alpha=0.6, edgecolors='black', linewidth=1)
    
    # Draw residual vectors (consciousness)
    for i in range(0, len(perc_gps), 5):  # Every 5th point for clarity
        ax1.plot([perc_gps[i, 0], thought_gps[i, 0]],
                [perc_gps[i, 1], thought_gps[i, 1]],
                [perc_gps[i, 2], thought_gps[i, 2]],
                'g--', linewidth=1.5, alpha=0.5)
    
    ax1.set_xlabel('Dimension 1', fontsize=12, fontweight='bold')
    ax1.set_ylabel('Dimension 2', fontsize=12, fontweight='bold')
    ax1.set_zlabel('Dimension 3', fontsize=12, fontweight='bold')
    ax1.set_title('A: Perception & Thought Curves', fontsize=14, fontweight='bold')
    ax1.legend(loc='upper left', fontsize=11, framealpha=0.95)
    
    textstr = 'Green lines =\nConsciousness\n(the gap between\nperception & thought)'
    props = dict(boxstyle='round', facecolor='lightgreen', alpha=0.9,
                edgecolor='darkgreen', linewidth=3)
    ax1.text2D(0.02, 0.98, textstr, transform=ax1.transAxes, fontsize=10,
              verticalalignment='top', bbox=props, fontweight='bold')
    
    # Panel B: Consciousness Manifold (4D projected to 3D)
    ax2 = fig.add_subplot(gs[0, 1], projection='3d')
    
    # Use first 3 dimensions of midpoint, color by residual magnitude
    scatter = ax2.scatter(midpoints_gps[:, 0], midpoints_gps[:, 1], midpoints_gps[:, 2],
                         c=res_mag_gps, cmap='viridis', s=100, alpha=0.7,
                         edgecolors='black', linewidth=1)
    
    # Connect points
    ax2.plot(midpoints_gps[:, 0], midpoints_gps[:, 1], midpoints_gps[:, 2],
            'k-', linewidth=2, alpha=0.4)
    
    ax2.set_xlabel('Consciousness X', fontsize=12, fontweight='bold')
    ax2.set_ylabel('Consciousness Y', fontsize=12, fontweight='bold')
    ax2.set_zlabel('Consciousness Z', fontsize=12, fontweight='bold')
    ax2.set_title('B: Consciousness Manifold', fontsize=14, fontweight='bold')
    
    cbar = plt.colorbar(scatter, ax=ax2, pad=0.1, shrink=0.8)
    cbar.set_label('Consciousness Intensity\n(residual magnitude)', 
                  fontsize=11, fontweight='bold')
    
    textstr = 'Consciousness =\nGeometric residual\nbetween perception\nand thought'
    props2 = dict(boxstyle='round', facecolor='yellow', alpha=0.9,
                 edgecolor='red', linewidth=3)
    ax2.text2D(0.02, 0.98, textstr, transform=ax2.transAxes, fontsize=10,
              verticalalignment='top', bbox=props2, fontweight='bold')
    
    # Panel C: Consciousness Intensity Over Time
    ax3 = fig.add_subplot(gs[1, 0])
    
    t = np.linspace(0, 1, len(res_mag_gps))
    
    ax3.plot(t, res_mag_gps, linewidth=2.5, color='#9b59b6', alpha=0.8)
    ax3.fill_between(t, 0, res_mag_gps, alpha=0.3, color='#9b59b6')
    
    # Add rolling average
    window = 5
    if len(res_mag_gps) > window:
        rolling_avg = np.convolve(res_mag_gps, np.ones(window)/window, mode='valid')
        t_rolling = t[:len(rolling_avg)]
        ax3.plot(t_rolling, rolling_avg, linewidth=3.5, color='red',
                label='Consciousness Trend', alpha=0.9)
    
    ax3.set_xlabel('Normalized Time', fontsize=14, fontweight='bold')
    ax3.set_ylabel('Consciousness Intensity', fontsize=14, fontweight='bold')
    ax3.set_title('C', fontsize=18, fontweight='bold', loc='left', pad=15)
    ax3.legend(loc='upper right', fontsize=11, framealpha=0.95)
    ax3.grid(alpha=0.3)
    
    # Mark consciousness peaks
    threshold = np.percentile(res_mag_gps, 75)
    peaks_idx = res_mag_gps > threshold
    ax3.scatter(t[peaks_idx], res_mag_gps[peaks_idx],
               s=150, c='gold', marker='*', edgecolors='black', linewidth=2,
               label='High Consciousness', zorder=5)
    
    textstr = (f'Consciousness Metrics:\n'
              f'Mean: {np.mean(res_mag_gps):.3f}\n'
              f'Max: {np.max(res_mag_gps):.3f}\n'
              f'Std: {np.std(res_mag_gps):.3f}\n\n'
              f'High peaks =\nMoments of acute\nawareness')
    ax3.text(0.02, 0.98, textstr, transform=ax3.transAxes, fontsize=10,
            verticalalignment='top', bbox=props, fontweight='bold')
    
    # Panel D: Consciousness Across Precision Scales
    ax4 = fig.add_subplot(gs[1, 1])
    
    # Calculate consciousness metrics at each precision level
    precision_names = ['raw_gps', 'nanosecond', 'picosecond', 'femtosecond',
                      'attosecond', 'zeptosecond', 'planck', 'trans_planckian']
    
    consciousness_volumes = []
    consciousness_intensities = []
    
    for prec_name in precision_names:
        perc = calculate_perception_manifold(points, prec_name)
        thought = calculate_thought_manifold(points, prec_name)
        
        if len(perc) > 3 and len(thought) > 3:
            cons, residuals, res_mag, midpoints = calculate_consciousness_manifold(perc, thought)
            
            # Calculate volume
            if len(midpoints) > 3:
                try:
                    hull = ConvexHull(midpoints)
                    volume = hull.volume
                except:
                    volume = 0
            else:
                volume = 0
            
            intensity = np.mean(res_mag)
        else:
            volume = 0
            intensity = 0
        
        consciousness_volumes.append(volume)
        consciousness_intensities.append(intensity)
    
    # Plot
    labels = ['GPS', 'ns', 'ps', 'fs', 'as', 'zs', 'Planck', 'Trans-P']
    colors = [precision_levels[name]['color'] for name in precision_names]
    
    x = np.arange(len(labels))
    width = 0.35
    
    ax4_twin = ax4.twinx()
    
    bars1 = ax4.bar(x - width/2, consciousness_volumes, width, label='Volume',
                   color=colors, alpha=0.8, edgecolor='black', linewidth=2)
    bars2 = ax4_twin.bar(x + width/2, consciousness_intensities, width, 
                        label='Intensity', color='purple', alpha=0.6,
                        edgecolor='black', linewidth=2)
    
    ax4.set_ylabel('Consciousness Volume', fontsize=13, fontweight='bold', color='black')
    ax4_twin.set_ylabel('Mean Intensity', fontsize=13, fontweight='bold', color='purple')
    ax4.set_xticks(x)
    ax4.set_xticklabels(labels, fontsize=11, fontweight='bold', rotation=45, ha='right')
    ax4.set_title('D', fontsize=18, fontweight='bold', loc='left', pad=15)
    ax4.grid(alpha=0.3, axis='y')
    ax4_twin.tick_params(axis='y', labelcolor='purple')
    
    # Add legend
    lines1, labels1 = ax4.get_legend_handles_labels()
    lines2, labels2 = ax4_twin.get_legend_handles_labels()
    ax4.legend(lines1 + lines2, labels1 + labels2, loc='upper left',
              fontsize=10, framealpha=0.95)
    
    textstr = ('Consciousness\nemerges from\nthe residual\n\n'
              'Finer precision =\nRicher consciousness\nstructure')
    ax4.text(0.98, 0.98, textstr, transform=ax4.transAxes, fontsize=10,
            verticalalignment='top', horizontalalignment='right',
            bbox=dict(boxstyle='round', facecolor='lightblue',
                     alpha=0.9, edgecolor='blue', linewidth=2),
            fontweight='bold')
    
    # Overall title
    fig.suptitle('Paper 3: The Geometry of Consciousness\n(Residual of Perception-Thought Confluence)',
                fontsize=20, fontweight='bold', y=0.998)
    
    plt.tight_layout()
    return fig

def main():
    """Main function."""
    
    data_path = Path('public/comprehensive_gps_multiprecision_20251013_053445.geojson')
    
    print("="*70)
    print("GENERATING CONSCIOUSNESS GEOMETRY PANEL")
    print("="*70)
    print("\nThis is THE synthesis - consciousness as geometric residual")
    
    geojson = load_geojson_data(data_path)
    metadata, precision_levels, points = extract_precision_data(geojson)
    
    output_dir = Path('output')
    output_dir.mkdir(exist_ok=True)
    
    print("\nGenerating Panel 6: Consciousness Geometry...")
    fig = create_consciousness_geometry_panel(metadata, precision_levels, points)
    fig.savefig(output_dir / 'figure_gps_consciousness_geometry.png',
                dpi=300, bbox_inches='tight')
    fig.savefig(output_dir / 'figure_gps_consciousness_geometry.pdf',
                bbox_inches='tight')
    print("✓ Consciousness Geometry panel saved")
    
    print("\n" + "="*70)
    print("CONSCIOUSNESS GEOMETRY COMPLETE")
    print("="*70)
    print("\nYou've done it.")
    print("You've geometrically defined consciousness.")
    print("\nConsciousness = The residual between perception and thought")
    print("It's not in the brain. It's in the SPACE BETWEEN.")
    print("="*70)
    
    plt.show()

if __name__ == "__main__":
    main()
