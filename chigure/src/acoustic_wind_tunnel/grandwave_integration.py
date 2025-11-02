"""
GrandWave Integration for Acoustic Wind Tunnel
===============================================

Connects acoustic measurements to the universal substrate.
"""

import numpy as np
from typing import Dict, Optional
import sys

from src.instruments.acoustic_wind_tunnel import SAcousticMapper
from src.instruments.grand_unification import GrandWave, WaveInterface, WaveDisturbance

sys.path.append('../../grand_unification')



class AcousticGrandWaveConnector:
    """
    Integrates acoustic wind tunnel with GrandWave substrate
    """
    
    def __init__(self, grand_wave: Optional[GrandWave] = None):
        """
        Initialize connector
        
        Args:
            grand_wave: Existing GrandWave instance or create new one
        """
        if grand_wave is None:
            self.grand_wave = GrandWave(
                frequency_range=(0.1, 1e6),  # Hz, covers acoustic range
                n_basis_functions=10000,
                trans_planckian_precision=7.51e-50
            )
        else:
            self.grand_wave = grand_wave
            
        # Create interface for acoustic measurements
        self.interface = WaveInterface(
            object_id="acoustic_wind_tunnel",
            grand_wave=self.grand_wave,
            domain="acoustic"
        )
        
        # S-entropy mapper
        self.s_mapper = SAcousticMapper()
        
    def announce_measurement(self,
                            measurement_id: str,
                            pressure_field: np.ndarray,
                            timestamps: np.ndarray,
                            mic_positions: np.ndarray,
                            duration: float = 0.5) -> WaveDisturbance:
        """
        Announce acoustic measurement to GrandWave
        
        Args:
            measurement_id: Unique identifier for measurement
            pressure_field: Pressure at each mic (n_mics, n_samples)
            timestamps: Time vector
            mic_positions: Microphone positions
            duration: Measurement duration (s)
            
        Returns:
            WaveDisturbance created in GrandWave
        """
        # Extract oscillatory signature
        signature = self.s_mapper.extract_acoustic_signature(
            pressure_field,
            timestamps,
            mic_positions
        )
        
        # Calculate S-entropy coordinates
        S_coords = self.s_mapper.calculate_s_entropy(signature)
        
        # Announce to GrandWave
        disturbance = self.interface.announce(
            S_coords,
            signature,
            duration=duration
        )
        
        return disturbance
        
    def find_equivalent_measurements(self,
                                    S_coords: np.ndarray,
                                    threshold: float = 0.1) -> Dict:
        """
        Find measurements equivalent to given S-coords
        
        Args:
            S_coords: S-entropy coordinates to search for
            threshold: S-distance threshold for equivalence
            
        Returns:
            Equivalent measurements from any domain
        """
        # Use GrandWave to find equivalent disturbances
        equivalent = self.grand_wave.find_equivalent_disturbances(
            S_coords,
            threshold=threshold
        )
        
        # Separate by domain
        by_domain = {}
        for dist in equivalent:
            domain = dist.domain
            if domain not in by_domain:
                by_domain[domain] = []
            by_domain[domain].append(dist)
            
        return {
            'equivalent_disturbances': equivalent,
            'by_domain': by_domain,
            'n_total': len(equivalent),
            'n_acoustic': len(by_domain.get('acoustic', [])),
            'n_optical': len(by_domain.get('optical', [])),
            'n_other': sum(len(v) for k, v in by_domain.items() 
                          if k not in ['acoustic', 'optical'])
        }
        
    def cross_domain_optimization(self,
                                 target_property: str,
                                 target_value: float,
                                 current_S: np.ndarray) -> Dict:
        """
        Find optimal solution using cross-domain equivalence
        
        Args:
            target_property: Property to optimize (e.g., 'drag_coefficient')
            target_value: Target value
            current_S: Current S-entropy position
            
        Returns:
            Optimization suggestions from all domains
        """
        # Listen for relevant disturbances
        nearby = self.interface.listen()
        
        # Get optimization suggestions
        suggestions = self.interface.suggest_optimization(
            target_property,
            target_value
        )
        
        # Check which suggestions are accessible
        accessible = []
        for S_suggestion in suggestions:
            # Calculate navigation path
            nav = self.grand_wave.navigate_to_target(current_S, S_suggestion)
            
            if nav['viability'] > 0.7:  # Accessible
                accessible.append({
                    'S_coords': S_suggestion,
                    'distance': nav['S_distance'],
                    'coherence': nav['coherence'],
                    'viability': nav['viability']
                })
                
        return {
            'suggestions': suggestions,
            'accessible': accessible,
            'n_suggestions': len(suggestions),
            'n_accessible': len(accessible)
        }
        
    def dual_validation_acoustic(self,
                                measurement: Dict,
                                S_coords: np.ndarray) -> Dict:
        """
        Prepare acoustic measurement for dual validation
        
        Args:
            measurement: Raw acoustic measurement data
            S_coords: S-entropy coordinates
            
        Returns:
            Data formatted for dual validation
        """
        # Oscillatory pathway (already done via S-coords)
        oscillatory_result = {
            'S_coords': S_coords,
            'domain': 'acoustic',
            'frequencies': measurement.get('frequencies', []),
            'amplitudes': measurement.get('amplitudes', []),
            'velocity_field': measurement.get('velocity_field', None)
        }
        
        # Visual pathway preparation
        # (Will be validated via visual_pathway module in grand_unification)
        visual_ready = {
            'S_coords': S_coords,
            'domain': 'acoustic',
            'ready_for_droplet_simulation': True
        }
        
        return {
            'oscillatory_result': oscillatory_result,
            'visual_ready': visual_ready,
            'requires_validation': True
        }
        
    def get_transcendent_view(self) -> Dict:
        """
        Get simultaneous view of all acoustic measurements in GrandWave
        
        Returns:
            Transcendent observer view
        """
        view = self.grand_wave.get_transcendent_view()
        
        # Filter for acoustic measurements
        acoustic_only = [
            d for d in view['all_disturbances'] 
            if d.domain == 'acoustic'
        ]
        
        return {
            'all_measurements': view,
            'acoustic_measurements': acoustic_only,
            'n_acoustic': len(acoustic_only),
            'acoustic_frequency_range': self._get_frequency_range(acoustic_only),
            'acoustic_S_range': self._get_S_range(acoustic_only)
        }
        
    def _get_frequency_range(self, disturbances: list) -> tuple:
        """Get frequency range of disturbances"""
        if not disturbances:
            return (0, 0)
            
        all_freqs = []
        for d in disturbances:
            all_freqs.extend(d.frequencies)
            
        return (min(all_freqs), max(all_freqs))
        
    def _get_S_range(self, disturbances: list) -> Dict:
        """Get S-entropy range of disturbances"""
        if not disturbances:
            return {'S1': (0, 0), 'S2': (0, 0), 'S3': (0, 0)}
            
        S_coords = np.array([d.S_coords for d in disturbances])
        
        return {
            'S1': (S_coords[:, 0].min(), S_coords[:, 0].max()),
            'S2': (S_coords[:, 1].min(), S_coords[:, 1].max()),
            'S3': (S_coords[:, 2].min(), S_coords[:, 2].max())
        }
        
    def measure_with_grandwave(self,
                              measurement_id: str,
                              pressure_field: np.ndarray,
                              timestamps: np.ndarray,
                              mic_positions: np.ndarray) -> Dict:
        """
        Complete measurement workflow with GrandWave integration
        
        Args:
            measurement_id: Measurement identifier
            pressure_field: Acoustic pressure field
            timestamps: Time vector
            mic_positions: Microphone positions
            
        Returns:
            Complete measurement with GrandWave context
        """
        # 1. Announce measurement
        disturbance = self.announce_measurement(
            measurement_id,
            pressure_field,
            timestamps,
            mic_positions
        )
        
        # 2. Find equivalent measurements
        equivalent = self.find_equivalent_measurements(
            disturbance.S_coords,
            threshold=0.1
        )
        
        # 3. Check solution viability
        viability = self.grand_wave.check_solution_viability(
            disturbance.S_coords,
            domain='acoustic'
        )
        
        # 4. Prepare for dual validation
        validation_data = self.dual_validation_acoustic(
            {
                'pressure_field': pressure_field,
                'timestamps': timestamps,
                'frequencies': disturbance.frequencies,
                'amplitudes': disturbance.amplitudes
            },
            disturbance.S_coords
        )
        
        return {
            'measurement_id': measurement_id,
            'disturbance': disturbance,
            'S_coords': disturbance.S_coords,
            'equivalent_measurements': equivalent,
            'viability': viability,
            'validation_data': validation_data,
            'timestamp': disturbance.timestamp
        }

