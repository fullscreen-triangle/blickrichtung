"""
O2 Categorical Clock

Quantum state cycling provides universal temporal coordinate.

Key Properties:
- 25,110 accessible O2 configurations  
- Categorical completion drives time emergence
- Provides coherent timing across all biological scales
"""

from dataclasses import dataclass
from typing import List
import numpy as np


@dataclass
class O2State:
    """
    O2 molecular quantum state.
    
    Attributes:
        quantum_numbers: (n, l, m_l, m_s) quantum state
        energy: Energy level (eV)
        configuration_index: Index in 25,110 total configurations
    """
    
    quantum_numbers: tuple = (0, 0, 0, 0)
    energy: float = 0.0
    configuration_index: int = 0
    
    @property
    def is_ground_state(self) -> bool:
        """Check if this is ground state."""
        return self.configuration_index == 0


class CategoricalClock:
    """
    O2-based categorical timing system.
    
    Provides universal temporal coordinate through quantum state cycling.
    """
    
    TOTAL_CONFIGURATIONS = 25110  # Total O2 accessible states
    CYCLE_FREQUENCY = 120.0  # Hz (master clock frequency)
    
    def __init__(self, initial_state: int = 0):
        """
        Initialize categorical clock.
        
        Args:
            initial_state: Initial configuration index (0-25109)
        """
        self.current_state = initial_state % self.TOTAL_CONFIGURATIONS
        self.cycle_count = 0
        self.time_elapsed = 0.0  # seconds
    
    def tick(self) -> int:
        """
        Advance clock by one categorical state.
        
        Returns:
            New state index
        """
        self.current_state = (self.current_state + 1) % self.TOTAL_CONFIGURATIONS
        
        if self.current_state == 0:
            self.cycle_count += 1
        
        # Update elapsed time
        self.time_elapsed = self.cycle_count / self.CYCLE_FREQUENCY
        
        return self.current_state
    
    def advance_to(self, target_state: int) -> int:
        """
        Advance clock to specific target state.
        
        Args:
            target_state: Target configuration index
            
        Returns:
            Number of ticks required
        """
        target = target_state % self.TOTAL_CONFIGURATIONS
        
        if target >= self.current_state:
            ticks = target - self.current_state
        else:
            ticks = (self.TOTAL_CONFIGURATIONS - self.current_state) + target
        
        for _ in range(ticks):
            self.tick()
        
        return ticks
    
    def reset(self) -> None:
        """Reset clock to ground state."""
        self.current_state = 0
        self.cycle_count = 0
        self.time_elapsed = 0.0
    
    @property
    def cycle_period(self) -> float:
        """Full cycle period (seconds)."""
        return self.TOTAL_CONFIGURATIONS / self.CYCLE_FREQUENCY
    
    @property
    def completion_fraction(self) -> float:
        """Fraction of current cycle completed (0-1)."""
        return self.current_state / self.TOTAL_CONFIGURATIONS
    
    def synchronize_with(self, other: 'CategoricalClock') -> bool:
        """
        Synchronize this clock with another.
        
        Args:
            other: Another CategoricalClock instance
            
        Returns:
            True if synchronization successful
        """
        # Synchronize to same state
        self.current_state = other.current_state
        self.cycle_count = other.cycle_count
        self.time_elapsed = other.time_elapsed
        return True
    
    def __repr__(self) -> str:
        return (f"CategoricalClock(state={self.current_state}/{self.TOTAL_CONFIGURATIONS}, "
                f"cycle={self.cycle_count}, t={self.time_elapsed:.3f}s)")

