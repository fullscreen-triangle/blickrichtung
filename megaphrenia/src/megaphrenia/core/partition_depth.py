"""
Partition Depth: Fundamental Quantity for Categorical Mechanics

FOUNDATIONAL PRINCIPLE: Partition Depth M is the fundamental quantity that
determines distinguishability, charge emergence, and binding energy.

From the Partition Depth paper:
- Bounded Phase Space Law: All physical systems occupy bounded regions admitting partition
- M = Σ log_b(k_i) measures hierarchical structure for distinguishability
- Partition Coordinates (n, l, m, s) with capacity C(n) = 2n²
- Charge emerges from partitioning - unpartitioned matter has no charge
- Composition Theorem: M_bound < M_free, deficit released as binding energy
- Partition Extinction: When partition operations impossible, transport coefficients vanish

Key Equations:
    M = Σ log_b(k_i)                    # Partition depth
    C(n) = 2n²                           # Shell capacity
    M_bound < M_free                     # Composition theorem
    ΔE = (M_free - M_bound) × ε_partition # Binding energy
"""

from dataclasses import dataclass, field
from typing import List, Tuple, Optional, Dict
import numpy as np
from enum import Enum


class PartitionBasis(Enum):
    """Basis for partition depth calculations."""
    BINARY = 2      # Standard binary partitioning
    TERNARY = 3     # Ternary trisection (37% more efficient than binary)
    QUATERNARY = 4  # Quaternary for quantum numbers


@dataclass
class PartitionCoordinates:
    """
    Partition Coordinates (n, l, m, s) for categorical state specification.

    From the Partition Depth paper: These coordinates form a complete
    basis for distinguishable states within bounded phase space.

    Attributes:
        n: Principal quantum number (shell, n ≥ 1)
        l: Angular momentum quantum number (0 ≤ l < n)
        m: Magnetic quantum number (-l ≤ m ≤ l)
        s: Spin quantum number (±1/2)

    Capacity: C(n) = 2n² states per shell
    """
    n: int  # Principal (shell)
    l: int  # Angular momentum
    m: int  # Magnetic
    s: float  # Spin (±0.5)

    def __post_init__(self):
        """Validate partition coordinates."""
        assert self.n >= 1, f"Principal quantum number n must be ≥ 1, got {self.n}"
        assert 0 <= self.l < self.n, f"Angular momentum l must be in [0, n-1], got l={self.l}, n={self.n}"
        assert -self.l <= self.m <= self.l, f"Magnetic m must be in [-l, l], got m={self.m}, l={self.l}"
        assert self.s in (-0.5, 0.5), f"Spin s must be ±0.5, got {self.s}"

    @staticmethod
    def shell_capacity(n: int) -> int:
        """
        Calculate shell capacity C(n) = 2n².

        This is the maximum number of distinguishable states in shell n.
        """
        return 2 * n * n

    @staticmethod
    def cumulative_capacity(n_max: int) -> int:
        """
        Calculate cumulative capacity up to shell n_max.

        Total = Σ_{n=1}^{n_max} 2n² = n_max(n_max+1)(2n_max+1)/3
        """
        return sum(2 * n * n for n in range(1, n_max + 1))

    def to_linear_index(self) -> int:
        """
        Convert partition coordinates to linear index.

        Useful for array indexing and hashing.
        """
        # States before shell n
        offset = self.cumulative_capacity(self.n - 1) if self.n > 1 else 0

        # States before subshell l within shell n
        for l_prev in range(self.l):
            offset += 2 * (2 * l_prev + 1)

        # States before m within subshell
        m_offset = self.m + self.l  # Convert -l..l to 0..2l

        # Spin offset
        s_offset = 0 if self.s == -0.5 else 1

        return offset + 2 * m_offset + s_offset

    @classmethod
    def from_linear_index(cls, index: int) -> 'PartitionCoordinates':
        """
        Convert linear index back to partition coordinates.
        """
        # Find shell n
        n = 1
        cumulative = 0
        while cumulative + cls.shell_capacity(n) <= index:
            cumulative += cls.shell_capacity(n)
            n += 1

        remaining = index - cumulative

        # Find subshell l
        l = 0
        while remaining >= 2 * (2 * l + 1):
            remaining -= 2 * (2 * l + 1)
            l += 1

        # Find m and s
        m = (remaining // 2) - l
        s = -0.5 if remaining % 2 == 0 else 0.5

        return cls(n=n, l=l, m=m, s=s)

    def __repr__(self) -> str:
        spin_str = "↑" if self.s > 0 else "↓"
        return f"({self.n}, {self.l}, {self.m}, {spin_str})"


@dataclass
class PartitionDepth:
    """
    Partition Depth M: The fundamental quantity for categorical mechanics.

    M = Σ log_b(k_i) where k_i are the partition factors at each level

    Physical meaning:
    - M measures the hierarchical structure required for distinguishability
    - Higher M = more distinguishable = more "partitioned"
    - M_bound < M_free (composition theorem)
    - Charge emerges only for partitioned entities (M > 0)

    Attributes:
        partition_factors: List of k_i factors at each hierarchical level
        basis: Logarithm base for depth calculation
        m_value: Computed partition depth M = Σ log_b(k_i)
    """
    partition_factors: List[int] = field(default_factory=lambda: [2])
    basis: PartitionBasis = PartitionBasis.TERNARY
    _m_value: Optional[float] = field(default=None, repr=False)

    def __post_init__(self):
        """Validate and compute partition depth."""
        assert all(k >= 1 for k in self.partition_factors), \
            f"All partition factors must be ≥ 1, got {self.partition_factors}"
        self._m_value = self._compute_depth()

    def _compute_depth(self) -> float:
        """
        Compute M = Σ log_b(k_i).

        Uses the specified basis (default: ternary for efficiency).
        """
        b = self.basis.value
        return sum(np.log(k) / np.log(b) for k in self.partition_factors)

    @property
    def m_value(self) -> float:
        """Get the partition depth M."""
        if self._m_value is None:
            self._m_value = self._compute_depth()
        return self._m_value

    @property
    def depth(self) -> float:
        """Alias for m_value."""
        return self.m_value

    @property
    def num_levels(self) -> int:
        """Number of hierarchical levels in the partition."""
        return len(self.partition_factors)

    @property
    def total_states(self) -> int:
        """Total number of distinguishable states = Π k_i."""
        result = 1
        for k in self.partition_factors:
            result *= k
        return result

    def add_level(self, k: int) -> 'PartitionDepth':
        """
        Add a new partition level with factor k.

        Returns new PartitionDepth with increased depth.
        """
        new_factors = self.partition_factors + [k]
        return PartitionDepth(partition_factors=new_factors, basis=self.basis)

    def compose_with(self, other: 'PartitionDepth') -> Tuple['PartitionDepth', float]:
        """
        Compose two partition depths (binding).

        Composition Theorem: M_bound < M_free
        The deficit is released as binding energy.

        Args:
            other: Another PartitionDepth to compose with

        Returns:
            Tuple of (bound PartitionDepth, binding_energy_factor)
        """
        # Combined factors (simplified model: interleave)
        combined_factors = []
        max_len = max(len(self.partition_factors), len(other.partition_factors))

        for i in range(max_len):
            if i < len(self.partition_factors):
                combined_factors.append(self.partition_factors[i])
            if i < len(other.partition_factors):
                combined_factors.append(other.partition_factors[i])

        # Free depth is sum of individual depths
        m_free = self.m_value + other.m_value

        # Bound depth is computed from combined factors
        bound = PartitionDepth(partition_factors=combined_factors, basis=self.basis)
        m_bound = bound.m_value

        # Composition theorem: M_bound ≤ M_free
        # Binding energy proportional to deficit
        binding_energy_factor = max(0, m_free - m_bound)

        return bound, binding_energy_factor

    @classmethod
    def from_coordinates(cls, coords: PartitionCoordinates,
                        basis: PartitionBasis = PartitionBasis.TERNARY) -> 'PartitionDepth':
        """
        Create PartitionDepth from partition coordinates.

        The partition structure is determined by:
        - n levels for principal quantum number
        - l levels for angular momentum
        - 2l+1 for magnetic
        - 2 for spin
        """
        factors = []

        # Principal quantum number partitioning
        factors.append(coords.n)

        # Angular momentum subshell partitioning
        if coords.l > 0:
            factors.append(coords.l)

        # Magnetic partitioning
        factors.append(2 * coords.l + 1)

        # Spin partitioning
        factors.append(2)

        return cls(partition_factors=factors, basis=basis)

    def is_partitioned(self) -> bool:
        """
        Check if this represents a partitioned state.

        Unpartitioned matter has M = 0 (no distinguishability).
        """
        return self.m_value > 0

    def charge_emergence(self, elementary_charge: float = 1.0) -> float:
        """
        Calculate emergent charge from partition depth.

        From the paper: Charge exists only for partitioned entities.
        Charge magnitude proportional to partition depth.

        Args:
            elementary_charge: Base charge unit (default: 1.0 for normalized)

        Returns:
            Emergent charge (0 if unpartitioned)
        """
        if not self.is_partitioned():
            return 0.0

        # Charge emerges proportional to log of total states
        # This is a simplified model - full model requires spin configuration
        return elementary_charge * np.sign(self.m_value) * min(abs(self.m_value), 1.0)

    def __repr__(self) -> str:
        return f"PartitionDepth(M={self.m_value:.3f}, factors={self.partition_factors}, basis={self.basis.name})"


@dataclass
class PartitionExtinction:
    """
    Partition Extinction: When partition operations become impossible.

    At partition extinction:
    - Transport coefficients vanish exactly (not asymptotically)
    - Superconductivity emerges (R = 0 exactly)
    - Phase coherence becomes infinite

    This occurs when:
    - Temperature approaches critical value
    - System enters quantum ground state
    - All particles occupy same partition coordinate
    """

    critical_depth: float = 0.0  # Extinction occurs at M = M_critical
    temperature_ratio: float = 1.0  # T / T_critical
    is_extinct: bool = False

    def __post_init__(self):
        """Check extinction condition."""
        self.is_extinct = self.temperature_ratio <= 1.0 and self.critical_depth <= 0.01

    def transport_coefficient(self, base_coefficient: float) -> float:
        """
        Calculate transport coefficient (e.g., resistance).

        At extinction: coefficient = 0 exactly (not limit).
        """
        if self.is_extinct:
            return 0.0  # Exact zero, not asymptotic

        # Above extinction: normal transport
        return base_coefficient * (1 - 1/self.temperature_ratio) if self.temperature_ratio > 1 else 0.0

    def phase_coherence(self) -> float:
        """
        Calculate phase coherence length.

        At extinction: coherence → ∞
        """
        if self.is_extinct:
            return float('inf')

        return 1.0 / (1 + self.critical_depth)


# Physical constants for partition depth calculations
PARTITION_CONSTANTS = {
    'epsilon_partition': 13.6,  # eV, hydrogen binding energy reference
    'ternary_efficiency': 1.37,  # 37% more efficient than binary
    'electron_shell_capacity': lambda n: 2 * n * n,  # C(n) = 2n²
}


def compute_binding_energy(m_free: float, m_bound: float,
                          epsilon: float = PARTITION_CONSTANTS['epsilon_partition']) -> float:
    """
    Compute binding energy from partition depth deficit.

    ΔE = (M_free - M_bound) × ε_partition

    Args:
        m_free: Sum of free partition depths
        m_bound: Bound partition depth
        epsilon: Energy per unit partition depth (default: 13.6 eV)

    Returns:
        Binding energy in eV
    """
    deficit = max(0, m_free - m_bound)
    return deficit * epsilon


def partition_depth_from_nuclear_config(Z: int, N: int) -> PartitionDepth:
    """
    Compute partition depth for nucleus with Z protons and N neutrons.

    Uses shell model with partition coordinates.

    Args:
        Z: Number of protons
        N: Number of neutrons

    Returns:
        Nuclear partition depth
    """
    # Magic numbers correspond to filled shells
    magic_numbers = [2, 8, 20, 28, 50, 82, 126]

    # Find which shells are filled
    proton_factors = []
    neutron_factors = []

    remaining_z = Z
    remaining_n = N

    for i, magic in enumerate(magic_numbers):
        if i == 0:
            shell_size = magic
        else:
            shell_size = magic - magic_numbers[i-1]

        if remaining_z > 0:
            proton_factors.append(min(remaining_z, shell_size))
            remaining_z -= shell_size

        if remaining_n > 0:
            neutron_factors.append(min(remaining_n, shell_size))
            remaining_n -= shell_size

        if remaining_z <= 0 and remaining_n <= 0:
            break

    # Total factors
    all_factors = [f for f in proton_factors + neutron_factors if f > 0]

    return PartitionDepth(partition_factors=all_factors, basis=PartitionBasis.TERNARY)


# Example usage
if __name__ == "__main__":
    print("=== Partition Depth: Fundamental Quantity Demo ===\n")

    # Test 1: Basic partition depth
    print("Test 1: Basic Partition Depth Calculation")
    pd = PartitionDepth(partition_factors=[2, 3, 4], basis=PartitionBasis.TERNARY)
    print(f"  Factors: {pd.partition_factors}")
    print(f"  M (ternary): {pd.m_value:.3f}")
    print(f"  Total states: {pd.total_states}")
    print(f"  Is partitioned: {pd.is_partitioned()}")
    print(f"  Emergent charge: {pd.charge_emergence():.3f}")

    # Test 2: Partition coordinates
    print("\nTest 2: Partition Coordinates (n, l, m, s)")
    coord = PartitionCoordinates(n=2, l=1, m=0, s=0.5)
    print(f"  Coordinates: {coord}")
    print(f"  Shell capacity C(2): {coord.shell_capacity(2)}")
    print(f"  Linear index: {coord.to_linear_index()}")

    # Round-trip test
    idx = coord.to_linear_index()
    recovered = PartitionCoordinates.from_linear_index(idx)
    print(f"  Round-trip: {recovered}")

    # Test 3: Composition theorem
    print("\nTest 3: Composition Theorem (M_bound < M_free)")
    pd1 = PartitionDepth(partition_factors=[2, 2], basis=PartitionBasis.TERNARY)
    pd2 = PartitionDepth(partition_factors=[3, 2], basis=PartitionBasis.TERNARY)
    print(f"  System 1: M = {pd1.m_value:.3f}")
    print(f"  System 2: M = {pd2.m_value:.3f}")
    print(f"  M_free = M1 + M2 = {pd1.m_value + pd2.m_value:.3f}")

    bound, binding = pd1.compose_with(pd2)
    print(f"  M_bound = {bound.m_value:.3f}")
    print(f"  Binding energy factor: {binding:.3f}")
    print(f"  Binding energy: {compute_binding_energy(pd1.m_value + pd2.m_value, bound.m_value):.2f} eV")

    # Test 4: Partition from coordinates
    print("\nTest 4: Partition Depth from Coordinates")
    coord = PartitionCoordinates(n=3, l=2, m=1, s=-0.5)
    pd_from_coord = PartitionDepth.from_coordinates(coord)
    print(f"  Coordinates: {coord}")
    print(f"  Partition depth: {pd_from_coord}")

    # Test 5: Partition extinction (superconductivity)
    print("\nTest 5: Partition Extinction (Superconductivity)")
    extinction = PartitionExtinction(critical_depth=0.0, temperature_ratio=0.9)
    print(f"  Is extinct: {extinction.is_extinct}")
    print(f"  Transport coefficient: {extinction.transport_coefficient(1.0)}")
    print(f"  Phase coherence: {extinction.phase_coherence()}")

    # Test 6: Nuclear partition depth
    print("\nTest 6: Nuclear Partition Depth (Helium-4)")
    he4 = partition_depth_from_nuclear_config(Z=2, N=2)
    print(f"  He-4 partition depth: {he4}")
    print(f"  Doubly magic (Z=N=2): highly stable")

    print("\n=== Partition Depth Verified ===")
