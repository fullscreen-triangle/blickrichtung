import json
import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import seaborn as sns
from scipy.signal import welch, find_peaks, hilbert, spectrogram
from scipy.fft import fft, fftfreq
from scipy.signal import correlate
from pathlib import Path

def load_joint_data(filepath):
    """Load joint angles CSV data."""
    return pd.read_csv(filepath)

def calculate_angular_velocity(angles, dt):
    """Calculate angular velocity."""
    return np.gradient(angles, dt)

def create_joint_frequency_panel(joint_data):
    """
    Create 4-panel figure showing frequency domain analysis.
    Demonstrates spectral precision and oscillatory structure.
    """
    
    plt.style.use('seaborn-v0_8-darkgrid')
    
    fig = plt.figure(figsize=(20, 14))
    gs = GridSpec(2, 2, figure=fig, hspace=0.3, wspace=0.3)
    
    t = joint_data['timestamp_s'].values
    dt = np.mean(np.diff(t))
    fs = 1 / dt
    
    hip = joint_data['hip'].values
    knee = joint_data['knee'].values
    ankle = joint_data['ankle'].values
    shoulder = joint_data['shoulder'].values
    elbow = joint_data['elbow'].values
    
    # Panel A: Power Spectral Density (All Joints)
    ax1 = fig.add_subplot(gs[0, 0])
    
    joints_psd = {
        'Hip': (hip, '#e74c3c'),
        'Knee': (knee, '#3498db'),
        'Ankle': (ankle, '#2ecc71'),
        'Shoulder': (shoulder, '#f39c12'),
        'Elbow': (elbow, '#9b59b6')
    }
    
    for joint_name, (angles, color) in joints_psd.items():
        freqs, psd = welch(angles, fs=fs, nperseg=min(512, len(angles)//4))
        ax1.semilogy(freqs, psd, linewidth=2.5, alpha=0.8, 
                    label=joint_name, color=color)
    
    ax1.set_xlabel('Frequency (Hz)', fontsize=14, fontweight='bold')
    ax1.set_ylabel('Power Spectral Density', fontsize=14, fontweight='bold')
    ax1.set_title('A', fontsize=18, fontweight='bold', loc='left', pad=15)
    ax1.legend(loc='upper right', fontsize=11, framealpha=0.95, ncol=2)
    ax1.grid(alpha=0.3, which='both', linewidth=0.5)
    ax1.set_xlim(0, 10)
    
    # Add frequency resolution
    freq_resolution = fs / len(angles)
    textstr = (f'Frequency Resolution:\n'
              f'{freq_resolution:.5f} Hz\n\n'
              f'Nyquist Frequency:\n'
              f'{fs/2:.2f} Hz')
    props = dict(boxstyle='round', facecolor='wheat', alpha=0.9, 
                edgecolor='black', linewidth=2)
    ax1.text(0.98, 0.98, textstr, transform=ax1.transAxes, fontsize=11,
            verticalalignment='top', horizontalalignment='right',
            bbox=props, family='monospace', fontweight='bold')
    
    # Panel B: Spectrogram (Time-Frequency Evolution - Knee)
    ax2 = fig.add_subplot(gs[0, 1])
    
    f, t_spec, Sxx = spectrogram(knee, fs=fs, nperseg=128, noverlap=120)
    
    im = ax2.pcolormesh(t_spec, f, 10 * np.log10(Sxx + 1e-10),
                        shading='gouraud', cmap='viridis')
    ax2.set_ylim(0, 5)
    
    ax2.set_xlabel('Time (s)', fontsize=14, fontweight='bold')
    ax2.set_ylabel('Frequency (Hz)', fontsize=14, fontweight='bold')
    ax2.set_title('B', fontsize=18, fontweight='bold', loc='left', pad=15)
    
    cbar = plt.colorbar(im, ax=ax2)
    cbar.set_label('Power (dB)', fontsize=12, fontweight='bold')
    
    # Add note
    textstr = 'Knee joint\ntime-frequency\nevolution'
    ax2.text(0.02, 0.98, textstr, transform=ax2.transAxes, fontsize=11,
            verticalalignment='top', bbox=props, fontweight='bold')
    
    # Panel C: Instantaneous Frequency (Hilbert Transform)
    ax3 = fig.add_subplot(gs[1, 0])
    
    # Calculate instantaneous frequency for knee and ankle
    knee_centered = knee - np.mean(knee)
    ankle_centered = ankle - np.mean(ankle)
    
    knee_analytic = hilbert(knee_centered)
    ankle_analytic = hilbert(ankle_centered)
    
    knee_phase = np.unwrap(np.angle(knee_analytic))
    ankle_phase = np.unwrap(np.angle(ankle_analytic))
    
    knee_inst_freq = np.diff(knee_phase) / (2.0 * np.pi * dt)
    ankle_inst_freq = np.diff(ankle_phase) / (2.0 * np.pi * dt)
    
    # Plot
    ax3.plot(t[1:], knee_inst_freq, linewidth=1, alpha=0.5, color='#3498db')
    ax3.plot(t[1:], ankle_inst_freq, linewidth=1, alpha=0.5, color='#2ecc71')
    
    # Add rolling averages
    window = 100
    if len(knee_inst_freq) > window:
        knee_rolling = np.convolve(knee_inst_freq, np.ones(window)/window, mode='valid')
        ankle_rolling = np.convolve(ankle_inst_freq, np.ones(window)/window, mode='valid')
        t_rolling = t[1:len(knee_rolling)+1]
        
        ax3.plot(t_rolling, knee_rolling, linewidth=3, alpha=0.9,
                color='#3498db', label='Knee')
        ax3.plot(t_rolling, ankle_rolling, linewidth=3, alpha=0.9,
                color='#2ecc71', label='Ankle')
    
    ax3.set_xlabel('Time (s)', fontsize=14, fontweight='bold')
    ax3.set_ylabel('Instantaneous Frequency (Hz)', fontsize=14, fontweight='bold')
    ax3.set_title('C', fontsize=18, fontweight='bold', loc='left', pad=15)
    ax3.legend(loc='upper right', fontsize=11, framealpha=0.95)
    ax3.grid(alpha=0.3, linewidth=0.5)
    ax3.set_ylim(0, 5)
    
    # Add note
    textstr = 'Hilbert transform\nreveals temporal\nfrequency modulation'
    ax3.text(0.02, 0.98, textstr, transform=ax3.transAxes, fontsize=11,
            verticalalignment='top', bbox=dict(boxstyle='round',
            facecolor='lightblue', alpha=0.9, edgecolor='black', linewidth=2),
            fontweight='bold')
    
    # Panel D: Cross-Spectral Coherence (Knee-Ankle)
    ax4 = fig.add_subplot(gs[1, 1])
    
    # Calculate cross-correlation in frequency domain
    from scipy.signal import coherence
    
    f_coh, coh = coherence(knee, ankle, fs=fs, nperseg=min(256, len(knee)//4))
    
    ax4.plot(f_coh, coh, linewidth=3, alpha=0.8, color='#9b59b6')
    ax4.fill_between(f_coh, 0, coh, alpha=0.3, color='#9b59b6')
    
    # Add significance threshold
    ax4.axhline(0.5, color='red', linestyle='--', linewidth=2, 
               label='Threshold (0.5)', alpha=0.7)
    
    ax4.set_xlabel('Frequency (Hz)', fontsize=14, fontweight='bold')
    ax4.set_ylabel('Coherence', fontsize=14, fontweight='bold')
    ax4.set_title('D', fontsize=18, fontweight='bold', loc='left', pad=15)
    ax4.legend(loc='upper right', fontsize=11, framealpha=0.95)
    ax4.grid(alpha=0.3, linewidth=0.5)
    ax4.set_xlim(0, 5)
    ax4.set_ylim(0, 1.05)
    
    # Find peak coherence
    peak_idx = np.argmax(coh[f_coh < 5])
    peak_freq = f_coh[peak_idx]
    peak_coh = coh[peak_idx]
    
    ax4.plot(peak_freq, peak_coh, 'ro', markersize=12,
            markeredgecolor='black', markeredgewidth=2)
    ax4.annotate(f'{peak_freq:.2f} Hz\nCoherence: {peak_coh:.3f}',
                xy=(peak_freq, peak_coh),
                xytext=(peak_freq + 0.5, peak_coh - 0.15),
                fontsize=11, fontweight='bold',
                arrowprops=dict(arrowstyle='->', color='red', lw=2),
                bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.8))
    
    plt.tight_layout()
    return fig

def main():
    """Main function."""
    
    data_path = Path('public/joint_angles_20251015_092343.csv')
    joint_data = load_joint_data(data_path)
    
    output_dir = Path('output')
    output_dir.mkdir(exist_ok=True)
    
    print("="*70)
    print("GENERATING JOINT ANGLES FREQUENCY ANALYSIS")
    print("="*70)
    
    print("\nGenerating Frequency Domain Panel...")
    fig = create_joint_frequency_panel(joint_data)
    fig.savefig(output_dir / 'figure_joint_angles_3_frequency.png',
                dpi=300, bbox_inches='tight')
    fig.savefig(output_dir / 'figure_joint_angles_3_frequency.pdf',
                bbox_inches='tight')
    print("✓ Frequency panel saved")
    
    print("\n" + "="*70)
    print("FREQUENCY ANALYSIS COMPLETE")
    print("="*70)
    print(f"\nOutput: {output_dir.absolute()}")
    
    plt.show()

if __name__ == "__main__":
    main()
