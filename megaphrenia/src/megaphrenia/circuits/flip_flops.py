"""
Flip-Flops: Memory Elements for Biological Integrated Circuits

Basic memory storage using coordinated BMD networks and logic gates.

Implemented Types:
- SR (Set-Reset) Flip-Flop
- D (Data) Flip-Flop
- JK Flip-Flop  
- T (Toggle) Flip-Flop
"""

from dataclasses import dataclass, field
from typing import Optional
import sys
sys.path.append('..')
from .logic_gates import NANDGate, NORGate, ANDGate, NOTGate, LogicGate


@dataclass
class SRFlipFlop:
    """
    SR (Set-Reset) Flip-Flop using NAND gates.
    
    Truth Table:
    S  R  | Q  Q̄
    ------+-----
    0  0  | 1  1  (invalid)
    0  1  | 1  0  (set)
    1  0  | 0  1  (reset)
    1  1  | Q  Q̄  (hold)
    """
    
    # State
    q: bool = False  # Output
    q_bar: bool = True  # Complement output
    
    # Gates
    nand1: Optional[NANDGate] = None
    nand2: Optional[NANDGate] = None
    
    def __post_init__(self):
        """Initialize NAND gates."""
        if self.nand1 is None:
            self.nand1 = NANDGate()
        if self.nand2 is None:
            self.nand2 = NANDGate()
    
    def set_reset(self, s: bool, r: bool) -> tuple:
        """
        Set or reset flip-flop.
        
        Args:
            s: Set input (active low for NAND implementation)
            r: Reset input (active low)
            
        Returns:
            (q, q_bar) tuple
        """
        # SR flip-flop using cross-coupled NAND gates
        # Q = NAND(S, Q̄)
        # Q̄ = NAND(R, Q)
        
        # Update iteratively until stable (typically 1-2 iterations)
        for _ in range(3):  # Max iterations
            old_q = self.q
            old_q_bar = self.q_bar
            
            self.q = self.nand1.compute(s, self.q_bar)
            self.q_bar = self.nand2.compute(r, self.q)
            
            # Check if stable
            if self.q == old_q and self.q_bar == old_q_bar:
                break
        
        return (self.q, self.q_bar)
    
    def get_state(self) -> bool:
        """Get current state (Q output)."""
        return self.q
    
    def __repr__(self) -> str:
        return f"SRFlipFlop(Q={int(self.q)}, Q̄={int(self.q_bar)})"


@dataclass  
class DFlipFlop:
    """
    D (Data) Flip-Flop with clock.
    
    Stores data input when clock transitions high.
    
    Truth Table:
    CLK  D  | Q(next)
    --------+--------
     ↑   0  | 0
     ↑   1  | 1
     0   X  | Q (hold)
     1   X  | Q (hold)
    """
    
    # State
    q: bool = False
    q_bar: bool = True
    
    # Previous clock state (for edge detection)
    _prev_clk: bool = False
    
    # Gates
    sr_flipflop: Optional[SRFlipFlop] = None
    not_gate: Optional[NOTGate] = None
    nand_s: Optional[NANDGate] = None
    nand_r: Optional[NANDGate] = None
    
    def __post_init__(self):
        """Initialize gates."""
        if self.sr_flipflop is None:
            self.sr_flipflop = SRFlipFlop()
        if self.not_gate is None:
            self.not_gate = NOTGate()
        if self.nand_s is None:
            self.nand_s = NANDGate()
        if self.nand_r is None:
            self.nand_r = NANDGate()
    
    def clock_data(self, clk: bool, d: bool) -> bool:
        """
        Clock in data.
        
        Args:
            clk: Clock signal
            d: Data input
            
        Returns:
            Current Q output
        """
        # Detect rising edge
        rising_edge = clk and not self._prev_clk
        self._prev_clk = clk
        
        if rising_edge:
            # On rising edge, capture D input
            d_bar = self.not_gate.compute(d)
            
            # Generate S and R signals
            s = self.nand_s.compute(d, clk)
            r = self.nand_r.compute(d_bar, clk)
            
            # Update SR flip-flop
            self.q, self.q_bar = self.sr_flipflop.set_reset(s, r)
        
        return self.q
    
    def get_state(self) -> bool:
        """Get current state."""
        return self.q
    
    def __repr__(self) -> str:
        return f"DFlipFlop(Q={int(self.q)})"


@dataclass
class JKFlipFlop:
    """
    JK Flip-Flop with clock.
    
    Universal flip-flop - can implement SR, D, and T.
    
    Truth Table:
    CLK  J  K  | Q(next)
    -----------+---------
     ↑   0  0  | Q (hold)
     ↑   0  1  | 0 (reset)
     ↑   1  0  | 1 (set)
     ↑   1  1  | Q̄ (toggle)
    """
    
    # State
    q: bool = False
    q_bar: bool = True
    
    # Previous clock
    _prev_clk: bool = False
    
    # Gates
    and_j: Optional[ANDGate] = None
    and_k: Optional[ANDGate] = None
    nand_s: Optional[NANDGate] = None
    nand_r: Optional[NANDGate] = None
    sr_flipflop: Optional[SRFlipFlop] = None
    
    def __post_init__(self):
        """Initialize gates."""
        if self.and_j is None:
            self.and_j = ANDGate()
        if self.and_k is None:
            self.and_k = ANDGate()
        if self.nand_s is None:
            self.nand_s = NANDGate()
        if self.nand_r is None:
            self.nand_r = NANDGate()
        if self.sr_flipflop is None:
            self.sr_flipflop = SRFlipFlop()
    
    def clock_jk(self, clk: bool, j: bool, k: bool) -> bool:
        """
        Clock in J and K inputs.
        
        Args:
            clk: Clock signal
            j: J input
            k: K input
            
        Returns:
            Current Q output
        """
        # Detect rising edge
        rising_edge = clk and not self._prev_clk
        self._prev_clk = clk
        
        if rising_edge:
            # Generate S and R from J, K, and current state
            j_and_q_bar = self.and_j.compute(j, self.q_bar)
            k_and_q = self.and_k.compute(k, self.q)
            
            s = self.nand_s.compute(j_and_q_bar, clk)
            r = self.nand_r.compute(k_and_q, clk)
            
            # Update SR flip-flop
            self.q, self.q_bar = self.sr_flipflop.set_reset(s, r)
        
        return self.q
    
    def get_state(self) -> bool:
        """Get current state."""
        return self.q
    
    def __repr__(self) -> str:
        return f"JKFlipFlop(Q={int(self.q)})"


@dataclass
class TFlipFlop:
    """
    T (Toggle) Flip-Flop.
    
    Toggles state when T=1 and clock rises.
    
    Truth Table:
    CLK  T  | Q(next)
    --------+---------
     ↑   0  | Q (hold)
     ↑   1  | Q̄ (toggle)
    """
    
    # State
    q: bool = False
    
    # Implemented using JK flip-flop (J=K=T)
    jk_flipflop: Optional[JKFlipFlop] = None
    
    def __post_init__(self):
        """Initialize JK flip-flop."""
        if self.jk_flipflop is None:
            self.jk_flipflop = JKFlipFlop()
    
    def clock_toggle(self, clk: bool, t: bool) -> bool:
        """
        Clock in toggle input.
        
        Args:
            clk: Clock signal
            t: Toggle input
            
        Returns:
            Current Q output
        """
        # T flip-flop: J=K=T
        self.q = self.jk_flipflop.clock_jk(clk, t, t)
        return self.q
    
    def get_state(self) -> bool:
        """Get current state."""
        return self.q
    
    def __repr__(self) -> str:
        return f"TFlipFlop(Q={int(self.q)})"


# Example usage and validation
if __name__ == "__main__":
    print("=" * 60)
    print("Flip-Flop Validation")
    print("=" * 60)
    
    # Test SR Flip-Flop
    print("\n1. SR Flip-Flop:")
    sr = SRFlipFlop()
    print(f"   Initial: {sr}")
    sr.set_reset(s=False, r=True)  # Set
    print(f"   After Set: {sr}")
    sr.set_reset(s=True, r=False)  # Reset
    print(f"   After Reset: {sr}")
    
    # Test D Flip-Flop
    print("\n2. D Flip-Flop:")
    d_ff = DFlipFlop()
    print(f"   Initial: {d_ff}")
    d_ff.clock_data(clk=True, d=True)  # Rising edge, D=1
    print(f"   After Clock(D=1): {d_ff}")
    d_ff.clock_data(clk=False, d=False)  # Falling edge (no change)
    print(f"   After Clock(D=0, falling): {d_ff}")
    d_ff.clock_data(clk=True, d=False)  # Rising edge, D=0
    print(f"   After Clock(D=0, rising): {d_ff}")
    
    # Test JK Flip-Flop
    print("\n3. JK Flip-Flop:")
    jk = JKFlipFlop()
    print(f"   Initial: {jk}")
    jk.clock_jk(clk=True, j=True, k=False)  # Set
    print(f"   After Set (J=1, K=0): {jk}")
    jk.clock_jk(clk=False, j=False, k=False)
    jk.clock_jk(clk=True, j=True, k=True)  # Toggle
    print(f"   After Toggle (J=1, K=1): {jk}")
    
    # Test T Flip-Flop
    print("\n4. T Flip-Flop:")
    t_ff = TFlipFlop()
    print(f"   Initial: {t_ff}")
    t_ff.clock_toggle(clk=True, t=True)  # Toggle
    print(f"   After Toggle: {t_ff}")
    t_ff.clock_toggle(clk=False, t=True)
    t_ff.clock_toggle(clk=True, t=True)  # Toggle again
    print(f"   After Toggle: {t_ff}")
    
    print("\n" + "=" * 60)
    print("Flip-Flops: VALIDATION COMPLETE")
    print("=" * 60)

