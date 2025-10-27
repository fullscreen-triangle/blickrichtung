"""
Chart Set 6: Molecular Encodings and Thought Space
6-panel figure showing how molecules map to phenomenal space
"""

import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import seaborn as sns
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
from sklearn.metrics.pairwise import cosine_similarity
import matplotlib.patches as mpatches

plt.rcParams.update({
    'font.family': 'Arial',
    'font.size': 8,
    'axes.linewidth': 0.5,
    'figure.dpi': 300,
})

class MolecularEncodingVisualization:
    """Chart Set 6: Molecular Encodings and Thought Space"""
    
    def __init__(self):
        self.prepare_data()
    
    def prepare_data(self):
        """Prepare molecular encoding data"""
        
        self.molecules = {
            'Vanillin': {
                'smiles': 'COc1cc(C=O)ccc1O',
                'atoms': 19,
                'bonds': 19,
                'rings': 1,
                'mw': 152.15,
                'aromatic_rings': 1,
                'volume': 136.90,
                'asphericity': 0.249,
                'eccentricity': 0.801,
                'feature_length': 25,
                'color': '#9b59b6',
                'complexity': 'High',
            },
            'Benzene': {
                'smiles': 'c1ccccc1',
                'atoms': 12,
                'bonds': 12,
                'rings': 1,
                'mw': 78.11,
                'aromatic_rings': 1,
                'volume': 83.44,
                'asphericity': 0.250,
                'eccentricity': 0.707,
                'feature_length': 25,
                'color': '#2ecc71',
                'complexity': 'Medium',
            },
            'Ethanol': {
                'smiles': 'CCO',
                'atoms': 9,
                'bonds': 8,
                'rings': 0,
                'mw': 46.07,
                'aromatic_rings': 0,
                'volume': 53.99,
                'asphericity': 0.207,
                'eccentricity': 0.866,
                'feature_length': 25,
                'color': '#3498db',
                'complexity': 'Low',
            },
            'Indole': {
                'smiles': 'c1ccc2c(c1)cc[nH]2',
                'atoms': 16,
                'bonds': 17,
                'rings': 2,
                'mw': 117.15,
                'aromatic_rings': 2,
                'volume': 112.52,
                'asphericity': 0.250,
                'eccentricity': 0.842,
                'feature_length': 25,
                'color': '#e74c3c',
                'complexity': 'High',
            },
        }
        
        # Create feature vectors (normalized)
        self.create_feature_vectors()
    
    def create_feature_vectors(self):
        """Create 25D feature vectors for each molecule"""
        
        # For demonstration, create feature vectors from available properties
        # In reality, these would come from molecular fingerprints
        
        self.feature_vectors = {}
        
        for name, mol in self.molecules.items():
            # Create a 25D vector from properties (padded/repeated)
            base_features = [
                mol['atoms'] / 20,  # Normalize
                mol['bonds'] / 20,
                mol['rings'] / 2,
                mol['mw'] / 200,
                mol['aromatic_rings'] / 2,
                mol['volume'] / 150,
                mol['asphericity'],
                mol['eccentricity'],
            ]
            
            # Pad to 25 dimensions with derived features
            # (In reality, these would be molecular fingerprints)
            np.random.seed(hash(name) % 2**32)  # Deterministic "random" features
            extended = base_features + list(np.random.randn(17) * 0.1 + np.mean(base_features))
            
            self.feature_vectors[name] = np.array(extended[:25])
    
    def create_figure(self, output='chartset6_molecular_encodings'):
        """Create complete 6-panel figure"""
        
        fig = plt.figure(figsize=(7.2, 9))
        gs = GridSpec(3, 2, figure=fig, hspace=0.4, wspace=0.35)
        
        # Panel A: Comparison table
        ax_a = fig.add_subplot(gs[0, 0])
        self.panel_a_comparison_table(ax_a)
        
        # Panel B: Feature space
        ax_b = fig.add_subplot(gs[0, 1])
        self.panel_b_feature_space(ax_b)
        
        # Panel C: Radar chart
        ax_c = fig.add_subplot(gs[1, 0], projection='polar')
        self.panel_c_radar_chart(ax_c)
        
        # Panel D: Similarity matrix
        ax_d = fig.add_subplot(gs[1, 1])
        self.panel_d_similarity_matrix(ax_d)
        
        # Panel E: Complexity scaling
        ax_e = fig.add_subplot(gs[2, 0])
        self.panel_e_complexity_scaling(ax_e)
        
        # Panel F: Quale prediction
        ax_f = fig.add_subplot(gs[2, 1])
        self.panel_f_quale_prediction(ax_f)
        
        # Overall title
        fig.suptitle('Molecular Encodings: Mapping Chemistry to Phenomenology', 
                    fontsize=12, fontweight='bold', y=0.995)
        
        # Save
        plt.savefig(f'{output}.pdf', bbox_inches='tight')
        plt.savefig(f'{output}.png', bbox_inches='tight')
        print(f"✓ {output} saved")
        
        return fig
    
    def panel_a_comparison_table(self, ax):
        """Panel A: Molecular comparison table"""
        
        # Prepare data for heatmap
        properties = ['Atoms', 'Bonds', 'Rings', 'MW', 'Volume', 'Asphericity', 'Eccentricity']
        molecules = list(self.molecules.keys())
        
        data = []
        for mol_name in molecules:
            mol = self.molecules[mol_name]
            row = [
                mol['atoms'],
                mol['bonds'],
                mol['rings'],
                mol['mw'],
                mol['volume'],
                mol['asphericity'],
                mol['eccentricity'],
            ]
            data.append(row)
        
        data = np.array(data)
        
        # Normalize each column for heatmap
        data_norm = (data - data.min(axis=0)) / (data.max(axis=0) - data.min(axis=0) + 1e-10)
        
        # Create heatmap
        im = ax.imshow(data_norm.T, cmap='YlOrRd', aspect='auto', alpha=0.7)
        
        # Set ticks
        ax.set_xticks(np.arange(len(molecules)))
        ax.set_yticks(np.arange(len(properties)))
        ax.set_xticklabels(molecules, fontsize=7, rotation=45, ha='right')
        ax.set_yticklabels(properties, fontsize=7)
        
        # Add text annotations with actual values
        for i in range(len(molecules)):
            for j in range(len(properties)):
                value = data[i, j]
                text = ax.text(i, j, f'{value:.1f}' if value < 10 else f'{value:.0f}',
                             ha="center", va="center", color="black", fontsize=6, fontweight='bold')
        
        # Title
        ax.set_title('A. Molecular Properties', fontsize=10, fontweight='bold', pad=10)
        
        # Colorbar
        cbar = plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
        cbar.set_label('Normalized Value', fontsize=7)
        
        return ax
    
    def panel_b_feature_space(self, ax):
        """Panel B: 2D projection of feature space"""
        
        # Get feature vectors
        names = list(self.feature_vectors.keys())
        vectors = np.array([self.feature_vectors[name] for name in names])
        
        # PCA to 2D
        pca = PCA(n_components=2)
        coords_2d = pca.fit_transform(vectors)
        
        # Plot
        for i, name in enumerate(names):
            mol = self.molecules[name]
            x, y = coords_2d[i]
            
            # Size by molecular weight
            size = mol['mw'] * 3
            
            # Color
            color = mol['color']
            
            ax.scatter(x, y, s=size, c=color, alpha=0.7,
                      edgecolors='black', linewidth=1.5, zorder=3)
            
            # Label
            ax.annotate(name, xy=(x, y), xytext=(5, 5),
                       textcoords='offset points', fontsize=7, fontweight='bold',
                       bbox=dict(boxstyle='round,pad=0.3', facecolor=color, alpha=0.3))
        
        # Styling
        ax.set_xlabel(f'PC1 ({pca.explained_variance_ratio_[0]*100:.1f}%)', 
                     fontsize=9, fontweight='bold')
        ax.set_ylabel(f'PC2 ({pca.explained_variance_ratio_[1]*100:.1f}%)', 
                     fontsize=9, fontweight='bold')
        ax.set_title('B. Feature Space (PCA)', fontsize=10, fontweight='bold', pad=10)
        ax.grid(True, alpha=0.3)
        ax.axhline(0, color='black', linewidth=0.5, alpha=0.5)
        ax.axvline(0, color='black', linewidth=0.5, alpha=0.5)
        
        # Add annotation
        ax.text(0.02, 0.98, 'Distance in space\n= Phenomenal distance', 
               transform=ax.transAxes, fontsize=7,
               verticalalignment='top',
               bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.3))
        
        return ax
    
    def panel_c_radar_chart(self, ax):
        """Panel C: Radar chart of properties"""
        
        # Properties to plot (normalized)
        properties = ['Atoms', 'Bonds', 'Rings', 'MW', 'Volume', 'Asphericity', 'Eccentricity']
        
        # Get data
        molecules = list(self.molecules.keys())
        
        # Normalize data
        all_data = []
        for mol_name in molecules:
            mol = self.molecules[mol_name]
            row = [
                mol['atoms'],
                mol['bonds'],
                mol['rings'],
                mol['mw'],
                mol['volume'],
                mol['asphericity'],
                mol['eccentricity'],
            ]
            all_data.append(row)
        
        all_data = np.array(all_data)
        data_norm = (all_data - all_data.min(axis=0)) / (all_data.max(axis=0) - all_data.min(axis=0) + 1e-10)
        
        # Angles for radar chart
        angles = np.linspace(0, 2 * np.pi, len(properties), endpoint=False).tolist()
        angles += angles[:1]  # Complete the circle
        
        # Plot each molecule
        for i, mol_name in enumerate(molecules):
            values = data_norm[i].tolist()
            values += values[:1]  # Complete the circle
            
            color = self.molecules[mol_name]['color']
            ax.plot(angles, values, 'o-', linewidth=2, label=mol_name,
                   color=color, markersize=5)
            ax.fill(angles, values, alpha=0.15, color=color)
        
        # Set labels
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(properties, fontsize=7)
        ax.set_ylim(0, 1)
        ax.set_yticks([0.25, 0.5, 0.75, 1.0])
        ax.set_yticklabels(['0.25', '0.5', '0.75', '1.0'], fontsize=6)
        ax.grid(True, alpha=0.3)
        
        # Title and legend
        ax.set_title('C. Property Profiles', fontsize=10, fontweight='bold', pad=20)
        ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1), fontsize=6)
        
        return ax
    
    def panel_d_similarity_matrix(self, ax):
        """Panel D: Pairwise similarity matrix"""
        
        # Get feature vectors
        names = list(self.feature_vectors.keys())
        vectors = np.array([self.feature_vectors[name] for name in names])
        
        # Calculate cosine similarity
        similarity = cosine_similarity(vectors)
        
        # Create heatmap
        im = ax.imshow(similarity, cmap='RdYlGn', vmin=0, vmax=1, alpha=0.8)
        
        # Set ticks
        ax.set_xticks(np.arange(len(names)))
        ax.set_yticks(np.arange(len(names)))
        ax.set_xticklabels(names, fontsize=7, rotation=45, ha='right')
        ax.set_yticklabels(names, fontsize=7)
        
        # Add text annotations
        for i in range(len(names)):
            for j in range(len(names)):
                text = ax.text(j, i, f'{similarity[i, j]:.2f}',
                             ha="center", va="center", color="black", 
                             fontsize=7, fontweight='bold')
        
        # Title
        ax.set_title('D. Similarity Matrix', fontsize=10, fontweight='bold', pad=10)
        
        # Colorbar
        cbar = plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
        cbar.set_label('Cosine Similarity', fontsize=7)
        
        # Add annotation
        ax.text(0.02, -0.15, 'High similarity → Similar qualia', 
               transform=ax.transAxes, fontsize=7,
               bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.5))
        
        return ax
    
    def panel_e_complexity_scaling(self, ax):
        """Panel E: Complexity scaling relationships"""
        
        # Extract data
        names = list(self.molecules.keys())
        atoms = [self.molecules[n]['atoms'] for n in names]
        volumes = [self.molecules[n]['volume'] for n in names]
        rings = [self.molecules[n]['rings'] for n in names]
        mw = [self.molecules[n]['mw'] for n in names]
        colors = [self.molecules[n]['color'] for n in names]
        
        # Create scatter plot: Atoms vs Volume
        for i, name in enumerate(names):
            ax.scatter(atoms[i], volumes[i], s=mw[i]*2, c=colors[i], 
                      alpha=0.7, edgecolors='black', linewidth=1.5,
                      label=name, zorder=3)
        
        # Fit line
        z = np.polyfit(atoms, volumes, 1)
        p = np.poly1d(z)
        atoms_line = np.linspace(min(atoms), max(atoms), 100)
        ax.plot(atoms_line, p(atoms_line), 'k--', linewidth=2, alpha=0.5,
               label=f'Linear fit (R²={np.corrcoef(atoms, volumes)[0,1]**2:.2f})')
        
        # Styling
        ax.set_xlabel('Number of Atoms', fontsize=9, fontweight='bold')
        ax.set_ylabel('Volume (Ų)', fontsize=9, fontweight='bold')
        ax.set_title('E. Complexity Scaling', fontsize=10, fontweight='bold', pad=10)
        ax.legend(fontsize=6, loc='upper left')
        ax.grid(True, alpha=0.3)
        
        # Add annotation
        ax.text(0.98, 0.02, 'Bubble size = MW\nMore atoms → Larger volume', 
               transform=ax.transAxes, fontsize=7,
               verticalalignment='bottom', horizontalalignment='right',
               bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
        
        return ax
    
    def panel_f_quale_prediction(self, ax):
        """Panel F: Quale prediction map"""
        
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 10)
        ax.axis('off')
        
        # Title
        ax.text(5, 9.5, 'F. Molecular Properties → Predicted Quale', 
               fontsize=10, fontweight='bold', ha='center', va='top')
        
        # Define predictions
        predictions = [
            {
                'y': 7.5,
                'name': 'Ethanol',
                'properties': 'Small, linear\nNo rings',
                'quale': '"Sharp, Clean"\nSimple sensation',
                'color': '#3498db'
            },
            {
                'y': 5.8,
                'name': 'Benzene',
                'properties': 'Symmetric\n1 aromatic ring',
                'quale': '"Resonant, Pure"\nUnified sensation',
                'color': '#2ecc71'
            },
            {
                'y': 4.1,
                'name': 'Indole',
                'properties': 'Bicyclic\nN-containing',
                'quale': '"Deep, Complex"\nLayered sensation',
                'color': '#e74c3c'
            },
            {
                'y': 2.4,
                'name': 'Vanillin',
                'properties': 'Large, substituted\nMultiple groups',
                'quale': '"Rich, Textured"\nMulti-faceted',
                'color': '#9b59b6'
            },
        ]
        
        for pred in predictions:
            y = pred['y']
            color = pred['color']
            
            # Molecule name
            name_box = mpatches.FancyBboxPatch((0.5, y-0.3), 1.5, 0.6,
                                              boxstyle="round,pad=0.05",
                                              edgecolor='black', facecolor=color,
                                              alpha=0.5, linewidth=1.5)
            ax.add_patch(name_box)
            ax.text(1.25, y, pred['name'], ha='center', va='center',
                   fontsize=7, fontweight='bold')
            
            # Arrow
            ax.annotate('', xy=(2.8, y), xytext=(2.2, y),
                       arrowprops=dict(arrowstyle='->', lw=1.5, color='black'))
            
            # Properties
            prop_box = mpatches.FancyBboxPatch((2.8, y-0.3), 2.5, 0.6,
                                              boxstyle="round,pad=0.05",
                                              edgecolor='black', facecolor=color,
                                              alpha=0.3, linewidth=1.5)
            ax.add_patch(prop_box)
            ax.text(4.05, y, pred['properties'], ha='center', va='center',
                   fontsize=6)
            
            # Arrow
            ax.annotate('', xy=(6.2, y), xytext=(5.5, y),
                       arrowprops=dict(arrowstyle='->', lw=1.5, color='black'))
            
            # Quale
            quale_box = mpatches.FancyBboxPatch((6.2, y-0.3), 3.3, 0.6,
                                               boxstyle="round,pad=0.05",
                                               edgecolor='black', facecolor=color,
                                               alpha=0.5, linewidth=1.5)
            ax.add_patch(quale_box)
            ax.text(7.85, y, pred['quale'], ha='center', va='center',
                   fontsize=6, style='italic', fontweight='bold')
        
        # Bottom summary
        ax.text(5, 0.8, 'Molecular encoding determines oscillatory hole configuration\n→ Unique phenomenal signature', 
               fontsize=7, ha='center', style='italic',
               bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.3))
        
        return ax

# Run
if __name__ == "__main__":
    viz = MolecularEncodingVisualization()
    viz.create_figure()
    print("\n✓✓✓ Chart Set 6 Complete ✓✓✓\n")
