"""
Megaphrenia Circuits Module

Circuit components for biological integrated circuits:
- BMD Transistors: Three-terminal oscillatory switches
- Logic Gates: AND, OR, NOT, NAND, NOR, XOR
- Flip-Flops: SR, D, JK, T memory elements
- Registers: Data storage and transfer
- Memory: S-entropy content-addressable memory
- ALU: Hierarchical Observer arithmetic/logic unit
- Multiplexers and Decoders: Data routing
"""

from .transistor import BMDTransistor, TransistorType
from .logic_gates import (
    LogicGate, ANDGate, ORGate, NOTGate, 
    NANDGate, NORGate, XORGate
)

__all__ = [
    'BMDTransistor',
    'TransistorType',
    'LogicGate',
    'ANDGate',
    'ORGate',
    'NOTGate',
    'NANDGate',
    'NORGate',
    'XORGate',
]

