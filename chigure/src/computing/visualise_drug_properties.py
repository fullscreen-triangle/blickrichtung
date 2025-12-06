import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import seaborn as sns
from matplotlib.patches import Circle, Rectangle
import matplotlib.patches as mpatches

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
    with open('drug_properties_20251106_211724.json', 'r') as f:
        data = json.load(f)

    drugs = data['drugs']
    drug_names = [d['name'].replace('_', ' ').title() for d in drugs]

    # Dynamic color assignment using seaborn palette
    n_drugs = len(drugs)
    color_palette = sns.color_palette("husl", n_drugs)
    colors = {name: color_palette[i] for i, name in enumerate(drug_names)}

    print(f"Loaded {n_drugs} drugs: {', '.join(drug_names)}")
    
    # Debug: Print available keys
    if drugs:
        print(f"Available keys in drug data: {list(drugs[0].keys())}")

    # Create figure with 6 panels (3x2 grid)
    fig = plt.figure(figsize=(18, 14))
    gs = GridSpec(3, 2, figure=fig, hspace=0.35, wspace=0.3,
                  left=0.08, right=0.95, top=0.93, bottom=0.06)

    # ============================================================================
    # PANEL A: Molecular Structure Characteristics
    # ============================================================================
    ax1 = fig.add_subplot(gs[0, 0])

    properties = ['molecular_weight', 'num_atoms', 'num_electrons', 'num_aromatic_rings']
    property_labels = ['Molecular\nWeight (g/mol)', 'Number of\nAtoms', 
                       'Number of\nElectrons', 'Aromatic\nRings']

    x_pos = np.arange(len(properties))
    width = 0.8 / n_drugs
    offset = np.linspace(-width*(n_drugs-1)/2, width*(n_drugs-1)/2, n_drugs)

    for idx, (drug, name) in enumerate(zip(drugs, drug_names)):
        values = [safe_get(drug, prop) for prop in properties]
        color = colors[name]
        
        ax1.bar(x_pos + offset[idx], values, width, 
                label=name, color=color, alpha=0.85, 
                edgecolor='black', linewidth=1.2)
        
        # Add value labels
        max_val = max([max([safe_get(d, p) for p in properties]) for d in drugs])
        for i, v in enumerate(values):
            if v > 0:
                ax1.text(x_pos[i] + offset[idx], v + max_val*0.02, 
                         f'{v:.0f}' if v >= 1 else f'{v:.1f}', 
                         ha='center', va='bottom', fontsize=7, 
                         fontweight='bold', color=color, rotation=90)

    ax1.set_xlabel('Structural Property', fontsize=12, fontweight='bold')
    ax1.set_ylabel('Property Value', fontsize=12, fontweight='bold')
    ax1.set_title('(A) Molecular Structure Characteristics', 
                  fontsize=13, fontweight='bold', pad=15)
    ax1.set_xticks(x_pos)
    ax1.set_xticklabels(property_labels, fontsize=9)
    ax1.legend(loc='upper left', frameon=True, framealpha=0.95, 
               edgecolor='black', fontsize=8, ncol=2)
    ax1.grid(axis='y', alpha=0.3, linestyle='--', linewidth=0.8)
    ax1.spines['top'].set_visible(False)
    ax1.spines['right'].set_visible(False)

    # ============================================================================
    # PANEL B: Chemical Properties (LogP, pKa, PSA)
    # ============================================================================
    ax2 = fig.add_subplot(gs[0, 1])

    chem_props = ['log_p', 'polar_surface_area', 'num_h_bond_donors', 'num_h_bond_acceptors']
    chem_labels = ['LogP\n(Lipophilicity)', 'Polar Surface\nArea (Ų)', 
                   'H-Bond\nDonors', 'H-Bond\nAcceptors']

    x_chem = np.arange(len(chem_props))

    for idx, (drug, name) in enumerate(zip(drugs, drug_names)):
        values = [safe_get(drug, prop) for prop in chem_props]
        color = colors[name]
        
        ax2.bar(x_chem + offset[idx], values, width, 
                label=name, color=color, alpha=0.85, 
                edgecolor='black', linewidth=1.2)
        
        # Add value labels
        max_val = max([max([safe_get(d, p) for p in chem_props]) for d in drugs])
        for i, v in enumerate(values):
            if v != 0:
                ax2.text(x_chem[i] + offset[idx], v + max_val*0.03, 
                         f'{v:.1f}', ha='center', va='bottom', 
                         fontsize=7, fontweight='bold', color=color, rotation=90)

    ax2.set_xlabel('Chemical Property', fontsize=12, fontweight='bold')
    ax2.set_ylabel('Property Value', fontsize=12, fontweight='bold')
    ax2.set_title('(B) Chemical Properties and Drug-Likeness', 
                  fontsize=13, fontweight='bold', pad=15)
    ax2.set_xticks(x_chem)
    ax2.set_xticklabels(chem_labels, fontsize=9)
    ax2.legend(loc='upper left', frameon=True, framealpha=0.95, 
               edgecolor='black', fontsize=8, ncol=2)
    ax2.grid(axis='y', alpha=0.3, linestyle='--', linewidth=0.8)
    ax2.spines['top'].set_visible(False)
    ax2.spines['right'].set_visible(False)

    # ============================================================================
    # PANEL C: Vibrational Frequencies (Log Scale)
    # ============================================================================
    ax3 = fig.add_subplot(gs[1, 0])

    vib_freqs = [safe_get(drug, 'vibrational_frequency', 1e12) for drug in drugs]
    vib_freqs_log = np.log10(vib_freqs)

    bars = ax3.bar(range(len(drug_names)), vib_freqs_log, 
                   color=[colors[name] for name in drug_names],
                   alpha=0.85, edgecolor='black', linewidth=1.5)

    # Add value labels
    for i, (freq, freq_log) in enumerate(zip(vib_freqs, vib_freqs_log)):
        ax3.text(i, freq_log + 0.1, f'{freq:.2e} Hz\n({freq_log:.1f} log₁₀)', 
                 ha='center', va='bottom', fontsize=7, fontweight='bold',
                 color=colors[drug_names[i]])

    ax3.set_xlabel('Drug', fontsize=12, fontweight='bold')
    ax3.set_ylabel('Vibrational Frequency (log₁₀ Hz)', fontsize=12, fontweight='bold')
    ax3.set_title('(C) Molecular Vibrational Frequencies', 
                  fontsize=13, fontweight='bold', pad=15)
    ax3.set_xticks(range(len(drug_names)))
    ax3.set_xticklabels(drug_names, fontsize=9, fontweight='bold', rotation=45, ha='right')
    ax3.grid(axis='y', alpha=0.3, linestyle='--', linewidth=0.8)
    ax3.spines['top'].set_visible(False)
    ax3.spines['right'].set_visible(False)

    # Add reference lines
    ax3.axhline(y=12, color='gray', linestyle='--', linewidth=1, alpha=0.5, label='10¹² Hz (THz)')
    ax3.axhline(y=13, color='gray', linestyle=':', linewidth=1, alpha=0.5, label='10¹³ Hz')
    ax3.legend(loc='upper right', fontsize=8)

    # ============================================================================
    # PANEL D: O₂ Aggregation Constants (Log Scale)
    # ============================================================================
    ax4 = fig.add_subplot(gs[1, 1])

    agg_constants = [safe_get(drug, 'o2_aggregation_constant', 1000) for drug in drugs]
    agg_log = np.log10(agg_constants)

    bars = ax4.bar(range(len(drug_names)), agg_log,
                   color=[colors[name] for name in drug_names],
                   alpha=0.85, edgecolor='black', linewidth=1.5)

    # Add value labels
    for i, (agg, agg_l) in enumerate(zip(agg_constants, agg_log)):
        ax4.text(i, agg_l + 0.05, f'{agg:.1e} M⁻¹\n({agg_l:.1f} log₁₀)', 
                 ha='center', va='bottom', fontsize=7, fontweight='bold',
                 color=colors[drug_names[i]])

    ax4.set_xlabel('Drug', fontsize=12, fontweight='bold')
    ax4.set_ylabel('O₂ Aggregation Constant (log₁₀ M⁻¹)', fontsize=12, fontweight='bold')
    ax4.set_title('(D) Drug-Oxygen Aggregation Constants', 
                  fontsize=13, fontweight='bold', pad=15)
    ax4.set_xticks(range(len(drug_names)))
    ax4.set_xticklabels(drug_names, fontsize=9, fontweight='bold', rotation=45, ha='right')
    ax4.grid(axis='y', alpha=0.3, linestyle='--', linewidth=0.8)
    ax4.spines['top'].set_visible(False)
    ax4.spines['right'].set_visible(False)

    # Add threshold line
    ax4.axhline(y=4, color='red', linestyle='--', linewidth=2, alpha=0.7, 
                label='Threshold: 10⁴ M⁻¹')
    ax4.legend(loc='lower right', fontsize=9)

    # ============================================================================
    # PANEL E: Electromagnetic Coupling Strength
    # ============================================================================
    ax5 = fig.add_subplot(gs[2, 0])

    em_coupling = [safe_get(drug, 'em_coupling_strength', 0.1) for drug in drugs]
    
    # Try different possible keys for paramagnetic susceptibility
    paramagnetic_keys = ['paramagnetic_susceptibility', 'magnetic_susceptibility', 
                         'susceptibility', 'chi_m']
    paramagnetic = []
    for drug in drugs:
        found = False
        for key in paramagnetic_keys:
            if key in drug:
                paramagnetic.append(drug[key])
                found = True
                break
        if not found:
            # Calculate from em_coupling if not available
            paramagnetic.append(safe_get(drug, 'em_coupling_strength', 0.1) * 1e-6)

    x_drugs = np.arange(len(drug_names))
    width_em = 0.35

    bars1 = ax5.bar(x_drugs - width_em/2, em_coupling, width_em,
                    label='EM Coupling Strength', 
                    color=[colors[name] for name in drug_names],
                    alpha=0.85, edgecolor='black', linewidth=1.5)

    ax5_twin = ax5.twinx()
    bars2 = ax5_twin.bar(x_drugs + width_em/2, paramagnetic, width_em,
                         label='Paramagnetic Susceptibility',
                         color=[colors[name] for name in drug_names],
                         alpha=0.5, edgecolor='black', linewidth=1.5, hatch='///')

    # Add value labels
    if em_coupling:
        max_em = max(em_coupling)
        for i, em in enumerate(em_coupling):
            ax5.text(i - width_em/2, em + max_em*0.02, f'{em:.3f}', 
                     ha='center', va='bottom', fontsize=7, fontweight='bold',
                     color=colors[drug_names[i]], rotation=90)
    
    if paramagnetic:
        max_para = max(paramagnetic)
        for i, para in enumerate(paramagnetic):
            ax5_twin.text(i + width_em/2, para + max_para*0.02, f'{para:.2e}', 
                          ha='center', va='bottom', fontsize=7, fontweight='bold',
                          color=colors[drug_names[i]], rotation=90)

    ax5.set_xlabel('Drug', fontsize=12, fontweight='bold')
    ax5.set_ylabel('EM Coupling Strength (arb. units)', fontsize=11, fontweight='bold')
    ax5_twin.set_ylabel('Paramagnetic Susceptibility (CGS)', fontsize=11, fontweight='bold')
    ax5.set_title('(E) Electromagnetic Coupling and Paramagnetic Properties', 
                  fontsize=13, fontweight='bold', pad=15)
    ax5.set_xticks(x_drugs)
    ax5.set_xticklabels(drug_names, fontsize=9, fontweight='bold', rotation=45, ha='right')
    ax5.grid(axis='y', alpha=0.3, linestyle='--', linewidth=0.8)
    ax5.spines['top'].set_visible(False)

    # Combined legend
    lines1, labels1 = ax5.get_legend_handles_labels()
    lines2, labels2 = ax5_twin.get_legend_handles_labels()
    ax5.legend(lines1 + lines2, labels1 + labels2, loc='upper left', 
               frameon=True, framealpha=0.95, edgecolor='black', fontsize=9)

    # ============================================================================
    # PANEL F: Resonance Quality Factors and Phase-Lock Capability
    # ============================================================================
    ax6 = fig.add_subplot(gs[2, 1])

    q_factors = [safe_get(drug, 'resonance_quality_factor', 1.0) for drug in drugs]
    phase_lock = [safe_get(drug, 'phase_lock_capability', 0.5) for drug in drugs]

    x_drugs = np.arange(len(drug_names))

    # Create scatter plot with size representing phase-lock capability
    scatter = ax6.scatter(x_drugs, q_factors, 
                          s=[p*500 for p in phase_lock],
                          c=[colors[name] for name in drug_names],
                          alpha=0.7, edgecolor='black', linewidth=2)

    # Add connecting lines
    ax6.plot(x_drugs, q_factors, 'k--', alpha=0.3, linewidth=1.5, zorder=0)

    # Add value labels
    if q_factors:
        max_q = max(q_factors)
        for i, (q, pl) in enumerate(zip(q_factors, phase_lock)):
            ax6.text(i, q + max_q*0.03, f'Q={q:.2f}\nΦ={pl:.2f}', 
                     ha='center', va='bottom', fontsize=7, fontweight='bold',
                     color=colors[drug_names[i]])

    ax6.set_xlabel('Drug', fontsize=12, fontweight='bold')
    ax6.set_ylabel('Resonance Quality Factor (Q)', fontsize=12, fontweight='bold')
    ax6.set_title('(F) Resonance Quality Factors and Phase-Lock Capability', 
                  fontsize=13, fontweight='bold', pad=15)
    ax6.set_xticks(x_drugs)
    ax6.set_xticklabels(drug_names, fontsize=9, fontweight='bold', rotation=45, ha='right')
    if q_factors:
        ax6.set_ylim(0, max(q_factors) * 1.3)
    ax6.grid(alpha=0.3, linestyle='--', linewidth=0.8)
    ax6.spines['top'].set_visible(False)
    ax6.spines['right'].set_visible(False)

    # Add legend for bubble size
    legend_sizes = [0.5, 0.75, 1.0]
    legend_labels = ['Φ = 0.5', 'Φ = 0.75', 'Φ = 1.0']
    legend_elements = [plt.scatter([], [], s=size*500, c='gray', alpha=0.7, 
                                   edgecolor='black', linewidth=2, label=label)
                       for size, label in zip(legend_sizes, legend_labels)]
    ax6.legend(handles=legend_elements, loc='upper right', frameon=True, 
               framealpha=0.95, edgecolor='black', fontsize=9,
               title='Phase-Lock Capability', title_fontsize=9)

    # Main title
    fig.suptitle('Molecular Properties for Consciousness Programming: Drug Characterization',
                 fontsize=16, fontweight='bold', y=0.97)

    # Subtitle
    subtitle = (f'Timestamp: {data["timestamp"]} | '
                f'Analysis: {len(drugs)} pharmaceutical agents with O₂ aggregation K_agg > 10³ M⁻¹')
    fig.text(0.5, 0.945, subtitle, ha='center', fontsize=9, style='italic')

    plt.savefig('drug_molecular_properties_6panel.png', dpi=300, bbox_inches='tight')
    plt.savefig('drug_molecular_properties_6panel.pdf', bbox_inches='tight')
    print("✓ Drug properties visualization saved")
    print(f"  - Analyzed {len(drugs)} drugs: {', '.join(drug_names)}")
    print(f"  - Output: drug_molecular_properties_6panel.png/pdf")

    plt.close()


if __name__ == "__main__":
    main()
