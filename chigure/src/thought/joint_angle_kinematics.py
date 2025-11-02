import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import seaborn as sns
from pathlib import Path
from scipy.signal import find_peaks
from scipy.interpolate import interp1d

def load_joint_data(filepath):
    """Load joint angle CSV data."""
    return pd.read_csv(filepath)

def create_joint_kinematics_panel(joint_data):
    """
    Create 4-panel figure showing joint angle kinematics during running.
    """
    
    plt.style.use('seaborn-v0_8-whitegrid')
    
    fig = plt.figure(figsize=(22, 14))
    gs = GridSpec(2, 2, figure=fig, hspace=0.35, wspace=0.35)
    
    # Extract data
    t = joint_data['timestamp_s'].values
    hip = joint_data['hip'].values
    knee = joint_data['knee'].values
    ankle = joint_data['ankle'].values
    shoulder = joint_data['shoulder'].values
    elbow = joint_data['elbow'].values
    
    # Panel A: Joint Angles Timeline (Lower Body)
    ax1 = fig.add_subplot(gs[0, 0])
    
    ax1.plot(t, hip, linewidth=2.5, color='#e74c3c', alpha=0.8, label='Hip')
    ax1.plot(t, knee, linewidth=2.5, color='#3498db', alpha=0.8, label='Knee')
    ax1.plot(t, ankle, linewidth=2.5, color='#2ecc71', alpha=0.8, label='Ankle')
    
    ax1.set_xlabel('Time (s)', fontsize=14, fontweight='bold')
    ax1.set_ylabel('Joint Angle (degrees)', fontsize=14, fontweight='bold')
    ax1.set_title('A', fontsize=18, fontweight='bold', loc='left', pad=15)
    ax1.legend(loc='upper right', fontsize=12, framealpha=0.95)
    ax1.grid(alpha=0.3)
    
    # Add metrics
    textstr = (f'Hip Range: {hip.max() - hip.min():.1f}°\n'
              f'Knee Range: {knee.max() - knee.min():.1f}°\n'
              f'Ankle Range: {ankle.max() - ankle.min():.1f}°\n'
              f'Duration: {t[-1]:.1f} s')
    props = dict(boxstyle='round', facecolor='wheat', alpha=0.9,
                edgecolor='black', linewidth=2)
    ax1.text(0.02, 0.98, textstr, transform=ax1.transAxes, fontsize=11,
            verticalalignment='top', bbox=props, family='monospace',
            fontweight='bold')
    
    # Panel B: Joint Angles Timeline (Upper Body)
    ax2 = fig.add_subplot(gs[0, 1])
    
    ax2.plot(t, shoulder, linewidth=2.5, color='#9b59b6', alpha=0.8, label='Shoulder')
    ax2.plot(t, elbow, linewidth=2.5, color='#f39c12', alpha=0.8, label='Elbow')
    
    ax2.set_xlabel('Time (s)', fontsize=14, fontweight='bold')
    ax2.set_ylabel('Joint Angle (degrees)', fontsize=14, fontweight='bold')
    ax2.set_title('B', fontsize=18, fontweight='bold', loc='left', pad=15)
    ax2.legend(loc='upper right', fontsize=12, framealpha=0.95)
    ax2.grid(alpha=0.3)
    
    # Add metrics
    textstr = (f'Shoulder Range: {shoulder.max() - shoulder.min():.1f}°\n'
              f'Elbow Range: {elbow.max() - elbow.min():.1f}°\n'
              f'Arm Swing Amplitude')
    ax2.text(0.98, 0.98, textstr, transform=ax2.transAxes, fontsize=11,
            verticalalignment='top', horizontalalignment='right',
            bbox=props, family='monospace', fontweight='bold')
    
    # Panel C: Joint Angular Velocity
    ax3 = fig.add_subplot(gs[1, 0])
    
    # Calculate angular velocities (degrees/second)
    dt = np.diff(t)
    hip_vel = np.gradient(hip, t)
    knee_vel = np.gradient(knee, t)
    ankle_vel = np.gradient(ankle, t)
    
    ax3.plot(t, hip_vel, linewidth=2, color='#e74c3c', alpha=0.7, label='Hip')
    ax3.plot(t, knee_vel, linewidth=2, color='#3498db', alpha=0.7, label='Knee')
    ax3.plot(t, ankle_vel, linewidth=2, color='#2ecc71', alpha=0.7, label='Ankle')
    
    # Add zero line
    ax3.axhline(0, color='black', linestyle='--', linewidth=1.5, alpha=0.5)
    
    ax3.set_xlabel('Time (s)', fontsize=14, fontweight='bold')
    ax3.set_ylabel('Angular Velocity (deg/s)', fontsize=14, fontweight='bold')
    ax3.set_title('C', fontsize=18, fontweight='bold', loc='left', pad=15)
    ax3.legend(loc='upper right', fontsize=11, framealpha=0.95)
    ax3.grid(alpha=0.3)
    
    # Add metrics
    textstr = (f'Hip Max Vel: {np.abs(hip_vel).max():.1f} deg/s\n'
              f'Knee Max Vel: {np.abs(knee_vel).max():.1f} deg/s\n'
              f'Ankle Max Vel: {np.abs(ankle_vel).max():.1f} deg/s')
    ax3.text(0.02, 0.02, textstr, transform=ax3.transAxes, fontsize=11,
            verticalalignment='bottom', bbox=props, family='monospace',
            fontweight='bold')
    
    # Panel D: Phase Space (Knee Angle vs Velocity)
    ax4 = fig.add_subplot(gs[1, 1])
    
    # Create phase space plot for knee (most important for running)
    scatter = ax4.scatter(knee, knee_vel, c=t, cmap='viridis',
                         s=30, alpha=0.6, edgecolors='black', linewidth=0.5)
    
    # Add trajectory line
    ax4.plot(knee, knee_vel, 'k-', linewidth=1, alpha=0.2)
    
    # Mark start and end
    ax4.scatter([knee[0]], [knee_vel[0]], s=200, c='green', marker='o',
               edgecolors='black', linewidth=2, label='Start', zorder=5)
    ax4.scatter([knee[-1]], [knee_vel[-1]], s=200, c='red', marker='s',
               edgecolors='black', linewidth=2, label='End', zorder=5)
    
    # Add zero velocity line
    ax4.axhline(0, color='gray', linestyle='--', linewidth=1.5, alpha=0.5)
    
    ax4.set_xlabel('Knee Angle (degrees)', fontsize=14, fontweight='bold')
    ax4.set_ylabel('Knee Angular Velocity (deg/s)', fontsize=14, fontweight='bold')
    ax4.set_title('D', fontsize=18, fontweight='bold', loc='left', pad=15)
    ax4.legend(loc='upper left', fontsize=11, framealpha=0.95)
    ax4.grid(alpha=0.3)
    
    # Add colorbar
    cbar = plt.colorbar(scatter, ax=ax4)
    cbar.set_label('Time (s)', fontsize=12, fontweight='bold')
    
    # Add note
    textstr = 'Phase space shows\nknee joint dynamics\n(cyclic pattern)'
    ax4.text(0.98, 0.02, textstr, transform=ax4.transAxes, fontsize=11,
            verticalalignment='bottom', horizontalalignment='right',
            bbox=props, fontweight='bold')
    
    # Overall title
    fig.suptitle('Joint Angle Kinematics During Running',
                fontsize=20, fontweight='bold', y=0.995)
    
    plt.tight_layout()
    return fig

def create_gait_cycle_panel(joint_data):
    """
    Create 4-panel figure showing gait cycle analysis.
    """
    
    plt.style.use('seaborn-v0_8-white')
    
    fig = plt.figure(figsize=(22, 14))
    gs = GridSpec(2, 2, figure=fig, hspace=0.35, wspace=0.35)
    
    # Extract data
    t = joint_data['timestamp_s'].values
    hip = joint_data['hip'].values
    knee = joint_data['knee'].values
    ankle = joint_data['ankle'].values
    
    # Detect gait cycles using knee angle peaks
    peaks, _ = find_peaks(knee, distance=len(t)//20, prominence=10)
    
    # Panel A: Gait Cycle Identification
    ax1 = fig.add_subplot(gs[0, 0])
    
    ax1.plot(t, knee, linewidth=2.5, color='#3498db', alpha=0.8, label='Knee Angle')
    
    # Mark detected cycles
    if len(peaks) > 0:
        ax1.scatter(t[peaks], knee[peaks], s=200, c='red', marker='o',
                   edgecolors='black', linewidth=2, zorder=5,
                   label=f'Gait Cycles (n={len(peaks)})')
        
        # Draw vertical lines for cycle boundaries
        for peak in peaks:
            ax1.axvline(t[peak], color='red', linestyle='--',
                       linewidth=1.5, alpha=0.5)
    
    ax1.set_xlabel('Time (s)', fontsize=14, fontweight='bold')
    ax1.set_ylabel('Knee Angle (degrees)', fontsize=14, fontweight='bold')
    ax1.set_title('A', fontsize=18, fontweight='bold', loc='left', pad=15)
    ax1.legend(loc='upper right', fontsize=11, framealpha=0.95)
    ax1.grid(alpha=0.3)
    
    # Calculate cycle statistics
    if len(peaks) > 1:
        cycle_times = np.diff(t[peaks])
        mean_cycle = np.mean(cycle_times)
        stride_freq = 1 / mean_cycle if mean_cycle > 0 else 0
        
        textstr = (f'Gait Cycles: {len(peaks)}\n'
                  f'Mean Cycle: {mean_cycle:.3f} s\n'
                  f'Stride Freq: {stride_freq:.2f} Hz\n'
                  f'Cadence: {stride_freq*60:.0f} steps/min')
    else:
        textstr = 'Insufficient cycles\nfor analysis'
    
    props = dict(boxstyle='round', facecolor='wheat', alpha=0.9,
                edgecolor='black', linewidth=2)
    ax1.text(0.02, 0.98, textstr, transform=ax1.transAxes, fontsize=11,
            verticalalignment='top', bbox=props, family='monospace',
            fontweight='bold')
    
    # Panel B: Normalized Gait Cycle (All Joints)
    ax2 = fig.add_subplot(gs[0, 1])
    
    if len(peaks) > 1:
        # Take first complete cycle
        start_idx = peaks[0]
        end_idx = peaks[1]
        
        # Normalize to 0-100% of gait cycle
        cycle_t = np.linspace(0, 100, end_idx - start_idx)
        
        hip_cycle = hip[start_idx:end_idx]
        knee_cycle = knee[start_idx:end_idx]
        ankle_cycle = ankle[start_idx:end_idx]
        
        ax2.plot(cycle_t, hip_cycle, linewidth=2.5, color='#e74c3c',
                alpha=0.8, label='Hip')
        ax2.plot(cycle_t, knee_cycle, linewidth=2.5, color='#3498db',
                alpha=0.8, label='Knee')
        ax2.plot(cycle_t, ankle_cycle, linewidth=2.5, color='#2ecc71',
                alpha=0.8, label='Ankle')
        
        # Mark stance and swing phases (approximate)
        ax2.axvspan(0, 60, alpha=0.2, color='blue', label='Stance')
        ax2.axvspan(60, 100, alpha=0.2, color='red', label='Swing')
        
        ax2.set_xlabel('Gait Cycle (%)', fontsize=14, fontweight='bold')
        ax2.set_ylabel('Joint Angle (degrees)', fontsize=14, fontweight='bold')
        ax2.set_title('B', fontsize=18, fontweight='bold', loc='left', pad=15)
        ax2.legend(loc='upper right', fontsize=10, framealpha=0.95)
        ax2.grid(alpha=0.3)
        
        textstr = 'Normalized single\ngait cycle\n(0-100%)'
        ax2.text(0.02, 0.02, textstr, transform=ax2.transAxes, fontsize=11,
                verticalalignment='bottom', bbox=props, fontweight='bold')
    else:
        ax2.text(0.5, 0.5, 'Insufficient data\nfor cycle normalization',
                transform=ax2.transAxes, fontsize=14, ha='center', va='center',
                bbox=props, fontweight='bold')
    
    # Panel C: Joint Coordination (Hip-Knee)
    ax3 = fig.add_subplot(gs[1, 0])
    
    # Plot hip vs knee angle
    scatter = ax3.scatter(hip, knee, c=t, cmap='viridis',
                         s=30, alpha=0.6, edgecolors='black', linewidth=0.5)
    ax3.plot(hip, knee, 'k-', linewidth=1, alpha=0.2)
    
    # Mark start and end
    ax3.scatter([hip[0]], [knee[0]], s=200, c='green', marker='o',
               edgecolors='black', linewidth=2, label='Start', zorder=5)
    ax3.scatter([hip[-1]], [knee[-1]], s=200, c='red', marker='s',
               edgecolors='black', linewidth=2, label='End', zorder=5)
    
    ax3.set_xlabel('Hip Angle (degrees)', fontsize=14, fontweight='bold')
    ax3.set_ylabel('Knee Angle (degrees)', fontsize=14, fontweight='bold')
    ax3.set_title('C', fontsize=18, fontweight='bold', loc='left', pad=15)
    ax3.legend(loc='upper left', fontsize=11, framealpha=0.95)
    ax3.grid(alpha=0.3)
    
    # Add colorbar
    cbar = plt.colorbar(scatter, ax=ax3)
    cbar.set_label('Time (s)', fontsize=12, fontweight='bold')
    
    # Calculate correlation
    corr = np.corrcoef(hip, knee)[0, 1]
    textstr = (f'Hip-Knee\nCoordination\n\n'
              f'Correlation: {corr:.3f}\n'
              f'(Cyclic coupling)')
    ax3.text(0.98, 0.98, textstr, transform=ax3.transAxes, fontsize=11,
            verticalalignment='top', horizontalalignment='right',
            bbox=props, fontweight='bold')
    
    # Panel D: Joint Range of Motion Summary
    ax4 = fig.add_subplot(gs[1, 1])
    
    # Calculate ROM for each joint
    joints = ['Hip', 'Knee', 'Ankle', 'Shoulder', 'Elbow']
    
    if 'shoulder' in joint_data.columns and 'elbow' in joint_data.columns:
        shoulder = joint_data['shoulder'].values
        elbow = joint_data['elbow'].values
        
        roms = [
            hip.max() - hip.min(),
            knee.max() - knee.min(),
            ankle.max() - ankle.min(),
            shoulder.max() - shoulder.min(),
            elbow.max() - elbow.min()
        ]
        
        means = [
            np.mean(hip),
            np.mean(knee),
            np.mean(ankle),
            np.mean(shoulder),
            np.mean(elbow)
        ]
    else:
        joints = joints[:3]
        roms = [
            hip.max() - hip.min(),
            knee.max() - knee.min(),
            ankle.max() - ankle.min()
        ]
        means = [
            np.mean(hip),
            np.mean(knee),
            np.mean(ankle)
        ]
    
    x = np.arange(len(joints))
    width = 0.35
    
    bars1 = ax4.bar(x - width/2, roms, width, label='Range of Motion',
                   color='#3498db', alpha=0.8, edgecolor='black', linewidth=2)
    bars2 = ax4.bar(x + width/2, means, width, label='Mean Angle',
                   color='#e74c3c', alpha=0.8, edgecolor='black', linewidth=2)
    
    ax4.set_ylabel('Angle (degrees)', fontsize=14, fontweight='bold')
    ax4.set_xticks(x)
    ax4.set_xticklabels(joints, fontsize=12, fontweight='bold')
    ax4.set_title('D', fontsize=18, fontweight='bold', loc='left', pad=15)
    ax4.legend(loc='upper right', fontsize=11, framealpha=0.95)
    ax4.grid(alpha=0.3, axis='y')
    
    # Add values on bars
    for bars in [bars1, bars2]:
        for bar in bars:
            height = bar.get_height()
            ax4.text(bar.get_x() + bar.get_width()/2., height + 2,
                    f'{height:.1f}°', ha='center', va='bottom',
                    fontsize=9, fontweight='bold')
    
    # Overall title
    fig.suptitle('Gait Cycle Analysis',
                fontsize=20, fontweight='bold', y=0.995)
    
    plt.tight_layout()
    return fig

def main():
    """Main function to generate joint kinematics visualizations."""
    
    # Load data
    data_path = Path('public/joint_angles_20251015_092343.csv')
    
    if not data_path.exists():
        print(f"Error: File not found: {data_path}")
        print("Please check the file path.")
        return
    
    joint_data = load_joint_data(data_path)
    
    # Create output directory
    output_dir = Path('output')
    output_dir.mkdir(exist_ok=True)
    
    print("="*70)
    print("GENERATING JOINT KINEMATICS ANALYSIS")
    print("="*70)
    print(f"\nLoaded {len(joint_data)} data points")
    print(f"Duration: {joint_data['timestamp_s'].max():.2f} seconds")
    print(f"Joints: {', '.join([col for col in joint_data.columns if col != 'timestamp_s'])}")
    
    print("\nGenerating Panel 1: Joint Kinematics...")
    fig1 = create_joint_kinematics_panel(joint_data)
    fig1.savefig(output_dir / 'figure_joint_kinematics.png',
                dpi=300, bbox_inches='tight')
    fig1.savefig(output_dir / 'figure_joint_kinematics.pdf',
                bbox_inches='tight')
    print("✓ Joint kinematics panel saved")
    
    print("\nGenerating Panel 2: Gait Cycle Analysis...")
    fig2 = create_gait_cycle_panel(joint_data)
    fig2.savefig(output_dir / 'figure_gait_cycle_analysis.png',
                dpi=300, bbox_inches='tight')
    fig2.savefig(output_dir / 'figure_gait_cycle_analysis.pdf',
                bbox_inches='tight')
    print("✓ Gait cycle panel saved")
    
    print("\n" + "="*70)
    print("JOINT KINEMATICS ANALYSIS COMPLETE")
    print("="*70)
    print(f"\nOutput location: {output_dir.absolute()}")
    
    plt.show()

if __name__ == "__main__":
    main()
