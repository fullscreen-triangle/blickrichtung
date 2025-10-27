"""
Megaphrenia Core Module

Fundamental primitives for biological integrated circuits:
- Psychon: Unit of mental activity (5D S-entropy coordinates)
- Oscillatory holes: Functional absences as active carriers
- BMD states: Biological Maxwell Demon information catalysts
- S-entropy: Universal coordinate system
- Categorical clock: O2-based temporal coordination
"""

from .psychon import Psychon, create_psychon_from_signature
from .oscillatory_hole import OscillatoryHole, HoleDynamics
from .bmd_state import BMDState, BMDFilter
from .s_entropy import SEntropyCalculator, calculate_s_entropy
from .categorical_clock import CategoricalClock, O2State

__all__ = [
    'Psychon',
    'create_psychon_from_signature',
    'OscillatoryHole',
    'HoleDynamics',
    'BMDState',
    'BMDFilter',
    'SEntropyCalculator',
    'calculate_s_entropy',
    'CategoricalClock',
    'O2State',
]

