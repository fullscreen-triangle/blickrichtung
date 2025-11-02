"""
Absorption Analysis
===================

Calculate absorption/transmission spectra.
"""

import numpy as np
from typing import Dict, Optional


class AbsorptionAnalyzer:
    """
    Analyzes absorption and transmission spectra
    """
    
    def __init__(self):
        """Initialize analyzer"""
        self.reference_spectrum = None
        
    def set_reference(self, reference_spectrum: np.ndarray):
        """
        Set reference spectrum (blank/background)
        
        Args:
            reference_spectrum: Reference intensity spectrum
        """
        self.reference_spectrum = reference_spectrum
        
    def calculate_transmission(self,
                              sample_spectrum: np.ndarray,
                              reference_spectrum: Optional[np.ndarray] = None) -> np.ndarray:
        """
        Calculate transmission spectrum
        
        Args:
            sample_spectrum: Sample intensity
            reference_spectrum: Reference intensity (or use stored)
            
        Returns:
            Transmission (0-1)
        """
        if reference_spectrum is None:
            if self.reference_spectrum is None:
                raise ValueError("No reference spectrum available")
            reference_spectrum = self.reference_spectrum
            
        # T = I_sample / I_reference
        # Avoid division by zero
        transmission = np.divide(
            sample_spectrum,
            reference_spectrum,
            out=np.zeros_like(sample_spectrum, dtype=float),
            where=reference_spectrum > 0
        )
        
        # Clip to valid range
        transmission = np.clip(transmission, 0, 1)
        
        return transmission
        
    def calculate_absorbance(self,
                            sample_spectrum: np.ndarray,
                            reference_spectrum: Optional[np.ndarray] = None) -> np.ndarray:
        """
        Calculate absorbance spectrum (Beer-Lambert law)
        
        Args:
            sample_spectrum: Sample intensity
            reference_spectrum: Reference intensity (or use stored)
            
        Returns:
            Absorbance (A = -log10(T))
        """
        transmission = self.calculate_transmission(
            sample_spectrum,
            reference_spectrum
        )
        
        # A = -log10(T)
        # Avoid log(0)
        absorbance = np.where(
            transmission > 1e-10,
            -np.log10(transmission),
            10.0  # Cap at A=10
        )
        
        return absorbance
        
    def calculate_extinction_coefficient(self,
                                        absorbance: np.ndarray,
                                        concentration: float,
                                        path_length: float) -> np.ndarray:
        """
        Calculate molar extinction coefficient
        
        Args:
            absorbance: Absorbance spectrum
            concentration: Concentration (mol/L)
            path_length: Path length (cm)
            
        Returns:
            Extinction coefficient ε (L/(mol·cm))
        """
        # Beer-Lambert: A = ε c l
        # ε = A / (c l)
        
        if concentration <= 0 or path_length <= 0:
            raise ValueError("Concentration and path length must be positive")
            
        epsilon = absorbance / (concentration * path_length)
        
        return epsilon
        
    def analyze_sample(self,
                      sample_spectrum: np.ndarray,
                      wavelengths: np.ndarray,
                      concentration: Optional[float] = None,
                      path_length: float = 1.0,
                      reference_spectrum: Optional[np.ndarray] = None) -> Dict:
        """
        Complete absorption analysis
        
        Args:
            sample_spectrum: Sample intensity
            wavelengths: Wavelength axis (nm)
            concentration: Sample concentration (mol/L)
            path_length: Path length (cm)
            reference_spectrum: Reference intensity
            
        Returns:
            Complete analysis
        """
        # Transmission
        transmission = self.calculate_transmission(
            sample_spectrum,
            reference_spectrum
        )
        
        # Absorbance
        absorbance = self.calculate_absorbance(
            sample_spectrum,
            reference_spectrum
        )
        
        # Find absorption peaks
        absorption_peaks = self._find_absorption_peaks(
            wavelengths,
            absorbance
        )
        
        result = {
            'wavelengths': wavelengths,
            'transmission': transmission,
            'absorbance': absorbance,
            'absorption_peaks': absorption_peaks,
            'max_absorbance': np.max(absorbance),
            'max_absorbance_wavelength': wavelengths[np.argmax(absorbance)]
        }
        
        # Extinction coefficient if concentration given
        if concentration is not None:
            epsilon = self.calculate_extinction_coefficient(
                absorbance,
                concentration,
                path_length
            )
            result['extinction_coefficient'] = epsilon
            result['max_extinction'] = np.max(epsilon)
            
        return result
        
    def _find_absorption_peaks(self,
                              wavelengths: np.ndarray,
                              absorbance: np.ndarray,
                              prominence: float = 0.1) -> Dict:
        """
        Find absorption peaks
        
        Args:
            wavelengths: Wavelength axis
            absorbance: Absorbance spectrum
            prominence: Minimum prominence
            
        Returns:
            Peak information
        """
        from scipy.signal import find_peaks
        
        # Find peaks
        peaks, properties = find_peaks(
            absorbance,
            prominence=prominence,
            width=2
        )
        
        if len(peaks) == 0:
            return {
                'n_peaks': 0,
                'peak_wavelengths': np.array([]),
                'peak_absorbances': np.array([])
            }
            
        return {
            'n_peaks': len(peaks),
            'peak_wavelengths': wavelengths[peaks],
            'peak_absorbances': absorbance[peaks],
            'peak_widths': properties['widths'],
            'peak_prominences': properties['prominences']
        }
        
    def compare_spectra(self,
                       spectrum_A: np.ndarray,
                       spectrum_B: np.ndarray,
                       wavelengths: np.ndarray) -> Dict:
        """
        Compare two absorption spectra
        
        Args:
            spectrum_A: First absorbance spectrum
            spectrum_B: Second absorbance spectrum
            wavelengths: Wavelength axis
            
        Returns:
            Comparison metrics
        """
        # Correlation
        correlation = np.corrcoef(spectrum_A, spectrum_B)[0, 1]
        
        # RMS difference
        rms_diff = np.sqrt(np.mean((spectrum_A - spectrum_B)**2))
        
        # Normalize to 0-1
        norm_A = (spectrum_A - spectrum_A.min()) / (spectrum_A.max() - spectrum_A.min() + 1e-10)
        norm_B = (spectrum_B - spectrum_B.min()) / (spectrum_B.max() - spectrum_B.min() + 1e-10)
        
        # Spectral angle
        dot_product = np.dot(norm_A, norm_B)
        norm_A_mag = np.linalg.norm(norm_A)
        norm_B_mag = np.linalg.norm(norm_B)
        
        if norm_A_mag > 0 and norm_B_mag > 0:
            cos_angle = dot_product / (norm_A_mag * norm_B_mag)
            spectral_angle = np.arccos(np.clip(cos_angle, -1, 1))
        else:
            spectral_angle = np.pi / 2
            
        # Similarity score (1 = identical, 0 = orthogonal)
        similarity = 1 - (spectral_angle / (np.pi / 2))
        
        return {
            'correlation': correlation,
            'rms_difference': rms_diff,
            'spectral_angle_rad': spectral_angle,
            'similarity_score': similarity,
            'match': similarity > 0.95
        }
        
    def estimate_concentration(self,
                             sample_absorbance: np.ndarray,
                             reference_absorbance: np.ndarray,
                             reference_concentration: float,
                             wavelength_index: int) -> Dict:
        """
        Estimate concentration from absorbance
        
        Args:
            sample_absorbance: Sample absorbance spectrum
            reference_absorbance: Reference absorbance (known concentration)
            reference_concentration: Reference concentration (mol/L)
            wavelength_index: Wavelength to use for comparison
            
        Returns:
            Estimated concentration
        """
        # Beer-Lambert: A ∝ c (at same wavelength and path length)
        A_sample = sample_absorbance[wavelength_index]
        A_reference = reference_absorbance[wavelength_index]
        
        if A_reference <= 0:
            raise ValueError("Reference absorbance must be positive")
            
        # c_sample = c_reference * (A_sample / A_reference)
        concentration = reference_concentration * (A_sample / A_reference)
        
        return {
            'estimated_concentration': concentration,
            'reference_concentration': reference_concentration,
            'absorbance_ratio': A_sample / A_reference,
            'wavelength_index': wavelength_index
        }
