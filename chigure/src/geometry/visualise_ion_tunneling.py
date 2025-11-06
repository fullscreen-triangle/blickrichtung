# visualize_ion_tunneling.py
import json
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.gridspec import GridSpec
from mpl_toolkits.mplot3d import Axes3D
import warnings
warnings.filterwarnings('ignore')

sns.set_style("whitegrid")

def load_ion_data():
    """Load quantum ion tunneling data"""
    print("Loading quantum ion tunneling data...")
    with open('experiment_1_ion_tunneling.json', 'r') as f:
        data = json.load(f)
    return data

def parse_field_data(field_str):
    """Parse field magnitude/phase strings into arrays"""
    try:
        # Remove brackets and split
        field_str = field_str.replace('[', '').replace(']', '')
        # Handle ellipsis
        if '...' in field_str:
            parts = field_str.split('...')
            start_vals = [float(x) for x in parts[0].split() if x]
            end_vals = [float(x) for x in parts[-1].split() if x]
            # Return start and end values
            return np.array(start_vals + end_vals)
        else:
            return np.array([float(x) for x in field_str.split() if x])
    except:
        return np.array([])

def create_ion_comparison_overview(data, output_dir='./'):
    """
    Create comprehensive overview comparing all ions
    """
    print("\nGenerating ion comparison overview...")
    
    ion_data = data['ion_quantum_data']
    ions = list(ion_data.keys())
    
    fig = plt.figure(figsize=(20, 14))
    gs = GridSpec(4, 3, figure=fig, hspace=0.4, wspace=0.35)
    
    # Colors for each ion
    ion_colors = {
        'H+': '#E74C3C',
        'Na+': '#3498DB',
        'K+': '#9B59B6',
        'Ca2+': '#2ECC71',
        'Mg2+': '#F39C12'
    }
    
    # Extract metrics
    masses = [ion_data[ion]['mass'] for ion in ions]
    wavelengths = [ion_data[ion]['de_broglie_wavelength'] for ion in ions]
    tunneling_probs = [ion_data[ion]['tunneling_probability'] for ion in ions]
    coherence_times = [ion_data[ion]['coherence_time'] for ion in ions]
    coherences = [ion_data[ion]['coherence'] for ion in ions]
    velocities = [ion_data[ion]['velocity'] for ion in ions]
    frequencies = [ion_data[ion]['quantum_frequency'] for ion in ions]
    
    # ========================================================================
    # Panel 1: Ion Masses
    # ========================================================================
    ax1 = fig.add_subplot(gs[0, 0])
    
    colors = [ion_colors[ion] for ion in ions]
    bars = ax1.bar(ions, np.array(masses) * 1e27, color=colors, alpha=0.7, 
                   edgecolor='black', linewidth=2)
    
    ax1.set_ylabel('Mass (×10⁻²⁷ kg)', fontweight='bold', fontsize=11)
    ax1.set_title('A. Ion Masses', fontweight='bold', fontsize=13)
    ax1.grid(True, alpha=0.3, axis='y')
    
    # Add values on bars
    for bar, mass in zip(bars, masses):
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height,
                f'{mass*1e27:.2f}',
                ha='center', va='bottom', fontweight='bold', fontsize=9)
    
    # ========================================================================
    # Panel 2: de Broglie Wavelengths
    # ========================================================================
    ax2 = fig.add_subplot(gs[0, 1])
    
    bars2 = ax2.bar(ions, np.array(wavelengths) * 1e12, color=colors, alpha=0.7,
                    edgecolor='black', linewidth=2)
    
    ax2.set_ylabel('Wavelength (pm)', fontweight='bold', fontsize=11)
    ax2.set_title('B. de Broglie Wavelengths', fontweight='bold', fontsize=13)
    ax2.grid(True, alpha=0.3, axis='y')
    
    for bar, wl in zip(bars2, wavelengths):
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height,
                f'{wl*1e12:.2f}',
                ha='center', va='bottom', fontweight='bold', fontsize=9)
    
    # ========================================================================
    # Panel 3: Tunneling Probabilities (log scale)
    # ========================================================================
    ax3 = fig.add_subplot(gs[0, 2])
    
    # Handle zero values
    tunneling_plot = []
    for prob in tunneling_probs:
        if prob > 0:
            tunneling_plot.append(np.log10(prob))
        else:
            tunneling_plot.append(-400)  # Very small value for zero
    
    bars3 = ax3.bar(ions, tunneling_plot, color=colors, alpha=0.7,
                    edgecolor='black', linewidth=2)
    
    ax3.set_ylabel('log₁₀(Tunneling Probability)', fontweight='bold', fontsize=11)
    ax3.set_title('C. Quantum Tunneling Probability', fontweight='bold', fontsize=13)
    ax3.grid(True, alpha=0.3, axis='y')
    ax3.axhline(y=-300, color='red', linestyle='--', linewidth=2, 
                label='Effective Zero', alpha=0.5)
    ax3.legend(fontsize=9)
    
    # ========================================================================
    # Panel 4: Coherence Times
    # ========================================================================
    ax4 = fig.add_subplot(gs[1, 0])
    
    bars4 = ax4.bar(ions, np.array(coherence_times) * 1e15, color=colors, alpha=0.7,
                    edgecolor='black', linewidth=2)
    
    ax4.set_ylabel('Coherence Time (fs)', fontweight='bold', fontsize=11)
    ax4.set_title('D. Quantum Coherence Time', fontweight='bold', fontsize=13)
    ax4.grid(True, alpha=0.3, axis='y')
    
    for bar, ct in zip(bars4, coherence_times):
        height = bar.get_height()
        ax4.text(bar.get_x() + bar.get_width()/2., height,
                f'{ct*1e15:.2f}',
                ha='center', va='bottom', fontweight='bold', fontsize=9)
    
    # ========================================================================
    # Panel 5: Coherence Values
    # ========================================================================
    ax5 = fig.add_subplot(gs[1, 1])
    
    bars5 = ax5.bar(ions, coherences, color=colors, alpha=0.7,
                    edgecolor='black', linewidth=2)
    
    ax5.set_ylabel('Coherence', fontweight='bold', fontsize=11)
    ax5.set_title('E. Quantum Coherence', fontweight='bold', fontsize=13)
    ax5.set_ylim([0, 1.1])
    ax5.grid(True, alpha=0.3, axis='y')
    
    for bar, coh in zip(bars5, coherences):
        height = bar.get_height()
        ax5.text(bar.get_x() + bar.get_width()/2., height,
                f'{coh:.6f}' if coh < 0.01 else f'{coh:.2f}',
                ha='center', va='bottom', fontweight='bold', fontsize=9)
    
    # ========================================================================
    # Panel 6: Ion Velocities
    # ========================================================================
    ax6 = fig.add_subplot(gs[1, 2])
    
    bars6 = ax6.bar(ions, velocities, color=colors, alpha=0.7,
                    edgecolor='black', linewidth=2)
    
    ax6.set_ylabel('Velocity (m/s)', fontweight='bold', fontsize=11)
    ax6.set_title('F. Ion Velocities', fontweight='bold', fontsize=13)
    ax6.grid(True, alpha=0.3, axis='y')
    
    for bar, vel in zip(bars6, velocities):
        height = bar.get_height()
        ax6.text(bar.get_x() + bar.get_width()/2., height,
                f'{vel:.0f}',
                ha='center', va='bottom', fontweight='bold', fontsize=9)
    
    # ========================================================================
    # Panel 7: Mass vs Wavelength
    # ========================================================================
    ax7 = fig.add_subplot(gs[2, 0])
    
    for i, ion in enumerate(ions):
        ax7.scatter(masses[i]*1e27, wavelengths[i]*1e12, 
                   s=200, color=ion_colors[ion], alpha=0.7,
                   edgecolors='black', linewidth=2, label=ion)
    
    ax7.set_xlabel('Mass (×10⁻²⁷ kg)', fontweight='bold', fontsize=11)
    ax7.set_ylabel('Wavelength (pm)', fontweight='bold', fontsize=11)
    ax7.set_title('G. Mass-Wavelength Relationship', fontweight='bold', fontsize=13)
    ax7.legend(fontsize=10)
    ax7.grid(True, alpha=0.3)
    
    # Add theoretical curve
    mass_range = np.linspace(min(masses), max(masses), 100)
    h = 6.626e-34  # Planck constant
    # λ = h / (m * v), assuming constant thermal velocity
    theoretical_wl = h / (mass_range * velocities[0])
    ax7.plot(mass_range*1e27, theoretical_wl*1e12, 'r--', 
            linewidth=2, alpha=0.5, label='Theoretical')
    
    # ========================================================================
    # Panel 8: Coherence vs Tunneling
    # ========================================================================
    ax8 = fig.add_subplot(gs[2, 1])
    
    for i, ion in enumerate(ions):
        tunnel_val = tunneling_probs[i] if tunneling_probs[i] > 0 else 1e-400
        ax8.scatter(coherences[i], tunnel_val,
                   s=200, color=ion_colors[ion], alpha=0.7,
                   edgecolors='black', linewidth=2, label=ion)
    
    ax8.set_xlabel('Coherence', fontweight='bold', fontsize=11)
    ax8.set_ylabel('Tunneling Probability', fontweight='bold', fontsize=11)
    ax8.set_title('H. Coherence vs Tunneling', fontweight='bold', fontsize=13)
    ax8.set_yscale('log')
    ax8.legend(fontsize=10)
    ax8.grid(True, alpha=0.3)
    
    # ========================================================================
    # Panel 9: Quantum Frequency Comparison
    # ========================================================================
    ax9 = fig.add_subplot(gs[2, 2])
    
    # All ions have same frequency - show as single value
    unique_freq = frequencies[0]
    
    ax9.text(0.5, 0.6, f'Quantum Frequency:', 
            ha='center', va='center', fontsize=14, fontweight='bold',
            transform=ax9.transAxes)
    ax9.text(0.5, 0.4, f'{unique_freq:.2e} Hz', 
            ha='center', va='center', fontsize=16, fontweight='bold',
            color='#E74C3C', transform=ax9.transAxes)
    ax9.text(0.5, 0.25, f'= {unique_freq/1e12:.1f} THz', 
            ha='center', va='center', fontsize=12,
            transform=ax9.transAxes)
    
    ax9.set_title('I. Quantum Frequency (All Ions)', fontweight='bold', fontsize=13)
    ax9.axis('off')
    
    # ========================================================================
    # Panel 10: Consciousness Predictions
    # ========================================================================
    ax10 = fig.add_subplot(gs[3, :])
    ax10.axis('off')
    
    predictions = data['consciousness_predictions']
    
    summary_text = f"""
╔════════════════════════════════════════════════════════════════════════════════════════════════╗
║                           QUANTUM ION TUNNELING ANALYSIS SUMMARY                                ║
╚════════════════════════════════════════════════════════════════════════════════════════════════╝

ION PROPERTIES:
  H⁺  (Proton):     Mass = {masses[0]*1e27:.2f}×10⁻²⁷ kg  |  λ = {wavelengths[0]*1e12:.2f} pm  |  P_tunnel = {tunneling_probs[0]:.2e}  |  Coherence = {coherences[0]:.6f}
  Na⁺ (Sodium):     Mass = {masses[1]*1e27:.2f}×10⁻²⁷ kg  |  λ = {wavelengths[1]*1e12:.2f} pm  |  P_tunnel = {tunneling_probs[1]:.2e}  |  Coherence = {coherences[1]:.2f}
  K⁺  (Potassium):  Mass = {masses[2]*1e27:.2f}×10⁻²⁷ kg  |  λ = {wavelengths[2]*1e12:.2f} pm  |  P_tunnel = {tunneling_probs[2]:.2e}  |  Coherence = {coherences[2]:.2f}
  Ca²⁺ (Calcium):   Mass = {masses[3]*1e27:.2f}×10⁻²⁷ kg  |  λ = {wavelengths[3]*1e12:.2f} pm  |  P_tunnel = {tunneling_probs[3]:.2e}  |  Coherence = {coherences[3]:.2f}
  Mg²⁺ (Magnesium): Mass = {masses[4]*1e27:.2f}×10⁻²⁷ kg  |  λ = {wavelengths[4]*1e12:.2f} pm  |  P_tunnel = {tunneling_probs[4]:.2e}  |  Coherence = {coherences[4]:.2f}

QUANTUM PARAMETERS:
  • Coherence Time: {coherence_times[0]*1e15:.2f} femtoseconds (all ions)
  • Quantum Frequency: {frequencies[0]:.2e} Hz = {frequencies[0]/1e12:.1f} THz
  • Temperature: 310 K (physiological)

KEY FINDINGS:
  ✓ H⁺ exhibits quantum tunneling (P = {tunneling_probs[0]:.2e})
  ✓ H⁺ has lowest coherence ({coherences[0]:.6f}) - indicates quantum decoherence
  ✓ Heavier ions (Na⁺, K⁺, Ca²⁺, Mg²⁺) show zero tunneling probability
  ✓ Heavier ions maintain perfect coherence (1.0) - classical behavior
  ✓ H⁺ velocity ({velocities[0]:.1f} m/s) >> other ions ({velocities[1]:.1f}-{velocities[4]:.1f} m/s)

CONSCIOUSNESS PREDICTIONS:
  • H⁺ Dominant: {predictions['h_plus_dominant']}
  • Sufficient Coherence: {predictions['sufficient_coherence']}
  • Timescale Match: {predictions['timescale_match']}
  • Emergence Possible: {predictions['emergence_possible']}

INTERPRETATION:
  The data suggests H⁺ (protons) are the ONLY ions exhibiting quantum behavior at physiological temperatures.
  However, coherence time (~25 fs) is FAR shorter than neural timescales (ms), suggesting:
  
  1. Quantum effects are TRANSIENT and localized
  2. Classical ion dynamics dominate neural computation
  3. Consciousness likely emerges from CLASSICAL network dynamics, not quantum coherence
  4. H⁺ quantum tunneling may play role in proton-coupled electron transfer (enzyme catalysis)
  
  ⚠ CONCLUSION: Quantum ion tunneling alone CANNOT explain consciousness
"""
    
    ax10.text(0.02, 0.98, summary_text, transform=ax10.transAxes,
             fontsize=9, verticalalignment='top', fontfamily='monospace',
             bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.5))
    
    # Main title
    fig.suptitle('Quantum Ion Tunneling in Neural Systems: Comparative Analysis of H⁺, Na⁺, K⁺, Ca²⁺, Mg²⁺',
                 fontsize=16, fontweight='bold', y=0.998)
    
    # Save
    output_path = f'{output_dir}/ion_tunneling_overview.png'
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"✓ Saved to {output_path}")
    
    plt.close()

def create_h_plus_detailed_analysis(data, output_dir='./'):
    """
    Detailed analysis of H+ (proton) quantum behavior
    """
    print("\nGenerating H+ detailed analysis...")
    
    h_plus = data['ion_quantum_data']['H+']
    time_array = np.array(data['time_array'])
    
    # Parse field data
    field_mag = parse_field_data(h_plus['field_magnitude'])
    field_phase = parse_field_data(h_plus['field_phase'])
    
    fig = plt.figure(figsize=(18, 12))
    gs = GridSpec(3, 3, figure=fig, hspace=0.4, wspace=0.35)
    
    # ========================================================================
    # Panel 1: Field Magnitude Time Series
    # ========================================================================
    ax1 = fig.add_subplot(gs[0, :])
    
    if len(field_mag) > 0:
        time_sample = time_array[:len(field_mag)]
        ax1.plot(time_sample * 1e6, field_mag, color='#E74C3C', 
                linewidth=1, alpha=0.7)
        ax1.set_xlabel('Time (μs)', fontweight='bold', fontsize=11)
        ax1.set_ylabel('Field Magnitude', fontweight='bold', fontsize=11)
        ax1.set_title('A. H⁺ Quantum Field Magnitude Over Time', 
                     fontweight='bold', fontsize=13)
        ax1.grid(True, alpha=0.3)
        ax1.set_yscale('log')
    
    # ========================================================================
    # Panel 2: Field Phase Time Series
    # ========================================================================
    ax2 = fig.add_subplot(gs[1, :])
    
    if len(field_phase) > 0:
        time_sample = time_array[:len(field_phase)]
        ax2.plot(time_sample * 1e6, field_phase, color='#9B59B6',
                linewidth=1, alpha=0.7)
        ax2.set_xlabel('Time (μs)', fontweight='bold', fontsize=11)
        ax2.set_ylabel('Field Phase (radians)', fontweight='bold', fontsize=11)
        ax2.set_title('B. H⁺ Quantum Field Phase Evolution',
                     fontweight='bold', fontsize=13)
        ax2.grid(True, alpha=0.3)
        ax2.axhline(y=0, color='red', linestyle='--', linewidth=1, alpha=0.5)
    
    # ========================================================================
    # Panel 3: Phase Space (Magnitude vs Phase)
    # ========================================================================
    ax3 = fig.add_subplot(gs[2, 0])
    
    if len(field_mag) > 0 and len(field_phase) > 0:
        min_len = min(len(field_mag), len(field_phase))
        scatter = ax3.scatter(field_phase[:min_len], field_mag[:min_len],
                             c=time_array[:min_len]*1e6, cmap='viridis',
                             s=10, alpha=0.5)
        ax3.set_xlabel('Phase (radians)', fontweight='bold', fontsize=11)
        ax3.set_ylabel('Magnitude', fontweight='bold', fontsize=11)
        ax3.set_title('C. Phase Space Portrait', fontweight='bold', fontsize=13)
        ax3.set_yscale('log')
        plt.colorbar(scatter, ax=ax3, label='Time (μs)')
        ax3.grid(True, alpha=0.3)
    
    # ========================================================================
    # Panel 4: Quantum Properties Summary
    # ========================================================================
    ax4 = fig.add_subplot(gs[2, 1])
    ax4.axis('off')
    
    properties_text = f"""
╔═══════════════════════════════════╗
║   H⁺ QUANTUM PROPERTIES           ║
╚═══════════════════════════════════╝

BASIC PROPERTIES:
  • Mass: {h_plus['mass']:.2e} kg
  • Velocity: {h_plus['velocity']:.1f} m/s

QUANTUM PARAMETERS:
  • de Broglie λ: {h_plus['de_broglie_wavelength']*1e12:.2f} pm
  • Tunneling P: {h_plus['tunneling_probability']:.2e}
  • Coherence time: {h_plus['coherence_time']*1e15:.2f} fs
  • Quantum freq: {h_plus['quantum_frequency']:.2e} Hz
  • Coherence: {h_plus['coherence']:.6f}

INTERPRETATION:
  The extremely low coherence
  ({h_plus['coherence']:.2e}) indicates
  rapid quantum decoherence.
  
  Coherence time of ~25 fs is
  orders of magnitude shorter
  than neural processing times
  (~1-100 ms).
  
  This suggests quantum effects
  are TRANSIENT and unlikely to
  support sustained quantum
  computation in neurons.
"""
    
    ax4.text(0.05, 0.95, properties_text, transform=ax4.transAxes,
            fontsize=9, verticalalignment='top', fontfamily='monospace',
            bbox=dict(boxstyle='round', facecolor='lightcoral', alpha=0.3))
    
    # ========================================================================
    # Panel 5: Timescale Comparison
    # ========================================================================
    ax5 = fig.add_subplot(gs[2, 2])
    
    timescales = {
        'H⁺ Coherence': h_plus['coherence_time'],
        'Synaptic\nTransmission': 1e-3,
        'Action\nPotential': 1e-3,
        'Neural\nIntegration': 10e-3,
        'Conscious\nPerception': 100e-3
    }
    
    names = list(timescales.keys())
    times = list(timescales.values())
    colors_ts = ['#E74C3C', '#3498DB', '#9B59B6', '#2ECC71', '#F39C12']
    
    bars = ax5.barh(names, np.log10(np.array(times)*1e3), color=colors_ts,
                    alpha=0.7, edgecolor='black', linewidth=2)
    
    ax5.set_xlabel('log₁₀(Time in ms)', fontweight='bold', fontsize=11)
    ax5.set_title('D. Timescale Comparison', fontweight='bold', fontsize=13)
    ax5.grid(True, alpha=0.3, axis='x')
    
    # Add value labels
    for bar, time in zip(bars, times):
        width = bar.get_width()
        ax5.text(width, bar.get_y() + bar.get_height()/2.,
                f'{time*1e3:.2e} ms',
                ha='left', va='center', fontweight='bold', fontsize=8)
    
    # Main title
    fig.suptitle('H⁺ (Proton) Quantum Behavior: Detailed Analysis',
                 fontsize=16, fontweight='bold', y=0.998)
    
    # Save
    output_path = f'{output_dir}/h_plus_detailed_analysis.png'
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"✓ Saved to {output_path}")
    
    plt.close()

def create_quantum_classical_boundary(data, output_dir='./'):
    """
    Visualize the quantum-classical boundary
    """
    print("\nGenerating quantum-classical boundary visualization...")
    
    ion_data = data['ion_quantum_data']
    ions = list(ion_data.keys())
    
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    
    # Extract data
    masses = np.array([ion_data[ion]['mass'] for ion in ions])
    wavelengths = np.array([ion_data[ion]['de_broglie_wavelength'] for ion in ions])
    tunneling_probs = np.array([ion_data[ion]['tunneling_probability'] for ion in ions])
    coherences = np.array([ion_data[ion]['coherence'] for ion in ions])
    
    ion_colors = {
        'H+': '#E74C3C',
        'Na+': '#3498DB',
        'K+': '#9B59B6',
        'Ca2+': '#2ECC71',
        'Mg2+': '#F39C12'
    }
    
    # ========================================================================
    # Panel 1: Quantum vs Classical Regime
    # ========================================================================
    ax1 = axes[0, 0]
    
    for i, ion in enumerate(ions):
        tunnel_val = tunneling_probs[i] if tunneling_probs[i] > 0 else 1e-400
        ax1.scatter(masses[i]*1e27, tunnel_val,
                   s=300, color=ion_colors[ion], alpha=0.7,
                   edgecolors='black', linewidth=2, label=ion, zorder=3)
    
    # Add boundary line
    ax1.axhline(y=1e-100, color='red', linestyle='--', linewidth=3,
               label='Quantum-Classical Boundary', zorder=2)
    
    # Shade regions
    ax1.fill_between([0, 100], 1e-400, 1e-100, alpha=0.2, color='blue',
                     label='Quantum Regime')
    ax1.fill_between([0, 100], 1e-100, 1, alpha=0.2, color='gray',
                     label='Classical Regime')
    
    ax1.set_xlabel('Mass (×10⁻²⁷ kg)', fontweight='bold', fontsize=12)
    ax1.set_ylabel('Tunneling Probability', fontweight='bold', fontsize=12)
    ax1.set_title('A. Quantum-Classical Boundary', fontweight='bold', fontsize=14)
    ax1.set_yscale('log')
    ax1.set_ylim([1e-400, 1])
    ax1.legend(fontsize=9, loc='upper right')
    ax1.grid(True, alpha=0.3)
    
    # ========================================================================
    # Panel 2: Coherence vs Mass
    # ========================================================================
    ax2 = axes[0, 1]
    
    for i, ion in enumerate(ions):
        ax2.scatter(masses[i]*1e27, coherences[i],
                   s=300, color=ion_colors[ion], alpha=0.7,
                   edgecolors='black', linewidth=2, label=ion)
    
    ax2.set_xlabel('Mass (×10⁻²⁷ kg)', fontweight='bold', fontsize=12)
    ax2.set_ylabel('Coherence', fontweight='bold', fontsize=12)
    ax2.set_title('B. Mass vs Quantum Coherence', fontweight='bold', fontsize=14)
    ax2.set_ylim([0, 1.1])
    ax2.legend(fontsize=10)
    ax2.grid(True, alpha=0.3)
    
    # Add annotation
    ax2.annotate('Quantum\nDecoherence', xy=(masses[0]*1e27, coherences[0]),
                xytext=(10, 0.5), fontsize=11, fontweight='bold',
                arrowprops=dict(arrowstyle='->', color='red', lw=2))
    ax2.annotate('Classical\nBehavior', xy=(masses[1]*1e27, coherences[1]),
                xytext=(20, 0.7), fontsize=11, fontweight='bold',
                arrowprops=dict(arrowstyle='->', color='blue', lw=2))
    
    # ========================================================================
    # Panel 3: Wavelength vs Mass (Quantum Criterion)
    # ========================================================================
    ax3 = axes[1, 0]
    
    for i, ion in enumerate(ions):
        ax3.scatter(masses[i]*1e27, wavelengths[i]*1e12,
                   s=300, color=ion_colors[ion], alpha=0.7,
                   edgecolors='black', linewidth=2, label=ion)
    
    # Add thermal de Broglie wavelength criterion
    # λ_thermal ~ h / sqrt(m * k_B * T)
    mass_range = np.linspace(min(masses), max(masses), 100)
    h = 6.626e-34
    k_B = 1.381e-23
    T = 310  # K
    lambda_thermal = h / np.sqrt(mass_range * k_B * T)
    
    ax3.plot(mass_range*1e27, lambda_thermal*1e12, 'r--', linewidth=2,
            label='Thermal λ (310K)', alpha=0.7)
    
    ax3.set_xlabel('Mass (×10⁻²⁷ kg)', fontweight='bold', fontsize=12)
    ax3.set_ylabel('de Broglie Wavelength (pm)', fontweight='bold', fontsize=12)
    ax3.set_title('C. Quantum Size Criterion', fontweight='bold', fontsize=14)
    ax3.legend(fontsize=10)
    ax3.grid(True, alpha=0.3)
    
    # ========================================================================
    # Panel 4: Summary Table
    # ========================================================================
    ax4 = axes[1, 1]
    ax4.axis('off')
    
    summary_text = f"""
╔═══════════════════════════════════════════════════════════╗
║         QUANTUM-CLASSICAL BOUNDARY ANALYSIS               ║
╚═══════════════════════════════════════════════════════════╝

QUANTUM REGIME (H⁺):
  • Exhibits tunneling (P = {tunneling_probs[0]:.2e})
  • Low coherence ({coherences[0]:.6f}) → rapid decoherence
  • Wavelength ({wavelengths[0]*1e12:.2f} pm) > atomic scale
  • Lightest ion → highest quantum character

CLASSICAL REGIME (Na⁺, K⁺, Ca²⁺, Mg²⁺):
  • Zero tunneling probability
  • Perfect coherence (1.0) → classical particles
  • Wavelengths < 5 pm (sub-atomic)
  • Heavier masses → classical behavior

BOUNDARY CRITERION:
  Quantum effects become negligible when:
  
  1. Mass > ~10×10⁻²⁷ kg (> 6 proton masses)
  2. Tunneling probability < 10⁻¹⁰⁰
  3. de Broglie wavelength < atomic spacing
  4. Decoherence time << interaction time

IMPLICATIONS FOR CONSCIOUSNESS:
  ✓ Only H⁺ shows quantum behavior
  ✓ All major neural ions (Na⁺, K⁺, Ca²⁺) are CLASSICAL
  ✓ Action potentials = classical ion flow
  ✓ Synaptic transmission = classical diffusion
  
  → Neural computation is CLASSICAL at ion level
  → Quantum effects limited to:
      • Enzyme catalysis (proton transfer)
      • Photoreceptor isomerization
      • Olfactory receptors (disputed)
  
  ⚠ CONCLUSION: Consciousness emerges from CLASSICAL
     network dynamics, not quantum ion coherence
"""
    
    ax4.text(0.05, 0.95, summary_text, transform=ax4.transAxes,
            fontsize=9.5, verticalalignment='top', fontfamily='monospace',
            bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.3))
    
    plt.suptitle('Quantum-Classical Boundary in Neural Ion Channels',
                fontsize=16, fontweight='bold', y=0.995)
    plt.tight_layout()
    
    output_path = f'{output_dir}/quantum_classical_boundary.png'
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"✓ Saved to {output_path}")
    
    plt.close()

def main():
    """Main visualization pipeline"""
    print("="*70)
    print("QUANTUM ION TUNNELING VISUALIZATION")
    print("="*70)
    
    try:
        # Load data
        data = load_ion_data()
        
        print(f"\nData loaded successfully")
        print(f"  • Ions analyzed: {len(data['ion_quantum_data'])}")
        print(f"  • Time points: {len(data['time_array'])}")
        
        # Create visualizations
        create_ion_comparison_overview(data)
        create_h_plus_detailed_analysis(data)
        create_quantum_classical_boundary(data)
        
        print("\n" + "="*70)
        print("VISUALIZATION COMPLETE!")
        print("="*70)
        print("\nGenerated files:")
        print("  1. ion_tunneling_overview.png")
        print("  2. h_plus_detailed_analysis.png")
        print("  3. quantum_classical_boundary.png")
        
        print("\n" + "="*70)
        print("KEY FINDINGS:")
        print("="*70)
        print("  ✓ H⁺ is the ONLY ion exhibiting quantum tunneling")
        print("  ✓ Coherence time (~25 fs) << neural timescales (ms)")
        print("  ✓ Major neural ions (Na⁺, K⁺, Ca²⁺) are CLASSICAL")
        print("  ✓ Consciousness likely emerges from classical dynamics")
        print("="*70)
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
