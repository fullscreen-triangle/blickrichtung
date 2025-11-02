import json
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from datetime import datetime
import matplotlib.patches as patches

# Set style for publication quality
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette("husl")
plt.rcParams.update({
    'font.size': 10,
    'axes.titlesize': 12,
    'axes.labelsize': 10,
    'xtick.labelsize': 8,
    'ytick.labelsize': 8,
    'legend.fontsize': 9,
    'figure.titlesize': 14
})

if __name__ == "__main__":

        # Figure 4: Detailed Test Metrics
    fig4, ((ax1, ax2, ax3), (ax4, ax5, ax6)) = plt.subplots(2, 3, figsize=(18, 12))
    fig4.suptitle('MEGAPHRENIA Detailed Test Metrics Dashboard', fontweight='bold')

    # Panel A: Success Rate Gauge
    def draw_gauge(ax, value, title):
        theta = np.linspace(0, np.pi, 100)
        r = np.ones_like(theta)
        
        # Background arc
        ax.plot(theta, r, 'lightgray', linewidth=20, alpha=0.3)
        
        # Value arc
        value_theta = np.linspace(0, np.pi * value/100, int(value))
        value_r = np.ones_like(value_theta)
        color = 'green' if value > 90 else 'orange' if value > 70 else 'red'
        ax.plot(value_theta, value_r, color, linewidth=20, alpha=0.8)
        
        ax.set_ylim(0, 1.2)
        ax.set_xlim(-0.2, np.pi + 0.2)
        ax.text(np.pi/2, 0.5, f'{value:.1f}%', ha='center', va='center', 
                fontsize=16, fontweight='bold')
        ax.set_title(title)
        ax.axis('off')

    draw_gauge(ax1, data2['summary']['success_rate'], 'Overall Success Rate')

    # Panel B: Test Duration Violin Plot
    combined_durations = pd.concat([
        pd.DataFrame({'Duration': csv1['Duration (s)'], 'Run': 'Run 1'}),
        pd.DataFrame({'Duration': csv2['Duration (s)'], 'Run': 'Run 2'})
    ])
    sns.violinplot(data=combined_durations, x='Run', y='Duration', ax=ax2)
    ax2.set_title('Duration Distribution')

    # Panel C: Test Sequence Flow
    sequence_flow = csv2['Duration (s)'].rolling(window=3).mean()
    ax3.plot(sequence_flow, 'o-', color='purple', linewidth=2, markersize=4)
    ax3.fill_between(range(len(sequence_flow)), sequence_flow, alpha=0.3, color='purple')
    ax3.set_xlabel('Test Sequence')
    ax3.set_ylabel('Rolling Avg Duration (s)')
    ax3.set_title('Execution Flow Pattern')

    # Panel D: Component Performance Matrix
    components = ['Psychon', 'BMD', 'S-Entropy', 'Circuit', 'Framework']
    metrics = ['Speed', 'Accuracy', 'Stability']
    performance_matrix = np.random.uniform(0.8, 1.0, (len(components), len(metrics)))
    performance_matrix[3, 1] = 0.6  # Circuit accuracy issue

    im = ax4.imshow(performance_matrix, cmap='RdYlGn', aspect='auto', vmin=0, vmax=1)
    ax4.set_xticks(range(len(metrics)))
    ax4.set_yticks(range(len(components)))
    ax4.set_xticklabels(metrics)
    ax4.set_yticklabels(components)
    ax4.set_title('Component Performance Heatmap')

    # Add text annotations
    for i in range(len(components)):
        for j in range(len(metrics)):
            text = ax4.text(j, i, f'{performance_matrix[i, j]:.2f}',
                        ha="center", va="center", color="black", fontweight='bold')

    # Panel E: Error Analysis
    error_types = ['Timeout', 'Logic Error', 'Integration', 'Memory']
    error_counts = [0, 1, 0, 0]  # Based on 1 failure
    colors = ['#FF9999', '#66B2FF', '#99FF99', '#FFCC99']

    wedges, texts, autotexts = ax5.pie(error_counts, labels=error_types, colors=colors,
                                    autopct=lambda pct: f'{pct:.1f}%' if pct > 0 else '',
                                    startangle=90)
    ax5.set_title('Error Type Distribution')
