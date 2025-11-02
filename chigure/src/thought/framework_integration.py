import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from mpl_toolkits.mplot3d import Axes3D
import seaborn as sns
from pathlib import Path

def create_framework_integration_figure():
    """
    Master Figure 1: Three-Paper Integration
    Shows how all three papers connect into unified consciousness framework.
    """
    
    plt.style.use('seaborn-v0_8-white')
    
    fig = plt.figure(figsize=(24, 16))
    gs = GridSpec(2, 2, figure=fig, hspace=0.3, wspace=0.3)
    
    # Panel A: Thought Manifold from Biomechanics (Paper 1)
    ax1 = fig.add_subplot(gs[0, 0], projection='3d')
    
    # Simulate running trajectory with thought signatures
    t = np.linspace(0, 10, 1000)
    
    # Base trajectory (smooth running)
    x_base = t * 4  # 4 m/s forward
    y_base = 0.5 * np.sin(2 * np.pi * 0.5 * t)  # Slight lateral oscillation
    
    # Add thought perturbations (decision moments)
    thought_times = [2.5, 5.0, 7.5]
    x = x_base.copy()
    y = y_base.copy()
    
    for tt in thought_times:
        mask = (t > tt) & (t < tt + 0.5)
        x[mask] += 0.3 * np.exp(-(t[mask] - tt) / 0.2)
        y[mask] += 0.2 * np.sin(10 * (t[mask] - tt))
    
    # Calculate acceleration and jerk (thought signatures)
    velocity = np.gradient(x)
    acceleration = np.gradient(velocity)
    jerk = np.gradient(acceleration)
    
    # Plot thought manifold
    scatter = ax1.scatter(acceleration, jerk, velocity, c=t, cmap='viridis',
                         s=30, alpha=0.6, edgecolors='black', linewidth=0.3)
    
    # Mark thought moments
    for tt in thought_times:
        idx = np.argmin(np.abs(t - tt))
        ax1.scatter([acceleration[idx]], [jerk[idx]], [velocity[idx]],
                   s=300, c='red', marker='*', edgecolors='black',
                   linewidth=2, zorder=5)
    
    ax1.set_xlabel('Acceleration (m/s²)', fontsize=11, fontweight='bold')
    ax1.set_ylabel('Jerk (m/s³)', fontsize=11, fontweight='bold')
    ax1.set_zlabel('Velocity (m/s)', fontsize=11, fontweight='bold')
    ax1.set_title('A: Thought Manifold (Paper 1)\nBiomechanical Signatures',
                 fontsize=14, fontweight='bold', pad=20)
    
    # Add colorbar
    cbar = plt.colorbar(scatter, ax=ax1, pad=0.1, shrink=0.8)
    cbar.set_label('Time (s)', fontsize=10, fontweight='bold')
    
    # Add annotation
    ax1.text2D(0.02, 0.98, 'Red stars = Thought events\n(Decision moments)',
              transform=ax1.transAxes, fontsize=10, verticalalignment='top',
              bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.8,
                       edgecolor='red', linewidth=2), fontweight='bold')
    
    # Panel B: Perception Quantization by Heartbeat (Paper 2)
    ax2 = fig.add_subplot(gs[0, 1])
    
    # Simulate heartbeat and perception frames
    duration = 5
    t_fine = np.linspace(0, duration, 5000)
    
    # Heartbeat signal (72 bpm = 1.2 Hz)
    heart_rate = 1.2
    heartbeat = np.sin(2 * np.pi * heart_rate * t_fine)
    
    # O2 equilibrium (perturbed by heartbeat)
    o2_baseline = 0.95
    o2_equilibrium = o2_baseline * np.ones(len(t_fine))
    
    # Add perturbations at each heartbeat
    rr_interval = 1 / heart_rate
    n_beats = int(duration / rr_interval)
    
    for i in range(n_beats):
        beat_time = i * rr_interval
        mask = t_fine >= beat_time
        time_since_beat = t_fine[mask] - beat_time
        
        # Exponential recovery
        tau = 0.0005  # 0.5 ms restoration time
        recovery = 1 - 0.05 * np.exp(-time_since_beat / tau)
        o2_equilibrium[mask] = np.minimum(o2_equilibrium[mask], o2_baseline * recovery)
    
    # Perception frames (occur at restoration)
    perception_rate = 1 / tau  # ~2000 Hz
    perception_times = np.arange(0, duration, 1/perception_rate)
    
    # Plot
    ax2_twin = ax2.twinx()
    
    line1 = ax2.plot(t_fine, heartbeat, linewidth=2, color='#e74c3c',
                    alpha=0.7, label='Heartbeat')
    line2 = ax2_twin.plot(t_fine, o2_equilibrium, linewidth=2.5,
                         color='#3498db', alpha=0.8, label='O₂ Equilibrium')
    
    # Mark heartbeats
    for i in range(n_beats):
        beat_time = i * rr_interval
        ax2.axvline(beat_time, color='red', linestyle='--',
                   linewidth=1.5, alpha=0.5)
    
    # Show perception frames (sample)
    sample_frames = perception_times[::100]  # Show every 100th frame
    for pf in sample_frames[:20]:
        if pf < duration:
            ax2.axvline(pf, color='green', linestyle='-',
                       linewidth=0.5, alpha=0.3)
    
    ax2.set_xlabel('Time (s)', fontsize=12, fontweight='bold')
    ax2.set_ylabel('Heartbeat Signal', fontsize=11, fontweight='bold',
                  color='#e74c3c')
    ax2_twin.set_ylabel('O₂ Saturation', fontsize=11, fontweight='bold',
                       color='#3498db')
    ax2.set_title('B: Perception Quantization (Paper 2)\nHeartbeat Creates Perception Frames',
                 fontsize=14, fontweight='bold', pad=15)
    ax2.tick_params(axis='y', labelcolor='#e74c3c')
    ax2_twin.tick_params(axis='y', labelcolor='#3498db')
    ax2.grid(alpha=0.3)
    
    # Legend
    lines = line1 + line2
    labels = [l.get_label() for l in lines]
    ax2.legend(lines, labels, loc='upper right', fontsize=10, framealpha=0.95)
    
    # Annotation
    textstr = (f'Heart Rate: {heart_rate:.1f} Hz\n'
              f'RR Interval: {rr_interval*1000:.0f} ms\n'
              f'Restoration: {tau*1000:.2f} ms\n'
              f'Perception Rate: {perception_rate:.0f} Hz\n\n'
              f'Red lines = Heartbeats\n'
              f'Green lines = Perception frames')
    props = dict(boxstyle='round', facecolor='lightblue', alpha=0.9,
                edgecolor='black', linewidth=2)
    ax2.text(0.02, 0.98, textstr, transform=ax2.transAxes, fontsize=9,
            verticalalignment='top', bbox=props, family='monospace',
            fontweight='bold')
    
    # Panel C: Consciousness as Geometric Residual (Paper 3)
    ax3 = fig.add_subplot(gs[1, 0], projection='3d')
    
    # Create perception and thought manifolds
    t_manifold = np.linspace(0, 2*np.pi, 200)
    s_manifold = np.linspace(0, 2*np.pi, 200)
    T_grid, S_grid = np.meshgrid(t_manifold, s_manifold)
    
    # Perception manifold (smooth surface)
    X_perception = np.cos(T_grid) * (3 + np.cos(S_grid))
    Y_perception = np.sin(T_grid) * (3 + np.cos(S_grid))
    Z_perception = np.sin(S_grid)
    
    # Thought manifold (offset and rotated)
    X_thought = np.cos(T_grid) * (3 + np.cos(S_grid)) + 1
    Y_thought = np.sin(T_grid) * (3 + np.cos(S_grid)) + 0.5
    Z_thought = np.sin(S_grid) + 0.5
    
    # Plot manifolds
    surf1 = ax3.plot_surface(X_perception, Y_perception, Z_perception,
                            alpha=0.6, cmap='Blues', edgecolor='none')
    surf2 = ax3.plot_surface(X_thought, Y_thought, Z_thought,
                            alpha=0.6, cmap='Reds', edgecolor='none')
    
    # Draw residual vectors (sample points)
    sample_indices = np.random.choice(len(t_manifold), 30, replace=False)
    
    for idx in sample_indices:
        i = idx % X_perception.shape[0]
        j = idx % X_perception.shape[1]
        
        x1, y1, z1 = X_perception[i,j], Y_perception[i,j], Z_perception[i,j]
        x2, y2, z2 = X_thought[i,j], Y_thought[i,j], Z_thought[i,j]
        
        ax3.plot([x1, x2], [y1, y2], [z1, z2], 'g-', linewidth=2, alpha=0.7)
        
        # Arrow at end
        ax3.scatter([x2], [y2], [z2], c='green', s=50, marker='>')
    
    ax3.set_xlabel('Spatial X', fontsize=11, fontweight='bold')
    ax3.set_ylabel('Spatial Y', fontsize=11, fontweight='bold')
    ax3.set_zlabel('Velocity', fontsize=11, fontweight='bold')
    ax3.set_title('C: Consciousness Manifold (Paper 3)\nGeometric Residual',
                 fontsize=14, fontweight='bold', pad=20)
    
    # Add legend manually
    from matplotlib.patches import Patch
    legend_elements = [
        Patch(facecolor='blue', alpha=0.6, label='Perception Manifold'),
        Patch(facecolor='red', alpha=0.6, label='Thought Manifold'),
        Patch(facecolor='green', alpha=0.7, label='Consciousness (Residual)')
    ]
    ax3.legend(handles=legend_elements, loc='upper left', fontsize=10,
              framealpha=0.95)
    
    # Annotation
    ax3.text2D(0.02, 0.02, 'Green vectors = Consciousness\n|C| = ||P - T||',
              transform=ax3.transAxes, fontsize=10, verticalalignment='bottom',
              bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.9,
                       edgecolor='darkgreen', linewidth=2), fontweight='bold')
    
    # Panel D: Complete Framework Integration
    ax4 = fig.add_subplot(gs[1, 1])
    ax4.axis('off')
    
    # Create flowchart
    from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
    
    # Box positions
    boxes = {
        'paper1': (0.1, 0.75, 0.25, 0.15),
        'paper2': (0.65, 0.75, 0.25, 0.15),
        'paper3': (0.375, 0.45, 0.25, 0.15),
        'consciousness': (0.3, 0.1, 0.4, 0.2)
    }
    
    # Draw boxes
    box1 = FancyBboxPatch((boxes['paper1'][0], boxes['paper1'][1]),
                          boxes['paper1'][2], boxes['paper1'][3],
                          boxstyle="round,pad=0.01", linewidth=3,
                          edgecolor='#e74c3c', facecolor='#ffcccc',
                          transform=ax4.transAxes, zorder=2)
    ax4.add_patch(box1)
    
    box2 = FancyBboxPatch((boxes['paper2'][0], boxes['paper2'][1]),
                          boxes['paper2'][2], boxes['paper2'][3],
                          boxstyle="round,pad=0.01", linewidth=3,
                          edgecolor='#3498db', facecolor='#cce5ff',
                          transform=ax4.transAxes, zorder=2)
    ax4.add_patch(box2)
    
    box3 = FancyBboxPatch((boxes['paper3'][0], boxes['paper3'][1]),
                          boxes['paper3'][2], boxes['paper3'][3],
                          boxstyle="round,pad=0.01", linewidth=3,
                          edgecolor='#2ecc71', facecolor='#ccffcc',
                          transform=ax4.transAxes, zorder=2)
    ax4.add_patch(box3)
    
    box4 = FancyBboxPatch((boxes['consciousness'][0], boxes['consciousness'][1]),
                          boxes['consciousness'][2], boxes['consciousness'][3],
                          boxstyle="round,pad=0.01", linewidth=4,
                          edgecolor='#9b59b6', facecolor='#e6ccff',
                          transform=ax4.transAxes, zorder=2)
    ax4.add_patch(box4)
    
    # Add text to boxes
    ax4.text(0.225, 0.825, 'PAPER 1', ha='center', va='center',
            fontsize=14, fontweight='bold', transform=ax4.transAxes)
    ax4.text(0.225, 0.79, 'Sprint Running\nThought Validation',
            ha='center', va='center', fontsize=10, transform=ax4.transAxes)
    ax4.text(0.225, 0.76, 'Thought → Biomechanics',
            ha='center', va='center', fontsize=9, style='italic',
            transform=ax4.transAxes)
    
    ax4.text(0.775, 0.825, 'PAPER 2', ha='center', va='center',
            fontsize=14, fontweight='bold', transform=ax4.transAxes)
    ax4.text(0.775, 0.79, 'Anthropometric-Cardiac\nOscillations',
            ha='center', va='center', fontsize=10, transform=ax4.transAxes)
    ax4.text(0.775, 0.76, 'Heartbeat → Perception',
            ha='center', va='center', fontsize=9, style='italic',
            transform=ax4.transAxes)
    
    ax4.text(0.5, 0.525, 'PAPER 3', ha='center', va='center',
            fontsize=14, fontweight='bold', transform=ax4.transAxes)
    ax4.text(0.5, 0.49, 'Geometry of\nConsciousness',
            ha='center', va='center', fontsize=10, transform=ax4.transAxes)
    ax4.text(0.5, 0.46, 'C = ||P - T||',
            ha='center', va='center', fontsize=9, style='italic',
            transform=ax4.transAxes)
    
    ax4.text(0.5, 0.2, 'UNIFIED FRAMEWORK', ha='center', va='center',
            fontsize=16, fontweight='bold', transform=ax4.transAxes)
    ax4.text(0.5, 0.145, 'Consciousness = Geometric Residual\nbetween Perception and Thought',
            ha='center', va='center', fontsize=11, transform=ax4.transAxes)
    ax4.text(0.5, 0.11, 'Quantized by Heartbeat | Measured via Movement',
            ha='center', va='center', fontsize=9, style='italic',
            transform=ax4.transAxes)
    
    # Draw arrows
    # Paper 1 to Paper 3
    arrow1 = FancyArrowPatch((0.225, 0.75), (0.425, 0.6),
                            arrowstyle='->', mutation_scale=30, linewidth=3,
                            color='#e74c3c', transform=ax4.transAxes, zorder=1)
    ax4.add_patch(arrow1)
    ax4.text(0.3, 0.67, 'Thought\nManifold', ha='center', va='center',
            fontsize=9, fontweight='bold', transform=ax4.transAxes,
            bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
    
    # Paper 2 to Paper 3
    arrow2 = FancyArrowPatch((0.775, 0.75), (0.575, 0.6),
                            arrowstyle='->', mutation_scale=30, linewidth=3,
                            color='#3498db', transform=ax4.transAxes, zorder=1)
    ax4.add_patch(arrow2)
    ax4.text(0.7, 0.67, 'Perception\nQuantization', ha='center', va='center',
            fontsize=9, fontweight='bold', transform=ax4.transAxes,
            bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
    
    # Paper 3 to Consciousness
    arrow3 = FancyArrowPatch((0.5, 0.45), (0.5, 0.3),
                            arrowstyle='->', mutation_scale=30, linewidth=3,
                            color='#2ecc71', transform=ax4.transAxes, zorder=1)
    ax4.add_patch(arrow3)
    ax4.text(0.55, 0.375, 'Geometric\nResidual', ha='center', va='center',
            fontsize=9, fontweight='bold', transform=ax4.transAxes,
            bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
    
    ax4.set_xlim(0, 1)
    ax4.set_ylim(0, 1)
    ax4.set_title('D: Complete Framework Integration',
                 fontsize=14, fontweight='bold', pad=15)
    
    # Overall title
    fig.suptitle('Three-Paper Framework: From Biomechanics to Consciousness Geometry',
                fontsize=20, fontweight='bold', y=0.98)
    
    plt.tight_layout()
    return fig

def main():
    print("="*80)
    print("GENERATING MASTER FIGURE 1: FRAMEWORK INTEGRATION")
    print("="*80)
    
    output_dir = Path('output/master_figures')
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print("\nCreating framework integration figure...")
    fig = create_framework_integration_figure()
    
    fig.savefig(output_dir / 'master_figure_1_framework_integration.png',
                dpi=300, bbox_inches='tight')
    fig.savefig(output_dir / 'master_figure_1_framework_integration.pdf',
                bbox_inches='tight')
    
    print("✓ Master Figure 1 saved")
    print(f"\nOutput location: {output_dir.absolute()}")
    
    plt.show()

if __name__ == "__main__":
    main()
