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

def calculate_perception_manifold(points, precision_level='raw_gps'):
    """
    Calculate perception manifold from GPS trajectory.
    Perception = spatial awareness + velocity awareness + temporal awareness
    """
    
    level_points = [p for p in points if p['properties']['precision_level'] == precision_level
                   and p['properties']['watch'] == 'Watch 1 (93 points)']
    
    # Extract coordinates and properties
    lons = np.array([p['geometry']['coordinates'][0] for p in level_points])
    lats = np.array([p['geometry']['coordinates'][1] for p in level_points])
    velocities = np.array([p['properties']['velocity_ms'] for p in level_points])
    uncertainties = np.array([p['properties']['position_uncertainty_m'] for p in level_points])
    
    # Normalize to [0, 1] for perception space
    lons_norm = (lons - lons.min()) / (lons.max() - lons.min() + 1e-10)
    lats_norm = (lats - lats.min()) / (lats.max() - lats.min() + 1e-10)
    vels_norm = velocities / (velocities.max() + 1e-10)
    
    # Perception coordinates: (space_x, space_y, velocity)
    perception_coords = np.column_stack([lons_norm, lats_norm, vels_norm])
    
    return perception_coords, lons_norm, lats_norm, vels_norm, velocities, uncertainties

def create_perception_geometry_panel(metadata, precision_levels, points):
    """
    Panel 4: Perception Geometry - How space is perceived during movement.
    Shows the perceptual manifold at different precision scales.
    """
    
    plt.style.use('seaborn-v0_8-whitegrid')
    
    fig = plt.figure(figsize=(22, 14))
    gs = GridSpec(2, 2, figure=fig, hspace=0.35, wspace=0.35)
    
    # Panel A: 3D Perception Manifold (GPS Level)
    ax1 = fig.add_subplot(gs[0, 0], projection='3d')
    
    perc_coords_gps, lons_gps, lats_gps, vels_gps, velocities_gps, unc_gps = \
        calculate_perception_manifold(points, 'raw_gps')
    
    # Color by velocity
    scatter = ax1.scatter(perc_coords_gps[:, 0], perc_coords_gps[:, 1], 
                         perc_coords_gps[:, 2],
                         c=velocities_gps, cmap='viridis', s=100, alpha=0.7,
                         edgecolors='black', linewidth=1)
    
    # Connect points to show trajectory
    ax1.plot(perc_coords_gps[:, 0], perc_coords_gps[:, 1], perc_coords_gps[:, 2],
            'k-', linewidth=1.5, alpha=0.3)
    
    ax1.set_xlabel('Spatial X (normalized)', fontsize=12, fontweight='bold')
    ax1.set_ylabel('Spatial Y (normalized)', fontsize=12, fontweight='bold')
    ax1.set_zlabel('Velocity (normalized)', fontsize=12, fontweight='bold')
    ax1.set_title('A: Perception Manifold (GPS)', fontsize=14, fontweight='bold')
    
    # Add colorbar
    cbar = plt.colorbar(scatter, ax=ax1, pad=0.1, shrink=0.8)
    cbar.set_label('Velocity (m/s)', fontsize=11, fontweight='bold')
    
    # Add note
    textstr = 'Perception =\nSpatial awareness\n+ Motion awareness'
    props = dict(boxstyle='round', facecolor='lightblue', alpha=0.9,
                edgecolor='black', linewidth=2)
    ax1.text2D(0.02, 0.98, textstr, transform=ax1.transAxes, fontsize=10,
              verticalalignment='top', bbox=props, fontweight='bold')
    
    # Panel B: Perception Manifold at Femtosecond Level
    ax2 = fig.add_subplot(gs[0, 1], projection='3d')
    
    perc_coords_fs, lons_fs, lats_fs, vels_fs, velocities_fs, unc_fs = \
        calculate_perception_manifold(points, 'femtosecond')
    
    if len(perc_coords_fs) > 0:
        scatter2 = ax2.scatter(perc_coords_fs[:, 0], perc_coords_fs[:, 1], 
                              perc_coords_fs[:, 2],
                              c=velocities_fs, cmap='plasma', s=100, alpha=0.7,
                              edgecolors='black', linewidth=1)
        
        ax2.plot(perc_coords_fs[:, 0], perc_coords_fs[:, 1], perc_coords_fs[:, 2],
                'k-', linewidth=1.5, alpha=0.3)
        
        cbar2 = plt.colorbar(scatter2, ax=ax2, pad=0.1, shrink=0.8)
        cbar2.set_label('Velocity (m/s)', fontsize=11, fontweight='bold')
    
    ax2.set_xlabel('Spatial X (normalized)', fontsize=12, fontweight='bold')
    ax2.set_ylabel('Spatial Y (normalized)', fontsize=12, fontweight='bold')
    ax2.set_zlabel('Velocity (normalized)', fontsize=12, fontweight='bold')
    ax2.set_title('B: Perception Manifold (Femtosecond)', fontsize=14, fontweight='bold')
    
    textstr = 'Enhanced precision\nreveals finer\nperceptual structure'
    props2 = dict(boxstyle='round', facecolor='#FFFF00', alpha=0.7,
                 edgecolor='black', linewidth=2)
    ax2.text2D(0.02, 0.98, textstr, transform=ax2.transAxes, fontsize=10,
              verticalalignment='top', bbox=props2, fontweight='bold')
    
    # Panel C: Perception Surface Curvature
    ax3 = fig.add_subplot(gs[1, 0])
    
    # Calculate curvature of perception manifold
    # Use 2D projection and calculate local curvature
    
    # Calculate path curvature (change in direction)
    dx = np.diff(lons_gps)
    dy = np.diff(lats_gps)
    
    # Tangent angles
    angles = np.arctan2(dy, dx)
    
    # Curvature = change in angle / distance
    d_angles = np.diff(angles)
    distances = np.sqrt(dx[:-1]**2 + dy[:-1]**2)
    curvatures = np.abs(d_angles) / (distances + 1e-10)
    
    # Extend to match original length
    curvatures_full = np.concatenate([[curvatures[0]], curvatures, [curvatures[-1]]])
    
    # Plot curvature along path
    path_distance = np.cumsum(np.concatenate([[0], np.sqrt(np.diff(lons_gps)**2 + np.diff(lats_gps)**2)]))
    
    ax3.plot(path_distance, curvatures_full, linewidth=2.5, color='#e74c3c', alpha=0.8)
    ax3.fill_between(path_distance, 0, curvatures_full, alpha=0.3, color='#e74c3c')
    
    ax3.set_xlabel('Path Distance (normalized)', fontsize=14, fontweight='bold')
    ax3.set_ylabel('Perception Curvature', fontsize=14, fontweight='bold')
    ax3.set_title('C', fontsize=18, fontweight='bold', loc='left', pad=15)
    ax3.grid(alpha=0.3)
    
    # Mark high curvature regions (turns)
    threshold = np.percentile(curvatures_full, 75)
    high_curv_idx = curvatures_full > threshold
    ax3.scatter(path_distance[high_curv_idx], curvatures_full[high_curv_idx],
               s=100, c='red', marker='o', edgecolors='black', linewidth=2,
               label='High Curvature (Turns)', zorder=5)
    
    ax3.legend(loc='upper right', fontsize=11, framealpha=0.95)
    
    # Add note
    textstr = (f'High curvature =\nSharp turns\n= Attention focus\n\n'
              f'Mean: {np.mean(curvatures_full):.3f}\n'
              f'Max: {np.max(curvatures_full):.3f}')
    ax3.text(0.02, 0.98, textstr, transform=ax3.transAxes, fontsize=10,
            verticalalignment='top', bbox=props, fontweight='bold')
    
    # Panel D: Perception Volume Across Scales
    ax4 = fig.add_subplot(gs[1, 1])
    
    # Calculate perception volume at each precision level
    precision_names = ['raw_gps', 'nanosecond', 'picosecond', 'femtosecond',
                      'attosecond', 'zeptosecond', 'planck', 'trans_planckian']
    
    volumes = []
    uncertainties_mean = []
    
    for prec_name in precision_names:
        perc_coords, _, _, _, _, uncs = calculate_perception_manifold(points, prec_name)
        
        if len(perc_coords) > 3:
            try:
                # Calculate convex hull volume
                hull = ConvexHull(perc_coords)
                volume = hull.volume
            except:
                volume = 0
        else:
            volume = 0
        
        volumes.append(volume)
        uncertainties_mean.append(np.mean(uncs) if len(uncs) > 0 else 0)
    
    # Plot
    labels = ['GPS', 'ns', 'ps', 'fs', 'as', 'zs', 'Planck', 'Trans-P']
    colors = [precision_levels[name]['color'] for name in precision_names]
    
    bars = ax4.bar(labels, volumes, color=colors, alpha=0.8,
                  edgecolor='black', linewidth=2)
    
    ax4.set_ylabel('Perception Volume (normalized)', fontsize=14, fontweight='bold')
    ax4.set_xlabel('Precision Level', fontsize=14, fontweight='bold')
    ax4.set_title('D', fontsize=18, fontweight='bold', loc='left', pad=15)
    ax4.grid(alpha=0.3, axis='y')
    
    # Add values
    for bar, vol in zip(bars, volumes):
        if vol > 0:
            height = bar.get_height()
            ax4.text(bar.get_x() + bar.get_width()/2., height + 0.001,
                    f'{vol:.4f}', ha='center', va='bottom', 
                    fontsize=9, fontweight='bold', rotation=45)
    
    # Add note
    textstr = ('Perception volume\nchanges with\nprecision scale\n\n'
              'Finer precision =\nRicher perceptual\nstructure')
    ax4.text(0.98, 0.98, textstr, transform=ax4.transAxes, fontsize=10,
            verticalalignment='top', horizontalalignment='right',
            bbox=dict(boxstyle='round', facecolor='lightgreen',
                     alpha=0.9, edgecolor='darkgreen', linewidth=2),
            fontweight='bold')
    
    # Overall title
    fig.suptitle('Paper 1: The Geometry of Perception', fontsize=20, fontweight='bold', y=0.995)
    
    plt.tight_layout()
    return fig

def main():
    """Main function."""
    
    data_path = Path('public/comprehensive_gps_multiprecision_20251013_053445.geojson')
    
    print("="*70)
    print("GENERATING PERCEPTION GEOMETRY PANEL")
    print("="*70)
    
    geojson = load_geojson_data(data_path)
    metadata, precision_levels, points = extract_precision_data(geojson)
    
    output_dir = Path('output')
    output_dir.mkdir(exist_ok=True)
    
    print("\nGenerating Panel 4: Perception Geometry...")
    fig = create_perception_geometry_panel(metadata, precision_levels, points)
    fig.savefig(output_dir / 'figure_gps_perception_geometry.png',
                dpi=300, bbox_inches='tight')
    fig.savefig(output_dir / 'figure_gps_perception_geometry.pdf',
                bbox_inches='tight')
    print("✓ Perception Geometry panel saved")
    
    print("\n" + "="*70)
    print("PERCEPTION GEOMETRY COMPLETE")
    print("="*70)
    
    plt.show()

if __name__ == "__main__":
    main()
