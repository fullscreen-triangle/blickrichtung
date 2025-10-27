"""
Harmonic Network Graph: Multi-Path Validation via Graph Redundancy

Builds harmonic network graphs where nodes are observation states and edges
are shared harmonic frequencies, enabling multi-path validation.

Based on Harmonic Network Graph theory (molecular-gas-harmonic-timekeeping.tex
lines 786-930):
    - Nodes: (component, frequency, recursion level)
    - Edges: shared harmonic frequencies
    - Enhancement: F_graph ≈ 100× via redundancy × amplification × topology
"""

import numpy as np
from dataclasses import dataclass, field
from typing import List, Dict, Set, Tuple, Optional
from collections import defaultdict
import sys
sys.path.append('../..')

try:
    from megaphrenia.core.psychon import Psychon
    from megaphrenia.integration.harmonic_analysis import HarmonicSignature, MultiDomainHarmonics
except ImportError:
    from core.psychon import Psychon
    from harmonic_analysis import HarmonicSignature, MultiDomainHarmonics


@dataclass
class HarmonicNode:
    """
    Node in harmonic network graph.
    
    Represents an observation state: (component, frequency, recursion level)
    
    Attributes:
        id: Unique node identifier
        component: Circuit component (e.g., "BMD_A", "XOR_gate")
        frequency: Fundamental frequency (Hz)
        recursion_level: Depth of recursive observation
        s_coordinates: S-entropy coordinates
        harmonics: Harmonic amplitudes
        betweenness_centrality: Hub importance metric
    """
    id: str
    component: str
    frequency: float
    recursion_level: int
    s_coordinates: np.ndarray
    harmonics: np.ndarray = field(default_factory=lambda: np.array([]))
    betweenness_centrality: float = 0.0
    
    def __hash__(self):
        return hash(self.id)
    
    def __eq__(self, other):
        if isinstance(other, HarmonicNode):
            return self.id == other.id
        return False


@dataclass
class HarmonicEdge:
    """
    Edge in harmonic network graph.
    
    Represents shared harmonic frequency between two nodes.
    
    Attributes:
        source: Source node ID
        target: Target node ID
        shared_frequency: Frequency at which harmonics coincide
        harmonic_orders: (n, m) where n×ω_source ≈ m×ω_target
        weight: Edge strength (coupling coefficient)
    """
    source: str
    target: str
    shared_frequency: float
    harmonic_orders: Tuple[int, int]
    weight: float = 1.0


class HarmonicNetworkGraph:
    """
    Network graph of harmonic observations.
    
    From Principle (Harmonic Network Convergence):
        When harmonics from different paths coincide, they create graph edges
        rather than separate tree branches, enabling multi-path validation.
    """
    
    def __init__(self, tolerance: float = 1e-3):
        """
        Initialize harmonic network.
        
        Args:
            tolerance: Frequency matching tolerance (relative)
        """
        self.nodes: Dict[str, HarmonicNode] = {}
        self.edges: List[HarmonicEdge] = []
        self.adjacency: Dict[str, Set[str]] = defaultdict(set)
        self.tolerance = tolerance
    
    def add_node(self, node: HarmonicNode):
        """Add node to graph."""
        self.nodes[node.id] = node
        if node.id not in self.adjacency:
            self.adjacency[node.id] = set()
    
    def add_edge(self, edge: HarmonicEdge):
        """Add edge to graph."""
        self.edges.append(edge)
        self.adjacency[edge.source].add(edge.target)
        self.adjacency[edge.target].add(edge.source)
    
    def find_harmonic_coincidences(self, max_harmonic: int = 10):
        """
        Find all harmonic coincidences and create edges.
        
        From Principle: If |nω_A - mω_B| < ε, nodes A and B are connected.
        
        Args:
            max_harmonic: Maximum harmonic order to check
        """
        node_list = list(self.nodes.values())
        
        for i, node_a in enumerate(node_list):
            for node_b in node_list[i+1:]:
                # Check all harmonic combinations
                for n in range(1, max_harmonic + 1):
                    for m in range(1, max_harmonic + 1):
                        freq_a = n * node_a.frequency
                        freq_b = m * node_b.frequency
                        
                        # Check if harmonics coincide
                        rel_diff = abs(freq_a - freq_b) / max(freq_a, freq_b)
                        
                        if rel_diff < self.tolerance:
                            # Create edge
                            edge = HarmonicEdge(
                                source=node_a.id,
                                target=node_b.id,
                                shared_frequency=(freq_a + freq_b) / 2,
                                harmonic_orders=(n, m),
                                weight=1.0 / (n * m)  # Lower harmonics → stronger
                            )
                            self.add_edge(edge)
    
    def find_all_paths(
        self,
        source_id: str,
        target_id: str,
        max_length: int = 10
    ) -> List[List[str]]:
        """
        Find all paths from source to target.
        
        Uses BFS to find all simple paths (no cycles).
        
        Args:
            source_id: Starting node
            target_id: Ending node
            max_length: Maximum path length
            
        Returns:
            List of paths (each path is list of node IDs)
        """
        if source_id not in self.nodes or target_id not in self.nodes:
            return []
        
        all_paths = []
        queue = [(source_id, [source_id])]
        
        while queue:
            current, path = queue.pop(0)
            
            if len(path) > max_length:
                continue
            
            if current == target_id:
                all_paths.append(path)
                continue
            
            for neighbor in self.adjacency[current]:
                if neighbor not in path:  # Avoid cycles
                    queue.append((neighbor, path + [neighbor]))
        
        return all_paths
    
    def find_shortest_paths(
        self,
        source_id: str,
        target_id: str
    ) -> List[List[str]]:
        """
        Find all shortest paths from source to target.
        
        Returns:
            List of shortest paths
        """
        all_paths = self.find_all_paths(source_id, target_id)
        
        if not all_paths:
            return []
        
        # Find minimum length
        min_length = min(len(p) for p in all_paths)
        
        # Return all paths of minimum length
        return [p for p in all_paths if len(p) == min_length]
    
    def calculate_betweenness_centrality(self):
        """
        Calculate betweenness centrality for all nodes.
        
        From Definition (Betweenness Centrality):
            C_B(v) = Σ σ_st(v) / σ_st
        
        High-centrality nodes are "precision hubs".
        """
        node_ids = list(self.nodes.keys())
        centrality = {node_id: 0.0 for node_id in node_ids}
        
        # For each pair of nodes
        for i, source in enumerate(node_ids):
            for target in node_ids[i+1:]:
                if source == target:
                    continue
                
                # Find all shortest paths
                paths = self.find_shortest_paths(source, target)
                
                if not paths:
                    continue
                
                total_paths = len(paths)
                
                # Count how many pass through each node
                for node_id in node_ids:
                    if node_id == source or node_id == target:
                        continue
                    
                    paths_through = sum(1 for p in paths if node_id in p)
                    centrality[node_id] += paths_through / total_paths
        
        # Normalize
        n = len(node_ids)
        if n > 2:
            normalization = 2.0 / ((n - 1) * (n - 2))
            centrality = {k: v * normalization for k, v in centrality.items()}
        
        # Update nodes
        for node_id, c_value in centrality.items():
            self.nodes[node_id].betweenness_centrality = c_value
        
        return centrality
    
    def identify_precision_hubs(self, top_k: int = 5) -> List[HarmonicNode]:
        """
        Identify precision hubs (high betweenness centrality nodes).
        
        From Definition: High-centrality nodes provide precision hubs where
        multiple observation paths converge, creating resonant amplification.
        
        Args:
            top_k: Number of top hubs to return
            
        Returns:
            List of hub nodes, sorted by centrality (descending)
        """
        # Ensure centrality is calculated
        if all(n.betweenness_centrality == 0.0 for n in self.nodes.values()):
            self.calculate_betweenness_centrality()
        
        # Sort by centrality
        sorted_nodes = sorted(
            self.nodes.values(),
            key=lambda n: n.betweenness_centrality,
            reverse=True
        )
        
        return sorted_nodes[:top_k]
    
    def calculate_enhancement_factor(self) -> float:
        """
        Calculate graph enhancement factor.
        
        From Theorem (Graph Enhancement Factor):
            F_graph = F_redundancy × F_amplification × F_topology
        
        where:
            F_redundancy = <k> (average node degree)
            F_amplification = √k_max (hub amplification)
            F_topology = 1/(1 + ρ) (graph density)
        
        Returns:
            Total enhancement factor
        """
        if not self.nodes:
            return 1.0
        
        # Average degree
        degrees = [len(neighbors) for neighbors in self.adjacency.values()]
        avg_degree = np.mean(degrees) if degrees else 1.0
        max_degree = max(degrees) if degrees else 1.0
        
        # Redundancy factor
        F_redundancy = avg_degree
        
        # Amplification factor
        F_amplification = np.sqrt(max_degree)
        
        # Topology factor (graph density)
        n_nodes = len(self.nodes)
        n_edges = len(self.edges)
        max_edges = n_nodes * (n_nodes - 1) / 2 if n_nodes > 1 else 1
        density = n_edges / max_edges if max_edges > 0 else 0
        F_topology = 1.0 / (1.0 + density)
        
        # Combined
        F_graph = F_redundancy * F_amplification * F_topology
        
        return F_graph
    
    def validate_via_multi_path(
        self,
        source_id: str,
        target_id: str
    ) -> Dict[str, any]:
        """
        Validate measurement via multiple paths.
        
        From Algorithm (Graph-Based Harmonic Navigation):
            Find all shortest paths, extract frequency via each,
            compute weighted consensus.
        
        Args:
            source_id: Start node
            target_id: Target node
            
        Returns:
            Validation results including consensus frequency and variance
        """
        # Find all paths
        all_paths = self.find_shortest_paths(source_id, target_id)
        
        if not all_paths:
            return {
                'valid': False,
                'reason': 'No path found',
                'paths': []
            }
        
        # Extract frequency measurements along each path
        path_measurements = []
        
        for path in all_paths:
            # Average frequency along path
            path_nodes = [self.nodes[node_id] for node_id in path]
            path_freq = np.mean([n.frequency for n in path_nodes])
            
            # Weight by path quality (inverse of length, hub passage)
            path_quality = 1.0 / len(path)
            
            # Bonus for passing through hubs
            for node in path_nodes:
                path_quality *= (1.0 + node.betweenness_centrality)
            
            path_measurements.append((path_freq, path_quality))
        
        # Weighted consensus
        total_weight = sum(w for _, w in path_measurements)
        consensus_freq = sum(f * w for f, w in path_measurements) / total_weight
        
        # Inter-path variance (measure of agreement)
        frequencies = [f for f, _ in path_measurements]
        variance = np.var(frequencies)
        std_dev = np.std(frequencies)
        
        # Validation: low variance = high agreement
        relative_std = std_dev / consensus_freq if consensus_freq > 0 else float('inf')
        valid = relative_std < 0.01  # < 1% variation
        
        return {
            'valid': valid,
            'consensus_frequency': consensus_freq,
            'frequency_variance': variance,
            'frequency_std': std_dev,
            'relative_std': relative_std,
            'n_paths': len(all_paths),
            'measurements': frequencies,
            'paths': all_paths
        }
    
    def get_graph_statistics(self) -> Dict[str, any]:
        """Get comprehensive graph statistics."""
        degrees = [len(neighbors) for neighbors in self.adjacency.values()]
        
        return {
            'n_nodes': len(self.nodes),
            'n_edges': len(self.edges),
            'avg_degree': np.mean(degrees) if degrees else 0,
            'max_degree': max(degrees) if degrees else 0,
            'density': len(self.edges) / (len(self.nodes) * (len(self.nodes) - 1) / 2) if len(self.nodes) > 1 else 0,
            'enhancement_factor': self.calculate_enhancement_factor(),
            'n_hubs': sum(1 for n in self.nodes.values() if n.betweenness_centrality > 0.1)
        }


def build_circuit_harmonic_graph(
    psychons: List[Psychon],
    multi_domain_harmonics: Optional[MultiDomainHarmonics] = None,
    tolerance: float = 1e-3
) -> HarmonicNetworkGraph:
    """
    Build harmonic network graph from circuit psychons.
    
    Args:
        psychons: List of psychons in circuit
        multi_domain_harmonics: Optional multi-domain harmonic analysis
        tolerance: Frequency matching tolerance
        
    Returns:
        Constructed harmonic network graph
    """
    graph = HarmonicNetworkGraph(tolerance=tolerance)
    
    # Create node for each psychon
    for i, psychon in enumerate(psychons):
        # Extract frequency from S-coordinates
        # Map S_time to molecular frequency range
        frequency = psychon.s_time * 1e13  # ~10¹³ Hz range
        
        node = HarmonicNode(
            id=f"psychon_{i}_{psychon.id}",
            component=psychon.id,
            frequency=frequency,
            recursion_level=0,  # Can be extended for nested observations
            s_coordinates=psychon.s_entropy_vector(),
            harmonics=np.array([frequency * n for n in range(1, 11)])  # First 10 harmonics
        )
        
        graph.add_node(node)
    
    # If multi-domain harmonics provided, add nodes for each domain
    if multi_domain_harmonics:
        for domain_name, signature in [
            ('standard', multi_domain_harmonics.standard),
            ('entropy', multi_domain_harmonics.entropy),
            ('convergence', multi_domain_harmonics.convergence),
            ('information', multi_domain_harmonics.information)
        ]:
            node = HarmonicNode(
                id=f"domain_{domain_name}",
                component=f"{domain_name}_domain",
                frequency=signature.fundamental_freq,
                recursion_level=1,
                s_coordinates=np.zeros(5),
                harmonics=signature.harmonics
            )
            graph.add_node(node)
    
    # Find harmonic coincidences and create edges
    graph.find_harmonic_coincidences(max_harmonic=10)
    
    # Calculate centrality
    graph.calculate_betweenness_centrality()
    
    return graph


# Example usage
if __name__ == "__main__":
    print("="*60)
    print("HARMONIC NETWORK GRAPH: MULTI-PATH VALIDATION")
    print("="*60)
    
    # Create test network with molecular frequencies
    graph = HarmonicNetworkGraph(tolerance=0.05)
    
    # Add nodes representing different circuit components
    # N₂ fundamental: 7.07×10¹³ Hz
    # O₂ fundamental: 4.74×10¹³ Hz
    
    nodes_data = [
        ("XOR_gate", 7.07e13, 0),
        ("AND_gate", 7.10e13, 0),
        ("OR_gate", 4.74e13, 0),
        ("BMD_A", 7.05e13, 1),
        ("BMD_B", 4.76e13, 1),
        ("output", 7.08e13, 2)
    ]
    
    for component, freq, level in nodes_data:
        node = HarmonicNode(
            id=component,
            component=component,
            frequency=freq,
            recursion_level=level,
            s_coordinates=np.random.rand(5)
        )
        graph.add_node(node)
    
    # Find harmonic coincidences
    print("\nFinding harmonic coincidences...")
    graph.find_harmonic_coincidences(max_harmonic=5)
    
    print(f"Found {len(graph.edges)} harmonic coincidences")
    
    # Show some edges
    print("\nSample edges:")
    for edge in graph.edges[:5]:
        node_a = graph.nodes[edge.source]
        node_b = graph.nodes[edge.target]
        n, m = edge.harmonic_orders
        print(f"  {edge.source} --[{n}×ω₁ ≈ {m}×ω₂]--> {edge.target}")
        print(f"    Shared freq: {edge.shared_frequency/1e12:.2f} THz")
    
    # Calculate centrality
    print("\nCalculating betweenness centrality...")
    centrality = graph.calculate_betweenness_centrality()
    
    # Identify hubs
    hubs = graph.identify_precision_hubs(top_k=3)
    print("\nPrecision Hubs:")
    for hub in hubs:
        print(f"  {hub.id}: centrality = {hub.betweenness_centrality:.4f}")
    
    # Multi-path validation
    print("\nMulti-path validation: XOR_gate → output")
    validation = graph.validate_via_multi_path("XOR_gate", "output")
    
    print(f"  Valid: {validation['valid']}")
    print(f"  Consensus frequency: {validation['consensus_frequency']/1e12:.2f} THz")
    print(f"  Number of paths: {validation['n_paths']}")
    print(f"  Relative std: {validation['relative_std']:.4f}")
    
    # Graph statistics
    print("\nGraph Statistics:")
    stats = graph.get_graph_statistics()
    for key, value in stats.items():
        if isinstance(value, float):
            print(f"  {key}: {value:.2f}")
        else:
            print(f"  {key}: {value}")
    
    print(f"\nEnhancement Factor: {stats['enhancement_factor']:.0f}×")
    print("(Target: ~100× from theory)")
    
    print("\n" + "="*60)
    print("Graph construction and validation complete!")
    print("="*60)
