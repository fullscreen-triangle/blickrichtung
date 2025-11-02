"""
S-Entropy Optical Mapping
==========================

Maps optical spectra to S-entropy coordinates.
"""

import numpy as np
import sys
sys.path.append('../../grand_unification')
from s_entropy import SEntropyCalculator
from oscillatory_signatures import OscillatorySignature


class SOpticalMapper:
    """
    Maps optical spectra to S-entropy space
    """
    
    def __init__(self):
        """Initialize optical S-entropy mapper"""
        self.s_calc = SEntropyCalculator(domain='optical')
        
    def spectrum_to_oscillatory_signature(self,
                                         wavelengths: np.ndarray,
                                         absorbance: np.ndarray) -> OscillatorySignature:
        """
        Convert absorption spectrum to oscillatory signature
        
        Args:
            wavelengths: Wavelength axis (nm)
            absorbance: Absorbance spectrum
            
        Returns:
            OscillatorySignature
        """
        # Convert wavelength to frequency
        # f = c / λ
        c = 299792458  # m/s
        wavelengths_m = wavelengths * 1e-9
        frequencies = c / wavelengths_m  # Hz
        
        # Sort by frequency (increasing)
        sorted_indices = np.argsort(frequencies)
        frequencies_sorted = frequencies[sorted_indices]
        absorbance_sorted = absorbance[sorted_indices]
        
        # Absorbance as amplitude
        amplitudes = absorbance_sorted
        
        # Phase: set to zero for absorption spectra
        phases = np.zeros_like(frequencies_sorted)
        
        # Estimate Q-factors from peak widths
        Q_factors = self._estimate_q_factors_from_spectrum(
            frequencies_sorted,
            amplitudes
        )
        
        # Power spectrum
        power_spectrum = amplitudes**2
        
        # Time-domain representation (inverse FFT for completeness)
        # This is somewhat artificial for absorption spectra
        time_signal = np.fft.irfft(amplitudes * np.exp(1j * phases))
        n_samples = len(time_signal)
        dt = 1.0 / (2 * frequencies_sorted[-1])  # Nyquist
        timestamps = np.arange(n_samples) * dt
        
        return OscillatorySignature(
            frequencies=frequencies_sorted,
            amplitudes=amplitudes,
            phases=phases,
            Q_factors=Q_factors,
            power_spectrum=power_spectrum,
            frequency_axis=frequencies_sorted,
            time_signal=time_signal,
            timestamps=timestamps
        )
        
    def calculate_s_entropy(self, signature: OscillatorySignature) -> np.ndarray:
        """
        Calculate S-entropy coordinates from optical signature
        
        Args:
            signature: Oscillatory signature
            
        Returns:
            S-entropy coordinates (S1, S2, S3)
        """
        return self.s_calc.calculate(signature)
        
    def spectrum_to_s_coords(self,
                            wavelengths: np.ndarray,
                            absorbance: np.ndarray) -> np.ndarray:
        """
        Direct conversion from spectrum to S-entropy
        
        Args:
            wavelengths: Wavelength axis (nm)
            absorbance: Absorbance spectrum
            
        Returns:
            S-entropy coordinates
        """
        signature = self.spectrum_to_oscillatory_signature(
            wavelengths,
            absorbance
        )
        
        return self.calculate_s_entropy(signature)
        
    def multi_wavelength_to_s_coords(self,
                                    led_measurements: Dict) -> np.ndarray:
        """
        Combine multiple LED measurements into S-coords
        
        Args:
            led_measurements: Dict with keys 'blue', 'green', 'red',
                            each containing wavelength and absorbance
            
        Returns:
            Combined S-entropy coordinates
        """
        # Combine all measurements
        all_wavelengths = []
        all_absorbances = []
        
        for color in ['blue', 'green', 'red']:
            if color in led_measurements:
                meas = led_measurements[color]
                all_wavelengths.extend(meas['wavelengths'])
                all_absorbances.extend(meas['absorbance'])
                
        # Sort by wavelength
        sorted_indices = np.argsort(all_wavelengths)
        wavelengths = np.array(all_wavelengths)[sorted_indices]
        absorbances = np.array(all_absorbances)[sorted_indices]
        
        # Convert to S-coords
        return self.spectrum_to_s_coords(wavelengths, absorbances)
        
    def _estimate_q_factors_from_spectrum(self,
                                         frequencies: np.ndarray,
                                         amplitudes: np.ndarray) -> np.ndarray:
        """
        Estimate Q-factors from spectral peaks
        
        Args:
            frequencies: Frequency axis
            amplitudes: Amplitude spectrum
            
        Returns:
            Q-factors
        """
        from scipy.signal import find_peaks
        
        # Find peaks
        peaks, properties = find_peaks(
            amplitudes,
            prominence=0.1 * np.max(amplitudes),
            width=2
        )
        
        if len(peaks) == 0:
            # No peaks, use default
            return np.ones(len(frequencies)) * 10.0
            
        # Initialize Q-factors
        Q_factors = np.ones(len(frequencies)) * 10.0
        
        # For each peak, estimate Q
        for i, peak_idx in enumerate(peaks):
            f0 = frequencies[peak_idx]
            width = properties['widths'][i]
            
            # Estimate bandwidth from width
            # Δf ≈ width * Δf_per_point
            df = np.mean(np.diff(frequencies))
            bandwidth = width * df
            
            if bandwidth > 0:
                Q = f0 / bandwidth
            else:
                Q = 100.0
                
            # Assign to nearby points
            Q_factors[peak_idx] = Q
            
        return Q_factors
        
    def calculate_chromophore_signature(self,
                                       wavelengths: np.ndarray,
                                       absorbance: np.ndarray) -> Dict:
        """
        Analyze chromophore characteristics from spectrum
        
        Args:
            wavelengths: Wavelength axis (nm)
            absorbance: Absorbance spectrum
            
        Returns:
            Chromophore signature
        """
        # Find absorption maximum
        max_idx = np.argmax(absorbance)
        lambda_max = wavelengths[max_idx]
        A_max = absorbance[max_idx]
        
        # Find absorption edge (wavelength where A drops to 10% of max)
        edge_threshold = 0.1 * A_max
        long_wavelength_edge = None
        short_wavelength_edge = None
        
        # Search long wavelength side
        for i in range(max_idx, len(wavelengths)):
            if absorbance[i] < edge_threshold:
                long_wavelength_edge = wavelengths[i]
                break
                
        # Search short wavelength side
        for i in range(max_idx, -1, -1):
            if absorbance[i] < edge_threshold:
                short_wavelength_edge = wavelengths[i]
                break
                
        # Bandwidth
        if long_wavelength_edge and short_wavelength_edge:
            bandwidth = long_wavelength_edge - short_wavelength_edge
        else:
            bandwidth = None
            
        return {
            'lambda_max': lambda_max,
            'A_max': A_max,
            'bandwidth': bandwidth,
            'long_wavelength_edge': long_wavelength_edge,
            'short_wavelength_edge': short_wavelength_edge,
            'integrated_absorbance': np.trapz(absorbance, wavelengths)
        }
