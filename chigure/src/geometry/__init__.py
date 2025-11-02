"""
Oscillatory Geometry Validators Package

This package contains comprehensive validators for testing oscillatory consciousness
theory across multiple scales and domains.

Validators:
-----------
- ComprehensiveConsciousnessValidator: Master integrator across all components
- MultiScaleOscillatoryConsciousnessValidator: 12-level hierarchy validator
- ActivitySleepOscillatoryMirrorValidator: Metabolic mirror analysis
- BMDFrameSelectionValidator: Frame selection dynamics
- FireConsciousnessCouplingValidator: Fire-consciousness evolution
- QuantumIonConsciousnessValidator: Quantum substrate dynamics
- OscillatoryNeuralValidator: Neural oscillation analysis
- OscillatoryMetabolicValidator: Metabolic oscillation analysis  
- OscillatoryTissueValidator: Tissue coordination analysis
- OscillatorySleepValidator: Sleep architecture analysis
- OscillatoryMembraneValidator: Membrane dynamics
- OscillatoryIntracellularValidator: Intracellular signaling
- OscillatoryGenomeValidator: Genomic oscillations
"""

__version__ = "1.0.0"
__author__ = "Kundai Farai Sachikonye"

# Import all validators
try:
    from .comprehensive_consciousness_validator import ComprehensiveConsciousnessValidator
except ImportError as e:
    print(f"Warning: Could not import ComprehensiveConsciousnessValidator: {e}")
    ComprehensiveConsciousnessValidator = None

try:
    from .multiscale_oscillatory_consciousness_validator import MultiScaleOscillatoryConsciousnessValidator
except ImportError as e:
    print(f"Warning: Could not import MultiScaleOscillatoryConsciousnessValidator: {e}")
    MultiScaleOscillatoryConsciousnessValidator = None

try:
    from .sleep_activity_oscillatory_mirror_validator import ActivitySleepOscillatoryMirrorValidator
except ImportError as e:
    print(f"Warning: Could not import ActivitySleepOscillatoryMirrorValidator: {e}")
    ActivitySleepOscillatoryMirrorValidator = None

try:
    from .bmd_frame_selection_validator import BMDFrameSelectionValidator
except ImportError as e:
    print(f"Warning: Could not import BMDFrameSelectionValidator: {e}")
    BMDFrameSelectionValidator = None

try:
    from .fire_consciousness_coupling_validator import FireConsciousnessCouplingValidator
except ImportError as e:
    print(f"Warning: Could not import FireConsciousnessCouplingValidator: {e}")
    FireConsciousnessCouplingValidator = None

try:
    from .quantum_ion_consciousness_validator import QuantumIonConsciousnessValidator
except ImportError as e:
    print(f"Warning: Could not import QuantumIonConsciousnessValidator: {e}")
    QuantumIonConsciousnessValidator = None

try:
    from .oscillatory_neural_validator import OscillatoryNeuralValidator
except ImportError as e:
    print(f"Warning: Could not import OscillatoryNeuralValidator: {e}")
    OscillatoryNeuralValidator = None

try:
    from .oscillatory_metabolic_validator import OscillatoryMetabolicValidator
except ImportError as e:
    print(f"Warning: Could not import OscillatoryMetabolicValidator: {e}")
    OscillatoryMetabolicValidator = None

try:
    from .oscillatory_tissue_validator import OscillatoryTissueValidator
except ImportError as e:
    print(f"Warning: Could not import OscillatoryTissueValidator: {e}")
    OscillatoryTissueValidator = None

try:
    from .oscillatory_sleep_validator import OscillatorySleepValidator
except ImportError as e:
    print(f"Warning: Could not import OscillatorySleepValidator: {e}")
    OscillatorySleepValidator = None

try:
    from .oscillatory_membrane_validator import OscillatoryMembraneValidator
except ImportError as e:
    print(f"Warning: Could not import OscillatoryMembraneValidator: {e}")
    OscillatoryMembraneValidator = None

try:
    from .oscillatory_intracellular_validator import OscillatoryIntracellularValidator
except ImportError as e:
    print(f"Warning: Could not import OscillatoryIntracellularValidator: {e}")
    OscillatoryIntracellularValidator = None

try:
    from .oscillatory_genome_validator import OscillatoryGenomeValidator
except ImportError as e:
    print(f"Warning: Could not import OscillatoryGenomeValidator: {e}")
    OscillatoryGenomeValidator = None

# Export all available validators
__all__ = [
    name for name in [
        'ComprehensiveConsciousnessValidator',
        'MultiScaleOscillatoryConsciousnessValidator',
        'ActivitySleepOscillatoryMirrorValidator',
        'BMDFrameSelectionValidator',
        'FireConsciousnessCouplingValidator',
        'QuantumIonConsciousnessValidator',
        'OscillatoryNeuralValidator',
        'OscillatoryMetabolicValidator',
        'OscillatoryTissueValidator',
        'OscillatorySleepValidator',
        'OscillatoryMembraneValidator',
        'OscillatoryIntracellularValidator',
        'OscillatoryGenomeValidator',
    ] if globals().get(name) is not None
]

print(f"Oscillatory Geometry Validators v{__version__}")
print(f"Loaded {len(__all__)} validator modules")

