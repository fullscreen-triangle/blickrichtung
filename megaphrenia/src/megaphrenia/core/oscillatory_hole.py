"""
Oscillatory Holes

Functional absences acting as active charge carriers in biological semiconductors.

Theoretical Foundation:
- Measured mobility: 0.0123 cm²/(V·s)
- P-type concentration: 2.80×10¹² cm⁻³
- Therapeutic conductivity: 7.53×10⁻⁸ S/cm
"""

from dataclasses import dataclass
from typing import Tuple
import numpy as np


# Physical constants
ELEMENTARY_CHARGE = 1.6e-19  # Coulombs
KB_T = 0.026  # eV at room temperature (310 K)


@dataclass
class OscillatoryHole:
    """
    An oscillatory hole - functional absence acting as charge carrier.
    
    Attributes:
        position: 3D position (x, y, z) in nanometers
        mobility: Hole mobility in cm²/(V·s)
        signature: 5D S-entropy signature
        state: "stable", "mobile", "recombining"
    """
    
    position: Tuple[float, float, float] = (0.0, 0.0, 0.0)
    mobility: float = 0.0123  # Measured value cm²/(V·s)
    signature: np.ndarray = None
    state: str = "stable"
    
    def __post_init__(self):
        """Initialize signature if not provided."""
        if self.signature is None:
            # Default signature: zeros except hydrophobic = -1 (hole indicator)
            self.signature = np.array([0.0, 0.0, -1.0, 0.0, 0.0])
    
    def drift_velocity(self, electric_field: Tuple[float, float, float]) -> np.ndarray:
        """
        Calculate drift velocity under electric field.
        
        v_drift = μ_h × E
        
        Args:
            electric_field: Electric field (V/cm) in (x, y, z)
            
        Returns:
            Drift velocity (cm/s) as numpy array
        """
        E = np.array(electric_field)
        return self.mobility * E
    
    def move(self, electric_field: Tuple[float, float, float], dt: float) -> None:
        """
        Update hole position under electric field for time dt.
        
        Args:
            electric_field: Electric field (V/cm)
            dt: Time step (seconds)
        """
        v_drift = self.drift_velocity(electric_field)
        
        # Convert velocity from cm/s to nm/s for position update
        v_drift_nm = v_drift * 1e7  # cm/s → nm/s
        
        # Update position
        new_pos = np.array(self.position) + v_drift_nm * dt
        self.position = tuple(new_pos)
        
        self.state = "mobile"


@dataclass  
class HoleDynamics:
    """
    Hole dynamics simulator for biological semiconductor.
    
    Simulates drift, diffusion, and recombination of oscillatory holes.
    """
    
    hole_concentration: float = 2.80e12  # cm⁻³ (measured P-type)
    electron_concentration: float = 3.57e7  # cm⁻³ (measured N-type)
    temperature: float = 310.0  # Kelvin (physiological)
    
    @property
    def intrinsic_concentration(self) -> float:
        """
        Calculate intrinsic carrier concentration.
        
        n_i = sqrt(n_e × p_h)
        """
        return np.sqrt(self.hole_concentration * self.electron_concentration)
    
    @property
    def is_p_type(self) -> bool:
        """Check if material is P-type (hole conduction dominant)."""
        return self.hole_concentration > self.intrinsic_concentration
    
    def diffusion_coefficient(self, mobility: float) -> float:
        """
        Calculate diffusion coefficient from mobility (Einstein relation).
        
        D = (kB T / q) × μ
        
        Args:
            mobility: Carrier mobility (cm²/(V·s))
            
        Returns:
            Diffusion coefficient (cm²/s)
        """
        return (KB_T / ELEMENTARY_CHARGE) * mobility
    
    def thermal_velocity(self, effective_mass: float = 1.0) -> float:
        """
        Calculate thermal velocity.
        
        v_th = sqrt(3 kB T / m*)
        
        Args:
            effective_mass: Effective mass in units of electron mass
            
        Returns:
            Thermal velocity (cm/s)
        """
        m_e = 9.11e-31  # Electron mass (kg)
        m_eff = effective_mass * m_e
        kB = 1.38e-23  # Boltzmann constant (J/K)
        
        v_th = np.sqrt(3 * kB * self.temperature / m_eff)
        return v_th * 100  # m/s → cm/s
    
    def recombination_rate(self, n: float, p: float, 
                          recombination_coefficient: float = 1e-10) -> float:
        """
        Calculate hole-electron recombination rate.
        
        R = B × n × p
        
        Args:
            n: Electron concentration (cm⁻³)
            p: Hole concentration (cm⁻³)
            recombination_coefficient: B coefficient (cm³/s)
            
        Returns:
            Recombination rate (cm⁻³/s)
        """
        return recombination_coefficient * n * p

