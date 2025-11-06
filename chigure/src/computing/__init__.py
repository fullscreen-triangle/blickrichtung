"""
Consciousness Programming: Computational Validation Suite

This package contains computational validation modules for the consciousness programming framework.
Each module validates a specific aspect of the theory using lithium, dopamine, and serotonin as test molecules.

Modules:
- electromagnetic_resonance_calculator: H+ EM field resonance with O2 oscillations
- kuramoto_oscillator_network: Phase-locking dynamics in drug-perturbed systems
- categorical_state_space_reduction: Drug-induced categorical constraint
- bmd_phace_sorting: Biological Maxwell Demon information catalysis
- hierarchical_bmd_composition: Nested BMD cascades for multi-level programming

Theoretical Foundations:
- Oscillatory framework: Reality as terminating oscillations
- Categorical equivalence: Categories = Oscillations
- H+ electromagnetic substrate: Proton EM fields sync with O2 oscillations
- BMDs as categorical boundary operators
- Phase-locking as consciousness programming mechanism
"""

__version__ = "2.0.0"
__author__ = "Kundai Farai Sachikonye"

# Core validation modules
from .electromagnetic_resonance_calculator import (
    ElectromagneticResonanceCalculator
)
from .kuramoto_oscillator_network import (
    KuramotoOscillatorNetwork
)
from .categorical_state_space_reduction import (
    CategoricalStateSpaceReducer
)
from .bmd_phace_sorting import (
    BMDPhaseSorter
)
from .hierarchical_bmd_composition import (
    HierarchicalBMDComposer
)

# Extension modules
from .drug_properties import (
    DrugPropertiesCalculator,
    DrugProperties
)
from .therapeutic_window_calculator import (
    TherapeuticWindowCalculator,
    TherapeuticWindow
)
from .metabolic_flux_hierarchy import (
    MetabolicFluxHierarchyAnalyzer,
    MetabolicLevel,
    HierarchicalFluxResults
)
from .metabolic_hierarchy_mapper import (
    MetabolicHierarchyMapper,
    DiseaseState,
    PatientProfile
)
from .metabolic_flux_protocol import (
    MetabolicFluxProtocolGenerator,
    ExperimentalProtocol
)

__all__ = [
    # Core validators
    'ElectromagneticResonanceCalculator',
    'KuramotoOscillatorNetwork',
    'CategoricalStateSpaceReducer',
    'BMDPhaseSorter',
    'HierarchicalBMDComposer',
    
    # Drug properties & therapeutic windows
    'DrugPropertiesCalculator',
    'DrugProperties',
    'TherapeuticWindowCalculator',
    'TherapeuticWindow',
    
    # Metabolic hierarchy
    'MetabolicFluxHierarchyAnalyzer',
    'MetabolicLevel',
    'HierarchicalFluxResults',
    'MetabolicHierarchyMapper',
    'DiseaseState',
    'PatientProfile',
    
    # Experimental protocols
    'MetabolicFluxProtocolGenerator',
    'ExperimentalProtocol',
]

