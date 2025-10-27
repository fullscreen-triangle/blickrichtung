"""
Oscillatory Signature Generation and Processing

Converts molecular structures and hardware measurements into oscillatory signatures,
then projects them into O₂ categorical space.

Modules:
- hardware_signature: Hardware → oscillatory signature
- molecular_signature: Molecule → oscillatory signature
- categorical_projection: Project to O₂ categorical space
- signature_distance: Calculate signature distances

Key Concept:
============
Every physical entity (molecule, hardware oscillation, neural activity) has an
oscillatory signature characterized by [frequency, amplitude, phase, damping, symmetry].

These signatures can be projected into O₂ categorical space (25,110 states) to
predict perceptual similarity.
"""

from .hardware_signature import HardwareSignatureGenerator
from .molecular_signature import MolecularSignatureGenerator
from .categorical_projection import CategoricalProjector
from .signature_distance import SignatureDistanceCalculator

__all__ = [
    'HardwareSignatureGenerator',
    'MolecularSignatureGenerator',
    'CategoricalProjector',
    'SignatureDistanceCalculator',
]

