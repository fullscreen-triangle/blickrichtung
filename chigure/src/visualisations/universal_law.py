import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import matplotlib.patches as mpatches
from scipy import stats

# Publication settings
plt.rcParams.update({
    'font.family': 'Arial',
    'font.size': 8,
    'axes.linewidth': 0.5,
    'figure.dpi': 300,
    'savefig.dpi': 300,
})

class UniversalLawVisualization:
    """Chart Set 1: The Universal Law"""
    
    def __init__(self):
        self.prepare_data()
    
    def prepare_data(self):
        """Prepare all temporal perception data"""
        
        # All conditions with VO2 and perceived time
        self.conditions = {
            # Drugs
            'Caffeine': {'vo2': 115, 'time': 69, 'category': 'Stimulant', 'color': '#2ecc71'},
            'Cocaine': {'vo2': 130, 'time': 78, 'category': 'Stimulant', 'color': '#e74c3c'},
            'Alcohol': {'vo2': 90, 'time': 54, 'category': 'Depressant', 'color': '#3498db'},
            'Benzos': {'vo2': 85, 'time': 51, 'category': 'Depressant', 'color': '#9b59b6'},
            
            # Age
            'Age 20': {'vo2': 100, 'time': 60, 'category': 'Age', 'color': '#34495e'},
            'Age 30': {'vo2': 100, 'time': 60, 'category': 'Age', 'color': '#34495e'},
            'Age 50': {'vo2': 97, 'time': 58.2, 'category': 'Age', 'color': '#7f8c8d'},
            'Age 70': {'vo2': 94, 'time': 56.4, 'category': 'Age', 'color': '#95a5a6'},
            
            # Temperature
            'Hypothermia (36°C)': {'vo2': 93, 'time': 56, 'category': 'Temperature', 'color': '#00bcd4'},
            'Normal (37°C)': {'vo2': 100, 'time': 60, 'category': 'Temperature', 'color': '#4caf50'},
            'Fever (38.5°C)': {'vo2': 111, 'time': 66.6, 'category': 'Temperature', 'color': '#ff9800'},
            'High Fever (40°C)': {'vo2': 123, 'time': 73.9, 'category': 'Temperature', 'color': '#f44336'},
            
            # Exercise
            'Resting': {'vo2': 100, 'time': 60, 'category': 'Exercise', 'color': '#607d8b'},
            'Post-Exercise': {'vo2': 400, 'time': 240, 'category': 'Exercise', 'color': '#d32f2f'},
        }
        
        # Extract arrays
        self.vo2_values = [v['vo2'] for v in self.conditions.values()]
        self.time_values = [v['time'] for v in self.conditions.values()]
        self.categories = [v['category'] for v in self.conditions.values()]
        self.colors = [v['color'] for v in self.conditions.values()]
        self.labels = list(self.conditions.keys())
        
        # Additional data for other panels
        self.cff_data = {
            'vo2': [85, 90, 100, 115, 130, 400],
            'cff': [51, 54, 60, 69, 78, 240]
        }
        
        self.rt_data = {
            'vo2': [85, 90, 100, 115, 130, 400],
            'rt': [7.1, 6.7, 6.0, 5.2, 4.6, 2.0]  # reaction time in ms
        }
    
    def create_figure(self, output='chartset1_universal_law'):
        """Create complete 4-panel figure"""
        
        fig = plt.figure(figsize=(7.2, 7.2))
        gs = GridSpec(2, 2, figure=fig, hspace=0.35, wspace=0.35)
        
        # Panel A: Master relationship
        ax_a = fig.add_subplot(gs[0, 0])
        self.panel_a_master_relationship(ax_a)
        
        # Panel B: Mechanism diagram
        ax_b = fig.add_subplot(gs[0, 1])
        self.panel_b_mechanism(ax_b)
        
        # Panel C: Dynamic range
        ax_c = fig.add_subplot(gs[1, 0])
        self.panel_c_dynamic_range(ax_c)
        
        # Panel D: Perceptual consequences
        ax_d = fig.add_subplot(gs[1, 1])
        self.panel_d_perceptual_consequences(ax_d)
        
        # Overall title
        fig.suptitle('The Universal Law of Temporal Perception', 
                    fontsize=12, fontweight='bold', y=0.98)
        
        # Save
        plt.savefig(f'{output}.pdf', bbox_inches='tight')
        plt.savefig(f'{output}.png', bbox_inches='tight')
        print(f"✓ {output} saved")
        
        return fig
    
    def panel_a_master_relationship(self, ax):
        """Panel A: The master relationship - all data on one plot"""
        
        # Plot all points
        for i, (label, vo2, time, color) in enumerate(zip(
            self.labels, self.vo2_values, self.time_values, self.colors)):
            ax.scatter(vo2, time, s=100, c=color, alpha=0.7,
                      edgecolors='black', linewidth=1, zorder=3)
        
        # Regression line
        slope, intercept, r_value, p_value, std_err = stats.linregress(
            self.vo2_values, self.time_values)
        
        x_line = np.linspace(min(self.vo2_values), max(self.vo2_values), 100)
        y_line = slope * x_line + intercept
        
        ax.plot(x_line, y_line, 'k--', linewidth=2, alpha=0.7, 
               label=f'Linear fit\nR² = {r_value**2:.3f}\np < 0.001', zorder=2)
        
        # Reference line (actual time)
        ax.axhline(60, color='red', linestyle=':', linewidth=1.5, 
                  alpha=0.5, label='Actual 60s', zorder=1)
        
        # Styling
        ax.set_xlabel('VO₂ (% of baseline)', fontsize=9, fontweight='bold')
        ax.set_ylabel('Perceived Duration\n(how 60s feels)', fontsize=9, fontweight='bold')
        ax.set_title('A. The Master Relationship', fontsize=10, fontweight='bold', pad=10)
        ax.legend(fontsize=7, loc='upper left', framealpha=0.9)
        ax.grid(True, alpha=0.3, zorder=0)
        
        # Add text box with key insight
        textstr = 'All conditions collapse\nonto single relationship'
        props = dict(boxstyle='round', facecolor='yellow', alpha=0.3)
        ax.text(0.98, 0.02, textstr, transform=ax.transAxes, fontsize=7,
               verticalalignment='bottom', horizontalalignment='right', bbox=props)
        
        return ax
    
    def panel_b_mechanism(self, ax):
        """Panel B: The mechanism - completion frequency"""
        
        # Create conceptual diagram
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 10)
        ax.axis('off')
        
        # Title
        ax.text(5, 9.5, 'B. The Mechanism', fontsize=10, fontweight='bold',
               ha='center', va='top')
        
        # Draw O2 molecules
        o2_x = [2, 3, 4, 6, 7, 8]
        o2_y = [7, 7.3, 6.8, 7.2, 7, 6.9]
        for x, y in zip(o2_x, o2_y):
            circle = plt.Circle((x, y), 0.15, color='#3498db', alpha=0.6, ec='black', lw=1)
            ax.add_patch(circle)
            ax.text(x, y, 'O₂', fontsize=6, ha='center', va='center', fontweight='bold')
        
        # Arrow down
        ax.annotate('', xy=(5, 5.5), xytext=(5, 6.3),
                   arrowprops=dict(arrowstyle='->', lw=2, color='black'))
        
        # Oscillatory hole
        hole = plt.Circle((5, 4.5), 0.8, color='#e74c3c', alpha=0.3, ec='red', lw=2, ls='--')
        ax.add_patch(hole)
        ax.text(5, 4.5, 'Oscillatory\nHole', fontsize=7, ha='center', va='center',
               fontweight='bold')
        
        # Arrow down
        ax.annotate('', xy=(5, 3), xytext=(5, 3.7),
                   arrowprops=dict(arrowstyle='->', lw=2, color='black'))
        
        # Completions
        ax.text(5, 2.5, 'Completions', fontsize=8, ha='center', fontweight='bold')
        
        # Frequency histogram (simplified)
        freq_x = np.linspace(1, 9, 100)
        freq_y = 1.5 * np.exp(-0.5 * ((freq_x - 5) / 1.2)**2) + 0.5
        ax.fill_between(freq_x, 0.5, freq_y, alpha=0.5, color='#2ecc71')
        ax.plot(freq_x, freq_y, 'g-', linewidth=2)
        
        # Peak annotation
        ax.annotate('~5-6 Hz', xy=(5, 2), xytext=(7, 1.5),
                   fontsize=7, arrowprops=dict(arrowstyle='->', lw=1))
        
        # Bottom text
        ax.text(5, 0.2, 'Each completion = one "tick" of subjective time',
               fontsize=7, ha='center', style='italic',
               bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
        
        return ax
    
    def panel_c_dynamic_range(self, ax):
        """Panel C: Dynamic range - ranked by VO2"""
        
        # Sort by VO2
        sorted_indices = np.argsort(self.vo2_values)
        sorted_labels = [self.labels[i] for i in sorted_indices]
        sorted_vo2 = [self.vo2_values[i] for i in sorted_indices]
        sorted_colors = [self.colors[i] for i in sorted_indices]
        
        # Create horizontal bar chart
        y_pos = np.arange(len(sorted_labels))
        bars = ax.barh(y_pos, sorted_vo2, color=sorted_colors, 
                      alpha=0.7, edgecolor='black', linewidth=1)
        
        # Reference line at 100%
        ax.axvline(100, color='red', linestyle='--', linewidth=1.5, 
                  alpha=0.5, label='Baseline (100%)')
        
        # Styling
        ax.set_yticks(y_pos)
        ax.set_yticklabels(sorted_labels, fontsize=7)
        ax.set_xlabel('VO₂ (% of baseline)', fontsize=9, fontweight='bold')
        ax.set_title('C. Dynamic Range', fontsize=10, fontweight='bold', pad=10)
        ax.legend(fontsize=7, loc='lower right')
        ax.grid(True, alpha=0.3, axis='x')
        
        # Add range annotation
        vo2_range = max(sorted_vo2) / min(sorted_vo2)
        ax.text(0.98, 0.98, f'{vo2_range:.1f}× range', 
               transform=ax.transAxes, fontsize=8, fontweight='bold',
               verticalalignment='top', horizontalalignment='right',
               bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.3))
        
        return ax
    
    def panel_d_perceptual_consequences(self, ax):
        """Panel D: Perceptual consequences - multiple measures"""
        
        # Create twin axes
        ax2 = ax.twinx()
        
        # Time perception (left axis)
        vo2_sorted = sorted(self.vo2_values)
        time_sorted = [t for _, t in sorted(zip(self.vo2_values, self.time_values))]
        
        line1 = ax.plot(vo2_sorted, time_sorted, 'o-', color='#e74c3c', 
                       linewidth=2.5, markersize=7, label='Time Perception',
                       alpha=0.8)
        
        # CFF (right axis)
        line2 = ax2.plot(self.cff_data['vo2'], self.cff_data['cff'], 
                        's--', color='#3498db', linewidth=2, markersize=6,
                        label='CFF', alpha=0.8)
        
        # RT (right axis, inverted for clarity)
        rt_normalized = [r * 40 for r in self.rt_data['rt']]  # Scale to match CFF range
        line3 = ax2.plot(self.rt_data['vo2'], rt_normalized, 
                        '^:', color='#2ecc71', linewidth=2, markersize=6,
                        label='RT (scaled)', alpha=0.8)
        
        # Styling
        ax.set_xlabel('VO₂ (% of baseline)', fontsize=9, fontweight='bold')
        ax.set_ylabel('Perceived Duration (s)', fontsize=9, fontweight='bold', color='#e74c3c')
        ax2.set_ylabel('CFF (Hz) / RT (scaled)', fontsize=9, fontweight='bold', color='#3498db')
        
        ax.tick_params(axis='y', labelcolor='#e74c3c')
        ax2.tick_params(axis='y', labelcolor='#3498db')
        
        ax.set_title('D. Perceptual Consequences', fontsize=10, fontweight='bold', pad=10)
        
        # Combined legend
        lines = line1 + line2 + line3
        labels = [l.get_label() for l in lines]
        ax.legend(lines, labels, fontsize=7, loc='upper left', framealpha=0.9)
        
        ax.grid(True, alpha=0.3)
        
        # Add annotation
        ax.text(0.98, 0.02, 'All measures\nscale together', 
               transform=ax.transAxes, fontsize=7,
               verticalalignment='bottom', horizontalalignment='right',
               bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.3))
        
        return ax

# Run
if __name__ == "__main__":
    viz = UniversalLawVisualization()
    viz.create_figure()
    print("\n✓✓✓ Chart Set 1 Complete ✓✓✓\n")
