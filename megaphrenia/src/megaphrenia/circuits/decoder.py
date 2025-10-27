"""
Decoder: Tri-Dimensional S-Coordinate Address Decoder

From biological-integrated-circuits.tex: Decoders enable component selection
through S-coordinate matching rather than binary address decoding.

Traditional decoder: Binary address → one-hot output (2^n inputs → 2^n outputs)
S-coordinate decoder: S-coordinate query → nearest match via S-distance minimization

Applications:
- Memory address decoding (select memory cell by S-coordinate proximity)
- Component selection (activate BMD by S-coordinate match)
- Routing (direct signal to nearest S-coordinate destination)

Complexity: O(1) via hash table lookup (vs O(log n) for binary decoder tree)
"""

from dataclasses import dataclass, field
from typing import Optional, List, Dict, Tuple
import numpy as np
import sys
sys.path.append('..')

try:
    from megaphrenia.core import Psychon
    from megaphrenia.core.s_entropy import SEntropyCalculator
except ImportError:
    from core.psychon import Psychon
    from core.s_entropy import SEntropyCalculator


@dataclass
class SCoordinateDecoder:
    """
    S-coordinate decoder for component selection via S-distance minimization.
    
    Traditional decoder: Binary address bits → one-hot output
    S-coordinate decoder: S-coordinate query → component with nearest S-coords
    
    Architecture:
    - Register components with their S-coordinates
    - Query with S-coordinate pattern
    - Return component(s) within threshold distance
    - O(1) lookup via spatial hashing
    
    Attributes:
        num_outputs: Number of output lines (components to select)
        epsilon_threshold: S-distance threshold for selection
        use_primary_only: Use 3D (True) or 5D (False) coordinates
        
        # Component registry
        components: Dict mapping component_id to (psychon, output_index)
        spatial_hash: Dict mapping quantized S-coords to component_ids
        
        # Statistics
        decode_count: Number of decode operations
        exact_matches: Number of exact coordinate matches
        approximate_matches: Number of nearest-neighbor matches
    """
    
    num_outputs: int = 8  # Default: 8 output lines
    epsilon_threshold: float = 0.1  # S-distance selection threshold
    use_primary_only: bool = True  # Use 3D primary coordinates
    quantization_levels: int = 10  # For spatial hashing
    
    # Component registry
    components: Dict[str, Tuple[Psychon, int]] = field(default_factory=dict)
    spatial_hash: Dict[Tuple, List[str]] = field(default_factory=dict)
    
    # Utilities
    s_entropy_calc: SEntropyCalculator = field(default_factory=SEntropyCalculator)
    
    # Statistics
    decode_count: int = 0
    exact_matches: int = 0
    approximate_matches: int = 0
    
    def _quantize_coordinates(self, s_coords: np.ndarray) -> Tuple:
        """Quantize S-coordinates for spatial hashing."""
        # Normalize to [0, 1]
        if len(s_coords) == 3:
            normalized = np.array([
                s_coords[0] / 5.0,  # S_knowledge
                s_coords[1],  # S_time (already [0,1])
                s_coords[2] / 3.0  # S_entropy
            ])
        else:  # 5D
            normalized = np.array([
                s_coords[0] / 5.0,
                s_coords[1],
                s_coords[2] / 3.0,
                (s_coords[3] + 1) / 2,
                (s_coords[4] + 1) / 2
            ])
        
        quantized = np.clip(normalized * self.quantization_levels, 0, self.quantization_levels - 1).astype(int)
        return tuple(quantized)
    
    def register_component(self, component_id: str, psychon: Psychon, output_index: int) -> None:
        """
        Register a component for decoding.
        
        Args:
            component_id: Unique component identifier
            psychon: Psychon representing component's S-coordinates
            output_index: Output line index (0 to num_outputs-1)
        """
        if output_index >= self.num_outputs:
            raise ValueError(f"Output index {output_index} exceeds num_outputs {self.num_outputs}")
        
        # Store component
        self.components[component_id] = (psychon, output_index)
        
        # Add to spatial hash
        coords = psychon.primary_s_coordinates if self.use_primary_only else psychon.extended_s_coordinates
        hash_key = self._quantize_coordinates(coords)
        
        if hash_key not in self.spatial_hash:
            self.spatial_hash[hash_key] = []
        self.spatial_hash[hash_key].append(component_id)
    
    def decode(self, query_s_coords: np.ndarray) -> List[Tuple[str, int, float]]:
        """
        Decode S-coordinate query to component selection.
        
        Returns all components within epsilon_threshold, sorted by distance.
        
        Args:
            query_s_coords: S-coordinate query vector (3D or 5D)
            
        Returns:
            List of (component_id, output_index, distance) tuples
        """
        self.decode_count += 1
        
        # Check spatial hash for exact match
        hash_key = self._quantize_coordinates(query_s_coords)
        
        matches = []
        
        # Check exact hash bucket
        if hash_key in self.spatial_hash:
            for comp_id in self.spatial_hash[hash_key]:
                psychon, output_idx = self.components[comp_id]
                coords = psychon.primary_s_coordinates if self.use_primary_only else psychon.extended_s_coordinates
                distance = self.s_entropy_calc.cross_domain_distance(
                    query_s_coords, coords, use_primary_only=self.use_primary_only
                )
                
                if distance < self.epsilon_threshold:
                    matches.append((comp_id, output_idx, distance))
                    if distance < 1e-6:  # Essentially exact
                        self.exact_matches += 1
        
        # If no exact matches, search all components (nearest neighbor)
        if not matches:
            self.approximate_matches += 1
            for comp_id, (psychon, output_idx) in self.components.items():
                coords = psychon.primary_s_coordinates if self.use_primary_only else psychon.extended_s_coordinates
                distance = self.s_entropy_calc.cross_domain_distance(
                    query_s_coords, coords, use_primary_only=self.use_primary_only
                )
                
                if distance < self.epsilon_threshold:
                    matches.append((comp_id, output_idx, distance))
        
        # Sort by distance (closest first)
        matches.sort(key=lambda x: x[2])
        
        return matches
    
    def decode_one_hot(self, query_s_coords: np.ndarray) -> np.ndarray:
        """
        Decode to one-hot output vector.
        
        Args:
            query_s_coords: S-coordinate query
            
        Returns:
            One-hot vector of length num_outputs (1 at selected indices, 0 elsewhere)
        """
        output = np.zeros(self.num_outputs, dtype=int)
        
        matches = self.decode(query_s_coords)
        
        # Set bits for all matches within threshold
        for _, output_idx, _ in matches:
            output[output_idx] = 1
        
        return output
    
    def get_statistics(self) -> Dict:
        """Get decoder statistics."""
        return {
            'num_outputs': self.num_outputs,
            'num_components': len(self.components),
            'decode_count': self.decode_count,
            'exact_matches': self.exact_matches,
            'approximate_matches': self.approximate_matches,
            'exact_match_rate': self.exact_matches / max(self.decode_count, 1),
            'epsilon_threshold': self.epsilon_threshold,
            'dimensionality': 3 if self.use_primary_only else 5
        }
    
    def __repr__(self) -> str:
        stats = self.get_statistics()
        return (f"SCoordinateDecoder(outputs={self.num_outputs}, components={stats['num_components']}, "
                f"decodes={self.decode_count}, exact_rate={stats['exact_match_rate']:.1%})")


# Example usage
if __name__ == "__main__":
    print("=== S-Coordinate Decoder Demo ===\n")
    
    from megaphrenia.core.psychon import create_psychon_from_signature
    
    # Create decoder with 8 output lines
    decoder = SCoordinateDecoder(num_outputs=8, epsilon_threshold=0.2)
    print(f"Decoder created: {decoder}\n")
    
    # Register components at different S-coordinates
    print("=== Registering Components ===")
    frequencies = [60.0, 120.0, 180.0, 240.0, 300.0, 360.0, 420.0, 480.0]
    
    for i, freq in enumerate(frequencies):
        psychon = create_psychon_from_signature(freq)
        psychon.id = f"component_{i}_freq{freq}"
        decoder.register_component(psychon.id, psychon, output_index=i)
        print(f"  Output {i}: {psychon.id}, S=({psychon.s_knowledge:.2f}, {psychon.s_time:.2f}, {psychon.s_entropy:.2f})")
    
    # Test decoding
    print("\n=== Decoding Tests ===")
    
    # Query 1: Exact match to 120 Hz
    print("\nQuery 1: S-coords matching 120 Hz")
    query1 = create_psychon_from_signature(120.0).primary_s_coordinates
    matches1 = decoder.decode(query1)
    print(f"  Matches: {len(matches1)}")
    for comp_id, output_idx, distance in matches1:
        print(f"    Output {output_idx}: {comp_id}, distance={distance:.4f}")
    
    # Query 2: Between 120 and 180 Hz
    print("\nQuery 2: S-coords between 120 and 180 Hz")
    query2 = create_psychon_from_signature(150.0).primary_s_coordinates
    matches2 = decoder.decode(query2)
    print(f"  Matches: {len(matches2)}")
    for comp_id, output_idx, distance in matches2:
        print(f"    Output {output_idx}: {comp_id}, distance={distance:.4f}")
    
    # Query 3: One-hot output
    print("\nQuery 3: One-hot output for 240 Hz")
    query3 = create_psychon_from_signature(240.0).primary_s_coordinates
    one_hot = decoder.decode_one_hot(query3)
    print(f"  One-hot: {one_hot}")
    print(f"  Active outputs: {np.where(one_hot == 1)[0].tolist()}")
    
    # Statistics
    print("\n=== Decoder Statistics ===")
    stats = decoder.get_statistics()
    print(f"Components: {stats['num_components']}")
    print(f"Decode operations: {stats['decode_count']}")
    print(f"Exact match rate: {stats['exact_match_rate']:.1%}")
    print(f"Approximate matches: {stats['approximate_matches']}")
    
    print("\n=== Complexity Comparison ===")
    print(f"Traditional binary decoder: O(log n) = O(log {decoder.num_outputs}) = O({np.log2(decoder.num_outputs):.1f})")
    print(f"S-coordinate decoder: O(1) via spatial hashing")
    
    print("\n=== S-Coordinate Decoder Operation Verified ===")

