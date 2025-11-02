"""
Spectrometer Calibration
=========================

Complete calibration system for optical spectrometer.
"""

import numpy as np
from typing import Dict, List, Optional
from dataclasses import dataclass
import json


@dataclass
class SpectrometerCalibration:
    """Complete spectrometer calibration"""
    wavelength_calibration: Dict
    intensity_calibration: Dict
    resolution: Dict
    valid: bool
    

class SpectrometerCalibrator:
    """
    Manages all spectrometer calibrations
    """
    
    def __init__(self):
        """Initialize calibrator"""
        self.wavelength_cal = None
        self.intensity_cal = None
        self.resolution = None
        
    def calibrate_wavelength(self,
                            led_wavelengths_nm: List[float],
                            measured_pixels: List[int]) -> Dict:
        """
        Calibrate pixel-to-wavelength mapping
        
        Args:
            led_wavelengths_nm: Known LED wavelengths
            measured_pixels: Measured pixel positions
            
        Returns:
            Wavelength calibration
        """
        if len(led_wavelengths_nm) != len(measured_pixels):
            raise ValueError("Wavelength and pixel lists must have same length")
            
        # Fit polynomial
        wavelengths = np.array(led_wavelengths_nm)
        pixels = np.array(measured_pixels)
        
        degree = min(2, len(wavelengths) - 1)
        coeffs_forward = np.polyfit(wavelengths, pixels, deg=degree)
        coeffs_inverse = np.polyfit(pixels, wavelengths, deg=degree)
        
        # Quality metrics
        pixels_fit = np.polyval(coeffs_forward, wavelengths)
        rms_error = np.sqrt(np.mean((pixels - pixels_fit)**2))
        
        self.wavelength_cal = {
            'coeffs_forward': coeffs_forward.tolist(),
            'coeffs_inverse': coeffs_inverse.tolist(),
            'degree': degree,
            'rms_error_pixels': float(rms_error),
            'calibration_points': {
                'wavelengths_nm': wavelengths.tolist(),
                'pixels': pixels.tolist()
            }
        }
        
        return self.wavelength_cal
        
    def calibrate_intensity(self,
                           reference_spectrum: np.ndarray,
                           dark_spectrum: Optional[np.ndarray] = None) -> Dict:
        """
        Calibrate intensity response
        
        Args:
            reference_spectrum: Known reference spectrum
            dark_spectrum: Dark current (no light)
            
        Returns:
            Intensity calibration
        """
        if dark_spectrum is not None:
            # Subtract dark
            corrected_reference = reference_spectrum - dark_spectrum
        else:
            corrected_reference = reference_spectrum
            dark_spectrum = np.zeros_like(reference_spectrum)
            
        # Calculate scaling factors
        max_intensity = np.max(corrected_reference)
        
        self.intensity_cal = {
            'dark_spectrum': dark_spectrum.tolist(),
            'reference_spectrum': corrected_reference.tolist(),
            'max_intensity': float(max_intensity),
            'has_dark_correction': dark_spectrum is not None
        }
        
        return self.intensity_cal
        
    def estimate_resolution(self) -> Dict:
        """
        Estimate spectral resolution
        
        Returns:
            Resolution metrics
        """
        if self.wavelength_cal is None:
            raise ValueError("Must calibrate wavelength first")
            
        # Get calibration data
        wavelengths = np.array(self.wavelength_cal['calibration_points']['wavelengths_nm'])
        pixels = np.array(self.wavelength_cal['calibration_points']['pixels'])
        
        # Resolution at center
        wl_center = (wavelengths.min() + wavelengths.max()) / 2
        coeffs = self.wavelength_cal['coeffs_inverse']
        
        # Calculate Δλ per pixel at center
        pixel_center = int(np.polyval(self.wavelength_cal['coeffs_forward'], wl_center))
        wl_minus = np.polyval(coeffs, pixel_center - 1)
        wl_plus = np.polyval(coeffs, pixel_center + 1)
        
        resolution_nm_per_pixel = (wl_plus - wl_minus) / 2
        
        # Resolving power
        resolving_power = wl_center / resolution_nm_per_pixel
        
        self.resolution = {
            'resolution_nm_per_pixel': float(resolution_nm_per_pixel),
            'resolving_power': float(resolving_power),
            'center_wavelength_nm': float(wl_center)
        }
        
        return self.resolution
        
    def pixel_to_wavelength(self, pixel: int) -> float:
        """Convert pixel to wavelength"""
        if self.wavelength_cal is None:
            raise ValueError("Must calibrate wavelength first")
            
        coeffs = self.wavelength_cal['coeffs_inverse']
        return float(np.polyval(coeffs, pixel))
        
    def wavelength_to_pixel(self, wavelength_nm: float) -> int:
        """Convert wavelength to pixel"""
        if self.wavelength_cal is None:
            raise ValueError("Must calibrate wavelength first")
            
        coeffs = self.wavelength_cal['coeffs_forward']
        return int(np.polyval(coeffs, wavelength_nm))
        
    def apply_intensity_calibration(self,
                                   raw_spectrum: np.ndarray) -> np.ndarray:
        """
        Apply intensity calibration to spectrum
        
        Args:
            raw_spectrum: Raw measured spectrum
            
        Returns:
            Calibrated spectrum
        """
        if self.intensity_cal is None:
            raise ValueError("Must calibrate intensity first")
            
        dark = np.array(self.intensity_cal['dark_spectrum'])
        
        # Subtract dark
        calibrated = raw_spectrum - dark
        
        # Ensure non-negative
        calibrated = np.maximum(calibrated, 0)
        
        return calibrated
        
    def generate_wavelength_axis(self,
                                n_pixels: int,
                                pixel_start: int = 0) -> np.ndarray:
        """
        Generate wavelength axis
        
        Args:
            n_pixels: Number of pixels
            pixel_start: Starting pixel
            
        Returns:
            Wavelength array (nm)
        """
        if self.wavelength_cal is None:
            raise ValueError("Must calibrate wavelength first")
            
        pixels = np.arange(pixel_start, pixel_start + n_pixels)
        wavelengths = np.array([
            self.pixel_to_wavelength(int(p)) for p in pixels
        ])
        
        return wavelengths
        
    def validate_calibration(self) -> Dict:
        """
        Validate calibration quality
        
        Returns:
            Validation results
        """
        issues = []
        
        # Check wavelength calibration
        wavelength_ok = False
        if self.wavelength_cal is None:
            issues.append("No wavelength calibration")
        else:
            rms_error = self.wavelength_cal['rms_error_pixels']
            if rms_error > 5:
                issues.append(f"High wavelength RMS error: {rms_error:.1f} pixels")
            wavelength_ok = rms_error < 5
            
        # Check intensity calibration
        intensity_ok = False
        if self.intensity_cal is None:
            issues.append("No intensity calibration")
        else:
            intensity_ok = True
            
        # Check resolution
        resolution_ok = False
        if self.resolution is None:
            if self.wavelength_cal is not None:
                self.estimate_resolution()
                resolution_ok = True
        else:
            resolution_ok = True
            
        all_ok = wavelength_ok and intensity_ok and resolution_ok
        
        return {
            'valid': all_ok,
            'wavelength_ok': wavelength_ok,
            'intensity_ok': intensity_ok,
            'resolution_ok': resolution_ok,
            'issues': issues
        }
        
    def get_calibration(self) -> SpectrometerCalibration:
        """
        Get complete calibration object
        
        Returns:
            SpectrometerCalibration
        """
        validation = self.validate_calibration()
        
        return SpectrometerCalibration(
            wavelength_calibration=self.wavelength_cal or {},
            intensity_calibration=self.intensity_cal or {},
            resolution=self.resolution or {},
            valid=validation['valid']
        )
        
    def save_calibration(self, filename: str):
        """Save calibration to file"""
        calibration = self.get_calibration()
        
        data = {
            'wavelength_calibration': calibration.wavelength_calibration,
            'intensity_calibration': calibration.intensity_calibration,
            'resolution': calibration.resolution,
            'valid': calibration.valid
        }
        
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
            
    def load_calibration(self, filename: str):
        """Load calibration from file"""
        with open(filename, 'r') as f:
            data = json.load(f)
            
        self.wavelength_cal = data.get('wavelength_calibration')
        self.intensity_cal = data.get('intensity_calibration')
        self.resolution = data.get('resolution')
        
    def quick_calibration_led(self,
                             spectrum_frame: np.ndarray,
                             led_wavelengths_nm: List[float]) -> Dict:
        """
        Quick automatic calibration using LED lines
        
        Args:
            spectrum_frame: Captured spectrum with LED light
            led_wavelengths_nm: Known LED wavelengths
            
        Returns:
            Calibration result
        """
        from scipy.signal import find_peaks
        
        # Sum to 1D
        spectrum_1d = np.sum(spectrum_frame, axis=0)
        
        # Find peaks
        peaks, properties = find_peaks(
            spectrum_1d,
            height=np.max(spectrum_1d) * 0.3,
            distance=20
        )
        
        # Sort by intensity
        peak_heights = properties['peak_heights']
        sorted_indices = np.argsort(peak_heights)[::-1]
        
        # Take top N
        n_expected = len(led_wavelengths_nm)
        if len(peaks) < n_expected:
            raise ValueError(f"Found {len(peaks)} peaks, expected {n_expected}")
            
        top_peaks = peaks[sorted_indices[:n_expected]]
        top_peaks = np.sort(top_peaks)
        
        wavelengths_sorted = sorted(led_wavelengths_nm)
        
        # Calibrate
        self.calibrate_wavelength(wavelengths_sorted, top_peaks.tolist())
        self.estimate_resolution()
        
        return {
            'detected_peaks': top_peaks.tolist(),
            'matched_wavelengths': wavelengths_sorted,
            'calibration': self.wavelength_cal,
            'resolution': self.resolution
        }

