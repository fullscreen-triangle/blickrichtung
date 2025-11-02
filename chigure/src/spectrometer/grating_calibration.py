"""
Grating Calibration
===================

Calibrates the diffraction grating wavelength mapping.
"""

import numpy as np
from typing import Dict, List, Tuple
from dataclasses import dataclass


@dataclass
class CalibrationLine:
    """Known spectral line for calibration"""
    wavelength_nm: float
    measured_pixel: int
    intensity: float
    

class GratingCalibration:
    """
    Calibrates pixel-to-wavelength mapping
    """
    
    def __init__(self):
        """Initialize calibration"""
        self.calibration_lines = []
        self.calibration_function = None
        
    def add_calibration_line(self,
                            wavelength_nm: float,
                            measured_pixel: int,
                            intensity: float = 1.0):
        """
        Add known spectral line
        
        Args:
            wavelength_nm: Known wavelength (nm)
            measured_pixel: Measured pixel position
            intensity: Line intensity
        """
        line = CalibrationLine(
            wavelength_nm=wavelength_nm,
            measured_pixel=measured_pixel,
            intensity=intensity
        )
        
        self.calibration_lines.append(line)
        
    def fit_calibration(self, degree: int = 2) -> Dict:
        """
        Fit polynomial calibration function
        
        Args:
            degree: Polynomial degree
            
        Returns:
            Calibration parameters
        """
        if len(self.calibration_lines) < degree + 1:
            raise ValueError(f"Need at least {degree+1} calibration lines")
            
        # Extract data
        wavelengths = np.array([l.wavelength_nm for l in self.calibration_lines])
        pixels = np.array([l.measured_pixel for l in self.calibration_lines])
        
        # Fit: pixel = f(wavelength)
        coeffs_forward = np.polyfit(wavelengths, pixels, deg=degree)
        
        # Fit inverse: wavelength = f(pixel)
        coeffs_inverse = np.polyfit(pixels, wavelengths, deg=degree)
        
        # Calculate fit quality
        pixels_fit = np.polyval(coeffs_forward, wavelengths)
        residuals = pixels - pixels_fit
        rms_error = np.sqrt(np.mean(residuals**2))
        
        # Calculate wavelength accuracy
        wavelengths_fit = np.polyval(coeffs_inverse, pixels)
        wavelength_rms = np.sqrt(np.mean((wavelengths - wavelengths_fit)**2))
        
        self.calibration_function = {
            'coeffs_forward': coeffs_forward,
            'coeffs_inverse': coeffs_inverse,
            'degree': degree,
            'rms_error_pixels': rms_error,
            'wavelength_accuracy_nm': wavelength_rms,
            'n_lines': len(self.calibration_lines),
            'wavelength_range_nm': (wavelengths.min(), wavelengths.max())
        }
        
        return self.calibration_function
        
    def pixel_to_wavelength(self, pixel: int) -> float:
        """
        Convert pixel position to wavelength
        
        Args:
            pixel: Pixel position
            
        Returns:
            Wavelength (nm)
        """
        if self.calibration_function is None:
            raise ValueError("Must fit calibration first")
            
        coeffs = self.calibration_function['coeffs_inverse']
        wavelength = np.polyval(coeffs, pixel)
        
        return wavelength
        
    def wavelength_to_pixel(self, wavelength_nm: float) -> int:
        """
        Convert wavelength to pixel position
        
        Args:
            wavelength_nm: Wavelength (nm)
            
        Returns:
            Pixel position
        """
        if self.calibration_function is None:
            raise ValueError("Must fit calibration first")
            
        coeffs = self.calibration_function['coeffs_forward']
        pixel = int(np.polyval(coeffs, wavelength_nm))
        
        return pixel
        
    def generate_wavelength_axis(self,
                                n_pixels: int,
                                pixel_start: int = 0) -> np.ndarray:
        """
        Generate wavelength axis for spectrum
        
        Args:
            n_pixels: Number of pixels
            pixel_start: Starting pixel
            
        Returns:
            Wavelength array (nm)
        """
        if self.calibration_function is None:
            raise ValueError("Must fit calibration first")
            
        pixels = np.arange(pixel_start, pixel_start + n_pixels)
        wavelengths = np.array([
            self.pixel_to_wavelength(p) for p in pixels
        ])
        
        return wavelengths
        
    def estimate_resolution(self) -> Dict:
        """
        Estimate spectral resolution
        
        Returns:
            Resolution metrics
        """
        if self.calibration_function is None:
            raise ValueError("Must fit calibration first")
            
        # Resolution at center wavelength
        wl_range = self.calibration_function['wavelength_range_nm']
        wl_center = (wl_range[0] + wl_range[1]) / 2
        
        # Resolution = Δλ per pixel at center
        pixel_center = self.wavelength_to_pixel(wl_center)
        wl_minus = self.pixel_to_wavelength(pixel_center - 1)
        wl_plus = self.pixel_to_wavelength(pixel_center + 1)
        
        resolution_nm_per_pixel = (wl_plus - wl_minus) / 2
        
        # Resolving power R = λ / Δλ
        resolving_power = wl_center / resolution_nm_per_pixel
        
        return {
            'resolution_nm_per_pixel': resolution_nm_per_pixel,
            'resolving_power': resolving_power,
            'center_wavelength_nm': wl_center
        }
        
    def led_calibration_auto(self,
                            led_wavelengths_nm: List[float],
                            spectrum_frame: np.ndarray) -> Dict:
        """
        Automatic calibration using known LED lines
        
        Args:
            led_wavelengths_nm: Known LED wavelengths
            spectrum_frame: Captured spectrum frame
            
        Returns:
            Calibration result
        """
        # Find peaks in spectrum
        from scipy.signal import find_peaks
        
        # Sum along vertical axis
        spectrum_1d = np.sum(spectrum_frame, axis=0)
        
        # Find peaks
        peaks, properties = find_peaks(
            spectrum_1d,
            height=np.max(spectrum_1d) * 0.3,
            distance=20  # Minimum separation
        )
        
        # Sort by intensity
        peak_heights = properties['peak_heights']
        sorted_indices = np.argsort(peak_heights)[::-1]
        
        # Take top N peaks
        n_expected = len(led_wavelengths_nm)
        if len(peaks) < n_expected:
            raise ValueError(f"Found {len(peaks)} peaks, expected {n_expected}")
            
        top_peaks = peaks[sorted_indices[:n_expected]]
        top_peaks = np.sort(top_peaks)  # Sort by position
        
        # Match peaks to wavelengths
        wavelengths_sorted = sorted(led_wavelengths_nm)
        
        # Add calibration lines
        self.calibration_lines = []
        for wl, pixel in zip(wavelengths_sorted, top_peaks):
            self.add_calibration_line(wl, int(pixel))
            
        # Fit calibration
        result = self.fit_calibration(degree=min(2, n_expected - 1))
        
        result['detected_peaks'] = top_peaks
        result['matched_wavelengths'] = wavelengths_sorted
        
        return result
