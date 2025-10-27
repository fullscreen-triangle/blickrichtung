"""
S-Entropy Coordinate System

Universal coordinate transformation for cross-domain equivalence.

Key Principle:
When ||S_A - S_B|| < ε, systems A and B are informationally equivalent,
enabling solution transfer between domains (acoustic ↔ electrical ↔ thermal ↔ optical).

Measured equivalence: ε = 0.1 typical threshold
"""

import numpy as np
from typing import Dict, Tuple, Optional


class SEntropyCalculator:
    """
    Calculator for 5-dimensional S-entropy coordinates.
    
    Transforms measurements from different domains into unified coordinate space.
    """
    
    def __init__(self):
        """Initialize S-entropy calculator."""
        self.reference_temperature = 310.0  # K (physiological)
    
    def from_oscillatory_signature(self, frequency: float, amplitude: float, 
                                   phase: float) -> np.ndarray:
        """
        Calculate S-entropy coordinates from oscillatory signature.
        
        Args:
            frequency: Characteristic frequency (Hz)
            amplitude: Oscillation amplitude
            phase: Phase angle (radians)
            
        Returns:
            5D S-entropy coordinate vector
        """
        # Use frequency-domain mappings
        log_freq = np.log10(max(frequency, 0.1))
        
        s_transform = 0.5 + 0.1 * np.sin(log_freq)
        s_charge = -0.15 + 0.05 * np.cos(log_freq)
        s_hydrophobic = 0.8 + 0.1 * np.sin(2 * log_freq) * amplitude
        s_packing = 0.7 + 0.05 * np.cos(2 * log_freq)
        s_temporal = 0.3 + 0.1 * (log_freq / 5.0) + 0.05 * phase
        
        return np.array([s_transform, s_charge, s_hydrophobic, s_packing, s_temporal])
    
    def from_lipid_sequence(self, lipid_types: list, hole_positions: list) -> np.ndarray:
        """
        Calculate S-entropy from lipid sequence with holes.
        
        Args:
            lipid_types: List of lipid identifiers
            hole_positions: Indices of hole positions
            
        Returns:
            5D S-entropy coordinate vector (averaged over sequence)
        """
        # Lipid type mappings (from hardware-lipid-llm paper)
        LIPID_COORDS = {
            'POPC': (0.523, -0.178, 0.842, 0.691, 0.334),
            'POPE': (0.487, -0.156, 0.798, 0.673, 0.312),
            'POPS': (0.501, -0.289, 0.756, 0.682, 0.298),
            'CHOL': (0.678, 0.012, 0.923, 0.801, 0.445),
            'DOPE': (0.491, -0.167, 0.812, 0.677, 0.321),
            'HOLE': (0.000, 0.000, -1.000, 0.000, 0.000)  # Hole signature
        }
        
        # Calculate average coordinates
        coords_sum = np.zeros(5)
        count = 0
        
        for i, lipid in enumerate(lipid_types):
            if i in hole_positions:
                coords = LIPID_COORDS['HOLE']
            else:
                coords = LIPID_COORDS.get(lipid, (0.5, 0.0, 0.8, 0.7, 0.3))
            
            coords_sum += np.array(coords)
            count += 1
        
        return coords_sum / count if count > 0 else coords_sum
    
    def cross_domain_distance(self, coords_a: np.ndarray, coords_b: np.ndarray) -> float:
        """
        Calculate cross-domain equivalence distance.
        
        Args:
            coords_a: S-entropy coordinates from domain A
            coords_b: S-entropy coordinates from domain B
            
        Returns:
            Euclidean distance in S-entropy space
        """
        return np.linalg.norm(coords_a - coords_b)
    
    def are_equivalent(self, coords_a: np.ndarray, coords_b: np.ndarray, 
                      threshold: float = 0.1) -> bool:
        """
        Check if two systems are equivalent in S-entropy space.
        
        From Circuit-Pathway Duality Theorem:
        If ||S_A - S_B|| < ε, systems are informationally equivalent.
        
        Args:
            coords_a: S-entropy coordinates from system A
            coords_b: S-entropy coordinates from system B
            threshold: Equivalence threshold (default: 0.1)
            
        Returns:
            True if systems are equivalent
        """
        return self.cross_domain_distance(coords_a, coords_b) < threshold


def calculate_s_entropy(measurement_data: Dict, domain: str) -> np.ndarray:
    """
    Calculate S-entropy coordinates from measurement data.
    
    Args:
        measurement_data: Dictionary of measurements
        domain: Measurement domain ('acoustic', 'electrical', 'thermal', etc.)
        
    Returns:
        5D S-entropy coordinate vector
    """
    calculator = SEntropyCalculator()
    
    # Domain-specific S-entropy calculations
    if domain == 'acoustic':
        # Acoustic: (velocity, turbulence, viscosity)
        velocity = measurement_data.get('velocity', 0)
        turbulence = measurement_data.get('turbulence', 0)
        viscosity = measurement_data.get('viscosity', 0)
        return np.array([velocity, turbulence, viscosity, 0, 0])
    
    elif domain == 'electrical' or domain == 'capacitive':
        # Electrical: (permittivity, loss, conductivity)
        permittivity = measurement_data.get('permittivity', 1.0)
        loss = measurement_data.get('loss_tangent', 0)
        conductivity = measurement_data.get('conductivity', 0)
        return np.array([permittivity, loss, conductivity, 0, 0])
    
    elif domain == 'thermal':
        # Thermal: (conductivity, capacity, diffusivity)
        conductivity = measurement_data.get('thermal_conductivity', 0)
        capacity = measurement_data.get('heat_capacity', 0)
        diffusivity = measurement_data.get('diffusivity', 0)
        return np.array([conductivity, capacity, diffusivity, 0, 0])
    
    elif domain == 'oscillatory':
        # From oscillatory signature
        frequency = measurement_data.get('frequency', 120.0)
        amplitude = measurement_data.get('amplitude', 1.0)
        phase = measurement_data.get('phase', 0.0)
        return calculator.from_oscillatory_signature(frequency, amplitude, phase)
    
    else:
        # Default: return zeros
        return np.zeros(5)

