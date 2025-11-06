import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import json
from scipy.interpolate import griddata
from scipy.stats import gaussian_kde
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.patches as mpatches
from matplotlib.patches import Circle, FancyBboxPatch
import warnings
import re
warnings.filterwarnings('ignore')

# Set publication quality defaults
plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300
plt.rcParams['font.size'] = 9
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['axes.linewidth'] = 1.5

# ============================================================================
# UTILITY FUNCTION TO PARSE NUMPY ARRAYS FROM JSON
# ============================================================================

def parse_numpy_array(array_string):
    """
    Safely parse numpy array string from JSON
    """
    try:
        # Remove brackets and split by whitespace
        clean_string = array_string.strip('[]')
        # Replace multiple spaces with single space
        clean_string = re.sub(r'\s+', ' ', clean_string)
        # Split and convert to complex numbers
        values = []
        for val in clean_string.split():
            if val == '...':
                continue
            try:
                # Handle complex numbers
                if 'j' in val:
                    values.append(complex(val))
                else:
                    values.append(float(val))
            except:
                continue
        return np.array(values)
    except Exception as e:
        print(f"Error parsing array: {e}")
        return np.array([])

# ============================================================================
# DATASET 1: ION TUNNELING - 6 PANEL FIGURE
# ============================================================================

def figure_1_ion_tunneling(save_path='figure_1_ion_tunneling.png'):
    """
    6-panel comprehensive analysis of ion quantum properties
    """
    print("Generating Figure 1: Ion Tunneling Analysis...")
    
    with open('experiment_1_ion_tunneling.json', 'r') as f:
        data = json.load(f)
    
    fig = plt.figure(figsize=(16, 10))
    gs = GridSpec(2, 3, figure=fig, hspace=0.35, wspace=0.35)
    
    ions = ['H+', 'Na+', 'K+', 'Ca2+', 'Mg2+']
    colors = ['#E74C3C', '#3498DB', '#2ECC71', '#F39C12', '#9B59B6']
    
    # Extract data
    masses = [data['ion_quantum_data'][ion]['mass'] for ion in ions]
    wavelengths = [data['ion_quantum_data'][ion]['de_broglie_wavelength'] for ion in ions]
    tunneling = [max(data['ion_quantum_data'][ion]['tunneling_probability'], 1e-320) for ion in ions]
    coherences = [data['ion_quantum_data'][ion]['coherence'] for ion in ions]
    coherence_times = [data['ion_quantum_data'][ion]['coherence_time'] for ion in ions]
    velocities = [data['ion_quantum_data'][ion]['velocity'] for ion in ions]
    
    # Panel A: Mass vs de Broglie Wavelength
    ax1 = fig.add_subplot(gs[0, 0])
    for ion, m, w, c in zip(ions, masses, wavelengths, colors):
        ax1.scatter(m, w, s=300, color=c, alpha=0.8, edgecolors='black', 
                   linewidth=2, label=ion, zorder=3)
    
    # Fit line
    log_m = np.log10(masses)
    log_w = np.log10(wavelengths)
    z = np.polyfit(log_m, log_w, 1)
    p = np.poly1d(z)
    m_fit = np.logspace(np.log10(min(masses)), np.log10(max(masses)), 100)
    w_fit = 10**p(np.log10(m_fit))
    ax1.plot(m_fit, w_fit, 'k--', alpha=0.5, linewidth=2, label=f'λ ∝ m^{z[0]:.2f}')
    
    ax1.set_xlabel('Ion Mass (kg)', fontweight='bold', fontsize=10)
    ax1.set_ylabel('de Broglie Wavelength (m)', fontweight='bold', fontsize=10)
    ax1.set_title('A. Quantum Scale Separation', fontweight='bold', fontsize=11, loc='left')
    ax1.set_xscale('log')
    ax1.set_yscale('log')
    ax1.legend(fontsize=8, loc='best', framealpha=0.95)
    ax1.grid(True, alpha=0.3, linestyle='--', which='both')
    
    # Panel B: Coherence Comparison
    ax2 = fig.add_subplot(gs[0, 1])
    x_pos = np.arange(len(ions))
    bars = ax2.bar(x_pos, coherences, color=colors, alpha=0.85, 
                   edgecolor='black', linewidth=2, width=0.6)
    
    # Add value labels
    for i, (bar, coh) in enumerate(zip(bars, coherences)):
        height = bar.get_height()
        if coh < 0.01:
            ax2.text(bar.get_x() + bar.get_width()/2., height,
                    f'{coh:.2e}', ha='center', va='bottom', fontsize=7, fontweight='bold')
        else:
            ax2.text(bar.get_x() + bar.get_width()/2., height,
                    f'{coh:.3f}', ha='center', va='bottom', fontsize=7, fontweight='bold')
    
    ax2.set_xticks(x_pos)
    ax2.set_xticklabels(ions, fontsize=10, fontweight='bold')
    ax2.set_ylabel('Coherence', fontweight='bold', fontsize=10)
    ax2.set_title('B. Ion Coherence Hierarchy', fontweight='bold', fontsize=11, loc='left')
    ax2.set_yscale('log')
    ax2.axhline(y=1.0, color='red', linestyle='--', linewidth=2, alpha=0.7, label='Perfect')
    ax2.axhline(y=0.001, color='orange', linestyle='--', linewidth=2, alpha=0.7, label='Threshold')
    ax2.legend(fontsize=8, loc='upper right', framealpha=0.95)
    ax2.grid(axis='y', alpha=0.3, linestyle='--')
    
    # Panel C: Tunneling Probability
    ax3 = fig.add_subplot(gs[0, 2])
    bars = ax3.bar(x_pos, tunneling, color=colors, alpha=0.85,
                   edgecolor='black', linewidth=2, width=0.6)
    
    ax3.set_xticks(x_pos)
    ax3.set_xticklabels(ions, fontsize=10, fontweight='bold')
    ax3.set_ylabel('Tunneling Probability', fontweight='bold', fontsize=10)
    ax3.set_title('C. Quantum Tunneling Effects', fontweight='bold', fontsize=11, loc='left')
    ax3.set_yscale('log')
    ax3.axhline(y=1e-100, color='red', linestyle='--', linewidth=2, alpha=0.7, 
               label='Negligible')
    ax3.legend(fontsize=8, loc='upper right', framealpha=0.95)
    ax3.grid(axis='y', alpha=0.3, linestyle='--')
    
    # Panel D: Velocity Distribution
    ax4 = fig.add_subplot(gs[1, 0])
    bars = ax4.barh(ions, velocities, color=colors, alpha=0.85,
                    edgecolor='black', linewidth=2, height=0.6)
    
    # Add value labels
    for bar, vel in zip(bars, velocities):
        width = bar.get_width()
        ax4.text(width, bar.get_y() + bar.get_height()/2.,
                f' {vel:.1f} m/s', ha='left', va='center', 
                fontsize=8, fontweight='bold')
    
    ax4.set_xlabel('Velocity (m/s)', fontweight='bold', fontsize=10)
    ax4.set_title('D. Ion Velocities', fontweight='bold', fontsize=11, loc='left')
    ax4.grid(axis='x', alpha=0.3, linestyle='--')
    ax4.set_xlim(0, max(velocities)*1.15)
    
    # Panel E: H+ Field Structure
    ax5 = fig.add_subplot(gs[1, 1])
    h_magnitude = parse_numpy_array(data['ion_quantum_data']['H+']['field_magnitude'])
    h_phase = parse_numpy_array(data['ion_quantum_data']['H+']['field_phase'])
    
    if len(h_magnitude) > 0 and len(h_phase) > 0:
        # Sample for visualization
        sample_size = min(1000, len(h_magnitude))
        indices = np.random.choice(len(h_magnitude), sample_size, replace=False)
        mag_sample = h_magnitude[indices]
        phase_sample = h_phase[indices]
        
        # 2D histogram
        h, xedges, yedges = np.histogram2d(phase_sample, mag_sample, bins=40)
        extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]]
        
        im = ax5.imshow(h.T, origin='lower', aspect='auto', cmap='hot',
                       extent=extent, interpolation='bilinear')
        
        ax5.set_xlabel('Phase (rad)', fontweight='bold', fontsize=10)
        ax5.set_ylabel('Field Magnitude', fontweight='bold', fontsize=10)
        ax5.set_title('E. H+ Field Phase-Magnitude', fontweight='bold', fontsize=11, loc='left')
        
        cbar = plt.colorbar(im, ax=ax5, fraction=0.046, pad=0.04)
        cbar.set_label('Density', fontsize=8, fontweight='bold')
        cbar.ax.tick_params(labelsize=7)
    else:
        ax5.text(0.5, 0.5, 'Data parsing error', ha='center', va='center',
                transform=ax5.transAxes, fontsize=10)
    
    # Panel F: Coherence Time Comparison
    ax6 = fig.add_subplot(gs[1, 2])
    
    # Convert to femtoseconds
    coh_times_fs = np.array(coherence_times) * 1e15
    
    bars = ax6.bar(x_pos, coh_times_fs, color=colors, alpha=0.85,
                   edgecolor='black', linewidth=2, width=0.6)
    
    ax6.set_xticks(x_pos)
    ax6.set_xticklabels(ions, fontsize=10, fontweight='bold')
    ax6.set_ylabel('Coherence Time (fs)', fontweight='bold', fontsize=10)
    ax6.set_title('F. Decoherence Timescales', fontweight='bold', fontsize=11, loc='left')
    ax6.grid(axis='y', alpha=0.3, linestyle='--')
    
    # Add consciousness timescale reference
    ax6.axhline(y=1e8, color='green', linestyle='--', linewidth=2.5, alpha=0.7,
               label='Consciousness (~100 ms)')
    ax6.set_yscale('log')
    ax6.legend(fontsize=8, loc='upper right', framealpha=0.95)
    
    fig.suptitle('Ion Quantum Properties: H+ Substrate vs Classical Dynamics', 
                 fontsize=15, fontweight='bold', y=0.995)
    
    plt.savefig(save_path, bbox_inches='tight', dpi=300)
    plt.close()
    print(f"✓ Saved: {save_path}")

# ============================================================================
# DATASET 2: COHERENCE FIELDS - 6 PANEL FIGURE
# ============================================================================

def figure_2_coherence_fields(save_path='figure_2_coherence_fields.png'):
    """
    6-panel comprehensive analysis of regional coherence fields
    """
    print("Generating Figure 2: Coherence Fields Analysis...")
    
    with open('experiment_2_coherence_fields.json', 'r') as f:
        data = json.load(f)
    
    fig = plt.figure(figsize=(16, 10))
    gs = GridSpec(2, 3, figure=fig, hspace=0.35, wspace=0.35)
    
    regions = ['region_0', 'region_1', 'region_2', 'region_3']
    ions = ['H+', 'Na+', 'K+', 'Ca2+', 'Mg2+']
    ion_colors = ['#E74C3C', '#3498DB', '#2ECC71', '#F39C12', '#9B59B6']
    
    # Panel A: Regional Field Magnitude Maps (Region 0)
    ax1 = fig.add_subplot(gs[0, 0])
    region = 'region_0'
    magnitude = parse_numpy_array(data['region_data'][region]['magnitude'])
    
    if len(magnitude) > 0:
        n = int(np.sqrt(len(magnitude)))
        if len(magnitude) != n**2:
            n = int(np.sqrt(len(magnitude))) + 1
            magnitude = np.pad(magnitude, (0, n**2 - len(magnitude)), mode='constant')
        
        mag_2d = magnitude.reshape(n, n)
        
        im = ax1.imshow(mag_2d, cmap='viridis', aspect='auto', origin='lower',
                       interpolation='bilinear')
        ax1.contour(mag_2d, levels=8, colors='white', alpha=0.4, linewidths=1)
        
        ax1.set_xlabel('x (a.u.)', fontweight='bold', fontsize=10)
        ax1.set_ylabel('y (a.u.)', fontweight='bold', fontsize=10)
        ax1.set_title('A. Regional Field Magnitude (R0)', fontweight='bold', fontsize=11, loc='left')
        
        cbar = plt.colorbar(im, ax=ax1, fraction=0.046, pad=0.04)
        cbar.set_label('|Field|', fontsize=8, fontweight='bold')
        cbar.ax.tick_params(labelsize=7)
    
    # Panel B: Phase Distribution (Region 0)
    ax2 = fig.add_subplot(gs[0, 1])
    phase = parse_numpy_array(data['region_data'][region]['phase'])
    
    if len(phase) > 0:
        n = int(np.sqrt(len(phase)))
        if len(phase) != n**2:
            n = int(np.sqrt(len(phase))) + 1
            phase = np.pad(phase, (0, n**2 - len(phase)), mode='constant')
        
        phase_2d = phase.reshape(n, n)
        
        im = ax2.imshow(phase_2d, cmap='twilight', aspect='auto', origin='lower',
                       interpolation='bilinear', vmin=-np.pi, vmax=np.pi)
        ax2.contour(phase_2d, levels=8, colors='black', alpha=0.3, linewidths=0.8)
        
        ax2.set_xlabel('x (a.u.)', fontweight='bold', fontsize=10)
        ax2.set_ylabel('y (a.u.)', fontweight='bold', fontsize=10)
        ax2.set_title('B. Phase Distribution (R0)', fontweight='bold', fontsize=11, loc='left')
        
        cbar = plt.colorbar(im, ax=ax2, fraction=0.046, pad=0.04)
        cbar.set_label('Phase (rad)', fontsize=8, fontweight='bold')
        cbar.ax.tick_params(labelsize=7)
    
    # Panel C: H+ Contribution Across Regions
    ax3 = fig.add_subplot(gs[0, 2])
    
    h_contributions = []
    for region in regions:
        h_field = parse_numpy_array(data['region_data'][region]['ion_contributions']['H+'])
        if len(h_field) > 0:
            h_contributions.append(np.mean(np.abs(h_field)))
        else:
            h_contributions.append(0)
    
    x_pos = np.arange(len(regions))
    bars = ax3.bar(x_pos, h_contributions, color='#E74C3C', alpha=0.85,
                   edgecolor='black', linewidth=2, width=0.6)
    
    ax3.set_xticks(x_pos)
    ax3.set_xticklabels(['R0', 'R1', 'R2', 'R3'], fontsize=10, fontweight='bold')
    ax3.set_ylabel('Mean |H+ Field|', fontweight='bold', fontsize=10)
    ax3.set_title('C. H+ Substrate Strength', fontweight='bold', fontsize=11, loc='left')
    ax3.grid(axis='y', alpha=0.3, linestyle='--')
    
    # Add value labels
    for bar, val in zip(bars, h_contributions):
        height = bar.get_height()
        if val > 0:
            ax3.text(bar.get_x() + bar.get_width()/2., height,
                    f'{val:.3f}', ha='center', va='bottom', fontsize=8, fontweight='bold')
    
    # Panel D: Ion Contribution Comparison (Region 0)
    ax4 = fig.add_subplot(gs[1, 0])
    
    region = 'region_0'
    ion_magnitudes = []
    for ion in ions:
        ion_field = parse_numpy_array(data['region_data'][region]['ion_contributions'][ion])
        if len(ion_field) > 0:
            ion_magnitudes.append(max(np.mean(np.abs(ion_field)), 1e-10))
        else:
            ion_magnitudes.append(1e-10)
    
    x_pos = np.arange(len(ions))
    bars = ax4.bar(x_pos, ion_magnitudes, color=ion_colors, alpha=0.85,
                   edgecolor='black', linewidth=2, width=0.6)
    
    ax4.set_xticks(x_pos)
    ax4.set_xticklabels(ions, fontsize=10, fontweight='bold')
    ax4.set_ylabel('Mean Field Magnitude', fontweight='bold', fontsize=10)
    ax4.set_title('D. Ion Contributions (R0)', fontweight='bold', fontsize=11, loc='left')
    ax4.set_yscale('log')
    ax4.grid(axis='y', alpha=0.3, linestyle='--')
    
    # Panel E: Regional Coherence Comparison
    ax5 = fig.add_subplot(gs[1, 1])
    
    mean_coherences = [data['region_data'][r]['mean_coherence'] for r in regions]
    
    x_pos = np.arange(len(regions))
    bars = ax5.bar(x_pos, mean_coherences, color='#16A085', alpha=0.85,
                   edgecolor='black', linewidth=2, width=0.6)
    
    ax5.set_xticks(x_pos)
    ax5.set_xticklabels(['R0', 'R1', 'R2', 'R3'], fontsize=10, fontweight='bold')
    ax5.set_ylabel('Mean Coherence', fontweight='bold', fontsize=10)
    ax5.set_title('E. Regional Coherence Levels', fontweight='bold', fontsize=11, loc='left')
    ax5.set_yscale('log')
    ax5.grid(axis='y', alpha=0.3, linestyle='--')
    
    # Add value labels
    for bar, val in zip(bars, mean_coherences):
        height = bar.get_height()
        ax5.text(bar.get_x() + bar.get_width()/2., height,
                f'{val:.2e}', ha='center', va='bottom', fontsize=7, fontweight='bold')
    
    # Panel F: Complex Field Structure (Region 0)
    ax6 = fig.add_subplot(gs[1, 2])
    
    region = 'region_0'
    regional_field = parse_numpy_array(data['region_data'][region]['regional_field'])
    
    if len(regional_field) > 0:
        # Sample for visualization
        sample_size = min(2000, len(regional_field))
        indices = np.random.choice(len(regional_field), sample_size, replace=False)
        field_sample = regional_field[indices]
        
        real_parts = np.real(field_sample)
        imag_parts = np.imag(field_sample)
        
        # 2D histogram
        h, xedges, yedges = np.histogram2d(real_parts, imag_parts, bins=50)
        extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]]
        
        im = ax6.imshow(h.T, origin='lower', aspect='auto', cmap='plasma',
                       extent=extent, interpolation='bilinear')
        
        # Add unit circle
        if len(field_sample) > 0:
            mean_mag = np.mean(np.abs(field_sample))
            circle = Circle((0, 0), mean_mag, 
                           fill=False, edgecolor='white', linewidth=2, linestyle='--', alpha=0.7)
            ax6.add_patch(circle)
        
        ax6.set_xlabel('Re(Field)', fontweight='bold', fontsize=10)
        ax6.set_ylabel('Im(Field)', fontweight='bold', fontsize=10)
        ax6.set_title('F. Complex Field Structure (R0)', fontweight='bold', fontsize=11, loc='left')
        ax6.axhline(y=0, color='white', linestyle='-', linewidth=0.5, alpha=0.5)
        ax6.axvline(x=0, color='white', linestyle='-', linewidth=0.5, alpha=0.5)
        
        cbar = plt.colorbar(im, ax=ax6, fraction=0.046, pad=0.04)
        cbar.set_label('Density', fontsize=8, fontweight='bold')
        cbar.ax.tick_params(labelsize=7)
    
    fig.suptitle('Regional Coherence Fields: H+ Substrate Geometry', 
                 fontsize=15, fontweight='bold', y=0.995)
    
    plt.savefig(save_path, bbox_inches='tight', dpi=300)
    plt.close()
    print(f"✓ Saved: {save_path}")

# ============================================================================
# DATASET 4: DECOHERENCE RESISTANCE - 6 PANEL FIGURE
# ============================================================================

def figure_3_decoherence_resistance(save_path='figure_3_decoherence_resistance.png'):
    """
    6-panel comprehensive analysis of decoherence under various perturbations
    """
    print("Generating Figure 3: Decoherence Resistance Analysis...")
    
    with open('experiment_4_decoherence_resistance.json', 'r') as f:
        data = json.load(f)
    
    fig = plt.figure(figsize=(16, 10))
    gs = GridSpec(2, 3, figure=fig, hspace=0.35, wspace=0.35)
    
    # Extract thermal noise data
    thermal_results = data['decoherence_analysis']['thermal_noise']['results']
    strengths = [r['strength'] for r in thermal_results]
    phase_coh = [r['phase_coherence'] for r in thermal_results]
    mag_stab = [r['magnitude_stability'] for r in thermal_results]
    
    # Panel A: Phase Coherence vs Noise Strength
    ax1 = fig.add_subplot(gs[0, 0])
    
    ax1.plot(strengths, phase_coh, 'o-', color='#E74C3C', linewidth=3,
            markersize=10, markeredgecolor='black', markeredgewidth=1.5,
            label='Phase Coherence')
    
    # Fit exponential decay
    from scipy.optimize import curve_fit
    def exp_decay(x, a, b):
        return a * np.exp(-b * x)
    
    try:
        popt, _ = curve_fit(exp_decay, strengths, phase_coh)
        x_fit = np.linspace(min(strengths), max(strengths), 100)
        y_fit = exp_decay(x_fit, *popt)
        ax1.plot(x_fit, y_fit, '--', color='black', linewidth=2, alpha=0.5,
                label=f'Fit: {popt[0]:.2e}·exp(-{popt[1]:.2f}x)')
    except:
        pass
    
    ax1.set_xlabel('Thermal Noise Strength', fontweight='bold', fontsize=10)
    ax1.set_ylabel('Phase Coherence', fontweight='bold', fontsize=10)
    ax1.set_title('A. Phase Coherence Decay', fontweight='bold', fontsize=11, loc='left')
    ax1.set_yscale('log')
    ax1.legend(fontsize=8, loc='best', framealpha=0.95)
    ax1.grid(True, alpha=0.3, linestyle='--')
    
    # Panel B: Magnitude Stability vs Noise Strength
    ax2 = fig.add_subplot(gs[0, 1])
    
    ax2.plot(strengths, mag_stab, 's-', color='#3498DB', linewidth=3,
            markersize=10, markeredgecolor='black', markeredgewidth=1.5,
            label='Magnitude Stability')
    
    ax2.set_xlabel('Thermal Noise Strength', fontweight='bold', fontsize=10)
    ax2.set_ylabel('Magnitude Stability', fontweight='bold', fontsize=10)
    ax2.set_title('B. Magnitude Stability', fontweight='bold', fontsize=11, loc='left')
    ax2.legend(fontsize=8, loc='best', framealpha=0.95)
    ax2.grid(True, alpha=0.3, linestyle='--')
    ax2.axhline(y=0.5, color='orange', linestyle='--', linewidth=2, alpha=0.7,
               label='Threshold')
    
    # Panel C: Phase-Magnitude Coupling
    ax3 = fig.add_subplot(gs[0, 2])
    
    scatter = ax3.scatter(phase_coh, mag_stab, c=strengths, s=200, 
                         cmap='coolwarm', alpha=0.8, edgecolors='black', linewidth=2)
    
    # Add arrows showing trajectory
    for i in range(len(strengths)-1):
        ax3.annotate('', xy=(phase_coh[i+1], mag_stab[i+1]),
                    xytext=(phase_coh[i], mag_stab[i]),
                    arrowprops=dict(arrowstyle='->', lw=2, color='black', alpha=0.5))
    
    ax3.set_xlabel('Phase Coherence', fontweight='bold', fontsize=10)
    ax3.set_ylabel('Magnitude Stability', fontweight='bold', fontsize=10)
    ax3.set_title('C. Coherence-Stability Coupling', fontweight='bold', fontsize=11, loc='left')
    ax3.set_xscale('log')
    ax3.grid(True, alpha=0.3, linestyle='--')
    
    cbar = plt.colorbar(scatter, ax=ax3, fraction=0.046, pad=0.04)
    cbar.set_label('Noise Strength', fontsize=8, fontweight='bold')
    cbar.ax.tick_params(labelsize=7)
    
    # Panel D: Field Magnitude Distribution Evolution
    ax4 = fig.add_subplot(gs[1, 0])
    
    # Plot distributions for different noise levels
    noise_levels = [0, len(thermal_results)//2, len(thermal_results)-1]
    colors_dist = ['#2ECC71', '#F39C12', '#E74C3C']
    labels_dist = ['Low Noise', 'Medium Noise', 'High Noise']
    
    for idx, color, label in zip(noise_levels, colors_dist, labels_dist):
        magnitude = parse_numpy_array(thermal_results[idx]['field_data']['magnitude'])
        if len(magnitude) > 0:
            ax4.hist(magnitude, bins=50, alpha=0.6, color=color, 
                    edgecolor='black', linewidth=1, label=label, density=True)
    
    ax4.set_xlabel('Field Magnitude', fontweight='bold', fontsize=10)
    ax4.set_ylabel('Probability Density', fontweight='bold', fontsize=10)
    ax4.set_title('D. Magnitude Distribution Evolution', fontweight='bold', fontsize=11, loc='left')
    ax4.legend(fontsize=8, loc='best', framealpha=0.95)
    ax4.grid(axis='y', alpha=0.3, linestyle='--')
    
    # Panel E: Phase Distribution Evolution
    ax5 = fig.add_subplot(gs[1, 1])
    
    for idx, color, label in zip(noise_levels, colors_dist, labels_dist):
        phase = parse_numpy_array(thermal_results[idx]['field_data']['phase'])
        if len(phase) > 0:
            ax5.hist(phase, bins=50, alpha=0.6, color=color,
                    edgecolor='black', linewidth=1, label=label, density=True)
    
    ax5.set_xlabel('Phase (rad)', fontweight='bold', fontsize=10)
    ax5.set_ylabel('Probability Density', fontweight='bold', fontsize=10)
    ax5.set_title('E. Phase Distribution Evolution', fontweight='bold', fontsize=11, loc='left')
    ax5.legend(fontsize=8, loc='best', framealpha=0.95)
    ax5.grid(axis='y', alpha=0.3, linestyle='--')
    ax5.set_xlim(-np.pi, np.pi)
    
    # Panel F: Consciousness Viability Map
    ax6 = fig.add_subplot(gs[1, 2])
    
    # Create 2D map of viability
    x = np.array(phase_coh)
    y = np.array(mag_stab)
    
    # Create grid
    xi = np.logspace(np.log10(min(x)), np.log10(max(x)), 100)
    yi = np.linspace(min(y), max(y), 100)
    Xi, Yi = np.meshgrid(xi, yi)
    
    # Define viability criterion
    viability = (Xi > 0.01) & (Yi > 0.6)
    
    im = ax6.contourf(Xi, Yi, viability.astype(float), levels=[0, 0.5, 1],
                     colors=['#E74C3C', '#2ECC71'], alpha=0.6)
    
    # Plot actual data points
    ax6.scatter(x, y, c='black', s=150, marker='o', 
               edgecolors='white', linewidth=2, zorder=5)
    
    # Add trajectory
    ax6.plot(x, y, 'k--', linewidth=2, alpha=0.5, zorder=4)
    
    ax6.set_xlabel('Phase Coherence', fontweight='bold', fontsize=10)
    ax6.set_ylabel('Magnitude Stability', fontweight='bold', fontsize=10)
    ax6.set_title('F. Consciousness Viability Map', fontweight='bold', fontsize=11, loc='left')
    ax6.set_xscale('log')
    ax6.grid(True, alpha=0.3, linestyle='--', color='white')
    
    # Add legend
    viable_patch = mpatches.Patch(color='#2ECC71', alpha=0.6, label='Viable')
    nonviable_patch = mpatches.Patch(color='#E74C3C', alpha=0.6, label='Non-viable')
    ax6.legend(handles=[viable_patch, nonviable_patch], fontsize=8, 
              loc='best', framealpha=0.95)
    
    fig.suptitle('Decoherence Resistance: H+ Field Stability Under Perturbation', 
                 fontsize=15, fontweight='bold', y=0.995)
    
    plt.savefig(save_path, bbox_inches='tight', dpi=300)
    plt.close()
    print(f"✓ Saved: {save_path}")

# ============================================================================
# DATASET 5: STATE TRANSITIONS - 6 PANEL FIGURE
# ============================================================================

def figure_4_state_transitions(save_path='figure_4_state_transitions.png'):
    """
    6-panel comprehensive analysis of consciousness state transitions
    """
    print("Generating Figure 4: State Transitions Analysis...")
    
    with open('experiment_5_state_transitions.json', 'r') as f:
        data = json.load(f)
    
    fig = plt.figure(figsize=(16, 10))
    gs = GridSpec(2, 3, figure=fig, hspace=0.35, wspace=0.35)
    
    states = ['awake_alert', 'awake_relaxed', 'light_sleep', 'deep_sleep', 'anesthesia']
    state_labels = ['Awake\nAlert', 'Awake\nRelaxed', 'Light\nSleep', 'Deep\nSleep', 'Anesthesia']
    colors = ['#E74C3C', '#F39C12', '#3498DB', '#2ECC71', '#9B59B6']
    
    # Extract state parameters
    coherence_levels = [data['consciousness_states'][s]['coherence_level'] for s in states]
    coupling_strengths = [data['consciousness_states'][s]['coupling_strength'] for s in states]
    noise_levels = [data['consciousness_states'][s]['noise_level'] for s in states]
    freq_ranges = [data['consciousness_states'][s]['frequency_range'] for s in states]
    
    # Panel A: State Parameter Space
    ax1 = fig.add_subplot(gs[0, 0])
    
    x_pos = np.arange(len(states))
    width = 0.25
    
    bars1 = ax1.bar(x_pos - width, coherence_levels, width, label='Coherence',
                   color='#E74C3C', alpha=0.85, edgecolor='black', linewidth=1.5)
    bars2 = ax1.bar(x_pos, coupling_strengths, width, label='Coupling',
                   color='#3498DB', alpha=0.85, edgecolor='black', linewidth=1.5)
    bars3 = ax1.bar(x_pos + width, noise_levels, width, label='Noise',
                   color='#2ECC71', alpha=0.85, edgecolor='black', linewidth=1.5)
    
    ax1.set_xticks(x_pos)
    ax1.set_xticklabels(state_labels, fontsize=9, fontweight='bold')
    ax1.set_ylabel('Parameter Value', fontweight='bold', fontsize=10)
    ax1.set_title('A. State Parameter Profiles', fontweight='bold', fontsize=11, loc='left')
    ax1.legend(fontsize=8, loc='best', framealpha=0.95)
    ax1.grid(axis='y', alpha=0.3, linestyle='--')
    ax1.set_ylim(0, 1.1)
    
    # Panel B: Frequency Range Distribution
    ax2 = fig.add_subplot(gs[0, 1])
    
    for i, (state, freq, color, label) in enumerate(zip(states, freq_ranges, colors, state_labels)):
        y_pos = len(states) - i - 1
        ax2.barh(y_pos, freq[1] - freq[0], left=freq[0], height=0.6,
                color=color, alpha=0.85, edgecolor='black', linewidth=2,
                label=label.replace('\n', ' '))
        
        # Add frequency labels
        ax2.text(freq[0], y_pos, f'{freq[0]}', ha='right', va='center',
                fontsize=7, fontweight='bold')
        ax2.text(freq[1], y_pos, f'{freq[1]}', ha='left', va='center',
                fontsize=7, fontweight='bold')
    
    ax2.set_yticks(range(len(states)))
    ax2.set_yticklabels([label.replace('\n', ' ') for label in state_labels[::-1]], 
                        fontsize=9, fontweight='bold')
    ax2.set_xlabel('Frequency (Hz)', fontweight='bold', fontsize=10)
    ax2.set_title('B. Frequency Band Ranges', fontweight='bold', fontsize=11, loc='left')
    ax2.set_xscale('log')
    ax2.grid(axis='x', alpha=0.3, linestyle='--')
    
    # Panel C: Coherence-Coupling Phase Space
    ax3 = fig.add_subplot(gs[0, 2])
    
    for i, (coh, coup, color, label) in enumerate(zip(coherence_levels, coupling_strengths, 
                                                       colors, state_labels)):
        ax3.scatter(coh, coup, s=400, color=color, alpha=0.85,
                   edgecolors='black', linewidth=2.5, label=label.replace('\n', ' '),
                   zorder=5)
        ax3.text(coh, coup, str(i+1), ha='center', va='center',
                fontsize=10, fontweight='bold', color='white')
    
    # Add trajectory
    ax3.plot(coherence_levels, coupling_strengths, 'k--', linewidth=2, 
            alpha=0.5, zorder=3)
    
    # Add arrows
    for i in range(len(coherence_levels)-1):
        ax3.annotate('', xy=(coherence_levels[i+1], coupling_strengths[i+1]),
                    xytext=(coherence_levels[i], coupling_strengths[i]),
                    arrowprops=dict(arrowstyle='->', lw=2.5, color='black', alpha=0.6))
    
    ax3.set_xlabel('Coherence Level', fontweight='bold', fontsize=10)
    ax3.set_ylabel('Coupling Strength', fontweight='bold', fontsize=10)
    ax3.set_title('C. State Phase Space', fontweight='bold', fontsize=11, loc='left')
    ax3.legend(fontsize=7, loc='best', framealpha=0.95, ncol=1)
    ax3.grid(True, alpha=0.3, linestyle='--')
    ax3.set_xlim(-0.05, 0.9)
    ax3.set_ylim(-0.05, 1.1)
    
    # Panel D: Coherence Trace Over Time
    ax4 = fig.add_subplot(gs[1, 0])
    
    coherence_trace = np.array(data['coherence_trace'])
    time = np.arange(len(coherence_trace))
    
    # Color segments by state
    n_samples = len(coherence_trace)
    segment_size = n_samples // len(states)
    
    for i, (state, color, label) in enumerate(zip(states, colors, state_labels)):
        start = i * segment_size
        end = (i + 1) * segment_size if i < len(states) - 1 else n_samples
        ax4.plot(time[start:end], coherence_trace[start:end],
                color=color, linewidth=2.5, label=label.replace('\n', ' '))
    
    ax4.set_xlabel('Time (a.u.)', fontweight='bold', fontsize=10)
    ax4.set_ylabel('Coherence Level', fontweight='bold', fontsize=10)
    ax4.set_title('D. Temporal Coherence Evolution', fontweight='bold', fontsize=11, loc='left')
    ax4.legend(fontsize=7, loc='best', framealpha=0.95, ncol=2)
    ax4.grid(True, alpha=0.3, linestyle='--')
    ax4.set_ylim(0, 1)
    
    # Panel E: Quantum Field Magnitude
    ax5 = fig.add_subplot(gs[1, 1])
    
    quantum_field = parse_numpy_array(data['quantum_field_trace'])
    
    if len(quantum_field) > 0:
        field_magnitude = np.abs(quantum_field)
        
        # Sample for visualization
        sample_size = min(5000, len(field_magnitude))
        indices = np.linspace(0, len(field_magnitude)-1, sample_size, dtype=int)
        time_sample = indices
        mag_sample = field_magnitude[indices]
        
        ax5.plot(time_sample, mag_sample, color='#16A085', linewidth=1, alpha=0.7)
        
        # Add moving average
        window = 100
        if len(mag_sample) > window:
            moving_avg = np.convolve(mag_sample, np.ones(window)/window, mode='valid')
            ax5.plot(time_sample[window-1:], moving_avg, color='#E74C3C', 
                    linewidth=2.5, label='Moving Average')
        
        ax5.set_xlabel('Time (a.u.)', fontweight='bold', fontsize=10)
        ax5.set_ylabel('|Quantum Field|', fontweight='bold', fontsize=10)
        ax5.set_title('E. Quantum Field Dynamics', fontweight='bold', fontsize=11, loc='left')
        ax5.legend(fontsize=8, loc='best', framealpha=0.95)
        ax5.grid(True, alpha=0.3, linestyle='--')
    
    # Panel F: State Transition Matrix
    ax6 = fig.add_subplot(gs[1, 2])
    
    # Create synthetic transition matrix based on state parameters
    n_states = len(states)
    transition_matrix = np.zeros((n_states, n_states))
    
    for i in range(n_states):
        for j in range(n_states):
            # Transition probability based on parameter similarity
            coh_diff = abs(coherence_levels[i] - coherence_levels[j])
            coup_diff = abs(coupling_strengths[i] - coupling_strengths[j])
            transition_matrix[i, j] = np.exp(-(coh_diff + coup_diff))
    
    # Normalize rows
    transition_matrix = transition_matrix / transition_matrix.sum(axis=1, keepdims=True)
    
    im = ax6.imshow(transition_matrix, cmap='YlOrRd', aspect='auto',
                   interpolation='nearest', vmin=0, vmax=1)
    
    ax6.set_xticks(range(n_states))
    ax6.set_yticks(range(n_states))
    ax6.set_xticklabels([label.replace('\n', ' ') for label in state_labels], 
                        fontsize=8, rotation=45, ha='right')
    ax6.set_yticklabels([label.replace('\n', ' ') for label in state_labels], 
                        fontsize=8)
    ax6.set_xlabel('To State', fontweight='bold', fontsize=10)
    ax6.set_ylabel('From State', fontweight='bold', fontsize=10)
    ax6.set_title('F. Transition Probability Matrix', fontweight='bold', fontsize=11, loc='left')
    
    # Add values
    for i in range(n_states):
        for j in range(n_states):
            text = ax6.text(j, i, f'{transition_matrix[i, j]:.2f}',
                          ha='center', va='center', color='black' if transition_matrix[i, j] < 0.5 else 'white',
                          fontsize=7, fontweight='bold')
    
    cbar = plt.colorbar(im, ax=ax6, fraction=0.046, pad=0.04)
    cbar.set_label('Probability', fontsize=8, fontweight='bold')
    cbar.ax.tick_params(labelsize=7)
    
    fig.suptitle('Consciousness State Transitions: Field Dynamics Across States', 
                 fontsize=15, fontweight='bold', y=0.995)
    
    plt.savefig(save_path, bbox_inches='tight', dpi=300)
    plt.close()
    print(f"✓ Saved: {save_path}")

# ============================================================================
# MAIN EXECUTION
# ============================================================================

def generate_all_comprehensive_figures():
    """Generate all 4 comprehensive multi-panel figures"""
    print("\n" + "="*70)
    print("GENERATING COMPREHENSIVE PUBLICATION-QUALITY FIGURES")
    print("="*70 + "\n")
    
    figure_1_ion_tunneling()
    figure_2_coherence_fields()
    figure_3_decoherence_resistance()
    figure_4_state_transitions()
    
    print("\n" + "="*70)
    print("ALL FIGURES GENERATED SUCCESSFULLY!")
    print("="*70)
    print("\nGenerated Files:")
    print("  1. figure_1_ion_tunneling.png          (6 panels)")
    print("  2. figure_2_coherence_fields.png       (6 panels)")
    print("  3. figure_3_decoherence_resistance.png (6 panels)")
    print("  4. figure_4_state_transitions.png      (6 panels)")
    print("\nTotal: 24 high-quality analysis panels")
    print("="*70 + "\n")

# Run
if __name__ == "__main__":
    generate_all_comprehensive_figures()
