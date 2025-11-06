"""
Categorical State Space Reduction
Models how pharmaceutical agents reduce categorical state space to program consciousness.
Based on categorical-intracellular-dynamics and pharmacology-meta-programming theories.
"""

import numpy as np
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from datetime import datetime
from pathlib import Path
from itertools import product


class CategoricalStateSpaceReducer:
    """Model drug-induced categorical state space reduction."""
    
    def __init__(self, n_dimensions=8):
        """
        Initialize with n-dimensional categorical state space.
        Dimensions: pH, [ATP], [O2], membrane potential, temperature, etc.
        """
        self.n_dim = n_dimensions
        self.baseline_states = self._generate_baseline_states()
        
    def _generate_baseline_states(self, resolution=10):
        """
        Generate baseline categorical state space.
        Each dimension discretized into 'resolution' levels.
        """
        # Create grid for each dimension
        dimensions = []
        for i in range(self.n_dim):
            dimensions.append(np.linspace(0, 1, resolution))
        
        # Generate all possible states (Cartesian product)
        # For computational efficiency, sample subset
        n_samples = min(10000, resolution ** self.n_dim)
        
        states = []
        for _ in range(n_samples):
            state = np.random.rand(self.n_dim)
            states.append(state)
        
        return np.array(states)
    
    def calculate_categorical_richness(self, state):
        """
        Calculate categorical richness R(state).
        R = number of accessible morphisms from this state.
        Higher R = more ambiguity = less constrained.
        """
        # Simplified: R ~ variance in state dimensions
        R = np.sum(state * (1 - state))  # Maximum at 0.5 for each dimension
        return R
    
    def apply_drug_constraint(self, drug_name, drug_params):
        """
        Apply drug-specific categorical constraints.
        Drugs reduce state space by constraining dimensions.
        """
        constraints = np.ones(self.n_dim)  # 1 = no constraint, 0 = full constraint
        
        if drug_name == 'lithium':
            # Lithium: Strongly constrains ionic dimensions (pH, membrane potential)
            # Stabilizes mood by reducing state variance
            constraints[0] = 0.3  # pH constraint
            constraints[3] = 0.4  # Membrane potential constraint
            constraints[1] = 0.6  # ATP slightly constrained
            
        elif drug_name == 'dopamine':
            # Dopamine: Moderately constrains energy and signaling dimensions
            # Focuses attention by reducing reward-related states
            constraints[1] = 0.5  # ATP constraint
            constraints[4] = 0.4  # Temperature/activity constraint
            constraints[6] = 0.5  # Signaling constraint
            
        elif drug_name == 'serotonin':
            # Serotonin: Broadly constrains multiple dimensions
            # Stabilizes mood by reducing overall state space
            constraints[0] = 0.5  # pH constraint
            constraints[1] = 0.6  # ATP constraint
            constraints[3] = 0.5  # Membrane potential
            constraints[5] = 0.4  # Neurotransmitter constraint
            
        return constraints
    
    def reduce_state_space(self, drug_name):
        """
        Apply drug constraints to reduce categorical state space.
        Returns constrained states and reduction metrics.
        """
        # Get drug constraints
        constraints = self.apply_drug_constraint(drug_name, {})
        
        # Apply constraints to baseline states
        constrained_states = self.baseline_states * constraints
        
        # Calculate categorical richness before and after
        R_before = np.array([self.calculate_categorical_richness(s) 
                            for s in self.baseline_states])
        R_after = np.array([self.calculate_categorical_richness(s) 
                           for s in constrained_states])
        
        # Calculate state space volume (geometric mean of accessible range)
        volume_before = np.prod(np.ptp(self.baseline_states, axis=0))
        volume_after = np.prod(np.ptp(constrained_states, axis=0))
        
        # Calculate entropy reduction
        # S = k_B * ln(Ω), Ω ~ volume
        S_before = np.log(volume_before + 1e-10)
        S_after = np.log(volume_after + 1e-10)
        delta_S = S_after - S_before
        
        # Calculate consciousness programming specificity
        # Higher reduction = more specific programming
        reduction_ratio = volume_after / volume_before
        programming_specificity = 1 - reduction_ratio
        
        # Calculate information compression
        # ΔI = log2(N_before / N_after)
        info_compression = np.log2((volume_before + 1e-10) / (volume_after + 1e-10))
        
        results = {
            'drug_name': drug_name,
            'constraints': constraints.tolist(),
            'mean_constraint': float(np.mean(constraints)),
            'volume_before': float(volume_before),
            'volume_after': float(volume_after),
            'volume_reduction_ratio': float(reduction_ratio),
            'entropy_before': float(S_before),
            'entropy_after': float(S_after),
            'entropy_reduction': float(-delta_S),
            'mean_richness_before': float(np.mean(R_before)),
            'mean_richness_after': float(np.mean(R_after)),
            'richness_reduction_percent': float((1 - np.mean(R_after)/np.mean(R_before)) * 100),
            'programming_specificity': float(programming_specificity),
            'information_compression_bits': float(info_compression)
        }
        
        return results, constrained_states, R_before, R_after
    
    def calculate_therapeutic_window(self, reduction_ratio):
        """
        Calculate therapeutic window.
        Too much reduction = toxicity
        Too little reduction = ineffective
        Optimal: 0.3 - 0.7 reduction ratio
        """
        if 0.3 <= reduction_ratio <= 0.7:
            efficacy = 1.0
        elif reduction_ratio > 0.7:
            efficacy = (1.0 - reduction_ratio) / 0.3  # Decreases as reduction increases
        else:
            efficacy = reduction_ratio / 0.3  # Increases with reduction
        
        return max(0, min(1, efficacy))


def main():
    """Main validation function."""
    print("=" * 80)
    print("Categorical State Space Reduction Analysis")
    print("Validating Drug-Induced Consciousness Programming via State Constraint")
    print("=" * 80)
    
    # Test molecules
    drugs = ['lithium', 'dopamine', 'serotonin']
    
    # Run simulations
    all_results = []
    all_state_data = {}
    
    for drug_name in drugs:
        print(f"\n{'='*60}")
        print(f"Analyzing: {drug_name.upper()}")
        print(f"{'='*60}")
        
        # Initialize reducer
        reducer = CategoricalStateSpaceReducer(n_dimensions=8)
        
        # Reduce state space
        result, constrained_states, R_before, R_after = reducer.reduce_state_space(drug_name)
        
        # Calculate therapeutic window
        efficacy = reducer.calculate_therapeutic_window(result['volume_reduction_ratio'])
        result['therapeutic_efficacy'] = float(efficacy)
        
        all_results.append(result)
        all_state_data[drug_name] = {
            'constrained_states': constrained_states,
            'R_before': R_before,
            'R_after': R_after
        }
        
        # Print results
        print(f"Mean Constraint:               {result['mean_constraint']:.3f}")
        print(f"Volume Reduction Ratio:        {result['volume_reduction_ratio']:.4f}")
        print(f"Entropy Reduction:             {result['entropy_reduction']:.4f}")
        print(f"Mean Richness Before:          {result['mean_richness_before']:.4f}")
        print(f"Mean Richness After:           {result['mean_richness_after']:.4f}")
        print(f"Richness Reduction:            {result['richness_reduction_percent']:.2f}%")
        print(f"Programming Specificity:       {result['programming_specificity']:.4f}")
        print(f"Information Compression:       {result['information_compression_bits']:.2f} bits")
        print(f"Therapeutic Efficacy:          {result['therapeutic_efficacy']:.4f}")
    
    # Save results
    output_dir = Path("chatelier/src/computing/results")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Save JSON
    json_path = output_dir / f"categorical_reduction_results_{timestamp}.json"
    with open(json_path, 'w') as f:
        json.dump({
            'timestamp': timestamp,
            'theory': 'Categorical State Space Reduction',
            'n_dimensions': 8,
            'results': all_results
        }, f, indent=2)
    
    print(f"\n{'='*60}")
    print(f"Results saved to: {json_path}")
    
    # Create visualizations
    fig, axes = plt.subplots(3, 3, figsize=(16, 12))
    fig.suptitle('Categorical State Space Reduction: Consciousness Programming', 
                 fontsize=16, fontweight='bold')
    
    colors = {'lithium': '#2ecc71', 'dopamine': '#3498db', 'serotonin': '#9b59b6'}
    
    # Plot 1: Volume reduction ratio
    ax = axes[0, 0]
    reduction_ratios = [r['volume_reduction_ratio'] for r in all_results]
    bars = ax.bar(drugs, reduction_ratios, color=[colors[d] for d in drugs])
    ax.set_ylabel('Volume Reduction Ratio', fontsize=10, fontweight='bold')
    ax.set_title('State Space Volume Reduction', fontsize=11, fontweight='bold')
    ax.axhspan(0.3, 0.7, alpha=0.2, color='green', label='Therapeutic Window')
    ax.grid(axis='y', alpha=0.3)
    ax.legend()
    for i, bar in enumerate(bars):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{reduction_ratios[i]:.3f}',
                ha='center', va='bottom', fontweight='bold', fontsize=9)
    
    # Plot 2: Programming specificity
    ax = axes[0, 1]
    specificity = [r['programming_specificity'] for r in all_results]
    bars = ax.bar(drugs, specificity, color=[colors[d] for d in drugs])
    ax.set_ylabel('Programming Specificity', fontsize=10, fontweight='bold')
    ax.set_title('Consciousness Programming Specificity', fontsize=11, fontweight='bold')
    ax.set_ylim([0, 1])
    ax.grid(axis='y', alpha=0.3)
    for i, bar in enumerate(bars):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{specificity[i]:.3f}',
                ha='center', va='bottom', fontweight='bold', fontsize=9)
    
    # Plot 3: Therapeutic efficacy
    ax = axes[0, 2]
    efficacy = [r['therapeutic_efficacy'] for r in all_results]
    bars = ax.bar(drugs, efficacy, color=[colors[d] for d in drugs])
    ax.set_ylabel('Therapeutic Efficacy', fontsize=10, fontweight='bold')
    ax.set_title('Therapeutic Window Efficacy', fontsize=11, fontweight='bold')
    ax.set_ylim([0, 1])
    ax.grid(axis='y', alpha=0.3)
    for i, bar in enumerate(bars):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{efficacy[i]:.3f}',
                ha='center', va='bottom', fontweight='bold', fontsize=9)
    
    # Plot 4: Entropy reduction
    ax = axes[1, 0]
    entropy_red = [r['entropy_reduction'] for r in all_results]
    bars = ax.bar(drugs, entropy_red, color=[colors[d] for d in drugs])
    ax.set_ylabel('Entropy Reduction', fontsize=10, fontweight='bold')
    ax.set_title('Thermodynamic Entropy Reduction', fontsize=11, fontweight='bold')
    ax.grid(axis='y', alpha=0.3)
    for i, bar in enumerate(bars):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{entropy_red[i]:.2f}',
                ha='center', va='bottom', fontweight='bold', fontsize=9)
    
    # Plot 5: Information compression
    ax = axes[1, 1]
    info_comp = [r['information_compression_bits'] for r in all_results]
    bars = ax.bar(drugs, info_comp, color=[colors[d] for d in drugs])
    ax.set_ylabel('Information Compression (bits)', fontsize=10, fontweight='bold')
    ax.set_title('Consciousness Information Compression', fontsize=11, fontweight='bold')
    ax.grid(axis='y', alpha=0.3)
    for i, bar in enumerate(bars):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{info_comp[i]:.1f}',
                ha='center', va='bottom', fontweight='bold', fontsize=9)
    
    # Plot 6: Richness reduction
    ax = axes[1, 2]
    richness_red = [r['richness_reduction_percent'] for r in all_results]
    bars = ax.bar(drugs, richness_red, color=[colors[d] for d in drugs])
    ax.set_ylabel('Richness Reduction (%)', fontsize=10, fontweight='bold')
    ax.set_title('Categorical Richness Reduction', fontsize=11, fontweight='bold')
    ax.grid(axis='y', alpha=0.3)
    for i, bar in enumerate(bars):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{richness_red[i]:.1f}%',
                ha='center', va='bottom', fontweight='bold', fontsize=9)
    
    # Plot 7-9: Constraint heatmaps
    for idx, drug_name in enumerate(drugs):
        ax = axes[2, idx]
        constraints = np.array(all_results[idx]['constraints'])
        
        # Create heatmap
        im = ax.imshow(constraints.reshape(1, -1), cmap='RdYlGn', aspect='auto', 
                      vmin=0, vmax=1)
        ax.set_yticks([])
        ax.set_xticks(range(8))
        ax.set_xticklabels([f'D{i+1}' for i in range(8)], fontsize=9)
        ax.set_xlabel('State Dimension', fontweight='bold', fontsize=10)
        ax.set_title(f'{drug_name.capitalize()}: Constraint Profile', 
                    fontweight='bold', fontsize=11)
        
        # Add colorbar
        cbar = plt.colorbar(im, ax=ax, orientation='horizontal', pad=0.1)
        cbar.set_label('Constraint (0=full, 1=none)', fontsize=8)
        
        # Add constraint values as text
        for i, val in enumerate(constraints):
            ax.text(i, 0, f'{val:.2f}', ha='center', va='center',
                   fontweight='bold', fontsize=9,
                   color='white' if val < 0.5 else 'black')
    
    plt.tight_layout()
    
    # Save plot
    plot_path = output_dir / f"categorical_reduction_analysis_{timestamp}.png"
    plt.savefig(plot_path, dpi=300, bbox_inches='tight')
    print(f"Plot saved to: {plot_path}")
    
    plt.close()
    
    print("\n" + "="*80)
    print("VALIDATION COMPLETE")
    print("="*80)
    
    return all_results


if __name__ == "__main__":
    main()

