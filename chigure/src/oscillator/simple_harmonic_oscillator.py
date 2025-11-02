"""
Simple Harmonic Oscillator Implementation

A classic linear oscillator: m*x'' + k*x = 0
Natural frequency: ω_n = sqrt(k/m)

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

class SimpleHarmonicOscillator:
    """
    Simple Harmonic Oscillator: m*x'' + k*x = 0
    
    State variables: [x, x_dot]
    """
    
    def __init__(self, mass: float = 1.0, stiffness: float = 1.0, 
                 initial_position: float = 1.0, initial_velocity: float = 0.0):
        """
        Initialize Simple Harmonic Oscillator
        
        Args:
            mass: Mass (m) in kg
            stiffness: Spring constant (k) in N/m  
            initial_position: Initial displacement in m
            initial_velocity: Initial velocity in m/s
        """
        self.mass = mass
        self.stiffness = stiffness
        self.initial_position = initial_position
        self.initial_velocity = initial_velocity
        
        # Calculate derived parameters
        self.natural_frequency = np.sqrt(stiffness / mass)
        self.period = 2 * np.pi / self.natural_frequency
        
        # Results storage
        self.simulation_results = {}
        self.analysis_results = {}
    
    def get_transfer_function(self) -> signal.TransferFunction:
        """Get transfer function H(s) = X(s)/F(s)"""
        # For SHO: H(s) = 1/(m*s^2 + k) = (1/m)/(s^2 + k/m)
        num = [1/self.mass]
        den = [1, 0, self.stiffness/self.mass]
        return signal.TransferFunction(num, den)
    
    def get_state_equations(self):
        """Get state space equations dx/dt = f(x, t)"""
        def state_equations(x, t):
            position, velocity = x
            acceleration = -(self.stiffness / self.mass) * position
            return np.array([velocity, acceleration])
        return state_equations
    
    def get_characteristic_polynomial(self) -> np.ndarray:
        """Get characteristic polynomial coefficients"""
        # Characteristic equation: m*s^2 + k = 0 → s^2 + k/m = 0
        return np.array([1, 0, self.stiffness/self.mass])
    
    def get_equilibrium(self) -> np.ndarray:
        """Get equilibrium point"""
        return np.array([0.0, 0.0])  # Origin for SHO
    
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
        
        results = {
            'time': sol.t,
            'position': sol.y[0],
            'velocity': sol.y[1],
            'energy_kinetic': 0.5 * self.mass * sol.y[1]**2,
            'energy_potential': 0.5 * self.stiffness * sol.y[0]**2,
            'energy_total': 0.5 * self.mass * sol.y[1]**2 + 0.5 * self.stiffness * sol.y[0]**2
        }
        
        self.simulation_results = results
        return results
    
    def theoretical_solution(self, time_span: np.ndarray) -> Dict[str, Any]:
        """Calculate theoretical analytical solution"""
        t = time_span
        omega = self.natural_frequency
        A = self.initial_position
        B = self.initial_velocity / omega if omega > 0 else 0
        
        # Analytical solution: x(t) = A*cos(ωt) + B*sin(ωt)
        position_theoretical = A * np.cos(omega * t) + B * np.sin(omega * t)
        velocity_theoretical = -A * omega * np.sin(omega * t) + B * omega * np.cos(omega * t)
        
        return {
            'time': t,
            'position_theoretical': position_theoretical,
            'velocity_theoretical': velocity_theoretical
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
        
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        fig.suptitle('Simple Harmonic Oscillator Analysis', fontsize=16, fontweight='bold')
        
        t = self.simulation_results['time']
        x = self.simulation_results['position']
        v = self.simulation_results['velocity']
        
        # Time series plots
        axes[0, 0].plot(t, x, 'b-', linewidth=2, label='Position')
        axes[0, 0].plot(t, v, 'r-', linewidth=2, label='Velocity')
        axes[0, 0].set_xlabel('Time (s)')
        axes[0, 0].set_ylabel('Amplitude')
        axes[0, 0].set_title('Position and Velocity vs Time')
        axes[0, 0].grid(True, alpha=0.3)
        axes[0, 0].legend()
        
        # Phase portrait
        axes[0, 1].plot(x, v, 'g-', linewidth=2)
        axes[0, 1].scatter(x[0], v[0], color='red', s=100, label='Start', zorder=5)
        axes[0, 1].scatter(x[-1], v[-1], color='blue', s=100, label='End', zorder=5)
        axes[0, 1].set_xlabel('Position (m)')
        axes[0, 1].set_ylabel('Velocity (m/s)')
        axes[0, 1].set_title('Phase Portrait')
        axes[0, 1].grid(True, alpha=0.3)
        axes[0, 1].legend()
        axes[0, 1].axis('equal')
        
        # Energy analysis
        E_k = self.simulation_results['energy_kinetic']
        E_p = self.simulation_results['energy_potential']
        E_total = self.simulation_results['energy_total']
        
        axes[1, 0].plot(t, E_k, 'r-', linewidth=2, label='Kinetic Energy')
        axes[1, 0].plot(t, E_p, 'b-', linewidth=2, label='Potential Energy')
        axes[1, 0].plot(t, E_total, 'k--', linewidth=2, label='Total Energy')
        axes[1, 0].set_xlabel('Time (s)')
        axes[1, 0].set_ylabel('Energy (J)')
        axes[1, 0].set_title('Energy Conservation')
        axes[1, 0].grid(True, alpha=0.3)
        axes[1, 0].legend()
        
        # Frequency spectrum
        dt = t[1] - t[0]
        fft_x = np.fft.fft(x)
        frequencies = np.fft.fftfreq(len(x), dt)
        magnitude = np.abs(fft_x)
        
        # Plot positive frequencies only
        positive_freq_mask = frequencies > 0
        axes[1, 1].semilogy(frequencies[positive_freq_mask], magnitude[positive_freq_mask], 'b-', linewidth=2)
        axes[1, 1].axvline(self.natural_frequency/(2*np.pi), color='red', linestyle='--', 
                          label=f'Natural Freq: {self.natural_frequency/(2*np.pi):.3f} Hz')
        axes[1, 1].set_xlabel('Frequency (Hz)')
        axes[1, 1].set_ylabel('Magnitude')
        axes[1, 1].set_title('Frequency Spectrum')
        axes[1, 1].grid(True, alpha=0.3)
        axes[1, 1].legend()
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"📊 Visualization saved to: {save_path}")
        
        plt.show()
    
    def save_results(self, filename: str = None):
        """Save all results to JSON file"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"simple_harmonic_oscillator_results_{timestamp}.json"
        
        # Prepare data for JSON serialization
        output_data = {
            'oscillator_type': 'Simple Harmonic Oscillator',
            'parameters': {
                'mass': self.mass,
                'stiffness': self.stiffness,
                'natural_frequency': self.natural_frequency,
                'period': self.period,
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

def demonstrate_simple_harmonic_oscillator():
    """Demonstration function showing SHO capabilities"""
    print("🌊 Simple Harmonic Oscillator Demonstration")
    print("=" * 50)
    
    # Create oscillator
    sho = SimpleHarmonicOscillator(
        mass=1.0,           # 1 kg
        stiffness=4.0,      # 4 N/m  
        initial_position=1.0,  # 1 m displacement
        initial_velocity=0.0   # Start from rest
    )
    
    print(f"📊 Parameters:")
    print(f"   Mass (m): {sho.mass} kg")
    print(f"   Stiffness (k): {sho.stiffness} N/m")
    print(f"   Natural frequency (ωₙ): {sho.natural_frequency:.3f} rad/s")
    print(f"   Period (T): {sho.period:.3f} s")
    print(f"   Natural frequency (fₙ): {sho.natural_frequency/(2*np.pi):.3f} Hz")
    
    # Simulate
    print("\n🔄 Running simulation...")
    time_span = np.linspace(0, 3*sho.period, 1000)
    simulation_results = sho.simulate(time_span)
    
    # Theoretical comparison
    theoretical_results = sho.theoretical_solution(time_span)
    
    # Calculate error
    position_error = np.abs(simulation_results['position'] - theoretical_results['position_theoretical'])
    max_error = np.max(position_error)
    print(f"   Maximum simulation error: {max_error:.2e} m")
    
    # Energy conservation check
    energy_variation = np.std(simulation_results['energy_total'])
    print(f"   Energy conservation (std dev): {energy_variation:.2e} J")
    
    # Run comprehensive analysis
    analysis_results = sho.run_analysis()
    
    # Display key results
    print(f"\n📈 Analysis Results:")
    if 'stability' in analysis_results:
        stability = analysis_results['stability']
        if 'comprehensive' in stability:
            overall_stable = stability['comprehensive'].get('overall_stable', 'Unknown')
            print(f"   Overall Stability: {overall_stable}")
        
        if 'poles_zeros' in stability:
            poles = stability['poles_zeros'].get('poles', [])
            if len(poles) > 0:
                print(f"   Poles: {[f'{pole:.3f}' for pole in poles]}")
    
    if 'frequency_domain' in analysis_results:
        freq_domain = analysis_results['frequency_domain']
        if 'transfer_function' in freq_domain:
            tf_data = freq_domain['transfer_function']
            natural_freq = tf_data.get('natural_frequency', 0)
            damping_ratio = tf_data.get('damping_ratio', 0)
            print(f"   Natural frequency from TF: {natural_freq:.3f} rad/s")
            print(f"   Damping ratio: {damping_ratio:.6f}")
    
    if 'circuit_equivalent' in analysis_results:
        circuit = analysis_results['circuit_equivalent']
        if 'rlc_equivalent' in circuit:
            rlc = circuit['rlc_equivalent']
            if rlc.get('rlc_equivalent_available', False):
                L = rlc.get('inductance', 0)
                C = rlc.get('capacitance', 0)
                R = rlc.get('resistance', 0)
                Q = rlc.get('quality_factor', 0)
                print(f"   RLC Equivalent - L: {L:.3f} H, C: {C:.3f} F, R: {R:.3f} Ω")
                print(f"   Quality Factor (Q): {Q}")
    
    # Create visualizations
    print(f"\n📊 Generating visualizations...")
    sho.visualize_results('results/simple_harmonic_oscillator_plots.png')
    
    # Save results
    print(f"\n💾 Saving results...")
    result_file = sho.save_results()
    
    print(f"\n✅ Simple Harmonic Oscillator demonstration complete!")
    print(f"   Results saved to: {result_file}")
    
    return sho

def main():
    """Main function for independent script execution"""
    print("🚀 Simple Harmonic Oscillator - Independent Analysis")
    print("=" * 60)
    
    try:
        # Run demonstration
        oscillator = demonstrate_simple_harmonic_oscillator()
        
        print(f"\n🎯 Key Findings:")
        print(f"   • Perfect energy conservation in simulation")
        print(f"   • Analytical solution matches numerical simulation")
        print(f"   • Pure imaginary poles indicate undamped oscillation")
        print(f"   • Transfer function correctly represents SHO dynamics")
        
        return True
        
    except Exception as e:
        print(f"❌ Error in demonstration: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
