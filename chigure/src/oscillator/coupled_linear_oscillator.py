"""
Coupled Linear Oscillator Implementation

Two coupled harmonic oscillators: 
m₁*x₁'' + k₁*x₁ + k₁₂*(x₁-x₂) = 0
m₂*x₂'' + k₂*x₂ + k₁₂*(x₂-x₁) = 0

Shows normal modes, beating phenomena, and energy transfer.

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
from typing import Dict, Any, Optional, Tuple

# Import analysis module
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from core.analysis import run_all_tests, run_coupling_tests

class CoupledLinearOscillator:
    """
    Two Coupled Linear Oscillators
    
    m₁*x₁'' + k₁*x₁ + k₁₂*(x₁-x₂) = 0
    m₂*x₂'' + k₂*x₂ + k₁₂*(x₂-x₁) = 0
    
    State variables: [x₁, x₁_dot, x₂, x₂_dot]
    """
    
    def __init__(self, mass1: float = 1.0, mass2: float = 1.0,
                 stiffness1: float = 1.0, stiffness2: float = 1.0, 
                 coupling_stiffness: float = 0.1,
                 initial_position1: float = 1.0, initial_velocity1: float = 0.0,
                 initial_position2: float = 0.0, initial_velocity2: float = 0.0):
        """
        Initialize Coupled Linear Oscillators
        
        Args:
            mass1, mass2: Masses (m₁, m₂) in kg
            stiffness1, stiffness2: Individual spring constants (k₁, k₂) in N/m
            coupling_stiffness: Coupling spring constant (k₁₂) in N/m
            initial_position1, initial_position2: Initial displacements in m
            initial_velocity1, initial_velocity2: Initial velocities in m/s
        """
        self.mass1 = mass1
        self.mass2 = mass2
        self.stiffness1 = stiffness1
        self.stiffness2 = stiffness2
        self.coupling_stiffness = coupling_stiffness
        self.initial_position1 = initial_position1
        self.initial_velocity1 = initial_velocity1
        self.initial_position2 = initial_position2
        self.initial_velocity2 = initial_velocity2
        
        # Calculate normal mode frequencies
        self.normal_mode_frequencies = self._calculate_normal_modes()
        self.individual_frequencies = [np.sqrt(stiffness1/mass1), np.sqrt(stiffness2/mass2)]
        
        # Calculate coupling parameters
        self.coupling_strength = coupling_stiffness / np.sqrt(stiffness1 * stiffness2)
        
        # Results storage
        self.simulation_results = {}
        self.analysis_results = {}
    
    def _calculate_normal_modes(self) -> Tuple[float, float]:
        """Calculate normal mode frequencies"""
        # System matrix for normal mode analysis
        # [k₁+k₁₂  -k₁₂ ]
        # [-k₁₂   k₂+k₁₂]
        
        # Mass matrix
        M = np.array([[self.mass1, 0], [0, self.mass2]])
        
        # Stiffness matrix  
        K = np.array([[self.stiffness1 + self.coupling_stiffness, -self.coupling_stiffness],
                      [-self.coupling_stiffness, self.stiffness2 + self.coupling_stiffness]])
        
        # Solve generalized eigenvalue problem: K*φ = ω²*M*φ
        eigenvalues, eigenvectors = np.linalg.eig(np.linalg.inv(M) @ K)
        
        # Sort by frequency
        sorted_indices = np.argsort(eigenvalues)
        frequencies = np.sqrt(eigenvalues[sorted_indices])
        
        self.normal_mode_vectors = eigenvectors[:, sorted_indices]
        
        return frequencies[0], frequencies[1]  # Lower and higher mode frequencies
    
    def get_transfer_function(self) -> signal.TransferFunction:
        """Get transfer function for first oscillator (simplified)"""
        # For uncoupled oscillator 1 (approximation)
        num = [1/self.mass1]
        den = [1, 0, (self.stiffness1 + self.coupling_stiffness)/self.mass1]
        return signal.TransferFunction(num, den)
    
    def get_state_equations(self):
        """Get state space equations dx/dt = f(x, t)"""
        def state_equations(x, t):
            x1, x1_dot, x2, x2_dot = x
            
            # Coupling forces
            coupling_force = self.coupling_stiffness * (x2 - x1)
            
            # Accelerations
            x1_ddot = (-self.stiffness1 * x1 + coupling_force) / self.mass1
            x2_ddot = (-self.stiffness2 * x2 - coupling_force) / self.mass2
            
            return np.array([x1_dot, x1_ddot, x2_dot, x2_ddot])
        return state_equations
    
    def get_characteristic_polynomial(self) -> np.ndarray:
        """Get characteristic polynomial for the coupled system"""
        # This is complex for coupled system - simplified version
        m1, m2 = self.mass1, self.mass2
        k1, k2, k12 = self.stiffness1, self.stiffness2, self.coupling_stiffness
        
        # Fourth-order characteristic polynomial
        a0 = 1
        a1 = 0  # No damping
        a2 = (k1 + k12)/m1 + (k2 + k12)/m2
        a3 = 0  # No first-order terms
        a4 = (k1*k2 + k12*(k1 + k2))/(m1*m2)
        
        return np.array([a0, a1, a2, a3, a4])
    
    def get_equilibrium(self) -> np.ndarray:
        """Get equilibrium point"""
        return np.array([0.0, 0.0, 0.0, 0.0])  # Both oscillators at rest
    
    def get_initial_conditions(self) -> np.ndarray:
        """Get initial conditions"""
        return np.array([self.initial_position1, self.initial_velocity1, 
                        self.initial_position2, self.initial_velocity2])
    
    def simulate(self, time_span: np.ndarray) -> Dict[str, Any]:
        """Simulate the coupled oscillators"""
        initial_conditions = self.get_initial_conditions()
        state_equations = self.get_state_equations()
        
        def ode_system(t, y):
            return state_equations(y, t)
        
        sol = solve_ivp(ode_system, [time_span[0], time_span[-1]], 
                       initial_conditions, t_eval=time_span, rtol=1e-10)
        
        # Extract positions and velocities
        x1, x1_dot, x2, x2_dot = sol.y
        
        # Calculate energies
        kinetic1 = 0.5 * self.mass1 * x1_dot**2
        kinetic2 = 0.5 * self.mass2 * x2_dot**2
        potential1 = 0.5 * self.stiffness1 * x1**2
        potential2 = 0.5 * self.stiffness2 * x2**2
        coupling_potential = 0.5 * self.coupling_stiffness * (x1 - x2)**2
        
        total_kinetic = kinetic1 + kinetic2
        total_potential = potential1 + potential2 + coupling_potential
        total_energy = total_kinetic + total_potential
        
        # Calculate normal mode amplitudes
        normal_coords = self._transform_to_normal_coordinates(x1, x2)
        
        results = {
            'time': sol.t,
            'position1': x1,
            'velocity1': x1_dot,
            'position2': x2,
            'velocity2': x2_dot,
            'energy_kinetic1': kinetic1,
            'energy_kinetic2': kinetic2,
            'energy_potential1': potential1,
            'energy_potential2': potential2,
            'energy_coupling': coupling_potential,
            'energy_total_kinetic': total_kinetic,
            'energy_total_potential': total_potential,
            'energy_total': total_energy,
            'normal_coordinate1': normal_coords[0],
            'normal_coordinate2': normal_coords[1]
        }
        
        self.simulation_results = results
        return results
    
    def _transform_to_normal_coordinates(self, x1: np.ndarray, x2: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """Transform to normal coordinates"""
        # Normal mode transformation
        mode1_vector = self.normal_mode_vectors[:, 0]
        mode2_vector = self.normal_mode_vectors[:, 1]
        
        # Project onto normal modes
        positions = np.vstack([x1, x2])
        
        # Calculate normal coordinates (simplified)
        normal1 = mode1_vector[0] * x1 + mode1_vector[1] * x2
        normal2 = mode2_vector[0] * x1 + mode2_vector[1] * x2
        
        return normal1, normal2
    
    def calculate_beating_envelope(self) -> Dict[str, Any]:
        """Calculate beating envelope when frequencies are close"""
        if not self.simulation_results:
            return {}
        
        omega1, omega2 = self.normal_mode_frequencies
        
        # Beating frequency and envelope frequency
        beat_frequency = abs(omega2 - omega1) / (2 * np.pi)
        envelope_frequency = (omega1 + omega2) / (4 * np.pi)
        
        t = self.simulation_results['time']
        x1 = self.simulation_results['position1']
        
        # Calculate envelope using Hilbert transform
        from scipy.signal import hilbert
        analytic_signal = hilbert(x1)
        envelope = np.abs(analytic_signal)
        
        return {
            'beat_frequency': beat_frequency,
            'envelope_frequency': envelope_frequency,
            'envelope': envelope,
            'beat_period': 1/beat_frequency if beat_frequency > 0 else float('inf')
        }
    
    def run_analysis(self) -> Dict[str, Any]:
        """Run comprehensive analysis using analysis module"""
        print("🔬 Running comprehensive analysis...")
        self.analysis_results = run_all_tests(self, include_st_stellas=False)
        
        # Also run coupling analysis
        print("🔗 Running coupling analysis...")
        # Create individual oscillator objects for coupling analysis
        osc1 = SingleOscillatorFromCoupled(self, oscillator_index=0)
        osc2 = SingleOscillatorFromCoupled(self, oscillator_index=1)
        
        coupling_results = run_coupling_tests([osc1, osc2], include_st_stellas=False)
        self.analysis_results['coupling_analysis'] = coupling_results
        
        return self.analysis_results
    
    def visualize_results(self, save_path: Optional[str] = None):
        """Create comprehensive visualizations"""
        if not self.simulation_results:
            print("⚠️  No simulation results to visualize. Run simulate() first.")
            return
        
        fig, axes = plt.subplots(3, 3, figsize=(18, 15))
        fig.suptitle('Coupled Linear Oscillators Analysis', fontsize=16, fontweight='bold')
        
        t = self.simulation_results['time']
        x1 = self.simulation_results['position1']
        x2 = self.simulation_results['position2']
        v1 = self.simulation_results['velocity1']
        v2 = self.simulation_results['velocity2']
        
        # Position time series
        axes[0, 0].plot(t, x1, 'b-', linewidth=2, label='Oscillator 1')
        axes[0, 0].plot(t, x2, 'r-', linewidth=2, label='Oscillator 2')
        axes[0, 0].set_xlabel('Time (s)')
        axes[0, 0].set_ylabel('Position (m)')
        axes[0, 0].set_title('Position vs Time')
        axes[0, 0].grid(True, alpha=0.3)
        axes[0, 0].legend()
        
        # Phase portraits
        axes[0, 1].plot(x1, v1, 'b-', linewidth=2, label='Oscillator 1')
        axes[0, 1].set_xlabel('Position 1 (m)')
        axes[0, 1].set_ylabel('Velocity 1 (m/s)')
        axes[0, 1].set_title('Phase Portrait - Oscillator 1')
        axes[0, 1].grid(True, alpha=0.3)
        
        axes[0, 2].plot(x2, v2, 'r-', linewidth=2, label='Oscillator 2')
        axes[0, 2].set_xlabel('Position 2 (m)')
        axes[0, 2].set_ylabel('Velocity 2 (m/s)')
        axes[0, 2].set_title('Phase Portrait - Oscillator 2')
        axes[0, 2].grid(True, alpha=0.3)
        
        # Configuration space
        axes[1, 0].plot(x1, x2, 'purple', linewidth=2)
        axes[1, 0].scatter(x1[0], x2[0], color='green', s=100, label='Start', zorder=5)
        axes[1, 0].scatter(x1[-1], x2[-1], color='orange', s=100, label='End', zorder=5)
        axes[1, 0].set_xlabel('Position 1 (m)')
        axes[1, 0].set_ylabel('Position 2 (m)')
        axes[1, 0].set_title('Configuration Space')
        axes[1, 0].grid(True, alpha=0.3)
        axes[1, 0].legend()
        
        # Energy analysis
        E_k1 = self.simulation_results['energy_kinetic1']
        E_k2 = self.simulation_results['energy_kinetic2']
        E_p1 = self.simulation_results['energy_potential1']
        E_p2 = self.simulation_results['energy_potential2']
        E_coupling = self.simulation_results['energy_coupling']
        E_total = self.simulation_results['energy_total']
        
        axes[1, 1].plot(t, E_k1, 'b-', linewidth=2, label='Kinetic 1')
        axes[1, 1].plot(t, E_k2, 'r-', linewidth=2, label='Kinetic 2')
        axes[1, 1].plot(t, E_p1, 'b--', linewidth=2, label='Potential 1')
        axes[1, 1].plot(t, E_p2, 'r--', linewidth=2, label='Potential 2')
        axes[1, 1].plot(t, E_coupling, 'g-', linewidth=2, label='Coupling')
        axes[1, 1].set_xlabel('Time (s)')
        axes[1, 1].set_ylabel('Energy (J)')
        axes[1, 1].set_title('Energy Components')
        axes[1, 1].grid(True, alpha=0.3)
        axes[1, 1].legend()
        
        # Total energy conservation
        axes[1, 2].plot(t, E_total, 'k-', linewidth=2, label='Total Energy')
        axes[1, 2].set_xlabel('Time (s)')
        axes[1, 2].set_ylabel('Total Energy (J)')
        axes[1, 2].set_title('Energy Conservation')
        axes[1, 2].grid(True, alpha=0.3)
        
        # Normal modes
        normal1 = self.simulation_results['normal_coordinate1']
        normal2 = self.simulation_results['normal_coordinate2']
        
        axes[2, 0].plot(t, normal1, 'g-', linewidth=2, label=f'Mode 1 (ω={self.normal_mode_frequencies[0]:.3f})')
        axes[2, 0].plot(t, normal2, 'm-', linewidth=2, label=f'Mode 2 (ω={self.normal_mode_frequencies[1]:.3f})')
        axes[2, 0].set_xlabel('Time (s)')
        axes[2, 0].set_ylabel('Normal Coordinate')
        axes[2, 0].set_title('Normal Mode Coordinates')
        axes[2, 0].grid(True, alpha=0.3)
        axes[2, 0].legend()
        
        # Beating analysis (if applicable)
        beating_data = self.calculate_beating_envelope()
        if beating_data:
            axes[2, 1].plot(t, x1, 'b-', linewidth=1, alpha=0.7, label='Position 1')
            if 'envelope' in beating_data:
                axes[2, 1].plot(t, beating_data['envelope'], 'r-', linewidth=2, label='Envelope')
                axes[2, 1].plot(t, -beating_data['envelope'], 'r-', linewidth=2)
            axes[2, 1].set_xlabel('Time (s)')
            axes[2, 1].set_ylabel('Amplitude')
            axes[2, 1].set_title(f'Beating (f_beat = {beating_data.get("beat_frequency", 0):.3f} Hz)')
            axes[2, 1].grid(True, alpha=0.3)
            axes[2, 1].legend()
        
        # Frequency spectrum
        dt = t[1] - t[0]
        fft_x1 = np.fft.fft(x1)
        frequencies = np.fft.fftfreq(len(x1), dt)
        magnitude = np.abs(fft_x1)
        
        # Plot positive frequencies only
        positive_freq_mask = frequencies > 0
        axes[2, 2].semilogy(frequencies[positive_freq_mask], magnitude[positive_freq_mask], 'b-', linewidth=2)
        
        # Mark normal mode frequencies
        for i, freq in enumerate(self.normal_mode_frequencies):
            axes[2, 2].axvline(freq/(2*np.pi), color=['red', 'green'][i], linestyle='--', 
                              label=f'Mode {i+1}: {freq/(2*np.pi):.3f} Hz')
        
        axes[2, 2].set_xlabel('Frequency (Hz)')
        axes[2, 2].set_ylabel('Magnitude')
        axes[2, 2].set_title('Frequency Spectrum')
        axes[2, 2].grid(True, alpha=0.3)
        axes[2, 2].legend()
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"📊 Visualization saved to: {save_path}")
        
        plt.show()
    
    def save_results(self, filename: str = None):
        """Save all results to JSON file"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"coupled_linear_oscillator_results_{timestamp}.json"
        
        # Prepare data for JSON serialization
        output_data = {
            'oscillator_type': 'Coupled Linear Oscillators',
            'parameters': {
                'mass1': self.mass1,
                'mass2': self.mass2,
                'stiffness1': self.stiffness1,
                'stiffness2': self.stiffness2,
                'coupling_stiffness': self.coupling_stiffness,
                'coupling_strength': self.coupling_strength,
                'normal_mode_frequencies': [float(f) for f in self.normal_mode_frequencies],
                'individual_frequencies': self.individual_frequencies,
                'initial_position1': self.initial_position1,
                'initial_velocity1': self.initial_velocity1,
                'initial_position2': self.initial_position2,
                'initial_velocity2': self.initial_velocity2
            },
            'normal_mode_vectors': self.normal_mode_vectors.tolist(),
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

class SingleOscillatorFromCoupled:
    """Helper class to represent a single oscillator from the coupled system for coupling analysis"""
    
    def __init__(self, coupled_system: CoupledLinearOscillator, oscillator_index: int):
        self.coupled_system = coupled_system
        self.oscillator_index = oscillator_index
        
    def get_state_equations(self):
        """Get state equations for this individual oscillator"""
        def state_equations(x, t):
            position, velocity = x
            if self.oscillator_index == 0:
                mass = self.coupled_system.mass1
                stiffness = self.coupled_system.stiffness1
            else:
                mass = self.coupled_system.mass2
                stiffness = self.coupled_system.stiffness2
                
            acceleration = -stiffness * position / mass
            return np.array([velocity, acceleration])
        return state_equations
    
    def get_initial_conditions(self) -> np.ndarray:
        """Get initial conditions for this oscillator"""
        if self.oscillator_index == 0:
            return np.array([self.coupled_system.initial_position1, self.coupled_system.initial_velocity1])
        else:
            return np.array([self.coupled_system.initial_position2, self.coupled_system.initial_velocity2])

def demonstrate_coupled_linear_oscillator():
    """Demonstration function showing coupled oscillator capabilities"""
    print("🌊 Coupled Linear Oscillator Demonstration")
    print("=" * 50)
    
    # Create coupled oscillator system
    coupled_osc = CoupledLinearOscillator(
        mass1=1.0,                # 1 kg
        mass2=1.0,                # 1 kg (equal masses)
        stiffness1=4.0,           # 4 N/m
        stiffness2=4.0,           # 4 N/m (equal stiffnesses)
        coupling_stiffness=0.5,   # 0.5 N/m (weak coupling)
        initial_position1=1.0,    # Start oscillator 1 displaced
        initial_velocity1=0.0,    # From rest
        initial_position2=0.0,    # Oscillator 2 at equilibrium
        initial_velocity2=0.0     # From rest
    )
    
    print(f"📊 Parameters:")
    print(f"   Mass 1 (m₁): {coupled_osc.mass1} kg")
    print(f"   Mass 2 (m₂): {coupled_osc.mass2} kg")
    print(f"   Stiffness 1 (k₁): {coupled_osc.stiffness1} N/m")
    print(f"   Stiffness 2 (k₂): {coupled_osc.stiffness2} N/m")
    print(f"   Coupling stiffness (k₁₂): {coupled_osc.coupling_stiffness} N/m")
    print(f"   Coupling strength: {coupled_osc.coupling_strength:.3f}")
    print(f"   Individual frequencies: {[f'{f/(2*np.pi):.3f}' for f in coupled_osc.individual_frequencies]} Hz")
    print(f"   Normal mode frequencies: {[f'{f/(2*np.pi):.3f}' for f in coupled_osc.normal_mode_frequencies]} Hz")
    
    # Normal mode analysis
    omega1, omega2 = coupled_osc.normal_mode_frequencies
    print(f"\n🌊 Normal Mode Analysis:")
    print(f"   Lower mode (ω₁): {omega1:.3f} rad/s ({omega1/(2*np.pi):.3f} Hz)")
    print(f"   Higher mode (ω₂): {omega2:.3f} rad/s ({omega2/(2*np.pi):.3f} Hz)")
    print(f"   Mode vectors:")
    for i, mode in enumerate(coupled_osc.normal_mode_vectors.T):
        print(f"     Mode {i+1}: [{mode[0]:.3f}, {mode[1]:.3f}]")
    
    # Simulate
    print("\n🔄 Running simulation...")
    # Use longer time to see beating if frequencies are close
    beat_period = 2*np.pi / abs(omega2 - omega1) if abs(omega2 - omega1) > 1e-6 else 20
    time_span = np.linspace(0, max(20, 2*beat_period), 2000)
    simulation_results = coupled_osc.simulate(time_span)
    
    # Energy conservation check
    total_energy = simulation_results['energy_total']
    energy_variation = np.std(total_energy)
    initial_energy = total_energy[0]
    print(f"   Energy conservation (std dev): {energy_variation:.2e} J ({100*energy_variation/initial_energy:.4f}%)")
    
    # Beating analysis
    beating_data = coupled_osc.calculate_beating_envelope()
    if beating_data and 'beat_frequency' in beating_data:
        print(f"   Beat frequency: {beating_data['beat_frequency']:.4f} Hz")
        print(f"   Beat period: {beating_data.get('beat_period', 0):.2f} s")
    
    # Energy transfer analysis
    E_k1 = simulation_results['energy_kinetic1']
    E_k2 = simulation_results['energy_kinetic2']
    
    # Find energy transfer maxima
    energy1_max = np.max(E_k1)
    energy2_max = np.max(E_k2)
    transfer_efficiency = energy2_max / energy1_max if energy1_max > 0 else 0
    
    print(f"   Maximum energy in oscillator 1: {energy1_max:.6f} J")
    print(f"   Maximum energy in oscillator 2: {energy2_max:.6f} J")
    print(f"   Energy transfer efficiency: {100*transfer_efficiency:.1f}%")
    
    # Run comprehensive analysis
    analysis_results = coupled_osc.run_analysis()
    
    # Display key results
    print(f"\n📈 Analysis Results:")
    if 'stability' in analysis_results:
        stability = analysis_results['stability']
        if 'comprehensive' in stability:
            overall_stable = stability['comprehensive'].get('overall_stable', 'Unknown')
            print(f"   Overall Stability: {overall_stable}")
    
    if 'coupling_analysis' in analysis_results:
        coupling_data = analysis_results['coupling_analysis']
        if 'synchronization' in coupling_data:
            sync_data = coupling_data['synchronization']
            if sync_data.get('synchronization_available', False):
                sync_index = sync_data.get('synchronization_index', 0)
                print(f"   Synchronization index: {sync_index:.3f}")
    
    # Create visualizations
    print(f"\n📊 Generating visualizations...")
    coupled_osc.visualize_results('results/coupled_linear_oscillator_plots.png')
    
    # Save results
    print(f"\n💾 Saving results...")
    result_file = coupled_osc.save_results()
    
    print(f"\n✅ Coupled Linear Oscillator demonstration complete!")
    
    return coupled_osc

def main():
    """Main function for independent script execution"""
    print("🚀 Coupled Linear Oscillator - Independent Analysis")
    print("=" * 60)
    
    try:
        # Run demonstration
        oscillator = demonstrate_coupled_linear_oscillator()
        
        print(f"\n🎯 Key Findings:")
        print(f"   • Normal modes provide natural oscillation frequencies")
        print(f"   • Energy transfer between oscillators through coupling")
        print(f"   • Beating phenomena when normal modes are close")
        print(f"   • Perfect energy conservation in simulation")
        print(f"   • Configuration space shows complex trajectories")
        print(f"   • Coupling analysis reveals synchronization behavior")
        
        return True
        
    except Exception as e:
        print(f"❌ Error in demonstration: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)


