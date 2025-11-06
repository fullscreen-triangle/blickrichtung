"""
Kuramoto Oscillator Network
Simulates phase-locking dynamics in drug-perturbed cellular oscillator networks.
Models O2-mediated phase coherence and drug-induced phase shifts.
"""

import numpy as np
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from datetime import datetime
from pathlib import Path
from scipy.integrate import odeint


class KuramotoOscillatorNetwork:
    """Simulate coupled oscillator networks for consciousness programming."""
    
    def __init__(self, n_oscillators=100, coupling_strength=0.5):
        self.n = n_oscillators
        self.K = coupling_strength  # Coupling strength
        
        # Natural frequencies (Hz) - distributed around O2 baseline
        self.omega = np.random.normal(1000, 100, n_oscillators)  # 1 kHz ± 100 Hz
        
    def kuramoto_derivatives(self, theta, t, K, omega, drug_perturbation):
        """
        Kuramoto model differential equations with drug perturbation.
        dθ_i/dt = ω_i + (K/N) Σ sin(θ_j - θ_i) + drug_perturbation_i
        """
        N = len(theta)
        dtheta = omega.copy()
        
        for i in range(N):
            interaction = np.sum(np.sin(theta - theta[i]))
            dtheta[i] += (K / N) * interaction + drug_perturbation[i]
        
        return dtheta
    
    def calculate_order_parameter(self, theta):
        """
        Calculate Kuramoto order parameter r.
        r = |1/N Σ exp(i*θ_j)|
        r = 1: perfect synchronization
        r = 0: complete disorder
        """
        N = len(theta)
        z = np.mean(np.exp(1j * theta))
        r = np.abs(z)
        psi = np.angle(z)  # Global phase
        
        return r, psi
    
    def apply_drug_perturbation(self, drug_name, drug_params):
        """
        Apply drug-specific phase perturbation.
        Models how drugs shift oscillatory states.
        """
        if drug_name == 'lithium':
            # Lithium: Strong phase-locking enhancer (mood stabilizer)
            # Increases coupling, narrows frequency distribution
            perturbation = np.random.normal(0, 10, self.n)  # Small noise
            K_modified = self.K * 1.5  # Enhance coupling
            
        elif drug_name == 'dopamine':
            # Dopamine: Moderate phase accelerator
            # Shifts phases forward, increases frequencies
            perturbation = np.random.normal(50, 20, self.n)  # Positive shift
            K_modified = self.K * 1.2
            
        elif drug_name == 'serotonin':
            # Serotonin: Phase decelerator and smoother
            # Slows oscillations, increases coherence
            perturbation = np.random.normal(-30, 15, self.n)  # Negative shift
            K_modified = self.K * 1.3
            
        else:
            perturbation = np.zeros(self.n)
            K_modified = self.K
        
        return perturbation, K_modified
    
    def simulate_phase_locking(self, drug_name, t_max=10.0, dt=0.001):
        """
        Simulate phase-locking dynamics with drug perturbation.
        """
        t = np.arange(0, t_max, dt)
        
        # Initial phases (random)
        theta0 = np.random.uniform(0, 2*np.pi, self.n)
        
        # Apply drug perturbation
        drug_perturbation, K_modified = self.apply_drug_perturbation(
            drug_name, {}
        )
        
        # Solve Kuramoto equations
        theta = odeint(
            self.kuramoto_derivatives,
            theta0,
            t,
            args=(K_modified, self.omega, drug_perturbation)
        )
        
        # Calculate order parameter over time
        r_t = np.zeros(len(t))
        psi_t = np.zeros(len(t))
        
        for i, theta_snapshot in enumerate(theta):
            r_t[i], psi_t[i] = self.calculate_order_parameter(theta_snapshot)
        
        # Calculate phase coherence metrics
        r_mean = np.mean(r_t[-1000:])  # Average over last 1 second
        r_std = np.std(r_t[-1000:])
        
        # Calculate time to synchronization (r > 0.8)
        sync_indices = np.where(r_t > 0.8)[0]
        t_sync = t[sync_indices[0]] if len(sync_indices) > 0 else np.nan
        
        # Calculate frequency entrainment
        final_phases = theta[-1, :]
        phase_variance = np.var(final_phases)
        
        results = {
            'drug_name': drug_name,
            'coupling_strength_modified': float(K_modified),
            'mean_order_parameter': float(r_mean),
            'order_parameter_std': float(r_std),
            'time_to_sync_sec': float(t_sync) if not np.isnan(t_sync) else None,
            'final_phase_variance': float(phase_variance),
            'phase_coherence': float(r_mean),  # Same as order parameter
            'consciousness_lock_strength': float(r_mean * K_modified / self.K)
        }
        
        return results, t, r_t, theta
    
    def calculate_information_transfer(self, r_mean, K_modified):
        """
        Calculate information transfer rate based on phase coherence.
        Higher coherence = higher information capacity.
        """
        # Shannon capacity: C = B * log2(1 + SNR)
        # SNR ~ r^2 (coherence squared)
        # Bandwidth ~ K (coupling strength)
        
        SNR = r_mean ** 2 * 100  # Scale to reasonable SNR
        bandwidth = K_modified * 1000  # Hz
        
        capacity = bandwidth * np.log2(1 + SNR)
        
        return capacity


def main():
    """Main validation function."""
    print("=" * 80)
    print("Kuramoto Oscillator Network Simulation")
    print("Validating Drug-Induced Phase-Locking Dynamics")
    print("=" * 80)
    
    # Test molecules
    drugs = ['lithium', 'dopamine', 'serotonin']
    
    # Run simulations
    all_results = []
    all_time_series = {}
    
    for drug_name in drugs:
        print(f"\n{'='*60}")
        print(f"Simulating: {drug_name.upper()}")
        print(f"{'='*60}")
        
        # Initialize network
        network = KuramotoOscillatorNetwork(n_oscillators=100, coupling_strength=0.5)
        
        # Simulate
        result, t, r_t, theta = network.simulate_phase_locking(
            drug_name=drug_name,
            t_max=10.0
        )
        
        # Calculate information transfer
        info_capacity = network.calculate_information_transfer(
            result['mean_order_parameter'],
            result['coupling_strength_modified']
        )
        result['information_transfer_bits_per_sec'] = float(info_capacity)
        
        all_results.append(result)
        all_time_series[drug_name] = {'t': t, 'r_t': r_t, 'theta': theta}
        
        # Print results
        print(f"Modified Coupling Strength:    {result['coupling_strength_modified']:.3f}")
        print(f"Mean Order Parameter (r):      {result['mean_order_parameter']:.4f}")
        print(f"Order Parameter StdDev:        {result['order_parameter_std']:.4f}")
        if result['time_to_sync_sec'] is not None:
            print(f"Time to Synchronization:       {result['time_to_sync_sec']:.3f} s")
        else:
            print(f"Time to Synchronization:       No sync achieved")
        print(f"Final Phase Variance:          {result['final_phase_variance']:.4f}")
        print(f"Phase Coherence:               {result['phase_coherence']:.4f}")
        print(f"Consciousness Lock Strength:   {result['consciousness_lock_strength']:.4f}")
        print(f"Information Transfer:          {result['information_transfer_bits_per_sec']:.2e} bits/s")
    
    # Save results
    output_dir = Path("chatelier/src/computing/results")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Save JSON
    json_path = output_dir / f"kuramoto_network_results_{timestamp}.json"
    with open(json_path, 'w') as f:
        json.dump({
            'timestamp': timestamp,
            'theory': 'Kuramoto Phase-Locking Dynamics',
            'n_oscillators': 100,
            'results': all_results
        }, f, indent=2)
    
    print(f"\n{'='*60}")
    print(f"Results saved to: {json_path}")
    
    # Create visualizations
    fig = plt.figure(figsize=(16, 10))
    gs = fig.add_gridspec(3, 3, hspace=0.3, wspace=0.3)
    
    fig.suptitle('Kuramoto Oscillator Network: Drug-Induced Phase-Locking', 
                 fontsize=16, fontweight='bold')
    
    colors = {'lithium': '#2ecc71', 'dopamine': '#3498db', 'serotonin': '#9b59b6'}
    
    # Plot 1-3: Order parameter time series for each drug
    for idx, drug_name in enumerate(drugs):
        ax = fig.add_subplot(gs[0, idx])
        data = all_time_series[drug_name]
        ax.plot(data['t'], data['r_t'], color=colors[drug_name], linewidth=2)
        ax.set_xlabel('Time (s)', fontweight='bold')
        ax.set_ylabel('Order Parameter r', fontweight='bold')
        ax.set_title(f'{drug_name.capitalize()}: Phase Coherence', fontweight='bold')
        ax.set_ylim([0, 1])
        ax.axhline(0.8, color='red', linestyle='--', alpha=0.5, label='Sync threshold')
        ax.grid(alpha=0.3)
        ax.legend()
    
    # Plot 4: Comparison of mean order parameters
    ax = fig.add_subplot(gs[1, 0])
    order_params = [r['mean_order_parameter'] for r in all_results]
    bars = ax.bar(drugs, order_params, color=[colors[d] for d in drugs])
    ax.set_ylabel('Mean Order Parameter', fontsize=11, fontweight='bold')
    ax.set_title('Phase Coherence Comparison', fontsize=12, fontweight='bold')
    ax.set_ylim([0, 1])
    ax.grid(axis='y', alpha=0.3)
    for i, bar in enumerate(bars):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{order_params[i]:.3f}',
                ha='center', va='bottom', fontweight='bold')
    
    # Plot 5: Consciousness lock strength
    ax = fig.add_subplot(gs[1, 1])
    lock_strength = [r['consciousness_lock_strength'] for r in all_results]
    bars = ax.bar(drugs, lock_strength, color=[colors[d] for d in drugs])
    ax.set_ylabel('Lock Strength', fontsize=11, fontweight='bold')
    ax.set_title('Consciousness Lock Strength', fontsize=12, fontweight='bold')
    ax.grid(axis='y', alpha=0.3)
    for i, bar in enumerate(bars):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{lock_strength[i]:.3f}',
                ha='center', va='bottom', fontweight='bold')
    
    # Plot 6: Information transfer capacity
    ax = fig.add_subplot(gs[1, 2])
    info_transfer = [r['information_transfer_bits_per_sec'] for r in all_results]
    bars = ax.bar(drugs, info_transfer, color=[colors[d] for d in drugs])
    ax.set_ylabel('Info Transfer (bits/s)', fontsize=11, fontweight='bold')
    ax.set_title('Information Transfer Capacity', fontsize=12, fontweight='bold')
    ax.grid(axis='y', alpha=0.3)
    ax.ticklabel_format(style='scientific', axis='y', scilimits=(0,0))
    for i, bar in enumerate(bars):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{info_transfer[i]:.1e}',
                ha='center', va='bottom', fontweight='bold', fontsize=9)
    
    # Plot 7-9: Final phase distributions
    for idx, drug_name in enumerate(drugs):
        ax = fig.add_subplot(gs[2, idx])
        data = all_time_series[drug_name]
        final_phases = data['theta'][-1, :]
        ax.hist(final_phases, bins=30, color=colors[drug_name], alpha=0.7, edgecolor='black')
        ax.set_xlabel('Phase (radians)', fontweight='bold')
        ax.set_ylabel('Count', fontweight='bold')
        ax.set_title(f'{drug_name.capitalize()}: Final Phase Distribution', fontweight='bold')
        ax.grid(axis='y', alpha=0.3)
        
        # Add phase variance annotation
        variance = all_results[idx]['final_phase_variance']
        ax.text(0.95, 0.95, f'Var: {variance:.3f}',
                transform=ax.transAxes, ha='right', va='top',
                bbox=dict(boxstyle='round', facecolor='white', alpha=0.8),
                fontweight='bold')
    
    # Save plot
    plot_path = output_dir / f"kuramoto_network_analysis_{timestamp}.png"
    plt.savefig(plot_path, dpi=300, bbox_inches='tight')
    print(f"Plot saved to: {plot_path}")
    
    plt.close()
    
    print("\n" + "="*80)
    print("VALIDATION COMPLETE")
    print("="*80)
    
    return all_results


if __name__ == "__main__":
    main()

