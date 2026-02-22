"""
Megaphrenia Core Module (Categorical Aperture Framework)

FOUNDATIONAL PRINCIPLES:
- Categorical Aperture: Zero-cost topological filtering (W = 0)
- Partition Depth: M = Σ log_b(k_i) determines distinguishability
- Phase-Lock Networks: Velocity-blind synchronization (dG_PL/dE_kin = 0)
- S-Entropy Coordinates: (S_k, S_t, S_e) ∈ [0,1]³

PARADIGM SHIFT (Maxwell Demon Resolution):
- OLD: Biological Maxwell Demons (BMDs) that sort and filter
- NEW: Categorical apertures that reveal pre-existing structure

Core Components:
- Psychon: Unit of mental activity (trajectory-terminus pair)
- Partition Depth: Fundamental quantity for distinguishability
- Categorical Aperture: Zero-work topological constraint
- Phase-Lock Network: Kuramoto dynamics for synchronization
- S-Entropy: Universal coordinate system
- Oscillatory Holes: Functional absences as active carriers
"""

# New foundational modules (Categorical Aperture Framework)
from .partition_depth import (
    PartitionDepth,
    PartitionCoordinates,
    PartitionBasis,
    PartitionExtinction,
    compute_binding_energy,
    partition_depth_from_nuclear_config,
    PARTITION_CONSTANTS,
)

from .categorical_aperture import (
    CategoricalAperture,
    CategoricalConstraint,
    ApertureMode,
    PhaseSpaceTopology,
    VelocityBlindInteraction,
    create_cylindrical_aperture,
    create_spherical_aperture,
    APERTURE_CONSTANTS,
)

from .phase_lock_network import (
    PhaseLockNetwork,
    Oscillator,
    SynchronizationState,
    PhaseLockBond,
    ProteinFoldingNetwork,
    create_random_network,
    create_ordered_network,
    PHASE_LOCK_CONSTANTS,
)

# Existing modules (updated for new framework)
from .psychon import (
    Psychon,
    CategoricalEquivalenceClass,
    CategoricalApertureState,
    create_psychon_from_signature,
)

from .oscillatory_hole import OscillatoryHole, HoleDynamics
from .bmd_state import BMDState, BMDFilter  # Legacy compatibility
from .s_entropy import SEntropyCalculator, calculate_s_entropy
from .categorical_clock import CategoricalClock, O2State

# Legacy aliases for backwards compatibility
BMDFilteringState = CategoricalApertureState

__all__ = [
    # New foundational components
    'PartitionDepth',
    'PartitionCoordinates',
    'PartitionBasis',
    'PartitionExtinction',
    'compute_binding_energy',
    'partition_depth_from_nuclear_config',
    'PARTITION_CONSTANTS',

    'CategoricalAperture',
    'CategoricalConstraint',
    'ApertureMode',
    'PhaseSpaceTopology',
    'VelocityBlindInteraction',
    'create_cylindrical_aperture',
    'create_spherical_aperture',
    'APERTURE_CONSTANTS',

    'PhaseLockNetwork',
    'Oscillator',
    'SynchronizationState',
    'PhaseLockBond',
    'ProteinFoldingNetwork',
    'create_random_network',
    'create_ordered_network',
    'PHASE_LOCK_CONSTANTS',

    # Core psychon
    'Psychon',
    'CategoricalEquivalenceClass',
    'CategoricalApertureState',
    'create_psychon_from_signature',

    # Supporting components
    'OscillatoryHole',
    'HoleDynamics',
    'SEntropyCalculator',
    'calculate_s_entropy',
    'CategoricalClock',
    'O2State',

    # Legacy compatibility
    'BMDState',
    'BMDFilter',
    'BMDFilteringState',
]
