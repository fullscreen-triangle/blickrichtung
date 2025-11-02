"""
Time Domain Analysis Module for Oscillators

Includes:
- Step response analysis
- Impulse response analysis  
- Free oscillation decay
- Forced response amplitude/phase
- St. Stellas time domain analysis
"""

import numpy as np
import scipy.signal as signal
from scipy.integrate import solve_ivp
from typing import Dict, Optional, Any
import warnings

class TimeDomainAnalyzer:
    """Time domain analysis for traditional and St. Stellas oscillators"""
    
    def __init__(self, oscillator=None):
        self.oscillator = oscillator
        self.analysis_results = {}
        
    def step_response_analysis(self, time_span: Optional[np.ndarray] = None) -> Dict[str, Any]:
        """Analyze step response of the oscillator"""
        if time_span is None:
            time_span = np.linspace(0, 10, 1000)
            
        if hasattr(self.oscillator, 'get_transfer_function'):
            transfer_function = self.oscillator.get_transfer_function()
            t, y = signal.step(transfer_function, T=time_span)
            
            # Calculate metrics
            final_value = y[-1]
            rise_time = self._calculate_rise_time(t, y)
            settling_time = self._calculate_settling_time(t, y, final_value)
            overshoot = self._calculate_overshoot(y, final_value)
            
        else:
            warnings.warn("No step response capability")
            return {'step_response_available': False}
        
        results = {
            'time': t,
            'response': y,
            'final_value': final_value,
            'rise_time': rise_time,
            'settling_time': settling_time,
            'overshoot': overshoot
        }
        
        self.analysis_results['step_response'] = results
        return results
    
    def impulse_response_analysis(self, time_span: Optional[np.ndarray] = None) -> Dict[str, Any]:
        """Analyze impulse response of the oscillator"""
        if time_span is None:
            time_span = np.linspace(0, 10, 1000)
            
        if hasattr(self.oscillator, 'get_transfer_function'):
            transfer_function = self.oscillator.get_transfer_function()
            t, y = signal.impulse(transfer_function, T=time_span)
            
            peak_value = np.max(np.abs(y))
            peak_time = t[np.argmax(np.abs(y))]
            energy = np.trapezoid(y**2, t)
            
        else:
            warnings.warn("No impulse response capability")
            return {'impulse_response_available': False}
        
        results = {
            'time': t,
            'response': y,
            'peak_value': peak_value,
            'peak_time': peak_time,
            'energy': energy
        }
        
        self.analysis_results['impulse_response'] = results
        return results
    
    def free_oscillation_analysis(self, initial_conditions: Optional[np.ndarray] = None,
                                time_span: Optional[np.ndarray] = None) -> Dict[str, Any]:
        """Analyze free oscillation decay characteristics"""
        if time_span is None:
            time_span = np.linspace(0, 20, 2000)
        if initial_conditions is None:
            initial_conditions = np.array([1.0, 0.0])
            
        if hasattr(self.oscillator, 'get_state_equations'):
            state_equations = self.oscillator.get_state_equations()
            
            def ode_system(t, y):
                return state_equations(y, t)
            
            sol = solve_ivp(ode_system, [time_span[0], time_span[-1]], 
                          initial_conditions, t_eval=time_span)
            
            t = sol.t
            y = sol.y[0]  # Position
            
            # Analyze characteristics
            frequency = self._estimate_frequency(t, y)
            envelope = self._extract_envelope(t, y)
            decay_rate = self._estimate_decay_rate(t, envelope)
            
        else:
            warnings.warn("No free oscillation capability")
            return {'free_oscillation_available': False}
        
        results = {
            'time': t,
            'response': y,
            'envelope': envelope,
            'frequency': frequency,
            'decay_rate': decay_rate
        }
        
        self.analysis_results['free_oscillation'] = results
        return results
    
    def st_stellas_time_analysis(self) -> Dict[str, Any]:
        """St. Stellas tri-dimensional time domain analysis"""
        if not hasattr(self.oscillator, 'get_s_entropy_coordinates'):
            return {'s_entropy_time_response': False, 'message': 'Not a St. Stellas oscillator'}
        
        s_coords = self.oscillator.get_s_entropy_coordinates()
        t_span = np.linspace(0, 10, 1000)
        
        # Default S-entropy evolution (exponential convergence)
        s_k0 = s_coords.get('s_knowledge', 0)
        s_t0 = s_coords.get('s_time', 0)
        s_e0 = s_coords.get('s_entropy', 0)
        
        tau_k, tau_t, tau_e = 2.0, 1.5, 3.0
        
        s_knowledge_evolution = s_k0 * np.exp(-t_span / tau_k)
        s_time_evolution = s_t0 * np.exp(-t_span / tau_t)
        s_entropy_evolution = s_e0 * np.exp(-t_span / tau_e)
        
        s_distance_evolution = np.sqrt(s_knowledge_evolution**2 + s_time_evolution**2 + s_entropy_evolution**2)
        
        # Equilibrium time
        initial_distance = s_distance_evolution[0]
        if initial_distance > 0:
            eq_indices = np.where(s_distance_evolution < 0.01 * initial_distance)[0]
            equilibrium_time = t_span[eq_indices[0]] if len(eq_indices) > 0 else t_span[-1]
        else:
            equilibrium_time = 0
        
        results = {
            's_entropy_time_response': True,
            'time': t_span,
            's_knowledge_evolution': s_knowledge_evolution,
            's_time_evolution': s_time_evolution,
            's_entropy_evolution': s_entropy_evolution,
            's_distance_evolution': s_distance_evolution,
            'equilibrium_time': equilibrium_time
        }
        
        self.analysis_results['st_stellas_time'] = results
        return results
    
    def _calculate_rise_time(self, t: np.ndarray, y: np.ndarray) -> float:
        """Calculate 10%-90% rise time"""
        final_value = y[-1]
        y_10 = 0.1 * final_value
        y_90 = 0.9 * final_value
        
        idx_10 = np.argmax(y >= y_10)
        idx_90 = np.argmax(y >= y_90)
        
        return t[idx_90] - t[idx_10] if idx_90 > idx_10 else 0
    
    def _calculate_settling_time(self, t: np.ndarray, y: np.ndarray, final_value: float) -> float:
        """Calculate settling time (within 2% of final value)"""
        tolerance = 0.02
        error = np.abs(y - final_value) / np.abs(final_value) if final_value != 0 else np.abs(y)
        settled_indices = np.where(error <= tolerance)[0]
        return t[settled_indices[0]] if len(settled_indices) > 0 else t[-1]
    
    def _calculate_overshoot(self, y: np.ndarray, final_value: float) -> float:
        """Calculate percentage overshoot"""
        peak_value = np.max(y)
        overshoot = ((peak_value - final_value) / final_value) * 100 if final_value != 0 else 0
        return max(0, overshoot)
    
    def _extract_envelope(self, t: np.ndarray, y: np.ndarray) -> np.ndarray:
        """Extract oscillation envelope"""
        from scipy.signal import find_peaks
        peaks, _ = find_peaks(np.abs(y))
        
        if len(peaks) > 1:
            envelope = np.interp(t, t[peaks], np.abs(y[peaks]))
        else:
            envelope = np.abs(y)
            
        return envelope
    
    def _estimate_frequency(self, t: np.ndarray, y: np.ndarray) -> float:
        """Estimate oscillation frequency using zero crossings"""
        zero_crossings = np.where(np.diff(np.sign(y)))[0]
        
        if len(zero_crossings) > 2:
            crossing_times = t[zero_crossings]
            period = 2 * np.mean(np.diff(crossing_times))
            frequency = 1 / period if period > 0 else 0
        else:
            frequency = 0
            
        return frequency
    
    def _estimate_decay_rate(self, t: np.ndarray, envelope: np.ndarray) -> float:
        """Estimate exponential decay rate"""
        if len(envelope) < 10 or np.max(envelope) <= 0:
            return 0
            
        log_envelope = np.log(np.maximum(envelope, 1e-10))
        coeffs = np.polyfit(t, log_envelope, 1)
        decay_rate = -coeffs[0]
        
        return max(0, decay_rate)
    
    def comprehensive_time_analysis(self) -> Dict[str, Any]:
        """Run all time domain tests"""
        comprehensive_results = {}
        
        try:
            comprehensive_results['step_response'] = self.step_response_analysis()
            comprehensive_results['impulse_response'] = self.impulse_response_analysis()
            comprehensive_results['free_oscillation'] = self.free_oscillation_analysis()
            comprehensive_results['st_stellas'] = self.st_stellas_time_analysis()
            
        except Exception as e:
            comprehensive_results['error'] = str(e)
            
        return comprehensive_results


def analyze_time_domain(oscillator, analysis_type: str = 'comprehensive') -> Dict[str, Any]:
    """Convenience function for time domain analysis"""
    analyzer = TimeDomainAnalyzer(oscillator)
    
    if analysis_type == 'comprehensive':
        return analyzer.comprehensive_time_analysis()
    elif analysis_type == 'step':
        return analyzer.step_response_analysis()
    elif analysis_type == 'impulse':
        return analyzer.impulse_response_analysis()
    elif analysis_type == 'free':
        return analyzer.free_oscillation_analysis()
    elif analysis_type == 'st_stellas':
        return analyzer.st_stellas_time_analysis()
    else:
        raise ValueError(f"Unknown analysis type: {analysis_type}")