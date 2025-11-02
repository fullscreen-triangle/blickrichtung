"""
Coupling Analysis Module for Oscillators

Includes:
- Synchronization analysis
- Phase-locking behavior
- Coupling strength effects
- Multi-oscillator stability
- St. Stellas cross-dimensional coupling
"""

import numpy as np
from scipy.integrate import solve_ivp
from typing import Dict, List, Optional, Any
import warnings

class CouplingAnalyzer:
    """Coupling analysis for traditional and St. Stellas oscillators"""
    
    def __init__(self, oscillators=None):
        self.oscillators = oscillators if isinstance(oscillators, list) else [oscillators] if oscillators else []
        self.analysis_results = {}
        
    def synchronization_analysis(self, coupling_strength: float = 0.1) -> Dict[str, Any]:
        """Analyze synchronization between coupled oscillators"""
        if len(self.oscillators) < 2:
            return {'synchronization_available': False, 'message': 'Need at least 2 oscillators'}
        
        # Simulate simple coupled system
        t_span = np.linspace(0, 50, 5000)
        
        if all(hasattr(osc, 'get_state_equations') for osc in self.oscillators):
            # Get initial conditions
            initial_conditions = []
            for osc in self.oscillators:
                ic = getattr(osc, 'get_initial_conditions', lambda: np.array([1.0, 0.0]))()
                initial_conditions.extend(ic)
            
            # Simple coupled system dynamics
            def coupled_system(t, y):
                n_per_osc = 2  # Assume 2 states per oscillator
                dydt = np.zeros_like(y)
                
                for i in range(len(self.oscillators)):
                    start = i * n_per_osc
                    end = (i + 1) * n_per_osc
                    y_i = y[start:end]
                    
                    # Individual dynamics
                    eq = self.oscillators[i].get_state_equations()
                    dydt_i = eq(y_i, t)
                    
                    # Add coupling
                    for j in range(len(self.oscillators)):
                        if i != j:
                            j_start = j * n_per_osc
                            y_j = y[j_start:j_start+n_per_osc]
                            dydt_i[1] += coupling_strength * (y_j[0] - y_i[0])
                    
                    dydt[start:end] = dydt_i
                
                return dydt
            
            sol = solve_ivp(coupled_system, [0, 50], initial_conditions, t_eval=t_span)
            
            # Extract trajectories
            n_per_osc = 2
            trajectories = []
            for i in range(len(self.oscillators)):
                start = i * n_per_osc
                trajectory = sol.y[start, :]  # Position only
                trajectories.append(trajectory)
            
            # Calculate synchronization metrics
            sync_index = self._calculate_sync_index(trajectories)
            
        else:
            return {'synchronization_available': False, 'message': 'No state equations'}
        
        results = {
            'synchronization_available': True,
            'time': sol.t,
            'trajectories': trajectories,
            'synchronization_index': sync_index,
            'coupling_strength': coupling_strength
        }
        
        self.analysis_results['synchronization'] = results
        return results
    
    def phase_locking_analysis(self) -> Dict[str, Any]:
        """Analyze phase-locking behavior"""
        if 'synchronization' not in self.analysis_results:
            self.synchronization_analysis()
        
        sync_data = self.analysis_results['synchronization']
        if not sync_data['synchronization_available']:
            return {'phase_locking_available': False}
        
        trajectories = sync_data['trajectories']
        
        # Calculate phases using Hilbert transform
        from scipy.signal import hilbert
        phases = []
        for traj in trajectories:
            analytic = hilbert(traj)
            phase = np.unwrap(np.angle(analytic))
            phases.append(phase)
        
        # Phase differences
        phase_diffs = []
        for i in range(len(phases)):
            for j in range(i+1, len(phases)):
                diff = phases[i] - phases[j]
                phase_diffs.append(diff)
        
        # Check locking (constant phase difference)
        locking_metrics = {}
        for idx, diff in enumerate(phase_diffs):
            std_dev = np.std(diff[-1000:])  # Last 1000 points
            is_locked = std_dev < 0.1
            
            locking_metrics[f'pair_{idx}'] = {
                'phase_std': std_dev,
                'is_locked': is_locked
            }
        
        results = {
            'phase_locking_available': True,
            'phases': phases,
            'phase_differences': phase_diffs,
            'locking_metrics': locking_metrics
        }
        
        self.analysis_results['phase_locking'] = results
        return results
    
    def st_stellas_cross_dimensional_coupling(self) -> Dict[str, Any]:
        """Analyze St. Stellas cross-dimensional coupling"""
        st_stellas_oscs = [osc for osc in self.oscillators if hasattr(osc, 'get_s_entropy_coordinates')]
        
        if len(st_stellas_oscs) == 0:
            return {'st_stellas_coupling_available': False, 'message': 'No St. Stellas oscillators'}
        
        # Get S-entropy coordinates
        s_coordinates = []
        for osc in st_stellas_oscs:
            s_coords = osc.get_s_entropy_coordinates()
            s_coordinates.append(s_coords)
        
        # Calculate cross-dimensional coupling
        n_oscs = len(st_stellas_oscs)
        coupling_matrix = np.zeros((n_oscs * 3, n_oscs * 3))  # 3 S-dimensions per oscillator
        
        for i in range(n_oscs):
            for j in range(n_oscs):
                if i != j:
                    # Calculate S-distance between oscillators
                    s_i = list(s_coordinates[i].values())
                    s_j = list(s_coordinates[j].values())
                    s_distance = np.linalg.norm(np.array(s_i) - np.array(s_j))
                    
                    # Coupling strength inversely related to S-distance
                    coupling_strength = 0.1 / (1 + s_distance)
                    
                    # Fill coupling matrix
                    for dim in range(3):
                        row = i * 3 + dim
                        col = j * 3 + dim
                        coupling_matrix[row, col] = coupling_strength
        
        # BMD equivalence analysis
        variance_states = []
        for s_coords in s_coordinates:
            s_k = s_coords.get('s_knowledge', 0)
            s_t = s_coords.get('s_time', 0)
            s_e = s_coords.get('s_entropy', 0)
            variance_state = s_k**2 + s_t**2 + s_e**2
            variance_states.append(variance_state)
        
        variance_std = np.std(variance_states)
        bmd_equivalent = variance_std < 0.1
        
        results = {
            'st_stellas_coupling_available': True,
            'n_oscillators': n_oscs,
            's_coordinates': s_coordinates,
            'coupling_matrix': coupling_matrix,
            'bmd_equivalence': bmd_equivalent,
            'variance_states': variance_states
        }
        
        self.analysis_results['st_stellas_coupling'] = results
        return results
    
    def _calculate_sync_index(self, trajectories: List[np.ndarray]) -> float:
        """Calculate synchronization index"""
        if len(trajectories) < 2:
            return 0.0
        
        correlations = []
        for i in range(len(trajectories)):
            for j in range(i+1, len(trajectories)):
                corr = np.corrcoef(trajectories[i], trajectories[j])[0, 1]
                correlations.append(corr)
        
        return np.mean(correlations)
    
    def comprehensive_coupling_analysis(self) -> Dict[str, Any]:
        """Run all coupling tests"""
        comprehensive_results = {}
        
        try:
            comprehensive_results['synchronization'] = self.synchronization_analysis()
            comprehensive_results['phase_locking'] = self.phase_locking_analysis()
            comprehensive_results['st_stellas_coupling'] = self.st_stellas_cross_dimensional_coupling()
            
        except Exception as e:
            comprehensive_results['error'] = str(e)
            
        return comprehensive_results


def analyze_coupling(oscillators, analysis_type: str = 'comprehensive') -> Dict[str, Any]:
    """Convenience function for coupling analysis"""
    analyzer = CouplingAnalyzer(oscillators)
    
    if analysis_type == 'comprehensive':
        return analyzer.comprehensive_coupling_analysis()
    elif analysis_type == 'synchronization':
        return analyzer.synchronization_analysis()
    elif analysis_type == 'phase_locking':
        return analyzer.phase_locking_analysis()
    elif analysis_type == 'st_stellas':
        return analyzer.st_stellas_cross_dimensional_coupling()
    else:
        raise ValueError(f"Unknown analysis type: {analysis_type}")