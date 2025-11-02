"""
Acoustic Velocimetry
====================

Cross-correlation analysis for velocity measurement from phase shifts.
"""

import numpy as np
from typing import Dict, Tuple
from scipy.signal import correlate, hilbert
from scipy.fft import fft, ifft, fftfreq


class CrossCorrelationVelocimetry:
    """
    Measure velocity from time-of-flight between microphones
    """
    
    def __init__(self):
        """Initialize velocimetry"""
        pass
        
    def measure_velocity_tof(self,
                            signal_A: np.ndarray,
                            signal_B: np.ndarray,
                            separation: float,
                            sample_rate: int) -> Dict:
        """
        Time-of-flight velocity measurement
        
        Args:
            signal_A: First microphone signal
            signal_B: Second microphone signal
            separation: Distance between mics (m)
            sample_rate: Sample rate (Hz)
            
        Returns:
            Velocity and confidence
        """
        # Cross-correlation
        correlation = correlate(signal_A, signal_B, mode='full')
        
        # Find peak
        peak_idx = np.argmax(np.abs(correlation))
        n_samples = len(signal_A)
        lag_samples = peak_idx - (n_samples - 1)
        
        # Convert to time
        time_delay = lag_samples / sample_rate
        
        # Calculate velocity
        if abs(time_delay) < 1e-9:
            velocity = 0.0
            confidence = 0.0
        else:
            velocity = separation / time_delay
            
            # Confidence from peak sharpness
            peak_value = np.abs(correlation[peak_idx])
            noise_level = np.median(np.abs(correlation))
            snr = peak_value / (noise_level + 1e-10)
            confidence = min(snr / 10.0, 1.0)
            
        return {
            'velocity': velocity,
            'time_delay': time_delay,
            'confidence': confidence,
            'correlation': correlation
        }
        
    def measure_velocity_phase(self,
                              signal_A: np.ndarray,
                              signal_B: np.ndarray,
                              separation: float,
                              carrier_frequency: float,
                              sample_rate: int) -> Dict:
        """
        Phase-based velocity measurement (more precise)
        
        Args:
            signal_A: First microphone signal
            signal_B: Second microphone signal
            separation: Distance between mics (m)
            carrier_frequency: Carrier frequency (Hz)
            sample_rate: Sample rate (Hz)
            
        Returns:
            Velocity and metrics
        """
        # Analytic signals
        analytic_A = hilbert(signal_A)
        analytic_B = hilbert(signal_B)
        
        # Instantaneous phases
        phase_A = np.unwrap(np.angle(analytic_A))
        phase_B = np.unwrap(np.angle(analytic_B))
        
        # Phase difference (median for stability)
        phase_diff = np.median(phase_B - phase_A)
        
        # Wavelength
        c_sound = 343  # m/s
        wavelength = c_sound / carrier_frequency
        
        # Phase in cycles
        phase_cycles = phase_diff / (2 * np.pi)
        
        # Distance = phase_cycles * wavelength
        # If distance known, can infer velocity from phase shift
        # For streaming, phase relates to acoustic intensity gradient
        
        # Time delay from phase
        time_delay = phase_cycles / carrier_frequency
        
        # Velocity
        if abs(time_delay) < 1e-9:
            velocity = 0.0
        else:
            velocity = separation / time_delay
            
        return {
            'velocity': velocity,
            'phase_difference': phase_diff,
            'time_delay': time_delay,
            'wavelength': wavelength
        }
        
    def calculate_velocity_field_multi_mic(self,
                                          signals: np.ndarray,
                                          mic_positions: np.ndarray,
                                          carrier_frequency: float,
                                          sample_rate: int) -> Dict:
        """
        Calculate 2D velocity field from multiple microphones
        
        Args:
            signals: Microphone signals, shape (n_mics, n_samples)
            mic_positions: Positions, shape (n_mics, 3)
            carrier_frequency: Carrier frequency (Hz)
            sample_rate: Sample rate (Hz)
            
        Returns:
            Velocity field
        """
        n_mics = signals.shape[0]
        
        # Pairwise velocities
        velocities = []
        pairs = []
        
        for i in range(n_mics):
            for j in range(i + 1, n_mics):
                # Separation
                sep_vector = mic_positions[j] - mic_positions[i]
                separation = np.linalg.norm(sep_vector)
                
                if separation < 0.001:  # Skip if too close
                    continue
                    
                # Measure velocity
                result = self.measure_velocity_phase(
                    signals[i],
                    signals[j],
                    separation,
                    carrier_frequency,
                    sample_rate
                )
                
                velocities.append(result['velocity'])
                pairs.append((i, j))
                
        return {
            'pairwise_velocities': np.array(velocities),
            'pairs': pairs,
            'mean_velocity': np.mean(velocities),
            'std_velocity': np.std(velocities)
        }
