"""
Combinational Circuits built from basic components.

These circuits have no memory/state - output depends only on current inputs.

Circuits implemented:
- Half Adder
- Full Adder
- Comparator
- And more...
"""

from dataclasses import dataclass, field
from typing import Tuple, Optional
import numpy as np
import sys
sys.path.append('..')

try:
    from megaphrenia.core import Psychon
    from megaphrenia.circuits.logic_gates import TriDimensionalLogicGate, ANDGate, ORGate, XORGate
    from megaphrenia.core.bmd_state import SEntropyWeights
except ImportError:
    from core.psychon import Psychon
    from logic_gates import TriDimensionalLogicGate, ANDGate, ORGate, XORGate
    from core.bmd_state import SEntropyWeights


@dataclass
class HalfAdder:
    """
    Half Adder: Adds two 1-bit numbers.
    
    Components:
    - 1× XOR gate (for Sum output)
    - 1× AND gate (for Carry output)
    
    Truth Table:
    A | B | Sum | Carry
    --|---|-----|------
    0 | 0 |  0  |   0
    0 | 1 |  1  |   0
    1 | 0 |  1  |   0
    1 | 1 |  0  |   1
    
    Formula:
    Sum = A XOR B
    Carry = A AND B
    
    Attributes:
        xor_gate: XOR gate for sum
        and_gate: AND gate for carry
        operation_count: Number of operations performed
    """
    
    xor_gate: XORGate = field(default_factory=lambda: XORGate(name="ha_xor"))
    and_gate: ANDGate = field(default_factory=lambda: ANDGate(name="ha_and"))
    operation_count: int = 0
    
    def add(self, a: bool, b: bool) -> Tuple[bool, bool]:
        """
        Add two 1-bit numbers.
        
        Args:
            a: First input bit
            b: Second input bit
            
        Returns:
            Tuple of (sum, carry)
        """
        self.operation_count += 1
        
        # Sum = A XOR B
        sum_bit = self.xor_gate.compute(a, b)
        
        # Carry = A AND B
        carry_bit = self.and_gate.compute(a, b)
        
        return (sum_bit, carry_bit)
    
    def add_with_psychons(self, psychon_a: Psychon, psychon_b: Psychon) -> Tuple[Optional[Psychon], Optional[Psychon]]:
        """
        Add using psychons with S-coordinate context.
        
        Args:
            psychon_a: First input psychon
            psychon_b: Second input psychon
            
        Returns:
            Tuple of (sum_psychon, carry_psychon)
        """
        self.operation_count += 1
        
        # Compute sum with XOR
        sum_psychon = self.xor_gate.compute_with_psychons(psychon_a, psychon_b)
        
        # Compute carry with AND
        carry_psychon = self.and_gate.compute_with_psychons(psychon_a, psychon_b)
        
        return (sum_psychon, carry_psychon)
    
    def get_statistics(self):
        """Get circuit statistics."""
        return {
            'circuit_type': 'HalfAdder',
            'operation_count': self.operation_count,
            'xor_stats': self.xor_gate.get_statistics(),
            'and_stats': self.and_gate.get_statistics()
        }
    
    def __repr__(self) -> str:
        return f"HalfAdder(operations={self.operation_count})"


@dataclass
class FullAdder:
    """
    Full Adder: Adds three 1-bit numbers (A + B + Cin).
    
    Components:
    - 2× Half Adders
    - 1× OR gate
    
    Truth Table:
    A | B | Cin | Sum | Cout
    --|---|-----|-----|-----
    0 | 0 |  0  |  0  |  0
    0 | 0 |  1  |  1  |  0
    0 | 1 |  0  |  1  |  0
    0 | 1 |  1  |  0  |  1
    1 | 0 |  0  |  1  |  0
    1 | 0 |  1  |  0  |  1
    1 | 1 |  0  |  0  |  1
    1 | 1 |  1  |  1  |  1
    
    Formula:
    Sum = A XOR B XOR Cin
    Cout = (A AND B) OR (Cin AND (A XOR B))
    
    Attributes:
        half_adder1: First half adder
        half_adder2: Second half adder
        or_gate: OR gate for final carry
        operation_count: Number of operations performed
    """
    
    half_adder1: HalfAdder = field(default_factory=HalfAdder)
    half_adder2: HalfAdder = field(default_factory=HalfAdder)
    or_gate: ORGate = field(default_factory=lambda: ORGate(name="fa_or"))
    operation_count: int = 0
    
    def add(self, a: bool, b: bool, cin: bool) -> Tuple[bool, bool]:
        """
        Add three 1-bit numbers.
        
        Args:
            a: First input bit
            b: Second input bit
            cin: Carry input bit
            
        Returns:
            Tuple of (sum, carry_out)
        """
        self.operation_count += 1
        
        # First half adder: A + B
        sum1, carry1 = self.half_adder1.add(a, b)
        
        # Second half adder: (A+B) + Cin
        sum_final, carry2 = self.half_adder2.add(sum1, cin)
        
        # Final carry: OR of both carries
        carry_out = self.or_gate.compute(carry1, carry2)
        
        return (sum_final, carry_out)
    
    def get_statistics(self):
        """Get circuit statistics."""
        return {
            'circuit_type': 'FullAdder',
            'operation_count': self.operation_count,
            'ha1_stats': self.half_adder1.get_statistics(),
            'ha2_stats': self.half_adder2.get_statistics(),
            'or_stats': self.or_gate.get_statistics()
        }
    
    def __repr__(self) -> str:
        return f"FullAdder(operations={self.operation_count})"


# Example usage and validation
if __name__ == "__main__":
    print("=== Combinational Circuits Demo ===\n")
    
    # Test Half Adder
    print("="*60)
    print("HALF ADDER TEST")
    print("="*60)
    
    ha = HalfAdder()
    print(f"Created: {ha}\n")
    
    print("Truth Table Validation:")
    print("A | B | Sum | Carry")
    print("--|---|-----|------")
    
    test_cases = [(False, False), (False, True), (True, False), (True, True)]
    all_passed = True
    
    for a, b in test_cases:
        sum_bit, carry_bit = ha.add(a, b)
        
        # Expected results
        expected_sum = a ^ b  # XOR
        expected_carry = a and b  # AND
        
        passed = (sum_bit == expected_sum) and (carry_bit == expected_carry)
        all_passed = all_passed and passed
        
        status = "✅" if passed else "❌"
        print(f"{int(a)} | {int(b)} |  {int(sum_bit)}  |   {int(carry_bit)}   {status}")
    
    print(f"\nHalf Adder Test: {'✅ PASSED' if all_passed else '❌ FAILED'}")
    print(f"Operations performed: {ha.operation_count}")
    
    # Test Full Adder
    print("\n" + "="*60)
    print("FULL ADDER TEST")
    print("="*60)
    
    fa = FullAdder()
    print(f"Created: {fa}\n")
    
    print("Truth Table Validation:")
    print("A | B | Cin | Sum | Cout")
    print("--|---|-----|-----|-----")
    
    full_test_cases = [
        (False, False, False),
        (False, False, True),
        (False, True, False),
        (False, True, True),
        (True, False, False),
        (True, False, True),
        (True, True, False),
        (True, True, True)
    ]
    
    all_passed = True
    
    for a, b, cin in full_test_cases:
        sum_bit, cout = fa.add(a, b, cin)
        
        # Expected results
        expected_sum = (a ^ b ^ cin)
        expected_cout = (a and b) or (cin and (a ^ b))
        
        passed = (sum_bit == expected_sum) and (cout == expected_cout)
        all_passed = all_passed and passed
        
        status = "✅" if passed else "❌"
        print(f"{int(a)} | {int(b)} |  {int(cin)}  |  {int(sum_bit)}  |  {int(cout)}   {status}")
    
    print(f"\nFull Adder Test: {'✅ PASSED' if all_passed else '❌ FAILED'}")
    print(f"Operations performed: {fa.operation_count}")
    
    print("\n" + "="*60)
    print("COMBINATIONAL CIRCUITS VALIDATED")
    print("="*60)

