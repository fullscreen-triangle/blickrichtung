"""
Integration Module: Shooting Methods with Harmonic Balance

Implements the complete shooting + harmonic balance validation framework
for biological integrated circuits, based on molecular gas harmonic timekeeping
and harmonic network graph theory.

Modules:
    - moon_landing: S-entropy navigation (shooting method)
    - harmonic_analysis: Multi-domain FFT harmonic extraction (balance method)
    - harmonic_network_graph: Graph redundancy and multi-path validation
    - circuit_configuration: Declarative circuit construction

This integration enables:
    1. Fast navigation to steady-state solutions (O(1)-O(10) iterations)
    2. Zeptosecond-precision harmonic measurement (2003× enhancement)
    3. Multi-path validation via graph redundancy (100× enhancement)
    4. Declarative circuit specification and testing
"""

from .moon_landing import (
    SEntropyNavigator,
    SSpaceState,
    NavigationPath,
    NavigationMode,
    shoot_circuit_to_steady_state
)

from .harmonic_analysis import (
    HarmonicAnalyzer,
    HarmonicSignature,
    MultiDomainHarmonics,
    FourierDomain,
    extract_beat_frequencies
)

from .harmonic_network_graph import (
    HarmonicNetworkGraph,
    HarmonicNode,
    HarmonicEdge,
    build_circuit_harmonic_graph
)

from .circuit_configuration import (
    CircuitConfig,
    ComponentConfig,
    WireConfig,
    ComponentType,
    CircuitBuilder,
    create_half_adder_config,
    create_full_adder_config,
    create_4bit_adder_config
)

__all__ = [
    # Moon Landing (Shooting)
    'SEntropyNavigator',
    'SSpaceState',
    'NavigationPath',
    'NavigationMode',
    'shoot_circuit_to_steady_state',
    
    # Harmonic Analysis (Balance)
    'HarmonicAnalyzer',
    'HarmonicSignature',
    'MultiDomainHarmonics',
    'FourierDomain',
    'extract_beat_frequencies',
    
    # Harmonic Network Graph (Redundancy)
    'HarmonicNetworkGraph',
    'HarmonicNode',
    'HarmonicEdge',
    'build_circuit_harmonic_graph',
    
    # Circuit Configuration
    'CircuitConfig',
    'ComponentConfig',
    'WireConfig',
    'ComponentType',
    'CircuitBuilder',
    'create_half_adder_config',
    'create_full_adder_config',
    'create_4bit_adder_config',
]

__version__ = "1.0.0"
__author__ = "Megaphrenia Team"
__description__ = "Shooting + Harmonic Balance Integration for Biological Circuits"

