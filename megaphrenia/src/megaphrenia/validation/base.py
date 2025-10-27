"""
Base classes for validation testing with automatic result persistence.

All validation tests inherit from these classes and automatically save
results in structured JSON format with proper metadata.
"""

import json
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional, List
from abc import ABC, abstractmethod


class ValidationTest(ABC):
    """
    Base class for all validation tests.
    
    Automatically handles:
    - Test metadata tracking
    - Timing measurements
    - Result persistence to JSON
    - Directory structure creation
    
    Subclasses must implement:
    - run(): Execute the test
    - get_category(): Return directory category
    """
    
    def __init__(self, test_name: str, description: str = ""):
        self.test_name = test_name
        self.description = description
        self.start_time = None
        self.results = {
            "test_metadata": {},
            "configuration": {},
            "results": {
                "measurements": [],
                "statistics": {},
                "validation": {}
            },
            "comparison": {}
        }
        
    def setup(self, **config):
        """
        Setup test environment.
        
        Args:
            **config: Configuration parameters to store
        """
        self.start_time = time.time()
        self.results["test_metadata"] = {
            "test_name": self.test_name,
            "description": self.description,
            "timestamp": datetime.now().isoformat(),
            "framework_version": "1.0.0"
        }
        self.results["configuration"] = config
        
    @abstractmethod
    def run(self) -> Dict[str, Any]:
        """
        Execute test and return results.
        
        Returns:
            Dictionary of test results
        """
        pass
    
    @abstractmethod
    def get_category(self) -> str:
        """
        Get test category for directory structure.
        
        Returns:
            Category path (e.g., 'components/transistor')
        """
        pass
    
    def add_measurement(self, trial: int, **data):
        """Add a single measurement to results."""
        measurement = {"trial": trial, **data}
        self.results["results"]["measurements"].append(measurement)
    
    def set_statistics(self, **stats):
        """Set aggregate statistics."""
        self.results["results"]["statistics"].update(stats)
    
    def set_validation(self, passed: bool, **validation_data):
        """Set validation results."""
        self.results["results"]["validation"]["passed"] = passed
        self.results["results"]["validation"].update(validation_data)
    
    def set_comparison(self, **comparison_data):
        """Set theoretical vs measured comparison."""
        self.results["comparison"].update(comparison_data)
    
    def save_results(self, custom_dir: Optional[Path] = None) -> Path:
        """
        Save results to JSON file.
        
        Args:
            custom_dir: Optional custom directory (uses get_category() if None)
            
        Returns:
            Path to saved file
        """
        # Create results directory
        if custom_dir:
            results_dir = Path("validation_results") / custom_dir
        else:
            results_dir = Path("validation_results") / self.get_category()
        results_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{self.test_name}_{timestamp}.json"
        filepath = results_dir / filename
        
        # Add test duration
        if self.start_time:
            duration = time.time() - self.start_time
            self.results["test_metadata"]["test_duration_seconds"] = duration
        
        # Save to JSON
        with open(filepath, 'w') as f:
            json.dump(self.results, f, indent=2)
        
        print(f"\n✅ Results saved to: {filepath}")
        return filepath
    
    def execute(self, **config) -> Path:
        """
        Full test execution: setup → run → save.
        
        Args:
            **config: Configuration parameters
            
        Returns:
            Path to saved results file
        """
        print(f"\n{'='*60}")
        print(f"VALIDATION TEST: {self.test_name}")
        print('='*60)
        
        # Setup
        self.setup(**config)
        print(f"Configuration: {config}")
        
        # Run
        print("\nRunning test...")
        test_results = self.run()
        
        # Save
        filepath = self.save_results()
        
        # Print summary
        if "validation" in self.results["results"]:
            passed = self.results["results"]["validation"].get("passed", False)
            status = "✅ PASSED" if passed else "❌ FAILED"
            print(f"\nTest Status: {status}")
        
        return filepath


class CircuitTest(ValidationTest):
    """Base class for circuit validation tests."""
    
    def get_category(self) -> str:
        """Circuits stored in 'circuits' directory."""
        return "circuits"


class HardwareTest(ValidationTest):
    """Base class for hardware harvesting tests."""
    
    def get_category(self) -> str:
        """Hardware tests stored in 'hardware' directory."""
        return "hardware"


# Example usage
if __name__ == "__main__":
    # Example of how to create a validation test
    class ExampleTest(ValidationTest):
        def run(self) -> Dict[str, Any]:
            # Simulate measurements
            for i in range(10):
                self.add_measurement(
                    trial=i,
                    value=42.1 + (i * 0.01),
                    success=True
                )
            
            # Set statistics
            self.set_statistics(
                mean_value=42.15,
                std_value=0.05
            )
            
            # Set validation
            self.set_validation(
                passed=True,
                target_met=True
            )
            
            # Set comparison
            self.set_comparison(
                theoretical=42.1,
                measured=42.15,
                percent_error=0.12
            )
            
            return self.results["results"]
        
        def get_category(self) -> str:
            return "examples"
    
    # Run example test
    test = ExampleTest("example_validation", "Example validation test")
    test.execute(parameter_a=1.0, parameter_b=2.0)

