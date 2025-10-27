"""
Hardware Oscillatory Signature Generation

Converts hardware oscillation measurements into oscillatory signatures.

Integrates with existing hardware infrastructure to harvest oscillations
from CPU, thermal, EM, audio, and other sources.
"""

import numpy as np
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from scipy import signal, fft
from dataclasses import dataclass, asdict


@dataclass
class HardwareOscillatorySignature:
    """Oscillatory signature from hardware measurements."""
    frequency: float  # Dominant frequency (Hz)
    amplitude: float  # Oscillation amplitude
    phase: float  # Phase (radians)
    damping: float  # Damping coefficient
    symmetry: float  # Symmetry factor
    
    # Metadata
    source: str  # 'cpu', 'thermal', 'em', 'audio', etc.
    sampling_rate: float  # Hz
    duration: float  # seconds
    
    def to_array(self) -> np.ndarray:
        """Convert to [5] numpy array [freq, amp, phase, damp, symm]."""
        return np.array([
            self.frequency,
            self.amplitude,
            self.phase,
            self.damping,
            self.symmetry
        ])
    
    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        return {
            'frequency': float(self.frequency),
            'amplitude': float(self.amplitude),
            'phase': float(self.phase),
            'damping': float(self.damping),
            'symmetry': float(self.symmetry),
            'source': self.source,
            'sampling_rate': float(self.sampling_rate),
            'duration': float(self.duration)
        }


class HardwareSignatureGenerator:
    """
    Generates oscillatory signatures from hardware measurements.
    
    Supports multiple hardware sources:
    - CPU frequency oscillations
    - Thermal oscillations
    - Electromagnetic field oscillations
    - Audio oscillations
    - Timing jitter
    
    Integrates with existing hardware modules.
    """
    
    def __init__(self):
        """Initialize hardware signature generator."""
        pass
    
    def generate_from_timeseries(self,
                                 timeseries: np.ndarray,
                                 sampling_rate: float,
                                 source: str = 'unknown') -> HardwareOscillatorySignature:
        """
        Generate oscillatory signature from time-series data.
        
        Args:
            timeseries: Time-series measurements [n_samples]
            sampling_rate: Sampling rate in Hz
            source: Source identifier
            
        Returns:
            HardwareOscillatorySignature object
        """
        # Extract signature components
        frequency = self._extract_dominant_frequency(timeseries, sampling_rate)
        amplitude = self._extract_amplitude(timeseries)
        phase = self._extract_phase(timeseries, sampling_rate)
        damping = self._extract_damping(timeseries, sampling_rate)
        symmetry = self._extract_symmetry(timeseries)
        
        return HardwareOscillatorySignature(
            frequency=frequency,
            amplitude=amplitude,
            phase=phase,
            damping=damping,
            symmetry=symmetry,
            source=source,
            sampling_rate=sampling_rate,
            duration=len(timeseries) / sampling_rate
        )
    
    def _extract_dominant_frequency(self, 
                                   timeseries: np.ndarray, 
                                   sampling_rate: float) -> float:
        """Extract dominant frequency using FFT."""
        # Compute FFT
        n = len(timeseries)
        fft_vals = fft.rfft(timeseries)
        fft_freqs = fft.rfftfreq(n, d=1.0/sampling_rate)
        
        # Find peak
        power = np.abs(fft_vals) ** 2
        peak_idx = np.argmax(power[1:]) + 1  # Skip DC component
        
        dominant_freq = float(fft_freqs[peak_idx])
        
        return dominant_freq
    
    def _extract_amplitude(self, timeseries: np.ndarray) -> float:
        """Extract oscillation amplitude (RMS)."""
        # Remove mean
        centered = timeseries - np.mean(timeseries)
        
        # RMS amplitude
        rms = np.sqrt(np.mean(centered ** 2))
        
        return float(rms)
    
    def _extract_phase(self, 
                      timeseries: np.ndarray, 
                      sampling_rate: float) -> float:
        """Extract phase at dominant frequency."""
        # FFT
        fft_vals = fft.rfft(timeseries)
        fft_freqs = fft.rfftfreq(len(timeseries), d=1.0/sampling_rate)
        
        # Find dominant frequency
        power = np.abs(fft_vals) ** 2
        peak_idx = np.argmax(power[1:]) + 1
        
        # Phase at dominant frequency
        phase = float(np.angle(fft_vals[peak_idx]))
        
        return phase
    
    def _extract_damping(self, 
                        timeseries: np.ndarray, 
                        sampling_rate: float) -> float:
        """
        Extract damping coefficient from autocorrelation decay.
        
        Assumes exponential decay: A(t) = A₀ * exp(-γt)
        """
        # Autocorrelation
        autocorr = signal.correlate(timeseries, timeseries, mode='full')
        autocorr = autocorr[len(autocorr)//2:]  # Keep positive lags
        autocorr = autocorr / autocorr[0]  # Normalize
        
        # Fit exponential decay
        # Find where autocorr drops to 1/e
        try:
            decay_idx = np.where(autocorr < 1.0/np.e)[0]
            if len(decay_idx) > 0:
                decay_time = decay_idx[0] / sampling_rate
                damping = 1.0 / decay_time if decay_time > 0 else 0.0
            else:
                damping = 0.0
        except:
            damping = 0.0
        
        return float(np.clip(damping, 0.0, 1.0))
    
    def _extract_symmetry(self, timeseries: np.ndarray) -> float:
        """
        Extract symmetry from time-series.
        
        Measures correlation between signal and its time-reversed version.
        """
        # Correlation with time-reversed signal
        reversed_ts = timeseries[::-1]
        
        # Pearson correlation
        correlation = np.corrcoef(timeseries, reversed_ts)[0, 1]
        
        # Map from [-1, 1] to [0, 1]
        symmetry = (correlation + 1.0) / 2.0
        
        return float(symmetry)
    
    def generate_from_hardware_data(self,
                                   hardware_data: Dict[str, np.ndarray],
                                   sampling_rates: Dict[str, float]) -> Dict[str, HardwareOscillatorySignature]:
        """
        Generate signatures from multiple hardware sources.
        
        Args:
            hardware_data: Dict[source_name] = timeseries
            sampling_rates: Dict[source_name] = sampling_rate_hz
            
        Returns:
            Dict[source_name] = HardwareOscillatorySignature
        """
        signatures = {}
        
        for source, timeseries in hardware_data.items():
            if source in sampling_rates:
                sr = sampling_rates[source]
                sig = self.generate_from_timeseries(timeseries, sr, source)
                signatures[source] = sig
        
        return signatures
    
    def combine_hardware_signatures(self,
                                   signatures: Dict[str, HardwareOscillatorySignature],
                                   weights: Optional[Dict[str, float]] = None) -> np.ndarray:
        """
        Combine multiple hardware signatures into unified signature.
        
        Args:
            signatures: Dict of HardwareOscillatorySignature objects
            weights: Optional weights for each source
            
        Returns:
            Combined [5] signature array
        """
        if weights is None:
            # Equal weights
            weights = {source: 1.0 for source in signatures.keys()}
        
        # Normalize weights
        total_weight = sum(weights.values())
        weights = {k: v/total_weight for k, v in weights.items()}
        
        # Combine signatures
        combined = np.zeros(5)
        
        for source, sig in signatures.items():
            w = weights.get(source, 0.0)
            combined += w * sig.to_array()
        
        return combined
    
    def map_to_molecular_scale(self,
                               signature: np.ndarray,
                               target_frequency: float = 1e13) -> np.ndarray:
        """
        Map hardware signature to molecular frequency scale.
        
        Hardware oscillations (Hz-GHz) → Molecular oscillations (THz)
        
        Uses gear reduction principle from hardware_mapping.py
        
        Args:
            signature: [5] hardware signature
            target_frequency: Target molecular frequency (Hz)
            
        Returns:
            [5] molecular-scale signature
        """
        freq, amp, phase, damp, symm = signature
        
        # Frequency scaling (gear reduction)
        # Map hardware frequency to molecular frequency
        freq_ratio = target_frequency / freq if freq > 0 else 1.0
        
        # Scale frequency
        new_freq = freq * freq_ratio
        
        # Amplitude scales with frequency (energy conservation)
        new_amp = amp / np.sqrt(freq_ratio)
        
        # Phase remains constant (phase-locked)
        new_phase = phase
        
        # Damping inverse scales (higher frequency = less damping)
        new_damp = damp / freq_ratio if freq_ratio > 0 else damp
        
        # Symmetry preserved
        new_symm = symm
        
        return np.array([new_freq, new_amp, new_phase, new_damp, new_symm])
    
    def save_signatures(self,
                       signatures: Dict[str, HardwareOscillatorySignature],
                       output_path: str,
                       metadata: Optional[Dict] = None) -> None:
        """
        Save hardware signatures to JSON file.
        
        Args:
            signatures: Dict[source_name] = HardwareOscillatorySignature
            output_path: Path to output JSON file
            metadata: Optional metadata to include
        """
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Convert signatures to dict
        signatures_dict = {
            source: sig.to_dict() 
            for source, sig in signatures.items()
        }
        
        # Build output data
        output_data = {
            'timestamp': datetime.now().isoformat(),
            'num_sources': len(signatures),
            'signatures': signatures_dict
        }
        
        if metadata:
            output_data['metadata'] = metadata
        
        # Save to JSON
        with open(output_path, 'w') as f:
            json.dump(output_data, f, indent=2)
        
        print(f"✓ Saved hardware signatures to {output_path}")
    
    def save_combined_signature(self,
                               combined_signature: np.ndarray,
                               output_path: str,
                               sources: Optional[List[str]] = None,
                               metadata: Optional[Dict] = None) -> None:
        """
        Save combined hardware signature to JSON file.
        
        Args:
            combined_signature: [5] signature array
            output_path: Path to output JSON file
            sources: Optional list of source names
            metadata: Optional metadata
        """
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        output_data = {
            'timestamp': datetime.now().isoformat(),
            'signature': {
                'frequency': float(combined_signature[0]),
                'amplitude': float(combined_signature[1]),
                'phase': float(combined_signature[2]),
                'damping': float(combined_signature[3]),
                'symmetry': float(combined_signature[4])
            }
        }
        
        if sources:
            output_data['sources'] = sources
        if metadata:
            output_data['metadata'] = metadata
        
        with open(output_path, 'w') as f:
            json.dump(output_data, f, indent=2)
        
        print(f"✓ Saved combined signature to {output_path}")


def demonstrate_hardware_signatures():
    """Demonstrate hardware signature generation."""
    print("="*80)
    print("HARDWARE OSCILLATORY SIGNATURE GENERATION")
    print("="*80 + "\n")
    
    generator = HardwareSignatureGenerator()
    
    # Simulate different hardware sources
    print("Generating signatures from simulated hardware...\n")
    
    # 1. CPU oscillations (GHz range)
    print("1. CPU Frequency Oscillations")
    cpu_fs = 1000  # Sample at 1 kHz
    cpu_duration = 1.0
    t_cpu = np.linspace(0, cpu_duration, int(cpu_fs * cpu_duration))
    cpu_signal = 3.5e9 + 0.1e9 * np.sin(2*np.pi*10*t_cpu) + np.random.normal(0, 1e7, len(t_cpu))
    
    cpu_sig = generator.generate_from_timeseries(cpu_signal, cpu_fs, 'cpu')
    print(f"  Dominant frequency: {cpu_sig.frequency:.2f} Hz")
    print(f"  Amplitude: {cpu_sig.amplitude:.2e}")
    print(f"  Phase: {cpu_sig.phase:.3f} rad")
    print(f"  Damping: {cpu_sig.damping:.3f}")
    print(f"  Symmetry: {cpu_sig.symmetry:.3f}")
    print()
    
    # 2. Thermal oscillations (mHz-Hz range)
    print("2. Thermal Oscillations")
    thermal_fs = 10
    thermal_duration = 10.0
    t_thermal = np.linspace(0, thermal_duration, int(thermal_fs * thermal_duration))
    thermal_signal = 62.5 + 5*np.sin(2*np.pi*0.1*t_thermal) + np.random.normal(0, 0.5, len(t_thermal))
    
    thermal_sig = generator.generate_from_timeseries(thermal_signal, thermal_fs, 'thermal')
    print(f"  Dominant frequency: {thermal_sig.frequency:.3f} Hz")
    print(f"  Amplitude: {thermal_sig.amplitude:.3f}")
    print(f"  Phase: {thermal_sig.phase:.3f} rad")
    print(f"  Damping: {thermal_sig.damping:.3f}")
    print(f"  Symmetry: {thermal_sig.symmetry:.3f}")
    print()
    
    # 3. EM oscillations (Hz-kHz range)
    print("3. Electromagnetic Field Oscillations")
    em_fs = 1000
    em_duration = 1.0
    t_em = np.linspace(0, em_duration, int(em_fs * em_duration))
    em_signal = 2*np.sin(2*np.pi*120*t_em) + 0.5*np.sin(2*np.pi*180*t_em) + np.random.normal(0, 0.1, len(t_em))
    
    em_sig = generator.generate_from_timeseries(em_signal, em_fs, 'em')
    print(f"  Dominant frequency: {em_sig.frequency:.2f} Hz")
    print(f"  Amplitude: {em_sig.amplitude:.3f}")
    print(f"  Phase: {em_sig.phase:.3f} rad")
    print(f"  Damping: {em_sig.damping:.3f}")
    print(f"  Symmetry: {em_sig.symmetry:.3f}")
    print()
    
    # Combine signatures
    print("Combined Hardware Signature:")
    print("-" * 80)
    signatures = {'cpu': cpu_sig, 'thermal': thermal_sig, 'em': em_sig}
    weights = {'cpu': 0.5, 'thermal': 0.3, 'em': 0.2}
    
    combined = generator.combine_hardware_signatures(signatures, weights)
    print(f"  Frequency: {combined[0]:.2f} Hz")
    print(f"  Amplitude: {combined[1]:.2e}")
    print(f"  Phase: {combined[2]:.3f} rad")
    print(f"  Damping: {combined[3]:.3f}")
    print(f"  Symmetry: {combined[4]:.3f}")
    print()
    
    # Map to molecular scale
    print("Mapped to Molecular Scale (10¹³ Hz):")
    print("-" * 80)
    molecular_sig = generator.map_to_molecular_scale(combined, target_frequency=1e13)
    print(f"  Frequency: {molecular_sig[0]:.2e} Hz")
    print(f"  Amplitude: {molecular_sig[1]:.2e}")
    print(f"  Phase: {molecular_sig[2]:.3f} rad")
    print(f"  Damping: {molecular_sig[3]:.6f}")
    print(f"  Symmetry: {molecular_sig[4]:.3f}")
    print()
    
    # Save results
    print("Saving results...")
    print("-" * 80)
    
    # Create output directory
    output_dir = Path("results/hardware_signatures")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Save individual signatures
    generator.save_signatures(
        signatures,
        output_dir / "hardware_signatures.json",
        metadata={'description': 'Individual hardware source signatures'}
    )
    
    # Save combined signature
    generator.save_combined_signature(
        combined,
        output_dir / "combined_signature.json",
        sources=list(signatures.keys()),
        metadata={'description': 'Weighted combination of hardware signatures', 'weights': weights}
    )
    
    # Save molecular-scale signature
    generator.save_combined_signature(
        molecular_sig,
        output_dir / "molecular_scale_signature.json",
        sources=list(signatures.keys()),
        metadata={
            'description': 'Hardware signature mapped to molecular scale',
            'target_frequency_hz': 1e13,
            'scaling_method': 'gear_reduction'
        }
    )
    
    print("✓ Hardware signature generation complete!")


if __name__ == "__main__":
    demonstrate_hardware_signatures()

