import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
from mpl_toolkits.mplot3d.art3d import Poly3DCollection


if __name__ == "__main__":
    fig = plt.figure(figsize=(16, 12))

    # ============================================================
    # PANEL A: Scale Hierarchy
    # ============================================================
    ax1 = plt.subplot(2, 2, 1)
    scales = {
        'Planck\nTime': 5.39e-44,
        'H⁺\nCoherence': 2.46e-14,
        'Neural\nSpike': 1e-3,
        'Heartbeat\nFrame': 0.833,
        'Conscious\nThought': 1.0
    }
    scale_names = list(scales.keys())
    scale_values = list(scales.values())
    colors_scale = ['purple', 'red', 'orange', 'blue', 'green']

    y_positions = np.arange(len(scales))
    bars = ax1.barh(y_positions, scale_values, color=colors_scale, 
                    edgecolor='black', linewidth=2, alpha=0.8)
    ax1.set_xscale('log')
    ax1.set_xlabel('Time (seconds)', fontsize=13, fontweight='bold')
    ax1.set_title('(A) Reality Hierarchy: Planck → Consciousness', 
                fontsize=14, fontweight='bold')
    ax1.set_yticks(y_positions)
    ax1.set_yticklabels(scale_names, fontsize=11, fontweight='bold')
    ax1.grid(True, alpha=0.3, axis='x')

    # Highlight H+ as bridge
    bars[1].set_edgecolor('red')
    bars[1].set_linewidth(4)
    ax1.annotate('REALITY\nSUBSTRATE', xy=(scale_values[1], 1), 
                xytext=(scale_values[1]*1e10, 1),
                arrowprops=dict(arrowstyle='->', lw=3, color='red'),
                fontsize=11, fontweight='bold', color='red',
                bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.9))

    # Add arrows showing emergence
    for i in range(len(scales)-1):
        ax1.annotate('', xy=(scale_values[i+1], i+1), 
                    xytext=(scale_values[i], i),
                    arrowprops=dict(arrowstyle='->', lw=2, color='black', alpha=0.5))

    # ============================================================
    # PANEL B: Reality Refresh Rate
    # ============================================================
    ax2 = plt.subplot(2, 2, 2)
    h_coherence_time = 2.46e-14  # seconds
    refresh_rate = 1 / h_coherence_time  # Hz

    # Create pulses
    time_fs = np.linspace(0, 100, 1000)  # femtoseconds
    pulses = np.zeros_like(time_fs)
    pulse_times = np.arange(0, 100, 24.6)
    for pt in pulse_times:
        idx = np.argmin(np.abs(time_fs - pt))
        pulses[max(0, idx-5):min(len(pulses), idx+5)] = 1.0

    ax2.fill_between(time_fs, 0, pulses, color='red', alpha=0.7, 
                    edgecolor='black', linewidth=2)
    ax2.set_xlabel('Time (femtoseconds)', fontsize=13, fontweight='bold')
    ax2.set_ylabel('Reality Frame', fontsize=13, fontweight='bold')
    ax2.set_title('(B) Reality Refresh Rate: 24.6 fs per Frame', 
                fontsize=14, fontweight='bold')
    ax2.set_ylim([0, 1.2])
    ax2.grid(True, alpha=0.3)

    # Add annotations
    ax2.text(50, 1.1, f'Refresh Rate: {refresh_rate:.2e} Hz', 
            ha='center', fontsize=11, fontweight='bold',
            bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.9))

    for i, pt in enumerate(pulse_times[:3]):
        ax2.annotate(f'Frame {i+1}', xy=(pt, 1.0), xytext=(pt, 0.5),
                    ha='center', fontsize=9, fontweight='bold')

    # ============================================================
    # PANEL C: Reality Container (3D)
    # ============================================================
    ax3 = plt.subplot(2, 2, 3, projection='3d')

    # Create H+ field manifold
    u = np.linspace(0, 2*np.pi, 50)
    v = np.linspace(0, np.pi, 50)
    U, V = np.meshgrid(u, v)

    # Reality container as sphere
    R = 1.0
    X = R * np.sin(V) * np.cos(U)
    Y = R * np.sin(V) * np.sin(U)
    Z = R * np.cos(V)

    # Color by "reality strength"
    colors_surf = np.sqrt(X**2 + Y**2 + Z**2)
    surf = ax3.plot_surface(X, Y, Z, facecolors=plt.cm.Reds(colors_surf/colors_surf.max()),
                            alpha=0.6, edgecolor='none')

    ax3.set_xlabel('X', fontsize=11, fontweight='bold')
    ax3.set_ylabel('Y', fontsize=11, fontweight='bold')
    ax3.set_zlabel('Z', fontsize=11, fontweight='bold')
    ax3.set_title('(C) H⁺-Defined Reality Container', fontsize=14, fontweight='bold', pad=20)

    # Add central point
    ax3.scatter([0], [0], [0], color='red', s=200, marker='*', 
                edgecolors='black', linewidth=2, label='H⁺ Source')
    ax3.legend(loc='upper right', fontsize=10)

    # ============================================================
    # PANEL D: Consciousness Within Container
    # ============================================================
    ax4 = plt.subplot(2, 2, 4, projection='3d')

    # Reality container (wireframe)
    ax4.plot_wireframe(X, Y, Z, color='red', alpha=0.2, linewidth=0.5)

    # Perception manifold (blue)
    t_p = np.linspace(0, 4*np.pi, 100)
    x_p = 0.5 * np.cos(t_p)
    y_p = 0.5 * np.sin(t_p)
    z_p = 0.3 * np.sin(2*t_p)
    ax4.plot(x_p, y_p, z_p, 'b-', linewidth=3, label='Perception (P)', alpha=0.8)

    # Thought manifold (green)
    t_t = np.linspace(0, 4*np.pi, 100)
    x_t = 0.6 * np.cos(t_t + np.pi/4)
    y_t = 0.6 * np.sin(t_t + np.pi/4)
    z_t = 0.4 * np.cos(2*t_t)
    ax4.plot(x_t, y_t, z_t, 'g-', linewidth=3, label='Thought (T)', alpha=0.8)

    # Consciousness vectors (P-T separation)
    n_vectors = 10
    for i in range(0, len(t_p), len(t_p)//n_vectors):
        ax4.plot([x_p[i], x_t[i]], [y_p[i], y_t[i]], [z_p[i], z_t[i]], 
                'purple', linewidth=2, alpha=0.6)

    ax4.set_xlabel('X', fontsize=11, fontweight='bold')
    ax4.set_ylabel('Y', fontsize=11, fontweight='bold')
    ax4.set_zlabel('Z', fontsize=11, fontweight='bold')
    ax4.set_title('(D) Consciousness Emerges Within Reality', 
                fontsize=14, fontweight='bold', pad=20)
    ax4.legend(loc='upper right', fontsize=10)

    # Add text annotation
    ax4.text2D(0.5, 0.95, r'$\mathbf{C} = ||\mathbf{P} - \mathbf{T}||$ within $\mathcal{R}_{H^+}$', 
            transform=ax4.transAxes, ha='center', fontsize=12, fontweight='bold',
            bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.9))

    # Main title
    fig.suptitle('H⁺ as Reality Substrate: The Container for Consciousness', 
                fontsize=17, fontweight='bold', y=0.98)

    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.savefig('figure_reality_substrate.png', dpi=300, bbox_inches='tight', facecolor='white')
    print("✓ Saved: figure_reality_substrate.png")
    plt.show()
