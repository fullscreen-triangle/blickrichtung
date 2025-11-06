"""
Hierarchical BMD Composition
Models nested cascades of Biological Maxwell Demons for multi-level consciousness programming.
Implements hierarchical information compression and categorical depth.
"""

import numpy as np
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from datetime import datetime
from pathlib import Path
import networkx as nx


class HierarchicalBMDComposer:
    """Simulate hierarchical BMD cascades for consciousness programming."""
    
    def __init__(self, n_levels=5, branching_factor=3):
        """
        Initialize hierarchical BMD cascade.
        
        Args:
            n_levels: Number of hierarchical levels (depth)
            branching_factor: Number of child BMDs per parent BMD
        """
        self.n_levels = n_levels
        self.branching = branching_factor
        
        # Physical constants
        self.kB = 1.380649e-23  # Boltzmann constant
        self.T = 310.15  # Temperature (K)
        
        # Build BMD hierarchy
        self.hierarchy = self._build_hierarchy()
        
    def _build_hierarchy(self):
        """Build hierarchical BMD network as directed graph."""
        G = nx.DiGraph()
        
        node_id = 0
        level_nodes = {0: [0]}
        G.add_node(0, level=0, bmd_id=0)
        node_id += 1
        
        for level in range(1, self.n_levels):
            level_nodes[level] = []
            for parent in level_nodes[level - 1]:
                for _ in range(self.branching):
                    G.add_node(node_id, level=level, bmd_id=node_id)
                    G.add_edge(parent, node_id)
                    level_nodes[level].append(node_id)
                    node_id += 1
        
        return G
    
    def generate_input_signals(self, n_signals=1000):
        """
        Generate input signals (oscillatory endpoints) at leaf level.
        """
        # Random phases and amplitudes
        phases = np.random.uniform(0, 2*np.pi, n_signals)
        amplitudes = np.random.exponential(1.0, n_signals)
        frequencies = np.random.normal(1000, 100, n_signals)
        
        signals = {
            'phases': phases,
            'amplitudes': amplitudes,
            'frequencies': frequencies,
            'information_content': np.random.exponential(1.0, n_signals)  # bits per signal
        }
        
        return signals
    
    def bmd_filtering(self, signals, filter_threshold, filter_type='phase'):
        """
        BMD filters signals based on specified criterion.
        
        Args:
            signals: Dictionary of signal properties
            filter_threshold: Threshold for filtering
            filter_type: 'phase', 'amplitude', or 'frequency'
        """
        if filter_type == 'phase':
            criterion = np.abs(signals['phases'] - filter_threshold)
            criterion = np.minimum(criterion, 2*np.pi - criterion)
            passed = criterion < np.pi/3  # 60° tolerance
            
        elif filter_type == 'amplitude':
            criterion = signals['amplitudes']
            passed = criterion > filter_threshold
            
        elif filter_type == 'frequency':
            criterion = np.abs(signals['frequencies'] - filter_threshold)
            passed = criterion < 200  # 200 Hz tolerance
        
        # Filter signals
        filtered_signals = {}
        for key in signals:
            filtered_signals[key] = signals[key][passed]
        
        filtering_rate = np.sum(passed) / len(passed)
        
        return filtered_signals, filtering_rate
    
    def calculate_information_compression(self, input_info, output_info):
        """
        Calculate information compression ratio.
        Compression = log2(I_in / I_out)
        """
        total_in = np.sum(input_info) if len(input_info) > 0 else 1e-10
        total_out = np.sum(output_info) if len(output_info) > 0 else 1e-10
        
        compression = np.log2(total_in / total_out) if total_out > 0 else 0
        
        return compression, total_in, total_out
    
    def propagate_through_hierarchy(self, input_signals, drug_params):
        """
        Propagate signals through hierarchical BMD cascade.
        Each level filters and compresses information.
        """
        # Get leaf nodes (highest level)
        leaf_level = self.n_levels - 1
        leaf_nodes = [n for n, d in self.hierarchy.nodes(data=True) 
                     if d['level'] == leaf_level]
        
        # Distribute input signals to leaf nodes
        signals_per_node = len(input_signals['phases']) // len(leaf_nodes)
        
        # Track information flow through hierarchy
        level_stats = []
        
        current_signals = input_signals
        
        # Process from leaves to root (bottom-up)
        for level in range(self.n_levels - 1, -1, -1):
            level_nodes = [n for n, d in self.hierarchy.nodes(data=True) 
                          if d['level'] == level]
            
            # Apply BMD filtering at this level
            # Filter parameters depend on drug and level
            filter_threshold = drug_params['filter_thresholds'][level]
            filter_type = drug_params['filter_types'][level]
            
            filtered_signals, filtering_rate = self.bmd_filtering(
                current_signals,
                filter_threshold,
                filter_type
            )
            
            # Calculate information compression
            compression, info_in, info_out = self.calculate_information_compression(
                current_signals['information_content'],
                filtered_signals['information_content']
            )
            
            # Calculate ATP cost (proportional to signals processed)
            atp_cost = len(current_signals['phases']) * len(level_nodes) * 0.5
            
            level_stats.append({
                'level': level,
                'n_nodes': len(level_nodes),
                'n_signals_in': len(current_signals['phases']),
                'n_signals_out': len(filtered_signals['phases']),
                'filtering_rate': float(filtering_rate),
                'information_in': float(info_in),
                'information_out': float(info_out),
                'compression_bits': float(compression),
                'atp_cost': float(atp_cost)
            })
            
            # Update signals for next level
            current_signals = filtered_signals
        
        return level_stats, current_signals
    
    def simulate_drug_cascade(self, drug_name):
        """
        Simulate drug-specific hierarchical BMD cascade.
        Different drugs have different filtering strategies.
        """
        # Define drug-specific filtering parameters
        if drug_name == 'lithium':
            # Lithium: Aggressive phase filtering (stabilization)
            drug_params = {
                'filter_thresholds': [0.0, 0.0, 0.0, 0.0, 0.0],  # Phase target = 0
                'filter_types': ['phase', 'phase', 'amplitude', 'frequency', 'phase']
            }
            
        elif drug_name == 'dopamine':
            # Dopamine: Amplitude-based filtering (activation)
            drug_params = {
                'filter_thresholds': [0.8, 0.9, 1.0, 1000, np.pi/2],
                'filter_types': ['amplitude', 'amplitude', 'amplitude', 'frequency', 'phase']
            }
            
        elif drug_name == 'serotonin':
            # Serotonin: Frequency stabilization
            drug_params = {
                'filter_thresholds': [1000, 1000, 1.0, np.pi, 1000],
                'filter_types': ['frequency', 'frequency', 'amplitude', 'phase', 'frequency']
            }
        
        # Generate input signals
        input_signals = self.generate_input_signals(n_signals=1000)
        
        # Propagate through hierarchy
        level_stats, final_signals = self.propagate_through_hierarchy(
            input_signals,
            drug_params
        )
        
        # Calculate overall metrics
        total_compression = sum(s['compression_bits'] for s in level_stats)
        total_atp = sum(s['atp_cost'] for s in level_stats)
        final_filtering_rate = len(final_signals['phases']) / 1000
        
        # Calculate categorical depth (number of active levels)
        active_levels = sum(1 for s in level_stats if s['n_signals_out'] > 0)
        
        # Calculate consciousness programming depth
        # Deeper hierarchies = more sophisticated programming
        programming_depth = active_levels / self.n_levels
        
        results = {
            'drug_name': drug_name,
            'n_hierarchical_levels': self.n_levels,
            'branching_factor': self.branching,
            'n_input_signals': 1000,
            'n_output_signals': len(final_signals['phases']),
            'overall_filtering_rate': float(final_filtering_rate),
            'total_information_compression_bits': float(total_compression),
            'total_atp_cost': float(total_atp),
            'active_levels': int(active_levels),
            'categorical_depth': int(active_levels),
            'programming_depth': float(programming_depth),
            'level_statistics': level_stats
        }
        
        return results, final_signals


def main():
    """Main validation function."""
    print("=" * 80)
    print("Hierarchical BMD Composition Analysis")
    print("Validating Nested Information Processing Cascades")
    print("=" * 80)
    
    # Test molecules
    drugs = ['lithium', 'dopamine', 'serotonin']
    
    # Run simulations
    all_results = []
    
    for drug_name in drugs:
        print(f"\n{'='*60}")
        print(f"Simulating: {drug_name.upper()}")
        print(f"{'='*60}")
        
        # Initialize composer
        composer = HierarchicalBMDComposer(n_levels=5, branching_factor=3)
        
        # Simulate cascade
        result, final_signals = composer.simulate_drug_cascade(drug_name)
        
        all_results.append(result)
        
        # Print results
        print(f"Hierarchical Levels:           {result['n_hierarchical_levels']}")
        print(f"Input Signals:                 {result['n_input_signals']}")
        print(f"Output Signals:                {result['n_output_signals']}")
        print(f"Overall Filtering Rate:        {result['overall_filtering_rate']:.4f}")
        print(f"Total Info Compression:        {result['total_information_compression_bits']:.2f} bits")
        print(f"Total ATP Cost:                {result['total_atp_cost']:.1f} ATP")
        print(f"Active Levels:                 {result['active_levels']}")
        print(f"Categorical Depth:             {result['categorical_depth']}")
        print(f"Programming Depth:             {result['programming_depth']:.4f}")
        
        print(f"\nLevel-by-Level Breakdown:")
        for level_stat in result['level_statistics']:
            print(f"  Level {level_stat['level']}: "
                  f"{level_stat['n_signals_in']} → {level_stat['n_signals_out']} signals, "
                  f"compression: {level_stat['compression_bits']:.2f} bits")
    
    # Save results
    output_dir = Path("chatelier/src/computing/results")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Save JSON
    json_path = output_dir / f"hierarchical_bmd_results_{timestamp}.json"
    with open(json_path, 'w') as f:
        json.dump({
            'timestamp': timestamp,
            'theory': 'Hierarchical BMD Composition',
            'results': all_results
        }, f, indent=2)
    
    print(f"\n{'='*60}")
    print(f"Results saved to: {json_path}")
    
    # Create visualizations
    fig = plt.figure(figsize=(16, 12))
    gs = fig.add_gridspec(3, 3, hspace=0.35, wspace=0.3)
    
    fig.suptitle('Hierarchical BMD Composition: Multi-Level Consciousness Programming', 
                 fontsize=15, fontweight='bold')
    
    colors = {'lithium': '#2ecc71', 'dopamine': '#3498db', 'serotonin': '#9b59b6'}
    
    # Plot 1: Overall filtering rates
    ax = fig.add_subplot(gs[0, 0])
    filtering_rates = [r['overall_filtering_rate'] for r in all_results]
    bars = ax.bar(drugs, filtering_rates, color=[colors[d] for d in drugs])
    ax.set_ylabel('Overall Filtering Rate', fontsize=10, fontweight='bold')
    ax.set_title('End-to-End Signal Filtering', fontsize=11, fontweight='bold')
    ax.set_ylim([0, 1])
    ax.grid(axis='y', alpha=0.3)
    for i, bar in enumerate(bars):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{filtering_rates[i]:.3f}',
                ha='center', va='bottom', fontweight='bold', fontsize=9)
    
    # Plot 2: Programming depth
    ax = fig.add_subplot(gs[0, 1])
    prog_depth = [r['programming_depth'] for r in all_results]
    bars = ax.bar(drugs, prog_depth, color=[colors[d] for d in drugs])
    ax.set_ylabel('Programming Depth', fontsize=10, fontweight='bold')
    ax.set_title('Consciousness Programming Depth', fontsize=11, fontweight='bold')
    ax.set_ylim([0, 1])
    ax.grid(axis='y', alpha=0.3)
    for i, bar in enumerate(bars):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{prog_depth[i]:.3f}',
                ha='center', va='bottom', fontweight='bold', fontsize=9)
    
    # Plot 3: Information compression
    ax = fig.add_subplot(gs[0, 2])
    compression = [r['total_information_compression_bits'] for r in all_results]
    bars = ax.bar(drugs, compression, color=[colors[d] for d in drugs])
    ax.set_ylabel('Total Compression (bits)', fontsize=10, fontweight='bold')
    ax.set_title('Hierarchical Information Compression', fontsize=11, fontweight='bold')
    ax.grid(axis='y', alpha=0.3)
    for i, bar in enumerate(bars):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{compression[i]:.1f}',
                ha='center', va='bottom', fontweight='bold', fontsize=9)
    
    # Plot 4-6: Level-by-level signal flow
    for idx, drug_name in enumerate(drugs):
        ax = fig.add_subplot(gs[1, idx])
        stats = all_results[idx]['level_statistics']
        levels = [s['level'] for s in stats]
        signals_in = [s['n_signals_in'] for s in stats]
        signals_out = [s['n_signals_out'] for s in stats]
        
        ax.plot(levels, signals_in, 'o-', linewidth=2, markersize=8, 
               label='Input', color=colors[drug_name], alpha=0.6)
        ax.plot(levels, signals_out, 's-', linewidth=2, markersize=8,
               label='Output', color=colors[drug_name])
        
        ax.set_xlabel('Hierarchical Level', fontweight='bold', fontsize=10)
        ax.set_ylabel('Number of Signals', fontweight='bold', fontsize=10)
        ax.set_title(f'{drug_name.capitalize()}: Signal Cascade', 
                    fontweight='bold', fontsize=11)
        ax.legend(fontsize=9)
        ax.grid(alpha=0.3)
        ax.invert_xaxis()  # Root at right
    
    # Plot 7: ATP costs comparison
    ax = fig.add_subplot(gs[2, 0])
    atp_costs = [r['total_atp_cost'] for r in all_results]
    bars = ax.bar(drugs, atp_costs, color=[colors[d] for d in drugs])
    ax.set_ylabel('Total ATP Cost', fontsize=10, fontweight='bold')
    ax.set_title('Thermodynamic Cost of Hierarchy', fontsize=11, fontweight='bold')
    ax.grid(axis='y', alpha=0.3)
    for i, bar in enumerate(bars):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{atp_costs[i]:.0f}',
                ha='center', va='bottom', fontweight='bold', fontsize=9)
    
    # Plot 8: Categorical depth
    ax = fig.add_subplot(gs[2, 1])
    cat_depth = [r['categorical_depth'] for r in all_results]
    bars = ax.bar(drugs, cat_depth, color=[colors[d] for d in drugs])
    ax.set_ylabel('Categorical Depth', fontsize=10, fontweight='bold')
    ax.set_title('Active Hierarchical Levels', fontsize=11, fontweight='bold')
    ax.set_ylim([0, 5])
    ax.grid(axis='y', alpha=0.3)
    for i, bar in enumerate(bars):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{cat_depth[i]}',
                ha='center', va='bottom', fontweight='bold', fontsize=9)
    
    # Plot 9: Compression per level (lithium example)
    ax = fig.add_subplot(gs[2, 2])
    stats = all_results[0]['level_statistics']  # Lithium
    levels = [s['level'] for s in stats]
    compressions = [s['compression_bits'] for s in stats]
    
    bars = ax.bar(levels, compressions, color=colors['lithium'], alpha=0.7, edgecolor='black')
    ax.set_xlabel('Hierarchical Level', fontweight='bold', fontsize=10)
    ax.set_ylabel('Compression (bits)', fontweight='bold', fontsize=10)
    ax.set_title('Lithium: Per-Level Compression', fontsize=11, fontweight='bold')
    ax.grid(axis='y', alpha=0.3)
    ax.invert_xaxis()
    
    # Save plot
    plot_path = output_dir / f"hierarchical_bmd_analysis_{timestamp}.png"
    plt.savefig(plot_path, dpi=300, bbox_inches='tight')
    print(f"Plot saved to: {plot_path}")
    
    plt.close()
    
    print("\n" + "="*80)
    print("VALIDATION COMPLETE")
    print("="*80)
    
    return all_results


if __name__ == "__main__":
    main()

