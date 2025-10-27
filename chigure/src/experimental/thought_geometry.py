"""
Thought Geometry: 3D Representation of Thoughts as Hole Configurations

THE BREAKTHROUGH INSIGHT:
========================

Thoughts are not abstract—they are GEOMETRIC OBJECTS.

Each thought = specific 3D arrangement of O₂ molecules around a hole.

Key concepts:
-------------

1. **Hole as 3D Structure**:
   - Hole = spatial arrangement of O₂ molecules around empty space
   - The "empty space" is the hole
   - O₂ configuration around it defines the structure
   - This structure = the BMD in physical form

2. **Similar Thoughts = Similar Geometries**:
   - Similar spatial arrangements → similar thoughts
   - Can measure geometric similarity
   - Thoughts form a continuous space of geometries

3. **Thought Capture as Geometric Units**:
   - Each hole configuration = one quantifiable thought
   - Can store thoughts as 3D geometry data
   - Can compare thoughts by comparing geometries
   - Can predict thoughts by generating geometries

4. **Electron Position = Thought Navigation**:
   - Don't need to rearrange entire gas configuration
   - Just move electron to different position in geometry
   - Small electron movement = small thought variation
   - Can GENERATE similar thoughts by moving electron

PHYSICAL IMPLEMENTATION:
------------------------

Gas Chamber (0.5% O₂)
    ↓
O₂ spatial configuration (3D)
    ↓
Hole detected (empty space + surrounding O₂)
    ↓
Electron positioned (stabilizes specific geometry)
    ↓
Thought captured = 3D geometry + electron position

THOUGHT OPERATIONS:
-------------------

1. Capture thought: Record 3D O₂ configuration
2. Compare thoughts: Calculate geometric similarity
3. Predict thought: Generate likely next geometry
4. Navigate thoughts: Move electron in geometry space
5. Generate thought: Create specific O₂ arrangement + electron position

This is HOW consciousness THINKS!
"""

import numpy as np
from typing import Dict, Any, List, Tuple, Optional
from dataclasses import dataclass
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy.spatial.distance import cdist
from sklearn.decomposition import PCA

# Import existing modules (with fallback for standalone execution)
import sys
from pathlib import Path

# Try package imports first
try:
    from experimental.oscillatory_hole_detector import (
        OscillatoryHoleSignature,
        ElectronStabilizationEvent,
        GasSemanticChamber,
        SemiconductorStabilizationCircuit
    )
except ImportError:
    # Try same-directory import
    try:
        from oscillatory_hole_detector import (
            OscillatoryHoleSignature,
            ElectronStabilizationEvent,
            GasSemanticChamber,
            SemiconductorStabilizationCircuit
        )
    except ImportError:
        # Add experimental directory to path
        experimental_path = Path(__file__).parent
        sys.path.insert(0, str(experimental_path))
        from oscillatory_hole_detector import (
            OscillatoryHoleSignature,
            ElectronStabilizationEvent,
            GasSemanticChamber,
            SemiconductorStabilizationCircuit
        )


@dataclass
class ThoughtGeometry:
    """
    3D geometric representation of a thought.
    
    A thought is a specific spatial arrangement of O₂ molecules
    around a hole (empty space).
    
    Attributes:
        o2_positions: 3D positions of O₂ molecules [N, 3]
        hole_center: Center of the hole (3D coordinate)
        hole_volume: Volume of the hole region (m³)
        electron_position: Where electron stabilizes [3]
        geometry_signature: Geometric fingerprint [features]
        energy: Energy of configuration (eV)
    """
    o2_positions: np.ndarray      # [N, 3] positions
    hole_center: np.ndarray       # [3] center point
    hole_volume: float            # m³
    electron_position: np.ndarray # [3] stabilization point
    geometry_signature: np.ndarray # [features] fingerprint
    energy: float                 # eV
    
    @property
    def n_molecules(self) -> int:
        """Number of O₂ molecules in configuration."""
        return len(self.o2_positions)
    
    def distance_to_hole(self) -> np.ndarray:
        """Distance of each O₂ molecule from hole center."""
        return np.linalg.norm(self.o2_positions - self.hole_center, axis=1)
    
    def electron_hole_distance(self) -> float:
        """Distance from electron to hole center."""
        return np.linalg.norm(self.electron_position - self.hole_center)


class ThoughtGeometryCapture:
    """
    Captures thoughts as 3D geometric configurations.
    
    Converts oscillatory hole signatures into explicit 3D geometries.
    """
    
    def __init__(self, chamber_volume_m3: float = 1e-3):
        """
        Initialize thought capture system.
        
        Args:
            chamber_volume_m3: Gas chamber volume (m³)
        """
        self.chamber_volume = chamber_volume_m3
        self.thought_library: List[ThoughtGeometry] = []
        
    def capture_thought_from_hole(self,
                                  hole: OscillatoryHoleSignature,
                                  electron_event: ElectronStabilizationEvent,
                                  o2_field: np.ndarray,
                                  sensor_positions: np.ndarray) -> ThoughtGeometry:
        """
        Capture a thought from oscillatory hole signature.
        
        Converts hole detection into explicit 3D geometry.
        
        Args:
            hole: Detected oscillatory hole
            electron_event: Electron stabilization event
            o2_field: O₂ density at each sensor position
            sensor_positions: 3D positions of sensors [N, 3]
            
        Returns:
            ThoughtGeometry object
        """
        # Hole is where O₂ density is perturbed
        # Find regions of low density (the "hole")
        baseline_density = np.mean(o2_field)
        density_perturbation = o2_field - baseline_density
        
        # Hole = regions with lower density
        hole_mask = density_perturbation < -0.05 * baseline_density
        
        if np.sum(hole_mask) == 0:
            # No clear hole, use lowest density region
            hole_mask = density_perturbation < np.percentile(density_perturbation, 20)
        
        # Hole center = centroid of low-density region
        hole_positions = sensor_positions[hole_mask]
        hole_center = np.mean(hole_positions, axis=0) if len(hole_positions) > 0 else np.array([0, 0, 0])
        
        # Hole volume (approximate from number of low-density sensors)
        n_hole_sensors = np.sum(hole_mask)
        total_sensors = len(sensor_positions)
        hole_volume = (n_hole_sensors / total_sensors) * self.chamber_volume
        
        # O₂ positions = where density is higher (surrounding the hole)
        o2_mask = ~hole_mask
        o2_positions = sensor_positions[o2_mask]
        
        # Electron position (where it stabilizes)
        # Typically near hole edge (highest gradient)
        distances = np.linalg.norm(sensor_positions - hole_center, axis=1)
        gradient_regions = (distances > 0.1) & (distances < 0.3)  # Near hole edge
        if np.sum(gradient_regions) > 0:
            electron_position = sensor_positions[gradient_regions][0]
        else:
            electron_position = hole_center + np.array([0.1, 0, 0])  # Default offset
        
        # Geometric signature (features describing the geometry)
        geometry_signature = self._compute_geometry_signature(
            o2_positions,
            hole_center,
            hole_volume,
            electron_position
        )
        
        # Energy from electron stabilization
        energy = electron_event.energy_released if electron_event.completed else 0.0
        
        thought = ThoughtGeometry(
            o2_positions=o2_positions,
            hole_center=hole_center,
            hole_volume=hole_volume,
            electron_position=electron_position,
            geometry_signature=geometry_signature,
            energy=energy
        )
        
        # Add to library
        self.thought_library.append(thought)
        
        return thought
    
    def _compute_geometry_signature(self,
                                   o2_positions: np.ndarray,
                                   hole_center: np.ndarray,
                                   hole_volume: float,
                                   electron_position: np.ndarray) -> np.ndarray:
        """
        Compute geometric signature (fingerprint) of thought.
        
        Features:
        ---------
        - Radial distribution around hole
        - Angular distribution
        - Distance statistics
        - Symmetry measures
        - Electron-hole geometry
        
        Args:
            o2_positions: O₂ molecule positions
            hole_center: Hole center position
            hole_volume: Hole volume
            electron_position: Electron position
            
        Returns:
            Feature vector describing geometry
        """
        # Distance from each O₂ to hole center
        distances = np.linalg.norm(o2_positions - hole_center, axis=1)
        
        # Radial distribution (histogram)
        radial_hist, _ = np.histogram(distances, bins=10, range=(0, 1.0))
        radial_hist = radial_hist / (np.sum(radial_hist) + 1e-10)
        
        # Angular distribution (spherical coordinates)
        relative_pos = o2_positions - hole_center
        theta = np.arctan2(relative_pos[:, 1], relative_pos[:, 0])  # Azimuthal
        phi = np.arccos(relative_pos[:, 2] / (distances + 1e-10))   # Polar
        
        theta_hist, _ = np.histogram(theta, bins=8, range=(-np.pi, np.pi))
        phi_hist, _ = np.histogram(phi, bins=4, range=(0, np.pi))
        
        theta_hist = theta_hist / (np.sum(theta_hist) + 1e-10)
        phi_hist = phi_hist / (np.sum(phi_hist) + 1e-10)
        
        # Distance statistics
        distance_features = [
            np.mean(distances),
            np.std(distances),
            np.min(distances),
            np.max(distances),
        ]
        
        # Symmetry measure (variance in angular distributions)
        symmetry = 1.0 / (1.0 + np.std(theta_hist) + np.std(phi_hist))
        
        # Electron-hole geometry
        electron_hole_dist = np.linalg.norm(electron_position - hole_center)
        electron_nearest_o2 = np.min(np.linalg.norm(o2_positions - electron_position, axis=1))
        
        electron_features = [
            electron_hole_dist,
            electron_nearest_o2,
            hole_volume,
        ]
        
        # Combine all features
        signature = np.concatenate([
            radial_hist,      # 10
            theta_hist,       # 8
            phi_hist,         # 4
            distance_features,# 4
            [symmetry],       # 1
            electron_features,# 3
        ])
        
        return signature  # Total: 30 features


class ThoughtSimilarityCalculator:
    """
    Calculates similarity between thoughts based on geometry.
    
    Similar geometries = similar thoughts.
    """
    
    def __init__(self):
        """Initialize similarity calculator."""
        pass
    
    def geometric_similarity(self,
                           thought_A: ThoughtGeometry,
                           thought_B: ThoughtGeometry) -> float:
        """
        Calculate geometric similarity between two thoughts.
        
        Similarity based on:
        - Signature distance (feature space)
        - Structural alignment (3D geometry)
        - Energy similarity
        
        Args:
            thought_A, thought_B: Thoughts to compare
            
        Returns:
            Similarity score [0, 1] (1 = identical)
        """
        # Signature similarity (Euclidean distance in feature space)
        sig_dist = np.linalg.norm(thought_A.geometry_signature - thought_B.geometry_signature)
        sig_similarity = 1.0 / (1.0 + sig_dist)
        
        # Hole size similarity
        volume_ratio = min(thought_A.hole_volume, thought_B.hole_volume) / (
            max(thought_A.hole_volume, thought_B.hole_volume) + 1e-10
        )
        
        # Energy similarity
        energy_diff = abs(thought_A.energy - thought_B.energy)
        energy_similarity = 1.0 / (1.0 + energy_diff / 100.0)
        
        # Overall similarity (weighted average)
        overall = 0.6 * sig_similarity + 0.2 * volume_ratio + 0.2 * energy_similarity
        
        return overall
    
    def find_similar_thoughts(self,
                            query_thought: ThoughtGeometry,
                            thought_library: List[ThoughtGeometry],
                            top_k: int = 5) -> List[Tuple[int, float]]:
        """
        Find most similar thoughts in library.
        
        Args:
            query_thought: Thought to match
            thought_library: Library of thoughts to search
            top_k: Number of similar thoughts to return
            
        Returns:
            List of (index, similarity) tuples, sorted by similarity
        """
        similarities = []
        
        for i, lib_thought in enumerate(thought_library):
            sim = self.geometric_similarity(query_thought, lib_thought)
            similarities.append((i, sim))
        
        # Sort by similarity (descending)
        similarities.sort(key=lambda x: x[1], reverse=True)
        
        return similarities[:top_k]


class ThoughtNavigator:
    """
    Navigates thought space by moving electron in geometries.
    
    KEY INSIGHT: Don't need to rearrange entire gas—just move electron!
    
    Small electron movements = small thought variations
    This allows GENERATING similar thoughts efficiently.
    """
    
    def __init__(self):
        """Initialize thought navigator."""
        self.current_thought: Optional[ThoughtGeometry] = None
        
    def move_electron(self,
                     thought: ThoughtGeometry,
                     displacement: np.ndarray) -> ThoughtGeometry:
        """
        Generate new thought by moving electron in existing geometry.
        
        CRITICAL: This doesn't change O₂ configuration—just electron position!
        
        Small displacement → similar thought
        Large displacement → different thought
        
        Args:
            thought: Current thought geometry
            displacement: 3D displacement vector for electron
            
        Returns:
            New thought geometry with moved electron
        """
        # New electron position
        new_electron_pos = thought.electron_position + displacement
        
        # Ensure electron stays near hole (physical constraint)
        hole_dist = np.linalg.norm(new_electron_pos - thought.hole_center)
        if hole_dist > 0.5:  # Too far from hole
            # Project back to reasonable distance
            direction = (new_electron_pos - thought.hole_center) / hole_dist
            new_electron_pos = thought.hole_center + direction * 0.5
        
        # Recompute geometry signature (electron position changed)
        # But O₂ positions stay the same!
        new_signature = self._compute_signature_with_new_electron(
            thought.o2_positions,
            thought.hole_center,
            thought.hole_volume,
            new_electron_pos
        )
        
        # Energy changes slightly with electron position
        # (different stabilization point)
        distance_change = np.linalg.norm(displacement)
        energy_change = distance_change * 10.0  # eV per unit displacement
        new_energy = thought.energy + np.random.normal(0, energy_change)
        
        new_thought = ThoughtGeometry(
            o2_positions=thought.o2_positions.copy(),  # Same O₂ config!
            hole_center=thought.hole_center.copy(),
            hole_volume=thought.hole_volume,
            electron_position=new_electron_pos,
            geometry_signature=new_signature,
            energy=new_energy
        )
        
        return new_thought
    
    def _compute_signature_with_new_electron(self,
                                            o2_positions: np.ndarray,
                                            hole_center: np.ndarray,
                                            hole_volume: float,
                                            electron_position: np.ndarray) -> np.ndarray:
        """Recompute signature with new electron position."""
        # Use same method as ThoughtGeometryCapture
        capture = ThoughtGeometryCapture()
        return capture._compute_geometry_signature(
            o2_positions,
            hole_center,
            hole_volume,
            electron_position
        )
    
    def explore_neighborhood(self,
                           thought: ThoughtGeometry,
                           n_neighbors: int = 8,
                           step_size: float = 0.1) -> List[ThoughtGeometry]:
        """
        Generate neighboring thoughts by exploring electron positions.
        
        Creates a "neighborhood" of similar thoughts by moving electron
        in different directions.
        
        Args:
            thought: Central thought
            n_neighbors: Number of neighbors to generate
            step_size: Electron displacement magnitude
            
        Returns:
            List of neighboring thoughts
        """
        neighbors = []
        
        # Generate random directions
        for _ in range(n_neighbors):
            # Random direction
            direction = np.random.randn(3)
            direction = direction / np.linalg.norm(direction)
            
            # Displacement
            displacement = direction * step_size
            
            # Generate neighbor
            neighbor = self.move_electron(thought, displacement)
            neighbors.append(neighbor)
        
        return neighbors
    
    def interpolate_thoughts(self,
                           thought_A: ThoughtGeometry,
                           thought_B: ThoughtGeometry,
                           n_steps: int = 10) -> List[ThoughtGeometry]:
        """
        Interpolate between two thoughts.
        
        Creates smooth transition by gradually moving electron from
        position A to position B.
        
        This is a "thought path" in geometry space!
        
        Args:
            thought_A, thought_B: Start and end thoughts
            n_steps: Number of intermediate steps
            
        Returns:
            List of thoughts forming path from A to B
        """
        path = []
        
        # Linear interpolation of electron position
        electron_start = thought_A.electron_position
        electron_end = thought_B.electron_position
        
        for i in range(n_steps + 1):
            alpha = i / n_steps
            
            # Interpolated electron position
            electron_interp = (1 - alpha) * electron_start + alpha * electron_end
            
            # Also interpolate O₂ configuration (blend geometries)
            # In real system, O₂ would naturally rearrange
            o2_interp = (1 - alpha) * thought_A.o2_positions + alpha * thought_B.o2_positions
            hole_interp = (1 - alpha) * thought_A.hole_center + alpha * thought_B.hole_center
            volume_interp = (1 - alpha) * thought_A.hole_volume + alpha * thought_B.hole_volume
            energy_interp = (1 - alpha) * thought_A.energy + alpha * thought_B.energy
            
            # Compute signature
            capture = ThoughtGeometryCapture()
            sig_interp = capture._compute_geometry_signature(
                o2_interp,
                hole_interp,
                volume_interp,
                electron_interp
            )
            
            interp_thought = ThoughtGeometry(
                o2_positions=o2_interp,
                hole_center=hole_interp,
                hole_volume=volume_interp,
                electron_position=electron_interp,
                geometry_signature=sig_interp,
                energy=energy_interp
            )
            
            path.append(interp_thought)
        
        return path


class ThoughtSpaceVisualizer:
    """
    Visualizes thought space (3D geometries).
    
    Projects high-dimensional thought geometries into 2D/3D for visualization.
    """
    
    def __init__(self):
        """Initialize visualizer."""
        pass
    
    def visualize_thought_3d(self,
                            thought: ThoughtGeometry,
                            show_electron: bool = True,
                            figsize: Tuple[int, int] = (10, 10)):
        """
        Visualize a single thought as 3D geometry.
        
        Shows:
        - O₂ molecule positions (blue spheres)
        - Hole center (red sphere)
        - Electron position (green sphere, if show_electron=True)
        
        Args:
            thought: Thought to visualize
            show_electron: Whether to show electron position
            figsize: Figure size
        """
        fig = plt.figure(figsize=figsize)
        ax = fig.add_subplot(111, projection='3d')
        
        # O₂ positions
        ax.scatter(
            thought.o2_positions[:, 0],
            thought.o2_positions[:, 1],
            thought.o2_positions[:, 2],
            c='blue',
            s=50,
            alpha=0.6,
            label='O₂ molecules'
        )
        
        # Hole center
        ax.scatter(
            [thought.hole_center[0]],
            [thought.hole_center[1]],
            [thought.hole_center[2]],
            c='red',
            s=200,
            marker='*',
            label='Hole center'
        )
        
        # Electron position
        if show_electron:
            ax.scatter(
                [thought.electron_position[0]],
                [thought.electron_position[1]],
                [thought.electron_position[2]],
                c='green',
                s=150,
                marker='^',
                label='Electron'
            )
            
            # Line from hole to electron
            ax.plot(
                [thought.hole_center[0], thought.electron_position[0]],
                [thought.hole_center[1], thought.electron_position[1]],
                [thought.hole_center[2], thought.electron_position[2]],
                'g--',
                alpha=0.5
            )
        
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        ax.set_title(f'Thought Geometry (Energy: {thought.energy:.1f} eV)')
        ax.legend()
        
        plt.tight_layout()
        return fig, ax
    
    def visualize_thought_space(self,
                               thoughts: List[ThoughtGeometry],
                               labels: Optional[List[str]] = None,
                               figsize: Tuple[int, int] = (12, 8)):
        """
        Visualize collection of thoughts in 2D projection.
        
        Uses PCA to project high-dimensional signatures into 2D.
        
        Args:
            thoughts: List of thoughts to visualize
            labels: Optional labels for each thought
            figsize: Figure size
        """
        # Extract signatures
        signatures = np.array([t.geometry_signature for t in thoughts])
        
        # PCA projection to 2D
        pca = PCA(n_components=2)
        projected = pca.fit_transform(signatures)
        
        # Plot
        fig, ax = plt.subplots(figsize=figsize)
        
        scatter = ax.scatter(
            projected[:, 0],
            projected[:, 1],
            c=[t.energy for t in thoughts],
            s=100,
            cmap='viridis',
            alpha=0.7
        )
        
        # Labels
        if labels is not None:
            for i, label in enumerate(labels):
                ax.annotate(
                    label,
                    (projected[i, 0], projected[i, 1]),
                    fontsize=8,
                    alpha=0.7
                )
        
        ax.set_xlabel(f'PC1 ({pca.explained_variance_ratio_[0]:.1%})')
        ax.set_ylabel(f'PC2 ({pca.explained_variance_ratio_[1]:.1%})')
        ax.set_title('Thought Space (2D Projection)')
        
        cbar = plt.colorbar(scatter, ax=ax)
        cbar.set_label('Energy (eV)')
        
        plt.tight_layout()
        return fig, ax


def demonstrate_thought_geometry():
    """
    Demonstrate thought geometry system.
    """
    print("\n" + "="*80)
    print("THOUGHT GEOMETRY SYSTEM")
    print("Thoughts as 3D Geometric Objects")
    print("="*80)
    print("\nKEY INSIGHT:")
    print("  Thoughts = 3D arrangements of O₂ molecules around holes")
    print("  Similar geometries = similar thoughts")
    print("  Moving electron in geometry = navigating thoughts")
    print("="*80 + "\n")
    
    # Create capture system
    capture = ThoughtGeometryCapture()
    navigator = ThoughtNavigator()
    similarity = ThoughtSimilarityCalculator()
    
    # Simulate capturing a thought
    print("1. CAPTURING A THOUGHT")
    print("-" * 80)
    
    # Fake O₂ field and sensors (in real system, from gas chamber)
    n_sensors = 64
    sensor_positions = np.random.rand(n_sensors, 3) - 0.5  # [-0.5, 0.5]³
    o2_field = np.random.rand(n_sensors) * 1e20  # molecules/m³
    
    # Create fake hole signature
    from oscillatory_hole_detector import OscillatoryHoleSignature, ElectronStabilizationEvent
    
    fake_hole = OscillatoryHoleSignature(
        spatial_configuration=o2_field,
        required_electron_density=1e18,
        stabilization_current=100e-12,  # 100 pA
        lifetime=0.01,  # 10 ms
        completion_signature=np.random.rand(100)
    )
    
    fake_electron = ElectronStabilizationEvent(
        hole_signature=fake_hole,
        electron_current=100e-12,
        recombination_time=0.01,
        energy_released=250.0,  # eV
        completed=True
    )
    
    # Capture thought
    thought_1 = capture.capture_thought_from_hole(
        fake_hole,
        fake_electron,
        o2_field,
        sensor_positions
    )
    
    print(f"✓ Thought captured!")
    print(f"  O₂ molecules: {thought_1.n_molecules}")
    print(f"  Hole center: {thought_1.hole_center}")
    print(f"  Hole volume: {thought_1.hole_volume:.2e} m³")
    print(f"  Electron position: {thought_1.electron_position}")
    print(f"  Energy: {thought_1.energy:.1f} eV")
    print(f"  Signature dimensions: {len(thought_1.geometry_signature)}")
    
    # Generate similar thought by moving electron
    print("\n2. GENERATING SIMILAR THOUGHT (Move Electron)")
    print("-" * 80)
    
    small_displacement = np.array([0.05, 0.02, -0.03])
    thought_2 = navigator.move_electron(thought_1, small_displacement)
    
    print(f"✓ Generated similar thought by moving electron")
    print(f"  Electron moved: {np.linalg.norm(small_displacement):.3f} units")
    print(f"  New electron position: {thought_2.electron_position}")
    print(f"  O₂ configuration: UNCHANGED (same molecules!)")
    print(f"  New energy: {thought_2.energy:.1f} eV")
    
    # Calculate similarity
    sim = similarity.geometric_similarity(thought_1, thought_2)
    print(f"  Similarity to original: {sim:.3f}")
    
    # Explore neighborhood
    print("\n3. EXPLORING THOUGHT NEIGHBORHOOD")
    print("-" * 80)
    
    neighbors = navigator.explore_neighborhood(thought_1, n_neighbors=5, step_size=0.08)
    
    print(f"✓ Generated {len(neighbors)} neighboring thoughts")
    for i, neighbor in enumerate(neighbors):
        sim_i = similarity.geometric_similarity(thought_1, neighbor)
        print(f"  Neighbor {i+1}: similarity = {sim_i:.3f}, energy = {neighbor.energy:.1f} eV")
    
    # Summary
    print("\n" + "="*80)
    print("SUMMARY")
    print("="*80)
    print("\n✓ Thoughts captured as 3D geometries")
    print("✓ Similar thoughts have similar geometries")
    print("✓ Can navigate thought space by moving electron")
    print("✓ Don't need to rearrange entire gas—just move electron!")
    print("\n🎯 THOUGHTS ARE GEOMETRIC OBJECTS WE CAN MANIPULATE!")
    print("="*80 + "\n")


if __name__ == "__main__":
    demonstrate_thought_geometry()

