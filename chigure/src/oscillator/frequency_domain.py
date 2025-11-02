"""
Frequency Domain Analysis Module for Oscillators

Includes:
- Transfer function H(s) = Y(s)/X(s) analysis
- Bode plots (magnitude/phase) 
- Nyquist stability criterion
- Frequency response validation
- St. Stellas tri-dimensional frequency response
"""

import numpy as np
import scipy.signal as signal
import matplotlib.pyplot as plt
from typing import Dict, Optional, Any
import warnings

class FrequencyDomainAnalyzer:
    """Frequency domain analysis for traditional and St. Stellas oscillators"""
    
    def __init__(self, oscillator=None):
        self.oscillator = oscillator
        self.analysis_results = {}
        
    def analyze_transfer_function(self, transfer_function: Optional[signal.TransferFunction] = None) -> Dict[str, Any]:
        """Analyze transfer function H(s) = Y(s)/X(s)"""
        if transfer_function is None:
            transfer_function = self.oscillator.get_transfer_function()
            
        # Extract key properties
        poles = transfer_function.poles
        zeros = transfer_function.zeros
        dc_gain = transfer_function.dcgain if hasattr(transfer_function, 'dcgain') else transfer_function.num[-1]/transfer_function.den[-1]
        
        # For 2nd order systems, extract natural frequency and damping
        if len(poles) == 2:
            den = transfer_function.den
            wn_squared = den[-1] / den[0]
            natural_frequency = np.sqrt(wn_squared) if wn_squared > 0 else 0
            damping_ratio = den[-2] / (2 * den[0] * natural_frequency) if natural_frequency > 0 else 0
        else:
            natural_frequency = damping_ratio = 0
        
        results = {
            'transfer_function': transfer_function,
            'poles': poles,
            'zeros': zeros,
            'dc_gain': dc_gain,
            'natural_frequency': natural_frequency,
            'damping_ratio': damping_ratio
        }
        
        self.analysis_results['transfer_function'] = results
        return results
    
    def generate_bode_plot(self, frequency_range: Optional[np.ndarray] = None) -> Dict[str, Any]:
        """Generate Bode plots (magnitude and phase)"""
        transfer_function = self.oscillator.get_transfer_function()
        
        if frequency_range is None:
            frequency_range = np.logspace(-2, 3, 1000)
            
        # Calculate frequency response
        w, mag, phase = signal.bode(transfer_function, frequency_range)
        mag_db = 20 * np.log10(np.abs(mag))
        phase_deg = np.degrees(phase)
        
        # Find -3dB bandwidth
        mag_3db = np.max(mag_db) - 3
        bandwidth_indices = np.where(mag_db >= mag_3db)[0]
        bandwidth = w[bandwidth_indices[-1]] - w[bandwidth_indices[0]] if len(bandwidth_indices) > 1 else 0
        
        # Gain and phase margins
        gain_margin, phase_margin, gm_freq, pm_freq = signal.margin(transfer_function)
        
        results = {
            'frequency': w,
            'magnitude_db': mag_db,
            'phase_deg': phase_deg,
            'bandwidth': bandwidth,
            'gain_margin': gain_margin,
            'phase_margin': phase_margin
        }
        
        self.analysis_results['bode'] = results
        return results
    
    def nyquist_analysis(self) -> Dict[str, Any]:
        """Perform Nyquist stability analysis"""
        transfer_function = self.oscillator.get_transfer_function()
        
        # Generate frequency range and calculate response
        w = np.logspace(-3, 3, 1000)
        w_nyquist, H_nyquist = signal.freqresp(transfer_function, w)
        
        # Check encirclements of -1+0j point (simplified)
        critical_point = -1 + 0j
        angles = np.angle(H_nyquist - critical_point)
        total_angle_change = np.sum(np.diff(np.unwrap(angles)))
        encirclements = int(np.round(total_angle_change / (2 * np.pi)))
        
        results = {
            'frequency': w_nyquist,
            'real_part': np.real(H_nyquist),
            'imaginary_part': np.imag(H_nyquist),
            'encirclements': encirclements,
            'stable': encirclements == 0
        }
        
        self.analysis_results['nyquist'] = results
        return results
    
    def st_stellas_frequency_analysis(self) -> Dict[str, Any]:
        """St. Stellas tri-dimensional frequency response analysis"""
        if not hasattr(self.oscillator, 'get_s_entropy_coordinates'):
            return {'s_entropy_frequency_response': False, 'message': 'Not a St. Stellas oscillator'}
        
        s_coords = self.oscillator.get_s_entropy_coordinates()
        
        # Generate default S-transfer function matrix for three dimensions
        s = 1j * np.logspace(-2, 3, 100)
        s_knowledge = s_coords.get('s_knowledge', 0)
        s_time = s_coords.get('s_time', 0)
        s_entropy = s_coords.get('s_entropy', 0)
        
        # Simple transfer functions for each S-dimension
        omega_k = 1.0 + abs(s_knowledge)
        omega_t = 2.0 + abs(s_time)
        omega_e = 0.5 + abs(s_entropy)
        
        H_kk = omega_k**2 / (s**2 + 0.1*omega_k*s + omega_k**2)
        H_tt = omega_t**2 / (s**2 + 0.2*omega_t*s + omega_t**2)
        H_ee = omega_e**2 / (s**2 + 0.3*omega_e*s + omega_e**2)
        
        # Analyze each dimension
        dimension_analysis = {
            's_knowledge': {'magnitude': np.abs(H_kk), 'phase': np.angle(H_kk)},
            's_time': {'magnitude': np.abs(H_tt), 'phase': np.angle(H_tt)},
            's_entropy': {'magnitude': np.abs(H_ee), 'phase': np.angle(H_ee)}
        }
        
        results = {
            's_entropy_frequency_response': True,
            'dimension_analysis': dimension_analysis,
            's_coordinates': s_coords,
            'frequency_range': np.imag(s)
        }
        
        self.analysis_results['st_stellas_frequency'] = results
        return results
    
    def comprehensive_frequency_analysis(self) -> Dict[str, Any]:
        """Run all frequency domain tests"""
        comprehensive_results = {}
        
        try:
            if hasattr(self.oscillator, 'get_transfer_function'):
                comprehensive_results['transfer_function'] = self.analyze_transfer_function()
                comprehensive_results['bode'] = self.generate_bode_plot()
                comprehensive_results['nyquist'] = self.nyquist_analysis()
                
            comprehensive_results['st_stellas'] = self.st_stellas_frequency_analysis()
            
        except Exception as e:
            comprehensive_results['error'] = str(e)
            
        self.analysis_results['comprehensive'] = comprehensive_results
        return comprehensive_results


def analyze_frequency_domain(oscillator, analysis_type: str = 'comprehensive') -> Dict[str, Any]:
    """
    Convenience function for frequency domain analysis
    
    Args:
        oscillator: Oscillator object to analyze
        analysis_type: 'comprehensive', 'transfer_function', 'bode', 'nyquist', 'st_stellas'
    """
    analyzer = FrequencyDomainAnalyzer(oscillator)
    
    if analysis_type == 'comprehensive':
        return analyzer.comprehensive_frequency_analysis()
    elif analysis_type == 'transfer_function':
        return analyzer.analyze_transfer_function()
    elif analysis_type == 'bode':
        return analyzer.generate_bode_plot()
    elif analysis_type == 'nyquist':
        return analyzer.nyquist_analysis()
    elif analysis_type == 'st_stellas':
        return analyzer.st_stellas_frequency_analysis()
    else:
        raise ValueError(f"Unknown analysis type: {analysis_type}")