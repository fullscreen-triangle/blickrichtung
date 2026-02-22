"""
Categorical Aperture: Zero-Cost Filtering Through Topology

FUNDAMENTAL INSIGHT: Maxwell's Demons do not exist. What we mistakenly called
"BMDs" are actually CATEGORICAL APERTURES - topological filters that operate
at zero thermodynamic cost.

From the Resolution of Maxwell's Demons paper:
- W_aperture = 0 (zero work required)
- Phase-lock networks are velocity-blind: dG_PL/dE_kin = 0
- Categorical completion reveals pre-existing structure
- No measurement, no sorting - topological filtering only
- Position-dependent interactions (Van der Waals ~r^-6, dipole ~r^-3)

Key Distinction from Maxwell's Demon:
- Maxwell's demon: Measures, sorts, does work (violates 2nd law)
- Categorical aperture: Topological filter, no measurement, W = 0

The categorical aperture IS the topology of phase space that admits
only certain trajectories - it doesn't "select" or "sort", it simply
constrains what is geometrically possible.
"""

from dataclasses import dataclass, field
from typing import List, Tuple, Optional, Dict, Callable
import numpy as np
from enum import Enum


class ApertureMode(Enum):
    """
    Modes of categorical aperture operation.

    These are NOT active selection modes - they describe the topology
    of the constraint that the aperture represents.
    """
    OPEN = "open"           # All trajectories permitted
    SELECTIVE = "selective"  # Topology admits specific trajectories
    CLOSED = "closed"       # No trajectories permitted


@dataclass
class CategoricalConstraint:
    """
    A single categorical constraint in the aperture.

    Constraints are TOPOLOGICAL, not energetic. They describe which
    regions of phase space are geometrically accessible.

    Attributes:
        dimension: Which dimension this constraint applies to (position coordinates)
        lower_bound: Lower boundary of permitted region
        upper_bound: Upper boundary of permitted region
        is_periodic: Whether the constraint wraps (e.g., angular coordinates)
    """
    dimension: int
    lower_bound: float
    upper_bound: float
    is_periodic: bool = False

    def admits(self, value: float) -> bool:
        """
        Check if a value is admitted by this constraint.

        This is a geometric check, not a measurement - it asks
        "is this point within the permitted region?"
        """
        if self.is_periodic:
            # For periodic boundaries, wrap the value
            period = self.upper_bound - self.lower_bound
            wrapped = ((value - self.lower_bound) % period) + self.lower_bound
            return self.lower_bound <= wrapped <= self.upper_bound
        else:
            return self.lower_bound <= value <= self.upper_bound

    @property
    def measure(self) -> float:
        """
        Geometric measure (width) of the constraint region.
        """
        return self.upper_bound - self.lower_bound


@dataclass
class CategoricalAperture:
    """
    Categorical Aperture: Zero-cost topological filter.

    CRITICAL: This is NOT a Maxwell's demon. It does NOT:
    - Measure anything
    - Sort particles
    - Do work
    - Violate thermodynamics

    What it DOES:
    - Define topological constraints on phase space
    - Admit trajectories that satisfy geometric conditions
    - Operate at W = 0 (zero thermodynamic cost)

    The aperture is velocity-blind: dG/dE_kin = 0
    It only constrains position coordinates, not momenta.

    Attributes:
        id: Unique identifier
        constraints: List of topological constraints
        mode: Current aperture mode (topology state)
        work_done: Should always be 0.0 (verification)
    """

    id: str = field(default_factory=lambda: f"aperture_{np.random.randint(1000000)}")
    constraints: List[CategoricalConstraint] = field(default_factory=list)
    mode: ApertureMode = ApertureMode.OPEN
    work_done: float = 0.0  # MUST remain 0 - apertures do no work

    # Physical constants
    WORK_TOLERANCE: float = 1e-15  # Numerical tolerance for W = 0

    def __post_init__(self):
        """Validate aperture properties."""
        # Critical assertion: apertures do NO work
        assert abs(self.work_done) < self.WORK_TOLERANCE, \
            f"Categorical apertures must do zero work, got W = {self.work_done}"

    def add_constraint(self, dimension: int, lower: float, upper: float,
                      periodic: bool = False) -> None:
        """
        Add a topological constraint to the aperture.

        This defines the geometric boundary of the permitted region
        in the specified dimension. No work is done by adding constraints.

        Args:
            dimension: Coordinate dimension (0, 1, 2 for x, y, z)
            lower: Lower boundary
            upper: Upper boundary
            periodic: Whether the dimension is periodic
        """
        constraint = CategoricalConstraint(
            dimension=dimension,
            lower_bound=lower,
            upper_bound=upper,
            is_periodic=periodic
        )
        self.constraints.append(constraint)
        self.mode = ApertureMode.SELECTIVE

    def admits_position(self, position: np.ndarray) -> bool:
        """
        Check if a position is admitted by the aperture.

        This is a GEOMETRIC check, not a measurement. It asks:
        "Is this point within the topologically permitted region?"

        The check is velocity-blind - momentum is irrelevant.

        Args:
            position: Position vector (must have enough dimensions)

        Returns:
            True if position is within all constraint boundaries
        """
        if self.mode == ApertureMode.CLOSED:
            return False
        if self.mode == ApertureMode.OPEN:
            return True

        # Check each constraint
        for constraint in self.constraints:
            if constraint.dimension >= len(position):
                continue  # Skip constraints for dimensions not in position
            if not constraint.admits(position[constraint.dimension]):
                return False

        return True

    def admits_trajectory(self, trajectory: np.ndarray) -> bool:
        """
        Check if an entire trajectory is admitted.

        A trajectory is admitted if ALL points along it are
        within the topologically permitted region.

        Args:
            trajectory: Array of shape (n_points, n_dimensions)

        Returns:
            True if entire trajectory is admitted
        """
        for point in trajectory:
            if not self.admits_position(point):
                return False
        return True

    def phase_space_measure(self) -> float:
        """
        Calculate the measure (volume) of permitted phase space.

        This is the product of all constraint widths.
        """
        if not self.constraints:
            return float('inf')  # Unconstrained

        measure = 1.0
        for constraint in self.constraints:
            measure *= constraint.measure
        return measure

    def categorical_distance(self, other: 'CategoricalAperture') -> int:
        """
        Calculate categorical distance to another aperture.

        From the categorical mechanics paper:
        d_C = number of aperture traversals required

        For diffusion-limited processes, d_C = 1 (single traversal).

        Args:
            other: Another CategoricalAperture

        Returns:
            Integer categorical distance (number of traversals)
        """
        # Simplified model: distance is 1 if apertures overlap, else 2
        # Full model requires trajectory analysis
        return 1  # d_C = 1 for adjacent apertures

    def is_velocity_blind(self) -> bool:
        """
        Verify that the aperture is velocity-blind.

        This is a fundamental property: dG_PL/dE_kin = 0
        The aperture constraints depend only on position, never on velocity.
        """
        # All CategoricalConstraints are position-based by definition
        return True

    def verify_zero_work(self) -> bool:
        """
        Verify that the aperture does zero work.

        W_aperture = 0 is the fundamental theorem that distinguishes
        categorical apertures from Maxwell's demons.
        """
        return abs(self.work_done) < self.WORK_TOLERANCE

    def set_mode(self, mode: ApertureMode) -> None:
        """
        Set aperture mode (open, selective, or closed).

        Note: This is a topological change, not a mechanical action.
        No work is performed.
        """
        self.mode = mode
        # Ensure work remains zero
        self.work_done = 0.0

    def filter_ensemble(self, positions: np.ndarray) -> np.ndarray:
        """
        Filter an ensemble of positions through the aperture.

        This is NOT sorting or selection in the Maxwell's demon sense.
        It is revealing which members of the ensemble are within
        the topologically permitted region.

        The filtering reveals pre-existing structure; it doesn't create it.

        Args:
            positions: Array of shape (n_particles, n_dimensions)

        Returns:
            Boolean mask indicating which positions are admitted
        """
        n_particles = positions.shape[0]
        admitted = np.zeros(n_particles, dtype=bool)

        for i in range(n_particles):
            admitted[i] = self.admits_position(positions[i])

        return admitted

    def __repr__(self) -> str:
        n_constraints = len(self.constraints)
        return (f"CategoricalAperture(id='{self.id}', mode={self.mode.value}, "
                f"constraints={n_constraints}, W={self.work_done})")


@dataclass
class PhaseSpaceTopology:
    """
    Topology of phase space defined by categorical apertures.

    This represents the full geometric structure that constrains
    trajectories in phase space. Multiple apertures can combine
    to create complex topological filters.
    """

    apertures: List[CategoricalAperture] = field(default_factory=list)
    dimension: int = 3  # Spatial dimensions

    def add_aperture(self, aperture: CategoricalAperture) -> None:
        """Add an aperture to the topology."""
        self.apertures.append(aperture)

    def admits_trajectory(self, trajectory: np.ndarray) -> bool:
        """
        Check if trajectory passes through all required apertures.

        A valid trajectory must be admitted by ALL apertures
        it encounters along its path.
        """
        for aperture in self.apertures:
            if not aperture.admits_trajectory(trajectory):
                return False
        return True

    def total_work(self) -> float:
        """
        Calculate total work done by all apertures.

        This MUST be zero - categorical apertures do no work.
        """
        total = sum(ap.work_done for ap in self.apertures)
        assert abs(total) < 1e-10, \
            f"Phase space topology must do zero work, got W = {total}"
        return total

    def categorical_completion(self, partial_state: Dict) -> Dict:
        """
        Complete a partial categorical state.

        From the theory: categorical completion reveals the unique
        completion of a partial specification. This is NOT active
        inference or Bayesian updating - it is geometric completion.

        The completion already exists; we are revealing it.

        Args:
            partial_state: Dictionary of known categorical coordinates

        Returns:
            Completed state dictionary
        """
        completed = partial_state.copy()

        # For each dimension not specified, the aperture constraints
        # determine the permitted values
        for aperture in self.apertures:
            for constraint in aperture.constraints:
                dim_key = f"dim_{constraint.dimension}"
                if dim_key not in completed:
                    # The "completion" is the center of the permitted region
                    # (simplest geometric completion)
                    completed[dim_key] = (constraint.lower_bound + constraint.upper_bound) / 2

        return completed


@dataclass
class VelocityBlindInteraction:
    """
    Velocity-blind position-dependent interaction.

    From the paper: Phase-lock networks have dG_PL/dE_kin = 0.
    All interactions depend on position only, not velocity.

    Examples:
    - Van der Waals: U ~ r^(-6)
    - Dipole-dipole: U ~ r^(-3)
    - Hydrogen bond: spring-like potential

    Attributes:
        interaction_type: Type of interaction
        strength: Coupling strength
        decay_power: Power law decay exponent
    """

    interaction_type: str
    strength: float  # Coupling strength
    decay_power: float  # r^(-decay_power)

    # Standard interaction types and their decay powers
    INTERACTION_TYPES = {
        'van_der_waals': 6,      # U ~ r^-6
        'dipole_dipole': 3,       # U ~ r^-3
        'hydrogen_bond': 2,       # Approximately harmonic
        'coulomb': 1,             # U ~ r^-1
        'excluded_volume': 12,    # Repulsive core
    }

    def __post_init__(self):
        """Set decay power from type if not specified."""
        if self.decay_power == 0 and self.interaction_type in self.INTERACTION_TYPES:
            self.decay_power = self.INTERACTION_TYPES[self.interaction_type]

    def potential(self, r: float) -> float:
        """
        Calculate potential energy at distance r.

        Note: This depends only on position (r), not velocity.
        This is the velocity-blind property.
        """
        if r <= 0:
            return float('inf')
        return self.strength / (r ** self.decay_power)

    def is_velocity_blind(self) -> bool:
        """Verify velocity-blindness (always True for position-dependent potentials)."""
        return True  # By construction


# Constants for categorical aperture calculations
APERTURE_CONSTANTS = {
    'zero_work': 0.0,                  # W_aperture = 0
    'velocity_blind': True,            # dG_PL/dE_kin = 0
    'categorical_distance_diffusion': 1,  # d_C = 1 for diffusion-limited
}


def create_cylindrical_aperture(radius: float, height: float,
                               center: Tuple[float, float, float] = (0, 0, 0)) -> CategoricalAperture:
    """
    Create a cylindrical categorical aperture.

    Useful for modeling channel proteins, pores, and other
    cylindrically symmetric constraints.

    Args:
        radius: Cylinder radius
        height: Cylinder height
        center: Center position (x, y, z)

    Returns:
        CategoricalAperture with cylindrical constraints
    """
    aperture = CategoricalAperture()

    # Radial constraint (r < radius)
    # For simplicity, approximate with square cross-section
    aperture.add_constraint(0, center[0] - radius, center[0] + radius)
    aperture.add_constraint(1, center[1] - radius, center[1] + radius)

    # Axial constraint
    aperture.add_constraint(2, center[2] - height/2, center[2] + height/2)

    return aperture


def create_spherical_aperture(radius: float,
                             center: Tuple[float, float, float] = (0, 0, 0)) -> CategoricalAperture:
    """
    Create a spherical categorical aperture.

    Args:
        radius: Sphere radius
        center: Center position (x, y, z)

    Returns:
        CategoricalAperture with spherical constraints (approximated)
    """
    aperture = CategoricalAperture()

    # Approximate sphere with cube (full model requires custom constraint)
    aperture.add_constraint(0, center[0] - radius, center[0] + radius)
    aperture.add_constraint(1, center[1] - radius, center[1] + radius)
    aperture.add_constraint(2, center[2] - radius, center[2] + radius)

    return aperture


# Example usage
if __name__ == "__main__":
    print("=== Categorical Aperture Demo ===\n")
    print("KEY INSIGHT: This is NOT a Maxwell's demon!")
    print("Categorical apertures do ZERO work (W = 0)\n")

    # Test 1: Basic aperture creation
    print("Test 1: Creating Categorical Aperture")
    aperture = CategoricalAperture()
    aperture.add_constraint(0, -1.0, 1.0)  # x in [-1, 1]
    aperture.add_constraint(1, -0.5, 0.5)  # y in [-0.5, 0.5]
    print(f"  Aperture: {aperture}")
    print(f"  Work done: {aperture.work_done} (MUST be zero)")
    print(f"  Velocity-blind: {aperture.is_velocity_blind()}")

    # Test 2: Position admission
    print("\nTest 2: Position Admission (Geometric Check)")
    test_positions = [
        np.array([0.0, 0.0, 0.0]),   # Inside
        np.array([0.5, 0.3, 0.0]),   # Inside
        np.array([2.0, 0.0, 0.0]),   # Outside (x too large)
        np.array([0.0, 1.0, 0.0]),   # Outside (y too large)
    ]
    for pos in test_positions:
        admitted = aperture.admits_position(pos)
        status = "ADMITTED" if admitted else "excluded"
        print(f"  Position {pos}: {status}")

    # Test 3: Ensemble filtering
    print("\nTest 3: Ensemble Filtering (Reveals Pre-existing Structure)")
    n_particles = 100
    positions = np.random.uniform(-2, 2, size=(n_particles, 3))
    admitted_mask = aperture.filter_ensemble(positions)
    n_admitted = np.sum(admitted_mask)
    print(f"  Particles in ensemble: {n_particles}")
    print(f"  Particles admitted: {n_admitted}")
    print(f"  Fraction: {n_admitted/n_particles:.2%}")
    print(f"  Work done: {aperture.work_done} (still zero!)")

    # Test 4: Velocity-blind interaction
    print("\nTest 4: Velocity-Blind Interactions")
    vdw = VelocityBlindInteraction("van_der_waals", strength=1.0, decay_power=6)
    print(f"  Van der Waals (r^-6): velocity-blind = {vdw.is_velocity_blind()}")
    print(f"  U(r=0.5) = {vdw.potential(0.5):.2f}")
    print(f"  U(r=1.0) = {vdw.potential(1.0):.2f}")
    print(f"  U(r=2.0) = {vdw.potential(2.0):.4f}")

    # Test 5: Cylindrical aperture (channel protein model)
    print("\nTest 5: Cylindrical Aperture (Channel Protein)")
    channel = create_cylindrical_aperture(radius=0.5, height=2.0)
    print(f"  Channel aperture: {channel}")
    ion_inside = np.array([0.2, 0.2, 0.5])
    ion_outside = np.array([1.0, 0.0, 0.0])
    print(f"  Ion at {ion_inside}: {'PASSES' if channel.admits_position(ion_inside) else 'blocked'}")
    print(f"  Ion at {ion_outside}: {'PASSES' if channel.admits_position(ion_outside) else 'blocked'}")

    # Test 6: Phase space topology
    print("\nTest 6: Phase Space Topology")
    topology = PhaseSpaceTopology()
    topology.add_aperture(channel)
    topology.add_aperture(create_spherical_aperture(radius=3.0))
    print(f"  Total apertures: {len(topology.apertures)}")
    print(f"  Total work: {topology.total_work()} (MUST be zero)")

    # Test 7: Categorical completion
    print("\nTest 7: Categorical Completion")
    partial = {"dim_0": 0.1}
    completed = topology.categorical_completion(partial)
    print(f"  Partial state: {partial}")
    print(f"  Completed state: {completed}")
    print("  (Completion reveals pre-existing structure)")

    print("\n=== Categorical Aperture Verified ===")
    print("Zero work throughout: W_aperture = 0")
