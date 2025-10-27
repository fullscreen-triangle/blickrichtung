"""
Chart Set 3: Mechanism Revealed
4-panel figure showing the complete causal chain
"""

import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
from mpl_toolkits.mplot3d import Axes3D

plt.rcParams.update({
    'font.family': 'Arial',
    'font.size': 8,
    'axes.linewidth': 0.5,
    'figure.dpi': 300,
})

class MechanismVisualization:
    """Chart Set 3: Mechanism Revealed"""
    
    def __init__(self):
        self.prepare_data()
    
    def prepare_data(self):
        """Prepare mechanism data"""
        
        # O2 positions (simplified for visualization)
        np.random.seed(42)
        self.o2_positions = np.random.randn(51, 3) * 2
        
        # Completion frequency data
        self.vo2_range = np.linspace(50, 400, 100)
        self.completion_freq = self.vo2_range * 0.24  # Hz, proportional to VO2
        
        # Time perception relationship
        self.freq_range = np.linspace(30, 240, 100)
        self.perceived_time = self.freq_range  # Direct relationship
        
        # Multi-scale data
        self.scales = {
            'Molecular': {'level': 5, 'measure': 'O₂ consumption', 'value': '250-1000 mL/min'},
            'Cellular': {'level': 4, 'measure': 'Completion frequency', 'value': '60-240 Hz'},
            'Neural': {'level': 3, 'measure': 'CFF / RT', 'value': '60-240 Hz / 2-6 ms'},
            'Perceptual': {'level': 2, 'measure': 'Subjective time', 'value': '60-240s'},
            'Behavioral': {'level': 1, 'measure': 'Reports / Actions', 'value': 'Variable'},
        }
    
    def create_figure(self, output='chartset3_mechanism'):
        """Create complete 4-panel figure"""
        
        fig = plt.figure(figsize=(7.2, 7.2))
        gs = GridSpec(2, 2, figure=fig, hspace=0.35, wspace=0.35)
        
        # Panel A: Completion cascade
        ax_a = fig.add_subplot(gs[0, 0], projection='3d')
        self.panel_a_cascade(ax_a)
        
        # Panel B: VO2 to frequency
        ax_b = fig.add_subplot(gs[0, 1])
        self.panel_b_vo2_to_frequency(ax_b)
        
        # Panel C: Frequency to time
        ax_c = fig.add_subplot(gs[1, 0])
        self.panel_c_frequency_to_time(ax_c)
        
        # Panel D: Multi-scale integration
        ax_d = fig.add_subplot(gs[1, 1])
        self.panel_d_multiscale(ax_d)
        
        # Overall title
        fig.suptitle('Mechanism Revealed: From O₂ to Consciousness', 
                    fontsize=12, fontweight='bold', y=0.98)
        
        # Save
        plt.savefig(f'{output}.pdf', bbox_inches='tight')
        plt.savefig(f'{output}.png', bbox_inches='tight')
        print(f"✓ {output} saved")
        
        return fig
    
    def panel_a_cascade(self, ax):
        """Panel A: The completion cascade (3D)"""
        
        # Plot O2 positions
        positions = self.o2_positions
        distances = np.linalg.norm(positions, axis=1)
        
        scatter = ax.scatter(positions[:, 0], positions[:, 1], positions[:, 2],
                           c=distances, cmap='viridis', s=50, alpha=0.6,
                           edgecolors='black', linewidth=0.5)
        
        # Mark center (hole)
        ax.scatter([0], [0], [0], c='red', s=300, marker='*',
                  edgecolors='black', linewidth=2, label='Oscillatory Hole')
        
        # Styling
        ax.set_xlabel('X (Å)', fontsize=7)
        ax.set_ylabel('Y (Å)', fontsize=7)
        ax.set_zlabel('Z (Å)', fontsize=7)
        ax.set_title('A. O₂ Configuration\nAround Hole', fontsize=10, fontweight='bold', pad=10)
        ax.view_init(elev=20, azim=45)
        
        # Add colorbar
        cbar = plt.colorbar(scatter, ax=ax, fraction=0.046, pad=0.1)
        cbar.set_label('Distance (Å)', fontsize=7)
        
        # Add frequency annotation
        ax.text2D(0.05, 0.95, 'Completion\nfrequency:\n~5-6 Hz', 
                 transform=ax.transAxes, fontsize=7,
                 verticalalignment='top',
                 bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.5))
        
        return ax
    
    def panel_b_vo2_to_frequency(self, ax):
        """Panel B: VO2 → Completion Frequency"""
        
        # Main relationship
        ax.plot(self.vo2_range, self.completion_freq, 'b-', linewidth=3, alpha=0.7)
        ax.fill_between(self.vo2_range, self.completion_freq * 0.9, 
                       self.completion_freq * 1.1, alpha=0.2, color='blue')
        
        # Mark key points
        key_points = [
            (85, 85*0.24, 'Benzos'),
            (100, 100*0.24, 'Baseline'),
            (130, 130*0.24, 'Cocaine'),
            (400, 400*0.24, 'Exercise'),
        ]
        
        for vo2, freq, label in key_points:
            ax.plot(vo2, freq, 'ro', markersize=8, markeredgecolor='black', markeredgewidth=1)
            ax.annotate(label, xy=(vo2, freq), xytext=(vo2+20, freq+10),
                       fontsize=7, arrowprops=dict(arrowstyle='->', lw=1))
        
        # Styling
        ax.set_xlabel('VO₂ (% of baseline)', fontsize=9, fontweight='bold')
        ax.set_ylabel('Completion Frequency (Hz)', fontsize=9, fontweight='bold')
        ax.set_title('B. VO₂ → Completion Frequency', fontsize=10, fontweight='bold', pad=10)
        ax.grid(True, alpha=0.3)
        
        # Add equation
        ax.text(0.05, 0.95, 'f = k × VO₂\nk ≈ 0.24 Hz per %', 
               transform=ax.transAxes, fontsize=8,
               verticalalignment='top',
               bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.5))
        
        return ax
    
    def panel_c_frequency_to_time(self, ax):
        """Panel C: Completion Frequency → Subjective Time"""
        
        # Create timeline visualization
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 10)
        ax.axis('off')
        
        # Title
        ax.text(5, 9.5, 'C. Frequency → Subjective Time', 
               fontsize=10, fontweight='bold', ha='center', va='top')
        
        # High frequency example (top)
        ax.text(0.5, 8, 'High Frequency (240 Hz):', fontsize=8, fontweight='bold', va='top')
        tick_x = np.linspace(1, 9, 24)  # Many ticks
        for x in tick_x:
            ax.plot([x, x], [7.2, 7.5], 'g-', linewidth=1)
        ax.text(5, 6.8, 'Many "ticks" → Time feels SLOWER', 
               fontsize=7, ha='center', style='italic',
               bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.5))
        ax.text(9.5, 7.35, '60s feels\nlike 240s', fontsize=6, ha='right', va='center',
               bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.5))
        
        # Normal frequency (middle)
        ax.text(0.5, 5.5, 'Normal Frequency (60 Hz):', fontsize=8, fontweight='bold', va='top')
        tick_x = np.linspace(1, 9, 6)  # Normal ticks
        for x in tick_x:
            ax.plot([x, x], [4.7, 5.0], 'b-', linewidth=1)
        ax.text(5, 4.3, 'Normal "ticks" → Time feels NORMAL', 
               fontsize=7, ha='center', style='italic',
               bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.5))
        ax.text(9.5, 4.85, '60s feels\nlike 60s', fontsize=6, ha='right', va='center',
               bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.5))
        
        # Low frequency (bottom)
        ax.text(0.5, 3, 'Low Frequency (15 Hz):', fontsize=8, fontweight='bold', va='top')
        tick_x = np.linspace(1, 9, 3)  # Few ticks
        for x in tick_x:
            ax.plot([x, x], [2.2, 2.5], 'r-', linewidth=1)
        ax.text(5, 1.8, 'Few "ticks" → Time feels FASTER', 
               fontsize=7, ha='center', style='italic',
               bbox=dict(boxstyle='round', facecolor='lightcoral', alpha=0.5))
        ax.text(9.5, 2.35, '60s feels\nlike 15s', fontsize=6, ha='right', va='center',
               bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.5))
        
        # Bottom explanation
        ax.text(5, 0.5, 'Mechanism: Each completion = one "tick" of subjective time\nMore completions/second = slower perceived time', 
               fontsize=7, ha='center', style='italic',
               bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
        
        return ax
    
    def panel_d_multiscale(self, ax):
        """Panel D: Multi-scale integration"""
        
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 10)
        ax.axis('off')
        
        # Title
        ax.text(5, 9.5, 'D. Multi-Scale Integration', 
               fontsize=10, fontweight='bold', ha='center', va='top')
        
        # Draw hierarchy
        scales = ['Molecular', 'Cellular', 'Neural', 'Perceptual', 'Behavioral']
        measures = ['O₂ consumption\n250-1000 mL/min', 
                   'Completion frequency\n60-240 Hz',
                   'CFF / RT\n60-240 Hz / 2-6 ms',
                   'Subjective time\n60-240s perceived',
                   'Reports / Actions\nVariable']
        
        y_positions = [8, 6.5, 5, 3.5, 2]
        colors = ['#3498db', '#2ecc71', '#f39c12', '#e74c3c', '#9b59b6']
        
        for i, (scale, measure, y, color) in enumerate(zip(scales, measures, y_positions, colors)):
            # Box
            box = FancyBboxPatch((1, y-0.4), 8, 0.8, 
                                boxstyle="round,pad=0.1", 
                                edgecolor='black', facecolor=color, 
                                alpha=0.3, linewidth=2)
            ax.add_patch(box)
            
            # Text
            ax.text(2, y, f'{scale}:', fontsize=8, fontweight='bold', va='center')
            ax.text(5.5, y, measure, fontsize=6.5, va='center', ha='center')
            
            # Arrow to next level
            if i < len(scales) - 1:
                arrow = FancyArrowPatch((5, y-0.5), (5, y_positions[i+1]+0.5),
                                      arrowstyle='->', mutation_scale=20, 
                                      linewidth=2, color='black', alpha=0.5)
                ax.add_patch(arrow)
                
                # Causation label
                if i == 0:
                    ax.text(5.5, (y + y_positions[i+1])/2, 'drives', 
                           fontsize=6, style='italic', ha='left')
        
        # Bottom summary
        ax.text(5, 0.8, 'Complete Causal Chain: O₂ → Frequency → Perception', 
               fontsize=8, ha='center', fontweight='bold',
               bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.5))
        
        # Side annotations
        ax.text(0.2, 8, '↑\nPhysical', fontsize=7, ha='center', va='center', rotation=90)
        ax.text(0.2, 2, '↓\nPhenomenal', fontsize=7, ha='center', va='center', rotation=90)
        
        return ax

# Run
if __name__ == "__main__":
    viz = MechanismVisualization()
    viz.create_figure()
    print("\n✓✓✓ Chart Set 3 Complete ✓✓✓\n")
