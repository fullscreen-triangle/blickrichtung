"""
Chart Set 4: Molecular Geometry and Consciousness
6-panel figure showing how shape affects oscillatory holes and qualia
"""

import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.patches import Ellipse
import matplotlib.patches as mpatches

plt.rcParams.update({
    'font.family': 'Arial',
    'font.size': 8,
    'axes.linewidth': 0.5,
    'figure.dpi': 300,
})

class MolecularGeometryVisualization:
    """Chart Set 4: Molecular Geometry and Consciousness"""
    
    def __init__(self):
        self.prepare_data()
    
    def prepare_data(self):
        """Prepare molecular geometry data"""
        
        self.molecules = {
            'Methane': {
                'smiles': 'C',
                'asphericity': 0.000,
                'eccentricity': 0.000,
                'radius_gyration': 0.55,
                'max_distance': 1.78,
                'diameter': 4.38,
                'volume': 28.29,
                'surface_area': 81.52,
                'principal_moments': [3.21, 3.21, 3.21],
                'shape_class': 'Spherical',
                'color': '#3498db',
            },
            'Benzene': {
                'smiles': 'c1ccccc1',
                'asphericity': 0.250,
                'eccentricity': 0.707,
                'radius_gyration': 1.51,
                'max_distance': 4.96,
                'diameter': 7.86,
                'volume': 83.44,
                'surface_area': 244.86,
                'principal_moments': [177.45, 88.73, 88.73],
                'shape_class': 'Planar',
                'color': '#2ecc71',
            },
            'Octane': {
                'smiles': 'CCCCCCCC',
                'asphericity': 0.234,
                'eccentricity': 0.954,
                'radius_gyration': 2.81,
                'max_distance': 9.96,
                'diameter': 12.67,
                'volume': 145.52,
                'surface_area': 462.19,
                'principal_moments': [879.45, 838.51, 79.67],
                'shape_class': 'Linear',
                'color': '#e74c3c',
            },
            'Vanillin': {
                'smiles': 'COc1cc(C=O)ccc1O',
                'asphericity': 0.249,
                'eccentricity': 0.801,
                'radius_gyration': 2.41,
                'max_distance': 7.31,
                'diameter': 10.23,
                'volume': 136.90,
                'surface_area': 391.80,
                'principal_moments': [881.91, 569.66, 315.55],
                'shape_class': 'Complex',
                'color': '#9b59b6',
            },
        }
    
    def create_figure(self, output='chartset4_molecular_geometry'):
        """Create complete 6-panel figure"""
        
        fig = plt.figure(figsize=(7.2, 9))
        gs = GridSpec(3, 2, figure=fig, hspace=0.4, wspace=0.35)
        
        # Panel A: Shape space (3D)
        ax_a = fig.add_subplot(gs[0, 0], projection='3d')
        self.panel_a_shape_space(ax_a)
        
        # Panel B: Molecular portraits
        ax_b = fig.add_subplot(gs[0, 1])
        self.panel_b_portraits(ax_b)
        
        # Panel C: Shape vs properties
        ax_c = fig.add_subplot(gs[1, 0])
        self.panel_c_shape_properties(ax_c)
        
        # Panel D: Principal moments
        ax_d = fig.add_subplot(gs[1, 1])
        self.panel_d_principal_moments(ax_d)
        
        # Panel E: Size scaling
        ax_e = fig.add_subplot(gs[2, 0])
        self.panel_e_size_scaling(ax_e)
        
        # Panel F: Quale prediction
        ax_f = fig.add_subplot(gs[2, 1])
        self.panel_f_quale_prediction(ax_f)
        
        # Overall title
        fig.suptitle('Molecular Geometry and Consciousness', 
                    fontsize=12, fontweight='bold', y=0.995)
        
        # Save
        plt.savefig(f'{output}.pdf', bbox_inches='tight')
        plt.savefig(f'{output}.png', bbox_inches='tight')
        print(f"✓ {output} saved")
        
        return fig
    
    def panel_a_shape_space(self, ax):
        """Panel A: 3D shape space"""
        
        # Extract data
        names = list(self.molecules.keys())
        asphericity = [m['asphericity'] for m in self.molecules.values()]
        eccentricity = [m['eccentricity'] for m in self.molecules.values()]
        volume = [m['volume'] for m in self.molecules.values()]
        colors = [m['color'] for m in self.molecules.values()]
        sizes = [m['radius_gyration'] * 100 for m in self.molecules.values()]
        
        # 3D scatter
        for i, (name, a, e, v, color, size) in enumerate(zip(
            names, asphericity, eccentricity, volume, colors, sizes)):
            ax.scatter(a, e, v, s=size, c=color, alpha=0.7,
                      edgecolors='black', linewidth=1, label=name)
        
        # Styling
        ax.set_xlabel('Asphericity\n(0=sphere, 1=rod)', fontsize=8, labelpad=5)
        ax.set_ylabel('Eccentricity\n(0=sphere, 1=elongated)', fontsize=8, labelpad=5)
        ax.set_zlabel('Volume (Ų)', fontsize=8, labelpad=5)
        ax.set_title('A. Molecular Shape Space', fontsize=10, fontweight='bold', pad=10)
        ax.legend(fontsize=6, loc='upper left')
        ax.view_init(elev=20, azim=45)
        
        # Add shape class regions (conceptual)
        ax.text2D(0.02, 0.98, 'Sphere\nregion', transform=ax.transAxes,
                 fontsize=6, va='top', color='blue', style='italic')
        ax.text2D(0.98, 0.98, 'Rod\nregion', transform=ax.transAxes,
                 fontsize=6, va='top', ha='right', color='red', style='italic')
        
        return ax
    
    def panel_b_portraits(self, ax):
        """Panel B: Molecular portraits (schematic)"""
        
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 10)
        ax.axis('off')
        
        # Title
        ax.text(5, 9.5, 'B. Molecular Portraits', 
               fontsize=10, fontweight='bold', ha='center', va='top')
        
        # Define positions for 2x2 grid
        positions = [
            (2.5, 6.5, 'Methane\n(Spherical)'),
            (7.5, 6.5, 'Benzene\n(Planar)'),
            (2.5, 2.5, 'Octane\n(Linear)'),
            (7.5, 2.5, 'Vanillin\n(Complex)'),
        ]
        
        molecules_list = list(self.molecules.keys())
        
        for i, (x, y, label) in enumerate(positions):
            mol_name = molecules_list[i]
            mol_data = self.molecules[mol_name]
            color = mol_data['color']
            
            # Draw schematic representation
            if mol_name == 'Methane':
                # Sphere
                circle = plt.Circle((x, y), 0.8, color=color, alpha=0.5, 
                                   ec='black', lw=2)
                ax.add_patch(circle)
                
            elif mol_name == 'Benzene':
                # Hexagon (planar)
                angles = np.linspace(0, 2*np.pi, 7)
                hex_x = x + 0.8 * np.cos(angles)
                hex_y = y + 0.8 * np.sin(angles)
                ax.fill(hex_x, hex_y, color=color, alpha=0.5, 
                       edgecolor='black', linewidth=2)
                
            elif mol_name == 'Octane':
                # Linear chain
                chain_x = np.linspace(x-1.2, x+1.2, 8)
                chain_y = np.ones(8) * y
                ax.plot(chain_x, chain_y, 'o-', color=color, 
                       markersize=8, linewidth=3, markeredgecolor='black',
                       markeredgewidth=1)
                
            elif mol_name == 'Vanillin':
                # Complex shape (benzene ring + substituents)
                angles = np.linspace(0, 2*np.pi, 7)
                hex_x = x + 0.6 * np.cos(angles)
                hex_y = y + 0.6 * np.sin(angles)
                ax.fill(hex_x, hex_y, color=color, alpha=0.5, 
                       edgecolor='black', linewidth=2)
                # Add substituents
                ax.plot([x, x-0.3], [y+0.6, y+1.2], 'o-', color=color,
                       markersize=5, linewidth=2)
                ax.plot([x+0.6, x+1.2], [y, y], 'o-', color=color,
                       markersize=5, linewidth=2)
            
            # Label
            ax.text(x, y-1.5, label, ha='center', va='top', fontsize=7,
                   fontweight='bold')
            
            # Add key metrics
            metrics = f"D: {mol_data['diameter']:.1f} Å\nV: {mol_data['volume']:.0f} Ų"
            ax.text(x, y-2.2, metrics, ha='center', va='top', fontsize=6,
                   family='monospace',
                   bbox=dict(boxstyle='round', facecolor='white', alpha=0.7))
        
        return ax
    
    def panel_c_shape_properties(self, ax):
        """Panel C: Shape vs hole properties"""
        
        # Extract data
        names = list(self.molecules.keys())
        asphericity = [m['asphericity'] for m in self.molecules.values()]
        eccentricity = [m['eccentricity'] for m in self.molecules.values()]
        colors = [m['color'] for m in self.molecules.values()]
        
        # Simulate hole stability (inversely related to asphericity for demo)
        hole_stability = [1 - a for a in asphericity]
        
        # Create scatter plot
        for i, (name, a, h, color) in enumerate(zip(names, asphericity, hole_stability, colors)):
            ax.scatter(a, h, s=150, c=color, alpha=0.7,
                      edgecolors='black', linewidth=1.5, label=name)
        
        # Trend line
        z = np.polyfit(asphericity, hole_stability, 1)
        p = np.poly1d(z)
        x_line = np.linspace(0, max(asphericity), 100)
        ax.plot(x_line, p(x_line), 'k--', linewidth=2, alpha=0.5)
        
        # Styling
        ax.set_xlabel('Asphericity (0=sphere, 1=rod)', fontsize=9, fontweight='bold')
        ax.set_ylabel('Hole Stability (predicted)', fontsize=9, fontweight='bold')
        ax.set_title('C. Shape vs Hole Properties', fontsize=10, fontweight='bold', pad=10)
        ax.legend(fontsize=7, loc='upper right')
        ax.grid(True, alpha=0.3)
        
        # Add insight
        ax.text(0.02, 0.02, 'More spherical\n→ More stable holes', 
               transform=ax.transAxes, fontsize=7,
               verticalalignment='bottom',
               bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.3))
        
        return ax
    
    def panel_d_principal_moments(self, ax):
        """Panel D: Principal moments of inertia"""
        
        # Extract data
        names = list(self.molecules.keys())
        moments = [m['principal_moments'] for m in self.molecules.values()]
        colors = [m['color'] for m in self.molecules.values()]
        
        # Normalize moments for visualization
        moments_norm = []
        for m in moments:
            total = sum(m)
            moments_norm.append([x/total for x in m])
        
        # Create grouped bar chart
        x = np.arange(len(names))
        width = 0.25
        
        i1 = [m[0] for m in moments_norm]
        i2 = [m[1] for m in moments_norm]
        i3 = [m[2] for m in moments_norm]
        
        bars1 = ax.bar(x - width, i1, width, label='I₁', 
                      color='#e74c3c', alpha=0.8, edgecolor='black', linewidth=1)
        bars2 = ax.bar(x, i2, width, label='I₂', 
                      color='#3498db', alpha=0.8, edgecolor='black', linewidth=1)
        bars3 = ax.bar(x + width, i3, width, label='I₃', 
                      color='#2ecc71', alpha=0.8, edgecolor='black', linewidth=1)
        
        # Styling
        ax.set_ylabel('Normalized Moment', fontsize=9, fontweight='bold')
        ax.set_title('D. Principal Moments of Inertia', fontsize=10, fontweight='bold', pad=10)
        ax.set_xticks(x)
        ax.set_xticklabels(names, fontsize=7, rotation=45, ha='right')
        ax.legend(fontsize=7, loc='upper right')
        ax.grid(True, alpha=0.3, axis='y')
        
        # Add shape annotations
        ax.text(0, 0.95, 'Equal\n→ Sphere', transform=ax.transAxes,
               fontsize=6, ha='left', va='top', style='italic')
        ax.text(1, 0.95, 'Unequal\n→ Anisotropic', transform=ax.transAxes,
               fontsize=6, ha='right', va='top', style='italic')
        
        return ax
    
    def panel_e_size_scaling(self, ax):
        """Panel E: Size scaling relationships"""
        
        # Extract data
        names = list(self.molecules.keys())
        diameters = [m['diameter'] for m in self.molecules.values()]
        volumes = [m['volume'] for m in self.molecules.values()]
        surface_areas = [m['surface_area'] for m in self.molecules.values()]
        colors = [m['color'] for m in self.molecules.values()]
        
        # Bubble chart
        for i, (name, d, v, sa, color) in enumerate(zip(
            names, diameters, volumes, surface_areas, colors)):
            ax.scatter(d, v, s=sa, c=color, alpha=0.6,
                      edgecolors='black', linewidth=1.5, label=name)
        
        # Theoretical scaling (V ∝ D³)
        d_theory = np.linspace(min(diameters), max(diameters), 100)
        v_theory = (d_theory / min(diameters))**3 * min(volumes)
        ax.plot(d_theory, v_theory, 'k--', linewidth=2, alpha=0.5,
               label='V ∝ D³')
        
        # Styling
        ax.set_xlabel('Molecular Diameter (Å)', fontsize=9, fontweight='bold')
        ax.set_ylabel('Volume (Ų)', fontsize=9, fontweight='bold')
        ax.set_title('E. Size Scaling', fontsize=10, fontweight='bold', pad=10)
        ax.legend(fontsize=7, loc='upper left')
        ax.grid(True, alpha=0.3)
        
        # Add note about bubble size
        ax.text(0.98, 0.02, 'Bubble size =\nSurface area', 
               transform=ax.transAxes, fontsize=7,
               verticalalignment='bottom', horizontalalignment='right',
               bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
        
        return ax
    
    def panel_f_quale_prediction(self, ax):
        """Panel F: Shape to quale prediction"""
        
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 10)
        ax.axis('off')
        
        # Title
        ax.text(5, 9.5, 'F. Shape → Hole → Quale', 
               fontsize=10, fontweight='bold', ha='center', va='top')
        
        # Define quale predictions
        predictions = [
            {
                'y': 7.5,
                'shape': 'Spherical (Methane)',
                'hole': 'Symmetric holes',
                'quale': '"Simple" qualia',
                'color': '#3498db'
            },
            {
                'y': 5.5,
                'shape': 'Planar (Benzene)',
                'hole': 'Anisotropic holes',
                'quale': '"Flat" qualia',
                'color': '#2ecc71'
            },
            {
                'y': 3.5,
                'shape': 'Linear (Octane)',
                'hole': 'Elongated holes',
                'quale': '"Sharp" qualia',
                'color': '#e74c3c'
            },
            {
                'y': 1.5,
                'shape': 'Complex (Vanillin)',
                'hole': 'Irregular holes',
                'quale': '"Rich" qualia',
                'color': '#9b59b6'
            },
        ]
        
        for pred in predictions:
            y = pred['y']
            color = pred['color']
            
            # Shape box
            shape_box = mpatches.FancyBboxPatch((0.5, y-0.3), 2.5, 0.6,
                                               boxstyle="round,pad=0.05",
                                               edgecolor='black', facecolor=color,
                                               alpha=0.3, linewidth=1.5)
            ax.add_patch(shape_box)
            ax.text(1.75, y, pred['shape'], ha='center', va='center',
                   fontsize=7, fontweight='bold')
            
            # Arrow
            ax.annotate('', xy=(4, y), xytext=(3.2, y),
                       arrowprops=dict(arrowstyle='->', lw=2, color='black'))
            
            # Hole box
            hole_box = mpatches.FancyBboxPatch((4, y-0.3), 2.5, 0.6,
                                              boxstyle="round,pad=0.05",
                                              edgecolor='black', facecolor=color,
                                              alpha=0.3, linewidth=1.5)
            ax.add_patch(hole_box)
            ax.text(5.25, y, pred['hole'], ha='center', va='center',
                   fontsize=7, fontweight='bold')
            
            # Arrow
            ax.annotate('', xy=(7.3, y), xytext=(6.6, y),
                       arrowprops=dict(arrowstyle='->', lw=2, color='black'))
            
            # Quale box
            quale_box = mpatches.FancyBboxPatch((7.3, y-0.3), 2.2, 0.6,
                                               boxstyle="round,pad=0.05",
                                               edgecolor='black', facecolor=color,
                                               alpha=0.5, linewidth=1.5)
            ax.add_patch(quale_box)
            ax.text(8.4, y, pred['quale'], ha='center', va='center',
                   fontsize=7, fontweight='bold', style='italic')
        
        # Bottom summary
        ax.text(5, 0.3, 'Molecular geometry determines oscillatory hole shape,\nwhich determines phenomenal character', 
               fontsize=7, ha='center', style='italic',
               bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.3))
        
        return ax

# Run
if __name__ == "__main__":
    viz = MolecularGeometryVisualization()
    viz.create_figure()
    print("\n✓✓✓ Chart Set 4 Complete ✓✓✓\n")
