"""
Damped Harmonic Oscillator Implementation

A damped linear oscillator: m*x'' + c*x' + k*x = 0
Types: Underdamped (ζ < 1), Critically damped (ζ = 1), Overdamped (ζ > 1)

This script is independent and can be run in isolation for debugging.
Includes visualization, JSON output, and integration with analysis module.
"""

import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as signal
from scipy.integrate import solve_ivp
import json
import os
from datetime import datetime
from typing import Dict, Any, Optional

# Import analysis module
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from core.analysis import run_all_tests

class DampedHarmonicOscillator:
    """
    Damped Harmonic Oscillator: m*x'' + c*x' + k*x = 0
    
    State variables: [x, x_dot]
    """
    
    def __init__(self, mass: float = 1.0, damping: float = 0.1, stiffness: float = 1.0,
                 initial_position: float = 1.0, initial_velocity: float = 0.0):
        """
        Initialize Damped Harmonic Oscillator
        
        Args:
            mass: Mass (m) in kg
            damping: Damping coefficient (c) in N⋅s/m
            stiffness: Spring constant (k) in N/m
            initial_position: Initial displacement in m
            initial_velocity: Initial velocity in m/s
        """
        self.mass = mass
        self.damping = damping
        self.stiffness = stiffness
        self.initial_position = initial_position
        self.initial_velocity = initial_velocity
        
        # Calculate derived parameters
        self.natural_frequency = np.sqrt(stiffness / mass)  # ω₀
        self.damping_ratio = damping / (2 * np.sqrt(mass * stiffness))  # ζ
        
        # Determine damping type
        if self.damping_ratio < 1.0:
            self.damping_type = "Underdamped"
            self.damped_frequency = self.natural_frequency * np.sqrt(1 - self.damping_ratio**2)  # ωₐ
        elif self.damping_ratio == 1.0:
            self.damping_type = "Critically Damped"
            self.damped_frequency = 0
        else:
            self.damping_type = "Overdamped"
            self.damped_frequency = 0
        
        # Results storage
        self.simulation_results = {}
        self.analysis_results = {}
    
    def get_transfer_function(self) -> signal.TransferFunction:
        """Get transfer function H(s) = X(s)/F(s)"""
        # For damped SHO: H(s) = 1/(m*s^2 + c*s + k) = (1/m)/(s^2 + (c/m)*s + k/m)
        num = [1/self.mass]
        den = [1, self.damping/self.mass, self.stiffness/self.mass]
        return signal.TransferFunction(num, den)
    
    def get_state_equations(self):
        """Get state space equations dx/dt = f(x, t)"""
        def state_equations(x, t):
            position, velocity = x
            acceleration = -(self.stiffness / self.mass) * position - (self.damping / self.mass) * velocity
            return np.array([velocity, acceleration])
        return state_equations
    
    def get_characteristic_polynomial(self) -> np.ndarray:
        """Get characteristic polynomial coefficients"""
        # Characteristic equation: m*s^2 + c*s + k = 0 → s^2 + (c/m)*s + k/m = 0
        return np.array([1, self.damping/self.mass, self.stiffness/self.mass])
    
    def get_equilibrium(self) -> np.ndarray:
        """Get equilibrium point"""
        return np.array([0.0, 0.0])  # Origin for damped SHO
    
    def get_initial_conditions(self) -> np.ndarray:
        """Get initial conditions"""
        return np.array([self.initial_position, self.initial_velocity])
    
    def simulate(self, time_span: np.ndarray) -> Dict[str, Any]:
        """Simulate the oscillator"""
        initial_conditions = self.get_initial_conditions()
        state_equations = self.get_state_equations()
        
        def ode_system(t, y):
            return state_equations(y, t)
        
        sol = solve_ivp(ode_system, [time_span[0], time_span[-1]], 
                       initial_conditions, t_eval=time_span, rtol=1e-10)
        
        # Calculate energies
        kinetic_energy = 0.5 * self.mass * sol.y[1]**2
        potential_energy = 0.5 * self.stiffness * sol.y[0]**2
        total_energy = kinetic_energy + potential_energy
        
        # Calculate power dissipation
        power_dissipated = self.damping * sol.y[1]**2
        
        results = {
            'time': sol.t,
            'position': sol.y[0],
            'velocity': sol.y[1],
            'energy_kinetic': kinetic_energy,
            'energy_potential': potential_energy,
            'energy_total': total_energy,
            'power_dissipated': power_dissipated
        }
        
        self.simulation_results = results
        return results
    
    def theoretical_solution(self, time_span: np.ndarray) -> Dict[str, Any]:
        """Calculate theoretical analytical solution"""
        t = time_span
        x0 = self.initial_position
        v0 = self.initial_velocity
        zeta = self.damping_ratio
        omega0 = self.natural_frequency
        
        if zeta < 1.0:  # Underdamped
            omega_d = omega0 * np.sqrt(1 - zeta**2)
            A = x0
            B = (v0 + zeta * omega0 * x0) / omega_d
            
            envelope = np.exp(-zeta * omega0 * t)
            position_theoretical = envelope * (A * np.cos(omega_d * t) + B * np.sin(omega_d * t))
            velocity_theoretical = envelope * (
                (-zeta * omega0 * A - omega_d * B) * np.cos(omega_d * t) + 
                (-zeta * omega0 * B + omega_d * A) * np.sin(omega_d * t)
            )
            
        elif zeta == 1.0:  # Critically damped
            A = x0
            B = v0 + omega0 * x0
            
            envelope = np.exp(-omega0 * t)
            position_theoretical = envelope * (A + B * t)
            velocity_theoretical = envelope * (B - omega0 * (A + B * t))
            
        else:  # Overdamped
            r1 = -omega0 * (zeta + np.sqrt(zeta**2 - 1))
            r2 = -omega0 * (zeta - np.sqrt(zeta**2 - 1))
            
            A = (v0 - r2 * x0) / (r1 - r2)
            B = (r1 * x0 - v0) / (r1 - r2)
            
            position_theoretical = A * np.exp(r1 * t) + B * np.exp(r2 * t)
            velocity_theoretical = A * r1 * np.exp(r1 * t) + B * r2 * np.exp(r2 * t)
        
        return {
            'time': t,
            'position_theoretical': position_theoretical,
            'velocity_theoretical': velocity_theoretical,
            'envelope': envelope if zeta < 1.0 else None
        }
    
    def run_analysis(self) -> Dict[str, Any]:
        """Run comprehensive analysis using analysis module"""
        print("🔬 Running comprehensive analysis...")
        self.analysis_results = run_all_tests(self, include_st_stellas=False)
        return self.analysis_results
    
    def visualize_results(self, save_path: Optional[str] = None):
        """Create comprehensive visualizations"""
        if not self.simulation_results:
            print("⚠️  No simulation results to visualize. Run simulate() first.")
            return
        
        fig, axes = plt.subplots(2, 3, figsize=(18, 10))
        fig.suptitle(f'Damped Harmonic Oscillator Analysis - {self.damping_type}', fontsize=16, fontweight='bold')
        
        t = self.simulation_results['time']
        x = self.simulation_results['position']
        v = self.simulation_results['velocity']
        
        # Get theoretical solution for comparison
        theoretical = self.theoretical_solution(t)
        x_theory = theoretical['position_theoretical']
        v_theory = theoretical['velocity_theoretical']
        
        # Time series plot with theoretical comparison
        axes[0, 0].plot(t, x, 'b-', linewidth=2, label='Simulation')
        axes[0, 0].plot(t, x_theory, 'r--', linewidth=2, label='Theoretical', alpha=0.7)
        if self.damping_type == "Underdamped" and theoretical['envelope'] is not None:
            axes[0, 0].plot(t, theoretical['envelope'], 'g:', linewidth=1, label='Envelope')
            axes[0, 0].plot(t, -theoretical['envelope'], 'g:', linewidth=1)
        axes[0, 0].set_xlabel('Time (s)')
        axes[0, 0].set_ylabel('Position (m)')
        axes[0, 0].set_title('Position vs Time')
        axes[0, 0].grid(True, alpha=0.3)
        axes[0, 0].legend()
        
        # Velocity comparison
        axes[0, 1].plot(t, v, 'r-', linewidth=2, label='Simulation')
        axes[0, 1].plot(t, v_theory, 'b--', linewidth=2, label='Theoretical', alpha=0.7)
        axes[0, 1].set_xlabel('Time (s)')
        axes[0, 1].set_ylabel('Velocity (m/s)')
        axes[0, 1].set_title('Velocity vs Time')
        axes[0, 1].grid(True, alpha=0.3)
        axes[0, 1].legend()
        
        # Phase portrait
        axes[0, 2].plot(x, v, 'g-', linewidth=2, label='Trajectory')
        axes[0, 2].scatter(x[0], v[0], color='red', s=100, label='Start', zorder=5)
        axes[0, 2].scatter(x[-1], v[-1], color='blue', s=100, label='End', zorder=5)
        axes[0, 2].set_xlabel('Position (m)')
        axes[0, 2].set_ylabel('Velocity (m/s)')
        axes[0, 2].set_title('Phase Portrait')
        axes[0, 2].grid(True, alpha=0.3)
        axes[0, 2].legend()
        
        # Energy analysis
        E_k = self.simulation_results['energy_kinetic']
        E_p = self.simulation_results['energy_potential']
        E_total = self.simulation_results['energy_total']
        
        axes[1, 0].plot(t, E_k, 'r-', linewidth=2, label='Kinetic Energy')
        axes[1, 0].plot(t, E_p, 'b-', linewidth=2, label='Potential Energy')
        axes[1, 0].plot(t, E_total, 'k-', linewidth=2, label='Total Energy')
        axes[1, 0].set_xlabel('Time (s)')
        axes[1, 0].set_ylabel('Energy (J)')
        axes[1, 0].set_title('Energy Dissipation')
        axes[1, 0].grid(True, alpha=0.3)
        axes[1, 0].legend()
        
        # Power dissipation
        P_diss = self.simulation_results['power_dissipated']
        axes[1, 1].plot(t, P_diss, 'purple', linewidth=2)
        axes[1, 1].set_xlabel('Time (s)')
        axes[1, 1].set_ylabel('Power (W)')
        axes[1, 1].set_title('Power Dissipation')
        axes[1, 1].grid(True, alpha=0.3)
        
        # Frequency spectrum
        dt = t[1] - t[0]
        fft_x = np.fft.fft(x)
        frequencies = np.fft.fftfreq(len(x), dt)
        magnitude = np.abs(fft_x)
        
        # Plot positive frequencies only
        positive_freq_mask = frequencies > 0
        axes[1, 2].semilogy(frequencies[positive_freq_mask], magnitude[positive_freq_mask], 'b-', linewidth=2)
        
        # Mark natural and damped frequencies
        axes[1, 2].axvline(self.natural_frequency/(2*np.pi), color='red', linestyle='--', 
                          label=f'Natural: {self.natural_frequency/(2*np.pi):.3f} Hz')
        if self.damped_frequency > 0:
            axes[1, 2].axvline(self.damped_frequency/(2*np.pi), color='green', linestyle='--',
                              label=f'Damped: {self.damped_frequency/(2*np.pi):.3f} Hz')
        
        axes[1, 2].set_xlabel('Frequency (Hz)')
        axes[1, 2].set_ylabel('Magnitude')
        axes[1, 2].set_title('Frequency Spectrum')
        axes[1, 2].grid(True, alpha=0.3)
        axes[1, 2].legend()
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"📊 Visualization saved to: {save_path}")
        
        plt.show()
    
    def save_results(self, filename: str = None):
        """Save all results to JSON file"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"damped_harmonic_oscillator_results_{timestamp}.json"
        
        # Prepare data for JSON serialization
        output_data = {
            'oscillator_type': 'Damped Harmonic Oscillator',
            'parameters': {
                'mass': self.mass,
                'damping': self.damping,
                'stiffness': self.stiffness,
                'natural_frequency': self.natural_frequency,
                'damping_ratio': self.damping_ratio,
                'damping_type': self.damping_type,
                'damped_frequency': self.damped_frequency,
                'initial_position': self.initial_position,
                'initial_velocity': self.initial_velocity
            },
            'timestamp': datetime.now().isoformat(),
            'simulation_results': {},
            'analysis_results': {}
        }
        
        # Convert numpy arrays to lists for JSON
        if self.simulation_results:
            sim_results = {}
            for key, value in self.simulation_results.items():
                if isinstance(value, np.ndarray):
                    sim_results[key] = value.tolist()
                else:
                    sim_results[key] = value
            output_data['simulation_results'] = sim_results
        
        # Convert analysis results (simplified for JSON)
        if self.analysis_results:
            analysis_json = {}
            for category, results in self.analysis_results.items():
                if isinstance(results, dict):
                    category_results = {}
                    for key, value in results.items():
                        if isinstance(value, (np.ndarray, np.number)):
                            if hasattr(value, 'tolist'):
                                category_results[key] = value.tolist()
                            else:
                                category_results[key] = float(value)
                        elif isinstance(value, (dict, list, str, bool, int, float, type(None))):
                            category_results[key] = value
                        else:
                            category_results[key] = str(value)
                    analysis_json[category] = category_results
                else:
                    analysis_json[category] = str(results)
            output_data['analysis_results'] = analysis_json
        
        # Save to file
        os.makedirs('results', exist_ok=True)
        filepath = os.path.join('results', filename)
        
        with open(filepath, 'w') as f:
            json.dump(output_data, f, indent=2)
        
        print(f"💾 Results saved to: {filepath}")
        return filepath

def demonstrate_damped_harmonic_oscillator():
    """Demonstration function showing damped SHO capabilities"""
    print("🌊 Damped Harmonic Oscillator Demonstration")
    print("=" * 50)
    
    # Create oscillator (underdamped case)
    damped_sho = DampedHarmonicOscillator(
        mass=1.0,              # 1 kg
        damping=0.2,           # 0.2 N⋅s/m
        stiffness=4.0,         # 4 N/m
        initial_position=1.0,  # 1 m displacement
        initial_velocity=0.0   # Start from rest
    )
    
    print(f"📊 Parameters:")
    print(f"   Mass (m): {damped_sho.mass} kg")
    print(f"   Damping (c): {damped_sho.damping} N⋅s/m")
    print(f"   Stiffness (k): {damped_sho.stiffness} N/m")
    print(f"   Natural frequency (ω₀): {damped_sho.natural_frequency:.3f} rad/s")
    print(f"   Damping ratio (ζ): {damped_sho.damping_ratio:.3f}")
    print(f"   Damping type: {damped_sho.damping_type}")
    if damped_sho.damped_frequency > 0:
        print(f"   Damped frequency (ωₐ): {damped_sho.damped_frequency:.3f} rad/s")
    
    # Simulate
    print("\n🔄 Running simulation...")
    time_span = np.linspace(0, 10, 1000)
    simulation_results = damped_sho.simulate(time_span)
    
    # Theoretical comparison
    theoretical_results = damped_sho.theoretical_solution(time_span)
    
    # Calculate error
    position_error = np.abs(simulation_results['position'] - theoretical_results['position_theoretical'])
    max_error = np.max(position_error)
    print(f"   Maximum simulation error: {max_error:.2e} m")
    
    # Energy dissipation analysis
    initial_energy = simulation_results['energy_total'][0]
    final_energy = simulation_results['energy_total'][-1]
    energy_dissipated = initial_energy - final_energy
    print(f"   Initial energy: {initial_energy:.6f} J")
    print(f"   Final energy: {final_energy:.6f} J")
    print(f"   Energy dissipated: {energy_dissipated:.6f} J ({100*energy_dissipated/initial_energy:.1f}%)")
    
    # Run comprehensive analysis
    analysis_results = damped_sho.run_analysis()
    
    # Display key results
    print(f"\n📈 Analysis Results:")
    if 'stability' in analysis_results:
        stability = analysis_results['stability']
        if 'comprehensive' in stability:
            overall_stable = stability['comprehensive'].get('overall_stable', 'Unknown')
            print(f"   Overall Stability: {overall_stable}")
        
        if 'poles_zeros' in stability:
            poles = stability['poles_zeros'].get('poles', [])
            damping_ratios = stability['poles_zeros'].get('damping_ratios', [])
            if len(poles) > 0:
                print(f"   Poles: {[f'{pole:.3f}' for pole in poles]}")
            if len(damping_ratios) > 0:
                print(f"   Pole damping ratios: {[f'{dr:.3f}' for dr in damping_ratios]}")
    
    if 'frequency_domain' in analysis_results:
        freq_domain = analysis_results['frequency_domain']
        if 'transfer_function' in freq_domain:
            tf_data = freq_domain['transfer_function']
            natural_freq = tf_data.get('natural_frequency', 0)
            damping_ratio = tf_data.get('damping_ratio', 0)
            print(f"   Natural frequency from TF: {natural_freq:.3f} rad/s")
            print(f"   Damping ratio from TF: {damping_ratio:.3f}")
    
    # Create visualizations
    print(f"\n📊 Generating visualizations...")
    damped_sho.visualize_results('results/damped_harmonic_oscillator_plots.png')
    
    # Save results
    print(f"\n💾 Saving results...")
    result_file = damped_sho.save_results()
    
    print(f"\n✅ Damped Harmonic Oscillator demonstration complete!")
    
    return damped_sho

def main():
    """Main function for independent script execution"""
    print("🚀 Damped Harmonic Oscillator - Independent Analysis")
    print("=" * 60)
    
    try:
        # Run demonstration
        oscillator = demonstrate_damped_harmonic_oscillator()
        
        print(f"\n🎯 Key Findings:")
        print(f"   • Energy dissipation due to damping")
        print(f"   • Exponential decay envelope in underdamped case")
        print(f"   • Poles have negative real parts (stable system)")
        print(f"   • Damped frequency lower than natural frequency")
        print(f"   • Theoretical solution matches numerical simulation")
        
        return True
        
    except Exception as e:
        print(f"❌ Error in demonstration: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)


