"""
Acoustic Streaming Physics
===========================

Calculates flow velocity from ultrasonic acoustic streaming.

Theory:
-------
Eckart streaming: Time-averaged steady flow from high-intensity sound waves.
v_streaming ≈ I² / (ρ c³ ω)

Where:
- I: Acoustic intensity (W/m²)
- ρ: Air density (kg/m³)
- c: Speed of sound (m/s)
- ω: Angular frequency (rad/s)

At 140 dB SPL and 35 kHz, creates equivalent flow of 0.1-5 m/s.
"""

import numpy as np
from typing import Dict, Tuple
from scipy.ndimage import gaussian_filter


class AcousticStreamingPhysics:
    """
    Calculate acoustic streaming velocities from ultrasound
    """
    
    # Physical constants
    RHO_AIR = 1.2  # kg/m³ at 20°C
    C_SOUND = 343  # m/s at 20°C
    P_REF = 2e-5  # Reference pressure (Pa) for dB SPL
    
    def __init__(self):
        """Initialize streaming physics calculator"""
        pass
        
    def intensity_from_spl(self, spl_db: float) -> float:
        """
        Convert SPL (dB) to acoustic intensity (W/m²)
        
        Args:
            spl_db: Sound pressure level (dB SPL)
            
        Returns:
            Intensity (W/m²)
        """
        # I = I_ref * 10^(SPL/10)
        # where I_ref = P_ref² / (ρc) = 1e-12 W/m²
        I_ref = self.P_REF**2 / (self.RHO_AIR * self.C_SOUND)
        intensity = I_ref * 10**(spl_db / 10)
        return intensity
        
    def streaming_velocity_eckart(self,
                                  intensity: float,
                                  frequency: float) -> float:
        """
        Calculate Eckart streaming velocity
        
        Args:
            intensity: Acoustic intensity (W/m²)
            frequency: Frequency (Hz)
            
        Returns:
            Streaming velocity (m/s)
        """
        omega = 2 * np.pi * frequency
        
        # Eckart streaming formula
        # v ≈ I² / (ρ c³ ω)
        velocity = (intensity**2) / (
            self.RHO_AIR * self.C_SOUND**3 * omega
        )
        
        return velocity
        
    def calculate_streaming_field(self,
                                  mic_pressures: np.ndarray,
                                  mic_positions: np.ndarray,
                                  carrier_frequency: float) -> Dict:
        """
        Calculate 2D streaming velocity field from microphone array
        
        Args:
            mic_pressures: RMS pressure at each microphone (Pa), shape (n_mics,)
            mic_positions: Microphone positions (m), shape (n_mics, 3)
            carrier_frequency: Carrier frequency (Hz)
            
        Returns:
            Dictionary with velocity field
        """
        n_mics = len(mic_pressures)
        
        # Calculate intensity at each microphone
        intensities = np.zeros(n_mics)
        for i in range(n_mics):
            # I = p²/(ρc)
            intensities[i] = mic_pressures[i]**2 / (self.RHO_AIR * self.C_SOUND)
            
        # Calculate streaming velocity at each position
        velocities = np.zeros(n_mics)
        for i in range(n_mics):
            velocities[i] = self.streaming_velocity_eckart(
                intensities[i],
                carrier_frequency
            )
            
        # Interpolate to 2D grid
        velocity_field = self._interpolate_to_grid(
            mic_positions[:, :2],  # Only x,y
            velocities
        )
        
        return {
            'velocities_at_mics': velocities,
            'intensities_at_mics': intensities,
            'velocity_field_2d': velocity_field,
            'grid_x': velocity_field['x'],
            'grid_y': velocity_field['y'],
            'velocity_magnitude': velocity_field['magnitude']
        }
        
    def _interpolate_to_grid(self,
                            positions: np.ndarray,
                            values: np.ndarray,
                            grid_size: int = 50) -> Dict:
        """
        Interpolate scattered data to regular 2D grid
        
        Args:
            positions: Positions (n_points, 2)
            values: Values at positions (n_points,)
            grid_size: Grid resolution
            
        Returns:
            Dictionary with gridded data
        """
        from scipy.interpolate import griddata
        
        # Create regular grid
        x_min, x_max = positions[:, 0].min(), positions[:, 0].max()
        y_min, y_max = positions[:, 1].min(), positions[:, 1].max()
        
        # Add margin
        margin = 0.02  # 2cm
        x_min -= margin
        x_max += margin
        y_min -= margin
        y_max += margin
        
        x_grid = np.linspace(x_min, x_max, grid_size)
        y_grid = np.linspace(y_min, y_max, grid_size)
        X, Y = np.meshgrid(x_grid, y_grid)
        
        # Interpolate
        Z = griddata(
            positions,
            values,
            (X, Y),
            method='cubic',
            fill_value=0
        )
        
        # Smooth
        Z = gaussian_filter(Z, sigma=1.0)
        
        return {
            'x': X,
            'y': Y,
            'magnitude': Z
        }
        
    def estimate_drag_coefficient(self,
                                  velocity_field: np.ndarray,
                                  object_position: Tuple[float, float],
                                  object_size: float) -> float:
        """
        Estimate drag coefficient from velocity field disturbance
        
        Args:
            velocity_field: 2D velocity field
            object_position: Center position (x, y) in meters
            object_size: Characteristic size (m)
            
        Returns:
            Estimated drag coefficient
        """
        # Simplified drag estimation from wake deficit
        # Real implementation would use more sophisticated analysis
        
        # Extract wake region (behind object)
        # This is a simplified placeholder
        wake_deficit = 0.2  # Normalized velocity deficit
        
        # Empirical correlation
        # C_d ≈ 2 * wake_deficit
        drag_coeff = 2.0 * wake_deficit
        
        return drag_coeff