"""
Oscillatory Signature Framework

Universal representation for oscillatory phenomena across all domains.

Theoretical Foundation:
- All perception operates through oscillatory resonance
- Oscillatory signatures are the "language" of consciousness
- Five fundamental components capture complete oscillatory behavior:
  1. Frequency - primary oscillation rate
  2. Amplitude - oscillation strength
  3. Phase - temporal offset
  4. Damping - decay/persistence
  5. Symmetry - structural regularity

Cross-Domain Universality:
- Molecular: vibrational signatures
- Acoustic: sound patterns
- Visual: light frequencies
- Thermal: temperature oscillations
- Neural: firing patterns

All map to same [5] signature space, enabling universal comparison.

Mathematical Framework:
- Signature space: ℝ⁵ (5-dimensional real space)
- Distance metric: weighted Euclidean (frequency-dominant)
- Resonance: normalized dot product + phase matching
- Similarity threshold: domain-specific cutoffs
"""

import numpy as np
import json
from pathlib import Path
from datetime import datetime
from typing import List, Tuple, Dict, Optional, Union
from dataclasses import dataclass, asdict
from scipy import signal, fft


@dataclass
class OscillatorySignature:
    """
    Universal oscillatory signature.
    
    The fundamental representation of any oscillatory phenomenon.
    These 5 numbers capture everything needed for perception and cognition.
    """
    frequency: float  # Hz - Primary oscillation frequency
    amplitude: float  # Arbitrary units - Oscillation strength
    phase: float  # Radians [0, 2π] - Temporal offset
    damping: float  # Dimensionless [0, 1] - Decay coefficient (0=highly damped, 1=undamped)
    symmetry: float  # Dimensionless [0, 1] - Structural regularity (0=asymmetric, 1=symmetric)
    
    # Metadata
    domain: Optional[str] = None  # 'molecular', 'acoustic', 'visual', etc.
    source: Optional[str] = None  # Source identifier
    timestamp: Optional[float] = None  # When signature was generated
    
    def to_array(self) -> np.ndarray:
        """Convert to [5] numpy array."""
        return np.array([
            self.frequency,
            self.amplitude,
            self.phase,
            self.damping,
            self.symmetry
        ], dtype=np.float64)
    
    def to_dict(self) -> dict:
        """Convert to JSON-serializable dictionary."""
        d = asdict(self)
        # Convert floats
        for key in ['frequency', 'amplitude', 'phase', 'damping', 'symmetry', 'timestamp']:
            if d[key] is not None:
                d[key] = float(d[key])
        return d
    
    def distance_to(self,
                   other: 'OscillatorySignature',
                   weights: Optional[np.ndarray] = None) -> float:
        """
        Calculate weighted distance to another signature.
        
        Args:
            other: Other oscillatory signature
            weights: [5] weight vector (default: [0.5, 0.2, 0.15, 0.1, 0.05])
        
        Returns:
            Weighted distance
        """
        if weights is None:
            # Default weights: frequency most important
            weights = np.array([0.5, 0.2, 0.15, 0.1, 0.05])
        
        v1 = self.to_array()
        v2 = other.to_array()
        
        # Normalize by typical scales
        scales = np.array([
            v1[0] + 1e-10,  # Frequency scale
            max(v1[1], v2[1]) + 1e-10,  # Amplitude scale
            np.pi,  # Phase scale
            1.0,  # Damping scale
            1.0  # Symmetry scale
        ])
        
        # Weighted Euclidean distance
        diff = (v1 - v2) / scales
        distance = np.sqrt(np.sum(weights * diff**2))
        
        return float(distance)
    
    def resonance_with(self, other: 'OscillatorySignature') -> float:
        """
        Calculate resonance strength with another signature.
        
        Resonance combines:
        - Frequency matching (exponential penalty for mismatch)
        - Amplitude compatibility
        - Phase relationship (cosine)
        - Damping similarity
        - Symmetry similarity
        
        Args:
            other: Other oscillatory signature
        
        Returns:
            Resonance strength [0, 1]
        """
        # Frequency matching (most critical)
        freq_ratio = min(self.frequency, other.frequency) / (max(self.frequency, other.frequency) + 1e-10)
        freq_match = freq_ratio  # Linear for small differences
        
        # Amplitude compatibility (geometric mean)
        amp_match = 2 * self.amplitude * other.amplitude / \
                   (self.amplitude + other.amplitude + 1e-10)
        amp_match = min(amp_match, 1.0)
        
        # Phase relationship (0 = in phase, π = out of phase)
        phase_diff = abs(self.phase - other.phase)
        phase_diff = min(phase_diff, 2*np.pi - phase_diff)  # Wrap to [0, π]
        phase_match = np.cos(phase_diff)  # 1 = in phase, -1 = out of phase
        phase_match = 0.5 * (1.0 + phase_match)  # Map to [0, 1]
        
        # Damping similarity
        damp_match = 1.0 - abs(self.damping - other.damping)
        
        # Symmetry similarity
        symm_match = 1.0 - abs(self.symmetry - other.symmetry)
        
        # Weighted combination
        resonance = (0.5 * freq_match +
                    0.2 * amp_match +
                    0.15 * phase_match +
                    0.10 * damp_match +
                    0.05 * symm_match)
        
        return float(np.clip(resonance, 0.0, 1.0))


class OscillatorySignatureGenerator:
    """
    Generate oscillatory signatures from various input types.
    
    Supports:
    - Time-series data
    - Frequency spectra
    - Explicit feature specification
    - Molecular structures (via integration with molecular modules)
    - Hardware sensor data (via integration with hardware modules)
    """
    
    def __init__(self, domain: str = 'generic'):
        """
        Initialize generator.
        
        Args:
            domain: Domain type ('molecular', 'acoustic', 'thermal', etc.)
        """
        self.domain = domain
    
    def from_timeseries(self,
                       timeseries: np.ndarray,
                       sampling_rate: float,
                       source: Optional[str] = None) -> OscillatorySignature:
        """
        Generate signature from time-series data.
        
        Args:
            timeseries: Time-series data [n_samples]
            sampling_rate: Sampling rate (Hz)
            source: Optional source identifier
        
        Returns:
            OscillatorySignature
        """
        # Compute FFT
        fft_vals = fft.rfft(timeseries)
        fft_freqs = fft.rfftfreq(len(timeseries), d=1.0/sampling_rate)
        
        # Remove DC component
        fft_vals = fft_vals[1:]
        fft_freqs = fft_freqs[1:]
        
        # Power spectrum
        power = np.abs(fft_vals) ** 2
        
        # 1. Frequency: power-weighted mean
        frequency = float(np.sum(fft_freqs * power) / np.sum(power))
        
        # 2. Amplitude: RMS of timeseries
        amplitude = float(np.sqrt(np.mean((timeseries - np.mean(timeseries))**2)))
        
        # 3. Phase: phase of dominant frequency
        dominant_idx = np.argmax(power)
        phase = float(np.angle(fft_vals[dominant_idx]))
        phase = phase % (2 * np.pi)  # Wrap to [0, 2π]
        
        # 4. Damping: from autocorrelation decay
        damping = self._calculate_damping(timeseries, sampling_rate)
        
        # 5. Symmetry: from time-reversal symmetry
        symmetry = self._calculate_symmetry(timeseries)
        
        return OscillatorySignature(
            frequency=frequency,
            amplitude=amplitude,
            phase=phase,
            damping=damping,
            symmetry=symmetry,
            domain=self.domain,
            source=source,
            timestamp=datetime.now().timestamp()
        )
    
    def from_spectrum(self,
                     frequencies: np.ndarray,
                     power: np.ndarray,
                     source: Optional[str] = None) -> OscillatorySignature:
        """
        Generate signature from frequency spectrum.
        
        Args:
            frequencies: Frequency array [n_freqs]
            power: Power at each frequency [n_freqs]
            source: Optional source identifier
        
        Returns:
            OscillatorySignature
        """
        # Normalize power
        power_norm = power / (np.sum(power) + 1e-10)
        
        # 1. Frequency: power-weighted mean
        frequency = float(np.sum(frequencies * power_norm))
        
        # 2. Amplitude: total power
        amplitude = float(np.sqrt(np.sum(power)))
        
        # 3. Phase: not available from power spectrum, use default
        phase = 0.0
        
        # 4. Damping: from spectral bandwidth
        mean_freq = frequency
        bandwidth = np.sqrt(np.sum(((frequencies - mean_freq)**2) * power_norm))
        damping = float(1.0 / (1.0 + bandwidth / (mean_freq + 1e-10)))
        
        # 5. Symmetry: from spectral shape regularity
        # High symmetry = narrow, well-defined peaks
        peaks, properties = signal.find_peaks(power, prominence=0.1*np.max(power))
        if len(peaks) > 0:
            peak_regularity = 1.0 / (1.0 + np.std(power[peaks]) / (np.mean(power[peaks]) + 1e-10))
        else:
            peak_regularity = 0.5
        symmetry = float(np.clip(peak_regularity, 0.0, 1.0))
        
        return OscillatorySignature(
            frequency=frequency,
            amplitude=amplitude,
            phase=phase,
            damping=damping,
            symmetry=symmetry,
            domain=self.domain,
            source=source,
            timestamp=datetime.now().timestamp()
        )
    
    def from_explicit(self,
                     frequency: float,
                     amplitude: float,
                     phase: float,
                     damping: float,
                     symmetry: float,
                     source: Optional[str] = None) -> OscillatorySignature:
        """
        Create signature from explicit parameters.
        
        Args:
            frequency: Frequency (Hz)
            amplitude: Amplitude
            phase: Phase (radians)
            damping: Damping coefficient [0, 1]
            symmetry: Symmetry factor [0, 1]
            source: Optional source identifier
        
        Returns:
            OscillatorySignature
        """
        return OscillatorySignature(
            frequency=frequency,
            amplitude=amplitude,
            phase=phase % (2*np.pi),  # Wrap phase
            damping=np.clip(damping, 0.0, 1.0),
            symmetry=np.clip(symmetry, 0.0, 1.0),
            domain=self.domain,
            source=source,
            timestamp=datetime.now().timestamp()
        )
    
    def _calculate_damping(self, timeseries: np.ndarray, sampling_rate: float) -> float:
        """Calculate damping from autocorrelation decay."""
        # Autocorrelation
        autocorr = signal.correlate(timeseries, timeseries, mode='full')
        autocorr = autocorr[len(autocorr)//2:]  # Positive lags only
        autocorr = autocorr / (autocorr[0] + 1e-10)  # Normalize
        
        # Find decay time (where autocorr drops to 1/e)
        try:
            decay_indices = np.where(autocorr < 1.0/np.e)[0]
            if len(decay_indices) > 0:
                decay_time = decay_indices[0] / sampling_rate
                # Damping = 1 / decay_time (normalized)
                # High damping = fast decay, Low damping = slow decay
                # Map to [0, 1] where 1 = undamped
                damping = np.exp(-decay_time * sampling_rate / len(timeseries))
            else:
                damping = 1.0  # No significant decay
        except:
            damping = 0.5  # Default
        
        return float(np.clip(damping, 0.0, 1.0))
    
    def _calculate_symmetry(self, timeseries: np.ndarray) -> float:
        """Calculate symmetry from time-reversal."""
        # Correlation with time-reversed signal
        reversed_ts = timeseries[::-1]
        correlation = np.corrcoef(timeseries, reversed_ts)[0, 1]
        
        # Map from [-1, 1] to [0, 1]
        symmetry = 0.5 * (1.0 + correlation)
        
        return float(np.clip(symmetry, 0.0, 1.0))


def calculate_signature_similarity_matrix(signatures: List[OscillatorySignature],
                                          metric: str = 'resonance') -> np.ndarray:
    """
    Calculate pairwise similarity matrix for signatures.
    
    Args:
        signatures: List of oscillatory signatures
        metric: 'resonance' or 'distance'
    
    Returns:
        np.ndarray: [n, n] similarity matrix
    """
    n = len(signatures)
    matrix = np.zeros((n, n), dtype=np.float64)
    
    for i in range(n):
        for j in range(i, n):
            if metric == 'resonance':
                sim = signatures[i].resonance_with(signatures[j])
            elif metric == 'distance':
                sim = 1.0 / (1.0 + signatures[i].distance_to(signatures[j]))
            else:
                raise ValueError(f"Unknown metric: {metric}")
            
            matrix[i, j] = sim
            matrix[j, i] = sim
    
    return matrix


def save_signatures(signatures_dict: Dict[str, OscillatorySignature],
                   output_path: str):
    """
    Save signatures to JSON file.
    
    Args:
        signatures_dict: Dict[name] = OscillatorySignature
        output_path: Path to output file
    """
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    data = {
        'timestamp': datetime.now().isoformat(),
        'num_signatures': len(signatures_dict),
        'signatures': {
            name: sig.to_dict()
            for name, sig in signatures_dict.items()
        }
    }
    
    with open(output_path, 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"✓ Saved {len(signatures_dict)} signatures to {output_path}")


def demonstrate_signatures():
    """Demonstrate oscillatory signature functionality."""
    print("="*80)
    print("OSCILLATORY SIGNATURE FRAMEWORK DEMONSTRATION")
    print("="*80 + "\n")
    
    generator = OscillatorySignatureGenerator(domain='molecular')
    
    # Test 1: From explicit parameters
    print("Test 1: Explicit Signatures")
    print("-"*80)
    
    signatures = {
        'Vanillin': generator.from_explicit(
            frequency=1.5e13,
            amplitude=5.0,
            phase=1.2,
            damping=0.7,
            symmetry=0.8,
            source='vanillin'
        ),
        'Ethyl Vanillin': generator.from_explicit(
            frequency=1.52e13,
            amplitude=5.1,
            phase=1.25,
            damping=0.68,
            symmetry=0.82,
            source='ethyl_vanillin'
        ),
        'Indole': generator.from_explicit(
            frequency=2.1e13,
            amplitude=6.2,
            phase=2.3,
            damping=0.4,
            symmetry=0.5,
            source='indole'
        ),
    }
    
    for name, sig in signatures.items():
        print(f"{name}:")
        print(f"  {sig.to_array()}")
    print()
    
    # Test 2: Resonance calculation
    print("Test 2: Resonance Analysis")
    print("-"*80)
    
    van_ethylvan = signatures['Vanillin'].resonance_with(signatures['Ethyl Vanillin'])
    van_indole = signatures['Vanillin'].resonance_with(signatures['Indole'])
    
    print(f"Vanillin ↔ Ethyl Vanillin: {van_ethylvan:.4f}")
    print(f"Vanillin ↔ Indole: {van_indole:.4f}")
    print(f"Ratio (similar/dissimilar): {van_ethylvan/van_indole:.4f}")
    print()
    
    if van_ethylvan > van_indole:
        print("✓ Similar molecules (both vanilla) have higher resonance")
    print()
    
    # Test 3: From time series
    print("Test 3: From Time Series")
    print("-"*80)
    
    # Generate synthetic oscillation
    t = np.linspace(0, 1.0, 10000)  # 1 second
    timeseries = np.sin(2*np.pi*120*t) + 0.3*np.sin(2*np.pi*240*t) + 0.05*np.random.randn(len(t))
    
    sig_ts = generator.from_timeseries(timeseries, sampling_rate=10000, source='synthetic')
    
    print(f"Generated from time series:")
    print(f"  Frequency: {sig_ts.frequency:.2f} Hz")
    print(f"  Amplitude: {sig_ts.amplitude:.3f}")
    print(f"  Phase: {sig_ts.phase:.3f} rad")
    print(f"  Damping: {sig_ts.damping:.3f}")
    print(f"  Symmetry: {sig_ts.symmetry:.3f}")
    print()
    
    # Test 4: Similarity matrix
    print("Test 4: Similarity Matrix")
    print("-"*80)
    
    sig_list = list(signatures.values())
    sim_matrix = calculate_signature_similarity_matrix(sig_list, metric='resonance')
    
    print("Resonance matrix:")
    names = list(signatures.keys())
    print(f"{'':15}", end='')
    for name in names:
        print(f"{name:15}", end='')
    print()
    
    for i, name1 in enumerate(names):
        print(f"{name1:15}", end='')
        for j in range(len(names)):
            print(f"{sim_matrix[i,j]:15.4f}", end='')
        print()
    print()
    
    # Save
    print("Saving Results:")
    print("-"*80)
    
    output_dir = Path("results/signatures")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    save_signatures(signatures, output_dir / "oscillatory_signatures.json")
    
    # Save similarity matrix
    np.save(output_dir / "similarity_matrix.npy", sim_matrix)
    
    with open(output_dir / "similarity_matrix.json", 'w') as f:
        json.dump({
            'timestamp': datetime.now().isoformat(),
            'molecules': names,
            'matrix': sim_matrix.tolist(),
            'metric': 'resonance'
        }, f, indent=2)
    
    print(f"✓ Saved similarity matrix")
    
    print("\n✓ Demonstration complete!")


if __name__ == "__main__":
    demonstrate_signatures()

