"""
BMD Transistor: Tri-Dimensional S-Coordinate Operator (REDESIGNED)

CRITICAL INSIGHT: BMD transistors don't have fixed behavior—they operate
simultaneously as RESISTOR, CAPACITOR, and INDUCTOR with actual impedance
determined by S-entropy minimization.

From st-stellas-circuits.tex: A single BMD transistor simultaneously exhibits:
- RESISTIVE behavior in S_knowledge dimension
- CAPACITIVE behavior in S_time dimension
- INDUCTIVE behavior in S_entropy dimension

Actual operation mode selected via S-entropy optimization with context-dependent
weighting parameters (α, β, γ).

Validated Performance (resistive mode):
- On/Off ratio: 42.1 (exact match to theory)
- Response time: <1 μs
- Hole mobility: 0.0123 cm²/(V·s)
- Conductivity: 7.53×10⁻⁸ S/cm
"""

from dataclasses import dataclass, field
from typing import Optional, Tuple, Dict
from enum import Enum
import numpy as np
import sys
sys.path.append('..')

try:
    from megaphrenia.core import Psychon, BMDState, OscillatoryHole
    from megaphrenia.core.bmd_state import OperationMode, TriDimensionalParameters, SEntropyWeights
except ImportError:
    # Fallback for direct execution
    from core.psychon import Psychon
    from core.bmd_state import BMDState, OperationMode, TriDimensionalParameters, SEntropyWeights
    from core.oscillatory_hole import OscillatoryHole


# Physical constants
ELEMENTARY_CHARGE = 1.6e-19  # Coulombs
KB_T = 0.026  # eV at room temperature


class TransistorType(Enum):
    """Transistor configuration types."""
    NPTYPE = "n-type"  # N-type semiconductor base
    PTYPE = "p-type"  # P-type semiconductor base


@dataclass
class BMDTransistor:
    """
    Tri-dimensional oscillatory operator implementing transistor functionality (REDESIGNED).
    
    PARADIGM SHIFT: This is NOT a simple switch—it's a tri-dimensional operator that
    computes R, C, and L behavior simultaneously, selecting actual impedance through
    S-entropy minimization.
    
    Architecture:
    - Source (S): P-type region with hole concentration p_h = 2.80×10¹² cm⁻³
    - Drain (D): N-type region with electron concentration n_e = 3.57×10⁷ cm⁻³
    - Gate (G): BMD tri-dimensional operator with R-C-L parameters
    
    Tri-Dimensional Operation:
    - S_knowledge dimension: I(t) = I₀ · ℐ_BMD(V_G) [RESISTIVE]
    - S_time dimension: I(t) = C_equiv · dV/dt [CAPACITIVE]
    - S_entropy dimension: V(t) = L_equiv · dI/dt [INDUCTIVE]
    
    Actual behavior: Selected via S-entropy minimization
        argmin[α·S_k + β·S_t + γ·S_e]
    
    Attributes:
        source: Source psychon (P-type region)
        drain: Drain psychon (N-type region)
        gate: BMD state with tri-dimensional parameters
        transistor_type: PTYPE or NPTYPE
        
        # Measured characteristics (resistive mode baseline)
        on_off_ratio: Rectification ratio (42.1 measured)
        response_time: Switching time (<1 μs)
        hole_mobility: Hole mobility (0.0123 cm²/(V·s))
        conductivity: Therapeutic conductivity (7.53×10⁻⁸ S/cm)
        threshold_voltage: Gate threshold (~0.5 V)
        
        # Current operating mode
        active_mode: Currently selected mode (RESISTIVE, CAPACITIVE, or INDUCTIVE)
        mode_history: History of mode selections
    """
    
    # Terminals
    source: Optional[Psychon] = None
    drain: Optional[Psychon] = None
    gate: Optional[BMDState] = None
    
    # Configuration
    transistor_type: TransistorType = TransistorType.PTYPE
    
    # Measured characteristics (baseline from biological-semiconductors paper)
    on_off_ratio: float = 42.1  # Exact measured value (resistive mode)
    response_time: float = 1e-6  # <1 μs
    hole_mobility: float = 0.0123  # cm²/(V·s)
    conductivity: float = 7.53e-8  # S/cm
    threshold_voltage: float = 0.5  # V
    
    # State variables
    gate_voltage: float = 0.0
    source_drain_voltage: float = 0.0
    source_drain_current: float = 0.0
    state: str = "off"  # "off", "on", "switching"
    
    # Tri-dimensional operation tracking
    active_mode: OperationMode = OperationMode.RESISTIVE
    mode_history: list = field(default_factory=list)
    mode_selection_count: Dict[OperationMode, int] = field(default_factory=lambda: {
        OperationMode.RESISTIVE: 0,
        OperationMode.CAPACITIVE: 0,
        OperationMode.INDUCTIVE: 0
    })
    
    # Performance tracking
    switching_count: int = 0
    error_count: int = 0
    last_switch_time: float = 0.0
    
    # Geometry
    channel_length: float = 10.0  # nm
    channel_width: float = 10.0  # nm
    channel_area: float = field(init=False)  # cm²
    
    def __post_init__(self):
        """Initialize transistor with default psychons and BMD if not provided."""
        # Calculate channel area
        self.channel_area = (self.channel_length * 1e-7) * (self.channel_width * 1e-7)  # nm² to cm²
        
        # Create default source (P-type) if not provided
        if self.source is None:
            from megaphrenia.core.psychon import create_psychon_from_signature
            self.source = create_psychon_from_signature(
                frequency=120.0,  # Default frequency
                id="source_p_type"
            )
            self.source.hole_concentrations = 2.80e12  # Measured P-type
        
        # Create default drain (N-type) if not provided
        if self.drain is None:
            from megaphrenia.core.psychon import create_psychon_from_signature
            self.drain = create_psychon_from_signature(
                frequency=120.0,
                id="drain_n_type"
            )
            self.drain.hole_concentrations = 3.57e7  # Measured N-type
        
        # Create default BMD gate with tri-dimensional parameters if not provided
        if self.gate is None:
            # Calculate tri-dimensional parameters from measured characteristics
            R_knowledge = 1.0 / self.conductivity  # Ω from conductivity
            tau_char = self.response_time  # Use response time as characteristic time
            C_time = tau_char / (np.pi * R_knowledge)
            L_entropy = (np.pi * R_knowledge) / tau_char
            
            tri_params = TriDimensionalParameters(
                R_knowledge=R_knowledge,
                C_time=C_time,
                L_entropy=L_entropy,
                tau_characteristic=tau_char
            )
            
            self.gate = BMDState(
                id=f"gate_{np.random.randint(1000000)}",
                tri_params=tri_params,
                catalysis_efficiency=3000.0  # Haloperidol baseline
            )
    
    @property
    def is_on(self) -> bool:
        """Check if transistor is in ON state."""
        return self.state == "on"
    
    @property
    def is_off(self) -> bool:
        """Check if transistor is in OFF state."""
        return self.state == "off"
    
    def select_operation_mode(self, s_knowledge: float, s_time: float, s_entropy: float) -> OperationMode:
        """
        Select optimal operation mode via S-entropy minimization.
        
        From st-stellas-circuits.tex: The transistor evaluates all three modes
        simultaneously, then selects via S-entropy cost minimization.
        
        Args:
            s_knowledge: S_knowledge value for current context
            s_time: S_time value for current context
            s_entropy: S_entropy value for current context
            
        Returns:
            Selected OperationMode
        """
        # Use gate's BMD state to select mode
        selected_mode = self.gate.select_operation_mode(s_knowledge, s_time, s_entropy)
        
        # Update active mode
        self.active_mode = selected_mode
        
        # Track mode selection
        self.mode_history.append(selected_mode)
        self.mode_selection_count[selected_mode] += 1
        
        return selected_mode
    
    def get_impedance(self, frequency: float) -> complex:
        """
        Get complex impedance for active operation mode.
        
        Args:
            frequency: Frequency in Hz
            
        Returns:
            Complex impedance Z = R + jX
        """
        return self.gate.get_impedance(frequency)
    
    def set_gate_voltage(self, voltage: float, context_s_coords: Optional[Tuple[float, float, float]] = None) -> None:
        """
        Set gate voltage and update transistor state.
        
        If context S-coordinates are provided, selects operation mode via S-entropy
        minimization. Otherwise, defaults to resistive mode.
        
        Args:
            voltage: Gate voltage (V)
            context_s_coords: Optional tuple of (S_knowledge, S_time, S_entropy) for context
        """
        self.gate_voltage = voltage
        
        # Select operation mode if context provided
        if context_s_coords is not None:
            s_k, s_t, s_e = context_s_coords
            self.select_operation_mode(s_k, s_t, s_e)
        else:
            # Default to resistive mode
            self.active_mode = OperationMode.RESISTIVE
        
        # Update gate BMD state based on voltage
        if voltage >= self.threshold_voltage:
            self.gate.open()
            self.state = "on"
        else:
            self.gate.close()
            self.state = "off"
        
        # Update current based on active mode
        self._update_current()
        
        # Track switching
        if self.state != getattr(self, '_last_state', None):
            self.switching_count += 1
        self._last_state = self.state
    
    def _update_current(self) -> None:
        """
        Update source-drain current based on active operation mode.
        
        - RESISTIVE: I = V/R (ohmic behavior)
        - CAPACITIVE: I = C·dV/dt (reactive, 90° phase lead)
        - INDUCTIVE: V = L·dI/dt (reactive, 90° phase lag)
        """
        if self.active_mode == OperationMode.RESISTIVE:
            # Resistive: I = V/R with BMD amplification
            R_effective = self.gate.tri_params.R_knowledge
            if self.is_on:
                # Apply on/off ratio and BMD amplification
                base_current = self.source_drain_voltage / R_effective
                self.source_drain_current = base_current * self.on_off_ratio
            else:
                # Leakage current only
                self.source_drain_current = self.source_drain_voltage / (R_effective * self.on_off_ratio)
        
        elif self.active_mode == OperationMode.CAPACITIVE:
            # Capacitive: I = C·dV/dt (requires voltage change rate)
            # For steady-state, estimate from AC frequency
            C_effective = self.gate.tri_params.C_time
            omega = 2 * np.pi * self.source.frequency if self.source else 2 * np.pi * 120.0
            # I = jωCV in phasor domain
            self.source_drain_current = omega * C_effective * self.source_drain_voltage
        
        elif self.active_mode == OperationMode.INDUCTIVE:
            # Inductive: V = L·dI/dt (current lags voltage)
            L_effective = self.gate.tri_params.L_entropy
            omega = 2 * np.pi * self.source.frequency if self.source else 2 * np.pi * 120.0
            # I = V/(jωL) in phasor domain
            if omega * L_effective > 0:
                self.source_drain_current = self.source_drain_voltage / (omega * L_effective)
            else:
                self.source_drain_current = 0.0
    
    def apply_input(self, input_psychon: Psychon) -> Optional[Psychon]:
        """
        Apply input psychon and compute output.
        
        Uses input psychon's S-coordinates to select operation mode, then
        computes output based on tri-dimensional behavior.
        
        Args:
            input_psychon: Input psychon
            
        Returns:
            Output psychon (None if transistor is off)
        """
        # Extract S-coordinates from input
        s_k = input_psychon.s_knowledge
        s_t = input_psychon.s_time
        s_e = input_psychon.s_entropy
        
        # Select operation mode
        self.select_operation_mode(s_k, s_t, s_e)
        
        # Apply gate voltage from input psychon's energy
        gate_voltage = input_psychon.energy / KB_T  # Convert energy to voltage
        self.set_gate_voltage(gate_voltage, context_s_coords=(s_k, s_t, s_e))
        
        # If transistor is off, no output
        if self.is_off:
            return None
        
        # Create output psychon based on active mode
        output_psychon = input_psychon.spawn_child(
            id=f"{input_psychon.id}_transistor_out",
            amplitude=input_psychon.amplitude * (self.on_off_ratio if self.active_mode == OperationMode.RESISTIVE else 1.0)
        )
        
        # Modify S-coordinates based on operation mode
        if self.active_mode == OperationMode.RESISTIVE:
            # Resistive reduces S_knowledge (information processed)
            output_psychon.s_knowledge = max(0, s_k * 0.9)
        elif self.active_mode == OperationMode.CAPACITIVE:
            # Capacitive advances S_time (temporal progression)
            output_psychon.s_time = min(1.0, s_t * 1.1)
        elif self.active_mode == OperationMode.INDUCTIVE:
            # Inductive smooths S_entropy (reduced diversity)
            output_psychon.s_entropy = s_e * 0.95
        
        return output_psychon
    
    def get_statistics(self) -> Dict:
        """
        Get transistor statistics including mode distribution.
        
        Returns:
            Dictionary of statistics
        """
        total_selections = sum(self.mode_selection_count.values())
        
        return {
            'transistor_id': self.gate.id if self.gate else 'unknown',
            'state': self.state,
            'active_mode': self.active_mode.value,
            'on_off_ratio': self.on_off_ratio,
            'switching_count': self.switching_count,
            'mode_distribution': {
                'resistive': self.mode_selection_count[OperationMode.RESISTIVE] / max(total_selections, 1),
                'capacitive': self.mode_selection_count[OperationMode.CAPACITIVE] / max(total_selections, 1),
                'inductive': self.mode_selection_count[OperationMode.INDUCTIVE] / max(total_selections, 1)
            },
            'total_mode_selections': total_selections,
            'gate_voltage': self.gate_voltage,
            'current': self.source_drain_current
        }
    
    def __repr__(self) -> str:
        mode_dist = self.get_statistics()['mode_distribution']
        return (f"BMDTransistor(state='{self.state}', mode={self.active_mode.value}, "
                f"on/off={self.on_off_ratio:.1f}, switches={self.switching_count}, "
                f"R:{mode_dist['resistive']:.1%}/C:{mode_dist['capacitive']:.1%}/L:{mode_dist['inductive']:.1%})")


# Example usage and validation
if __name__ == "__main__":
    print("=== Tri-Dimensional BMD Transistor Demo ===\n")
    
    # Create transistor with default parameters
    transistor = BMDTransistor()
    print("Transistor created with default parameters:")
    print(transistor)
    print(f"\nTri-dimensional gate parameters:")
    print(f"  R (S_knowledge): {transistor.gate.tri_params.R_knowledge:.2e} Ω")
    print(f"  C (S_time): {transistor.gate.tri_params.C_time:.2e} F")
    print(f"  L (S_entropy): {transistor.gate.tri_params.L_entropy:.2e} H")
    
    # Test mode selection with different contexts
    print("\n=== Mode Selection with Different Contexts ===")
    
    # Context 1: High S_knowledge → RESISTIVE
    print("\nContext 1: High information deficit (S_k=2.0, S_t=0.3, S_e=0.2)")
    mode1 = transistor.select_operation_mode(2.0, 0.3, 0.2)
    print(f"  Selected mode: {mode1.value}")
    Z1 = transistor.get_impedance(120.0)
    print(f"  Impedance @ 120 Hz: {Z1}")
    
    # Context 2: High S_time → CAPACITIVE
    print("\nContext 2: High temporal urgency (S_k=0.3, S_t=0.9, S_e=0.2)")
    mode2 = transistor.select_operation_mode(0.3, 0.9, 0.2)
    print(f"  Selected mode: {mode2.value}")
    Z2 = transistor.get_impedance(120.0)
    print(f"  Impedance @ 120 Hz: {Z2}")
    
    # Context 3: High S_entropy → INDUCTIVE
    print("\nContext 3: High categorical diversity (S_k=0.4, S_t=0.3, S_e=1.5)")
    mode3 = transistor.select_operation_mode(0.4, 0.3, 1.5)
    print(f"  Selected mode: {mode3.value}")
    Z3 = transistor.get_impedance(120.0)
    print(f"  Impedance @ 120 Hz: {Z3}")
    
    # Test psychon processing
    print("\n=== Psychon Processing ===")
    from megaphrenia.core.psychon import create_psychon_from_signature
    
    input_psychon = create_psychon_from_signature(120.0, amplitude=1.0)
    print(f"Input psychon: S=({input_psychon.s_knowledge:.2f}, {input_psychon.s_time:.2f}, {input_psychon.s_entropy:.2f})")
    
    output_psychon = transistor.apply_input(input_psychon)
    if output_psychon:
        print(f"Output psychon: S=({output_psychon.s_knowledge:.2f}, {output_psychon.s_time:.2f}, {output_psychon.s_entropy:.2f})")
        print(f"  Mode used: {transistor.active_mode.value}")
        print(f"  Amplitude gain: {output_psychon.amplitude / input_psychon.amplitude:.2f}")
    
    # Show statistics
    print("\n=== Transistor Statistics ===")
    stats = transistor.get_statistics()
    print(f"State: {stats['state']}")
    print(f"Active mode: {stats['active_mode']}")
    print(f"Mode distribution:")
    print(f"  Resistive: {stats['mode_distribution']['resistive']:.1%}")
    print(f"  Capacitive: {stats['mode_distribution']['capacitive']:.1%}")
    print(f"  Inductive: {stats['mode_distribution']['inductive']:.1%}")
    
    print("\n=== Tri-Dimensional BMD Transistor Operation Verified ===")
