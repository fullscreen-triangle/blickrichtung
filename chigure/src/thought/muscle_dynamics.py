import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import seaborn as sns
from pathlib import Path
from scipy.signal import find_peaks

def load_muscle_data(filepath):
    """Load muscle activation CSV data."""
    return pd.read_csv(filepath)

def create_muscle_activation_panel(muscle_data):
    """
    Create 4-panel figure showing muscle activation patterns during running.
    """
    
    plt.style.use('seaborn-v0_8-whitegrid')
    
    fig = plt.figure(figsize=(22, 14))
    gs = GridSpec(2, 2, figure=fig, hspace=0.35, wspace=0.35)
    
    # Extract data
    t = muscle_data['timestamp_s'].values
    quadriceps = muscle_data['quadriceps'].values
    hamstrings = muscle_data['hamstrings'].values
    gastrocnemius = muscle_data['gastrocnemius'].values
    hip_flexors = muscle_data['hip_flexors'].values
    glutes = muscle_data['glutes'].values
    tibialis = muscle_data['tibialis_anterior'].values
    
    # Panel A: Muscle Activation Timeline (Leg Extensors)
    ax1 = fig.add_subplot(gs[0, 0])
    
    ax1.plot(t, quadriceps, linewidth=2.5, color='#e74c3c', alpha=0.8,
            label='Quadriceps')
    ax1.plot(t, hamstrings, linewidth=2.5, color='#3498db', alpha=0.8,
            label='Hamstrings')
    ax1.plot(t, gastrocnemius, linewidth=2.5, color='#2ecc71', alpha=0.8,
            label='Gastrocnemius')
    
    ax1.set_xlabel('Time (s)', fontsize=14, fontweight='bold')
    ax1.set_ylabel('Muscle Activation (0-1)', fontsize=14, fontweight='bold')
    ax1.set_title('A', fontsize=18, fontweight='bold', loc='left', pad=15)
    ax1.legend(loc='upper right', fontsize=11, framealpha=0.95)
    ax1.grid(alpha=0.3)
    ax1.set_ylim(-0.05, 1.05)
    
    # Add metrics
    textstr = (f'Quad Mean: {np.mean(quadriceps):.3f}\n'
              f'Hamstring Mean: {np.mean(hamstrings):.3f}\n'
              f'Gastro Mean: {np.mean(gastrocnemius):.3f}\n'
              f'Duration: {t[-1]:.1f} s')
    props = dict(boxstyle='round', facecolor='wheat', alpha=0.9,
                edgecolor='black', linewidth=2)
    ax1.text(0.02, 0.98, textstr, transform=ax1.transAxes, fontsize=11,
            verticalalignment='top', bbox=props, family='monospace',
            fontweight='bold')
    
    # Panel B: Muscle Activation Timeline (Hip & Ankle)
    ax2 = fig.add_subplot(gs[0, 1])
    
    ax2.plot(t, hip_flexors, linewidth=2.5, color='#9b59b6', alpha=0.8,
            label='Hip Flexors')
    ax2.plot(t, glutes, linewidth=2.5, color='#f39c12', alpha=0.8,
            label='Glutes')
    ax2.plot(t, tibialis, linewidth=2.5, color='#1abc9c', alpha=0.8,
            label='Tibialis Anterior')
    
    ax2.set_xlabel('Time (s)', fontsize=14, fontweight='bold')
    ax2.set_ylabel('Muscle Activation (0-1)', fontsize=14, fontweight='bold')
    ax2.set_title('B', fontsize=18, fontweight='bold', loc='left', pad=15)
    ax2.legend(loc='upper right', fontsize=11, framealpha=0.95)
    ax2.grid(alpha=0.3)
    ax2.set_ylim(-0.05, 1.05)
    
    # Add metrics
    textstr = (f'Hip Flexor Mean: {np.mean(hip_flexors):.3f}\n'
              f'Glute Mean: {np.mean(glutes):.3f}\n'
              f'Tibialis Mean: {np.mean(tibialis):.3f}')
    ax2.text(0.98, 0.98, textstr, transform=ax2.transAxes, fontsize=11,
            verticalalignment='top', horizontalalignment='right',
            bbox=props, family='monospace', fontweight='bold')
    
    # Panel C: Muscle Coordination Heatmap
    ax3 = fig.add_subplot(gs[1, 0])
    
    # Create correlation matrix
    muscles = {
        'Quadriceps': quadriceps,
        'Hamstrings': hamstrings,
        'Gastrocnemius': gastrocnemius,
        'Hip Flexors': hip_flexors,
        'Glutes': glutes,
        'Tibialis': tibialis
    }
    
    muscle_names = list(muscles.keys())
    muscle_data_matrix = np.array([muscles[name] for name in muscle_names])
    
    # Calculate correlation matrix
    corr_matrix = np.corrcoef(muscle_data_matrix)
    
    # Plot heatmap
    im = ax3.imshow(corr_matrix, cmap='RdBu_r', aspect='auto',
                   vmin=-1, vmax=1)
    
    # Add labels
    ax3.set_xticks(np.arange(len(muscle_names)))
    ax3.set_yticks(np.arange(len(muscle_names)))
    ax3.set_xticklabels(muscle_names, rotation=45, ha='right', fontsize=10)
    ax3.set_yticklabels(muscle_names, fontsize=10)
    
    # Add correlation values
    for i in range(len(muscle_names)):
        for j in range(len(muscle_names)):
            text = ax3.text(j, i, f'{corr_matrix[i, j]:.2f}',
                          ha='center', va='center', color='black',
                          fontsize=9, fontweight='bold')
    
    ax3.set_title('C', fontsize=18, fontweight='bold', loc='left', pad=15)
    
    # Add colorbar
    cbar = plt.colorbar(im, ax=ax3)
    cbar.set_label('Correlation', fontsize=12, fontweight='bold')
    
    # Panel D: Muscle Synergy Analysis
    ax4 = fig.add_subplot(gs[1, 1])
    
    # Calculate total activation and antagonist pairs
    extensor_synergy = (quadriceps + glutes + gastrocnemius) / 3
    flexor_synergy = (hamstrings + hip_flexors + tibialis) / 3
    
    ax4.plot(t, extensor_synergy, linewidth=3, color='#e74c3c',
            alpha=0.8, label='Extensor Synergy')
    ax4.plot(t, flexor_synergy, linewidth=3, color='#3498db',
            alpha=0.8, label='Flexor Synergy')
    
    # Fill between to show co-activation
    ax4.fill_between(t, extensor_synergy, flexor_synergy,
                    alpha=0.2, color='purple', label='Co-activation')
    
    ax4.set_xlabel('Time (s)', fontsize=14, fontweight='bold')
    ax4.set_ylabel('Synergy Activation (0-1)', fontsize=14, fontweight='bold')
    ax4.set_title('D', fontsize=18, fontweight='bold', loc='left', pad=15)
    ax4.legend(loc='upper right', fontsize=11, framealpha=0.95)
    ax4.grid(alpha=0.3)
    ax4.set_ylim(-0.05, 1.05)
    
    # Calculate co-activation index
    coactivation = np.minimum(extensor_synergy, flexor_synergy)
    coactivation_index = np.mean(coactivation)
    
    textstr = (f'Extensor Mean: {np.mean(extensor_synergy):.3f}\n'
              f'Flexor Mean: {np.mean(flexor_synergy):.3f}\n'
              f'Co-activation: {coactivation_index:.3f}\n\n'
              f'Higher co-activation =\nGreater stability')
    ax4.text(0.02, 0.02, textstr, transform=ax4.transAxes, fontsize=11,
            verticalalignment='bottom', bbox=props, fontweight='bold')
    
    # Overall title
    fig.suptitle('Muscle Activation Dynamics During Running',
                fontsize=20, fontweight='bold', y=0.995)
    
    plt.tight_layout()
    return fig

def create_muscle_timing_panel(muscle_data):
    """
    Create 4-panel figure showing muscle activation timing and patterns.
    """
    
    plt.style.use('seaborn-v0_8-white')
    
    fig = plt.figure(figsize=(22, 14))
    gs = GridSpec(2, 2, figure=fig, hspace=0.35, wspace=0.35)
    
    # Extract data
    t = muscle_data['timestamp_s'].values
    quadriceps = muscle_data['quadriceps'].values
    hamstrings = muscle_data['hamstrings'].values
    gastrocnemius = muscle_data['gastrocnemius'].values
    
    # Panel A: Activation Onset Detection
    ax1 = fig.add_subplot(gs[0, 0])
    
    # Detect activation onsets (threshold crossing)
    threshold = 0.3
    
    quad_onsets, _ = find_peaks(quadriceps, height=threshold, distance=len(t)//20)
    ham_onsets, _ = find_peaks(hamstrings, height=threshold, distance=len(t)//20)
    gastro_onsets, _ = find_peaks(gastrocnemius, height=threshold, distance=len(t)//20)
    
    ax1.plot(t, quadriceps, linewidth=2, color='#e74c3c', alpha=0.6,
            label='Quadriceps')
    ax1.plot(t, hamstrings, linewidth=2, color='#3498db', alpha=0.6,
            label='Hamstrings')
    ax1.plot(t, gastrocnemius, linewidth=2, color='#2ecc71', alpha=0.6,
            label='Gastrocnemius')
    
    # Mark onsets
    if len(quad_onsets) > 0:
        ax1.scatter(t[quad_onsets], quadriceps[quad_onsets], s=100,
                   c='red', marker='o', edgecolors='black', linewidth=2,
                   zorder=5)
    if len(ham_onsets) > 0:
        ax1.scatter(t[ham_onsets], hamstrings[ham_onsets], s=100,
                   c='blue', marker='s', edgecolors='black', linewidth=2,
                   zorder=5)
    if len(gastro_onsets) > 0:
        ax1.scatter(t[gastro_onsets], gastrocnemius[gastro_onsets], s=100,
                   c='green', marker='^', edgecolors='black', linewidth=2,
                   zorder=5)
    
    # Add threshold line
    ax1.axhline(threshold, color='black', linestyle='--', linewidth=2,
               alpha=0.5, label=f'Threshold ({threshold})')
    
    ax1.set_xlabel('Time (s)', fontsize=14, fontweight='bold')
    ax1.set_ylabel('Muscle Activation (0-1)', fontsize=14, fontweight='bold')
    ax1.set_title('A', fontsize=18, fontweight='bold', loc='left', pad=15)
    ax1.legend(loc='upper right', fontsize=10, framealpha=0.95)
    ax1.grid(alpha=0.3)
    ax1.set_ylim(-0.05, 1.05)
    
    # Add metrics
    props = dict(boxstyle='round', facecolor='wheat', alpha=0.9,
                edgecolor='black', linewidth=2)
    textstr = (f'Quad Activations: {len(quad_onsets)}\n'
              f'Ham Activations: {len(ham_onsets)}\n'
              f'Gastro Activations: {len(gastro_onsets)}')
    ax1.text(0.02, 0.98, textstr, transform=ax1.transAxes, fontsize=11,
            verticalalignment='top', bbox=props, family='monospace',
            fontweight='bold')
    
    # Panel B: Muscle Activation Sequence
    ax2 = fig.add_subplot(gs[0, 1])
    
    # Create raster plot showing activation timing
    muscles_list = ['Quadriceps', 'Hamstrings', 'Gastrocnemius',
                   'Hip Flexors', 'Glutes', 'Tibialis']
    
    for i, muscle_name in enumerate(muscles_list):
        muscle_col = muscle_name.lower().replace(' ', '_')
        if muscle_col in muscle_data.columns:
            activation = muscle_data[muscle_col].values
            
            # Find active periods
            active = activation > threshold
            
            # Plot as horizontal bars
            for j in range(len(t)-1):
                if active[j]:
                    ax2.plot([t[j], t[j+1]], [i, i], linewidth=8,
                            color='red', alpha=0.7)
        else:
            # Handle column name variations
            if muscle_name == 'Hip Flexors' and 'hip_flexors' in muscle_data.columns:
                activation = muscle_data['hip_flexors'].values
                active = activation > threshold
                for j in range(len(t)-1):
                    if active[j]:
                        ax2.plot([t[j], t[j+1]], [i, i], linewidth=8,
                                color='red', alpha=0.7)
    
    ax2.set_yticks(range(len(muscles_list)))
    ax2.set_yticklabels(muscles_list, fontsize=11, fontweight='bold')
    ax2.set_xlabel('Time (s)', fontsize=14, fontweight='bold')
    ax2.set_title('B', fontsize=18, fontweight='bold', loc='left', pad=15)
    ax2.grid(alpha=0.3, axis='x')
    ax2.set_ylim(-0.5, len(muscles_list) - 0.5)
    
    textstr = 'Red bars =\nActive periods\n(> threshold)'
    ax2.text(0.98, 0.98, textstr, transform=ax2.transAxes, fontsize=11,
            verticalalignment='top', horizontalalignment='right',
            bbox=props, fontweight='bold')
    
    # Panel C: Activation Duration Distribution
    ax3 = fig.add_subplot(gs[1, 0])
    
    # Calculate activation durations for each muscle
    muscles_for_duration = {
        'Quadriceps': quadriceps,
        'Hamstrings': hamstrings,
        'Gastrocnemius': gastrocnemius
    }
    
    durations_all = []
    labels_all = []
    
    for muscle_name, activation in muscles_for_duration.items():
        # Find continuous activation periods
        active = activation > threshold
        changes = np.diff(active.astype(int))
        
        starts = np.where(changes == 1)[0]
        ends = np.where(changes == -1)[0]
        
        # Match starts and ends
        if len(starts) > 0 and len(ends) > 0:
            if starts[0] > ends[0]:
                ends = ends[1:]
            if len(starts) > len(ends):
                starts = starts[:len(ends)]
            
            durations = (t[ends] - t[starts]) * 1000  # Convert to ms
            durations_all.extend(durations)
            labels_all.extend([muscle_name] * len(durations))
    
    if len(durations_all) > 0:
        # Create violin plot
        df_durations = pd.DataFrame({'Duration (ms)': durations_all,
                                     'Muscle': labels_all})
        
        unique_muscles = df_durations['Muscle'].unique()
        positions = np.arange(len(unique_muscles))
        
        parts = ax3.violinplot([df_durations[df_durations['Muscle'] == m]['Duration (ms)'].values
                               for m in unique_muscles],
                              positions=positions, widths=0.7,
                              showmeans=True, showmedians=True)
        
        # Color violins
        colors = ['#e74c3c', '#3498db', '#2ecc71']
        for pc, color in zip(parts['bodies'], colors):
            pc.set_facecolor(color)
            pc.set_alpha(0.7)
        
        ax3.set_xticks(positions)
        ax3.set_xticklabels(unique_muscles, fontsize=11, fontweight='bold')
        ax3.set_ylabel('Activation Duration (ms)', fontsize=14, fontweight='bold')
        ax3.set_title('C', fontsize=18, fontweight='bold', loc='left', pad=15)
        ax3.grid(alpha=0.3, axis='y')
    else:
        ax3.text(0.5, 0.5, 'No activations detected\nabove threshold',
                transform=ax3.transAxes, fontsize=14, ha='center', va='center',
                bbox=props, fontweight='bold')
    
    # Panel D: Total Muscle Work (Integrated Activation)
    ax4 = fig.add_subplot(gs[1, 1])
    
    # Calculate integrated activation (area under curve)
    dt = np.mean(np.diff(t))
    
    work_values = []
    muscle_names_work = []
    
    for col in muscle_data.columns:
        if col != 'timestamp_s':
            activation = muscle_data[col].values
            work = np.trapz(activation, dx=dt)
            work_values.append(work)
            # Clean up column name for display
            display_name = col.replace('_', ' ').title()
            muscle_names_work.append(display_name)
    
    # Sort by work
    sorted_indices = np.argsort(work_values)[::-1]
    work_values = [work_values[i] for i in sorted_indices]
    muscle_names_work = [muscle_names_work[i] for i in sorted_indices]
    
    colors_work = plt.cm.viridis(np.linspace(0, 1, len(work_values)))
    
    bars = ax4.barh(muscle_names_work, work_values, color=colors_work,
                   alpha=0.8, edgecolor='black', linewidth=2)
    
    ax4.set_xlabel('Integrated Activation (work)', fontsize=14, fontweight='bold')
    ax4.set_title('D', fontsize=18, fontweight='bold', loc='left', pad=15)
    ax4.grid(alpha=0.3, axis='x')
    
    # Add values
    for bar, val in zip(bars, work_values):
        width = bar.get_width()
        ax4.text(width + 0.5, bar.get_y() + bar.get_height()/2,
                f'{val:.2f}', va='center', fontsize=10, fontweight='bold')
    
    textstr = 'Total work =\nIntegrated activation\nover time'
    ax4.text(0.98, 0.02, textstr, transform=ax4.transAxes, fontsize=11,
            verticalalignment='bottom', horizontalalignment='right',
            bbox=props, fontweight='bold')
    
    # Overall title
    fig.suptitle('Muscle Activation Timing and Patterns',
                fontsize=20, fontweight='bold', y=0.995)
    
    plt.tight_layout()
    return fig

def main():
    """Main function to generate muscle activation visualizations."""
    
    # Load data
    data_path = Path('public/muscle_activation_20251015_092343.csv')
    
    if not data_path.exists():
        print(f"Error: File not found: {data_path}")
        print("Please check the file path.")
        return
    
    muscle_data = load_muscle_data(data_path)
    
    # Create output directory
    output_dir = Path('output')
    output_dir.mkdir(exist_ok=True)
    
    print("="*70)
    print("GENERATING MUSCLE ACTIVATION ANALYSIS")
    print("="*70)
    print(f"\nLoaded {len(muscle_data)} data points")
    print(f"Duration: {muscle_data['timestamp_s'].max():.2f} seconds")
    print(f"Muscles: {', '.join([col for col in muscle_data.columns if col != 'timestamp_s'])}")
    
    print("\nGenerating Panel 1: Muscle Activation...")
    fig1 = create_muscle_activation_panel(muscle_data)
    fig1.savefig(output_dir / 'figure_muscle_activation.png',
                dpi=300, bbox_inches='tight')
    fig1.savefig(output_dir / 'figure_muscle_activation.pdf',
                bbox_inches='tight')
    print("✓ Muscle activation panel saved")
    
    print("\nGenerating Panel 2: Muscle Timing...")
    fig2 = create_muscle_timing_panel(muscle_data)
    fig2.savefig(output_dir / 'figure_muscle_timing.png',
                dpi=300, bbox_inches='tight')
    fig2.savefig(output_dir / 'figure_muscle_timing.pdf',
                bbox_inches='tight')
    print("✓ Muscle timing panel saved")
    
    print("\n" + "="*70)
    print("MUSCLE ACTIVATION ANALYSIS COMPLETE")
    print("="*70)
    print(f"\nOutput location: {output_dir.absolute()}")
    
    plt.show()

if __name__ == "__main__":
    main()
