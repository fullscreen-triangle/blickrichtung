"""
Core Theoretical Framework

The mathematical and physical foundations of consciousness as generalized olfaction.

Modules:
- oxygen_categorical_clock: O₂ cycling through 25,110 states at ~10¹³ Hz
- saint_entropy: S-entropy coordinate system for universal comparison
- biological_maxwell_demon: BMDs as oscillatory holes (information catalysts)
- oscillatory_signature: Universal [5] signature representation

These modules implement the rigorous theoretical framework that unifies:
- Molecular perception (olfaction)
- Drug effects (psychoactives)
- Temporal perception (time estimation)
- Hardware oscillations (BMD generation)
- Consciousness (oscillatory hole-filling)
"""

from .oxygen_categorical_clock import (
    OxygenCategoricalClock,
    O2QuantumNumbers,
    O2StateProperties
)

from .saint_entropy import (
    SEntropyCalculator,
    SEntropyCoordinates,
    calculate_similarity_matrix
)

from .biological_maxwell_demon import (
    BiologicalMaxwellDemon,
    BMDGeometry,
    BMDActivationEvent,
    BMDCompletionEvent,
    BMDEnsemble
)

from .oscillatory_signature import (
    OscillatorySignature,
    OscillatorySignatureGenerator,
    calculate_signature_similarity_matrix,
    save_signatures
)


__all__ = [
    # Oxygen Categorical Clock
    'OxygenCategoricalClock',
    'O2QuantumNumbers',
    'O2StateProperties',
    
    # S-Entropy
    'SEntropyCalculator',
    'SEntropyCoordinates',
    'calculate_similarity_matrix',
    
    # Biological Maxwell Demons
    'BiologicalMaxwellDemon',
    'BMDGeometry',
    'BMDActivationEvent',
    'BMDCompletionEvent',
    'BMDEnsemble',
    
    # Oscillatory Signatures
    'OscillatorySignature',
    'OscillatorySignatureGenerator',
    'calculate_signature_similarity_matrix',
    'save_signatures',
]

