"""
Acoustic Wind Tunnel Calibration
=================================

Calibrates acoustic streaming parameters against known references.
"""

import numpy as np
from typing import Dict, List, Tuple
from dataclasses import dataclass


@dataclass
class CalibrationPoint:
    """Single calibration measurement"""
    streaming_intensity: float  # Input (0-1)
    measured_velocity: float    # Output (m/s)
    carrier_freq: float         # Hz
    modulation_freq: float      # Hz
    spl_db: float              # dB SPL


class AcousticCalibration:
    """
    Calibrates acoustic streaming velocity measurements
    """
    
    def __init__(self):
        """Initialize calibration"""
        self.calibration_curve = None
        self.calibration_points = []
        
    def add_calibration_point(self,
                             streaming_intensity: float,
                             measured_velocity: float,
                             carrier_freq: float,
                             modulation_freq: float,
                             spl_db: float):
        """
        Add a calibration measurement
        
        Args:
            streaming_intensity: Control parameter (0-1)
            measured_velocity: Measured velocity (m/s)
            carrier_freq: Carrier frequency (Hz)
            modulation_freq: Modulation frequency (Hz)
            spl_db: Sound pressure level (dB)
        """
        point = CalibrationPoint(
            streaming_intensity=streaming_intensity,
            measured_velocity=measured_velocity,
            carrier_freq=carrier_freq,
            modulation_freq=modulation_freq,
            spl_db=spl_db
        )
        
        self.calibration_points.append(point)
        
    def fit_calibration_curve(self) -> Dict:
        """
        Fit polynomial calibration curve
        
        Returns:
            Calibration parameters
        """
        if len(self.calibration_points) < 3:
            raise ValueError("Need at least 3 calibration points")
            
        # Extract data
        intensities = np.array([p.streaming_intensity for p in self.calibration_points])
        velocities = np.array([p.measured_velocity for p in self.calibration_points])
        
        # Fit polynomial (2nd order)
        coeffs = np.polyfit(intensities, velocities, deg=2)
        
        # Calculate R²
        v_fit = np.polyval(coeffs, intensities)
        ss_res = np.sum((velocities - v_fit)**2)
        ss_tot = np.sum((velocities - np.mean(velocities))**2)
        r_squared = 1 - (ss_res / ss_tot)
        
        # Calculate RMS error
        rms_error = np.sqrt(np.mean((velocities - v_fit)**2))
        
        self.calibration_curve = {
            'coefficients': coeffs,
            'r_squared': r_squared,
            'rms_error': rms_error,
            'n_points': len(self.calibration_points),
            'velocity_range': (velocities.min(), velocities.max())
        }
        
        return self.calibration_curve
        
    def apply_calibration(self, streaming_intensity: float) -> float:
        """
        Apply calibration to convert intensity to velocity
        
        Args:
            streaming_intensity: Control parameter (0-1)
            
        Returns:
            Calibrated velocity (m/s)
        """
        if self.calibration_curve is None:
            raise ValueError("Must fit calibration curve first")
            
        coeffs = self.calibration_curve['coefficients']
        velocity = np.polyval(coeffs, streaming_intensity)
        
        return velocity
        
    def generate_calibration_sequence(self,
                                     carrier_freq: float = 35000,
                                     modulation_freq: float = 100) -> List[Dict]:
        """
        Generate recommended calibration sequence
        
        Args:
            carrier_freq: Carrier frequency (Hz)
            modulation_freq: Modulation frequency (Hz)
            
        Returns:
            List of calibration settings to measure
        """
        # Standard calibration points
        intensities = [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]
        
        sequence = []
        for intensity in intensities:
            sequence.append({
                'streaming_intensity': intensity,
                'carrier_frequency': carrier_freq,
                'modulation_frequency': modulation_freq,
                'duration': 0.5,  # seconds
                'instruction': f"Measure at {intensity*100:.0f}% intensity"
            })
            
        return sequence
        
    def validate_calibration(self) -> Dict:
        """
        Validate calibration quality
        
        Returns:
            Validation metrics
        """
        if self.calibration_curve is None:
            raise ValueError("Must fit calibration curve first")
            
        # Check R²
        r_squared = self.calibration_curve['r_squared']
        r_squared_ok = r_squared > 0.95
        
        # Check RMS error
        rms_error = self.calibration_curve['rms_error']
        v_range = self.calibration_curve['velocity_range']
        relative_error = rms_error / (v_range[1] - v_range[0])
        error_ok = relative_error < 0.05  # 5% error
        
        # Check coverage
        n_points = self.calibration_curve['n_points']
        coverage_ok = n_points >= 5
        
        all_ok = r_squared_ok and error_ok and coverage_ok
        
        return {
            'valid': all_ok,
            'r_squared': r_squared,
            'r_squared_ok': r_squared_ok,
            'rms_error': rms_error,
            'relative_error': relative_error,
            'error_ok': error_ok,
            'n_points': n_points,
            'coverage_ok': coverage_ok,
            'issues': self._identify_issues(r_squared_ok, error_ok, coverage_ok)
        }
        
    def _identify_issues(self,
                        r_squared_ok: bool,
                        error_ok: bool,
                        coverage_ok: bool) -> List[str]:
        """Identify calibration issues"""
        issues = []
        
        if not r_squared_ok:
            issues.append("Low R² - check for measurement errors")
        if not error_ok:
            issues.append("High RMS error - need more calibration points")
        if not coverage_ok:
            issues.append("Insufficient calibration points")
            
        return issues
        
    def save_calibration(self, filename: str):
        """Save calibration to file"""
        import json
        
        data = {
            'calibration_curve': self.calibration_curve,
            'calibration_points': [
                {
                    'streaming_intensity': p.streaming_intensity,
                    'measured_velocity': p.measured_velocity,
                    'carrier_freq': p.carrier_freq,
                    'modulation_freq': p.modulation_freq,
                    'spl_db': p.spl_db
                }
                for p in self.calibration_points
            ]
        }
        
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
            
    def load_calibration(self, filename: str):
        """Load calibration from file"""
        import json
        
        with open(filename, 'r') as f:
            data = json.load(f)
            
        self.calibration_curve = data['calibration_curve']
        
        self.calibration_points = [
            CalibrationPoint(**p)
            for p in data['calibration_points']
        ]
