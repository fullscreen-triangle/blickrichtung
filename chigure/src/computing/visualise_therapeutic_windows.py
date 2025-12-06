import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import matplotlib.patches as mpatches
from matplotlib.patches import Rectangle
import seaborn as sns

# Set publication-quality style
plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300
plt.rcParams['font.family'] = 'Arial'
plt.rcParams['font.size'] = 10
plt.rcParams['axes.linewidth'] = 1.5


def safe_get(drug, key, default=0.0):
    """Safely get value from drug dict with default fallback"""
    return drug.get(key, default)


def main():
    # Load data
    with open('therapeutic_window_results_20251106_211754.json', 'r') as f:
        data = json.load(f)

    results = data['results']
    drug_names = [r['drug_name'].replace('_', ' ').title() for r in results]

    # Dynamic color assignment using seaborn palette
    n_drugs = len(results)
    color_palette = sns.color_palette("husl", n_drugs)
    colors = {name: color_palette[i] for i, name in enumerate(drug_names)}

    print(f"Loaded {n_drugs} drugs: {', '.join(drug_names)}")
    
    # Debug: Print available keys
    if results:
        print(f"Available keys in results: {list(results[0].keys())}")

    # Create figure with 4 panels (2x2 grid)
    fig = plt.figure(figsize=(16, 12))
    gs = GridSpec(2, 2, figure=fig, hspace=0.35, wspace=0.3,
                  left=0.08, right=0.95, top=0.92, bottom=0.07)

    # ============================================================================
    # PANEL A: Therapeutic Window Ranges
    # ============================================================================
    ax1 = fig.add_subplot(gs[0, :])  # Spans both columns

    y_pos = np.arange(len(drug_names))
    height = 0.6

    for idx, (drug, name) in enumerate(zip(results, drug_names)):
        min_dose = safe_get(drug, 'min_effective_dose_mg', 0.1)
        max_dose = safe_get(drug, 'max_safe_dose_mg', 10.0)
        optimal = safe_get(drug, 'optimal_dose_mg', 1.0)
        color = colors[name]
        
        # Draw therapeutic window bar
        window_width = max_dose - min_dose
        rect = Rectangle((min_dose, idx - height/2), window_width, height,
                         facecolor=color, alpha=0.3, edgecolor=color, 
                         linewidth=2.5, label=f'{name} Window')
        ax1.add_patch(rect)
        
        # Mark minimum effective dose
        ax1.plot(min_dose, idx, 'o', markersize=10, color=color, 
                 markeredgecolor='black', markeredgewidth=2, zorder=5)
        ax1.text(min_dose, idx + height/2 + 0.15, f'Min: {min_dose:.3f} mg', 
                 ha='center', va='bottom', fontsize=8, fontweight='bold', color=color)
        
        # Mark maximum safe dose
        ax1.plot(max_dose, idx, 's', markersize=10, color=color,
                 markeredgecolor='black', markeredgewidth=2, zorder=5)
        ax1.text(max_dose, idx + height/2 + 0.15, f'Max: {max_dose:.2f} mg', 
                 ha='center', va='bottom', fontsize=8, fontweight='bold', color=color)
        
        # Mark optimal dose
        ax1.plot(optimal, idx, 'D', markersize=12, color='gold',
                 markeredgecolor='black', markeredgewidth=2.5, zorder=6)
        ax1.text(optimal, idx - height/2 - 0.15, f'Optimal: {optimal:.3f} mg', 
                 ha='center', va='top', fontsize=8, fontweight='bold', 
                 color='darkgoldenrod')
        
        # Add therapeutic index annotation
        ti = safe_get(drug, 'therapeutic_index', 10.0)
        ax1.text(max_dose * 1.05, idx, f'TI = {ti:.1f}', 
                 ha='left', va='center', fontsize=9, fontweight='bold',
                 bbox=dict(boxstyle='round,pad=0.3', facecolor='white', 
                          edgecolor=color, linewidth=1.5))

    ax1.set_xlabel('Dose (mg)', fontsize=13, fontweight='bold')
    ax1.set_ylabel('Drug', fontsize=13, fontweight='bold')
    ax1.set_title('(A) Therapeutic Window Ranges and Optimal Dosing', 
                  fontsize=14, fontweight='bold', pad=20)
    ax1.set_yticks(y_pos)
    ax1.set_yticklabels(drug_names, fontsize=11, fontweight='bold')
    ax1.set_xscale('log')
    ax1.grid(axis='x', alpha=0.3, linestyle='--', linewidth=0.8)
    ax1.spines['top'].set_visible(False)
    ax1.spines['right'].set_visible(False)

    # Add legend
    legend_elements = [
        plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='gray', 
                   markersize=10, markeredgecolor='black', markeredgewidth=2,
                   label='Minimum Effective Dose'),
        plt.Line2D([0], [0], marker='s', color='w', markerfacecolor='gray',
                   markersize=10, markeredgecolor='black', markeredgewidth=2,
                   label='Maximum Safe Dose'),
        plt.Line2D([0], [0], marker='D', color='w', markerfacecolor='gold',
                   markersize=12, markeredgecolor='black', markeredgewidth=2.5,
                   label='Optimal Dose'),
    ]
    ax1.legend(handles=legend_elements, loc='upper left', frameon=True,
               framealpha=0.95, edgecolor='black', fontsize=10)

    # ============================================================================
    # PANEL B: Therapeutic Index Comparison
    # ============================================================================
    ax2 = fig.add_subplot(gs[1, 0])

    therapeutic_indices = [safe_get(r, 'therapeutic_index', 10.0) for r in results]
    ti_log = np.log10(therapeutic_indices)

    bars = ax2.barh(range(len(drug_names)), ti_log,
                    color=[colors[name] for name in drug_names],
                    alpha=0.85, edgecolor='black', linewidth=1.5)

    # Add value labels
    for i, (ti, ti_l) in enumerate(zip(therapeutic_indices, ti_log)):
        ax2.text(ti_l + 0.05, i, f'{ti:.1f}\n({ti_l:.2f} log₁₀)', 
                 ha='left', va='center', fontsize=9, fontweight='bold',
                 color=colors[drug_names[i]])

    ax2.set_xlabel('Therapeutic Index (log₁₀)', fontsize=12, fontweight='bold')
    ax2.set_ylabel('Drug', fontsize=12, fontweight='bold')
    ax2.set_title('(B) Therapeutic Index: Safety Margin', 
                  fontsize=13, fontweight='bold', pad=15)
    ax2.set_yticks(range(len(drug_names)))
    ax2.set_yticklabels(drug_names, fontsize=10, fontweight='bold')
    ax2.grid(axis='x', alpha=0.3, linestyle='--', linewidth=0.8)
    ax2.spines['top'].set_visible(False)
    ax2.spines['right'].set_visible(False)

    # Add safety zones
    ax2.axvline(x=1, color='red', linestyle='--', linewidth=2, alpha=0.5, label='TI = 10 (Narrow)')
    ax2.axvline(x=2, color='orange', linestyle='--', linewidth=2, alpha=0.5, label='TI = 100 (Moderate)')
    ax2.axvline(x=3, color='green', linestyle='--', linewidth=2, alpha=0.5, label='TI = 1000 (Wide)')
    ax2.legend(loc='lower right', fontsize=8, frameon=True, framealpha=0.95)

    # Add interpretation text
    ax2.text(0.98, 0.97, 'Higher TI = Safer Drug\n(Wider Therapeutic Window)', 
             transform=ax2.transAxes, fontsize=9, ha='right', va='top',
             bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8,
                      edgecolor='black', linewidth=1.5))

    # ============================================================================
    # PANEL C: Dose-Response Curves (Simulated)
    # ============================================================================
    ax3 = fig.add_subplot(gs[1, 1])

    # Simulate dose-response curves
    dose_range = np.logspace(-3, 2, 1000)  # 0.001 to 100 mg

    for drug, name in zip(results, drug_names):
        min_dose = safe_get(drug, 'min_effective_dose_mg', 0.1)
        max_dose = safe_get(drug, 'max_safe_dose_mg', 10.0)
        optimal = safe_get(drug, 'optimal_dose_mg', 1.0)
        color = colors[name]
        
        # Sigmoid response curve
        # Response = 1 / (1 + exp(-(dose - optimal)/scale))
        scale = (max_dose - min_dose) / 6
        if scale == 0:
            scale = 1.0  # Prevent division by zero
        response = 1 / (1 + np.exp(-(dose_range - optimal) / scale))
        
        # Plot curve
        ax3.plot(dose_range, response, linewidth=2.5, color=color, 
                 label=name, alpha=0.85)
        
        # Mark therapeutic window
        window_mask = (dose_range >= min_dose) & (dose_range <= max_dose)
        ax3.fill_between(dose_range[window_mask], 0, response[window_mask],
                         color=color, alpha=0.2)
        
        # Mark optimal dose
        optimal_response = 1 / (1 + np.exp(-(optimal - optimal) / scale))
        ax3.plot(optimal, optimal_response, 'D', markersize=10, color='gold',
                 markeredgecolor='black', markeredgewidth=2, zorder=5)

    ax3.set_xlabel('Dose (mg)', fontsize=12, fontweight='bold')
    ax3.set_ylabel('Therapeutic Response (normalized)', fontsize=12, fontweight='bold')
    ax3.set_title('(C) Dose-Response Curves', 
                  fontsize=13, fontweight='bold', pad=15)
    ax3.set_xscale('log')
    ax3.set_xlim(1e-3, 1e2)
    ax3.set_ylim(0, 1.05)
    ax3.legend(loc='upper left', frameon=True, framealpha=0.95, 
               edgecolor='black', fontsize=9, ncol=2)
    ax3.grid(alpha=0.3, linestyle='--', linewidth=0.8)
    ax3.spines['top'].set_visible(False)
    ax3.spines['right'].set_visible(False)

    # Add response zones
    ax3.axhline(y=0.2, color='red', linestyle=':', linewidth=1.5, alpha=0.5)
    ax3.text(1e-3, 0.22, 'Sub-therapeutic', fontsize=8, color='red', style='italic')
    ax3.axhline(y=0.8, color='orange', linestyle=':', linewidth=1.5, alpha=0.5)
    ax3.text(1e-3, 0.82, 'Toxic', fontsize=8, color='orange', style='italic')
    ax3.fill_between([1e-3, 1e2], 0.2, 0.8, color='green', alpha=0.1, zorder=0)
    ax3.text(1e-3, 0.5, 'Therapeutic\nZone', fontsize=9, color='darkgreen', 
             fontweight='bold', va='center')

    # Main title
    fig.suptitle('Therapeutic Window Analysis',
                 fontsize=16, fontweight='bold', y=0.96)

    # Subtitle
    subtitle = (f'Timestamp: {data["timestamp"]} | '
                f'Safety margin quantification for {len(results)} pharmaceutical agents')
    fig.text(0.5, 0.935, subtitle, ha='center', fontsize=9, style='italic')

    plt.savefig('therapeutic_windows_4panel.png', dpi=300, bbox_inches='tight')
    plt.savefig('therapeutic_windows_4panel.pdf', bbox_inches='tight')
    print("✓ Therapeutic window visualization saved")
    print(f"  - Analyzed {len(results)} drugs")
    print(f"  - Therapeutic indices range: {min(therapeutic_indices):.1f} - {max(therapeutic_indices):.1f}")
    print(f"  - Output: therapeutic_windows_4panel.png/pdf")

    plt.close()


if __name__ == "__main__":
    main()
