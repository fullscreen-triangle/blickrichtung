"""
Half Adder Validation Test with Result Persistence

This is our FIRST circuit validation test and serves as a template
for all future circuit validations.

Tests:
- Functional correctness (truth table)
- Performance (operation time)
- Component behavior (gate statistics)
- S-coordinate awareness (tri-dimensional operation)
"""

import sys
sys.path.append('src')

from megaphrenia.validation.base import CircuitTest
from megaphrenia.circuits.combinational import HalfAdder
from megaphrenia.core.psychon import create_psychon_from_signature
import time
from typing import Dict, Any


class HalfAdderValidation(CircuitTest):
    """Validation test for Half Adder circuit."""
    
    def __init__(self):
        super().__init__(
            test_name="half_adder_functional",
            description="Functional and performance validation of Half Adder circuit"
        )
        self.half_adder = None
    
    def run(self) -> Dict[str, Any]:
        """Execute Half Adder validation."""
        
        # Create Half Adder
        self.half_adder = HalfAdder()
        print(f"Created Half Adder: {self.half_adder}")
        
        # Test 1: Functional Correctness (Truth Table)
        print("\n--- Test 1: Truth Table Validation ---")
        functional_passed = self._test_truth_table()
        
        # Test 2: Performance Measurement
        print("\n--- Test 2: Performance Measurement ---")
        perf_results = self._test_performance()
        
        # Test 3: S-Coordinate Aware Operation
        print("\n--- Test 3: S-Coordinate Operation ---")
        s_coord_results = self._test_s_coordinate_operation()
        
        # Aggregate validation
        all_passed = (
            functional_passed and
            perf_results['within_target'] and
            s_coord_results['valid']
        )
        
        self.set_validation(
            passed=all_passed,
            functional_correct=functional_passed,
            performance_acceptable=perf_results['within_target'],
            s_coordinate_valid=s_coord_results['valid']
        )
        
        # Set comparison with theoretical predictions
        self.set_comparison(
            theoretical_operations=4,  # 1 XOR + 1 AND per test case
            measured_operations=self.half_adder.operation_count,
            theoretical_latency_ns=100,  # <100 ns target per operation
            measured_latency_ns=perf_results['mean_latency_ns']
        )
        
        return self.results["results"]
    
    def _test_truth_table(self) -> bool:
        """Test all 4 input combinations against truth table."""
        test_cases = [
            # (A, B, expected_sum, expected_carry)
            (False, False, False, False),
            (False, True, True, False),
            (True, False, True, False),
            (True, True, False, True)
        ]
        
        all_correct = True
        
        for trial, (a, b, exp_sum, exp_carry) in enumerate(test_cases):
            # Execute addition
            sum_bit, carry_bit = self.half_adder.add(a, b)
            
            # Check correctness
            correct = (sum_bit == exp_sum) and (carry_bit == exp_carry)
            all_correct = all_correct and correct
            
            # Record measurement
            self.add_measurement(
                trial=trial,
                input_a=int(a),
                input_b=int(b),
                output_sum=int(sum_bit),
                output_carry=int(carry_bit),
                expected_sum=int(exp_sum),
                expected_carry=int(exp_carry),
                correct=correct
            )
            
            status = "✅" if correct else "❌"
            print(f"  Test {trial}: A={int(a)}, B={int(b)} → Sum={int(sum_bit)}, Carry={int(carry_bit)} {status}")
        
        accuracy = sum(1 for m in self.results["results"]["measurements"] if m["correct"]) / len(test_cases)
        
        self.set_statistics(
            truth_table_accuracy=accuracy,
            correct_outputs=sum(1 for m in self.results["results"]["measurements"] if m["correct"]),
            total_tests=len(test_cases)
        )
        
        print(f"\nTruth table accuracy: {accuracy:.1%}")
        return all_correct
    
    def _test_performance(self) -> Dict[str, Any]:
        """Measure operation latency."""
        num_trials = 1000
        latencies = []
        
        print(f"  Running {num_trials} operations...")
        
        for i in range(num_trials):
            # Random inputs
            import random
            a = random.choice([True, False])
            b = random.choice([True, False])
            
            # Time the operation
            start = time.perf_counter()
            _, _ = self.half_adder.add(a, b)
            end = time.perf_counter()
            
            latency_ns = (end - start) * 1e9
            latencies.append(latency_ns)
        
        # Calculate statistics
        import numpy as np
        mean_latency = np.mean(latencies)
        std_latency = np.std(latencies)
        min_latency = np.min(latencies)
        max_latency = np.max(latencies)
        
        # Target: <100 ns per operation
        within_target = mean_latency < 100.0
        
        self.set_statistics(
            mean_latency_ns=mean_latency,
            std_latency_ns=std_latency,
            min_latency_ns=min_latency,
            max_latency_ns=max_latency,
            performance_target_ns=100.0,
            within_target=within_target
        )
        
        print(f"  Mean latency: {mean_latency:.1f} ns")
        print(f"  Std latency: {std_latency:.1f} ns")
        print(f"  Range: {min_latency:.1f} - {max_latency:.1f} ns")
        print(f"  Target (<100 ns): {'✅ MET' if within_target else '❌ MISSED'}")
        
        return {
            'mean_latency_ns': mean_latency,
            'within_target': within_target
        }
    
    def _test_s_coordinate_operation(self) -> Dict[str, Any]:
        """Test operation with psychons (S-coordinate aware)."""
        print("  Testing with psychons...")
        
        # Create psychons at different frequencies
        psychon_0 = create_psychon_from_signature(120.0, amplitude=0.0)  # Represents 0
        psychon_0.id = "input_0"
        
        psychon_1 = create_psychon_from_signature(240.0, amplitude=1.0)  # Represents 1
        psychon_1.id = "input_1"
        
        # Test: 1 + 1 = 0 (sum), 1 (carry)
        sum_psychon, carry_psychon = self.half_adder.add_with_psychons(psychon_1, psychon_1)
        
        # Verify S-coordinates are present
        valid = (
            sum_psychon is None and  # Sum=0 → None
            carry_psychon is not None and  # Carry=1 → psychon
            hasattr(carry_psychon, 's_knowledge')
        )
        
        if carry_psychon:
            print(f"  Carry psychon S-coords: ({carry_psychon.s_knowledge:.2f}, {carry_psychon.s_time:.2f}, {carry_psychon.s_entropy:.2f})")
        
        self.set_statistics(
            s_coordinate_operation_valid=valid,
            carry_psychon_present=carry_psychon is not None
        )
        
        print(f"  S-coordinate operation: {'✅ VALID' if valid else '❌ INVALID'}")
        
        return {'valid': valid}
    
    def get_category(self) -> str:
        """Half Adder is a combinational circuit."""
        return "circuits/combinational"


# Run validation
if __name__ == "__main__":
    print("="*60)
    print("HALF ADDER VALIDATION TEST")
    print("="*60)
    print("\nThis test validates the first combinational circuit")
    print("and serves as a template for future circuit validations.")
    print("\nAll results will be saved to JSON for future analysis.")
    
    # Create and execute test
    test = HalfAdderValidation()
    
    # Run with configuration
    filepath = test.execute(
        component="HalfAdder",
        gates_used=["XOR", "AND"],
        complexity="O(1)",
        theoretical_delay="<100ns"
    )
    
    # Print final status
    print("\n" + "="*60)
    print("VALIDATION COMPLETE")
    print("="*60)
    
    results = test.results
    if results["results"]["validation"]["passed"]:
        print("\n✅ ALL TESTS PASSED")
        print("\nHalf Adder is:")
        print("  ✅ Functionally correct (truth table 100%)")
        print("  ✅ Performance acceptable (<100 ns)")
        print("  ✅ S-coordinate aware (tri-dimensional)")
    else:
        print("\n❌ SOME TESTS FAILED")
        print("\nReview saved results for details:")
        print(f"  {filepath}")
    
    print("\nNext steps:")
    print("1. Review saved results JSON")
    print("2. Build Full Adder")
    print("3. Compare Half Adder performance across runs")

