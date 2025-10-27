"""
Chart Set 5: Vibrational Landscape and Quale Texture
6-panel figure showing how bond vibrations create phenomenal character
"""

import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import matplotlib.patches as mpatches
from scipy import signal

plt.rcParams.update({
    'font.family': 'Arial',
    'font.size': 8,
    'axes.linewidth': 0.5,
    'figure.dpi': 300,
})

class VibrationalLandscapeVisualization:
    """Chart Set 5: Vibrational Landscape and Quale Texture"""
    
    def __init__(self):
        self.prepare_data()
    
    def prepare_data(self):
        """Prepare vibrational data for vanillin"""
        
        # Bond data from analysis
        self.bonds = [
            {'type': 'C-O', 'order': 'SINGLE', 'k': 360, 'freq': 2.83e13, 'length': 1.421, 'aromatic': False},
            {'type': 'O-C', 'order': 'SINGLE', 'k': 360, 'freq': 2.83e13, 'length': 1.370, 'aromatic': False},
            {'type': 'C-C', 'order': 'AROMATIC', 'k': 700, 'freq': 4.22e13, 'length': 1.397, 'aromatic': True},
            {'type': 'C-C', 'order': 'AROMATIC', 'k': 700, 'freq': 4.22e13, 'length': 1.401, 'aromatic': True},
            {'type': 'C-C', 'order': 'SINGLE', 'k': 450, 'freq': 3.38e13, 'length': 1.477, 'aromatic': False},
            {'type': 'C-O', 'order': 'DOUBLE', 'k': 1200, 'freq': 5.17e13, 'length': 1.225, 'aromatic': False},
            {'type': 'C-C', 'order': 'AROMATIC', 'k': 700, 'freq': 4.22e13, 'length': 1.397, 'aromatic': True},
            {'type': 'C-C', 'order': 'AROMATIC', 'k': 700, 'freq': 4.22e13, 'length': 1.394, 'aromatic': True},
            {'type': 'C-C', 'order': 'AROMATIC', 'k': 700, 'freq': 4.22e13, 'length': 1.396, 'aromatic': True},
            {'type': 'C-O', 'order': 'SINGLE', 'k': 360, 'freq': 2.83e13, 'length': 1.370, 'aromatic': False},
        ]
        
        # Dominant modes
        self.dominant_modes = [
            {'type': 'O-H', 'freq': 1.11e14},
            {'type': 'C-H', 'freq': 9.06e13},
            {'type': 'C-H', 'freq': 9.06e13},
            {'type': 'C-H', 'freq': 9.06e13},
            {'type': 'C-H', 'freq': 9.06e13},
        ]
        
        # Average frequency
        self.avg_freq = 6.15e13  # Hz
        
        # Conjugated bonds
        self.n_conjugated = 10
        
        # Bond type colors
        self.bond_colors = {
            'C-O SINGLE': '#3498db',
            'C-O DOUBLE': '#e74c3c',
            'C-C SINGLE': '#95a5a6',
            'C-C AROMATIC': '#2ecc71',
            'O-H': '#f39c12',
            'C-H': '#9b59b6',
        }
    
    def create_figure(self, output='chartset5_vibrational_landscape'):
        """Create complete 6-panel figure"""
        
        fig = plt.figure(figsize=(7.2, 9))
        gs = GridSpec(3, 2, figure=fig, hspace=0.4, wspace=0.35)
        
        # Panel A: Frequency spectrum
        ax_a = fig.add_subplot(gs[0, 0])
        self.panel_a_frequency_spectrum(ax_a)
        
        # Panel B: Force constant vs frequency
        ax_b = fig.add_subplot(gs[0, 1])
        self.panel_b_force_vs_frequency(ax_b)
        
        # Panel C: Oscillatory landscape
        ax_c = fig.add_subplot(gs[1, 0])
        self.panel_c_oscillatory_landscape(ax_c)
        
        # Panel D: Temporal beating
        ax_d = fig.add_subplot(gs[1, 1])
        self.panel_d_temporal_beating(ax_d)
        
        # Panel E: Conjugation network
        ax_e = fig.add_subplot(gs[2, 0])
        self.panel_e_conjugation_network(ax_e)
        
        # Panel F: Quale prediction
        ax_f = fig.add_subplot(gs[2, 1])
        self.panel_f_quale_prediction(ax_f)
        
        # Overall title
        fig.suptitle('Vibrational Landscape: From Bonds to Qualia', 
                    fontsize=12, fontweight='bold', y=0.995)
        
        # Save
        plt.savefig(f'{output}.pdf', bbox_inches='tight')
        plt.savefig(f'{output}.png', bbox_inches='tight')
        print(f"✓ {output} saved")
        
        return fig
    
    def panel_a_frequency_spectrum(self, ax):
        """Panel A: Frequency spectrum histogram"""
        
        # Collect all frequencies (bonds + dominant modes)
        all_freqs = [b['freq'] / 1e13 for b in self.bonds]  # Convert to THz (10^13 Hz)
        all_types = [f"{b['type']} {b['order']}" for b in self.bonds]
        
        # Add dominant modes
        for mode in self.dominant_modes:
            all_freqs.append(mode['freq'] / 1e13)
            all_types.append(mode['type'])
        
        # Create histogram bins
        bins = np.linspace(2, 12, 21)
        
        # Separate by bond type for stacking
        freq_by_type = {}
        for freq, btype in zip(all_freqs, all_types):
            if btype not in freq_by_type:
                freq_by_type[btype] = []
            freq_by_type[btype].append(freq)
        
        # Plot stacked histogram
        bottom = np.zeros(len(bins)-1)
        for btype, freqs in freq_by_type.items():
            color = self.bond_colors.get(btype, '#95a5a6')
            counts, _ = np.histogram(freqs, bins=bins)
            ax.bar(bins[:-1], counts, width=np.diff(bins), bottom=bottom,
                  label=btype, color=color, alpha=0.7, edgecolor='black', linewidth=0.5,
                  align='edge')
            bottom += counts
        
        # Mark average
        avg_thz = self.avg_freq / 1e13
        ax.axvline(avg_thz, color='red', linestyle='--', linewidth=2,
                  label=f'Average: {avg_thz:.1f} THz')
        
        # Styling
        ax.set_xlabel('Vibrational Frequency (THz)', fontsize=9, fontweight='bold')
        ax.set_ylabel('Number of Bonds', fontsize=9, fontweight='bold')
        ax.set_title('A. Frequency Spectrum', fontsize=10, fontweight='bold', pad=10)
        ax.legend(fontsize=5, loc='upper right', ncol=2)
        ax.grid(True, alpha=0.3, axis='y')
        
        # Add range annotation
        freq_range = max(all_freqs) / min(all_freqs)
        ax.text(0.02, 0.98, f'Frequency range:\n{freq_range:.1f}× (broad)', 
               transform=ax.transAxes, fontsize=7,
               verticalalignment='top',
               bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.3))
        
        return ax
    
    def panel_b_force_vs_frequency(self, ax):
        """Panel B: Force constant vs frequency relationship"""
        
        # Extract data
        force_constants = [b['k'] for b in self.bonds]
        frequencies = [b['freq'] / 1e13 for b in self.bonds]  # THz
        bond_types = [f"{b['type']} {b['order']}" for b in self.bonds]
        lengths = [b['length'] for b in self.bonds]
        
        # Plot points
        for k, f, btype, length in zip(force_constants, frequencies, bond_types, lengths):
            color = self.bond_colors.get(btype, '#95a5a6')
            size = (2.0 / length) * 100  # Inverse of length for size
            ax.scatter(k, f, s=size, c=color, alpha=0.7,
                      edgecolors='black', linewidth=1, label=btype)
        
        # Theoretical relationship: f ∝ √k (for fixed mass)
        k_theory = np.linspace(min(force_constants), max(force_constants), 100)
        # f = (1/2π) √(k/μ), but we'll just show proportionality
        f_theory = np.sqrt(k_theory / min(force_constants)) * min(frequencies)
        ax.plot(k_theory, f_theory, 'k--', linewidth=2, alpha=0.5,
               label='f ∝ √k')
        
        # Remove duplicate labels
        handles, labels = ax.get_legend_handles_labels()
        by_label = dict(zip(labels, handles))
        ax.legend(by_label.values(), by_label.keys(), fontsize=6, loc='upper left')
        
        # Styling
        ax.set_xlabel('Force Constant (N/m)', fontsize=9, fontweight='bold')
        ax.set_ylabel('Frequency (THz)', fontsize=9, fontweight='bold')
        ax.set_title('B. Force Constant → Frequency', fontsize=10, fontweight='bold', pad=10)
        ax.grid(True, alpha=0.3)
        
        # Add annotation
        ax.text(0.98, 0.02, 'Stronger bonds\n→ Higher frequency', 
               transform=ax.transAxes, fontsize=7,
               verticalalignment='bottom', horizontalalignment='right',
               bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.5))
        
        return ax
    
    def panel_c_oscillatory_landscape(self, ax):
        """Panel C: 2D oscillatory landscape (superposition)"""
        
        # Create 2D grid
        x = np.linspace(-5, 5, 200)
        y = np.linspace(-5, 5, 200)
        X, Y = np.meshgrid(x, y)
        
        # Superpose oscillations from different bonds
        Z = np.zeros_like(X)
        
        # Add contribution from each bond type
        for i, bond in enumerate(self.bonds[:5]):  # Use first 5 for visualization
            freq = bond['freq'] / 1e13  # THz
            k = bond['k']
            
            # Create oscillatory pattern (simplified)
            # Position each "source" at different locations
            angle = 2 * np.pi * i / 5
            x0 = 2 * np.cos(angle)
            y0 = 2 * np.sin(angle)
            
            # Distance from source
            R = np.sqrt((X - x0)**2 + (Y - y0)**2)
            
            # Oscillatory pattern (amplitude decays with distance)
            amplitude = k / 1000  # Scale by force constant
            Z += amplitude * np.cos(2 * np.pi * freq * R / 10) * np.exp(-R / 3)
        
        # Add dominant O-H mode (highest frequency)
        freq_oh = self.dominant_modes[0]['freq'] / 1e13
        R_center = np.sqrt(X**2 + Y**2)
        Z += 1.2 * np.cos(2 * np.pi * freq_oh * R_center / 10) * np.exp(-R_center / 4)
        
        # Plot as heatmap
        im = ax.contourf(X, Y, Z, levels=30, cmap='RdBu_r', alpha=0.8)
        
        # Add contour lines
        ax.contour(X, Y, Z, levels=10, colors='black', linewidths=0.5, alpha=0.3)
        
        # Mark bond positions
        for i in range(5):
            angle = 2 * np.pi * i / 5
            x0 = 2 * np.cos(angle)
            y0 = 2 * np.sin(angle)
            ax.plot(x0, y0, 'ko', markersize=8, markeredgecolor='white', markeredgewidth=1)
        
        # Center (O-H)
        ax.plot(0, 0, 'r*', markersize=15, markeredgecolor='white', markeredgewidth=1)
        
        # Styling
        ax.set_xlabel('X (Å)', fontsize=9, fontweight='bold')
        ax.set_ylabel('Y (Å)', fontsize=9, fontweight='bold')
        ax.set_title('C. Oscillatory Landscape', fontsize=10, fontweight='bold', pad=10)
        ax.set_aspect('equal')
        
        # Colorbar
        cbar = plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
        cbar.set_label('Amplitude', fontsize=7)
        
        # Add annotation
        ax.text(0.02, 0.98, 'Complex interference\n→ "Textured" quale', 
               transform=ax.transAxes, fontsize=7,
               verticalalignment='top',
               bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.7))
        
        return ax
    
    def panel_d_temporal_beating(self, ax):
        """Panel D: Temporal beating patterns"""
        
        # Time array (in femtoseconds)
        t = np.linspace(0, 200, 2000)  # 200 fs
        
        # Create signals for different bond types
        signals = {}
        
        # O-H (highest frequency)
        freq_oh = self.dominant_modes[0]['freq']
        period_oh = 1 / freq_oh * 1e15  # Convert to fs
        signals['O-H (111 THz)'] = np.sin(2 * np.pi * t / period_oh)
        
        # C-H
        freq_ch = self.dominant_modes[1]['freq']
        period_ch = 1 / freq_ch * 1e15
        signals['C-H (91 THz)'] = np.sin(2 * np.pi * t / period_ch)
        
        # C=O
        freq_co = 5.17e13
        period_co = 1 / freq_co * 1e15
        signals['C=O (52 THz)'] = np.sin(2 * np.pi * t / period_co)
        
        # C-C aromatic
        freq_cc = 4.22e13
        period_cc = 1 / freq_cc * 1e15
        signals['C-C arom (42 THz)'] = np.sin(2 * np.pi * t / period_cc)
        
        # Superposition
        superposition = sum(signals.values()) / len(signals)
        
        # Plot individual signals (offset for clarity)
        colors = ['#f39c12', '#9b59b6', '#e74c3c', '#2ecc71']
        offsets = [3, 2, 1, 0]
        
        for (label, sig), color, offset in zip(signals.items(), colors, offsets):
            ax.plot(t, sig + offset, color=color, linewidth=1, alpha=0.7, label=label)
        
        # Plot superposition (bold, at bottom)
        ax.plot(t, superposition - 1.5, 'k-', linewidth=2, label='Superposition')
        
        # Styling
        ax.set_xlabel('Time (femtoseconds)', fontsize=9, fontweight='bold')
        ax.set_ylabel('Amplitude (offset)', fontsize=9, fontweight='bold')
        ax.set_title('D. Temporal Beating Patterns', fontsize=10, fontweight='bold', pad=10)
        ax.legend(fontsize=6, loc='upper right')
        ax.grid(True, alpha=0.3, axis='x')
        ax.set_ylim(-3, 4)
        
        # Add annotation
        ax.text(0.02, 0.02, 'Multiple frequencies\n→ Complex temporal pattern', 
               transform=ax.transAxes, fontsize=7,
               verticalalignment='bottom',
               bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.5))
        
        return ax
    
    def panel_e_conjugation_network(self, ax):
        """Panel E: Conjugation network with frequency overlay"""
        
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 10)
        ax.axis('off')
        
        # Title
        ax.text(5, 9.5, 'E. Conjugation Network', 
               fontsize=10, fontweight='bold', ha='center', va='top')
        
        # Draw benzene ring (hexagon)
        angles = np.linspace(0, 2*np.pi, 7)
        hex_x = 5 + 2 * np.cos(angles)
        hex_y = 5 + 2 * np.sin(angles)
        
        # Draw aromatic bonds (colored by frequency)
        for i in range(6):
            x_coords = [hex_x[i], hex_x[i+1]]
            y_coords = [hex_y[i], hex_y[i+1]]
            ax.plot(x_coords, y_coords, color='#2ecc71', linewidth=4, alpha=0.7)
            
            # Add frequency label
            mid_x = (hex_x[i] + hex_x[i+1]) / 2
            mid_y = (hex_y[i] + hex_y[i+1]) / 2
            if i == 0:  # Label one bond
                ax.text(mid_x, mid_y + 0.3, '42 THz', fontsize=6, ha='center',
                       bbox=dict(boxstyle='round', facecolor='white', alpha=0.7))
        
        # Draw substituents
        # -OCH3 (top left)
        ax.plot([hex_x[1], hex_x[1]-1.5], [hex_y[1], hex_y[1]+0.5], 
               color='#3498db', linewidth=3, alpha=0.7)
        ax.text(hex_x[1]-1.8, hex_y[1]+0.5, 'OCH₃', fontsize=7, fontweight='bold')
        ax.text(hex_x[1]-1.0, hex_y[1]+0.8, '28 THz', fontsize=5,
               bbox=dict(boxstyle='round', facecolor='white', alpha=0.7))
        
        # -CHO (top right)
        ax.plot([hex_x[5], hex_x[5]+1.5], [hex_y[5], hex_y[5]+0.5], 
               color='#e74c3c', linewidth=3, alpha=0.7)
        ax.text(hex_x[5]+1.8, hex_y[5]+0.5, 'CHO', fontsize=7, fontweight='bold')
        ax.text(hex_x[5]+1.0, hex_y[5]+0.8, '52 THz', fontsize=5,
               bbox=dict(boxstyle='round', facecolor='white', alpha=0.7))
        
        # -OH (bottom)
        ax.plot([hex_x[3], hex_x[3]], [hex_y[3], hex_y[3]-1.5], 
               color='#f39c12', linewidth=3, alpha=0.7)
        ax.text(hex_x[3], hex_y[3]-1.8, 'OH', fontsize=7, fontweight='bold')
        ax.text(hex_x[3], hex_y[3]-1.0, '111 THz', fontsize=5,
               bbox=dict(boxstyle='round', facecolor='white', alpha=0.7))
        
        # Add atoms at vertices
        for i in range(6):
            circle = plt.Circle((hex_x[i], hex_y[i]), 0.2, color='gray', 
                               edgecolor='black', linewidth=1, zorder=10)
            ax.add_patch(circle)
        
        # Legend
        legend_elements = [
            mpatches.Patch(color='#2ecc71', label='Aromatic (42 THz)'),
            mpatches.Patch(color='#e74c3c', label='C=O (52 THz)'),
            mpatches.Patch(color='#f39c12', label='O-H (111 THz)'),
            mpatches.Patch(color='#3498db', label='C-O (28 THz)'),
        ]
        ax.legend(handles=legend_elements, fontsize=6, loc='lower center', ncol=2)
        
        # Add annotation
        ax.text(5, 1, f'{self.n_conjugated} conjugated bonds\n→ Coupled oscillations', 
               ha='center', fontsize=7, style='italic',
               bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.3))
        
        return ax
    
    def panel_f_quale_prediction(self, ax):
        """Panel F: From spectrum to quale"""
        
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 10)
        ax.axis('off')
        
        # Title
        ax.text(5, 9.5, 'F. Spectrum → Quale', 
               fontsize=10, fontweight='bold', ha='center', va='top')
        
        # Define spectrum types and their qualia
        spectrum_types = [
            {
                'y': 7,
                'name': 'Narrow Spectrum',
                'example': '(e.g., Methane)',
                'bars': [1, 1, 1],
                'quale': '"Simple" quale',
                'color': '#3498db'
            },
            {
                'y': 5,
                'name': 'Bimodal Spectrum',
                'example': '(e.g., Benzene)',
                'bars': [0.5, 0, 1],
                'quale': '"Resonant" quale',
                'color': '#2ecc71'
            },
            {
                'y': 3,
                'name': 'Broad Spectrum',
                'example': '(e.g., Vanillin)',
                'bars': [0.7, 0.9, 1, 0.8, 0.6],
                'quale': '"Rich, Complex" quale',
                'color': '#9b59b6'
            },
        ]
        
        for spec in spectrum_types:
            y = spec['y']
            color = spec['color']
            
            # Name
            ax.text(1, y + 0.5, spec['name'], fontsize=7, fontweight='bold')
            ax.text(1, y + 0.2, spec['example'], fontsize=6, style='italic')
            
            # Spectrum bars (mini histogram)
            bar_width = 0.3
            bar_x = np.arange(len(spec['bars'])) * bar_width + 2.5
            for i, height in enumerate(spec['bars']):
                rect = mpatches.Rectangle((bar_x[i], y - 0.3), bar_width * 0.8, height * 0.6,
                                         facecolor=color, edgecolor='black', linewidth=1, alpha=0.7)
                ax.add_patch(rect)
            
            # Arrow
            ax.annotate('', xy=(6.5, y), xytext=(5.5, y),
                       arrowprops=dict(arrowstyle='->', lw=2, color='black'))
            
            # Quale
            quale_box = mpatches.FancyBboxPatch((6.5, y - 0.4), 3, 0.8,
                                               boxstyle="round,pad=0.1",
                                               edgecolor='black', facecolor=color,
                                               alpha=0.5, linewidth=1.5)
            ax.add_patch(quale_box)
            ax.text(8, y, spec['quale'], ha='center', va='center',
                   fontsize=7, fontweight='bold', style='italic')
        
        # Bottom summary
        ax.text(5, 0.8, 'Vanillin: 4× frequency range + multiple peaks\n→ Complex, textured phenomenal character', 
               fontsize=7, ha='center', style='italic',
               bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.3))
        
        return ax

# Run
if __name__ == "__main__":
    viz = VibrationalLandscapeVisualization()
    viz.create_figure()
    print("\n✓✓✓ Chart Set 5 Complete ✓✓✓\n")
