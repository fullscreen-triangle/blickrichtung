"""
Tests for experimental module - Physical consciousness detection

Run with:
    pytest tests/test_experimental.py -v
"""

import pytest
import numpy as np
from experimental import (
    OscillatoryHoleDetector,
    ThoughtGeometry,
    ThoughtGeometryCapture,
    ThoughtSimilarityCalculator,
    ThoughtNavigator,
    ConsciousnessDetectionSystem,
)


class TestOscillatoryHoleDetector:
    """Tests for oscillatory hole detection."""
    
    def test_initialization(self):
        """Test detector initializes correctly."""
        detector = OscillatoryHoleDetector()
        assert detector is not None
        assert detector.gas_chamber is not None
        assert detector.circuit is not None
    
    def test_detect_scent(self):
        """Test scent detection produces valid results."""
        detector = OscillatoryHoleDetector()
        
        odorant = {'name': 'Vanillin', 'molecular_mass': 152.15}
        result = detector.detect_scent(odorant)
        
        assert 'hole' in result
        assert 'stabilization' in result
        assert result['hole'].stabilization_current > 0
        assert result['stabilization'].completed
    
    def test_compare_scents(self):
        """Test scent comparison."""
        detector = OscillatoryHoleDetector()
        
        odorant_A = {'name': 'Vanillin', 'molecular_mass': 152.15}
        odorant_B = {'name': 'Ethyl Vanillin', 'molecular_mass': 166.17}
        
        comparison = detector.compare_scents(odorant_A, odorant_B)
        
        assert 'oscillatory_similarity' in comparison
        assert 0 <= comparison['oscillatory_similarity'] <= 1
        assert comparison['similar_compounds']


class TestThoughtGeometry:
    """Tests for thought geometry."""
    
    def test_thought_geometry_creation(self):
        """Test thought geometry dataclass."""
        o2_positions = np.random.randn(50, 3) * 0.05
        
        thought = ThoughtGeometry(
            o2_positions=o2_positions,
            hole_center=np.array([0.0, 0.0, 0.0]),
            hole_volume=1e-5,
            electron_position=np.array([0.01, 0.01, 0.05]),
            geometry_signature=np.random.randn(30),
            energy=250.0
        )
        
        assert thought.n_molecules == 50
        assert thought.hole_volume == 1e-5
        assert thought.energy == 250.0
    
    def test_thought_capture(self):
        """Test thought capture from hole detection."""
        from experimental.oscillatory_hole_detector import OscillatoryHoleSignature
        
        # Create mock hole
        hole = OscillatoryHoleSignature(
            timestamp=0.0,
            hole_frequency=1e13,
            stabilization_current=500e-12,
            spatial_extent=0.05,
            temporal_duration=0.15,
            variance_before=100.0,
            variance_after=5.0,
            completion_signature=np.random.randn(20)
        )
        
        # Mock electron event
        from experimental.oscillatory_hole_detector import ElectronStabilizationEvent
        electron_event = ElectronStabilizationEvent(
            timestamp=0.0,
            electron_position=np.array([0.01, 0.01, 0.05]),
            hole_position=np.array([0.0, 0.0, 0.0]),
            stabilization_current=500e-12,
            completion_time=0.001,
            completed=True
        )
        
        # Mock O2 field
        o2_field = np.ones(64) * 0.005
        sensor_positions = np.random.randn(64, 3) * 0.1
        
        # Capture
        capture = ThoughtGeometryCapture()
        thought = capture.capture_thought_from_hole(
            hole, electron_event, o2_field, sensor_positions
        )
        
        assert thought is not None
        assert thought.n_molecules > 0
        assert len(thought.geometry_signature) == 30


class TestThoughtSimilarity:
    """Tests for thought similarity calculation."""
    
    def test_geometric_similarity(self):
        """Test geometric similarity calculation."""
        # Create two similar thoughts
        thought_A = ThoughtGeometry(
            o2_positions=np.random.randn(50, 3) * 0.05,
            hole_center=np.array([0.0, 0.0, 0.0]),
            hole_volume=1e-5,
            electron_position=np.array([0.01, 0.01, 0.05]),
            geometry_signature=np.random.randn(30),
            energy=250.0
        )
        
        thought_B = ThoughtGeometry(
            o2_positions=np.random.randn(50, 3) * 0.05,
            hole_center=np.array([0.0, 0.0, 0.0]),
            hole_volume=1.1e-5,
            electron_position=np.array([0.012, 0.009, 0.051]),
            geometry_signature=thought_A.geometry_signature + np.random.randn(30) * 0.1,
            energy=255.0
        )
        
        calculator = ThoughtSimilarityCalculator()
        similarity = calculator.geometric_similarity(thought_A, thought_B)
        
        assert 0 <= similarity <= 1
        assert similarity > 0.7  # Should be quite similar


class TestThoughtNavigation:
    """Tests for thought space navigation."""
    
    def test_move_electron(self):
        """Test electron movement generates similar thought."""
        # Create original thought
        original = ThoughtGeometry(
            o2_positions=np.random.randn(50, 3) * 0.05,
            hole_center=np.array([0.0, 0.0, 0.0]),
            hole_volume=1e-5,
            electron_position=np.array([0.01, 0.01, 0.05]),
            geometry_signature=np.random.randn(30),
            energy=250.0
        )
        
        # Move electron
        navigator = ThoughtNavigator()
        displacement = np.array([0.01, 0.0, 0.0])
        new_thought = navigator.move_electron(original, displacement)
        
        # Check new thought is similar
        calculator = ThoughtSimilarityCalculator()
        similarity = calculator.geometric_similarity(original, new_thought)
        
        assert similarity > 0.85  # High similarity for small movement
        assert not np.allclose(new_thought.electron_position, original.electron_position)
    
    def test_explore_neighborhood(self):
        """Test neighborhood exploration."""
        thought = ThoughtGeometry(
            o2_positions=np.random.randn(50, 3) * 0.05,
            hole_center=np.array([0.0, 0.0, 0.0]),
            hole_volume=1e-5,
            electron_position=np.array([0.01, 0.01, 0.05]),
            geometry_signature=np.random.randn(30),
            energy=250.0
        )
        
        navigator = ThoughtNavigator()
        neighbors = navigator.explore_neighborhood(thought, n_neighbors=8, radius=0.03)
        
        assert len(neighbors) == 8
        
        # All neighbors should be similar
        calculator = ThoughtSimilarityCalculator()
        for neighbor in neighbors:
            similarity = calculator.geometric_similarity(thought, neighbor)
            assert similarity > 0.7


class TestConsciousnessDetectionSystem:
    """Tests for complete integrated system."""
    
    def test_system_initialization(self):
        """Test system initializes in simulation mode."""
        system = ConsciousnessDetectionSystem(simulation_mode=True)
        assert system is not None
        assert system.simulation_mode
        assert system.hardware is not None
    
    def test_capture_thought(self):
        """Test thought capture workflow."""
        system = ConsciousnessDetectionSystem(simulation_mode=True)
        system.startup()
        
        odorant = {'name': 'Vanillin', 'molecular_mass': 152.15}
        thought = system.capture_thought(odorant, capture_duration=0.5)
        
        assert thought is not None
        assert thought.n_molecules > 0
        assert len(system.thought_library) == 1
        
        system.shutdown()
    
    def test_navigate_thought_space(self):
        """Test thought space navigation."""
        system = ConsciousnessDetectionSystem(simulation_mode=True)
        system.startup()
        
        # Capture initial thought
        odorant = {'name': 'Vanillin', 'molecular_mass': 152.15}
        thought = system.capture_thought(odorant, capture_duration=0.5)
        
        # Navigate
        path = system.navigate_thought_space(0, n_steps=5, step_size=0.03)
        
        assert len(path) == 6  # Initial + 5 steps
        
        # Check continuity
        calculator = ThoughtSimilarityCalculator()
        for i in range(len(path) - 1):
            similarity = calculator.geometric_similarity(path[i], path[i+1])
            assert similarity > 0.7  # Continuous path
        
        system.shutdown()


# Pytest fixtures
@pytest.fixture
def detector():
    """Provide oscillatory hole detector."""
    return OscillatoryHoleDetector()


@pytest.fixture
def thought():
    """Provide sample thought geometry."""
    return ThoughtGeometry(
        o2_positions=np.random.randn(50, 3) * 0.05,
        hole_center=np.array([0.0, 0.0, 0.0]),
        hole_volume=1e-5,
        electron_position=np.array([0.01, 0.01, 0.05]),
        geometry_signature=np.random.randn(30),
        energy=250.0
    )


@pytest.fixture
def system():
    """Provide consciousness detection system in simulation mode."""
    system = ConsciousnessDetectionSystem(simulation_mode=True)
    system.startup()
    yield system
    system.shutdown()


# Integration test
def test_complete_workflow(system):
    """Test complete experimental workflow."""
    # Capture multiple thoughts
    odorants = [
        {'name': 'Vanillin', 'molecular_mass': 152.15},
        {'name': 'Indole', 'molecular_mass': 117.15},
    ]
    
    for odorant in odorants:
        system.capture_thought(odorant, capture_duration=0.5)
    
    assert len(system.thought_library) == 2
    
    # Navigate from first thought
    path = system.navigate_thought_space(0, n_steps=3, step_size=0.03)
    assert len(path) == 4
    
    # Validate similarity
    results = system.validate_similarity_prediction()
    assert 'similarities' in results
    assert len(results['similarities']) > 0


if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v", "--tb=short"])

