"""
Validation Framework for Biological Integrated Circuits

All validation tests inherit from ValidationTest base class and automatically
save results in structured JSON format.
"""

from .base import ValidationTest, CircuitTest, HardwareTest
from .utils import load_results, compare_results, aggregate_results

__all__ = [
    'ValidationTest',
    'CircuitTest',
    'HardwareTest',
    'load_results',
    'compare_results',
    'aggregate_results'
]

