import json
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import seaborn as sns
from pathlib import Path

def load_quantum_data(filepath):
    """Load heartbeat perception quantum data."""
    with open(filepath, 'r') as f:
        return json.load(f)

def create_perception_quantum_panel(data):
    """
    Panel 2: Perception Quantum Boundaries
    Shows heartbeat as fundamental unit of conscious perception.
    """
    
    plt.style.use('seaborn-v0_8-white')
    
    fig = plt.figure(figsize=(22, 14))
    gs = GridSpec(2, 2, figure=fig, hspace=0.35, wspace=0.35)
    
    # Extract data
    hypothesis = data['hypothesis']
    author_insight = data['author_insight']
    
    # Panel A: Heartbeat as Quantum Boundary
    ax1 = fig.add_subplot(gs[0, 0])
    
    # Create visualization of quantum perception units
    n_beats = 10
    beat_interval = 0.43  # seconds (from previous data)
    t = np.linspace(0, n_beats * beat_interval, 1000)
    
    # Create perception quantum states
    perception_states = np.zeros(len(t))
    
    for i in range(n_beats):
        beat_time = i * beat_interval
        
        # Each heartbeat creates a perception quantum
        mask = (t >= beat_time) & (t < beat_time + beat_interval)
        
        # Quantum state: rises during interval, collapses at next beat
        t_local = t[mask] - beat_time
        perception_states[mask] = 1 - np.exp(-t_local / (beat_interval * 0.3))
    
    # Plot
    ax1.plot(t, perception_states, linewidth=3, color='#3498db', alpha=0.8)
    ax1.fill_between(t, 0, perception_states, alpha=0.3, color='#3498db')
    
    # Mark heartbeats
    for i in range(n_beats + 1):
        beat_time = i * beat_interval
        ax1.axvline(beat_time, color='red', linestyle='--', 
                   linewidth=2, alpha=0.7)
        
        if i < n_beats:
            # Add quantum number
            ax1.text(beat_time + beat_interval/2, 0.5, f'Q{i+1}',
                    fontsize=14, fontweight='bold', ha='center',
                    bbox=dict(boxstyle='round', facecolor='yellow',
                             alpha=0.8, edgecolor='black', linewidth=2))
    
    ax1.set_xlabel('Time (s)', fontsize=14, fontweight='bold')
    ax1.set_ylabel('Perception Quantum State', fontsize=14, fontweight='bold')
    ax1.set_title('A', fontsize=18, fontweight='bold', loc='left', pad=15)
    ax1.grid(alpha=0.3)
    ax1.set_ylim(-0.1, 1.2)
    
    # Add note
    textstr = ('Each heartbeat\ndefines one\nperception quantum\n\n'
              'Red lines =\nQuantum boundaries')
    props = dict(boxstyle='round', facecolor='lightblue', alpha=0.9,
                edgecolor='black', linewidth=2)
    ax1.text(0.02, 0.98, textstr, transform=ax1.transAxes, fontsize=11,
            verticalalignment='top', bbox=props, fontweight='bold')
    
    # Panel B: Oscillatory Cycle Convergence
    ax2 = fig.add_subplot(gs[0, 1])
    
    # Show multiple oscillatory cycles converging to heartbeat
    t_cycle = np.linspace(0, beat_interval * 3, 1000)
    
    # Different oscillatory frequencies
    frequencies = {
        'Neural α (10 Hz)': 10,
        'Neural β (20 Hz)': 20,
        'Neural γ (40 Hz)': 40,
        'Molecular (100 Hz)': 100
    }
    
    colors_osc = ['#FFD700', '#32CD32', '#1E90FF', '#9370DB']
    
    for (name, freq), color in zip(frequencies.items(), colors_osc):
        oscillation = np.sin(2 * np.pi * freq * t_cycle)
        ax2.plot(t_cycle, oscillation, linewidth=2, alpha=0.7,
                color=color, label=name)
    
    # Mark heartbeat boundaries
    for i in range(4):
        beat_time = i * beat_interval
        ax2.axvline(beat_time, color='red', linestyle='--',
                   linewidth=2.5, alpha=0.7)
    
    ax2.set_xlabel('Time (s)', fontsize=14, fontweight='bold')
    ax2.set_ylabel('Oscillation Amplitude', fontsize=14, fontweight='bold')
    ax2.set_title('B', fontsize=18, fontweight='bold', loc='left', pad=15)
    ax2.legend(loc='upper right', fontsize=10, framealpha=0.95)
    ax2.grid(alpha=0.3)
    
    # Add note
    textstr = ('All oscillations\nmust complete\nwithin heartbeat\nboundary')
    ax2.text(0.02, 0.02, textstr, transform=ax2.transAxes, fontsize=11,
            verticalalignment='bottom', bbox=dict(boxstyle='round',
            facecolor='lightgreen', alpha=0.9, edgecolor='darkgreen',
            linewidth=2), fontweight='bold')
    
    # Panel C: Conscious vs Unconscious States
    ax3 = fig.add_subplot(gs[1, 0])
    
    # Create comparison
    states = ['Conscious\n(Awake)', 'Sleep\n(Dreaming)', 'Deep Sleep', 
             'Coma\n(No Resonance)']
    
    # Resonance quality for each state
    resonance_quality = [1.0, 0.6, 0.2, 0.0]
    heartbeat_present = [1.0, 1.0, 1.0, 1.0]  # All have heartbeats
    perception_active = [1.0, 0.6, 0.1, 0.0]  # But not all perceive
    
    x = np.arange(len(states))
    width = 0.25
    
    bars1 = ax3.bar(x - width, heartbeat_present, width, label='Heartbeat Present',
                   color='#e74c3c', alpha=0.8, edgecolor='black', linewidth=2)
    bars2 = ax3.bar(x, resonance_quality, width, label='Resonance Quality',
                   color='#3498db', alpha=0.8, edgecolor='black', linewidth=2)
    bars3 = ax3.bar(x + width, perception_active, width, label='Perception Active',
                   color='#2ecc71', alpha=0.8, edgecolor='black', linewidth=2)
    
    ax3.set_ylabel('Normalized Value', fontsize=14, fontweight='bold')
    ax3.set_xticks(x)
    ax3.set_xticklabels(states, fontsize=12, fontweight='bold')
    ax3.set_title('C', fontsize=18, fontweight='bold', loc='left', pad=15)
    ax3.legend(loc='upper right', fontsize=11, framealpha=0.95)
    ax3.grid(alpha=0.3, axis='y')
    ax3.set_ylim(0, 1.2)
    
    # Add values on bars
    for bars in [bars1, bars2, bars3]:
        for bar in bars:
            height = bar.get_height()
            if height > 0:
                ax3.text(bar.get_x() + bar.get_width()/2., height + 0.02,
                        f'{height:.1f}', ha='center', va='bottom',
                        fontsize=10, fontweight='bold')
    
    # Add critical note
    textstr = ('CRITICAL:\nComa patients have\nheartbeats but\ncannot resonate\n\n'
              'Consciousness ≠\nHeartbeat alone')
    ax3.text(0.98, 0.98, textstr, transform=ax3.transAxes, fontsize=11,
            verticalalignment='top', horizontalalignment='right',
            bbox=dict(boxstyle='round', facecolor='yellow',
                     alpha=0.9, edgecolor='red', linewidth=3),
            fontweight='bold')
    
    # Panel D: Perception Quantum Energy Levels
    ax4 = fig.add_subplot(gs[1, 1])
    
    # Create energy level diagram
    ax4.axis('off')
    
    # Energy levels
    levels = [0, 1, 2, 3, 4]
    level_heights = [0.1, 0.3, 0.5, 0.7, 0.9]
    level_labels = ['Ground State\n(Coma)', 'Deep Sleep', 'Light Sleep',
                   'Drowsy', 'Fully Conscious']
    level_colors = ['#8B0000', '#FF4500', '#FFA500', '#FFD700', '#00FF00']
    
    # Draw levels
    for i, (height, label, color) in enumerate(zip(level_heights, level_labels, level_colors)):
        # Level line
        ax4.plot([0.2, 0.8], [height, height], linewidth=4,
                color=color, alpha=0.8)
        
        # Label
        ax4.text(0.85, height, label, fontsize=11, fontweight='bold',
                va='center', ha='left')
        
        # Energy value
        ax4.text(0.15, height, f'E{i}', fontsize=12, fontweight='bold',
                va='center', ha='right',
                bbox=dict(boxstyle='round', facecolor='white',
                         alpha=0.9, edgecolor='black', linewidth=1))
    
    # Draw transitions
    for i in range(len(levels) - 1):
        y1 = level_heights[i]
        y2 = level_heights[i + 1]
        
        # Upward arrow (requires energy from heartbeat)
        ax4.annotate('', xy=(0.5, y2), xytext=(0.5, y1),
                    arrowprops=dict(arrowstyle='->', lw=2, color='blue'))
        
        # Label
        ax4.text(0.52, (y1 + y2)/2, 'Heartbeat\nResonance',
                fontsize=8, ha='left', va='center',
                bbox=dict(boxstyle='round', facecolor='lightblue',
                         alpha=0.7, edgecolor='blue'))
    
    # Title
    ax4.text(0.5, 0.98, 'Perception Quantum Energy Levels',
            fontsize=16, fontweight='bold', ha='center', va='top',
            transform=ax4.transAxes)
    
    # Note
    textstr = ('Heartbeat provides\nenergy for quantum\ntransitions\n\n'
              'No resonance =\nStuck at ground state')
    ax4.text(0.5, 0.02, textstr, fontsize=11, ha='center', va='bottom',
            transform=ax4.transAxes,
            bbox=dict(boxstyle='round', facecolor='wheat',
                     alpha=0.9, edgecolor='black', linewidth=2),
            fontweight='bold')
    
    ax4.set_xlim(0, 1)
    ax4.set_ylim(0, 1)
    ax4.set_title('D', fontsize=18, fontweight='bold', loc='left', pad=20)
    
    # Overall title
    fig.suptitle('Heartbeat as Fundamental Quantum Boundary of Conscious Perception',
                fontsize=18, fontweight='bold', y=0.995)
    
    plt.tight_layout()
    return fig

def main():
    """Main function."""
    
    data_path = Path('public/heartbeat_perception_quantum_20251015_000448.json')
    
    print("="*70)
    print("GENERATING PERCEPTION QUANTUM BOUNDARIES PANEL")
    print("="*70)
    
    data = load_quantum_data(data_path)
    
    output_dir = Path('output')
    output_dir.mkdir(exist_ok=True)
    
    print("\nGenerating Panel 2: Perception Quantum...")
    fig = create_perception_quantum_panel(data)
    fig.savefig(output_dir / 'figure_perception_quantum_boundaries.png',
                dpi=300, bbox_inches='tight')
    fig.savefig(output_dir / 'figure_perception_quantum_boundaries.pdf',
                bbox_inches='tight')
    print("✓ Panel 2 saved")
    
    print("\n" + "="*70)
    print("PERCEPTION QUANTUM BOUNDARIES COMPLETE")
    print("="*70)
    
    plt.show()

if __name__ == "__main__":
    main()
