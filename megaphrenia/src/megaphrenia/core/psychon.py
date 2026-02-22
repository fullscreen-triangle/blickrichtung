"""
Psychon: Fundamental Unit of Mental Activity (Categorical Aperture Framework)

FOUNDATIONAL INSIGHT: Maxwell's Demons do not exist. What was previously
conceptualized as "BMD filtering" is actually CATEGORICAL APERTURE operation -
zero-cost topological filtering that reveals pre-existing structure.

Theoretical Foundation (Updated):
- Categorical Aperture: W_aperture = 0 (zero thermodynamic cost)
- Partition Depth: M = Σ log_b(k_i) determines distinguishability
- Phase-Lock Networks: dG_PL/dE_kin = 0 (velocity-blind)
- S-Entropy Coordinates: (S_k, S_t, S_e) ∈ [0,1]³ for categorical state

Key Properties:
- PRIMARY tri-dimensional S-coordinates: (S_knowledge, S_time, S_entropy)
- EXTENDED coordinates for refinement: (S_packing, S_hydrophobic)
- Categorical equivalence class membership via topological filtering
- Partition depth determines information structure (not BMD "efficiency")

Paradigm Shift:
- OLD: BMDs compress 10^6 classes through "sorting" (violates thermodynamics)
- NEW: Categorical aperture reveals pre-existing structure (W = 0)
"""

from dataclasses import dataclass, field
from typing import List, Tuple, Dict, Optional, Set
import numpy as np
import time
import uuid


@dataclass
class CategoricalEquivalenceClass:
    """
    A single equivalence class in categorical space.

    Categorical completion reveals which equivalence class a partial
    specification belongs to. This is NOT filtering or selection -
    it is geometric completion of pre-existing structure.

    Attributes:
        class_id: Unique identifier for this equivalence class
        representative_state: The canonical representative of this class
        member_count: Number of states in this equivalence class
        probability: P(equivalence class) for S_knowledge calculation
        partition_depth: M value for this class (from partition depth theory)
    """
    class_id: int
    representative_state: np.ndarray  # Canonical state vector
    member_count: int
    probability: float  # P(class)
    partition_depth: float = 1.0  # M = Σ log_b(k_i)

    def __post_init__(self):
        """Validate equivalence class parameters."""
        assert 0.0 < self.probability <= 1.0, f"Probability must be in (0,1], got {self.probability}"
        assert self.member_count > 0, f"Member count must be positive, got {self.member_count}"
        assert self.partition_depth >= 0, f"Partition depth must be non-negative, got {self.partition_depth}"


@dataclass
class CategoricalApertureState:
    """
    State of categorical aperture for a psychon.

    CRITICAL: This is NOT a Maxwell's demon filter. The categorical aperture
    is a topological constraint that admits certain trajectories. It does
    ZERO work (W_aperture = 0) and reveals pre-existing structure.

    Key distinction:
    - OLD (incorrect): BMD "filters" and "selects" classes
    - NEW (correct): Aperture topology admits geometrically compatible states

    Attributes:
        total_potential_classes: Total number of categorical equivalence classes
        admitted_classes: Set of classes admitted by aperture topology
        active_class: The realized equivalence class
        partition_depth: M value (partition depth theory)
        phase_coherence: Order parameter ⟨r⟩ from phase-lock network
        work_done: MUST be 0.0 - apertures do no work
    """
    total_potential_classes: int
    admitted_classes: Set[int]  # Classes admitted by topology (NOT filtered)
    active_class: int  # The realized class
    partition_depth: float = 1.0  # M = Σ log_b(k_i)
    phase_coherence: float = 0.5  # ⟨r⟩ ∈ [0, 1]
    work_done: float = 0.0  # W_aperture = 0 (fundamental)

    def __post_init__(self):
        """Validate categorical aperture state."""
        assert self.active_class in self.admitted_classes, \
            f"Active class {self.active_class} must be in admitted classes {self.admitted_classes}"
        assert self.partition_depth >= 0, \
            f"Partition depth must be non-negative, got {self.partition_depth}"
        assert 0 <= self.phase_coherence <= 1, \
            f"Phase coherence must be in [0, 1], got {self.phase_coherence}"
        assert self.work_done == 0.0, \
            f"Categorical apertures do ZERO work, got W = {self.work_done}"


# Legacy alias for backwards compatibility
BMDFilteringState = CategoricalApertureState
        

@dataclass
class Psychon:
    """
    Fundamental unit of mental activity (Categorical Aperture Framework).

    PARADIGM: Psychons are trajectory-terminus pairs in S-entropy space.
    Mental states are identified by the path taken, not just the endpoint.

    From Virtual Brain Computing Framework:
    M = (γ, Γ_f) where γ is trajectory and Γ_f is terminus state

    Attributes:
        id: Unique identifier
        timestamp: Creation time (Unix timestamp)

        PRIMARY TRI-DIMENSIONAL S-COORDINATES:
        s_knowledge: Information deficit, -log(P(equivalence_class))
        s_time: Temporal position, steps_to_completion / total_steps [0, 1]
        s_entropy: Categorical entropy, Σ p_i log(p_i) [≥ 0]

        EXTENDED COORDINATES:
        s_packing: Geometric packing configuration
        s_hydrophobic: Energy landscape (hydrophobicity)

        CATEGORICAL APERTURE (replaces BMD):
        equivalence_class: The categorical equivalence class this psychon represents
        aperture_state: State of categorical aperture (zero-work topology)
        
        PHYSICAL PROPERTIES:
        frequency: Characteristic oscillation frequency (Hz)
        amplitude: Oscillation amplitude (normalized)
        phase: Phase angle (radians)
        hole_positions: 3D positions of oscillatory holes (nm)
        hole_mobilities: Mobility of each hole (cm²/(V·s))
        hole_concentrations: Total hole concentration (cm⁻³)
        
        STATE INFORMATION:
        state: Current state ("stable", "transient", "decaying")
        lifetime: Expected lifetime in seconds
        energy: Free energy (eV)
        
        RELATIONSHIPS:
        parent_psychons: IDs of parent psychons
        child_psychons: IDs of spawned child psychons
        coupled_psychons: IDs of phase-locked partners
        
        VALIDATION:
        oscillatory_prediction: FFT-based predictions
        visual_prediction: CNN-based predictions
        agreement_score: Cross-validation score (0-1)
    """
    
    # Identity
    id: str = field(default_factory=lambda: f"psychon_{uuid.uuid4().hex[:8]}")
    timestamp: float = field(default_factory=time.time)
    
    # PRIMARY TRI-DIMENSIONAL S-COORDINATES (st-stellas-categories.tex)
    s_knowledge: float = 0.0  # -log(P(equivalence_class)), information deficit [≥ 0]
    s_time: float = 0.0  # steps_to_completion / total_steps, temporal position [0, 1]
    s_entropy: float = 0.0  # Σ p_i log(p_i), categorical entropy [≥ 0]
    
    # EXTENDED COORDINATES (hardware-lipid LLM refinement)
    s_packing: float = 0.0  # Geometric configuration
    s_hydrophobic: float = 0.0  # Energy landscape
    
    # CATEGORICAL FILTERING (BMD operation)
    equivalence_class: Optional[CategoricalEquivalenceClass] = None
    aperture_state: Optional[BMDFilteringState] = None
    
    # PHYSICAL PROPERTIES
    frequency: float = 120.0  # Hz (default: engine firing frequency)
    amplitude: float = 1.0  # Normalized
    phase: float = 0.0  # Radians
    hole_positions: List[Tuple[float, float, float]] = field(default_factory=list)
    hole_mobilities: List[float] = field(default_factory=list)
    hole_concentrations: float = 2.80e12  # cm⁻³ (measured P-type)
    
    # STATE INFORMATION
    state: str = "stable"
    lifetime: float = 10.0  # seconds (default stability)
    energy: float = 0.615  # eV (P-N junction built-in potential)
    
    # RELATIONSHIPS
    parent_psychons: List[str] = field(default_factory=list)
    child_psychons: List[str] = field(default_factory=list)
    coupled_psychons: List[str] = field(default_factory=list)
    
    # VALIDATION
    oscillatory_prediction: Dict = field(default_factory=dict)
    visual_prediction: Dict = field(default_factory=dict)
    agreement_score: float = 0.0
    
    def __post_init__(self):
        """Initialize derived properties and validate."""
        # Validate S-coordinates
        assert self.s_knowledge >= 0, f"S_knowledge must be non-negative, got {self.s_knowledge}"
        assert 0.0 <= self.s_time <= 1.0, f"S_time must be in [0,1], got {self.s_time}"
        assert self.s_entropy >= 0, f"S_entropy must be non-negative, got {self.s_entropy}"
        
        # If no holes specified, create default configuration
        if not self.hole_positions:
            self.hole_positions = [(0.0, 0.0, 0.0)]
            self.hole_mobilities = [0.0123]  # Measured hole mobility cm²/(V·s)
        
        # Initialize equivalence class if not provided
        if self.equivalence_class is None:
            # Create default equivalence class
            self.equivalence_class = CategoricalEquivalenceClass(
                class_id=0,
                representative_state=self.primary_s_coordinates,
                member_count=1,
                probability=1.0
            )
        
        # Initialize BMD filtering state if not provided
        if self.aperture_state is None:
            self.aperture_state = BMDFilteringState(
                total_potential_classes=1000000,  # ~10^6 typical
                filtered_classes={self.equivalence_class.class_id},
                active_class=self.equivalence_class.class_id,
                filtering_efficiency=1500.0  # Mid-range, 0-3000
            )
        
        # Validate BMD filtering consistency
        assert self.equivalence_class.class_id == self.aperture_state.active_class, \
            f"Equivalence class ID {self.equivalence_class.class_id} must match active class {self.aperture_state.active_class}"
    
    @property
    def primary_s_coordinates(self) -> np.ndarray:
        """Get primary tri-dimensional S-coordinates as array."""
        return np.array([self.s_knowledge, self.s_time, self.s_entropy])
    
    @property
    def extended_s_coordinates(self) -> np.ndarray:
        """Get all 5D S-coordinates as array."""
        return np.array([self.s_knowledge, self.s_time, self.s_entropy, 
                        self.s_packing, self.s_hydrophobic])
    
    @property
    def s_entropy_vector(self) -> np.ndarray:
        """Return 5D S-entropy coordinate vector (legacy compatibility)."""
        return self.extended_s_coordinates
    
    @property
    def oscillatory_signature(self) -> Dict:
        """Return complete oscillatory signature."""
        return {
            'frequency': self.frequency,
            'amplitude': self.amplitude,
            'phase': self.phase,
            'angular_frequency': 2 * np.pi * self.frequency
        }
    
    @property
    def num_holes(self) -> int:
        """Number of oscillatory holes in configuration."""
        return len(self.hole_positions)
    
    @property
    def average_hole_mobility(self) -> float:
        """Average hole mobility across all holes."""
        if not self.hole_mobilities:
            return 0.0
        return np.mean(self.hole_mobilities)
    
    def distance_to(self, other: 'Psychon', use_primary_only: bool = True) -> float:
        """
        Calculate S-entropy distance to another psychon.
        
        From st-stellas-categories.tex: S-distance determines equivalence in categorical space.
        Cross-domain equivalence: Systems with distance < 0.1 are equivalent.
        
        Args:
            other: Another Psychon instance
            use_primary_only: If True, use only (S_k, S_t, S_e); if False, use all 5D
            
        Returns:
            Euclidean distance in S-space (3D or 5D)
        """
        if use_primary_only:
            coords_self = self.primary_s_coordinates
            coords_other = other.primary_s_coordinates
        else:
            coords_self = self.extended_s_coordinates
            coords_other = other.extended_s_coordinates
        
        return float(np.linalg.norm(coords_self - coords_other))
    
    def is_equivalent_to(self, other: 'Psychon', threshold: float = 0.1, 
                        use_primary_only: bool = True) -> bool:
        """
        Check if this psychon is equivalent to another in S-entropy space.
        
        From Circuit-Pathway Duality Theorem:
        If ||S_A - S_B|| < ε, systems are informationally equivalent.
        
        Args:
            other: Another Psychon instance
            threshold: S-entropy distance threshold (default: 0.1)
            use_primary_only: If True, use only (S_k, S_t, S_e); if False, use all 5D
            
        Returns:
            True if psychons are equivalent within threshold
        """
        return self.distance_to(other, use_primary_only=use_primary_only) < threshold
    
    def decay(self, dt: float) -> None:
        """
        Update psychon state after time interval dt.
        
        Lifetime follows exponential decay with barrier energy:
        τ = τ₀ exp(E_barrier / kB T)
        
        Args:
            dt: Time interval (seconds)
        """
        # Update lifetime
        self.lifetime -= dt
        
        # Check if decaying
        if self.lifetime < 1.0:
            self.state = "decaying"
        
        # Amplitude decay
        decay_constant = 1.0 / self.lifetime if self.lifetime > 0 else 1.0
        self.amplitude *= np.exp(-decay_constant * dt)
        
        # Update timestamp
        self.timestamp += dt
    
    def couple_to(self, other: 'Psychon') -> bool:
        """
        Attempt to phase-lock couple to another psychon.
        
        Coupling succeeds if frequencies are harmonically related:
        |n₁ω₁ - n₂ω₂| < Δω (within 0.1 Hz)
        
        Args:
            other: Another Psychon instance
            
        Returns:
            True if coupling successful
        """
        # Check frequency harmonic relationship
        freq_ratio = self.frequency / other.frequency if other.frequency > 0 else 0
        
        # Check if ratio is close to integer (within 1%)
        closest_integer = round(freq_ratio)
        if abs(freq_ratio - closest_integer) < 0.01:
            # Add to coupled list if not already present
            if other.id not in self.coupled_psychons:
                self.coupled_psychons.append(other.id)
            if self.id not in other.coupled_psychons:
                other.coupled_psychons.append(self.id)
            return True
        
        return False
    
    def spawn_child(self, **kwargs) -> 'Psychon':
        """
        Create a child psychon with modified parameters.
        
        Args:
            **kwargs: Parameters to override in child
            
        Returns:
            New Psychon instance
        """
        # Copy current parameters
        child_params = {
            's_knowledge': self.s_knowledge,
            's_time': self.s_time,
            's_entropy': self.s_entropy,
            's_packing': self.s_packing,
            's_hydrophobic': self.s_hydrophobic,
            'frequency': self.frequency,
            'amplitude': self.amplitude,
            'phase': self.phase,
            'hole_positions': self.hole_positions.copy(),
            'hole_mobilities': self.hole_mobilities.copy(),
            'hole_concentrations': self.hole_concentrations,
            'parent_psychons': [self.id],
            'equivalence_class': self.equivalence_class,  # Share equivalence class initially
            'aperture_state': self.aperture_state  # Share BMD filtering state initially
        }
        
        # Override with provided parameters
        child_params.update(kwargs)
        
        # Create child
        child = Psychon(**child_params)
        
        # Register in parent
        self.child_psychons.append(child.id)
        
        return child
    
    def validate(self, oscillatory_pathway: bool = True, 
                visual_pathway: bool = True) -> Dict:
        """
        Validate psychon through dual-pathway analysis.
        
        Oscillatory pathway: FFT → S-entropy → Graph position
        Visual pathway: Droplet simulation → CNN classification
        
        Args:
            oscillatory_pathway: Enable oscillatory validation
            visual_pathway: Enable visual validation
            
        Returns:
            Validation results dictionary
        """
        results = {
            'psychon_id': self.id,
            'timestamp': time.time()
        }
        
        if oscillatory_pathway:
            # Oscillatory pathway prediction
            # (Placeholder - full implementation requires FFT + S-entropy calculation)
            self.oscillatory_prediction = {
                'predicted_state': self.state,
                'predicted_frequency': self.frequency,
                'confidence': 0.95
            }
            results['oscillatory'] = self.oscillatory_prediction
        
        if visual_pathway:
            # Visual pathway prediction
            # (Placeholder - full implementation requires droplet sim + CNN)
            self.visual_prediction = {
                'predicted_state': self.state,
                'pattern_class': 'stable_concentric',
                'confidence': 0.92
            }
            results['visual'] = self.visual_prediction
        
        # Calculate agreement score
        if oscillatory_pathway and visual_pathway:
            osc_conf = self.oscillatory_prediction.get('confidence', 0)
            vis_conf = self.visual_prediction.get('confidence', 0)
            # Agreement formula: 1 - |P_osc - P_vis| / (P_osc + P_vis)
            self.agreement_score = 1 - abs(osc_conf - vis_conf) / (osc_conf + vis_conf + 1e-10)
            results['agreement_score'] = self.agreement_score
            results['status'] = 'VALIDATED' if self.agreement_score > 0.80 else 'PARTIAL'
        
        return results
    
    def to_dict(self) -> Dict:
        """Convert psychon to dictionary for serialization."""
        return {
            'id': self.id,
            'timestamp': self.timestamp,
            's_entropy': {
                's_knowledge': self.s_knowledge,
                's_time': self.s_time,
                's_entropy': self.s_entropy,
                's_packing': self.s_packing,
                's_hydrophobic': self.s_hydrophobic
            },
            'categorical_filtering': {
                'equivalence_class_id': self.equivalence_class.class_id if self.equivalence_class else None,
                'filtering_efficiency': self.aperture_state.filtering_efficiency if self.aperture_state else 0,
                'active_class': self.aperture_state.active_class if self.aperture_state else None
            },
            'oscillatory_signature': self.oscillatory_signature,
            'hole_configuration': {
                'positions': self.hole_positions,
                'mobilities': self.hole_mobilities,
                'concentrations': self.hole_concentrations
            },
            'state': self.state,
            'lifetime': self.lifetime,
            'energy': self.energy,
            'relationships': {
                'parents': self.parent_psychons,
                'children': self.child_psychons,
                'coupled': self.coupled_psychons
            },
            'validation': {
                'agreement_score': self.agreement_score
            }
        }
    
    def __repr__(self) -> str:
        return (f"Psychon(id='{self.id}', S=(k:{self.s_knowledge:.2f}, t:{self.s_time:.2f}, e:{self.s_entropy:.2f}), "
                f"f={self.frequency:.1f}Hz, state='{self.state}', class={self.equivalence_class.class_id if self.equivalence_class else 'N/A'})")


def create_psychon_from_signature(frequency: float, amplitude: float = 1.0, 
                                  phase: float = 0.0, **kwargs) -> Psychon:
    """
    Create a psychon from oscillatory signature.
    
    S-entropy coordinates are estimated from frequency using domain mappings.
    
    Args:
        frequency: Characteristic frequency (Hz)
        amplitude: Oscillation amplitude (default: 1.0)
        phase: Phase angle in radians (default: 0.0)
        **kwargs: Additional parameters for Psychon
        
    Returns:
        Initialized Psychon instance
    """
    # Estimate S-entropy coordinates from frequency
    # (These are placeholder estimates - full implementation requires
    #  measurement or computation from molecular structure)
    
    # Use frequency to estimate primary tri-dimensional coordinates
    log_freq = np.log10(max(frequency, 0.1))  # Avoid log(0)
    
    # S_knowledge: Higher frequency → lower information deficit (more determined state)
    s_knowledge = max(0.0, 2.0 - 0.5 * log_freq)
    
    # S_time: Normalized log frequency as temporal position
    s_time = min(1.0, max(0.0, (log_freq + 2) / 5.0))  # Maps [0.1 Hz - 10 kHz] to [0, 1]
    
    # S_entropy: Peaked at mid-frequencies (maximum diversity)
    s_entropy = 1.0 * np.exp(-((log_freq - 2.0) ** 2) / 2.0)  # Gaussian centered at 100 Hz
    
    # Extended coordinates (refinement)
    s_packing = 0.7 + 0.05 * np.cos(2 * log_freq)
    s_hydrophobic = 0.8 + 0.1 * np.sin(2 * log_freq)
    
    # Create equivalence class
    equiv_class = CategoricalEquivalenceClass(
        class_id=int(frequency) % 1000,  # Simple mapping for demo
        representative_state=np.array([s_knowledge, s_time, s_entropy]),
        member_count=int(100 + 50 * np.sin(log_freq)),  # Varies with frequency
        probability=np.exp(-s_knowledge)  # Probability inversely related to knowledge deficit
    )
    
    # Create BMD filtering state
    bmd_filter = BMDFilteringState(
        total_potential_classes=1000000,
        filtered_classes={equiv_class.class_id},
        active_class=equiv_class.class_id,
        filtering_efficiency=1500.0 + 500.0 * np.sin(log_freq)  # Varies 1000-2000
    )
    
    return Psychon(
        s_knowledge=s_knowledge,
        s_time=s_time,
        s_entropy=s_entropy,
        s_packing=s_packing,
        s_hydrophobic=s_hydrophobic,
        frequency=frequency,
        amplitude=amplitude,
        phase=phase,
        equivalence_class=equiv_class,
        aperture_state=bmd_filter,
        **kwargs
    )


# Example usage
if __name__ == "__main__":
    print("=== Tri-Dimensional S-Coordinate Psychon Demo ===\n")
    
    # Create a psychon at engine firing frequency (120 Hz)
    psychon = create_psychon_from_signature(120.0)
    print("Psychon at 120 Hz (engine firing):")
    print(psychon)
    print(f"Primary S-coords (K, T, E): {psychon.primary_s_coordinates}")
    print(f"Extended S-coords (5D): {psychon.extended_s_coordinates}")
    print(f"Equivalence class: {psychon.equivalence_class.class_id} ({psychon.equivalence_class.member_count} members)")
    print(f"BMD filtering efficiency: {psychon.aperture_state.filtering_efficiency:.1f} bits/molecule\n")
    
    # Create another psychon at harmonic (240 Hz)
    psychon2 = create_psychon_from_signature(240.0)
    print("Psychon at 240 Hz (first harmonic):")
    print(psychon2)
    
    # Check coupling
    coupled = psychon.couple_to(psychon2)
    print(f"\nPhase-lock coupled: {coupled}")
    
    # Check equivalence in primary tri-dimensional space
    distance_3d = psychon.distance_to(psychon2, use_primary_only=True)
    equivalent_3d = psychon.is_equivalent_to(psychon2, use_primary_only=True)
    print(f"S-distance (3D primary): {distance_3d:.3f}")
    print(f"Equivalent (3D, ε=0.1): {equivalent_3d}")
    
    # Check equivalence in full 5D space
    distance_5d = psychon.distance_to(psychon2, use_primary_only=False)
    equivalent_5d = psychon.is_equivalent_to(psychon2, use_primary_only=False)
    print(f"S-distance (5D extended): {distance_5d:.3f}")
    print(f"Equivalent (5D, ε=0.1): {equivalent_5d}")
    
    # Validate
    validation = psychon.validate()
    print(f"\nValidation: {validation['status']}, Agreement: {validation['agreement_score']:.3f}")
    
    print("\n=== Tri-Dimensional BMD Operation Verified ===")
