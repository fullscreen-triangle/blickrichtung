import json
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import seaborn as sns
from pathlib import Path

def load_reality_perception_data(filepath):
    """Load reality perception JSON data."""
    with open(filepath, 'r') as f:
        return json.load(f)

def create_coros_consciousness_panel(data):
    """
    COROS Watch Analysis: Focus on consciousness metrics and neural dynamics.
    Shows frame rate, perception bandwidth, and neural efficiency.
    """
    
    plt.style.use('seaborn-v0_8-whitegrid')
    
    fig = plt.figure(figsize=(20, 14))
    gs = GridSpec(2, 2, figure=fig, hspace=0.35, wspace=0.35)
    
    # Extract data
    consciousness = data['consciousness']
    neural = data['neural']
    metadata = data['metadata']
    
    # Panel A: Consciousness Frame Rate Analysis
    ax1 = fig.add_subplot(gs[0, 0])
    
    frame_rate = consciousness['frame_rate_hz']
    frame_duration = consciousness['frame_duration_ms']
    total_frames = consciousness['total_conscious_frames']
    duration = consciousness['total_duration_s']
    
    # Create timeline visualization
    t = np.linspace(0, duration, int(total_frames))
    
    # Simulate frame selection events
    frame_events = np.ones(len(t))
    
    # Plot as stem plot
    markerline, stemlines, baseline = ax1.stem(t, frame_events, 
                                                linefmt='g-', markerfmt='go',
                                                basefmt='k-')
    plt.setp(stemlines, linewidth=2, alpha=0.6)
    plt.setp(markerline, markersize=8, markeredgecolor='black', 
             markeredgewidth=1, alpha=0.8)
    
    ax1.set_xlabel('Time (s)', fontsize=14, fontweight='bold')
    ax1.set_ylabel('Conscious Frame', fontsize=14, fontweight='bold')
    ax1.set_title('A', fontsize=18, fontweight='bold', loc='left', pad=15)
    ax1.set_ylim(0, 1.5)
    ax1.set_yticks([0, 1])
    ax1.set_yticklabels(['', 'Frame'], fontsize=12)
    ax1.grid(alpha=0.3)
    
    # Add metrics box
    textstr = (f'Frame Rate: {frame_rate:.1f} Hz\n'
              f'Frame Duration: {frame_duration:.0f} ms\n'
              f'Total Frames: {total_frames}\n'
              f'Duration: {duration:.1f} s\n'
              f'State: {consciousness["interpretation"]}')
    props = dict(boxstyle='round', facecolor='lightblue', alpha=0.9,
                edgecolor='black', linewidth=2)
    ax1.text(0.02, 0.98, textstr, transform=ax1.transAxes, fontsize=11,
            verticalalignment='top', bbox=props, family='monospace',
            fontweight='bold')
    
    # Panel B: Perception Bandwidth & Cognitive Frequencies
    ax2 = fig.add_subplot(gs[0, 1])
    
    # Extract cognitive frequencies
    perception_bw = consciousness['perception_bandwidth']
    hrv_freq = consciousness['hrv_cognitive_freq_hz']
    motor_freq = consciousness['motor_cognitive_freq_hz']
    body_freq = consciousness['body_awareness_freq_hz']
    
    categories = ['Perception\nBandwidth', 'HRV\nCognitive', 
                 'Motor\nCognitive', 'Body\nAwareness']
    values = [perception_bw, hrv_freq, motor_freq, body_freq]
    colors = ['#e74c3c', '#3498db', '#2ecc71', '#f39c12']
    
    # Use dual y-axis (perception bandwidth is much larger)
    ax2_twin = ax2.twinx()
    
    bars1 = ax2.bar([0], [values[0]], color=colors[0], alpha=0.8,
                   edgecolor='black', linewidth=2, width=0.6)
    bars2 = ax2_twin.bar([1, 2, 3], values[1:], color=colors[1:], alpha=0.8,
                        edgecolor='black', linewidth=2, width=0.6)
    
    ax2.set_ylabel('Perception Bandwidth', fontsize=13, fontweight='bold',
                  color=colors[0])
    ax2_twin.set_ylabel('Cognitive Frequency (Hz)', fontsize=13, 
                       fontweight='bold', color='black')
    ax2.set_xticks([0, 1, 2, 3])
    ax2.set_xticklabels(categories, fontsize=11, fontweight='bold')
    ax2.set_title('B', fontsize=18, fontweight='bold', loc='left', pad=15)
    ax2.grid(alpha=0.3, axis='y')
    ax2.tick_params(axis='y', labelcolor=colors[0])
    
    # Add values on bars
    for bar, val in zip([bars1[0]], [values[0]]):
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height + 5,
                f'{val:.1f}', ha='center', va='bottom',
                fontsize=11, fontweight='bold', color=colors[0])
    
    for i, (bar, val) in enumerate(zip(bars2, values[1:])):
        height = bar.get_height()
        ax2_twin.text(bar.get_x() + bar.get_width()/2., height + 0.05,
                     f'{val:.1f} Hz', ha='center', va='bottom',
                     fontsize=11, fontweight='bold')
    
    # Panel C: Neural Firing Dynamics
    ax3 = fig.add_subplot(gs[1, 0])
    
    mean_firing = neural['mean_firing_rate_hz']
    total_events = neural['total_neural_events']
    neural_efficiency = neural['neural_efficiency']
    
    # Simulate neural firing pattern
    t_neural = np.linspace(0, duration, 1000)
    
    # Base firing rate with modulation
    firing_rate = mean_firing * (1 + 0.2 * np.sin(2*np.pi*0.5*t_neural) +
                                 0.1 * np.sin(2*np.pi*2*t_neural))
    
    ax3.plot(t_neural, firing_rate, linewidth=2.5, color='#9b59b6', alpha=0.8)
    ax3.fill_between(t_neural, 0, firing_rate, alpha=0.3, color='#9b59b6')
    
    # Add mean line
    ax3.axhline(mean_firing, color='red', linestyle='--', linewidth=2.5,
               label=f'Mean: {mean_firing:.1f} Hz')
    
    ax3.set_xlabel('Time (s)', fontsize=14, fontweight='bold')
    ax3.set_ylabel('Neural Firing Rate (Hz)', fontsize=14, fontweight='bold')
    ax3.set_title('C', fontsize=18, fontweight='bold', loc='left', pad=15)
    ax3.legend(loc='upper right', fontsize=11, framealpha=0.95)
    ax3.grid(alpha=0.3)
    
    # Add metrics
    textstr = (f'Total Events: {total_events}\n'
              f'Duration: {duration:.1f} s\n'
              f'Neural Efficiency: {neural_efficiency:.3f}')
    ax3.text(0.98, 0.98, textstr, transform=ax3.transAxes, fontsize=11,
            verticalalignment='top', horizontalalignment='right',
            bbox=props, family='monospace', fontweight='bold')
    
    # Panel D: Consciousness State Gauge
    ax4 = fig.add_subplot(gs[1, 1])
    
    # Create consciousness state visualization
    # Based on frame rate and neural efficiency
    consciousness_level = min(1.0, (frame_rate / 10) * neural_efficiency)
    
    # Create circular gauge
    theta = np.linspace(0, np.pi, 100)
    r = 1
    
    # Background arc
    ax4.plot(r * np.cos(theta), r * np.sin(theta), 'k-',
            linewidth=12, alpha=0.2)
    
    # Consciousness level arc
    theta_conscious = np.linspace(0, consciousness_level * np.pi, 100)
    
    # Color based on state
    if frame_duration > 500:
        color = '#3498db'  # Blue for meditative
        state_label = 'MEDITATIVE'
    elif frame_duration > 100:
        color = '#2ecc71'  # Green for normal
        state_label = 'NORMAL'
    else:
        color = '#e74c3c'  # Red for hyperactive
        state_label = 'HYPERACTIVE'
    
    ax4.plot(r * np.cos(theta_conscious), r * np.sin(theta_conscious),
            linewidth=12, alpha=0.9, color=color)
    
    # Add needle
    needle_angle = consciousness_level * np.pi
    ax4.plot([0, r * np.cos(needle_angle)], [0, r * np.sin(needle_angle)],
            'r-', linewidth=4)
    ax4.plot(0, 0, 'ro', markersize=20, markeredgecolor='black',
            markeredgewidth=2)
    
    # Add labels
    ax4.text(-1.3, 0, '0.0\nUnconscious', fontsize=11, fontweight='bold',
            ha='center', va='center')
    ax4.text(0, 1.3, '0.5\nNormal', fontsize=11, fontweight='bold',
            ha='center', va='center')
    ax4.text(1.3, 0, '1.0\nPeak', fontsize=11, fontweight='bold',
            ha='center', va='center')
    
    # Add current value
    ax4.text(0, -0.5, f'{consciousness_level:.3f}', fontsize=32,
            fontweight='bold', ha='center', va='center',
            bbox=dict(boxstyle='round', facecolor='yellow',
                     alpha=0.9, edgecolor='black', linewidth=3))
    
    ax4.text(0, -0.85, state_label, fontsize=16,
            fontweight='bold', ha='center', va='center',
            color=color)
    
    ax4.text(0, -1.1, f'COROS Watch', fontsize=14,
            fontweight='bold', ha='center', va='center',
            bbox=dict(boxstyle='round', facecolor='lightgray',
                     alpha=0.8, edgecolor='black', linewidth=2))
    
    ax4.set_xlim(-1.6, 1.6)
    ax4.set_ylim(-1.3, 1.6)
    ax4.set_aspect('equal')
    ax4.axis('off')
    ax4.set_title('D', fontsize=18, fontweight='bold', loc='left', pad=20)
    
    plt.tight_layout()
    return fig

def main():
    """Main function to generate COROS watch visualizations."""
    
    # Load data
    data_path = Path('public/reality_perception_coros_cleaned_20251013_000747_20251014_234018.json')
    data = load_reality_perception_data(data_path)
    
    # Create output directory
    output_dir = Path('output')
    output_dir.mkdir(exist_ok=True)
    
    print("="*70)
    print("GENERATING COROS WATCH ANALYSIS - CONSCIOUSNESS FOCUS")
    print("="*70)
    
    print("\nGenerating COROS Consciousness Panel...")
    fig = create_coros_consciousness_panel(data)
    fig.savefig(output_dir / 'figure_coros_consciousness.png',
                dpi=300, bbox_inches='tight')
    fig.savefig(output_dir / 'figure_coros_consciousness.pdf',
                bbox_inches='tight')
    print("✓ COROS panel saved")
    
    print("\n" + "="*70)
    print("COROS ANALYSIS COMPLETE")
    print("="*70)
    print(f"\nOutput location: {output_dir.absolute()}")
    print("\nKey Findings:")
    print(f"  • Frame Rate: {data['consciousness']['frame_rate_hz']:.1f} Hz")
    print(f"  • State: {data['consciousness']['interpretation']}")
    print(f"  • Neural Efficiency: {data['neural']['neural_efficiency']:.3f}")
    print(f"  • Total Frames: {data['consciousness']['total_conscious_frames']}")
    
    plt.show()

if __name__ == "__main__":
    main()
