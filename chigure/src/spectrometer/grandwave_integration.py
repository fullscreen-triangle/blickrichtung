"""
GrandWave Integration for Optical Spectrometer
===============================================

Connects optical measurements to the universal substrate.
"""

import numpy as np
from typing import Dict, Optional
import sys
sys.path.append('../../grand_unification')
from GrandWave import GrandWave, WaveDisturbance
from Interface import WaveInterface
from s_entropy_optical import SOpticalMapper
from oscillatory_signatures import OscillatorySignature


class SpectrometerGrandWaveConnector:
    """
    Integrates optical spectrometer with GrandWave substrate
    """
    
    def __init__(self, grand_wave: Optional[GrandWave] = None):
        """
        Initialize connector
        
        Args:
            grand_wave: Existing GrandWave instance or create new one
        """
        if grand_wave is None:
            self.grand_wave = GrandWave(
                frequency_range=(1e14, 1e15),  # Hz, visible light range
                n_basis_functions=10000,
                trans_planckian_precision=7.51e-50
            )
        else:
            self.grand_wave = grand_wave
            
        # Create interface for optical measurements
        self.interface = WaveInterface(
            object_id="optical_spectrometer",
            grand_wave=self.grand_wave,
            domain="optical"
        )
        
        # S-entropy mapper
        self.s_mapper = SOpticalMapper()
        
    def announce_measurement(self,
                            measurement_id: str,
                            wavelengths: np.ndarray,
                            absorbance: np.ndarray,
                            duration: float = 0.01) -> WaveDisturbance:
        """
        Announce optical measurement to GrandWave
        
        Args:
            measurement_id: Unique identifier for measurement
            wavelengths: Wavelength axis (nm)
            absorbance: Absorbance spectrum
            duration: Measurement duration (s)
            
        Returns:
            WaveDisturbance created in GrandWave
        """
        # Convert to oscillatory signature
        signature = self.s_mapper.spectrum_to_oscillatory_signature(
            wavelengths,
            absorbance
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
            'n_optical': len(by_domain.get('optical', [])),
            'n_acoustic': len(by_domain.get('acoustic', [])),
            'cross_domain_matches': len(equivalent) - len(by_domain.get('optical', []))
        }
        
    def find_similar_chromophores(self,
                                 S_coords: np.ndarray,
                                 threshold: float = 0.15) -> Dict:
        """
        Find chromophores with similar absorption characteristics
        
        Args:
            S_coords: S-entropy coordinates of query chromophore
            threshold: Similarity threshold
            
        Returns:
            Similar chromophores
        """
        similar = self.grand_wave.find_equivalent_disturbances(
            S_coords,
            threshold=threshold
        )
        
        # Filter for optical domain only
        optical_only = [d for d in similar if d.domain == 'optical']
        
        # Sort by S-distance
        distances = [
            np.linalg.norm(d.S_coords - S_coords)
            for d in optical_only
        ]
        
        sorted_indices = np.argsort(distances)
        sorted_similar = [optical_only[i] for i in sorted_indices]
        sorted_distances = [distances[i] for i in sorted_indices]
        
        return {
            'similar_chromophores': sorted_similar,
            'S_distances': sorted_distances,
            'n_similar': len(sorted_similar),
            'closest_match': sorted_similar[0] if sorted_similar else None,
            'closest_distance': sorted_distances[0] if sorted_distances else None
        }
        
    def cross_domain_optimization(self,
                                 target_property: str,
                                 target_value: float,
                                 current_S: np.ndarray) -> Dict:
        """
        Find optimal solution using cross-domain equivalence
        
        Args:
            target_property: Property to optimize (e.g., 'extinction_coefficient')
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
        
    def dual_validation_optical(self,
                               measurement: Dict,
                               S_coords: np.ndarray) -> Dict:
        """
        Prepare optical measurement for dual validation
        
        Args:
            measurement: Raw optical measurement data
            S_coords: S-entropy coordinates
            
        Returns:
            Data formatted for dual validation
        """
        # Oscillatory pathway (already done via S-coords)
        oscillatory_result = {
            'S_coords': S_coords,
            'domain': 'optical',
            'wavelengths': measurement.get('wavelengths', []),
            'absorbance': measurement.get('absorbance', []),
            'peak_wavelengths': measurement.get('peak_wavelengths', [])
        }
        
        # Visual pathway preparation
        visual_ready = {
            'S_coords': S_coords,
            'domain': 'optical',
            'ready_for_droplet_simulation': True
        }
        
        return {
            'oscillatory_result': oscillatory_result,
            'visual_ready': visual_ready,
            'requires_validation': True
        }
        
    def acoustic_to_optical_transfer(self,
                                    acoustic_S: np.ndarray) -> Dict:
        """
        Check if acoustic solution can transfer to optical domain
        
        Args:
            acoustic_S: S-entropy coordinates from acoustic measurement
            
        Returns:
            Transfer viability and suggestions
        """
        # Calculate S-distance to optical domain
        optical_disturbances = [
            d for d in self.grand_wave.disturbances
            if d.domain == 'optical'
        ]
        
        if not optical_disturbances:
            return {
                'transferable': False,
                'reason': 'No optical measurements in GrandWave yet'
            }
            
        # Find closest optical measurement
        min_distance = float('inf')
        closest = None
        
        for d in optical_disturbances:
            distance = np.linalg.norm(d.S_coords - acoustic_S)
            if distance < min_distance:
                min_distance = distance
                closest = d
                
        transferable = min_distance < 0.1  # Equivalence threshold
        
        return {
            'transferable': transferable,
            'S_distance': min_distance,
            'threshold': 0.1,
            'closest_optical': closest,
            'suggested_S_coords': closest.S_coords if closest else None,
            'coherence': 1.0 - (min_distance / 0.1) if transferable else 0.0
        }
        
    def get_transcendent_view(self) -> Dict:
        """
        Get simultaneous view of all optical measurements in GrandWave
        
        Returns:
            Transcendent observer view
        """
        view = self.grand_wave.get_transcendent_view()
        
        # Filter for optical measurements
        optical_only = [
            d for d in view['all_disturbances'] 
            if d.domain == 'optical'
        ]
        
        return {
            'all_measurements': view,
            'optical_measurements': optical_only,
            'n_optical': len(optical_only),
            'optical_frequency_range': self._get_frequency_range(optical_only),
            'optical_S_range': self._get_S_range(optical_only)
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
                              wavelengths: np.ndarray,
                              absorbance: np.ndarray) -> Dict:
        """
        Complete measurement workflow with GrandWave integration
        
        Args:
            measurement_id: Measurement identifier
            wavelengths: Wavelength axis (nm)
            absorbance: Absorbance spectrum
            
        Returns:
            Complete measurement with GrandWave context
        """
        # 1. Announce measurement
        disturbance = self.announce_measurement(
            measurement_id,
            wavelengths,
            absorbance
        )
        
        # 2. Find equivalent measurements
        equivalent = self.find_equivalent_measurements(
            disturbance.S_coords,
            threshold=0.1
        )
        
        # 3. Find similar chromophores
        similar = self.find_similar_chromophores(
            disturbance.S_coords,
            threshold=0.15
        )
        
        # 4. Check solution viability
        viability = self.grand_wave.check_solution_viability(
            disturbance.S_coords,
            domain='optical'
        )
        
        # 5. Prepare for dual validation
        validation_data = self.dual_validation_optical(
            {
                'wavelengths': wavelengths,
                'absorbance': absorbance
            },
            disturbance.S_coords
        )
        
        return {
            'measurement_id': measurement_id,
            'disturbance': disturbance,
            'S_coords': disturbance.S_coords,
            'equivalent_measurements': equivalent,
            'similar_chromophores': similar,
            'viability': viability,
            'validation_data': validation_data,
            'timestamp': disturbance.timestamp
        }

