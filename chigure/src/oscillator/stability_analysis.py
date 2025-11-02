"""
Stability Analysis Module for Oscillators

Includes:
- Laplace transform poles/zeros analysis
- Routh-Hurwitz criteria implementation  
- Lyapunov stability for non-linear cases
- Bifurcation analysis
- St. Stellas tri-dimensional stability analysis
"""

import numpy as np
import scipy.signal as signal
import scipy.linalg as linalg
from typing import Dict, List, Tuple, Optional, Any, Union
import warnings

class StabilityAnalyzer:
    """Comprehensive stability analysis for traditional and St. Stellas oscillators"""
    
    def __init__(self, oscillator=None):
        self.oscillator = oscillator
        self.analysis_results = {}
        
    def analyze_poles_zeros(self, transfer_function: Optional[signal.TransferFunction] = None) -> Dict[str, Any]:
        """Analyze poles and zeros of transfer function H(s) = Y(s)/X(s)"""
        if transfer_function is None and hasattr(self.oscillator, 'get_transfer_function'):
            transfer_function = self.oscillator.get_transfer_function()
        elif transfer_function is None:
            raise ValueError("No transfer function provided")
            
        poles = transfer_function.poles
        zeros = transfer_function.zeros
        
        # Stability assessment
        stable = np.all(np.real(poles) < 0)
        marginally_stable = np.any(np.real(poles) == 0) and np.all(np.real(poles) <= 0)
        
        # Damping ratios for complex poles
        damping_ratios = []
        for pole in poles:
            if np.iscomplex(pole):
                natural_freq = np.abs(pole)
                damping_ratio = -np.real(pole) / natural_freq if natural_freq > 0 else 0
                damping_ratios.append(damping_ratio)
        
        results = {
            'poles': poles,
            'zeros': zeros,
            'stable': stable,
            'marginally_stable': marginally_stable,
            'damping_ratios': np.array(damping_ratios),
            'dominant_pole': poles[np.argmin(np.abs(np.real(poles)))] if len(poles) > 0 else None
        }
        
        self.analysis_results['poles_zeros'] = results
        return results
    
    def routh_hurwitz_criterion(self, characteristic_poly: Union[np.ndarray, List[float]]) -> Dict[str, Any]:
        """Apply Routh-Hurwitz stability criterion"""
        if isinstance(characteristic_poly, list):
            characteristic_poly = np.array(characteristic_poly)
            
        n = len(characteristic_poly) - 1
        characteristic_poly = characteristic_poly[characteristic_poly != 0]
        
        if len(characteristic_poly) == 0:
            return {'stable': False, 'routh_table': None, 'sign_changes': float('inf')}
        
        # Construct Routh table
        routh_table = np.zeros((n + 1, (n + 2) // 2))
        
        # Fill first two rows
        routh_table[0, :len(characteristic_poly[::2])] = characteristic_poly[::2]
        if n > 0:
            routh_table[1, :len(characteristic_poly[1::2])] = characteristic_poly[1::2]
        
        # Fill remaining rows
        for i in range(2, n + 1):
            for j in range((n + 1) // 2):
                if j < routh_table.shape[1] - 1 and routh_table[i-1, 0] != 0:
                    routh_table[i, j] = (routh_table[i-1, 0] * routh_table[i-2, j+1] - 
                                       routh_table[i-2, 0] * routh_table[i-1, j+1]) / routh_table[i-1, 0]
        
        # Count sign changes in first column
        first_column = routh_table[:, 0]
        first_column = first_column[first_column != 0]
        sign_changes = np.sum(np.diff(np.sign(first_column)) != 0)
        
        results = {
            'stable': sign_changes == 0,
            'routh_table': routh_table,
            'sign_changes': sign_changes,
            'first_column': first_column
        }
        
        self.analysis_results['routh_hurwitz'] = results
        return results
    
    def lyapunov_stability(self, state_equations: callable, equilibrium: np.ndarray) -> Dict[str, Any]:
        """Analyze Lyapunov stability for nonlinear systems"""
        
        # Numerical Jacobian calculation
        def jacobian_numerical(x, h=1e-8):
            n = len(x)
            J = np.zeros((n, n))
            
            for i in range(n):
                x_plus = x.copy()
                x_minus = x.copy()
                x_plus[i] += h
                x_minus[i] -= h
                
                f_plus = state_equations(x_plus, 0)
                f_minus = state_equations(x_minus, 0)
                
                J[:, i] = (f_plus - f_minus) / (2 * h)
            
            return J
        
        # Calculate Jacobian at equilibrium
        J = jacobian_numerical(equilibrium)
        eigenvalues = linalg.eigvals(J)
        
        # Stability assessment
        asymptotically_stable = np.all(np.real(eigenvalues) < 0)
        stable = np.all(np.real(eigenvalues) <= 0)
        
        results = {
            'jacobian': J,
            'eigenvalues': eigenvalues,
            'asymptotically_stable': asymptotically_stable,
            'stable': stable,
            'equilibrium': equilibrium
        }
        
        self.analysis_results['lyapunov'] = results
        return results
    
    def st_stellas_stability_analysis(self) -> Dict[str, Any]:
        """St. Stellas tri-dimensional stability analysis across S-entropy coordinates"""
        if not hasattr(self.oscillator, 'get_s_entropy_coordinates'):
            return {'s_entropy_stable': False, 'message': 'Not a St. Stellas oscillator'}
        
        # Get S-entropy coordinates
        s_coords = self.oscillator.get_s_entropy_coordinates()
        s_knowledge = s_coords.get('s_knowledge', 0)
        s_time = s_coords.get('s_time', 0)  
        s_entropy = s_coords.get('s_entropy', 0)
        
        # St. Stellas stability criteria - S-distance minimization
        s_distance = np.sqrt(s_knowledge**2 + s_time**2 + s_entropy**2)
        
        # Tri-dimensional oscillatory coherence
        max_coord = max(abs(s_knowledge), abs(s_time), abs(s_entropy))
        coherence = 1.0 / (1.0 + np.var([s_knowledge, s_time, s_entropy])) if max_coord > 0 else 1.0
        
        # St. Stellas stability conditions
        s_stable = s_distance < 1.0
        coherence_stable = coherence > 0.8
        
        results = {
            's_entropy_stable': s_stable and coherence_stable,
            's_distance': s_distance,
            'oscillatory_coherence': coherence,
            's_coordinates': s_coords,
            'tri_dimensional_stable': {
                's_knowledge_stable': abs(s_knowledge) < 0.5,
                's_time_stable': abs(s_time) < 0.5,
                's_entropy_stable': abs(s_entropy) < 0.5
            }
        }
        
        self.analysis_results['st_stellas_stability'] = results
        return results
    
    def comprehensive_stability_analysis(self) -> Dict[str, Any]:
        """Run all stability tests and return comprehensive results"""
        comprehensive_results = {}
        
        try:
            # Traditional stability analysis
            if hasattr(self.oscillator, 'get_transfer_function'):
                comprehensive_results['poles_zeros'] = self.analyze_poles_zeros()
                
            if hasattr(self.oscillator, 'get_characteristic_polynomial'):
                char_poly = self.oscillator.get_characteristic_polynomial()
                comprehensive_results['routh_hurwitz'] = self.routh_hurwitz_criterion(char_poly)
                
            if hasattr(self.oscillator, 'get_state_equations'):
                state_eq = self.oscillator.get_state_equations()
                equilibrium = self.oscillator.get_equilibrium() if hasattr(self.oscillator, 'get_equilibrium') else np.zeros(2)
                comprehensive_results['lyapunov'] = self.lyapunov_stability(state_eq, equilibrium)
                
            # St. Stellas stability analysis
            comprehensive_results['st_stellas'] = self.st_stellas_stability_analysis()
            
            # Overall stability assessment
            overall_stable = True
            for key in ['poles_zeros', 'routh_hurwitz', 'lyapunov']:
                if key in comprehensive_results:
                    overall_stable &= comprehensive_results[key]['stable']
            if 'st_stellas' in comprehensive_results:
                overall_stable &= comprehensive_results['st_stellas']['s_entropy_stable']
                
            comprehensive_results['overall_stable'] = overall_stable
            
        except Exception as e:
            comprehensive_results['error'] = str(e)
            comprehensive_results['overall_stable'] = False
            
        self.analysis_results['comprehensive'] = comprehensive_results
        return comprehensive_results


def analyze_stability(oscillator, analysis_type: str = 'comprehensive') -> Dict[str, Any]:
    """
    Convenience function for stability analysis
    
    Args:
        oscillator: Oscillator object to analyze
        analysis_type: Type of analysis ('comprehensive', 'poles_zeros', 'routh_hurwitz', 'lyapunov', 'st_stellas')
        
    Returns:
        Dict containing analysis results
    """
    analyzer = StabilityAnalyzer(oscillator)
    
    if analysis_type == 'comprehensive':
        return analyzer.comprehensive_stability_analysis()
    elif analysis_type == 'poles_zeros':
        return analyzer.analyze_poles_zeros()
    elif analysis_type == 'routh_hurwitz':
        char_poly = oscillator.get_characteristic_polynomial()
        return analyzer.routh_hurwitz_criterion(char_poly)
    elif analysis_type == 'lyapunov':
        state_eq = oscillator.get_state_equations()
        equilibrium = oscillator.get_equilibrium() if hasattr(oscillator, 'get_equilibrium') else np.zeros(2)
        return analyzer.lyapunov_stability(state_eq, equilibrium)
    elif analysis_type == 'st_stellas':
        return analyzer.st_stellas_stability_analysis()
    else:
        raise ValueError(f"Unknown analysis type: {analysis_type}")