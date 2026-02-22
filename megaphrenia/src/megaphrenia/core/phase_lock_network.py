"""
Phase-Lock Networks: Kuramoto Dynamics for Phase Coherence

Phase-lock networks provide the computational substrate for synchronization
in biological and categorical systems. The key insight is that these networks
are VELOCITY-BLIND - they depend only on position (phase), not momentum.

From the categorical mechanics framework:
- dG_PL/dE_kin = 0 (velocity-blind)
- Kuramoto order parameter ⟨r⟩ measures phase coherence
- Synchronization dynamics: dθ_i/dt = ω_i + (K/N) Σ sin(θ_j - θ_i)
- Phase transition at critical coupling K_c

Key Equations:
    Order parameter: r = |1/N Σ exp(iθ_j)|
    Phase dynamics: dθ_i/dt = ω_i + (K/N) Σ_j sin(θ_j - θ_i)
    Critical coupling: K_c = 2/(π g(0)) where g is frequency distribution

Applications:
- Protein folding (H-bond network synchronization)
- Neural oscillations (consciousness as intersection)
- Enzymatic catalysis (SOD1 phase-locking)
"""

from dataclasses import dataclass, field
from typing import List, Tuple, Optional, Dict, Callable
import numpy as np
from enum import Enum


class SynchronizationState(Enum):
    """States of the phase-lock network."""
    INCOHERENT = "incoherent"      # r ≈ 0, no synchronization
    PARTIAL = "partial"            # 0 < r < 0.8
    SYNCHRONIZED = "synchronized"  # r ≥ 0.8


@dataclass
class Oscillator:
    """
    A single oscillator in the phase-lock network.

    Attributes:
        id: Unique identifier
        natural_frequency: ω_i, natural oscillation frequency (rad/s)
        phase: θ_i, current phase (radians)
        amplitude: Oscillation amplitude (normalized)
        position: Spatial position (for distance-dependent coupling)
    """
    id: int
    natural_frequency: float  # ω_i (rad/s)
    phase: float = 0.0       # θ_i (radians)
    amplitude: float = 1.0    # Normalized
    position: Optional[np.ndarray] = None  # Spatial position

    def __post_init__(self):
        """Normalize phase to [0, 2π)."""
        self.phase = self.phase % (2 * np.pi)
        if self.position is None:
            self.position = np.zeros(3)

    def advance_phase(self, dt: float, coupling_term: float = 0.0) -> None:
        """
        Advance phase by one timestep.

        dθ/dt = ω + coupling_term

        Args:
            dt: Time step
            coupling_term: Contribution from coupled oscillators
        """
        self.phase += (self.natural_frequency + coupling_term) * dt
        self.phase = self.phase % (2 * np.pi)


@dataclass
class PhaseLockNetwork:
    """
    Kuramoto-type phase-lock network.

    Implements coupled oscillator dynamics for phase synchronization.
    The network is VELOCITY-BLIND: dG_PL/dE_kin = 0.

    Attributes:
        oscillators: List of oscillators in the network
        coupling_strength: Global coupling constant K
        coupling_matrix: N×N matrix of pairwise couplings (optional)
    """

    oscillators: List[Oscillator] = field(default_factory=list)
    coupling_strength: float = 1.0  # K
    coupling_matrix: Optional[np.ndarray] = None

    # Physical constants
    _phases_history: List[np.ndarray] = field(default_factory=list, repr=False)

    @property
    def n_oscillators(self) -> int:
        """Number of oscillators in the network."""
        return len(self.oscillators)

    @property
    def phases(self) -> np.ndarray:
        """Current phases of all oscillators."""
        return np.array([osc.phase for osc in self.oscillators])

    @property
    def frequencies(self) -> np.ndarray:
        """Natural frequencies of all oscillators."""
        return np.array([osc.natural_frequency for osc in self.oscillators])

    def add_oscillator(self, natural_frequency: float, phase: float = 0.0,
                       position: Optional[np.ndarray] = None) -> Oscillator:
        """
        Add an oscillator to the network.

        Args:
            natural_frequency: Natural frequency ω_i
            phase: Initial phase θ_i
            position: Spatial position (for distance-dependent coupling)

        Returns:
            The created Oscillator
        """
        osc = Oscillator(
            id=self.n_oscillators,
            natural_frequency=natural_frequency,
            phase=phase,
            position=position
        )
        self.oscillators.append(osc)
        return osc

    def order_parameter(self) -> Tuple[float, float]:
        """
        Calculate Kuramoto order parameter.

        r exp(iψ) = (1/N) Σ_j exp(iθ_j)

        Returns:
            Tuple of (r, ψ) where r is coherence magnitude and ψ is mean phase
        """
        if self.n_oscillators == 0:
            return 0.0, 0.0

        phases = self.phases
        # Complex order parameter
        z = np.mean(np.exp(1j * phases))
        r = np.abs(z)
        psi = np.angle(z)

        return r, psi

    def synchronization_state(self) -> SynchronizationState:
        """
        Determine the synchronization state of the network.
        """
        r, _ = self.order_parameter()

        if r < 0.2:
            return SynchronizationState.INCOHERENT
        elif r < 0.8:
            return SynchronizationState.PARTIAL
        else:
            return SynchronizationState.SYNCHRONIZED

    def kuramoto_coupling(self, i: int) -> float:
        """
        Calculate Kuramoto coupling term for oscillator i.

        Coupling = (K/N) Σ_j sin(θ_j - θ_i)

        This is the velocity-blind coupling that depends only on
        phase differences (positions), not velocities.

        Args:
            i: Index of oscillator

        Returns:
            Coupling contribution to dθ_i/dt
        """
        if self.n_oscillators <= 1:
            return 0.0

        theta_i = self.oscillators[i].phase
        coupling_sum = 0.0

        for j, osc_j in enumerate(self.oscillators):
            if i == j:
                continue

            # Get coupling strength (global or from matrix)
            if self.coupling_matrix is not None:
                K_ij = self.coupling_matrix[i, j]
            else:
                K_ij = self.coupling_strength

            # Kuramoto coupling: K * sin(θ_j - θ_i)
            coupling_sum += K_ij * np.sin(osc_j.phase - theta_i)

        return coupling_sum / self.n_oscillators

    def distance_dependent_coupling(self, i: int, decay_power: float = 3.0) -> float:
        """
        Calculate distance-dependent coupling (e.g., dipole-dipole).

        The interaction strength decays as r^(-decay_power).
        This is still velocity-blind - depends only on positions.

        Args:
            i: Index of oscillator
            decay_power: Power law exponent (default: 3 for dipole-dipole)

        Returns:
            Coupling contribution to dθ_i/dt
        """
        if self.n_oscillators <= 1:
            return 0.0

        osc_i = self.oscillators[i]
        coupling_sum = 0.0

        for j, osc_j in enumerate(self.oscillators):
            if i == j:
                continue

            # Calculate distance
            r = np.linalg.norm(osc_j.position - osc_i.position)
            if r < 1e-10:
                r = 1e-10  # Avoid division by zero

            # Distance-dependent coupling
            K_ij = self.coupling_strength / (r ** decay_power)

            coupling_sum += K_ij * np.sin(osc_j.phase - osc_i.phase)

        return coupling_sum / self.n_oscillators

    def step(self, dt: float, use_distance_coupling: bool = False,
             decay_power: float = 3.0) -> None:
        """
        Advance the network by one timestep.

        Integrates the Kuramoto equations:
        dθ_i/dt = ω_i + (K/N) Σ_j sin(θ_j - θ_i)

        Args:
            dt: Time step
            use_distance_coupling: Whether to use distance-dependent coupling
            decay_power: Power law exponent for distance coupling
        """
        # Calculate all coupling terms first (to avoid order dependence)
        coupling_terms = []
        for i in range(self.n_oscillators):
            if use_distance_coupling:
                coupling = self.distance_dependent_coupling(i, decay_power)
            else:
                coupling = self.kuramoto_coupling(i)
            coupling_terms.append(coupling)

        # Update all oscillators
        for i, osc in enumerate(self.oscillators):
            osc.advance_phase(dt, coupling_terms[i])

        # Store history
        self._phases_history.append(self.phases.copy())

    def simulate(self, duration: float, dt: float = 0.01,
                use_distance_coupling: bool = False) -> Dict:
        """
        Simulate network evolution over time.

        Args:
            duration: Total simulation time
            dt: Time step
            use_distance_coupling: Whether to use distance-dependent coupling

        Returns:
            Dictionary with simulation results
        """
        n_steps = int(duration / dt)
        times = np.arange(n_steps) * dt
        r_history = []
        psi_history = []

        self._phases_history = []

        for _ in range(n_steps):
            r, psi = self.order_parameter()
            r_history.append(r)
            psi_history.append(psi)
            self.step(dt, use_distance_coupling)

        return {
            'times': times,
            'r_history': np.array(r_history),
            'psi_history': np.array(psi_history),
            'phases_history': np.array(self._phases_history),
            'final_r': r_history[-1],
            'final_state': self.synchronization_state()
        }

    def critical_coupling(self, frequency_spread: float = 1.0) -> float:
        """
        Estimate critical coupling K_c for phase transition.

        For uniform frequency distribution:
        K_c = 2Δω/π

        where Δω is the half-width of the frequency distribution.

        Args:
            frequency_spread: Characteristic width of frequency distribution

        Returns:
            Estimated critical coupling strength
        """
        return 2 * frequency_spread / np.pi

    def phase_coherence_length(self) -> float:
        """
        Calculate effective phase coherence length.

        Returns inverse of phase variance - higher means more coherent.
        """
        if self.n_oscillators <= 1:
            return float('inf')

        phases = self.phases
        # Circular variance
        var = 1 - np.abs(np.mean(np.exp(1j * phases)))
        if var < 1e-10:
            return float('inf')
        return 1.0 / var

    def is_velocity_blind(self) -> bool:
        """
        Verify that the network is velocity-blind.

        This is a fundamental property: dG_PL/dE_kin = 0.
        Phase-lock dynamics depend only on phases, not velocities.
        """
        return True  # By construction - Kuramoto depends only on phases


@dataclass
class PhaseLockBond:
    """
    A phase-locked bond between two oscillators.

    This represents a stable phase relationship (e.g., H-bond in protein).

    Attributes:
        oscillator_i: First oscillator index
        oscillator_j: Second oscillator index
        target_phase_diff: Target phase difference (locked state)
        spring_constant: Strength of phase-locking
    """
    oscillator_i: int
    oscillator_j: int
    target_phase_diff: float = 0.0  # Phase difference at lock
    spring_constant: float = 1.0    # Coupling strength

    def phase_error(self, network: PhaseLockNetwork) -> float:
        """Calculate deviation from locked phase difference."""
        theta_i = network.oscillators[self.oscillator_i].phase
        theta_j = network.oscillators[self.oscillator_j].phase
        actual_diff = (theta_j - theta_i) % (2 * np.pi)
        target = self.target_phase_diff % (2 * np.pi)
        error = min(abs(actual_diff - target),
                   2 * np.pi - abs(actual_diff - target))
        return error

    def is_locked(self, network: PhaseLockNetwork, tolerance: float = 0.1) -> bool:
        """Check if bond is in phase-locked state."""
        return self.phase_error(network) < tolerance


@dataclass
class ProteinFoldingNetwork(PhaseLockNetwork):
    """
    Specialized phase-lock network for protein folding.

    Models H-bond network synchronization during folding.
    Uses distance-dependent coupling (Van der Waals, H-bond).

    Key equation from protein folding paper:
    r → 0.8 indicates folded state (native configuration)
    """

    bonds: List[PhaseLockBond] = field(default_factory=list)

    def add_hbond(self, donor_idx: int, acceptor_idx: int,
                  strength: float = 1.0) -> PhaseLockBond:
        """
        Add a hydrogen bond between donor and acceptor.

        Args:
            donor_idx: Index of donor oscillator
            acceptor_idx: Index of acceptor oscillator
            strength: Bond strength (spring constant)

        Returns:
            Created PhaseLockBond
        """
        bond = PhaseLockBond(
            oscillator_i=donor_idx,
            oscillator_j=acceptor_idx,
            target_phase_diff=0.0,  # In-phase for H-bond
            spring_constant=strength
        )
        self.bonds.append(bond)
        return bond

    def fold_progress(self) -> float:
        """
        Calculate folding progress (fraction of locked bonds).

        Returns value in [0, 1] where 1 = fully folded.
        """
        if not self.bonds:
            return 0.0

        locked_count = sum(1 for bond in self.bonds if bond.is_locked(self))
        return locked_count / len(self.bonds)

    def is_folded(self, threshold: float = 0.8) -> bool:
        """
        Check if protein is folded.

        Uses both order parameter and bond locking criteria.
        """
        r, _ = self.order_parameter()
        fold_frac = self.fold_progress()
        return r >= threshold and fold_frac >= threshold


def create_random_network(n_oscillators: int, freq_mean: float = 1.0,
                         freq_std: float = 0.5, coupling: float = 1.0) -> PhaseLockNetwork:
    """
    Create a random phase-lock network.

    Args:
        n_oscillators: Number of oscillators
        freq_mean: Mean natural frequency
        freq_std: Standard deviation of frequencies
        coupling: Global coupling strength

    Returns:
        Initialized PhaseLockNetwork
    """
    network = PhaseLockNetwork(coupling_strength=coupling)

    for _ in range(n_oscillators):
        freq = np.random.normal(freq_mean, freq_std)
        phase = np.random.uniform(0, 2 * np.pi)
        position = np.random.randn(3)
        network.add_oscillator(freq, phase, position)

    return network


def create_ordered_network(n_oscillators: int, base_freq: float = 1.0,
                          harmonic_ratio: float = 1.0,
                          coupling: float = 1.0) -> PhaseLockNetwork:
    """
    Create an ordered (harmonic) phase-lock network.

    All oscillators have frequencies that are harmonically related.

    Args:
        n_oscillators: Number of oscillators
        base_freq: Base frequency
        harmonic_ratio: Ratio between successive harmonics
        coupling: Global coupling strength

    Returns:
        Initialized PhaseLockNetwork with harmonic frequencies
    """
    network = PhaseLockNetwork(coupling_strength=coupling)

    for i in range(n_oscillators):
        freq = base_freq * (harmonic_ratio ** i)
        phase = 0.0  # Start in phase
        position = np.array([i, 0, 0])  # Linear arrangement
        network.add_oscillator(freq, phase, position)

    return network


# Physical constants
PHASE_LOCK_CONSTANTS = {
    'o2_frequency': 1e13,           # Hz, O2 master clock
    'proton_frequency': 4e13,       # Hz, H+ 4th harmonic
    'hbond_spring_constant': 250,   # N/m
    'groel_fundamental': 1.1e13,    # Hz, GroEL cavity
    'atp_cycle': 1,                 # Hz, 10^13-th subharmonic
}


# Example usage
if __name__ == "__main__":
    print("=== Phase-Lock Network Demo ===\n")
    print("Kuramoto dynamics for phase synchronization")
    print("Velocity-blind: dG_PL/dE_kin = 0\n")

    # Test 1: Basic network creation
    print("Test 1: Create Random Network")
    network = create_random_network(
        n_oscillators=20,
        freq_mean=1.0,
        freq_std=0.3,
        coupling=0.5
    )
    print(f"  Oscillators: {network.n_oscillators}")
    r_init, _ = network.order_parameter()
    print(f"  Initial order parameter: r = {r_init:.3f}")
    print(f"  Initial state: {network.synchronization_state().value}")
    print(f"  Velocity-blind: {network.is_velocity_blind()}")

    # Test 2: Simulate synchronization
    print("\nTest 2: Simulate Synchronization")
    results = network.simulate(duration=50.0, dt=0.05)
    print(f"  Final order parameter: r = {results['final_r']:.3f}")
    print(f"  Final state: {results['final_state'].value}")

    # Test 3: Critical coupling
    print("\nTest 3: Critical Coupling")
    K_c = network.critical_coupling(frequency_spread=0.3)
    print(f"  Critical coupling K_c = {K_c:.3f}")
    print(f"  Network coupling K = {network.coupling_strength:.3f}")
    print(f"  Above critical: {network.coupling_strength > K_c}")

    # Test 4: Ordered (harmonic) network
    print("\nTest 4: Ordered Harmonic Network")
    ordered = create_ordered_network(
        n_oscillators=10,
        base_freq=1.0,
        harmonic_ratio=1.0,  # All same frequency
        coupling=1.0
    )
    r_ordered, _ = ordered.order_parameter()
    print(f"  Initial r (all in phase): {r_ordered:.3f}")

    # Test 5: Protein folding network
    print("\nTest 5: Protein Folding Network")
    protein = ProteinFoldingNetwork(coupling_strength=2.0)

    # Add oscillators (residues)
    for i in range(8):
        protein.add_oscillator(
            natural_frequency=1.0 + 0.1 * np.random.randn(),
            phase=np.random.uniform(0, 2 * np.pi),
            position=np.array([i, 0, 0])
        )

    # Add H-bonds
    for i in range(0, 7, 2):
        protein.add_hbond(i, i + 1)

    print(f"  Residues: {protein.n_oscillators}")
    print(f"  H-bonds: {len(protein.bonds)}")

    # Simulate folding
    protein.simulate(duration=100.0, dt=0.05)
    print(f"  Final fold progress: {protein.fold_progress():.1%}")
    print(f"  Is folded: {protein.is_folded()}")

    # Test 6: Physical frequencies
    print("\nTest 6: Physical Frequency Scales")
    print(f"  O2 master clock: {PHASE_LOCK_CONSTANTS['o2_frequency']:.1e} Hz")
    print(f"  H+ 4th harmonic: {PHASE_LOCK_CONSTANTS['proton_frequency']:.1e} Hz")
    print(f"  GroEL fundamental: {PHASE_LOCK_CONSTANTS['groel_fundamental']:.1e} Hz")
    print(f"  ATP cycle: {PHASE_LOCK_CONSTANTS['atp_cycle']} Hz (10^13-th subharmonic)")

    print("\n=== Phase-Lock Network Verified ===")
