"""
Figure Generation for Psychon Circuit Mechanics Paper

Generates panel figures for:
1. S-Entropy Coordinate System
2. Psychon: Trajectory-Terminus Pairs
3. Circuit Equivalence (R-C-L)
4. Consciousness as Geometric Intersection
5. Emergent Mental Phenomena

Each figure panel: 4 charts in a row, at least one 3D chart
Minimal text, publication quality
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.patches import Circle, Wedge, Rectangle, FancyArrowPatch
from matplotlib.collections import PatchCollection
from matplotlib import cm
from mpl_toolkits.mplot3d.art3d import Line3DCollection
from scipy.integrate import odeint
import os

# Set publication style
plt.rcParams.update({
    'font.size': 10,
    'font.family': 'serif',
    'axes.labelsize': 11,
    'axes.titlesize': 12,
    'xtick.labelsize': 9,
    'ytick.labelsize': 9,
    'legend.fontsize': 9,
    'figure.dpi': 150,
    'savefig.dpi': 300,
    'savefig.bbox': 'tight',
    'axes.linewidth': 1.2,
})

# Create output directory
os.makedirs('figures', exist_ok=True)


def figure1_sentropy_coordinates():
    """
    Figure 1: S-Entropy Coordinate System
    Panel A: 3D S-entropy space (Sk, St, Se)
    Panel B: Information deficit Sk distribution
    Panel C: Temporal progression St
    Panel D: Categorical entropy Se
    """
    fig = plt.figure(figsize=(16, 4))

    # Panel A: 3D S-Entropy Space
    ax1 = fig.add_subplot(141, projection='3d')

    # Generate sample points in S-space
    np.random.seed(42)
    n_points = 100

    # Clustered psychon states
    Sk = np.concatenate([
        np.random.beta(2, 5, n_points//3),
        np.random.beta(5, 2, n_points//3),
        np.random.beta(2, 2, n_points//3 + 1)
    ])
    St = np.concatenate([
        np.random.beta(2, 5, n_points//3),
        np.random.beta(3, 3, n_points//3),
        np.random.beta(5, 2, n_points//3 + 1)
    ])
    Se = np.concatenate([
        np.random.beta(5, 2, n_points//3),
        np.random.beta(2, 2, n_points//3),
        np.random.beta(2, 5, n_points//3 + 1)
    ])

    colors = cm.viridis(Se)
    ax1.scatter(Sk, St, Se, c=Se, cmap='viridis', s=30, alpha=0.7)

    # Draw unit cube boundary
    ax1.plot([0, 1], [0, 0], [0, 0], 'k-', alpha=0.3)
    ax1.plot([0, 0], [0, 1], [0, 0], 'k-', alpha=0.3)
    ax1.plot([0, 0], [0, 0], [0, 1], 'k-', alpha=0.3)
    ax1.plot([1, 1], [0, 1], [0, 0], 'k-', alpha=0.3)
    ax1.plot([1, 1], [0, 0], [0, 1], 'k-', alpha=0.3)
    ax1.plot([0, 1], [1, 1], [0, 0], 'k-', alpha=0.3)
    ax1.plot([0, 0], [1, 1], [0, 1], 'k-', alpha=0.3)
    ax1.plot([0, 1], [0, 0], [1, 1], 'k-', alpha=0.3)
    ax1.plot([0, 0], [0, 1], [1, 1], 'k-', alpha=0.3)
    ax1.plot([1, 1], [1, 1], [0, 1], 'k-', alpha=0.3)
    ax1.plot([1, 1], [0, 1], [1, 1], 'k-', alpha=0.3)
    ax1.plot([0, 1], [1, 1], [1, 1], 'k-', alpha=0.3)

    ax1.set_xlabel('$S_k$')
    ax1.set_ylabel('$S_t$')
    ax1.set_zlabel('$S_e$')
    ax1.set_title('(A) S-Entropy Space $\\mathcal{S}_N$')
    ax1.set_xlim(0, 1)
    ax1.set_ylim(0, 1)
    ax1.set_zlim(0, 1)

    # Panel B: Information Deficit
    ax2 = fig.add_subplot(142)

    # P(equivalence class) distribution
    P = np.linspace(0.01, 1, 100)
    Sk_values = -np.log(P)

    ax2.plot(P, Sk_values, 'b-', linewidth=2)
    ax2.fill_between(P, 0, Sk_values, alpha=0.3)

    # Mark key points
    ax2.plot(0.5, -np.log(0.5), 'ro', markersize=10)
    ax2.annotate('$P = 0.5$', xy=(0.5, -np.log(0.5)), xytext=(0.6, 1.5),
                fontsize=10, arrowprops=dict(arrowstyle='->', color='red'))

    ax2.set_xlabel('Probability $P$')
    ax2.set_ylabel('$S_k = -\\log P$')
    ax2.set_title('(B) Information Deficit')
    ax2.set_xlim(0, 1)
    ax2.set_ylim(0, 5)
    ax2.grid(True, alpha=0.3)

    # Panel C: Temporal Position
    ax3 = fig.add_subplot(143)

    # Steps to completion
    total_steps = 100
    current_steps = np.arange(0, total_steps + 1)
    St_values = current_steps / total_steps

    ax3.bar(current_steps[::10], St_values[::10], width=8, color='coral',
            edgecolor='darkred', alpha=0.7)

    # Progression arrow
    ax3.annotate('', xy=(90, 0.9), xytext=(10, 0.1),
                arrowprops=dict(arrowstyle='->', color='green', lw=2))

    ax3.set_xlabel('Steps to Completion')
    ax3.set_ylabel('$S_t = n / N$')
    ax3.set_title('(C) Temporal Position $S_t \\in [0, 1]$')
    ax3.set_xlim(0, 100)
    ax3.set_ylim(0, 1.1)

    # Panel D: Categorical Entropy
    ax4 = fig.add_subplot(144)

    # Shannon entropy for different distributions
    n_states = 10
    alphas = [0.5, 1.0, 2.0, 5.0]
    colors = ['red', 'orange', 'green', 'blue']

    x = np.arange(n_states)
    for alpha, color in zip(alphas, colors):
        # Dirichlet-like distribution
        p = np.random.dirichlet(np.ones(n_states) * alpha)
        p = np.sort(p)[::-1]
        Se = -np.sum(p * np.log(p + 1e-10))

        ax4.bar(x + 0.2 * (alphas.index(alpha) - 1.5), p, width=0.18,
               color=color, alpha=0.7, label=f'$S_e = {Se:.2f}$')

    ax4.set_xlabel('State Index')
    ax4.set_ylabel('Probability $p_i$')
    ax4.set_title('(D) Categorical Entropy $S_e$')
    ax4.legend(loc='upper right', fontsize=8)
    ax4.set_xticks(x)

    plt.tight_layout()
    plt.savefig('figures/fig1_sentropy_coordinates.png')
    plt.savefig('figures/fig1_sentropy_coordinates.pdf')
    plt.close()
    print("Generated: fig1_sentropy_coordinates")


def figure2_trajectory_terminus():
    """
    Figure 2: Psychon Trajectory-Terminus Pairs
    Panel A: 3D trajectories to same terminus
    Panel B: Context dependence (different paths)
    Panel C: Ternary address structure
    Panel D: Mental state non-identity
    """
    fig = plt.figure(figsize=(16, 4))

    # Panel A: 3D Trajectories
    ax1 = fig.add_subplot(141, projection='3d')

    # Different trajectories to same terminus
    t = np.linspace(0, 1, 100)

    # Terminus point
    terminus = np.array([0.7, 0.8, 0.5])
    ax1.scatter(*terminus, c='red', s=200, marker='*', label='Terminus $\\Gamma_f$')

    # Different trajectories (γ)
    trajectories = [
        {'start': [0.1, 0.1, 0.9], 'color': 'blue', 'style': '-'},
        {'start': [0.9, 0.1, 0.1], 'color': 'green', 'style': '--'},
        {'start': [0.1, 0.9, 0.1], 'color': 'purple', 'style': ':'},
        {'start': [0.5, 0.5, 0.9], 'color': 'orange', 'style': '-.'},
    ]

    for traj in trajectories:
        start = np.array(traj['start'])
        # Curved path to terminus
        path = np.outer(1-t**2, start) + np.outer(t**2, terminus)
        # Add some curvature
        path[:, 0] += 0.2 * np.sin(2*np.pi*t)
        path[:, 1] += 0.15 * np.sin(3*np.pi*t)

        ax1.plot(path[:, 0], path[:, 1], path[:, 2],
                traj['style'], color=traj['color'], linewidth=2)
        ax1.scatter(*start, c=traj['color'], s=50, marker='o')

    ax1.set_xlabel('$S_k$')
    ax1.set_ylabel('$S_t$')
    ax1.set_zlabel('$S_e$')
    ax1.set_title('(A) $\\mathcal{M} = (\\gamma, \\Gamma_f)$')
    ax1.set_xlim(0, 1)
    ax1.set_ylim(0, 1)
    ax1.set_zlim(0, 1)

    # Panel B: Context Dependence
    ax2 = fig.add_subplot(142)

    # Show same content, different context
    contexts = ['Party', 'Exam', 'Search', 'Memory']
    colors = ['#e74c3c', '#3498db', '#2ecc71', '#9b59b6']

    # Draw thought content (same for all)
    content_circle = Circle((0.5, 0.5), 0.15, fill=True, facecolor='yellow',
                            edgecolor='gold', linewidth=3, alpha=0.9)
    ax2.add_patch(content_circle)
    ax2.text(0.5, 0.5, 'Thought', ha='center', va='center', fontsize=9)

    # Draw different context paths
    angles = [45, 135, 225, 315]
    for i, (ctx, angle, color) in enumerate(zip(contexts, angles, colors)):
        rad = np.radians(angle)
        x_start = 0.5 + 0.4 * np.cos(rad)
        y_start = 0.5 + 0.4 * np.sin(rad)

        # Draw curved arrow
        arrow_path = np.array([
            [x_start, y_start],
            [0.5 + 0.25*np.cos(rad), 0.5 + 0.25*np.sin(rad)],
        ])

        ax2.annotate('', xy=(0.5 + 0.17*np.cos(rad), 0.5 + 0.17*np.sin(rad)),
                    xytext=(x_start, y_start),
                    arrowprops=dict(arrowstyle='->', color=color, lw=2,
                                  connectionstyle='arc3,rad=0.2'))

        ax2.text(x_start, y_start, ctx, ha='center', va='center',
                fontsize=9, color=color, fontweight='bold')

    ax2.set_xlim(0, 1)
    ax2.set_ylim(0, 1)
    ax2.set_aspect('equal')
    ax2.axis('off')
    ax2.set_title('(B) Same Content, Different States')

    # Panel C: Ternary Address
    ax3 = fig.add_subplot(143)

    # Draw ternary tree structure
    def draw_ternary_node(ax, x, y, level, address, max_level=3):
        if level >= max_level:
            ax.plot(x, y, 'ko', markersize=8)
            ax.text(x, y - 0.08, address, ha='center', fontsize=7)
            return

        # Draw branches
        dx = 0.3 / (level + 1)
        dy = 0.25

        for i, digit in enumerate([0, 1, 2]):
            new_x = x + (i - 1) * dx
            new_y = y - dy
            ax.plot([x, new_x], [y, new_y], 'k-', linewidth=1)
            draw_ternary_node(ax, new_x, new_y, level + 1,
                            address + str(digit), max_level)

    draw_ternary_node(ax3, 0.5, 0.95, 0, '', max_level=3)

    ax3.set_xlim(0, 1)
    ax3.set_ylim(0, 1)
    ax3.axis('off')
    ax3.set_title('(C) Ternary Address: $O(\\log_3 n)$')

    # Panel D: Mental State Non-Identity
    ax4 = fig.add_subplot(144)

    # Show γ₁ ≠ γ₂ ⟹ M₁ ≠ M₂
    categories = ['$\\gamma_1$', '$\\gamma_2$', '$\\Gamma_f$', '$\\mathcal{M}$']
    traj1_vals = [1, 0, 0.5, 0]
    traj2_vals = [0, 1, 0.5, 0]

    x = np.arange(len(categories))
    width = 0.35

    bars1 = ax4.bar(x[:3] - width/2, traj1_vals[:3], width, color='steelblue',
                    label='State 1', edgecolor='navy')
    bars2 = ax4.bar(x[:3] + width/2, traj2_vals[:3], width, color='coral',
                    label='State 2', edgecolor='darkred')

    # Add not-equal symbol
    ax4.text(3, 0.5, '$\\neq$', fontsize=30, ha='center', va='center')

    # M1 ≠ M2 bars
    ax4.bar(2.6, 0.8, 0.25, color='steelblue', edgecolor='navy')
    ax4.bar(3.4, 0.8, 0.25, color='coral', edgecolor='darkred')

    ax4.set_xticks(x)
    ax4.set_xticklabels(categories)
    ax4.set_ylabel('Value')
    ax4.set_title('(D) $\\gamma_1 \\neq \\gamma_2 \\Rightarrow \\mathcal{M}_1 \\neq \\mathcal{M}_2$')
    ax4.legend(loc='upper right')
    ax4.set_ylim(0, 1.2)

    plt.tight_layout()
    plt.savefig('figures/fig2_trajectory_terminus.png')
    plt.savefig('figures/fig2_trajectory_terminus.pdf')
    plt.close()
    print("Generated: fig2_trajectory_terminus")


def figure3_circuit_equivalence():
    """
    Figure 3: Circuit Equivalence (R-C-L)
    Panel A: 3D mode selection surface
    Panel B: R-C-L trichotomy in S-dimensions
    Panel C: S-entropy minimization
    Panel D: Impedance frequency response
    """
    fig = plt.figure(figsize=(16, 4))

    # Panel A: 3D Mode Selection
    ax1 = fig.add_subplot(141, projection='3d')

    # Create surface showing which mode dominates
    Sk = np.linspace(0, 1, 30)
    St = np.linspace(0, 1, 30)
    Sk_grid, St_grid = np.meshgrid(Sk, St)

    # Mode selection: highest S-coordinate determines mode
    # R = Sk, C = St, L = 1 - Sk - St (approximately Se)
    Se_grid = np.clip(1 - Sk_grid - St_grid, 0, 1)

    # Color by dominant mode
    mode = np.zeros_like(Sk_grid)
    mode[Sk_grid > np.maximum(St_grid, Se_grid)] = 0  # R (red)
    mode[St_grid > np.maximum(Sk_grid, Se_grid)] = 0.5  # C (green)
    mode[Se_grid > np.maximum(Sk_grid, St_grid)] = 1  # L (blue)

    surf = ax1.plot_surface(Sk_grid, St_grid, mode, cmap='RdYlBu',
                           alpha=0.8, edgecolor='none')

    ax1.set_xlabel('$S_k$ (R mode)')
    ax1.set_ylabel('$S_t$ (C mode)')
    ax1.set_zlabel('Mode')
    ax1.set_title('(A) Mode Selection Surface')
    ax1.view_init(elev=30, azim=45)

    # Panel B: R-C-L Trichotomy
    ax2 = fig.add_subplot(142)

    # Draw three overlapping circles (Venn-like)
    theta = np.linspace(0, 2*np.pi, 100)
    r = 0.3

    centers = [
        (0.35, 0.6),  # R - Sk
        (0.65, 0.6),  # C - St
        (0.5, 0.3),   # L - Se
    ]
    colors = ['red', 'green', 'blue']
    labels = ['R ($S_k$)', 'C ($S_t$)', 'L ($S_e$)']

    for center, color, label in zip(centers, colors, labels):
        circle = Circle(center, r, fill=True, facecolor=color,
                       edgecolor='black', linewidth=2, alpha=0.4)
        ax2.add_patch(circle)
        ax2.text(center[0], center[1], label, ha='center', va='center',
                fontsize=11, fontweight='bold')

    # Central overlap (psychon)
    ax2.text(0.5, 0.5, 'Psychon', ha='center', va='center',
            fontsize=10, style='italic')

    ax2.set_xlim(0, 1)
    ax2.set_ylim(0, 1)
    ax2.set_aspect('equal')
    ax2.axis('off')
    ax2.set_title('(B) Simultaneous R-C-L Operation')

    # Panel C: S-Entropy Minimization
    ax3 = fig.add_subplot(143)

    # Cost function visualization
    alpha, beta, gamma = 0.4, 0.3, 0.3
    contexts = ['High $S_k$', 'High $S_t$', 'High $S_e$', 'Balanced']

    # Sample S-coordinates for each context
    s_values = [
        [0.8, 0.1, 0.1],  # High Sk → R mode
        [0.1, 0.8, 0.1],  # High St → C mode
        [0.1, 0.1, 0.8],  # High Se → L mode
        [0.33, 0.33, 0.34],  # Balanced
    ]

    # Calculate costs for each mode
    x = np.arange(len(contexts))
    width = 0.25

    for i, (ctx, s) in enumerate(zip(contexts, s_values)):
        cost_R = alpha * s[0]
        cost_C = beta * s[1]
        cost_L = gamma * s[2]

        ax3.bar(x[i] - width, cost_R, width, color='red', alpha=0.7)
        ax3.bar(x[i], cost_C, width, color='green', alpha=0.7)
        ax3.bar(x[i] + width, cost_L, width, color='blue', alpha=0.7)

    ax3.set_xticks(x)
    ax3.set_xticklabels(contexts, fontsize=8)
    ax3.set_ylabel('Cost = $\\alpha S_k + \\beta S_t + \\gamma S_e$')
    ax3.set_title('(C) Mode Selection by Minimum Cost')

    # Add legend
    from matplotlib.patches import Patch
    legend_elements = [Patch(facecolor='red', alpha=0.7, label='R'),
                      Patch(facecolor='green', alpha=0.7, label='C'),
                      Patch(facecolor='blue', alpha=0.7, label='L')]
    ax3.legend(handles=legend_elements, loc='upper right')

    # Panel D: Impedance Response
    ax4 = fig.add_subplot(144)

    # Frequency response
    omega = np.logspace(-1, 3, 200)
    R = 1e6  # 1 MΩ
    C = 1e-12  # 1 pF
    L = 1e-3  # 1 mH

    Z_R = R * np.ones_like(omega)
    Z_C = 1 / (omega * C)
    Z_L = omega * L

    ax4.loglog(omega, Z_R, 'r-', linewidth=2, label='$|Z_R| = R$')
    ax4.loglog(omega, Z_C, 'g-', linewidth=2, label='$|Z_C| = 1/\\omega C$')
    ax4.loglog(omega, Z_L, 'b-', linewidth=2, label='$|Z_L| = \\omega L$')

    # Resonance point
    omega_0 = 1 / np.sqrt(L * C)
    ax4.axvline(x=omega_0, color='purple', linestyle='--', alpha=0.7)
    ax4.text(omega_0 * 1.2, 1e8, '$\\omega_0$', fontsize=10, color='purple')

    ax4.set_xlabel('Frequency $\\omega$ (rad/s)')
    ax4.set_ylabel('Impedance $|Z|$ ($\\Omega$)')
    ax4.set_title('(D) Impedance Frequency Response')
    ax4.legend(loc='upper right')
    ax4.grid(True, alpha=0.3, which='both')

    plt.tight_layout()
    plt.savefig('figures/fig3_circuit_equivalence.png')
    plt.savefig('figures/fig3_circuit_equivalence.pdf')
    plt.close()
    print("Generated: fig3_circuit_equivalence")


def figure4_consciousness_intersection():
    """
    Figure 4: Consciousness as Geometric Intersection
    Panel A: 3D intersection visualization
    Panel B: Decay curves P(t) and T(t)
    Panel C: Consciousness window
    Panel D: |C| = min(P, T)
    """
    fig = plt.figure(figsize=(16, 4))

    # Time parameters
    t = np.linspace(0, 10, 200)
    tau_P = 0.5  # Perception decay
    tau_T = 1.0  # Thought decay

    # Decay curves
    I_sensory = 0.8 * (np.sin(t) > 0).astype(float)  # Pulsed sensory input
    P_decay = np.zeros_like(t)
    T_decay = np.zeros_like(t)

    # Simulate decay dynamics
    dt = t[1] - t[0]
    for i in range(1, len(t)):
        dP = (-P_decay[i-1]/tau_P + I_sensory[i-1]) * dt
        dT = (-T_decay[i-1]/tau_T + 0.3 + 0.2*np.sin(0.5*t[i-1])) * dt
        P_decay[i] = max(0, P_decay[i-1] + dP)
        T_decay[i] = max(0, T_decay[i-1] + dT)

    # Normalize
    P_decay = P_decay / (np.max(P_decay) + 0.01)
    T_decay = T_decay / (np.max(T_decay) + 0.01)

    # Panel A: 3D Intersection
    ax1 = fig.add_subplot(141, projection='3d')

    # Create surfaces for P and T
    t_grid = np.linspace(0, 10, 50)
    x_grid = np.linspace(0, 1, 20)
    T_mesh, X_mesh = np.meshgrid(t_grid, x_grid)

    # P surface (decays from sensory)
    P_surface = np.exp(-T_mesh/2) * np.sin(T_mesh)**2
    P_surface = np.clip(P_surface, 0, 1)

    # T surface
    T_surface = 0.5 + 0.3 * np.sin(0.5 * T_mesh)

    # Plot surfaces
    ax1.plot_surface(T_mesh, X_mesh, P_surface, alpha=0.5, color='blue',
                    label='$P_{\\rm decay}$')
    ax1.plot_surface(T_mesh, X_mesh, T_surface, alpha=0.5, color='red',
                    label='$T_{\\rm decay}$')

    # Intersection line
    ax1.plot(t_grid, 0.5*np.ones_like(t_grid),
            np.minimum(P_surface[10, :], T_surface[10, :]),
            'g-', linewidth=3, label='$\\mathcal{C} = P \\cap T$')

    ax1.set_xlabel('Time')
    ax1.set_ylabel('$x$')
    ax1.set_zlabel('Intensity')
    ax1.set_title('(A) $\\mathcal{C} = P \\cap T$')
    ax1.view_init(elev=25, azim=45)

    # Panel B: Decay Curves
    ax2 = fig.add_subplot(142)

    ax2.plot(t, P_decay, 'b-', linewidth=2, label='$P_{\\rm decay}(t)$')
    ax2.plot(t, T_decay, 'r-', linewidth=2, label='$T_{\\rm decay}(t)$')

    # Fill intersection region
    intersection = np.minimum(P_decay, T_decay)
    ax2.fill_between(t, 0, intersection, alpha=0.3, color='green',
                    label='Intersection')

    ax2.set_xlabel('Time')
    ax2.set_ylabel('Decay Curve Value')
    ax2.set_title('(B) Perception and Thought Decay')
    ax2.legend(loc='upper right')
    ax2.set_ylim(0, 1.1)
    ax2.grid(True, alpha=0.3)

    # Panel C: Consciousness Window
    ax3 = fig.add_subplot(143)

    theta = 0.3  # Threshold

    # Find consciousness windows
    conscious = (P_decay > theta) & (T_decay > theta)

    ax3.fill_between(t, 0, conscious.astype(float), alpha=0.5, color='gold',
                    label='Conscious ($W_C$)')
    ax3.axhline(y=1, color='gray', linestyle=':', alpha=0.5)

    # Mark threshold
    ax3.axhline(y=theta, color='black', linestyle='--', linewidth=1)
    ax3.text(0.5, theta + 0.05, '$\\theta$', fontsize=10)

    # Show P and T relative to threshold
    ax3.plot(t, P_decay, 'b-', linewidth=1.5, alpha=0.7)
    ax3.plot(t, T_decay, 'r-', linewidth=1.5, alpha=0.7)

    ax3.set_xlabel('Time')
    ax3.set_ylabel('State')
    ax3.set_title('(C) Consciousness Window $W_C$')
    ax3.set_ylim(0, 1.2)

    # Panel D: Magnitude
    ax4 = fig.add_subplot(144)

    C_magnitude = np.minimum(P_decay, T_decay)

    ax4.plot(t, P_decay, 'b--', linewidth=1.5, alpha=0.5, label='$P$')
    ax4.plot(t, T_decay, 'r--', linewidth=1.5, alpha=0.5, label='$T$')
    ax4.plot(t, C_magnitude, 'g-', linewidth=3, label='$|\\mathcal{C}| = \\min(P, T)$')

    ax4.fill_between(t, 0, C_magnitude, alpha=0.3, color='green')

    ax4.set_xlabel('Time')
    ax4.set_ylabel('Magnitude')
    ax4.set_title('(D) $|\\mathcal{C}| = \\min(P_{\\rm decay}, T_{\\rm decay})$')
    ax4.legend(loc='upper right')
    ax4.set_ylim(0, 1.1)
    ax4.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('figures/fig4_consciousness_intersection.png')
    plt.savefig('figures/fig4_consciousness_intersection.pdf')
    plt.close()
    print("Generated: fig4_consciousness_intersection")


def figure5_emergent_phenomena():
    """
    Figure 5: Emergent Mental Phenomena
    Panel A: 3D memory as emotional integral
    Panel B: Dream dynamics (P = 0)
    Panel C: Drug trajectory modification
    Panel D: Mental state equivalence classes
    """
    fig = plt.figure(figsize=(16, 4))

    t = np.linspace(0, 10, 200)

    # Panel A: 3D Memory Accumulation
    ax1 = fig.add_subplot(141, projection='3d')

    # Emotional field H(t)
    H = 0.5 + 0.3*np.sin(2*t) + 0.2*np.cos(3*t)

    # dH/dt
    dH_dt = np.gradient(H, t)

    # Memory = integral of positive dH/dt
    dH_positive = np.maximum(dH_dt, 0)
    Memory = np.cumsum(dH_positive) * (t[1] - t[0])

    # 3D visualization
    ax1.plot(t, H, Memory, 'b-', linewidth=2)
    ax1.plot(t, H, np.zeros_like(t), 'r--', linewidth=1, alpha=0.5)

    # Mark high emotional change regions
    peaks = np.where(dH_positive > 0.1)[0]
    if len(peaks) > 0:
        ax1.scatter(t[peaks[::10]], H[peaks[::10]], Memory[peaks[::10]],
                   c='red', s=50, marker='o')

    ax1.set_xlabel('Time $t$')
    ax1.set_ylabel('$H(t)$')
    ax1.set_zlabel('Memory $M$')
    ax1.set_title('(A) $M = \\int \\dot{H}^+ dt$')
    ax1.view_init(elev=20, azim=45)

    # Panel B: Dream Dynamics
    ax2 = fig.add_subplot(142)

    # Normal waking
    P_wake = 0.5 + 0.3*np.sin(t)
    T_wake = 0.6 + 0.2*np.cos(1.5*t)

    # Dream (P = 0)
    P_dream = np.zeros_like(t)
    T_dream = 0.6 + 0.4*np.sin(0.8*t) + 0.2*np.random.randn(len(t))
    T_dream = np.clip(T_dream, 0, 1)

    ax2.plot(t, P_wake, 'b-', linewidth=2, alpha=0.5, label='$P$ (wake)')
    ax2.plot(t, T_wake, 'r-', linewidth=2, alpha=0.5, label='$T$ (wake)')
    ax2.plot(t, P_dream, 'b--', linewidth=2, label='$P$ (dream) = 0')
    ax2.plot(t, T_dream, 'r--', linewidth=2, label='$T$ (dream)')

    # Mark dream region
    ax2.fill_between(t[50:150], 0, 1, alpha=0.1, color='purple')
    ax2.text(5, 0.9, 'Dream State', ha='center', fontsize=10,
            bbox=dict(boxstyle='round', facecolor='lavender'))

    ax2.set_xlabel('Time')
    ax2.set_ylabel('Decay Curve')
    ax2.set_title('(B) Dreams: $P = 0$, $T > 0$')
    ax2.legend(loc='upper right', fontsize=8)
    ax2.set_ylim(-0.1, 1.1)

    # Panel C: Drug Trajectory Modification
    ax3 = fig.add_subplot(143)

    # Trajectories before/after drug
    t_traj = np.linspace(0, 1, 50)

    # Anxious trajectory (high variance, spiky)
    traj_anxious = 0.5 + 0.3*np.sin(10*t_traj) + 0.1*np.random.randn(len(t_traj))

    # Calm trajectory (smooth)
    traj_calm = 0.5 + 0.1*np.sin(2*t_traj)

    ax3.plot(t_traj, traj_anxious, 'r-', linewidth=2, label='$\\gamma_{\\rm anxious}$')
    ax3.plot(t_traj, traj_calm, 'g-', linewidth=2, label='$\\gamma_{\\rm calm}$')

    # Same terminus
    ax3.scatter([1, 1], [traj_anxious[-1], traj_calm[-1]], s=100, c='black',
               marker='*', zorder=5)

    # Arrow showing drug effect
    ax3.annotate('Drug', xy=(0.5, 0.7), xytext=(0.5, 0.9),
                fontsize=10, ha='center',
                arrowprops=dict(arrowstyle='->', color='blue', lw=2))

    ax3.set_xlabel('Trajectory Progress')
    ax3.set_ylabel('State')
    ax3.set_title('(C) $\\mathcal{P}_{\\rm drug}: \\gamma \\to \\gamma\'$')
    ax3.legend(loc='lower right')
    ax3.set_ylim(0, 1.2)

    # Panel D: Equivalence Classes
    ax4 = fig.add_subplot(144)

    # Draw clusters representing equivalence classes
    np.random.seed(123)

    # Generate clustered data
    n_clusters = 4
    n_points_per_cluster = 20
    cluster_centers = [(0.2, 0.8), (0.8, 0.8), (0.2, 0.3), (0.7, 0.3)]
    cluster_colors = ['#e74c3c', '#3498db', '#2ecc71', '#9b59b6']

    for center, color in zip(cluster_centers, cluster_colors):
        x = center[0] + 0.08 * np.random.randn(n_points_per_cluster)
        y = center[1] + 0.08 * np.random.randn(n_points_per_cluster)
        ax4.scatter(x, y, c=color, s=40, alpha=0.7)

        # Draw enclosing ellipse
        circle = Circle(center, 0.12, fill=False, edgecolor=color,
                       linewidth=2, linestyle='--')
        ax4.add_patch(circle)

    ax4.set_xlim(0, 1)
    ax4.set_ylim(0, 1)
    ax4.set_xlabel('$S_k$')
    ax4.set_ylabel('$S_t$')
    ax4.set_title('(D) Equivalence Classes $[\\mathcal{M}]$')
    ax4.set_aspect('equal')

    plt.tight_layout()
    plt.savefig('figures/fig5_emergent_phenomena.png')
    plt.savefig('figures/fig5_emergent_phenomena.pdf')
    plt.close()
    print("Generated: fig5_emergent_phenomena")


if __name__ == "__main__":
    print("Generating figures for Psychon Circuit Mechanics paper...")
    print("=" * 50)

    figure1_sentropy_coordinates()
    figure2_trajectory_terminus()
    figure3_circuit_equivalence()
    figure4_consciousness_intersection()
    figure5_emergent_phenomena()

    print("=" * 50)
    print("All figures generated in 'figures/' directory")
