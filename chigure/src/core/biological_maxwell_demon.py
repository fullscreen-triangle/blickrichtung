"""
Biological Maxwell Demon (BMD)

BMDs are NOT Maxwell's paradox-breaking demons. They are oscillatory holes themselves.

Theoretical Foundation:
- BMDs = functional absences in oscillatory pathways
- NOT entities that violate thermodynamics
- They ARE the "holes" that need filling
- Information catalysts: enable specific transitions without energy input

Physical Mechanism:
- BMD = transient O₂ configuration around a space
- Electron from semiconductor stabilizes the configuration
- Stabilization = circuit completion = perception event
- Each BMD has unique oscillatory signature

Key Insight:
- Holes are NOT deficiencies - they are PATTERNS
- BMDs are 3D geometric arrangements of O₂ molecules
- Similar geometric patterns → similar perceptions
- Consciousness navigates thought space by moving electrons

Mathematical Framework:
- BMD state = superposition of O₂ categorical states
- Activation = resonance with external oscillatory signature
- Completion = electron stabilization → state collapse
- Memory = stored BMD geometric patterns
"""

import numpy as np
import json
from pathlib import Path
from datetime import datetime
from typing import List, Tuple, Dict, Optional
from dataclasses import dataclass, asdict


@dataclass
class BMDGeometry:
    """
    3D geometric structure of a Biological Maxwell Demon.
    
    The BMD is a specific 3D arrangement of O₂ molecules around a hole.
    This geometry determines what oscillatory signatures it can accept.
    """
    o2_positions: np.ndarray  # [n_molecules, 3] O₂ positions around hole (Angstroms)
    hole_center: np.ndarray  # [3] Center of hole (Angstroms)
    hole_radius: float  # Effective hole radius (Angstroms)
    molecular_density: float  # O₂ molecules per nm³
    geometry_signature: np.ndarray  # [5] Oscillatory signature of this geometry
    
    def to_dict(self) -> dict:
        """Convert to JSON-serializable dictionary."""
        return {
            'o2_positions': self.o2_positions.tolist(),
            'hole_center': self.hole_center.tolist(),
            'hole_radius': float(self.hole_radius),
            'molecular_density': float(self.molecular_density),
            'geometry_signature': self.geometry_signature.tolist()
        }


@dataclass
class BMDActivationEvent:
    """
    Record of BMD activation (oscillatory resonance).
    
    Activation occurs when external signature resonates with BMD geometry.
    """
    timestamp: float  # Seconds
    bmd_index: int  # Which BMD was activated
    input_signature: np.ndarray  # [5] Input oscillatory signature
    resonance_strength: float  # 0-1, strength of resonance
    pre_activation_state: np.ndarray  # [n_o2_states] O₂ state distribution before
    post_activation_state: np.ndarray  # [n_o2_states] O₂ state distribution after
    
    def to_dict(self) -> dict:
        """Convert to JSON-serializable dictionary."""
        return {
            'timestamp': float(self.timestamp),
            'bmd_index': int(self.bmd_index),
            'input_signature': self.input_signature.tolist(),
            'resonance_strength': float(self.resonance_strength),
            'pre_activation_state': self.pre_activation_state.tolist(),
            'post_activation_state': self.post_activation_state.tolist()
        }


@dataclass
class BMDCompletionEvent:
    """
    Record of BMD completion (electron stabilization).
    
    Completion occurs when electron stabilizes the O₂ configuration.
    This is the PERCEPTION event.
    """
    timestamp: float  # Seconds
    bmd_index: int  # Which BMD was completed
    activation_event: BMDActivationEvent  # Preceding activation
    electron_position: np.ndarray  # [3] Electron position (Angstroms)
    stabilization_energy: float  # Energy released (arbitrary units)
    completion_signature: np.ndarray  # [5] Final oscillatory signature
    is_perception: bool  # True if this registered as conscious perception
    
    def to_dict(self) -> dict:
        """Convert to JSON-serializable dictionary."""
        return {
            'timestamp': float(self.timestamp),
            'bmd_index': int(self.bmd_index),
            'activation': self.activation_event.to_dict(),
            'electron_position': self.electron_position.tolist(),
            'stabilization_energy': float(self.stabilization_energy),
            'completion_signature': self.completion_signature.tolist(),
            'is_perception': bool(self.is_perception)
        }


class BiologicalMaxwellDemon:
    """
    A single BMD: oscillatory hole with specific geometric configuration.
    
    This is NOT a thermodynamics-violating demon. It's a PATTERN - a specific
    3D arrangement of O₂ molecules that can be stabilized by an electron.
    
    Think of it as a "lock" that only specific oscillatory "keys" can open.
    """
    
    def __init__(self,
                 geometry: BMDGeometry,
                 index: int,
                 resonance_threshold: float = 0.5):
        """
        Initialize BMD.
        
        Args:
            geometry: 3D geometric structure
            index: Unique identifier
            resonance_threshold: Minimum resonance for activation
        """
        self.geometry = geometry
        self.index = index
        self.resonance_threshold = resonance_threshold
        
        # State
        self.is_active = False
        self.activation_history: List[BMDActivationEvent] = []
        self.completion_history: List[BMDCompletionEvent] = []
        
        # Current O₂ state distribution (probability over 25,110 states)
        self.o2_state_distribution = self._initialize_state_distribution()
    
    def _initialize_state_distribution(self) -> np.ndarray:
        """
        Initialize O₂ state distribution for this BMD.
        
        Each BMD has preferred O₂ states based on its geometry.
        """
        # In full implementation, would calculate from geometry
        # Here we use geometric signature to weight states
        n_states = 25110
        distribution = np.random.rand(n_states)
        distribution /= np.sum(distribution)
        return distribution
    
    def calculate_resonance(self, input_signature: np.ndarray) -> float:
        """
        Calculate resonance between input signature and BMD geometry.
        
        Args:
            input_signature: [5] oscillatory signature
        
        Returns:
            Resonance strength (0-1)
        """
        geom_sig = self.geometry.geometry_signature
        
        # Frequency matching (most important)
        freq_match = np.exp(-abs(input_signature[0] - geom_sig[0]) / (geom_sig[0] + 1e-10))
        
        # Amplitude compatibility
        amp_match = 2 * input_signature[1] * geom_sig[1] / (input_signature[1] + geom_sig[1] + 1e-10)
        
        # Phase relationship
        phase_match = 0.5 * (1.0 + np.cos(input_signature[2] - geom_sig[2]))
        
        # Damping similarity
        damp_match = 1.0 - abs(input_signature[3] - geom_sig[3])
        
        # Symmetry similarity
        symm_match = 1.0 - abs(input_signature[4] - geom_sig[4])
        
        # Weighted combination
        resonance = (0.5 * freq_match +
                    0.2 * amp_match +
                    0.15 * phase_match +
                    0.10 * damp_match +
                    0.05 * symm_match)
        
        return float(np.clip(resonance, 0.0, 1.0))
    
    def activate(self,
                input_signature: np.ndarray,
                timestamp: float) -> Optional[BMDActivationEvent]:
        """
        Attempt to activate BMD with input signature.
        
        Args:
            input_signature: [5] oscillatory signature
            timestamp: Current time (seconds)
        
        Returns:
            BMDActivationEvent if activation successful, None otherwise
        """
        resonance = self.calculate_resonance(input_signature)
        
        if resonance >= self.resonance_threshold:
            # Activation successful
            pre_state = self.o2_state_distribution.copy()
            
            # Update O₂ state distribution based on input
            self._update_state_distribution(input_signature, resonance)
            
            event = BMDActivationEvent(
                timestamp=timestamp,
                bmd_index=self.index,
                input_signature=input_signature,
                resonance_strength=resonance,
                pre_activation_state=pre_state,
                post_activation_state=self.o2_state_distribution.copy()
            )
            
            self.is_active = True
            self.activation_history.append(event)
            
            return event
        
        return None
    
    def _update_state_distribution(self, input_signature: np.ndarray, resonance: float):
        """Update O₂ state distribution based on input."""
        # Simplified: shift distribution toward states matching input
        # In full implementation, would use proper quantum mechanics
        perturbation = np.random.rand(len(self.o2_state_distribution)) * resonance * 0.1
        self.o2_state_distribution += perturbation
        self.o2_state_distribution /= np.sum(self.o2_state_distribution)
    
    def complete(self,
                activation_event: BMDActivationEvent,
                electron_position: np.ndarray,
                timestamp: float) -> BMDCompletionEvent:
        """
        Complete BMD by electron stabilization.
        
        This is the PERCEPTION event - the hole is filled, circuit is complete.
        
        Args:
            activation_event: Preceding activation
            electron_position: [3] Electron position
            timestamp: Current time
        
        Returns:
            BMDCompletionEvent
        """
        # Calculate stabilization energy
        # Energy released when electron stabilizes O₂ configuration
        distance_to_hole = np.linalg.norm(electron_position - self.geometry.hole_center)
        stabilization_energy = 1.0 / (1.0 + distance_to_hole)  # Arbitrary units
        
        # Final oscillatory signature (after electron stabilization)
        completion_signature = self._calculate_completion_signature(
            activation_event.input_signature,
            electron_position
        )
        
        # This registers as perception if stabilization is strong
        is_perception = stabilization_energy > 0.5
        
        event = BMDCompletionEvent(
            timestamp=timestamp,
            bmd_index=self.index,
            activation_event=activation_event,
            electron_position=electron_position,
            stabilization_energy=stabilization_energy,
            completion_signature=completion_signature,
            is_perception=is_perception
        )
        
        self.is_active = False
        self.completion_history.append(event)
        
        return event
    
    def _calculate_completion_signature(self,
                                       input_signature: np.ndarray,
                                       electron_position: np.ndarray) -> np.ndarray:
        """Calculate final oscillatory signature after completion."""
        # Signature is modified by electron stabilization
        geom_sig = self.geometry.geometry_signature.copy()
        
        # Frequency slightly shifts
        geom_sig[0] *= 1.01
        
        # Amplitude increases (stabilization adds energy)
        geom_sig[1] *= 1.1
        
        # Phase shifts based on electron position
        phase_shift = np.sum(electron_position) * 0.01
        geom_sig[2] = (geom_sig[2] + phase_shift) % (2 * np.pi)
        
        # Damping decreases (more stable)
        geom_sig[3] *= 0.9
        
        return geom_sig


class BMDEnsemble:
    """
    Ensemble of BMDs forming a perceptual pathway.
    
    This represents a complete neural pathway (olfactory, serotonergic, etc.)
    as a collection of oscillatory holes that need filling.
    """
    
    def __init__(self,
                 name: str,
                 n_bmds: int = 100,
                 o2_concentration: float = 0.005):
        """
        Initialize BMD ensemble.
        
        Args:
            name: Pathway name ('olfactory', 'serotonin', 'dopamine', etc.)
            n_bmds: Number of BMDs in pathway
            o2_concentration: O₂ concentration (fraction, 0.005 = 0.5%)
        """
        self.name = name
        self.n_bmds = n_bmds
        self.o2_concentration = o2_concentration
        
        print(f"Initializing {name} BMD ensemble with {n_bmds} demons...")
        
        # Generate BMD geometries
        self.bmds = self._generate_bmds()
        
        # Pathway state
        self.active_bmds: List[int] = []
        self.perception_stream: List[BMDCompletionEvent] = []
        
        print(f"✓ {name} ensemble ready")
    
    def _generate_bmds(self) -> List[BiologicalMaxwellDemon]:
        """Generate ensemble of BMDs with diverse geometries."""
        bmds = []
        
        for i in range(self.n_bmds):
            # Generate random BMD geometry
            geometry = self._generate_random_geometry(i)
            
            bmd = BiologicalMaxwellDemon(
                geometry=geometry,
                index=i,
                resonance_threshold=0.5
            )
            
            bmds.append(bmd)
        
        return bmds
    
    def _generate_random_geometry(self, seed: int) -> BMDGeometry:
        """Generate random BMD geometry."""
        np.random.seed(seed)
        
        # Random hole position
        hole_center = np.random.randn(3) * 10.0  # Angstroms
        hole_radius = 2.0 + np.random.rand() * 3.0  # 2-5 Angstroms
        
        # O₂ molecules around hole (cellular concentration)
        n_molecules = int(self.o2_concentration * 1000)  # ~5 molecules
        o2_positions = hole_center + np.random.randn(n_molecules, 3) * hole_radius
        
        # Molecular density
        volume = (4/3) * np.pi * (hole_radius**3) * 1e-27  # m³
        density = n_molecules / (volume * 1e27)  # molecules/nm³
        
        # Geometric signature (derived from positions)
        signature = self._calculate_geometric_signature(o2_positions, hole_center)
        
        return BMDGeometry(
            o2_positions=o2_positions,
            hole_center=hole_center,
            hole_radius=hole_radius,
            molecular_density=density,
            geometry_signature=signature
        )
    
    def _calculate_geometric_signature(self,
                                      o2_positions: np.ndarray,
                                      hole_center: np.ndarray) -> np.ndarray:
        """Calculate oscillatory signature from geometry."""
        # Distances from hole center
        distances = np.linalg.norm(o2_positions - hole_center, axis=1)
        
        # Frequency from average distance (closer = higher frequency)
        avg_dist = np.mean(distances)
        frequency = 1e13 / (1.0 + avg_dist / 5.0)
        
        # Amplitude from number of molecules
        amplitude = np.sqrt(len(o2_positions))
        
        # Phase from spatial distribution
        phase = np.angle(np.sum(o2_positions[:, 0] + 1j * o2_positions[:, 1]))
        
        # Damping from distance spread
        damping = 1.0 / (1.0 + np.std(distances))
        
        # Symmetry from geometric regularity
        center_of_mass = np.mean(o2_positions, axis=0)
        deviation_from_center = np.linalg.norm(center_of_mass - hole_center)
        symmetry = 1.0 / (1.0 + deviation_from_center)
        
        return np.array([frequency, amplitude, phase, damping, symmetry])
    
    def process_input(self,
                     input_signature: np.ndarray,
                     timestamp: float) -> List[BMDActivationEvent]:
        """
        Process input signature through BMD ensemble.
        
        Args:
            input_signature: [5] oscillatory signature
            timestamp: Current time
        
        Returns:
            List of activation events
        """
        activations = []
        
        for bmd in self.bmds:
            if not bmd.is_active:
                event = bmd.activate(input_signature, timestamp)
                if event is not None:
                    activations.append(event)
                    self.active_bmds.append(bmd.index)
        
        return activations
    
    def complete_active_bmds(self, timestamp: float) -> List[BMDCompletionEvent]:
        """
        Complete all active BMDs with electron stabilization.
        
        Args:
            timestamp: Current time
        
        Returns:
            List of completion events
        """
        completions = []
        
        for bmd_idx in self.active_bmds:
            bmd = self.bmds[bmd_idx]
            
            if bmd.activation_history:
                # Get last activation
                activation = bmd.activation_history[-1]
                
                # Generate random electron position
                electron_pos = bmd.geometry.hole_center + np.random.randn(3) * bmd.geometry.hole_radius * 0.5
                
                # Complete BMD
                completion = bmd.complete(activation, electron_pos, timestamp)
                completions.append(completion)
                
                # Add to perception stream if registered
                if completion.is_perception:
                    self.perception_stream.append(completion)
        
        # Clear active BMDs
        self.active_bmds = []
        
        return completions
    
    def save_ensemble(self, output_path: str):
        """Save BMD ensemble to file."""
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        data = {
            'timestamp': datetime.now().isoformat(),
            'name': self.name,
            'n_bmds': self.n_bmds,
            'o2_concentration': float(self.o2_concentration),
            'geometries': [bmd.geometry.to_dict() for bmd in self.bmds],
            'perception_stream_length': len(self.perception_stream)
        }
        
        with open(output_path, 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"✓ Saved {self.name} ensemble to {output_path}")


def demonstrate_bmd():
    """Demonstrate BMD functionality."""
    print("="*80)
    print("BIOLOGICAL MAXWELL DEMON DEMONSTRATION")
    print("="*80 + "\n")
    
    # Create olfactory BMD ensemble
    olfactory = BMDEnsemble(name='olfactory', n_bmds=50, o2_concentration=0.005)
    
    print("\nEnsemble Properties:")
    print("-"*80)
    print(f"  Name: {olfactory.name}")
    print(f"  Number of BMDs: {olfactory.n_bmds}")
    print(f"  O₂ concentration: {olfactory.o2_concentration*100}%")
    
    # Show sample BMD
    print("\nSample BMD Geometry:")
    print("-"*80)
    bmd = olfactory.bmds[0]
    print(f"  Index: {bmd.index}")
    print(f"  Hole center: {bmd.geometry.hole_center}")
    print(f"  Hole radius: {bmd.geometry.hole_radius:.2f} Å")
    print(f"  O₂ molecules: {len(bmd.geometry.o2_positions)}")
    print(f"  Density: {bmd.geometry.molecular_density:.2f} molecules/nm³")
    print(f"  Signature: {bmd.geometry.geometry_signature}")
    
    # Test activation
    print("\n\nActivation Test:")
    print("-"*80)
    
    # Input signature (vanillin-like)
    input_sig = np.array([1.5e13, 5.0, 1.2, 0.7, 0.8])
    print(f"Input signature: {input_sig}")
    
    activations = olfactory.process_input(input_sig, timestamp=0.0)
    print(f"\nActivated BMDs: {len(activations)}")
    
    for act in activations[:5]:  # Show first 5
        print(f"  BMD {act.bmd_index}: resonance = {act.resonance_strength:.3f}")
    
    # Complete active BMDs
    print("\n\nCompletion Test:")
    print("-"*80)
    
    completions = olfactory.complete_active_bmds(timestamp=1e-12)
    print(f"Completed BMDs: {len(completions)}")
    print(f"Perceptions: {len(olfactory.perception_stream)}")
    
    for comp in completions[:5]:  # Show first 5
        print(f"  BMD {comp.bmd_index}:")
        print(f"    Stabilization energy: {comp.stabilization_energy:.3f}")
        print(f"    Is perception: {comp.is_perception}")
    
    # Save
    print("\n\nSaving Results:")
    print("-"*80)
    
    output_dir = Path("results/bmds")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    olfactory.save_ensemble(output_dir / "olfactory_ensemble.json")
    
    print("\n✓ Demonstration complete!")


if __name__ == "__main__":
    demonstrate_bmd()

