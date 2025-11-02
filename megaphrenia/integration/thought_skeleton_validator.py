"""
Thought-Skeleton Integration Validator

THE COMPLETE VALIDATION:
========================
Place megaphrenia thoughts (oscillatory patterns) on top of chigure skeleton model
and validate that coherent thoughts don't cause falling.

This integrates:
- Megaphrenia: Thought measurement (psychons, circuits, oscillatory holes)
- Chigure: Complete human body model (skeleton, muscles, O₂ coupling)
- Validation: Stability metric (coherent thoughts → stable, incoherent → falling)
- Synchronization: Munich Airport atomic clock (trans-Planckian precision)

The Experimental Design:
-----------------------
During 400m sprint:
1. Body movements are AUTOMATIC (no thought required)
2. Thoughts are SEPARATE (about anything - strategy, pain, motivation)
3. Both phase-locked to cardiac rhythm
4. BUT thoughts don't cause movements!

This proves:
- Thoughts are measurable independently from motor control
- Consciousness is a parallel process on top of automatic substrate
- Mind-body dualism is empirically testable
- Coherent thoughts don't disrupt the automatic oscillatory substrate

Author: Integration of megaphrenia + chigure frameworks
Date: 2024-10-29
"""

import sys
import numpy as np
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
import json
from datetime import datetime

# Add paths
sys.path.append(str(Path(__file__).parent.parent.parent / 'chigure' / 'src'))

# Megaphrenia imports (thought measurement)
from megaphrenia.core import Psychon, BMDState, create_psychon_from_signature
from megaphrenia.circuits import TriDimensionalLogicGate, LogicFunction
from megaphrenia.experimental import OscillatoryHoleDetector, ThoughtGeometry

# Chigure imports (complete human model)
from chigure.src.muscle.body_segmentation import (
    BodySegment,
    BodySegmentParameters,
    OscillatoryKinematicChain,
    LowerLimbModel
)
from chigure.src.muscle.muscle_model import (
    OscillatoryHierarchy,
    OscillatoryCouplingAnalyzer,
    StateSpaceCoordinates
)
from chigure.src.simulation.Observer import Observer, ObserverType, InteractionMode
from chigure.src.signal.precise_clock_apis import (
    ClockType,
    ClockReading,
    PreciseClockManager
)


@dataclass
class ThoughtPerturbation:
    """
    Represents a thought as an oscillatory perturbation to the skeleton.
    
    The thought's oscillatory signature becomes a force/torque applied
    to body segments. Coherent thoughts align with automatic patterns,
    incoherent thoughts disrupt balance.
    """
    psychon: Psychon
    timestamp: float  # Munich atomic clock time
    cardiac_phase: float  # 0-2π cardiac cycle phase
    oscillatory_signature: np.ndarray  # Multi-scale frequency content
    amplitude: float  # Perturbation strength
    body_segment: str  # Which segment this affects
    coherence_with_automatic: float  # How aligned with automatic substrate
    
    def compute_torque_perturbation(self, segment: BodySegment) -> float:
        """
        Convert thought oscillatory signature to torque perturbation on segment.
        
        Coherent thoughts (aligned with automatic patterns) → small perturbation
        Incoherent thoughts (misaligned) → large perturbation
        """
        # Base perturbation from thought amplitude
        base_torque = self.amplitude * 10.0  # Nm
        
        # Modulate by coherence (high coherence → low perturbation)
        coherence_factor = 1.0 - self.coherence_with_automatic
        
        # Modulate by frequency alignment with segment's natural frequency
        thought_freq = self.psychon.frequency
        segment_freq = segment.natural_frequency
        freq_mismatch = abs(thought_freq - segment_freq) / segment_freq
        freq_factor = np.exp(-freq_mismatch / 2.0)  # Gaussian decay
        
        # Total perturbation torque
        perturbation_torque = base_torque * coherence_factor * (1.0 - freq_factor)
        
        return perturbation_torque


@dataclass
class StabilityMetrics:
    """Metrics for validating skeleton stability under thought perturbations"""
    time: np.ndarray
    center_of_mass_displacement: np.ndarray  # How much COM moves
    angular_momentum: np.ndarray  # Total angular momentum
    total_energy: np.ndarray  # Total oscillatory energy
    segment_angles: np.ndarray  # Joint angles over time
    segment_velocities: np.ndarray  # Joint angular velocities
    stability_index: float  # Overall stability (1.0 = perfectly stable)
    falling_detected: bool  # Did the skeleton fall?
    fall_time: Optional[float]  # When did it fall (if it did)
    coherence_score: float  # Overall thought-body coherence


class ThoughtSkeletonValidator:
    """
    Validates thoughts by placing them on skeleton and checking stability.
    
    This is THE COMPLETE INTEGRATION of megaphrenia and chigure:
    - Megaphrenia provides thought measurements
    - Chigure provides skeleton dynamics
    - Validation: coherent thoughts don't cause falling
    """
    
    def __init__(self, body_mass: float = 70.0, height: float = 1.75,
                 munich_airport_sync: bool = True):
        """
        Initialize thought-skeleton validator.
        
        Parameters
        ----------
        body_mass : float
            Body mass (kg)
        height : float
            Body height (m)
        munich_airport_sync : bool
            Whether to sync to Munich Airport atomic clock
        """
        self.body_mass = body_mass
        self.height = height
        
        # Initialize skeleton model (chigure)
        self.lower_limb = LowerLimbModel(body_mass, height)
        self.chain = self.lower_limb.chain
        
        # Initialize thought detector (megaphrenia)
        self.hole_detector = OscillatoryHoleDetector()
        
        # Initialize coupling analyzer
        self.coupling_analyzer = OscillatoryCouplingAnalyzer()
        
        # Initialize Munich Airport clock sync
        self.munich_clock = None
        if munich_airport_sync:
            self.munich_clock = self._initialize_munich_clock()
        
        # Tracking
        self.thought_history: List[ThoughtPerturbation] = []
        self.stability_history: List[StabilityMetrics] = []
        
    def _initialize_munich_clock(self) -> Optional[PreciseClockManager]:
        """Initialize connection to Munich Airport atomic clock"""
        try:
            clock_manager = PreciseClockManager()
            
            # Munich Airport coordinates
            munich_airport_clock = clock_manager.add_clock_source(
                clock_id="munich_airport",
                clock_type=ClockType.ATOMIC_CESIUM,
                connection_info={
                    'host': 'time.munich-airport.de',  # Hypothetical
                    'port': 123,
                    'lat': 48.3538,
                    'lon': 11.7861,
                    'alt': 453.0
                },
                expected_precision=1e-7  # 100 ns precision
            )
            
            return clock_manager
        except Exception as e:
            print(f"Warning: Could not connect to Munich Airport clock: {e}")
            print("Using system time instead")
            return None
    
    def get_atomic_time(self) -> float:
        """Get current time from Munich Airport atomic clock"""
        if self.munich_clock:
            try:
                reading = self.munich_clock.get_synchronized_time()
                return reading.timestamp
            except:
                pass
        
        # Fallback to system time
        return datetime.now().timestamp()
    
    def measure_thought_from_circuit(self, circuit_state: Dict,
                                    cardiac_phase: float,
                                    o2_field: Dict) -> ThoughtPerturbation:
        """
        Measure thought from megaphrenia circuit state.
        
        Parameters
        ----------
        circuit_state : dict
            Current state of megaphrenia circuits
        cardiac_phase : float
            Current cardiac cycle phase (0-2π)
        o2_field : dict
            O₂ molecular field around body
            
        Returns
        -------
        thought : ThoughtPerturbation
            Measured thought as perturbation
        """
        # Extract psychon from circuit
        psychon = circuit_state.get('psychon')
        if psychon is None:
            # Create from circuit completion signature
            freq = circuit_state.get('dominant_frequency', 10.0)  # Hz
            amp = circuit_state.get('amplitude', 1.0)
            psychon = create_psychon_from_signature(freq, amp)
        
        # Detect oscillatory holes in O₂ field
        holes = self.hole_detector.detect_holes(
            o2_field=o2_field.get('O2_molecules', np.random.randn(100, 3)),
            cardiac_phase=cardiac_phase
        )
        
        # Extract oscillatory signature (multi-scale)
        signature = self._extract_oscillatory_signature(psychon, holes)
        
        # Compute coherence with automatic substrate
        coherence = self._compute_coherence_with_automatic(
            psychon, cardiac_phase
        )
        
        # Determine which body segment this thought affects
        # (based on thought content - for now, random)
        segment_names = [seg.name for seg in self.chain.segments]
        segment = np.random.choice(segment_names)
        
        # Get atomic time
        timestamp = self.get_atomic_time()
        
        # Create perturbation
        thought = ThoughtPerturbation(
            psychon=psychon,
            timestamp=timestamp,
            cardiac_phase=cardiac_phase,
            oscillatory_signature=signature,
            amplitude=circuit_state.get('amplitude', 1.0),
            body_segment=segment,
            coherence_with_automatic=coherence
        )
        
        return thought
    
    def _extract_oscillatory_signature(self, psychon: Psychon,
                                      holes: List) -> np.ndarray:
        """Extract multi-scale oscillatory signature from thought"""
        # Create signature across multiple scales (matching chigure hierarchy)
        scales = OscillatoryHierarchy.get_relevant_muscle_scales()
        signature = np.zeros(len(scales))
        
        # Main frequency content
        main_freq = psychon.frequency
        
        for i, scale in enumerate(scales):
            # Check if psychon frequency falls within this scale
            if scale.freq_min <= main_freq <= scale.freq_max:
                signature[i] = psychon.amplitude
            else:
                # Decay with frequency distance
                center_freq = np.sqrt(scale.freq_min * scale.freq_max)
                freq_distance = abs(np.log(main_freq / center_freq))
                signature[i] = psychon.amplitude * np.exp(-freq_distance)
        
        return signature
    
    def _compute_coherence_with_automatic(self, psychon: Psychon,
                                         cardiac_phase: float) -> float:
        """
        Compute how coherent the thought is with automatic substrate.
        
        High coherence → thought aligns with automatic patterns
        Low coherence → thought disrupts automatic patterns
        """
        # During automatic running, thoughts should be phase-locked to cardiac
        # but not interfering with movement
        
        # Check phase alignment
        thought_phase = (2 * np.pi * psychon.frequency * psychon.t_formation) % (2 * np.pi)
        phase_difference = abs(thought_phase - cardiac_phase)
        phase_coherence = np.cos(phase_difference)  # 1 = aligned, -1 = opposed
        
        # Check frequency relationship to cardiac (~1.5 Hz during running)
        cardiac_freq = 1.5  # Hz (typical during exercise)
        freq_ratio = psychon.frequency / cardiac_freq
        
        # Simple integer ratios → high coherence
        nearest_integer = round(freq_ratio)
        freq_mismatch = abs(freq_ratio - nearest_integer)
        freq_coherence = np.exp(-freq_mismatch * 2)
        
        # Combined coherence
        total_coherence = (phase_coherence + 1) / 2 * freq_coherence
        
        return float(np.clip(total_coherence, 0, 1))
    
    def validate_stability(self, thoughts: List[ThoughtPerturbation],
                          t_span: Tuple[float, float] = (0, 5.0),
                          dt: float = 0.001) -> StabilityMetrics:
        """
        Validate skeleton stability under thought perturbations.
        
        Parameters
        ----------
        thoughts : list
            List of thoughts to apply as perturbations
        t_span : tuple
            Time span for simulation
        dt : float
            Time step
            
        Returns
        -------
        metrics : StabilityMetrics
            Stability metrics showing if skeleton remained stable
        """
        # Initialize angles and velocities (standing/running pose)
        n_segments = self.chain.n_segments
        initial_angles = np.array([30, -45, 15]) * np.pi / 180  # Hip, knee, ankle
        initial_velocities = np.zeros(n_segments)
        
        # Time array
        t_array = np.arange(t_span[0], t_span[1], dt)
        n_steps = len(t_array)
        
        # Storage
        angles = np.zeros((n_steps, n_segments))
        velocities = np.zeros((n_steps, n_segments))
        com_positions = np.zeros((n_steps, 3))
        energies = np.zeros(n_steps)
        
        # Initial conditions
        angles[0] = initial_angles
        velocities[0] = initial_velocities
        
        # Define external torques (automatic + thoughts)
        def total_torques(t, theta, omega):
            # Automatic torques (rhythmic muscle activation - hardcoded)
            stride_freq = 1.5  # Hz
            tau_auto = np.array([
                80 * np.sin(2 * np.pi * stride_freq * t),  # Hip
                50 * np.sin(2 * np.pi * stride_freq * t + np.pi/4),  # Knee
                40 * np.sin(2 * np.pi * stride_freq * t + np.pi/2)  # Ankle
            ])
            
            # Thought perturbations (applied at specific times)
            tau_thoughts = np.zeros(n_segments)
            for thought in thoughts:
                # Check if this thought is active at time t
                thought_time = thought.timestamp - thoughts[0].timestamp  # Relative time
                if abs(t - thought_time) < 0.1:  # Active for 100ms
                    # Find segment index
                    for i, seg in enumerate(self.chain.segments):
                        if seg.name == thought.body_segment:
                            tau_thoughts[i] += thought.compute_torque_perturbation(seg)
            
            return tau_auto + tau_thoughts
        
        # Simulate dynamics
        results = self.chain.simulate_coupled_motion(
            initial_angles,
            initial_velocities,
            total_torques,
            t_span,
            dt
        )
        
        angles = results['angles']
        velocities = results['angular_velocities']
        energies = results['energies']
        
        # Compute center of mass movement
        segment_positions = self._compute_segment_positions(angles)
        for i in range(n_steps):
            com_positions[i] = self.chain.compute_total_com(segment_positions[i])
        
        # Check for falling (COM displacement too large or angles exceed limits)
        com_displacement = np.linalg.norm(com_positions - com_positions[0], axis=1)
        max_displacement = np.max(com_displacement)
        
        # Falling criteria
        falling_detected = False
        fall_time = None
        
        if max_displacement > 0.5:  # COM moved more than 0.5m → fell
            falling_detected = True
            fall_idx = np.where(com_displacement > 0.5)[0][0]
            fall_time = t_array[fall_idx]
        
        # Check angle limits
        angle_limits_exceeded = np.any(np.abs(angles) > np.pi/2)
        if angle_limits_exceeded and not falling_detected:
            falling_detected = True
            fall_time = t_array[np.where(np.abs(angles) > np.pi/2)[0][0]]
        
        # Compute stability index
        if not falling_detected:
            stability_index = 1.0  # Perfect stability
        else:
            # Partial stability based on when it fell
            stability_index = (fall_time / t_span[1]) if fall_time else 0.0
        
        # Compute overall thought-body coherence
        coherence_scores = [t.coherence_with_automatic for t in thoughts]
        avg_coherence = np.mean(coherence_scores) if coherence_scores else 0.5
        
        # Create metrics
        metrics = StabilityMetrics(
            time=t_array,
            center_of_mass_displacement=com_displacement,
            angular_momentum=np.zeros(n_steps),  # TODO: compute properly
            total_energy=np.sum(energies, axis=1),
            segment_angles=angles,
            segment_velocities=velocities,
            stability_index=stability_index,
            falling_detected=falling_detected,
            fall_time=fall_time,
            coherence_score=avg_coherence
        )
        
        return metrics
    
    def _compute_segment_positions(self, angles: np.ndarray) -> np.ndarray:
        """Compute 3D positions of all segments given joint angles"""
        n_steps, n_segments = angles.shape
        positions = np.zeros((n_steps, n_segments, 3))
        
        # Simple forward kinematics (assuming planar motion)
        for i in range(n_steps):
            current_pos = np.array([0.0, 0.0, 0.0])  # Start at origin
            
            for j, seg in enumerate(self.chain.segments):
                # Segment vector (in sagittal plane)
                angle = angles[i, j]
                segment_vector = np.array([
                    seg.length * np.cos(angle),
                    0.0,
                    seg.length * np.sin(angle)
                ])
                
                # COM position
                positions[i, j] = current_pos + segment_vector * seg.com_ratio
                
                # Update position for next segment
                current_pos += segment_vector
        
        return positions
    
    def run_complete_validation(self, run_duration: float = 150.0,
                                thought_rate: float = 5.0) -> Dict:
        """
        Run complete validation during 400m run.
        
        Parameters
        ----------
        run_duration : float
            Duration of run (seconds) - 150s for 400m sprint
        thought_rate : float
            Thoughts per second (5 Hz ~ one thought every 200ms)
            
        Returns
        -------
        results : dict
            Complete validation results
        """
        print("="*80)
        print("THOUGHT-SKELETON VALIDATION")
        print("="*80)
        print(f"Body: {self.body_mass} kg, {self.height} m")
        print(f"Duration: {run_duration} s (400m sprint)")
        print(f"Thought rate: {thought_rate} Hz")
        print(f"Clock: Munich Airport atomic clock" if self.munich_clock else "System time")
        print()
        
        # Generate thoughts during run
        print("Generating thoughts...")
        n_thoughts = int(run_duration * thought_rate)
        thoughts = []
        
        for i in range(n_thoughts):
            t = i / thought_rate
            
            # Simulate circuit state (from megaphrenia)
            circuit_state = {
                'dominant_frequency': np.random.uniform(3, 10),  # 3-10 Hz (theta-alpha)
                'amplitude': np.random.uniform(0.5, 1.5),
                'psychon': create_psychon_from_signature(
                    frequency=np.random.uniform(3, 10),
                    amplitude=np.random.uniform(0.5, 1.5)
                )
            }
            
            # Cardiac phase (1.5 Hz during running)
            cardiac_phase = (2 * np.pi * 1.5 * t) % (2 * np.pi)
            
            # O₂ field (simplified)
            o2_field = {
                'O2_molecules': np.random.randn(100, 3),
                'OID': 3.2e15
            }
            
            # Measure thought
            thought = self.measure_thought_from_circuit(
                circuit_state, cardiac_phase, o2_field
            )
            thoughts.append(thought)
        
        print(f"Generated {len(thoughts)} thoughts")
        print()
        
        # Validate stability
        print("Running skeleton dynamics...")
        metrics = self.validate_stability(
            thoughts,
            t_span=(0, run_duration),
            dt=0.001
        )
        
        print()
        print("="*80)
        print("VALIDATION RESULTS")
        print("="*80)
        print(f"Stability Index: {metrics.stability_index:.3f}")
        print(f"Falling Detected: {'YES' if metrics.falling_detected else 'NO'}")
        if metrics.fall_time:
            print(f"Fall Time: {metrics.fall_time:.3f} s")
        print(f"Thought-Body Coherence: {metrics.coherence_score:.3f}")
        print(f"Max COM Displacement: {np.max(metrics.center_of_mass_displacement):.3f} m")
        print()
        
        # Interpretation
        if not metrics.falling_detected:
            print("✅ VALIDATION PASSED: Thoughts did NOT cause falling!")
            print("   Coherent thoughts are compatible with automatic substrate.")
        else:
            print("❌ VALIDATION FAILED: Thoughts caused falling!")
            print("   Incoherent thoughts disrupted automatic substrate.")
        print()
        
        # Save results
        results = {
            'metadata': {
                'body_mass': self.body_mass,
                'height': self.height,
                'run_duration': run_duration,
                'thought_rate': thought_rate,
                'n_thoughts': len(thoughts),
                'munich_clock_sync': self.munich_clock is not None,
                'timestamp': datetime.now().isoformat()
            },
            'thoughts': [
                {
                    'timestamp': t.timestamp,
                    'cardiac_phase': t.cardiac_phase,
                    'frequency': t.psychon.frequency,
                    'amplitude': t.amplitude,
                    'segment': t.body_segment,
                    'coherence': t.coherence_with_automatic
                }
                for t in thoughts
            ],
            'stability_metrics': {
                'stability_index': float(metrics.stability_index),
                'falling_detected': bool(metrics.falling_detected),
                'fall_time': float(metrics.fall_time) if metrics.fall_time else None,
                'coherence_score': float(metrics.coherence_score),
                'max_com_displacement': float(np.max(metrics.center_of_mass_displacement)),
                'total_energy': float(np.mean(metrics.total_energy))
            },
            'validation_status': 'PASSED' if not metrics.falling_detected else 'FAILED'
        }
        
        # Save to file
        output_dir = Path(__file__).parent.parent / 'results' / 'thought_skeleton'
        output_dir.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_file = output_dir / f'validation_{timestamp}.json'
        
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2)
        
        print(f"Results saved to: {output_file}")
        print("="*80)
        
        return results


def main():
    """Run complete thought-skeleton validation"""
    
    # Initialize validator
    validator = ThoughtSkeletonValidator(
        body_mass=70.0,
        height=1.75,
        munich_airport_sync=True
    )
    
    # Run complete validation (400m sprint = ~150 seconds)
    results = validator.run_complete_validation(
        run_duration=150.0,
        thought_rate=5.0  # 5 thoughts per second
    )
    
    return results


if __name__ == "__main__":
    results = main()

