"""
S-Entropy Coordinate System

Universal coordinate system for oscillatory phenomena across domains.

Theoretical Foundation:
- S-entropy provides domain-independent representation of oscillatory information
- Three coordinates capture: primary content, gradients, and couplings
- Enables cross-domain comparison (molecular ↔ acoustic ↔ thermal ↔ etc.)
- Distance in S-entropy space → perceptual/functional similarity

Mathematical Framework:
- S₁: Primary oscillatory content (weighted frequency integral)
- S₂: Oscillatory gradients (variability, complexity)
- S₃: Oscillatory couplings (interactions, correlations)

Physical Interpretation:
- S-entropy coordinates are NOT thermodynamic entropy
- "Saint" = Stella's Adaptive Information Notation Transform
- Provides universal "language" for biological information processing
- Consciousness operates by comparing S-entropy coordinates

Applications:
- Scent similarity: Similar S-entropy → similar smell
- Drug effects: Similar S-entropy → similar pharmacology
- Cross-modal perception: Map any sensory domain to S-entropy space
"""

import numpy as np
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple, Optional, Callable
from dataclasses import dataclass, asdict
from scipy import signal, integrate, fft
from scipy.stats import entropy


@dataclass
class SEntropyCoordinates:
    """
    S-entropy coordinates for an oscillatory phenomenon.
    
    Attributes:
        S1: Primary oscillatory content
        S2: Oscillatory gradients/variability
        S3: Oscillatory couplings/interactions
        domain: Source domain ('molecular', 'acoustic', etc.)
        metadata: Optional additional information
    """
    S1: float
    S2: float
    S3: float
    domain: str
    metadata: Optional[Dict] = None
    
    def to_array(self) -> np.ndarray:
        """Convert to [3] numpy array."""
        return np.array([self.S1, self.S2, self.S3], dtype=np.float64)
    
    def to_dict(self) -> dict:
        """Convert to JSON-serializable dictionary."""
        d = {
            'S1': float(self.S1),
            'S2': float(self.S2),
            'S3': float(self.S3),
            'domain': self.domain
        }
        if self.metadata:
            d['metadata'] = self.metadata
        return d
    
    def distance_to(self, other: 'SEntropyCoordinates', metric: str = 'euclidean') -> float:
        """
        Calculate distance to another S-entropy coordinate.
        
        Args:
            other: Other S-entropy coordinates
            metric: Distance metric ('euclidean', 'manhattan', 'cosine')
        
        Returns:
            Distance value
        """
        v1 = self.to_array()
        v2 = other.to_array()
        
        if metric == 'euclidean':
            return float(np.linalg.norm(v1 - v2))
        elif metric == 'manhattan':
            return float(np.sum(np.abs(v1 - v2)))
        elif metric == 'cosine':
            dot_product = np.dot(v1, v2)
            norms = np.linalg.norm(v1) * np.linalg.norm(v2)
            if norms == 0:
                return 1.0
            return float(1.0 - dot_product / norms)
        else:
            raise ValueError(f"Unknown metric: {metric}")


class SEntropyCalculator:
    """
    Calculate S-entropy coordinates from oscillatory data.
    
    Supports multiple input types:
    - Time-series data (raw oscillations)
    - Frequency spectra (FFT/PSD)
    - Oscillatory signatures ([5] feature vectors)
    - O₂ categorical state distributions
    
    Domain-specific weighting ensures meaningful cross-domain comparison.
    """
    
    def __init__(self, domain: str = 'molecular'):
        """
        Initialize S-entropy calculator.
        
        Args:
            domain: Domain type ('molecular', 'acoustic', 'thermal', 'visual', 'generic')
        """
        self.domain = domain
        self.weights = self._get_domain_weights(domain)
        self.normalization = self._get_normalization_constants(domain)
    
    def _get_domain_weights(self, domain: str) -> Dict[str, Callable]:
        """
        Get frequency weighting functions for domain.
        
        Different domains emphasize different frequency ranges:
        - Molecular: THz range (10¹²-10¹⁴ Hz)
        - Acoustic: Hz-kHz range (10-10⁴ Hz)
        - Thermal: mHz-Hz range (10⁻³-10 Hz)
        - Visual: ~10¹⁴ Hz (optical frequencies)
        """
        if domain == 'molecular':
            f0 = 1e13  # 10 THz (O₂ cycling frequency)
            sigma = 1e12  # 1 THz bandwidth
            return {
                'w1': lambda f: np.exp(-((f - f0) / sigma)**2),  # Gaussian centered at f0
                'w2': lambda f: f / (f0 + f),  # Frequency-dependent
                'w3': lambda f: 1.0 / (1.0 + (f / f0)**2)  # Lorentzian
            }
        
        elif domain == 'acoustic':
            f0 = 120.0  # 120 Hz (typical pitch)
            sigma = 50.0
            return {
                'w1': lambda f: np.exp(-((f - f0) / sigma)**2),
                'w2': lambda f: f / (1000 + f),
                'w3': lambda f: 1.0 / (1.0 + (f / 100)**2)
            }
        
        elif domain == 'thermal':
            f0 = 0.1  # 0.1 Hz
            sigma = 0.05
            return {
                'w1': lambda f: np.exp(-((f - f0) / sigma)**2),
                'w2': lambda f: f / (1.0 + f),
                'w3': lambda f: 1.0 / (1.0 + (f / 0.1)**2)
            }
        
        elif domain == 'visual':
            f0 = 5e14  # ~500 THz (green light)
            sigma = 1e14
            return {
                'w1': lambda f: np.exp(-((f - f0) / sigma)**2),
                'w2': lambda f: f / (1e15 + f),
                'w3': lambda f: 1.0 / (1.0 + (f / 5e14)**2)
            }
        
        else:  # Generic
            return {
                'w1': lambda f: np.ones_like(f),
                'w2': lambda f: np.ones_like(f),
                'w3': lambda f: np.ones_like(f)
            }
    
    def _get_normalization_constants(self, domain: str) -> Dict[str, float]:
        """
        Get normalization constants for domain.
        
        Ensures S-entropy coordinates are in comparable ranges across domains.
        """
        if domain == 'molecular':
            return {'S1': 1e13, 'S2': 1e12, 'S3': 1e11}
        elif domain == 'acoustic':
            return {'S1': 100.0, 'S2': 10.0, 'S3': 1.0}
        elif domain == 'thermal':
            return {'S1': 1.0, 'S2': 0.1, 'S3': 0.01}
        elif domain == 'visual':
            return {'S1': 1e14, 'S2': 1e13, 'S3': 1e12}
        else:
            return {'S1': 1.0, 'S2': 1.0, 'S3': 1.0}
    
    def calculate_from_timeseries(self,
                                   timeseries: np.ndarray,
                                   sampling_rate: float,
                                   metadata: Optional[Dict] = None) -> SEntropyCoordinates:
        """
        Calculate S-entropy from time-series data.
        
        Args:
            timeseries: Time-series data [n_samples]
            sampling_rate: Sampling rate in Hz
            metadata: Optional metadata
        
        Returns:
            SEntropyCoordinates
        """
        # Compute power spectral density
        freqs, psd = signal.welch(timeseries, fs=sampling_rate, nperseg=min(1024, len(timeseries)))
        
        # Remove DC component
        freqs = freqs[1:]
        psd = psd[1:]
        
        # Calculate S-entropy coordinates
        S1 = self._calculate_S1(freqs, psd)
        S2 = self._calculate_S2(freqs, psd, timeseries, sampling_rate)
        S3 = self._calculate_S3(freqs, psd, timeseries)
        
        return SEntropyCoordinates(
            S1=S1,
            S2=S2,
            S3=S3,
            domain=self.domain,
            metadata=metadata
        )
    
    def calculate_from_signature(self,
                                 signature: np.ndarray,
                                 metadata: Optional[Dict] = None) -> SEntropyCoordinates:
        """
        Calculate S-entropy from oscillatory signature.
        
        Args:
            signature: [5] oscillatory features [freq, amp, phase, damp, symm]
            metadata: Optional metadata
        
        Returns:
            SEntropyCoordinates
        """
        freq, amp, phase, damp, symm = signature
        
        # S1: Primary content (weighted by amplitude and frequency)
        w1_val = self.weights['w1'](freq)
        S1 = freq * amp * w1_val / self.normalization['S1']
        
        # S2: Variability (from damping and symmetry)
        # High damping = high variability
        # Low symmetry = high variability
        variability = (1.0 - damp) * (1.0 - symm)
        w2_val = self.weights['w2'](freq)
        S2 = freq * variability * w2_val / self.normalization['S2']
        
        # S3: Coupling strength (from phase and symmetry)
        # Phase coherence + symmetry = strong coupling
        coupling = np.cos(phase) * symm
        w3_val = self.weights['w3'](freq)
        S3 = freq * coupling * w3_val / self.normalization['S3']
        
        return SEntropyCoordinates(
            S1=S1,
            S2=S2,
            S3=S3,
            domain=self.domain,
            metadata=metadata
        )
    
    def calculate_from_spectrum(self,
                               frequencies: np.ndarray,
                               power: np.ndarray,
                               metadata: Optional[Dict] = None) -> SEntropyCoordinates:
        """
        Calculate S-entropy from frequency spectrum.
        
        Args:
            frequencies: Frequency array [n_freqs]
            power: Power at each frequency [n_freqs]
            metadata: Optional metadata
        
        Returns:
            SEntropyCoordinates
        """
        # Normalize power
        power_norm = power / (np.sum(power) + 1e-10)
        
        S1 = self._calculate_S1(frequencies, power_norm)
        S2 = self._calculate_S2_from_spectrum(frequencies, power_norm)
        S3 = self._calculate_S3_from_spectrum(frequencies, power_norm)
        
        return SEntropyCoordinates(
            S1=S1,
            S2=S2,
            S3=S3,
            domain=self.domain,
            metadata=metadata
        )
    
    def _calculate_S1(self, freqs: np.ndarray, psd: np.ndarray) -> float:
        """
        Calculate S1: Primary oscillatory content.
        
        S1 = ∫ f · P(f) · w1(f) df
        
        This captures the dominant frequency content weighted by domain-specific
        importance function w1(f).
        """
        # Apply weight function
        weights = self.weights['w1'](freqs)
        
        # Weighted frequency integral
        integrand = freqs * psd * weights
        S1 = integrate.simpson(integrand, x=freqs)
        
        # Normalize
        S1 /= self.normalization['S1']
        
        return float(S1)
    
    def _calculate_S2(self,
                     freqs: np.ndarray,
                     psd: np.ndarray,
                     timeseries: np.ndarray,
                     sampling_rate: float) -> float:
        """
        Calculate S2: Oscillatory gradients/variability.
        
        S2 quantifies how much the oscillatory content changes:
        - Spectral entropy (frequency diversity)
        - Temporal variability (amplitude modulation)
        """
        # Spectral entropy
        psd_norm = psd / (np.sum(psd) + 1e-10)
        spectral_entropy = entropy(psd_norm)
        
        # Temporal variability (from envelope)
        analytic_signal = signal.hilbert(timeseries)
        envelope = np.abs(analytic_signal)
        envelope_std = np.std(envelope) / (np.mean(envelope) + 1e-10)
        
        # Apply weight function
        weights = self.weights['w2'](freqs)
        weighted_entropy = spectral_entropy * np.mean(weights)
        
        # Combine
        S2 = (weighted_entropy + envelope_std) / self.normalization['S2']
        
        return float(S2)
    
    def _calculate_S2_from_spectrum(self, freqs: np.ndarray, power: np.ndarray) -> float:
        """Calculate S2 from spectrum only (when timeseries unavailable)."""
        # Spectral entropy
        power_norm = power / (np.sum(power) + 1e-10)
        spectral_entropy = entropy(power_norm)
        
        # Spectral spread (bandwidth)
        mean_freq = np.sum(freqs * power_norm)
        spread = np.sqrt(np.sum(((freqs - mean_freq)**2) * power_norm))
        spread_norm = spread / (mean_freq + 1e-10)
        
        # Apply weight
        weights = self.weights['w2'](freqs)
        weighted_entropy = spectral_entropy * np.mean(weights)
        
        S2 = (weighted_entropy + spread_norm) / self.normalization['S2']
        
        return float(S2)
    
    def _calculate_S3(self, freqs: np.ndarray, psd: np.ndarray, timeseries: np.ndarray) -> float:
        """
        Calculate S3: Oscillatory couplings/interactions.
        
        S3 quantifies how different frequency components interact:
        - Phase coherence across frequencies
        - Cross-frequency coupling
        - Nonlinear interactions
        """
        # Phase coherence from Hilbert transform
        analytic_signal = signal.hilbert(timeseries)
        phase = np.angle(analytic_signal)
        
        # Phase variance (low = high coherence)
        phase_coherence = 1.0 / (1.0 + np.var(np.diff(phase)))
        
        # Cross-frequency coupling: bispectrum estimate (simplified)
        # For full implementation, would use higher-order spectra
        # Here we use autocorrelation of PSD as proxy
        psd_autocorr = np.correlate(psd, psd, mode='same')
        coupling_strength = np.max(psd_autocorr[len(psd_autocorr)//2:]) / (psd_autocorr[len(psd_autocorr)//2] + 1e-10)
        
        # Apply weight
        weights = self.weights['w3'](freqs)
        weighted_coupling = coupling_strength * np.mean(weights)
        
        S3 = (phase_coherence + weighted_coupling) / self.normalization['S3']
        
        return float(S3)
    
    def _calculate_S3_from_spectrum(self, freqs: np.ndarray, power: np.ndarray) -> float:
        """Calculate S3 from spectrum only."""
        # Peak prominence (strong peaks = strong coupling)
        peaks, properties = signal.find_peaks(power, prominence=0.1*np.max(power))
        
        if len(peaks) == 0:
            peak_strength = 0.0
        else:
            peak_strength = np.mean(properties['prominences']) / (np.mean(power) + 1e-10)
        
        # Spectral correlation (autocorrelation of power)
        power_autocorr = np.correlate(power, power, mode='same')
        correlation_strength = np.max(power_autocorr) / (power_autocorr[len(power_autocorr)//2] + 1e-10)
        
        # Apply weight
        weights = self.weights['w3'](freqs)
        weighted_coupling = (peak_strength + correlation_strength) * np.mean(weights)
        
        S3 = weighted_coupling / self.normalization['S3']
        
        return float(S3)
    
    def save_coordinates(self,
                        coordinates: SEntropyCoordinates,
                        output_path: str) -> None:
        """
        Save S-entropy coordinates to JSON.
        
        Args:
            coordinates: S-entropy coordinates to save
            output_path: Path to output file
        """
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        data = {
            'timestamp': datetime.now().isoformat(),
            'coordinates': coordinates.to_dict()
        }
        
        with open(output_path, 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"✓ Saved S-entropy coordinates to {output_path}")
    
    def save_batch_coordinates(self,
                              coordinates_dict: Dict[str, SEntropyCoordinates],
                              output_path: str) -> None:
        """
        Save batch of S-entropy coordinates.
        
        Args:
            coordinates_dict: Dict[name] = SEntropyCoordinates
            output_path: Path to output file
        """
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        data = {
            'timestamp': datetime.now().isoformat(),
            'domain': self.domain,
            'num_items': len(coordinates_dict),
            'coordinates': {
                name: coords.to_dict()
                for name, coords in coordinates_dict.items()
            }
        }
        
        with open(output_path, 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"✓ Saved {len(coordinates_dict)} S-entropy coordinates to {output_path}")


def calculate_similarity_matrix(coordinates_list: List[SEntropyCoordinates],
                                metric: str = 'euclidean') -> np.ndarray:
    """
    Calculate pairwise similarity matrix for S-entropy coordinates.
    
    Args:
        coordinates_list: List of S-entropy coordinates
        metric: Distance metric
    
    Returns:
        np.ndarray: [n, n] distance matrix
    """
    n = len(coordinates_list)
    matrix = np.zeros((n, n), dtype=np.float64)
    
    for i in range(n):
        for j in range(i+1, n):
            dist = coordinates_list[i].distance_to(coordinates_list[j], metric)
            matrix[i, j] = dist
            matrix[j, i] = dist
    
    return matrix


def demonstrate_sentropy():
    """Demonstrate S-entropy calculation."""
    print("="*80)
    print("S-ENTROPY COORDINATE SYSTEM DEMONSTRATION")
    print("="*80 + "\n")
    
    # Initialize calculator
    calc = SEntropyCalculator(domain='molecular')
    
    print("Domain: molecular")
    print("Normalization constants:")
    print(f"  S1: {calc.normalization['S1']:.2e}")
    print(f"  S2: {calc.normalization['S2']:.2e}")
    print(f"  S3: {calc.normalization['S3']:.2e}")
    print()
    
    # Test with oscillatory signatures
    print("Test 1: From Oscillatory Signatures")
    print("-"*80)
    
    signatures = {
        'Vanillin': np.array([1.5e13, 5.0, 1.2, 0.7, 0.8]),
        'Ethyl Vanillin': np.array([1.52e13, 5.1, 1.25, 0.68, 0.82]),
        'Indole': np.array([2.1e13, 6.2, 2.3, 0.4, 0.5]),
    }
    
    coords_dict = {}
    
    for name, sig in signatures.items():
        coords = calc.calculate_from_signature(sig, metadata={'molecule': name})
        coords_dict[name] = coords
        
        print(f"{name}:")
        print(f"  Signature: {sig}")
        print(f"  S-entropy: (S1={coords.S1:.3f}, S2={coords.S2:.3f}, S3={coords.S3:.3f})")
        print()
    
    # Calculate similarity
    print("Similarity Analysis:")
    print("-"*80)
    
    van_indole_dist = coords_dict['Vanillin'].distance_to(coords_dict['Indole'])
    van_ethylvan_dist = coords_dict['Vanillin'].distance_to(coords_dict['Ethyl Vanillin'])
    
    print(f"Vanillin ↔ Ethyl Vanillin: {van_ethylvan_dist:.4f}")
    print(f"Vanillin ↔ Indole: {van_indole_dist:.4f}")
    print(f"Ratio (similar/dissimilar): {van_ethylvan_dist/van_indole_dist:.4f}")
    print()
    
    if van_ethylvan_dist < van_indole_dist:
        print("✓ Similar molecules (both vanilla) are closer in S-entropy space")
    else:
        print("✗ Unexpected: dissimilar molecules are closer")
    print()
    
    # Test with synthetic time series
    print("\nTest 2: From Time Series")
    print("-"*80)
    
    # Generate synthetic molecular oscillation
    t = np.linspace(0, 1e-11, 10000)  # 10 ps
    signal1 = np.sin(2*np.pi*1.5e13*t) + 0.2*np.sin(2*np.pi*3e13*t)
    
    coords_ts = calc.calculate_from_timeseries(
        signal1,
        sampling_rate=1/np.mean(np.diff(t)),
        metadata={'type': 'synthetic'}
    )
    
    print(f"Time series S-entropy: (S1={coords_ts.S1:.3f}, S2={coords_ts.S2:.3f}, S3={coords_ts.S3:.3f})")
    print()
    
    # Save results
    print("Saving Results:")
    print("-"*80)
    
    output_dir = Path("results/sentropy")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    calc.save_batch_coordinates(
        coords_dict,
        output_dir / "sentropy_coordinates.json"
    )
    
    # Save similarity matrix
    coords_list = list(coords_dict.values())
    sim_matrix = calculate_similarity_matrix(coords_list)
    
    sim_data = {
        'timestamp': datetime.now().isoformat(),
        'molecules': list(coords_dict.keys()),
        'similarity_matrix': sim_matrix.tolist(),
        'metric': 'euclidean'
    }
    
    with open(output_dir / "similarity_matrix.json", 'w') as f:
        json.dump(sim_data, f, indent=2)
    
    print(f"✓ Saved similarity matrix")
    
    print("\n✓ Demonstration complete!")


if __name__ == "__main__":
    demonstrate_sentropy()

