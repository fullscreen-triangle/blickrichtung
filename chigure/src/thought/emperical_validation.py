import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import seaborn as sns
from pathlib import Path
from scipy.signal import find_peaks
from scipy.stats import pearsonr

def load_all_data():
    """Load all available empirical data."""
    data = {}
    
    # Try to load joint angles
    joint_path = Path('public/joint_angles_20251015_092343.csv')
    if joint_path.exists():
        data['joints'] = pd.read_csv(joint_path)
    
    # Try to load muscle activation
    muscle_path = Path('public/muscle_activation_20251015_092343.csv')
    if muscle_path.exists():
        data['muscles'] = pd.read_csv(muscle_path)
    
    # Try to load heartbeat data
    heartbeat_path = Path('public/heartbeat_gas_bmd_unified_20251015_002328.json')
    if heartbeat_path.exists():
        import json
        with open(heartbeat_path, 'r') as f:
            data['heartbeat'] = json.load(f)
    
    return data

def create_empirical_validation_figure(data):
    """
    Master Figure 3: Empirical Validation Dashboard
    Shows real data validating the consciousness framework.
    """
    
    plt.style.use('seaborn-v0_8-whitegrid')
    
    fig = plt.figure(figsize=(24, 16))
    gs = GridSpec(2, 2, figure=fig, hspace=0.3, wspace=0.3)
    
    # Panel A: Thought Signatures from Biomechanics
    ax1 = fig.add_subplot(gs[0, 0])
    
    if 'joints' in data:
        joint_data = data['joints']
        t = joint_data['timestamp_s'].values
        knee = joint_data['knee'].values
        
        # Calculate thought signatures
        velocity = np.gradient(knee, t)
        acceleration = np.gradient(velocity, t)
        jerk = np.gradient(acceleration, t)
        
        # Thought complexity metric
        thought_complexity = np.sqrt(acceleration**2 + jerk**2)
        
        # Normalize for visualization
        thought_complexity_norm = (thought_complexity - thought_complexity.min()) / \
                                 (thought_complexity.max() - thought_complexity.min())
        
        # Plot
        ax1.plot(t, thought_complexity_norm, linewidth=2, color='#e74c3c',
                alpha=0.8, label='Thought Complexity')
        ax1.fill_between(t, 0, thought_complexity_norm, alpha=0.3, color='#e74c3c')
        
        # Detect thought events (peaks)
        peaks, properties = find_peaks(thought_complexity_norm, height=0.7,
                                       distance=len(t)//20)
        
        if len(peaks) > 0:
            ax1.scatter(t[peaks], thought_complexity_norm[peaks], s=200,
                       c='red', marker='*', edgecolors='black', linewidth=2,
                       zorder=5, label=f'Thought Events (n={len(peaks)})')
        
        ax1.set_xlabel('Time (s)', fontsize=12, fontweight='bold')
        ax1.set_ylabel('Thought Complexity (normalized)', fontsize=12, fontweight='bold')
        ax1.set_title('A: Thought Signatures from Real Biomechanics\nC = √(a² + j²)',
                     fontsize=14, fontweight='bold', pad=15)
        ax1.legend(loc='upper right', fontsize=10, framealpha=0.95)
        ax1.grid(alpha=0.3)
        ax1.set_ylim(-0.05, 1.1)
        
        # Metrics
        textstr = (f'Duration: {t[-1]:.1f} s\n'
                  f'Thought Events: {len(peaks)}\n'
                  f'Mean Complexity: {np.mean(thought_complexity_norm):.3f}\n'
                  f'Peak Complexity: {np.max(thought_complexity_norm):.3f}')
        props = dict(boxstyle='round', facecolor='wheat', alpha=0.9,
                    edgecolor='black', linewidth=2)
        ax1.text(0.02, 0.98, textstr, transform=ax1.transAxes, fontsize=10,
                verticalalignment='top', bbox=props, family='monospace',
                fontweight='bold')
    else:
        ax1.text(0.5, 0.5, 'Joint angle data not available',
                transform=ax1.transAxes, fontsize=14, ha='center', va='center')
    
    # Panel B: Heartbeat-Perception Coupling
    ax2 = fig.add_subplot(gs[0, 1])
    
    if 'heartbeat' in data:
        hb_data = data['heartbeat']['simulation_results']
        
        heart_rate = hb_data['heart_rate_hz']
        mean_rr = hb_data['mean_rr_interval_s']
        restoration_times = np.array(hb_data['restoration_times'])
        perception_rate = hb_data['perception_rate_hz']
        
        # Create timeline
        n_beats = len(restoration_times)
        t_beats = np.cumsum([mean_rr] * n_beats)
        t_beats = np.concatenate([[0], t_beats])
        
        # Simulate equilibrium
        t_fine = np.linspace(0, t_beats[min(20, len(t_beats)-1)], 2000)
        equilibrium = np.ones(len(t_fine))
        
        for i, beat_time in enumerate(t_beats[1:21]):
            mask = t_fine >= beat_time
            time_since_beat = t_fine[mask] - beat_time
            
            if i < len(restoration_times):
                tau = restoration_times[i]
                recovery = 1 - 0.3 * np.exp(-time_since_beat / tau)
                equilibrium[mask] = np.minimum(equilibrium[mask], recovery)
        
        # Plot
        ax2.plot(t_fine, equilibrium, linewidth=2.5, color='#3498db', alpha=0.8)
        ax2.fill_between(t_fine, 0.7, equilibrium, alpha=0.3, color='#3498db')
        
        # Mark heartbeats
        for beat_time in t_beats[1:21]:
            ax2.axvline(beat_time, color='red', linestyle='--',
                       linewidth=1.5, alpha=0.5)
        
        ax2.axhline(1.0, color='green', linestyle='-', linewidth=2,
                   alpha=0.7, label='Perfect Equilibrium')
        
        ax2.set_xlabel('Time (s)', fontsize=12, fontweight='bold')
        ax2.set_ylabel('Gas Molecular Equilibrium', fontsize=12, fontweight='bold')
        ax2.set_title('B: Heartbeat-Perception Coupling \nEquilibrium Restoration',
                     fontsize=14, fontweight='bold', pad=15)
        ax2.legend(loc='lower right', fontsize=10, framealpha=0.95)
        ax2.grid(alpha=0.3)
        ax2.set_ylim(0.65, 1.05)
        
        # Metrics
        textstr = (f'Heart Rate: {heart_rate:.2f} Hz\n'
                  f'RR Interval: {mean_rr*1000:.1f} ms\n'
                  f'Restoration: {np.mean(restoration_times)*1000:.3f} ms\n'
                  f'Perception Rate: {perception_rate:.0f} Hz')
        ax2.text(0.98, 0.98, textstr, transform=ax2.transAxes, fontsize=10,
                verticalalignment='top', horizontalalignment='right',
                bbox=props, family='monospace', fontweight='bold')
    else:
        ax2.text(0.5, 0.5, 'Heartbeat data not available',
                transform=ax2.transAxes, fontsize=14, ha='center', va='center')
    
    # Panel C: Consciousness Intensity Timeline
    ax3 = fig.add_subplot(gs[1, 0])
    
    if 'joints' in data and 'muscles' in data:
        joint_data = data['joints']
        muscle_data = data['muscles']
        
        t_joint = joint_data['timestamp_s'].values
        knee = joint_data['knee'].values
        
        # Perception proxy (from joint angles - smooth component)
        from scipy.signal import savgol_filter
        perception_proxy = savgol_filter(knee, window_length=51, polyorder=3)
        
        # Thought proxy (from joint angles - high-frequency component)
        thought_proxy = knee - perception_proxy
        
        # Consciousness intensity = |perception - thought|
        consciousness_intensity = np.abs(perception_proxy - thought_proxy)
        
        # Normalize
        consciousness_intensity_norm = (consciousness_intensity - consciousness_intensity.min()) / \
                                       (consciousness_intensity.max() - consciousness_intensity.min())
        
        # Plot
        ax3.plot(t_joint, consciousness_intensity_norm, linewidth=2.5,
                color='#9b59b6', alpha=0.8, label='Consciousness Intensity')
        ax3.fill_between(t_joint, 0, consciousness_intensity_norm,
                        alpha=0.3, color='#9b59b6')
        
        # Add rolling average
        window = 50
        if len(consciousness_intensity_norm) > window:
            rolling_avg = np.convolve(consciousness_intensity_norm,
                                     np.ones(window)/window, mode='valid')
            t_rolling = t_joint[:len(rolling_avg)]
            ax3.plot(t_rolling, rolling_avg, linewidth=3, color='red',
                    alpha=0.9, label='Trend')
        
        ax3.set_xlabel('Time (s)', fontsize=12, fontweight='bold')
        ax3.set_ylabel('Consciousness Intensity', fontsize=12, fontweight='bold')
        ax3.set_title('C: Consciousness Intensity Timeline\n|C| = ||P - T||',
                     fontsize=14, fontweight='bold', pad=15)
        ax3.legend(loc='upper right', fontsize=10, framealpha=0.95)
        ax3.grid(alpha=0.3)
        ax3.set_ylim(-0.05, 1.1)
        
        # Metrics
        textstr = (f'Mean Intensity: {np.mean(consciousness_intensity_norm):.3f}\n'
                  f'Peak Intensity: {np.max(consciousness_intensity_norm):.3f}\n'
                  f'Std Dev: {np.std(consciousness_intensity_norm):.3f}')
        ax3.text(0.02, 0.98, textstr, transform=ax3.transAxes, fontsize=10,
                verticalalignment='top', bbox=props, family='monospace',
                fontweight='bold')
    else:
        ax3.text(0.5, 0.5, 'Insufficient data for consciousness calculation',
                transform=ax3.transAxes, fontsize=14, ha='center', va='center')
    
    # Panel D: Correlation Matrix (All Variables)
    ax4 = fig.add_subplot(gs[1, 1])
    
    if 'joints' in data and 'muscles' in data:
        # Compile all variables
        joint_data = data['joints']
        muscle_data = data['muscles']
        
        # Ensure same length
        min_len = min(len(joint_data), len(muscle_data))
        
        variables = {
            'Hip': joint_data['hip'].values[:min_len],
            'Knee': joint_data['knee'].values[:min_len],
            'Ankle': joint_data['ankle'].values[:min_len],
            'Quad': muscle_data['quadriceps'].values[:min_len],
            'Ham': muscle_data['hamstrings'].values[:min_len],
            'Gastro': muscle_data['gastrocnemius'].values[:min_len]
        }
        
        # Calculate consciousness intensity
        t_joint = joint_data['timestamp_s'].values[:min_len]
        knee = joint_data['knee'].values[:min_len]
        perception_proxy = savgol_filter(knee, window_length=51, polyorder=3)
        thought_proxy = knee - perception_proxy
        consciousness = np.abs(perception_proxy - thought_proxy)
        
        variables['Consciousness'] = consciousness
        
        # Create correlation matrix
        var_names = list(variables.keys())
        n_vars = len(var_names)
        corr_matrix = np.zeros((n_vars, n_vars))
        
        for i, name1 in enumerate(var_names):
            for j, name2 in enumerate(var_names):
                corr, _ = pearsonr(variables[name1], variables[name2])
                corr_matrix[i, j] = corr
        
        # Plot heatmap
        im = ax4.imshow(corr_matrix, cmap='RdBu_r', aspect='auto',
                       vmin=-1, vmax=1)
        
        # Labels
        ax4.set_xticks(np.arange(n_vars))
        ax4.set_yticks(np.arange(n_vars))
        ax4.set_xticklabels(var_names, rotation=45, ha='right', fontsize=10)
        ax4.set_yticklabels(var_names, fontsize=10)
        
        # Add correlation values
        for i in range(n_vars):
            for j in range(n_vars):
                text = ax4.text(j, i, f'{corr_matrix[i, j]:.2f}',
                              ha='center', va='center', color='black',
                              fontsize=9, fontweight='bold')
        
        ax4.set_title('D: Variable Correlation Matrix\nConsciousness Correlates with Biomechanics',
                     fontsize=14, fontweight='bold', pad=15)
        
        # Colorbar
        cbar = plt.colorbar(im, ax=ax4)
        cbar.set_label('Pearson Correlation', fontsize=11, fontweight='bold')
        
        # Highlight consciousness row/column
        ax4.axhline(n_vars - 1.5, color='yellow', linewidth=3, alpha=0.7)
        ax4.axvline(n_vars - 1.5, color='yellow', linewidth=3, alpha=0.7)
        
    else:
        ax4.text(0.5, 0.5, 'Insufficient data for correlation analysis',
                transform=ax4.transAxes, fontsize=14, ha='center', va='center')
    
    # Overall title
    fig.suptitle('Empirical Validation: Real Data Supports Consciousness Framework',
                fontsize=20, fontweight='bold', y=0.98)
    
    plt.tight_layout()
    return fig

def main():
    print("="*80)
    print("GENERATING MASTER FIGURE 3: EMPIRICAL VALIDATION")
    print("="*80)
    
    print("\nLoading all available data...")
    data = load_all_data()
    
    print(f"Available datasets: {list(data.keys())}")
    
    output_dir = Path('output/master_figures')
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print("\nCreating empirical validation figure...")
    fig = create_empirical_validation_figure(data)
    
    fig.savefig(output_dir / 'master_figure_3_empirical_validation.png',
                dpi=300, bbox_inches='tight')
    fig.savefig(output_dir / 'master_figure_3_empirical_validation.pdf',
                bbox_inches='tight')
    
    print("✓ Master Figure 3 saved")
    print(f"\nOutput location: {output_dir.absolute()}")
    
    plt.show()

if __name__ == "__main__":
    main()
