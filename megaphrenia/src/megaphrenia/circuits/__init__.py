"""
Megaphrenia Circuits Module

Circuit components for biological integrated circuits:
- BMD Transistors: Three-terminal oscillatory switches
- Logic Gates: Tri-dimensional logic gates (AND, OR, XOR)
- Flip-Flops: SR, D, JK, T memory elements
- Registers: Data storage and transfer
- Memory: S-entropy content-addressable memory
- ALU: Hierarchical Observer arithmetic/logic unit
- Multiplexers and Decoders: Data routing
"""

from .transistor import BMDTransistor, TransistorType
from .logic_gates import (
    TriDimensionalLogicGate,
    LogicFunction,
    ANDGate,
    ORGate,
    XORGate
)
from .combinational import HalfAdder, FullAdder

__all__ = [
    'BMDTransistor',
    'TransistorType',
    'TriDimensionalLogicGate',
    'LogicFunction',
    'ANDGate',
    'ORGate',
    'XORGate',
    'HalfAdder',
    'FullAdder',
]

