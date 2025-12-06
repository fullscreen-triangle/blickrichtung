import numpy as np
import matplotlib
matplotlib.use('Agg')
from matplotlib.patches import Rectangle, FancyBboxPatch, Polygon, FancyArrowPatch
import matplotlib.pyplot as plt
from matplotlib.collections import PatchCollection
import matplotlib.patches as mpatches
from matplotlib.gridspec import GridSpec
import seaborn as sns

# Set publication-quality style
plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300
plt.rcParams['font.family'] = 'Arial'
plt.rcParams['font.size'] = 10
plt.rcParams['axes.linewidth'] = 1.5
plt.rcParams['xtick.major.width'] = 1.5
plt.rcParams['ytick.major.width'] = 1.5


def main():
    # Data structure
    data = {
        'BASELINE': {
            'levels': ['Glucose\nTransport', 'Glycolysis', 'TCA\nCycle', 'Oxidative\nPhosphorylation', 'Gene\nExpression'],
            'flux': [100.0, 80.0, 60.8, 43.8, 29.8],
            'info': [8.00, 5.12, 2.96, 1.53, 0.71],
            'atp': [100.0, 160.0, 0.0, -1313.3, 148.8],
            'end_to_end': 0.298,
            'total_info_compression': 7.29,
            'total_atp': 1722.1,
            'atp_efficiency': 4.234,
            'color': '#3498db'  # Blue
        },
        'METFORMIN': {
            'levels': ['Glucose\nTransport', 'Glycolysis', 'TCA\nCycle', 'Oxidative\nPhosphorylation', 'Gene\nExpression'],
            'flux': [100.0, 96.0, 87.6, 75.6, 61.7],
            'info': [8.00, 7.37, 6.13, 4.58, 3.05],
            'atp': [100.0, 192.0, 0.0, -2269.3, 308.6],
            'end_to_end': 0.617,
            'total_info_compression': 4.95,
            'total_atp': 2870.0,
            'atp_efficiency': 1.725,
            'color': '#2ecc71'  # Green
        },
        'INSULIN_RESISTANCE': {
            'levels': ['Glucose\nTransport', 'Glycolysis', 'TCA\nCycle', 'Oxidative\nPhosphorylation', 'Gene\nExpression'],
            'flux': [100.0, 48.0, 21.9, 9.5, 3.9],
            'info': [8.00, 1.84, 0.38, 0.07, 0.01],
            'atp': [100.0, 96.0, 0.0, -283.7, 19.3],
            'end_to_end': 0.039,
            'total_info_compression': 7.99,
            'total_atp': 499.0,
            'atp_efficiency': 16.010,
            'color': '#e74c3c'  # Red
        },
        'LITHIUM': {
            'levels': ['Glucose\nTransport', 'Glycolysis', 'TCA\nCycle', 'Oxidative\nPhosphorylation', 'Gene\nExpression'],
            'flux': [100.0, 80.0, 60.8, 43.8, 29.8],
            'info': [8.00, 5.12, 2.96, 1.53, 0.71],
            'atp': [100.0, 160.0, 0.0, -1313.3, 148.8],
            'end_to_end': 0.298,
            'total_info_compression': 7.29,
            'total_atp': 1722.1,
            'atp_efficiency': 4.234,
            'color': '#9b59b6'  # Purple
        }
    }

    # Create figure with 6 panels (3x2 grid)
    fig = plt.figure(figsize=(18, 16))
    gs = GridSpec(3, 2, figure=fig, hspace=0.35, wspace=0.25,
                  left=0.07, right=0.96, top=0.94, bottom=0.05)

    conditions = ['BASELINE', 'METFORMIN', 'INSULIN_RESISTANCE', 'LITHIUM']
    condition_labels = ['Baseline', 'Metformin', 'Insulin Resistance', 'Lithium']

    # ============================================================================
    # PANEL A: Sankey-style Flux Flow Diagram
    # ============================================================================
    ax1 = fig.add_subplot(gs[0, :])  # Spans both columns

    # Create Sankey-style visualization
    y_levels = np.array([0, 1, 2, 3, 4])
    level_names = ['L1: Glucose\nTransport', 'L2: Glycolysis', 'L3: TCA Cycle', 
                   'L4: OxPhos', 'L5: Gene Expression']

    for idx, condition in enumerate(conditions):
        flux = np.array(data[condition]['flux'])
        color = data[condition]['color']
        
        # Offset for each condition
        x_offset = idx * 1.5
        
        # Draw flux bars at each level
        for i, (y, f, name) in enumerate(zip(y_levels, flux, level_names)):
            bar_height = f / 100 * 0.8  # Scale to fit
            rect = FancyBboxPatch((x_offset, y - bar_height/2), 0.4, bar_height,
                                  boxstyle="round,pad=0.02", 
                                  facecolor=color, edgecolor='black', 
                                  linewidth=2, alpha=0.7)
            ax1.add_patch(rect)
            
            # Add flux value
            ax1.text(x_offset + 0.2, y, f'{f:.1f}', ha='center', va='center',
                     fontsize=8, fontweight='bold', color='white')
            
            # Draw connecting flows
            if i < len(flux) - 1:
                # Calculate next level bar height
                next_bar_height = flux[i+1] / 100 * 0.8
                
                # Create trapezoid for flow
                verts = [
                    (x_offset + 0.4, y + bar_height/2),
                    (x_offset + 0.4, y - bar_height/2),
                    (x_offset + 0.4, y_levels[i+1] - next_bar_height/2),
                    (x_offset + 0.4, y_levels[i+1] + next_bar_height/2)
                ]
                
                # Draw flow lines
                for v1, v2 in [(verts[0], verts[3]), (verts[1], verts[2])]:
                    ax1.plot([v1[0], v2[0]], [v1[1], v2[1]], 
                             color=color, alpha=0.3, linewidth=2)
        
        # Add condition label
        ax1.text(x_offset + 0.2, -0.8, condition_labels[idx], 
                 ha='center', fontsize=11, fontweight='bold', color=color)

    # Add level labels on the left
    for i, name in enumerate(level_names):
        ax1.text(-0.5, y_levels[i], name, ha='right', va='center',
                 fontsize=9, fontweight='bold')

    ax1.set_xlim(-1, 6.5)
    ax1.set_ylim(-1.2, 5)
    ax1.axis('off')
    ax1.set_title('(A) Hierarchical Flux Propagation: Sankey Flow Diagram', 
                  fontsize=14, fontweight='bold', pad=20)

    # ============================================================================
    # PANEL B: Flux Cascade
    # ============================================================================
    ax2 = fig.add_subplot(gs[1, 0])

    x_pos = np.arange(5)
    width = 0.18
    offset = np.array([-1.5, -0.5, 0.5, 1.5]) * width

    for idx, condition in enumerate(conditions):
        flux = data[condition]['flux']
        color = data[condition]['color']
        ax2.bar(x_pos + offset[idx], flux, width, 
                label=condition_labels[idx], color=color, 
                alpha=0.85, edgecolor='black', linewidth=1.2)

    ax2.set_xlabel('Metabolic Level', fontsize=11, fontweight='bold')
    ax2.set_ylabel('Metabolic Flux (% of L1)', fontsize=11, fontweight='bold')
    ax2.set_title('(B) Hierarchical Flux Cascade', fontsize=12, fontweight='bold', pad=12)
    ax2.set_xticks(x_pos)
    ax2.set_xticklabels(['L1', 'L2', 'L3', 'L4', 'L5'], fontsize=9)
    ax2.set_ylim(0, 110)
    ax2.legend(loc='upper right', frameon=True, framealpha=0.95, fontsize=8)
    ax2.grid(axis='y', alpha=0.3, linestyle='--', linewidth=0.8)
    ax2.spines['top'].set_visible(False)
    ax2.spines['right'].set_visible(False)

    # ============================================================================
    # PANEL C: Information Compression
    # ============================================================================
    ax3 = fig.add_subplot(gs[1, 1])

    for idx, condition in enumerate(conditions):
        info = data[condition]['info']
        color = data[condition]['color']
        ax3.plot(x_pos, info, marker='o', markersize=8, linewidth=2.5,
                 label=condition_labels[idx], color=color, alpha=0.85)
        
        for i in range(len(info)):
            ax3.scatter(x_pos[i], info[i], s=100, color=color, 
                       edgecolor='black', linewidth=1.5, zorder=5, alpha=0.9)

    ax3.set_xlabel('Metabolic Level', fontsize=11, fontweight='bold')
    ax3.set_ylabel('Information Content (bits)', fontsize=11, fontweight='bold')
    ax3.set_title('(C) Information Compression', fontsize=12, fontweight='bold', pad=12)
    ax3.set_xticks(x_pos)
    ax3.set_xticklabels(['L1', 'L2', 'L3', 'L4', 'L5'], fontsize=9)
    ax3.set_ylim(-0.5, 9)
    ax3.legend(loc='upper right', frameon=True, framealpha=0.95, fontsize=8)
    ax3.grid(alpha=0.3, linestyle='--', linewidth=0.8)
    ax3.spines['top'].set_visible(False)
    ax3.spines['right'].set_visible(False)

    # ============================================================================
    # PANEL D: ATP Profile
    # ============================================================================
    ax4 = fig.add_subplot(gs[2, 0])

    for idx, condition in enumerate(conditions):
        atp = data[condition]['atp']
        color = data[condition]['color']
        
        atp_pos = [max(0, a) for a in atp]
        atp_neg = [min(0, a) for a in atp]
        
        ax4.bar(x_pos + offset[idx], atp_pos, width, 
                color=color, alpha=0.85, edgecolor='black', linewidth=1.2)
        ax4.bar(x_pos + offset[idx], atp_neg, width, 
                color=color, alpha=0.85, edgecolor='black', linewidth=1.2, hatch='///')

    ax4.axhline(y=0, color='black', linestyle='-', linewidth=2)
    ax4.set_xlabel('Metabolic Level', fontsize=11, fontweight='bold')
    ax4.set_ylabel('ATP Production/Consumption', fontsize=11, fontweight='bold')
    ax4.set_title('(D) ATP Production/Consumption Profile', fontsize=12, fontweight='bold', pad=12)
    ax4.set_xticks(x_pos)
    ax4.set_xticklabels(['L1', 'L2', 'L3', 'L4', 'L5'], fontsize=9)
    ax4.set_ylim(-2500, 400)
    ax4.grid(axis='y', alpha=0.3, linestyle='--', linewidth=0.8)
    ax4.spines['top'].set_visible(False)
    ax4.spines['right'].set_visible(False)

    legend_elements = [mpatches.Patch(facecolor=data[c]['color'], 
                                     edgecolor='black', linewidth=1.2,
                                     label=condition_labels[i], alpha=0.85)
                      for i, c in enumerate(conditions)]
    ax4.legend(handles=legend_elements, loc='lower left', frameon=True, fontsize=8)

    # ============================================================================
    # PANEL E: Efficiency Metrics
    # ============================================================================
    ax5 = fig.add_subplot(gs[2, 1])

    metrics = ['End-to-End\nFlux', 'Info Compression\n(bits)', 
               'ATP Efficiency\n(bits/kATP)', 'Net ATP\n(×100)']
    metric_keys = ['end_to_end', 'total_info_compression', 'atp_efficiency', 'total_atp']
    metric_scales = [1, 1, 1, 0.01]

    x_metric = np.arange(len(metrics))

    for idx, condition in enumerate(conditions):
        values = [data[condition][key] * scale 
                  for key, scale in zip(metric_keys, metric_scales)]
        color = data[condition]['color']
        
        ax5.bar(x_metric + offset[idx], values, width, 
                label=condition_labels[idx], color=color, 
                alpha=0.85, edgecolor='black', linewidth=1.2)

    ax5.set_xlabel('Efficiency Metrics', fontsize=11, fontweight='bold')
    ax5.set_ylabel('Normalized Value', fontsize=11, fontweight='bold')
    ax5.set_title('(E) Metabolic Efficiency Comparison', fontsize=12, fontweight='bold', pad=12)
    ax5.set_xticks(x_metric)
    ax5.set_xticklabels(metrics, fontsize=8)
    ax5.set_ylim(0, 20)
    ax5.legend(loc='upper left', frameon=True, framealpha=0.95, fontsize=8)
    ax5.grid(axis='y', alpha=0.3, linestyle='--', linewidth=0.8)
    ax5.spines['top'].set_visible(False)
    ax5.spines['right'].set_visible(False)

    # Main title
    fig.suptitle('Metabolic Flux Hierarchy: Multi-Scale Information Cascades Through Drug-Modulated Pathways',
                 fontsize=17, fontweight='bold', y=0.97)

    plt.savefig('metabolic_flux_hierarchy_extended.png', dpi=300, bbox_inches='tight')
    plt.savefig('metabolic_flux_hierarchy_extended.pdf', bbox_inches='tight')
    print("✓ Extended figure saved: metabolic_flux_hierarchy_extended.png")
    print("✓ Extended figure saved: metabolic_flux_hierarchy_extended.pdf")

    plt.close()


if __name__ == "__main__":
    main()
