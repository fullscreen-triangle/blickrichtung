"""
Temporal Perception Validation Module

Validates consciousness framework through temporal perception experiments.

Core hypothesis: O₂ cycling rate at ~10^13 Hz determines temporal perception.

Modules:
- temporal_clock.py: Links O₂ cycling to perceived time
- duration_estimation.py: Time estimation experiments
- critical_flicker_fusion.py: CFF measurements
- reaction_time.py: RT as function of O₂ metabolism
- temporal_validator.py: Complete validation framework
"""

from .temporal_clock import TemporalClock, O2TemporalPredictor
from .duration_estimation import DurationEstimationValidator
from .critical_flicker_fusion import CriticalFlickerFusionValidator  
from .reaction_time import ReactionTimeValidator
from .temporal_validator import TemporalPerceptionValidator

__all__ = [
    'TemporalClock',
    'O2TemporalPredictor',
    'DurationEstimationValidator',
    'CriticalFlickerFusionValidator',
    'ReactionTimeValidator',
    'TemporalPerceptionValidator',
]


