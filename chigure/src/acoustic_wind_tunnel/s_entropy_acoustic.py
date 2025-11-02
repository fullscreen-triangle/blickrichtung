"""
S-Entropy Acoustic Mapping
===========================

Maps acoustic measurements to S-entropy coordinates.
"""

import numpy as np
import sys
sys.path.append('../../grand_unification')
from s_entropy import SEntropyCalculator
from oscillatory_signatures import OscillatorySignature


class SAcousticMapper:
    """
    Maps acoustic data to S-entropy space
    """
    
    def __init__(self):
        """Initialize acoustic S-entropy mapper"""
        self.s_calc = SEntropyCalculator(domain='acoustic')
        
    def extract_acoustic_signature(self,
                                   pressure_field: np.ndarray,
                                   timestamps: np.ndarray,
                                   mic_positions: np.ndarray) -> OscillatorySignature:
        """
        Extract oscillatory signature from acoustic measurement
        
        Args:
            pressure_field: Pressure at each mic, shape (n_mics, n_samples)
            timestamps: Time vector
            mic_positions: Microphone positions
            
        Returns:
            OscillatorySignature
        """
        # Combine all microphone data
        combined_signal = np.mean(pressure_field, axis=0)
        
        # FFT analysis
        n_samples = len(combined_signal)
        dt = timestamps[1] - timestamps[0]
        freqs = np.fft.rfftfreq(n_samples, dt)
        fft_result = np.fft.rfft(combined_signal)
        
        magnitudes = np.abs(fft_result)
        phases = np.angle(fft_result)
        
        # Find dominant peaks
        n_peaks = 50
        peak_indices = np.argsort(magnitudes)[-n_peaks:][::-1]
        
        dominant_freqs = freqs[peak_indices]
        dominant_amps = magnitudes[peak_indices]
        dominant_phases = phases[peak_indices]
        
        # Estimate Q-factors from peak widths
        Q_factors = self._estimate_q_factors(freqs, magnitudes, dominant_freqs)
        
        # Power spectrum
        power_spectrum = magnitudes**2
        
        return OscillatorySignature(
            frequencies=dominant_freqs,
            amplitudes=dominant_amps,
            phases=dominant_phases,
            Q_factors=Q_factors,
            power_spectrum=power_spectrum,
            frequency_axis=freqs,
            time_signal=combined_signal,
            timestamps=timestamps
        )
        
    def calculate_s_entropy(self, signature: OscillatorySignature) -> np.ndarray:
        """
        Calculate S-entropy coordinates from acoustic signature
        
        Args:
            signature: Oscillatory signature
            
        Returns:
            S-entropy coordinates (S1, S2, S3)
        """
        return self.s_calc.calculate(signature)
        
    def acoustic_to_s_coords(self,
                            pressure_field: np.ndarray,
                            timestamps: np.ndarray,
                            mic_positions: np.ndarray) -> np.ndarray:
        """
        Direct conversion from acoustic data to S-entropy
        
        Args:
            pressure_field: Pressure field
            timestamps: Time vector
            mic_positions: Mic positions
            
        Returns:
            S-entropy coordinates
        """
        signature = self.extract_acoustic_signature(
            pressure_field,
            timestamps,
            mic_positions
        )
        
        return self.calculate_s_entropy(signature)
        
    def _estimate_q_factors(self,
                           freqs: np.ndarray,
                           magnitudes: np.ndarray,
                           peak_freqs: np.ndarray) -> np.ndarray:
        """
        Estimate Q-factors from peak widths
        
        Args:
            freqs: Frequency axis
            magnitudes: Magnitude spectrum
            peak_freqs: Peak frequencies
            
        Returns:
            Q-factors for each peak
        """
        Q_factors = np.zeros(len(peak_freqs))
        
        for i, f0 in enumerate(peak_freqs):
            # Find peak in spectrum
            idx = np.argmin(np.abs(freqs - f0))
            peak_mag = magnitudes[idx]
            
            # Find half-power points
            half_power = peak_mag / np.sqrt(2)
            
            # Search left
            idx_left = idx
            while idx_left > 0 and magnitudes[idx_left] > half_power:
                idx_left -= 1
                
            # Search right
            idx_right = idx
            while idx_right < len(freqs) - 1 and magnitudes[idx_right] > half_power:
                idx_right += 1
                
            # Bandwidth
            f_left = freqs[idx_left]
            f_right = freqs[idx_right]
            bandwidth = f_right - f_left
            
            if bandwidth > 0:
                Q_factors[i] = f0 / bandwidth
            else:
                Q_factors[i] = 100.0  # High Q if very narrow
                
        return Q_factors
