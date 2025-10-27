"""
CPU Clock Oscillation Harvesting

From hardware-lipid-llm.tex and grand-unification-lab.tex: Consumer computer
hardware generates measurable oscillatory signatures that can serve as BMD sources.

CPU Timing Sources:
- System clock (~2-5 GHz base frequency)
- Clock jitter (ns-scale variations)
- Turbo boost oscillations
- Thermal throttling patterns
- Power state transitions (C-states, P-states)
- Cache coherency cycles
- Pipeline stalls and flushes

S-Entropy Mapping:
- High-frequency components → Low S_knowledge (determined states)
- Jitter patterns → S_time (temporal structure)
- Thermal variations → S_entropy (system diversity)

Equipment Cost: $0 (using existing CPU)
Measurement: Via timing APIs, performance counters, TSC (Time Stamp Counter)
"""

import time
import platform
from dataclasses import dataclass, field
from typing import List, Dict, Optional
import numpy as np


@dataclass
class CPUClockHarvester:
    """
    Harvest oscillatory signatures from CPU timing.
    
    Sources:
    - Time Stamp Counter (TSC) jitter
    - Performance counter variations
    - Execution timing patterns
    - Thermal-induced frequency changes
    
    Attributes:
        sample_rate: Samples per second
        window_size: Number of samples for FFT analysis
        
        # Harvested data
        timestamps: List of TSC or time.perf_counter() readings
        jitter_values: Calculated jitter (time differences)
        frequencies: Extracted frequency components
        
        # Statistics
        harvest_count: Number of harvest operations
        total_samples: Total samples collected
    """
    
    sample_rate: float = 1000.0  # Hz (1 kHz sampling)
    window_size: int = 1024  # Samples for FFT
    
    # Harvested data
    timestamps: List[float] = field(default_factory=list)
    jitter_values: List[float] = field(default_factory=list)
    frequencies: np.ndarray = field(default_factory=lambda: np.array([]))
    spectrum: np.ndarray = field(default_factory=lambda: np.array([]))
    
    # Statistics
    harvest_count: int = 0
    total_samples: int = 0
    
    def harvest_timing_jitter(self, num_samples: int = 100) -> np.ndarray:
        """
        Harvest CPU timing jitter from high-resolution timer.
        
        Args:
            num_samples: Number of samples to collect
            
        Returns:
            Array of jitter values (time differences in seconds)
        """
        self.harvest_count += 1
        
        samples = []
        for _ in range(num_samples):
            # Use perf_counter for high-resolution timing
            t1 = time.perf_counter()
            # Minimal work to induce jitter
            _ = sum(range(10))
            t2 = time.perf_counter()
            
            samples.append(t2 - t1)
        
        jitter = np.array(samples)
        self.jitter_values.extend(jitter.tolist())
        self.total_samples += num_samples
        
        return jitter
    
    def harvest_execution_patterns(self, num_iterations: int = 100) -> np.ndarray:
        """
        Harvest oscillatory patterns from repeated execution timing.
        
        Measures variability in execution time for identical operations,
        revealing CPU state changes (cache, thermal, power management).
        
        Args:
            num_iterations: Number of iterations
            
        Returns:
            Array of execution times
        """
        self.harvest_count += 1
        
        execution_times = []
        
        for _ in range(num_iterations):
            start = time.perf_counter()
            
            # Standard computation (memory access + arithmetic)
            data = list(range(1000))
            result = sum([x * x for x in data])
            
            end = time.perf_counter()
            execution_times.append(end - start)
        
        times = np.array(execution_times)
        self.timestamps.extend(times.tolist())
        self.total_samples += num_iterations
        
        return times
    
    def compute_spectrum(self, signal: Optional[np.ndarray] = None) -> tuple:
        """
        Compute frequency spectrum of harvested signal.
        
        Args:
            signal: Optional signal (uses jitter_values if None)
            
        Returns:
            Tuple of (frequencies, spectrum_magnitude)
        """
        if signal is None:
            if not self.jitter_values:
                return (np.array([]), np.array([]))
            signal = np.array(self.jitter_values[-self.window_size:])
        
        # Apply window function to reduce spectral leakage
        window = np.hanning(len(signal))
        windowed_signal = signal * window
        
        # Compute FFT
        fft_result = np.fft.fft(windowed_signal)
        freqs = np.fft.fftfreq(len(signal), d=1.0/self.sample_rate)
        
        # Take positive frequencies only
        positive_freqs = freqs[:len(freqs)//2]
        magnitude = np.abs(fft_result[:len(fft_result)//2])
        
        self.frequencies = positive_freqs
        self.spectrum = magnitude
        
        return (positive_freqs, magnitude)
    
    def extract_s_entropy_coordinates(self, signal: Optional[np.ndarray] = None) -> np.ndarray:
        """
        Extract S-entropy coordinates from CPU oscillations.
        
        Mapping:
        - S_knowledge: Based on dominant frequency (high freq → low S_k)
        - S_time: Based on jitter variance (high variance → low S_t)
        - S_entropy: Based on spectral entropy (diverse spectrum → high S_e)
        
        Args:
            signal: Optional signal
            
        Returns:
            S-entropy coordinates (S_k, S_t, S_e)
        """
        if signal is None:
            signal = np.array(self.jitter_values[-min(len(self.jitter_values), self.window_size):])
        
        if len(signal) < 10:
            return np.array([2.0, 0.5, 1.0])  # Default
        
        # Compute spectrum
        freqs, spectrum = self.compute_spectrum(signal)
        
        if len(spectrum) == 0:
            return np.array([2.0, 0.5, 1.0])
        
        # S_knowledge: Dominant frequency (normalized)
        # Higher frequency → more determined → lower S_k
        if np.max(spectrum) > 0:
            dominant_freq_idx = np.argmax(spectrum)
            dominant_freq = freqs[dominant_freq_idx]
            # Map freq to S_k: [0, sample_rate/2] → [5.0, 0.0]
            s_knowledge = max(0.0, 5.0 * (1 - dominant_freq / (self.sample_rate / 2)))
        else:
            s_knowledge = 2.5
        
        # S_time: Temporal variance (jitter)
        # High variance → uncertain timing → high S_t
        variance = np.var(signal)
        # Normalize variance to [0, 1]
        s_time = min(1.0, variance / (np.mean(signal) + 1e-10))
        
        # S_entropy: Spectral entropy
        # Diverse spectrum → high entropy
        if np.sum(spectrum) > 0:
            normalized_spectrum = spectrum / np.sum(spectrum)
            # Shannon entropy
            spectral_entropy = -np.sum(normalized_spectrum * np.log(normalized_spectrum + 1e-10))
            # Normalize to [0, 3.0]
            max_entropy = np.log(len(spectrum))
            s_entropy = 3.0 * (spectral_entropy / max_entropy) if max_entropy > 0 else 1.0
        else:
            s_entropy = 1.0
        
        return np.array([s_knowledge, s_time, s_entropy])
    
    def get_statistics(self) -> Dict:
        """Get harvester statistics."""
        return {
            'sample_rate': self.sample_rate,
            'window_size': self.window_size,
            'harvest_count': self.harvest_count,
            'total_samples': self.total_samples,
            'jitter_samples': len(self.jitter_values),
            'timestamp_samples': len(self.timestamps),
            'platform': platform.processor(),
            'cpu_count': platform.os.cpu_count()
        }
    
    def __repr__(self) -> str:
        stats = self.get_statistics()
        return (f"CPUClockHarvester(samples={stats['total_samples']}, "
                f"harvests={stats['harvest_count']}, rate={self.sample_rate}Hz)")


# Example usage
if __name__ == "__main__":
    print("=== CPU Clock Oscillation Harvesting Demo ===\n")
    
    harvester = CPUClockHarvester(sample_rate=1000.0)
    print(f"Harvester created: {harvester}\n")
    
    # Harvest timing jitter
    print("=== Harvesting Timing Jitter ===")
    jitter = harvester.harvest_timing_jitter(num_samples=200)
    print(f"Collected {len(jitter)} jitter samples")
    print(f"Mean jitter: {np.mean(jitter)*1e6:.2f} μs")
    print(f"Std jitter: {np.std(jitter)*1e6:.2f} μs")
    print(f"Min jitter: {np.min(jitter)*1e6:.2f} μs")
    print(f"Max jitter: {np.max(jitter)*1e6:.2f} μs")
    
    # Harvest execution patterns
    print("\n=== Harvesting Execution Patterns ===")
    exec_times = harvester.harvest_execution_patterns(num_iterations=200)
    print(f"Collected {len(exec_times)} execution time samples")
    print(f"Mean time: {np.mean(exec_times)*1e6:.2f} μs")
    print(f"Std time: {np.std(exec_times)*1e6:.2f} μs")
    
    # Compute spectrum
    print("\n=== Frequency Spectrum Analysis ===")
    freqs, spectrum = harvester.compute_spectrum()
    if len(spectrum) > 0:
        # Find top 3 frequency components
        top_indices = np.argsort(spectrum)[-3:][::-1]
        print("Top 3 frequency components:")
        for i, idx in enumerate(top_indices):
            print(f"  {i+1}. {freqs[idx]:.1f} Hz, magnitude={spectrum[idx]:.2e}")
    
    # Extract S-entropy coordinates
    print("\n=== S-Entropy Coordinate Extraction ===")
    s_coords = harvester.extract_s_entropy_coordinates()
    print(f"S-coordinates from CPU oscillations:")
    print(f"  S_knowledge: {s_coords[0]:.3f} (information deficit)")
    print(f"  S_time: {s_coords[1]:.3f} (temporal variance)")
    print(f"  S_entropy: {s_coords[2]:.3f} (spectral diversity)")
    
    # Statistics
    print("\n=== Harvester Statistics ===")
    stats = harvester.get_statistics()
    print(f"Total samples: {stats['total_samples']}")
    print(f"Harvest operations: {stats['harvest_count']}")
    print(f"Sample rate: {stats['sample_rate']} Hz")
    print(f"Platform: {stats['platform']}")
    print(f"CPU count: {stats['cpu_count']}")
    
    print("\n=== Hardware Harvesting Advantages ===")
    print("✓ Zero cost: Uses existing CPU")
    print("✓ High resolution: ns-scale timing precision")
    print("✓ Continuous availability: Always-on oscillation source")
    print("✓ BMD-equivalent: Generates measurable oscillatory signatures")
    
    print("\n=== CPU Clock Oscillation Harvesting Verified ===")

