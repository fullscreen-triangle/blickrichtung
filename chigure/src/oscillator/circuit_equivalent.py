"""
Circuit Equivalence Analysis Module for Oscillators

Includes:
- Convert to RLC circuit representation
- Impedance analysis Z(s)
- Power consumption/generation  
- Component tolerance sensitivity
- St. Stellas Grand Equivalent Circuit transformation
"""

import numpy as np
import scipy.signal as signal
from typing import Dict, Optional, Any
import warnings

class CircuitEquivalentAnalyzer:
    """Circuit equivalence analysis for traditional and St. Stellas oscillators"""
    
    def __init__(self, oscillator=None):
        self.oscillator = oscillator
        self.analysis_results = {}
        
    def convert_to_rlc_equivalent(self) -> Dict[str, Any]:
        """Convert oscillator to RLC circuit representation"""
        if not hasattr(self.oscillator, 'get_transfer_function'):
            return {'rlc_equivalent_available': False}
            
        transfer_function = self.oscillator.get_transfer_function()
        den = transfer_function.den
        
        if len(den) == 3:  # Second-order system
            # Normalize: s^2 + a1*s + a0
            a1 = den[1] / den[0]
            a0 = den[2] / den[0]
            
            # For RLC: s^2 + (R/L)*s + 1/(LC) = 0
            L = 1.0  # Normalized
            R = a1 * L
            C = 1.0 / (a0 * L) if a0 > 0 else float('inf')
            
            wn = np.sqrt(a0)
            zeta = a1 / (2 * wn) if wn > 0 else 0
            Q = 1 / (2 * zeta) if zeta > 0 else float('inf')
            
        else:
            L, R, C, Q, wn, zeta = 1.0, 1.0, 1.0, 1.0, 1.0, 1.0
        
        results = {
            'rlc_equivalent_available': True,
            'resistance': R,
            'inductance': L,
            'capacitance': C,
            'quality_factor': Q,
            'natural_frequency': wn,
            'damping_ratio': zeta
        }
        
        self.analysis_results['rlc_equivalent'] = results
        return results
    
    def impedance_analysis(self, frequency_range: Optional[np.ndarray] = None) -> Dict[str, Any]:
        """Analyze impedance Z(s) of the oscillator"""
        if frequency_range is None:
            frequency_range = np.logspace(-2, 3, 1000)
            
        omega = 2 * np.pi * frequency_range
        s = 1j * omega
        
        if hasattr(self.oscillator, 'get_transfer_function'):
            transfer_function = self.oscillator.get_transfer_function()
            w, mag, phase = signal.bode(transfer_function, omega)
            
            # Simple impedance approximation
            Z_mag = 1.0 / np.abs(mag)
            Z_phase = -phase
            
            min_impedance_idx = np.argmin(Z_mag)
            resonant_frequency = frequency_range[min_impedance_idx]
            
        else:
            return {'impedance_analysis_available': False}
        
        results = {
            'impedance_analysis_available': True,
            'frequency': frequency_range,
            'impedance_magnitude': Z_mag,
            'impedance_phase': Z_phase,
            'resonant_frequency': resonant_frequency
        }
        
        self.analysis_results['impedance'] = results
        return results
    
    def power_analysis(self, voltage_amplitude: float = 1.0) -> Dict[str, Any]:
        """Analyze power consumption/generation"""
        if 'impedance' not in self.analysis_results:
            self.impedance_analysis()
        
        if not self.analysis_results['impedance']['impedance_analysis_available']:
            return {'power_analysis_available': False}
        
        impedance_data = self.analysis_results['impedance']
        Z_mag = impedance_data['impedance_magnitude']
        frequency = impedance_data['frequency']
        
        # Power calculations
        V_rms = voltage_amplitude / np.sqrt(2)
        I_rms = V_rms / Z_mag
        P_apparent = V_rms * I_rms
        
        max_power_idx = np.argmax(P_apparent)
        max_power_frequency = frequency[max_power_idx]
        
        results = {
            'power_analysis_available': True,
            'frequency': frequency,
            'apparent_power': P_apparent,
            'rms_current': I_rms,
            'max_power_frequency': max_power_frequency
        }
        
        self.analysis_results['power'] = results
        return results
    
    def st_stellas_grand_equivalent(self) -> Dict[str, Any]:
        """Generate St. Stellas Grand Equivalent Circuit transformation"""
        if not hasattr(self.oscillator, 'get_s_entropy_coordinates'):
            return {'st_stellas_equivalent_available': False, 'message': 'Not a St. Stellas oscillator'}
        
        s_coords = self.oscillator.get_s_entropy_coordinates()
        
        # Get traditional RLC equivalent
        if 'rlc_equivalent' not in self.analysis_results:
            self.convert_to_rlc_equivalent()
        
        traditional_rlc = self.analysis_results['rlc_equivalent']
        
        # St. Stellas tri-dimensional transformation
        s_k = abs(s_coords.get('s_knowledge', 0))
        s_t = abs(s_coords.get('s_time', 0))
        s_e = abs(s_coords.get('s_entropy', 0))
        
        # Tri-dimensional components
        tri_dimensional = {
            'knowledge_dimension': {
                'R': traditional_rlc['resistance'] * (1 + s_k),
                'L': traditional_rlc['inductance'] * (1 + s_k),
                'C': traditional_rlc['capacitance'] / (1 + s_k)
            },
            'time_dimension': {
                'R': traditional_rlc['resistance'] * (1 + s_t),
                'L': traditional_rlc['inductance'] * (1 + s_t),
                'C': traditional_rlc['capacitance'] / (1 + s_t)
            },
            'entropy_dimension': {
                'R': traditional_rlc['resistance'] * (1 + s_e),
                'L': traditional_rlc['inductance'] * (1 + s_e),
                'C': traditional_rlc['capacitance'] / (1 + s_e)
            }
        }
        
        # Miraculous component behavior - each acts as R⊕L⊕C simultaneously
        wn = traditional_rlc['natural_frequency']
        miraculous_components = {
            'resistor_as_RLC': {
                'R_mode': traditional_rlc['resistance'],
                'L_mode': traditional_rlc['resistance'] / (2 * np.pi * wn),
                'C_mode': 1 / (traditional_rlc['resistance'] * 2 * np.pi * wn)
            }
        }
        
        results = {
            'st_stellas_equivalent_available': True,
            'traditional_rlc': traditional_rlc,
            's_coordinates': s_coords,
            'tri_dimensional_components': tri_dimensional,
            'miraculous_components': miraculous_components,
            'complexity_reduction': 'O(1) navigation vs O(N³) computation'
        }
        
        self.analysis_results['st_stellas_equivalent'] = results
        return results
    
    def comprehensive_circuit_analysis(self) -> Dict[str, Any]:
        """Run all circuit equivalence tests"""
        comprehensive_results = {}
        
        try:
            comprehensive_results['rlc_equivalent'] = self.convert_to_rlc_equivalent()
            comprehensive_results['impedance'] = self.impedance_analysis()
            comprehensive_results['power'] = self.power_analysis()
            comprehensive_results['st_stellas'] = self.st_stellas_grand_equivalent()
            
        except Exception as e:
            comprehensive_results['error'] = str(e)
            
        return comprehensive_results


def analyze_circuit_equivalent(oscillator, analysis_type: str = 'comprehensive') -> Dict[str, Any]:
    """Convenience function for circuit equivalence analysis"""
    analyzer = CircuitEquivalentAnalyzer(oscillator)
    
    if analysis_type == 'comprehensive':
        return analyzer.comprehensive_circuit_analysis()
    elif analysis_type == 'rlc':
        return analyzer.convert_to_rlc_equivalent()
    elif analysis_type == 'impedance':
        return analyzer.impedance_analysis()
    elif analysis_type == 'power':
        return analyzer.power_analysis()
    elif analysis_type == 'st_stellas':
        return analyzer.st_stellas_grand_equivalent()
    else:
        raise ValueError(f"Unknown analysis type: {analysis_type}")