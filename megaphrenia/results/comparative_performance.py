import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from matplotlib.patches import Rectangle

# Set publication style
plt.rcParams.update({
    'font.size': 12,
    'axes.titlesize': 14,
    'axes.labelsize': 12,
    'xtick.labelsize': 10,
    'ytick.labelsize': 10,
    'legend.fontsize': 10,
    'figure.titlesize': 16
})

if __name__ == "__main__":


    # Figure 3: Comparative Analysis
    fig3, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10))
    fig3.suptitle('MEGAPHRENIA Comparative Performance Analysis', fontweight='bold')

    # Panel A: Run Comparison
    runs = ['Run 1\n(09:00:44)', 'Run 2\n(09:19:57)']
    success_rates = [data1['summary']['success_rate'], data2['summary']['success_rate']]
    durations = [data1['metadata']['total_duration_seconds'], data2['metadata']['total_duration_seconds']]

    x = np.arange(len(runs))
    width = 0.35

    bars1 = ax1.bar(x - width/2, success_rates, width, label='Success Rate (%)', color='lightblue', alpha=0.8)
    ax1_twin = ax1.twinx()
    bars2 = ax1_twin.bar(x + width/2, durations, width, label='Duration (s)', color='lightcoral', alpha=0.8)

    ax1.set_xlabel('Test Runs')
    ax1.set_ylabel('Success Rate (%)', color='blue')
    ax1_twin.set_ylabel('Duration (seconds)', color='red')
    ax1.set_title('Performance Comparison')
    ax1.set_xticks(x)
    ax1.set_xticklabels(runs)

    # Panel B: Test Category Stability
    categories = ['Psychon\nCreation', 'BMD\nOperations', 'S-Entropy\nCoords', 'Circuit\nIntegration']
    run1_perf = [100, 100, 100, 75]
    run2_perf = [100, 100, 100, 75]

    x_pos = np.arange(len(categories))
    ax2.plot(x_pos, run1_perf, 'o-', label='Run 1', linewidth=2, markersize=8, color='blue')
    ax2.plot(x_pos, run2_perf, 's-', label='Run 2', linewidth=2, markersize=8, color='red')
    ax2.set_xticks(x_pos)
    ax2.set_xticklabels(categories, rotation=45, ha='right')
    ax2.set_ylabel('Success Rate (%)')
    ax2.set_title('Category Consistency')
    ax2.legend()
    ax2.grid(True, alpha=0.3)

    # Panel C: Execution Time Comparison
    test_names_short = [name[:15] + '...' for name in csv1['Test Name'].str.replace('"', '')]
    run1_times = csv1['Duration (s)']
    run2_times = csv2['Duration (s)']

    x_pos = np.arange(len(test_names_short))
    bars1 = ax3.bar(x_pos - 0.4, run1_times, 0.4, label='Run 1', alpha=0.8, color='skyblue')
    bars2 = ax3.bar(x_pos, run2_times, 0.4, label='Run 2', alpha=0.8, color='lightcoral')
    ax3.set_xlabel('Tests')
    ax3.set_ylabel('Duration (seconds)')
    ax3.set_title('Individual Test Comparison')
    ax3.set_xticks(x_pos)
    ax3.set_xticklabels(test_names_short, rotation=90, fontsize=6)
    ax3.legend()

    # Panel D: Improvement Analysis
    improvement = ((run1_times - run2_times) / run1_times * 100).fillna(0)
    colors = ['green' if x > 0 else 'red' for x in improvement]
    bars = ax4.bar(range(len(improvement)), improvement, color=colors, alpha=0.7)
    ax4.axhline(y=0, color='black', linestyle='-', alpha=0.5)
    ax4.set_xlabel('Test Index')
    ax4.set_ylabel('Improvement (%)')
    ax4.set_title('Performance Delta')

    plt.tight_layout()
    plt.savefig('megaphrenia_comparative_analysis.png', dpi=300, bbox_inches='tight')
    plt.show()
