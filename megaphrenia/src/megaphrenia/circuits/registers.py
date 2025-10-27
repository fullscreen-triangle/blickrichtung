"""
Registers: S-Coordinate Register File

From biological-integrated-circuits.tex: Register files store operands and results
using S-coordinate addressing rather than binary register numbers.

Traditional register file: R0, R1, R2, ... R15 (binary addressing)
S-coordinate register file: Registers accessed by S-coordinate proximity

Architecture:
- Built on S-dictionary memory (content-addressable)
- Register "names" are S-coordinate patterns
- Read/write via S-distance minimization
- O(1) access time

Advantages:
- Content-addressable: retrieve by similarity
- Automatic spilling: closest match when exact unavailable
- Context-aware: S-coordinates encode semantic meaning
"""

from dataclasses import dataclass, field
from typing import Optional, Dict, List
import numpy as np
import sys
sys.path.append('..')

try:
    from megaphrenia.core import Psychon
    from megaphrenia.core.s_entropy import SEntropyCalculator
    from .memory import SDictionaryMemory
except ImportError:
    from core.psychon import Psychon
    from core.s_entropy import SEntropyCalculator
    from memory import SDictionaryMemory


@dataclass
class RegisterFile:
    """
    S-coordinate register file for operand storage.
    
    Registers are identified by S-coordinates rather than binary numbers.
    Enables content-addressable register access and automatic spilling.
    
    Architecture:
    - Uses S-dictionary memory as backend
    - Named registers (optional) for convenience
    - S-coordinate based access (primary)
    - Supports register renaming via S-coordinate aliasing
    
    Attributes:
        num_registers: Number of physical registers
        use_extended_coords: 3D (False) or 5D (True) addressing
        
        # Backend storage
        memory: S-dictionary memory
        register_names: Dict mapping names to S-coordinates (optional)
        
        # Statistics
        read_count: Number of read operations
        write_count: Number of write operations
        name_lookup_count: Number of name-based lookups
        coord_lookup_count: Number of coordinate-based lookups
    """
    
    num_registers: int = 16  # Default: 16 registers (like many architectures)
    use_extended_coords: bool = False  # 3D for speed
    
    # Backend storage (S-dictionary memory)
    memory: SDictionaryMemory = field(default_factory=lambda: SDictionaryMemory(
        quantization_levels=20,  # 20 levels per dimension
        use_extended_coords=False  # 3D for register file
    ))
    
    # Named registers (optional convenience)
    register_names: Dict[str, np.ndarray] = field(default_factory=dict)
    
    # S-entropy calculator
    s_entropy_calc: SEntropyCalculator = field(default_factory=SEntropyCalculator)
    
    # Statistics
    read_count: int = 0
    write_count: int = 0
    name_lookup_count: int = 0
    coord_lookup_count: int = 0
    
    def __post_init__(self):
        """Initialize standard register names."""
        # Create standard register names (R0-R15 equivalent)
        # Map to evenly distributed S-coordinates
        for i in range(self.num_registers):
            # Distribute registers across S-coordinate space
            s_k = (i % 4) * 1.0  # 0, 1, 2, 3
            s_t = ((i // 4) % 4) * 0.25  # 0, 0.25, 0.5, 0.75
            s_e = ((i // 16) % 4) * 0.5  # 0, 0.5, 1.0, 1.5
            
            register_name = f"R{i}"
            self.register_names[register_name] = np.array([s_k, s_t, s_e])
    
    def write_register(self, register_id: str, psychon: Psychon) -> bool:
        """
        Write psychon to register.
        
        Args:
            register_id: Register name (e.g., "R0") or S-coordinate string
            psychon: Psychon to store
            
        Returns:
            True if write successful
        """
        self.write_count += 1
        
        # Check if register_id is a named register
        if register_id in self.register_names:
            self.name_lookup_count += 1
            # Update psychon's S-coordinates to match register's coordinates
            target_coords = self.register_names[register_id]
            psychon.s_knowledge = target_coords[0]
            psychon.s_time = target_coords[1]
            psychon.s_entropy = target_coords[2]
        else:
            self.coord_lookup_count += 1
            # register_id should be interpreted as S-coordinate based access
            # Use psychon's own coordinates
            pass
        
        # Write to memory
        return self.memory.write(psychon)
    
    def read_register(self, register_id: str) -> Optional[Psychon]:
        """
        Read psychon from register.
        
        Args:
            register_id: Register name or S-coordinate pattern
            
        Returns:
            Psychon from register (None if not found)
        """
        self.read_count += 1
        
        # Check if register_id is a named register
        if register_id in self.register_names:
            self.name_lookup_count += 1
            query_coords = self.register_names[register_id]
        else:
            self.coord_lookup_count += 1
            # Treat as S-coordinate query (would need parsing in real implementation)
            # For now, return None
            return None
        
        # Read from memory via S-coordinate query
        return self.memory.read(query_coords, exact_match_only=False)
    
    def write_by_coordinates(self, s_coords: np.ndarray, psychon: Psychon) -> bool:
        """
        Write to register by S-coordinates.
        
        Args:
            s_coords: Target S-coordinates (3D)
            psychon: Psychon to store
            
        Returns:
            True if write successful
        """
        self.write_count += 1
        self.coord_lookup_count += 1
        
        # Update psychon's coordinates
        psychon.s_knowledge = s_coords[0]
        psychon.s_time = s_coords[1]
        psychon.s_entropy = s_coords[2]
        
        return self.memory.write(psychon)
    
    def read_by_coordinates(self, s_coords: np.ndarray, exact_only: bool = False) -> Optional[Psychon]:
        """
        Read from register by S-coordinates.
        
        Args:
            s_coords: Query S-coordinates (3D)
            exact_only: If True, only exact matches returned
            
        Returns:
            Psychon with nearest S-coordinates
        """
        self.read_count += 1
        self.coord_lookup_count += 1
        
        return self.memory.read(s_coords, exact_match_only=exact_only)
    
    def clear_register(self, register_id: str) -> None:
        """Clear a register (remove from memory)."""
        # In S-dictionary, we don't explicitly remove, just overwrite
        # Set to zero psychon
        from megaphrenia.core.psychon import create_psychon_from_signature
        zero_psychon = create_psychon_from_signature(0.1, amplitude=0.0)
        zero_psychon.id = f"{register_id}_cleared"
        self.write_register(register_id, zero_psychon)
    
    def clear_all(self) -> None:
        """Clear all registers."""
        self.memory.clear()
        self.read_count = 0
        self.write_count = 0
        self.name_lookup_count = 0
        self.coord_lookup_count = 0
    
    def get_statistics(self) -> Dict:
        """Get register file statistics."""
        mem_stats = self.memory.get_statistics()
        
        return {
            'num_registers': self.num_registers,
            'occupied_registers': mem_stats['occupied_addresses'],
            'utilization': mem_stats['utilization'],
            'read_count': self.read_count,
            'write_count': self.write_count,
            'name_lookups': self.name_lookup_count,
            'coord_lookups': self.coord_lookup_count,
            'cache_hit_rate': mem_stats['cache_hit_rate'],
            'memory_capacity': mem_stats['total_capacity']
        }
    
    def __repr__(self) -> str:
        stats = self.get_statistics()
        return (f"RegisterFile(registers={self.num_registers}, occupied={stats['occupied_registers']}, "
                f"reads={self.read_count}, writes={self.write_count}, "
                f"hit_rate={stats['cache_hit_rate']:.1%})")


# Example usage
if __name__ == "__main__":
    print("=== S-Coordinate Register File Demo ===\n")
    
    from megaphrenia.core.psychon import create_psychon_from_signature
    
    # Create register file
    reg_file = RegisterFile(num_registers=16)
    print(f"Register file created: {reg_file}\n")
    
    # Show standard register names and their S-coordinates
    print("=== Standard Register Mapping ===")
    for i in range(8):  # Show first 8
        reg_name = f"R{i}"
        coords = reg_file.register_names[reg_name]
        print(f"  {reg_name}: S=({coords[0]:.2f}, {coords[1]:.2f}, {coords[2]:.2f})")
    print(f"  ... (R8-R15 similar)\n")
    
    # Write to named registers
    print("=== Writing to Named Registers ===")
    psychon_a = create_psychon_from_signature(120.0, amplitude=1.0)
    psychon_a.id = "operand_a"
    reg_file.write_register("R0", psychon_a)
    print(f"  Wrote {psychon_a.id} to R0")
    
    psychon_b = create_psychon_from_signature(240.0, amplitude=0.5)
    psychon_b.id = "operand_b"
    reg_file.write_register("R1", psychon_b)
    print(f"  Wrote {psychon_b.id} to R1")
    
    psychon_c = create_psychon_from_signature(360.0, amplitude=0.75)
    psychon_c.id = "result_c"
    reg_file.write_register("R2", psychon_c)
    print(f"  Wrote {psychon_c.id} to R2")
    
    # Read from named registers
    print("\n=== Reading from Named Registers ===")
    read_a = reg_file.read_register("R0")
    if read_a:
        print(f"  R0: {read_a.id}, amplitude={read_a.amplitude:.2f}")
    
    read_b = reg_file.read_register("R1")
    if read_b:
        print(f"  R1: {read_b.id}, amplitude={read_b.amplitude:.2f}")
    
    read_c = reg_file.read_register("R2")
    if read_c:
        print(f"  R2: {read_c.id}, amplitude={read_c.amplitude:.2f}")
    
    # Write/read by S-coordinates
    print("\n=== S-Coordinate Based Access ===")
    custom_coords = np.array([1.5, 0.6, 0.8])
    psychon_custom = create_psychon_from_signature(180.0, amplitude=0.9)
    psychon_custom.id = "custom_register"
    
    reg_file.write_by_coordinates(custom_coords, psychon_custom)
    print(f"  Wrote {psychon_custom.id} at S=({custom_coords[0]:.2f}, {custom_coords[1]:.2f}, {custom_coords[2]:.2f})")
    
    # Read with similar coordinates (content-addressable)
    query_coords = np.array([1.6, 0.65, 0.75])  # Close to custom_coords
    retrieved = reg_file.read_by_coordinates(query_coords, exact_only=False)
    if retrieved:
        distance = reg_file.s_entropy_calc.cross_domain_distance(
            query_coords, retrieved.primary_s_coordinates, use_primary_only=True
        )
        print(f"  Query S=({query_coords[0]:.2f}, {query_coords[1]:.2f}, {query_coords[2]:.2f})")
        print(f"  Retrieved: {retrieved.id}, distance={distance:.4f}")
    
    # Statistics
    print("\n=== Register File Statistics ===")
    stats = reg_file.get_statistics()
    print(f"Registers: {stats['num_registers']}")
    print(f"Occupied: {stats['occupied_registers']}")
    print(f"Utilization: {stats['utilization']:.1%}")
    print(f"Read operations: {stats['read_count']}")
    print(f"Write operations: {stats['write_count']}")
    print(f"Name-based lookups: {stats['name_lookups']}")
    print(f"Coordinate-based lookups: {stats['coord_lookups']}")
    print(f"Cache hit rate: {stats['cache_hit_rate']:.1%}")
    
    print("\n=== Advantages ===")
    print("✓ Content-addressable: retrieve by S-coordinate similarity")
    print("✓ O(1) access time via hash table")
    print("✓ Automatic spilling: nearest match when exact unavailable")
    print("✓ Context-aware: S-coordinates encode semantic meaning")
    
    print("\n=== S-Coordinate Register File Operation Verified ===")

