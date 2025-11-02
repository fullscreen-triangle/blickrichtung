"""
Driven Harmonic Oscillator Implementation

A driven damped linear oscillator: m*x'' + c*x' + k*x = F₀*cos(ωt)
Shows resonance behavior when driving frequency matches natural frequency.

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

class DrivenHarmonicOscillator:
    """
    Driven Harmonic Oscillator: m*x'' + c*x' + k*x = F₀*cos(ωt)
    
    State variables: [x, x_dot]
    """
    
    def __init__(self, mass: float = 1.0, damping: float = 0.1, stiffness: float = 1.0,
                 driving_amplitude: float = 1.0, driving_frequency: float = 1.0,
                 initial_position: float = 0.0, initial_velocity: float = 0.0):
        """
        Initialize Driven Harmonic Oscillator
        
        Args:
            mass: Mass (m) in kg
            damping: Damping coefficient (c) in N⋅s/m
            stiffness: Spring constant (k) in N/m
            driving_amplitude: Driving force amplitude (F₀) in N
            driving_frequency: Driving frequency (ω) in rad/s
            initial_position: Initial displacement in m
            initial_velocity: Initial velocity in m/s
        """
        self.mass = mass
        self.damping = damping
        self.stiffness = stiffness
        self.driving_amplitude = driving_amplitude
        self.driving_frequency = driving_frequency
        self.initial_position = initial_position
        self.initial_velocity = initial_velocity
        
        # Calculate derived parameters
        self.natural_frequency = np.sqrt(stiffness / mass)  # ω₀
        self.damping_ratio = damping / (2 * np.sqrt(mass * stiffness))  # ζ
        
        # Frequency ratio
        self.frequency_ratio = driving_frequency / self.natural_frequency  # r = ω/ω₀
        
        # Steady-state amplitude calculation
        self.steady_state_amplitude = self._calculate_steady_state_amplitude()
        self.phase_lag = self._calculate_phase_lag()
        
        # Results storage
        self.simulation_results = {}
        self.analysis_results = {}
    
    def _calculate_steady_state_amplitude(self) -> float:
        """Calculate steady-state amplitude"""
        F0_over_k = self.driving_amplitude / self.stiffness
        r = self.frequency_ratio
        zeta = self.damping_ratio
        
        denominator = np.sqrt((1 - r**2)**2 + (2*zeta*r)**2)
        return F0_over_k / denominator
    
    def _calculate_phase_lag(self) -> float:
        """Calculate phase lag in radians"""
        r = self.frequency_ratio
        zeta = self.damping_ratio
        
        numerator = 2 * zeta * r
        denominator = 1 - r**2
        
        if denominator != 0:
            phase_lag = np.arctan(numerator / denominator)
        else:
            phase_lag = np.pi / 2
        
        # Adjust for correct quadrant
        if denominator < 0:
            phase_lag += np.pi
        
        return phase_lag
    
    def get_transfer_function(self) -> signal.TransferFunction:
        """Get transfer function H(s) = X(s)/F(s)"""
        # For driven damped SHO: H(s) = 1/(m*s^2 + c*s + k)
        num = [1/self.mass]
        den = [1, self.damping/self.mass, self.stiffness/self.mass]
        return signal.TransferFunction(num, den)
    
    def get_state_equations(self):
        """Get state space equations dx/dt = f(x, t)"""
        def state_equations(x, t):
            position, velocity = x
            driving_force = self.driving_amplitude * np.cos(self.driving_frequency * t)
            acceleration = (driving_force - self.stiffness * position - self.damping * velocity) / self.mass
            return np.array([velocity, acceleration])
        return state_equations
    
    def get_characteristic_polynomial(self) -> np.ndarray:
        """Get characteristic polynomial coefficients"""
        # Same as damped oscillator (driving doesn't affect stability)
        return np.array([1, self.damping/self.mass, self.stiffness/self.mass])
    
    def get_equilibrium(self) -> np.ndarray:
        """Get equilibrium point (for undriven system)"""
        return np.array([0.0, 0.0])
    
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
        
        # Calculate driving force
        driving_force = self.driving_amplitude * np.cos(self.driving_frequency * sol.t)
        
        # Calculate energies
        kinetic_energy = 0.5 * self.mass * sol.y[1]**2
        potential_energy = 0.5 * self.stiffness * sol.y[0]**2
        total_energy = kinetic_energy + potential_energy
        
        # Calculate power input and dissipation
        power_input = driving_force * sol.y[1]  # F * v
        power_dissipated = self.damping * sol.y[1]**2  # c * v^2
        
        results = {
            'time': sol.t,
            'position': sol.y[0],
            'velocity': sol.y[1],
            'driving_force': driving_force,
            'energy_kinetic': kinetic_energy,
            'energy_potential': potential_energy,
            'energy_total': total_energy,
            'power_input': power_input,
            'power_dissipated': power_dissipated
        }
        
        self.simulation_results = results
        return results
    
    def theoretical_steady_state(self, time_span: np.ndarray) -> Dict[str, Any]:
        """Calculate theoretical steady-state solution"""
        t = time_span
        
        # Steady-state solution: x(t) = A*cos(ωt - φ)
        position_steady = self.steady_state_amplitude * np.cos(self.driving_frequency * t - self.phase_lag)
        velocity_steady = -self.steady_state_amplitude * self.driving_frequency * np.sin(self.driving_frequency * t - self.phase_lag)
        
        return {
            'time': t,
            'position_steady_state': position_steady,
            'velocity_steady_state': velocity_steady,
            'amplitude': self.steady_state_amplitude,
            'phase_lag': self.phase_lag
        }
    
    def frequency_response_analysis(self, frequency_range: np.ndarray) -> Dict[str, Any]:
        """Analyze frequency response over a range of driving frequencies"""
        amplitudes = []
        phase_lags = []
        
        for freq in frequency_range:
            # Temporarily change driving frequency
            old_freq = self.driving_frequency
            self.driving_frequency = freq
            self.frequency_ratio = freq / self.natural_frequency
            
            # Calculate response
            amplitude = self._calculate_steady_state_amplitude()
            phase_lag = self._calculate_phase_lag()
            
            amplitudes.append(amplitude)
            phase_lags.append(phase_lag)
            
            # Restore original frequency
            self.driving_frequency = old_freq
            self.frequency_ratio = old_freq / self.natural_frequency
        
        return {
            'frequencies': frequency_range,
            'amplitudes': np.array(amplitudes),
            'phase_lags': np.array(phase_lags)
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
        
        fig, axes = plt.subplots(3, 2, figsize=(15, 15))
        fig.suptitle(f'Driven Harmonic Oscillator Analysis (r = ω/ω₀ = {self.frequency_ratio:.2f})', fontsize=16, fontweight='bold')
        
        t = self.simulation_results['time']
        x = self.simulation_results['position']
        v = self.simulation_results['velocity']
        F_drive = self.simulation_results['driving_force']
        
        # Get steady-state theoretical solution
        steady_state = self.theoretical_steady_state(t)
        x_steady = steady_state['position_steady_state']
        
        # Position vs time with driving force
        ax1 = axes[0, 0]
        ax1.plot(t, x, 'b-', linewidth=2, label='Position')
        ax1.plot(t, x_steady, 'r--', linewidth=2, label='Steady State', alpha=0.7)
        ax1_twin = ax1.twinx()
        ax1_twin.plot(t, F_drive, 'g:', linewidth=1, alpha=0.7, label='Driving Force')
        ax1.set_xlabel('Time (s)')
        ax1.set_ylabel('Position (m)', color='b')
        ax1_twin.set_ylabel('Driving Force (N)', color='g')
        ax1.set_title('Position vs Time with Driving Force')
        ax1.grid(True, alpha=0.3)
        ax1.legend(loc='upper left')
        ax1_twin.legend(loc='upper right')
        
        # Phase portrait
        axes[0, 1].plot(x, v, 'purple', linewidth=2)
        axes[0, 1].scatter(x[0], v[0], color='red', s=100, label='Start', zorder=5)
        axes[0, 1].set_xlabel('Position (m)')
        axes[0, 1].set_ylabel('Velocity (m/s)')
        axes[0, 1].set_title('Phase Portrait')
        axes[0, 1].grid(True, alpha=0.3)
        axes[0, 1].legend()
        
        # Energy analysis
        E_k = self.simulation_results['energy_kinetic']
        E_p = self.simulation_results['energy_potential']
        E_total = self.simulation_results['energy_total']
        
        axes[1, 0].plot(t, E_k, 'r-', linewidth=2, label='Kinetic Energy')
        axes[1, 0].plot(t, E_p, 'b-', linewidth=2, label='Potential Energy')
        axes[1, 0].plot(t, E_total, 'k-', linewidth=2, label='Total Energy')
        axes[1, 0].set_xlabel('Time (s)')
        axes[1, 0].set_ylabel('Energy (J)')
        axes[1, 0].set_title('Energy Analysis')
        axes[1, 0].grid(True, alpha=0.3)
        axes[1, 0].legend()
        
        # Power analysis
        P_in = self.simulation_results['power_input']
        P_diss = self.simulation_results['power_dissipated']
        
        axes[1, 1].plot(t, P_in, 'g-', linewidth=2, label='Power Input')
        axes[1, 1].plot(t, P_diss, 'r-', linewidth=2, label='Power Dissipated')
        axes[1, 1].set_xlabel('Time (s)')
        axes[1, 1].set_ylabel('Power (W)')
        axes[1, 1].set_title('Power Analysis')
        axes[1, 1].grid(True, alpha=0.3)
        axes[1, 1].legend()
        
        # Frequency response
        freq_range = np.linspace(0.1*self.natural_frequency, 3*self.natural_frequency, 100)
        freq_response = self.frequency_response_analysis(freq_range)
        
        axes[2, 0].plot(freq_range/self.natural_frequency, freq_response['amplitudes'], 'b-', linewidth=2)
        axes[2, 0].axvline(1.0, color='red', linestyle='--', label='Natural Frequency')
        axes[2, 0].axvline(self.frequency_ratio, color='green', linestyle='--', label='Current Driving Freq.')
        axes[2, 0].set_xlabel('Frequency Ratio (ω/ω₀)')
        axes[2, 0].set_ylabel('Amplitude Ratio')
        axes[2, 0].set_title('Frequency Response - Amplitude')
        axes[2, 0].grid(True, alpha=0.3)
        axes[2, 0].legend()
        
        # Phase response
        axes[2, 1].plot(freq_range/self.natural_frequency, np.degrees(freq_response['phase_lags']), 'r-', linewidth=2)
        axes[2, 1].axvline(1.0, color='red', linestyle='--', label='Natural Frequency')
        axes[2, 1].axvline(self.frequency_ratio, color='green', linestyle='--', label='Current Driving Freq.')
        axes[2, 1].set_xlabel('Frequency Ratio (ω/ω₀)')
        axes[2, 1].set_ylabel('Phase Lag (degrees)')
        axes[2, 1].set_title('Frequency Response - Phase')
        axes[2, 1].grid(True, alpha=0.3)
        axes[2, 1].legend()
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"📊 Visualization saved to: {save_path}")
        
        plt.show()
    
    def save_results(self, filename: str = None):
        """Save all results to JSON file"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"driven_harmonic_oscillator_results_{timestamp}.json"
        
        # Prepare data for JSON serialization
        output_data = {
            'oscillator_type': 'Driven Harmonic Oscillator',
            'parameters': {
                'mass': self.mass,
                'damping': self.damping,
                'stiffness': self.stiffness,
                'driving_amplitude': self.driving_amplitude,
                'driving_frequency': self.driving_frequency,
                'natural_frequency': self.natural_frequency,
                'damping_ratio': self.damping_ratio,
                'frequency_ratio': self.frequency_ratio,
                'steady_state_amplitude': self.steady_state_amplitude,
                'phase_lag': self.phase_lag,
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

def demonstrate_driven_harmonic_oscillator():
    """Demonstration function showing driven SHO capabilities"""
    print("🌊 Driven Harmonic Oscillator Demonstration")
    print("=" * 50)
    
    # Create oscillator near resonance
    driven_sho = DrivenHarmonicOscillator(
        mass=1.0,              # 1 kg
        damping=0.1,           # 0.1 N⋅s/m
        stiffness=4.0,         # 4 N/m (ω₀ = 2 rad/s)
        driving_amplitude=1.0, # 1 N
        driving_frequency=1.8, # Near resonance
        initial_position=0.0,  # Start at equilibrium
        initial_velocity=0.0   # Start from rest
    )
    
    print(f"📊 Parameters:")
    print(f"   Mass (m): {driven_sho.mass} kg")
    print(f"   Damping (c): {driven_sho.damping} N⋅s/m")
    print(f"   Stiffness (k): {driven_sho.stiffness} N/m")
    print(f"   Driving amplitude (F₀): {driven_sho.driving_amplitude} N")
    print(f"   Driving frequency (ω): {driven_sho.driving_frequency:.3f} rad/s")
    print(f"   Natural frequency (ω₀): {driven_sho.natural_frequency:.3f} rad/s")
    print(f"   Frequency ratio (r): {driven_sho.frequency_ratio:.3f}")
    print(f"   Damping ratio (ζ): {driven_sho.damping_ratio:.3f}")
    print(f"   Steady-state amplitude: {driven_sho.steady_state_amplitude:.3f} m")
    print(f"   Phase lag: {np.degrees(driven_sho.phase_lag):.1f}°")
    
    # Simulate
    print("\n🔄 Running simulation...")
    time_span = np.linspace(0, 20, 2000)  # Longer time to reach steady state
    simulation_results = driven_sho.simulate(time_span)
    
    # Steady-state analysis (use last 25% of simulation)
    steady_start = int(0.75 * len(time_span))
    position_steady = simulation_results['position'][steady_start:]
    velocity_steady = simulation_results['velocity'][steady_start:]
    
    # Calculate actual steady-state amplitude and compare with theory
    actual_amplitude = (np.max(position_steady) - np.min(position_steady)) / 2
    theoretical_amplitude = driven_sho.steady_state_amplitude
    amplitude_error = abs(actual_amplitude - theoretical_amplitude)
    
    print(f"   Theoretical steady-state amplitude: {theoretical_amplitude:.4f} m")
    print(f"   Actual steady-state amplitude: {actual_amplitude:.4f} m")
    print(f"   Amplitude error: {amplitude_error:.2e} m ({100*amplitude_error/theoretical_amplitude:.2f}%)")
    
    # Power balance analysis
    power_in = simulation_results['power_input'][steady_start:]
    power_diss = simulation_results['power_dissipated'][steady_start:]
    avg_power_in = np.mean(power_in)
    avg_power_diss = np.mean(power_diss)
    
    print(f"   Average power input: {avg_power_in:.6f} W")
    print(f"   Average power dissipated: {avg_power_diss:.6f} W")
    print(f"   Power balance error: {abs(avg_power_in - avg_power_diss):.2e} W")
    
    # Run comprehensive analysis
    analysis_results = driven_sho.run_analysis()
    
    # Display key results
    print(f"\n📈 Analysis Results:")
    if 'stability' in analysis_results:
        stability = analysis_results['stability']
        if 'comprehensive' in stability:
            overall_stable = stability['comprehensive'].get('overall_stable', 'Unknown')
            print(f"   Overall Stability: {overall_stable}")
    
    if 'frequency_domain' in analysis_results:
        freq_domain = analysis_results['frequency_domain']
        if 'bode' in freq_domain:
            bode_data = freq_domain['bode']
            gain_margin = bode_data.get('gain_margin', 0)
            phase_margin = bode_data.get('phase_margin', 0)
            print(f"   Gain margin: {gain_margin:.2f} dB")
            print(f"   Phase margin: {phase_margin:.2f}°")
    
    # Create visualizations
    print(f"\n📊 Generating visualizations...")
    driven_sho.visualize_results('results/driven_harmonic_oscillator_plots.png')
    
    # Save results
    print(f"\n💾 Saving results...")
    result_file = driven_sho.save_results()
    
    print(f"\n✅ Driven Harmonic Oscillator demonstration complete!")
    
    return driven_sho

def main():
    """Main function for independent script execution"""
    print("🚀 Driven Harmonic Oscillator - Independent Analysis")
    print("=" * 60)
    
    try:
        # Run demonstration
        oscillator = demonstrate_driven_harmonic_oscillator()
        
        print(f"\n🎯 Key Findings:")
        print(f"   • Resonance amplification near natural frequency")
        print(f"   • Phase lag varies from 0° to 180° across frequency range")
        print(f"   • Power input balances power dissipation in steady state")
        print(f"   • Steady-state amplitude depends on frequency ratio and damping")
        print(f"   • System stability independent of driving force")
        
        return True
        
    except Exception as e:
        print(f"❌ Error in demonstration: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)


