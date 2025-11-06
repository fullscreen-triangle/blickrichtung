"""
BMD Phase Sorting
Models Biological Maxwell Demons sorting oscillatory endpoints by phase.
Implements information catalysis and entropy manipulation for consciousness programming.
"""

import numpy as np
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from datetime import datetime
from pathlib import Path
from scipy.stats import entropy as scipy_entropy


class BMDPhaseSorter:
    """Simulate BMD-mediated phase sorting and information catalysis."""
    
    def __init__(self, n_endpoints=10000, n_bmds=50):
        self.n_endpoints = n_endpoints
        self.n_bmds = n_bmds
        
        # BMD parameters
        self.kB = 1.380649e-23  # Boltzmann constant (J/K)
        self.T = 310.15  # Temperature (K)
        
    def generate_oscillatory_endpoints(self, base_freq=1000):
        """
        Generate random oscillatory endpoints.
        Each endpoint has: phase, voltage, timestamp
        """
        # Random phases (0 to 2π)
        phases = np.random.uniform(0, 2*np.pi, self.n_endpoints)
        
        # Voltages centered around resting potential (-75 mV)
        voltages = np.random.normal(-75, 10, self.n_endpoints)  # mV
        
        # Timestamps (uniformly distributed over 10 seconds)
        timestamps = np.random.uniform(0, 10, self.n_endpoints)
        
        # Oscillation frequencies (small variation around base)
        frequencies = np.random.normal(base_freq, 50, self.n_endpoints)
        
        endpoints = {
            'phases': phases,
            'voltages': voltages,
            'timestamps': timestamps,
            'frequencies': frequencies
        }
        
        return endpoints
    
    def bmd_phase_detection(self, phases, drug_phase_target):
        """
        BMD detects and sorts phases based on drug-specific target phase.
        Returns sorting decision for each endpoint.
        """
        # Calculate phase difference from target
        phase_diff = np.abs(phases - drug_phase_target)
        phase_diff = np.minimum(phase_diff, 2*np.pi - phase_diff)  # Circular distance
        
        # BMD decision: accept if within tolerance (π/4 = 45°)
        tolerance = np.pi / 4
        accepted = phase_diff < tolerance
        
        return accepted, phase_diff
    
    def calculate_entropy_change(self, before_distribution, after_distribution):
        """
        Calculate entropy change due to BMD sorting.
        ΔS = S_after - S_before
        """
        # Bin the distributions
        bins = 30
        hist_before, _ = np.histogram(before_distribution, bins=bins, density=True)
        hist_after, _ = np.histogram(after_distribution, bins=bins, density=True)
        
        # Add small constant to avoid log(0)
        hist_before = hist_before + 1e-10
        hist_after = hist_after + 1e-10
        
        # Normalize
        hist_before = hist_before / np.sum(hist_before)
        hist_after = hist_after / np.sum(hist_after)
        
        # Calculate Shannon entropy
        S_before = scipy_entropy(hist_before)
        S_after = scipy_entropy(hist_after)
        
        delta_S = S_after - S_before
        
        return delta_S, S_before, S_after
    
    def calculate_information_gain(self, acceptance_rate):
        """
        Calculate information gained by BMD sorting.
        I = -log2(p), where p is acceptance probability
        """
        p = acceptance_rate
        if p > 0 and p < 1:
            info_bits = -p * np.log2(p) - (1-p) * np.log2(1-p)
        else:
            info_bits = 0
        
        return info_bits
    
    def calculate_atp_cost(self, n_sorted, n_bmds):
        """
        Calculate ATP cost for BMD sorting operation.
        Each BMD requires ATP to maintain information processing.
        """
        # Cost per BMD per endpoint: ~1 ATP (simplified)
        atp_per_sort = 1.0
        total_atp = n_sorted * atp_per_sort
        
        # Cost per BMD to maintain active state
        atp_maintenance = n_bmds * 10  # ATP per BMD
        
        total_cost = total_atp + atp_maintenance
        
        return total_cost
    
    def simulate_drug_specific_sorting(self, drug_name, endpoints):
        """
        Simulate BMD sorting with drug-specific phase targets.
        """
        # Drug-specific phase targets
        if drug_name == 'lithium':
            # Lithium: Targets phases near 0 (stabilization)
            target_phase = 0.0
            
        elif drug_name == 'dopamine':
            # Dopamine: Targets phases near π/2 (activation)
            target_phase = np.pi / 2
            
        elif drug_name == 'serotonin':
            # Serotonin: Targets phases near π (inhibition)
            target_phase = np.pi
            
        else:
            target_phase = 0.0
        
        # BMD sorting
        accepted, phase_diff = self.bmd_phase_detection(
            endpoints['phases'],
            target_phase
        )
        
        # Separate accepted and rejected endpoints
        accepted_phases = endpoints['phases'][accepted]
        rejected_phases = endpoints['phases'][~accepted]
        
        accepted_voltages = endpoints['voltages'][accepted]
        rejected_voltages = endpoints['voltages'][~accepted]
        
        # Calculate metrics
        acceptance_rate = np.sum(accepted) / len(accepted)
        
        # Entropy change (in voltage space)
        delta_S_voltage, S_before_v, S_after_v = self.calculate_entropy_change(
            endpoints['voltages'],
            accepted_voltages if len(accepted_voltages) > 0 else endpoints['voltages']
        )
        
        # Entropy change (in phase space)
        delta_S_phase, S_before_p, S_after_p = self.calculate_entropy_change(
            endpoints['phases'],
            accepted_phases if len(accepted_phases) > 0 else endpoints['phases']
        )
        
        # Information gain
        info_bits = self.calculate_information_gain(acceptance_rate)
        
        # ATP cost
        atp_cost = self.calculate_atp_cost(np.sum(accepted), self.n_bmds)
        
        # Consciousness programming efficiency
        # High info, low entropy increase = efficient programming
        programming_efficiency = info_bits / (np.abs(delta_S_phase) + 1e-6)
        
        results = {
            'drug_name': drug_name,
            'target_phase_radians': float(target_phase),
            'n_endpoints_total': int(self.n_endpoints),
            'n_endpoints_accepted': int(np.sum(accepted)),
            'n_endpoints_rejected': int(np.sum(~accepted)),
            'acceptance_rate': float(acceptance_rate),
            'entropy_before_voltage': float(S_before_v),
            'entropy_after_voltage': float(S_after_v),
            'entropy_change_voltage': float(delta_S_voltage),
            'entropy_before_phase': float(S_before_p),
            'entropy_after_phase': float(S_after_p),
            'entropy_change_phase': float(delta_S_phase),
            'information_gain_bits': float(info_bits),
            'atp_cost': float(atp_cost),
            'atp_per_endpoint': float(atp_cost / np.sum(accepted)) if np.sum(accepted) > 0 else 0,
            'programming_efficiency': float(programming_efficiency),
            'mean_phase_diff': float(np.mean(phase_diff))
        }
        
        sorting_data = {
            'accepted_phases': accepted_phases,
            'rejected_phases': rejected_phases,
            'accepted_voltages': accepted_voltages,
            'rejected_voltages': rejected_voltages,
            'phase_diff': phase_diff
        }
        
        return results, sorting_data


def main():
    """Main validation function."""
    print("=" * 80)
    print("BMD Phase Sorting Analysis")
    print("Validating Biological Maxwell Demon Information Catalysis")
    print("=" * 80)
    
    # Test molecules
    drugs = ['lithium', 'dopamine', 'serotonin']
    
    # Run simulations
    all_results = []
    all_sorting_data = {}
    
    for drug_name in drugs:
        print(f"\n{'='*60}")
        print(f"Simulating: {drug_name.upper()}")
        print(f"{'='*60}")
        
        # Initialize sorter
        sorter = BMDPhaseSorter(n_endpoints=10000, n_bmds=50)
        
        # Generate endpoints
        endpoints = sorter.generate_oscillatory_endpoints(base_freq=1000)
        
        # Simulate sorting
        result, sorting_data = sorter.simulate_drug_specific_sorting(drug_name, endpoints)
        
        all_results.append(result)
        all_sorting_data[drug_name] = sorting_data
        
        # Print results
        print(f"Target Phase:                  {result['target_phase_radians']:.4f} rad ({np.degrees(result['target_phase_radians']):.1f}°)")
        print(f"Endpoints Accepted:            {result['n_endpoints_accepted']} / {result['n_endpoints_total']}")
        print(f"Acceptance Rate:               {result['acceptance_rate']:.4f}")
        print(f"Entropy Change (Phase):        {result['entropy_change_phase']:.4f}")
        print(f"Entropy Change (Voltage):      {result['entropy_change_voltage']:.4f}")
        print(f"Information Gain:              {result['information_gain_bits']:.4f} bits")
        print(f"ATP Cost:                      {result['atp_cost']:.1f} ATP")
        print(f"ATP per Endpoint:              {result['atp_per_endpoint']:.3f} ATP")
        print(f"Programming Efficiency:        {result['programming_efficiency']:.4f}")
    
    # Save results
    output_dir = Path("chatelier/src/computing/results")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Save JSON
    json_path = output_dir / f"bmd_phase_sorting_results_{timestamp}.json"
    with open(json_path, 'w') as f:
        json.dump({
            'timestamp': timestamp,
            'theory': 'BMD Phase Sorting and Information Catalysis',
            'n_endpoints': 10000,
            'n_bmds': 50,
            'results': all_results
        }, f, indent=2)
    
    print(f"\n{'='*60}")
    print(f"Results saved to: {json_path}")
    
    # Create visualizations
    fig = plt.figure(figsize=(16, 12))
    gs = fig.add_gridspec(3, 3, hspace=0.35, wspace=0.3)
    
    fig.suptitle('BMD Phase Sorting: Information Catalysis for Consciousness Programming', 
                 fontsize=15, fontweight='bold')
    
    colors = {'lithium': '#2ecc71', 'dopamine': '#3498db', 'serotonin': '#9b59b6'}
    
    # Plot 1: Acceptance rates
    ax = fig.add_subplot(gs[0, 0])
    acceptance = [r['acceptance_rate'] for r in all_results]
    bars = ax.bar(drugs, acceptance, color=[colors[d] for d in drugs])
    ax.set_ylabel('Acceptance Rate', fontsize=10, fontweight='bold')
    ax.set_title('BMD Endpoint Acceptance Rate', fontsize=11, fontweight='bold')
    ax.set_ylim([0, 1])
    ax.grid(axis='y', alpha=0.3)
    for i, bar in enumerate(bars):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{acceptance[i]:.3f}',
                ha='center', va='bottom', fontweight='bold', fontsize=9)
    
    # Plot 2: Information gain
    ax = fig.add_subplot(gs[0, 1])
    info_gain = [r['information_gain_bits'] for r in all_results]
    bars = ax.bar(drugs, info_gain, color=[colors[d] for d in drugs])
    ax.set_ylabel('Information Gain (bits)', fontsize=10, fontweight='bold')
    ax.set_title('Information Catalysis Efficiency', fontsize=11, fontweight='bold')
    ax.grid(axis='y', alpha=0.3)
    for i, bar in enumerate(bars):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{info_gain[i]:.3f}',
                ha='center', va='bottom', fontweight='bold', fontsize=9)
    
    # Plot 3: Programming efficiency
    ax = fig.add_subplot(gs[0, 2])
    efficiency = [r['programming_efficiency'] for r in all_results]
    bars = ax.bar(drugs, efficiency, color=[colors[d] for d in drugs])
    ax.set_ylabel('Programming Efficiency', fontsize=10, fontweight='bold')
    ax.set_title('Consciousness Programming Efficiency', fontsize=11, fontweight='bold')
    ax.grid(axis='y', alpha=0.3)
    for i, bar in enumerate(bars):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{efficiency[i]:.2f}',
                ha='center', va='bottom', fontweight='bold', fontsize=9)
    
    # Plot 4-6: Phase distributions (before/after sorting)
    for idx, drug_name in enumerate(drugs):
        ax = fig.add_subplot(gs[1, idx], projection='polar')
        data = all_sorting_data[drug_name]
        
        # Plot accepted phases
        ax.scatter(data['accepted_phases'], np.ones_like(data['accepted_phases']),
                  c=colors[drug_name], alpha=0.3, s=5, label='Accepted')
        
        # Plot rejected phases
        ax.scatter(data['rejected_phases'], np.ones_like(data['rejected_phases']) * 0.5,
                  c='red', alpha=0.2, s=5, label='Rejected')
        
        # Mark target phase
        target = all_results[idx]['target_phase_radians']
        ax.plot([target, target], [0, 1.2], 'k--', linewidth=3, label='Target')
        
        ax.set_ylim([0, 1.2])
        ax.set_title(f'{drug_name.capitalize()}: Phase Sorting', 
                    fontweight='bold', fontsize=11, pad=20)
        ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1), fontsize=8)
    
    # Plot 7: Entropy changes
    ax = fig.add_subplot(gs[2, 0])
    entropy_phase = [r['entropy_change_phase'] for r in all_results]
    entropy_voltage = [r['entropy_change_voltage'] for r in all_results]
    
    x = np.arange(len(drugs))
    width = 0.35
    
    bars1 = ax.bar(x - width/2, entropy_phase, width, label='Phase', 
                   color=[colors[d] for d in drugs], alpha=0.8)
    bars2 = ax.bar(x + width/2, entropy_voltage, width, label='Voltage',
                   color=[colors[d] for d in drugs], alpha=0.5)
    
    ax.set_ylabel('Entropy Change', fontsize=10, fontweight='bold')
    ax.set_title('Entropy Reduction by BMD Sorting', fontsize=11, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(drugs)
    ax.axhline(0, color='black', linestyle='-', linewidth=0.8)
    ax.legend(fontsize=9)
    ax.grid(axis='y', alpha=0.3)
    
    # Plot 8: ATP cost
    ax = fig.add_subplot(gs[2, 1])
    atp_per_endpoint = [r['atp_per_endpoint'] for r in all_results]
    bars = ax.bar(drugs, atp_per_endpoint, color=[colors[d] for d in drugs])
    ax.set_ylabel('ATP per Endpoint', fontsize=10, fontweight='bold')
    ax.set_title('Thermodynamic Cost of Information Catalysis', fontsize=11, fontweight='bold')
    ax.grid(axis='y', alpha=0.3)
    for i, bar in enumerate(bars):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{atp_per_endpoint[i]:.3f}',
                ha='center', va='bottom', fontweight='bold', fontsize=9)
    
    # Plot 9: Phase difference distribution for lithium (example)
    ax = fig.add_subplot(gs[2, 2])
    phase_diff = all_sorting_data['lithium']['phase_diff']
    ax.hist(phase_diff, bins=40, color=colors['lithium'], alpha=0.7, edgecolor='black')
    ax.axvline(np.pi/4, color='red', linestyle='--', linewidth=2, label='Tolerance')
    ax.set_xlabel('Phase Difference (rad)', fontweight='bold', fontsize=10)
    ax.set_ylabel('Count', fontweight='bold', fontsize=10)
    ax.set_title('Phase Difference Distribution (Lithium)', fontsize=11, fontweight='bold')
    ax.legend(fontsize=9)
    ax.grid(axis='y', alpha=0.3)
    
    # Save plot
    plot_path = output_dir / f"bmd_phase_sorting_analysis_{timestamp}.png"
    plt.savefig(plot_path, dpi=300, bbox_inches='tight')
    print(f"Plot saved to: {plot_path}")
    
    plt.close()
    
    print("\n" + "="*80)
    print("VALIDATION COMPLETE")
    print("="*80)
    
    return all_results


if __name__ == "__main__":
    main()

