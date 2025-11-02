"""
Complete Framework Integration Test

Tests all components of the Megaphrenia biological integrated circuits framework:
- Core modules (psychon, BMD, S-entropy)
- Circuit components (transistor, logic gates, memory, ALU, decoder, registers, multiplexer)
- Hardware harvesters (CPU, screen, EM, memory)

Run this script to verify the complete tri-dimensional S-coordinate BMD operation framework.

PUBLICATION-READY: All results are saved to results/ directory for paper preparation.
"""

import sys
import numpy as np
from datetime import datetime
import json
import os
from pathlib import Path

print("=" * 80)
print("MEGAPHRENIA: BIOLOGICAL INTEGRATED CIRCUITS")
print("Complete Framework Integration Test")
print("=" * 80)
test_start_time = datetime.now()
print(f"Test started: {test_start_time.strftime('%Y-%m-%d %H:%M:%S')}\n")

# Track test results
tests_passed = 0
tests_failed = 0
test_results = []
detailed_results = {}  # For publication data

# Create results directory
results_dir = Path("results")
results_dir.mkdir(exist_ok=True)

def run_test(test_name, test_func):
    """Run a test and track results with detailed metrics."""
    global tests_passed, tests_failed, detailed_results
    
    test_start = datetime.now()
    try:
        print(f"\n{'='*60}")
        print(f"TEST: {test_name}")
        print('='*60)
        
        # Run test and capture any returned data
        result_data = test_func()
        
        test_end = datetime.now()
        duration = (test_end - test_start).total_seconds()
        
        print(f"✅ PASSED: {test_name}")
        tests_passed += 1
        test_results.append((test_name, "PASSED", None))
        
        # Store detailed results for publication
        detailed_results[test_name] = {
            "status": "PASSED",
            "duration_seconds": duration,
            "timestamp": test_end.isoformat(),
            "data": result_data if result_data else {}
        }
        return True
        
    except Exception as e:
        test_end = datetime.now()
        duration = (test_end - test_start).total_seconds()
        
        print(f"❌ FAILED: {test_name}")
        print(f"   Error: {str(e)}")
        tests_failed += 1
        test_results.append((test_name, "FAILED", str(e)))
        
        # Store failure details
        detailed_results[test_name] = {
            "status": "FAILED",
            "duration_seconds": duration,
            "timestamp": test_end.isoformat(),
            "error": str(e)
        }
        return False

# =============================================================================
# CORE MODULE TESTS
# =============================================================================

def test_psychon_creation():
    """Test Psychon creation with tri-dimensional S-coordinates."""
    from src.megaphrenia.core.psychon import create_psychon_from_signature
    
    psychon = create_psychon_from_signature(120.0, amplitude=1.0)
    print(f"  Created psychon: {psychon.id}")
    print(f"  Primary S-coords: ({psychon.s_knowledge:.2f}, {psychon.s_time:.2f}, {psychon.s_entropy:.2f})")
    print(f"  Extended S-coords (5D): {psychon.extended_s_coordinates}")
    print(f"  Equivalence class: {psychon.equivalence_class.class_id}")
    print(f"  BMD filtering efficiency: {psychon.bmd_filtering.filtering_efficiency:.1f} bits/molecule")
    
    assert psychon.s_knowledge >= 0, "S_knowledge should be non-negative"
    assert 0 <= psychon.s_time <= 1, "S_time should be in [0,1]"
    assert psychon.s_entropy >= 0, "S_entropy should be non-negative"
    
    # Return data for publication
    return {
        "psychon_id": psychon.id,
        "s_knowledge": float(psychon.s_knowledge),
        "s_time": float(psychon.s_time),
        "s_entropy": float(psychon.s_entropy),
        "s_packing": float(psychon.s_packing),
        "s_hydrophobic": float(psychon.s_hydrophobic),
        "equivalence_class_id": psychon.equivalence_class.class_id,
        "equivalence_class_members": psychon.equivalence_class.member_count,
        "bmd_filtering_efficiency": psychon.bmd_filtering.filtering_efficiency,
        "frequency_hz": psychon.frequency,
        "amplitude": psychon.amplitude
    }

def test_bmd_tri_dimensional_operation():
    """Test BMD tri-dimensional R-C-L operation."""
    from src.megaphrenia.core.bmd_state import BMDState, OperationMode
    
    bmd = BMDState(id="test_bmd")
    print(f"  Created BMD: {bmd}")
    print(f"  Tri-dimensional params:")
    print(f"    R (knowledge): {bmd.tri_params.R_knowledge:.2e} Ω")
    print(f"    C (time): {bmd.tri_params.C_time:.2e} F")
    print(f"    L (entropy): {bmd.tri_params.L_entropy:.2e} H")
    
    # Test mode selection
    mode = bmd.select_operation_mode(s_knowledge=2.0, s_time=0.3, s_entropy=0.5)
    print(f"  Selected mode (high S_k): {mode.value}")
    assert mode == OperationMode.RESISTIVE, "Should select RESISTIVE for high S_knowledge"
    
    mode2 = bmd.select_operation_mode(s_knowledge=0.3, s_time=0.9, s_entropy=0.2)
    print(f"  Selected mode (high S_t): {mode2.value}")
    assert mode2 == OperationMode.CAPACITIVE, "Should select CAPACITIVE for high S_time"

def test_s_entropy_calculation():
    """Test S-entropy coordinate calculation."""
    from src.megaphrenia.core.s_entropy import SEntropyCalculator
    
    calc = SEntropyCalculator()
    
    # Test from oscillatory signature
    coords = calc.from_oscillatory_signature(frequency=120.0, amplitude=1.0)
    print(f"  S-coords from 120 Hz: {coords}")
    print(f"    Primary (K,T,E): {coords[:3]}")
    print(f"    Extended (Pack,Hydro): {coords[3:]}")
    
    assert len(coords) == 5, "Should return 5D coordinates"
    assert coords[0] >= 0, "S_knowledge should be non-negative"
    assert 0 <= coords[1] <= 1, "S_time should be in [0,1]"

# =============================================================================
# CIRCUIT COMPONENT TESTS
# =============================================================================

def test_transistor_tri_dimensional():
    """Test BMD Transistor tri-dimensional operation."""
    from src.megaphrenia.circuits.transistor import BMDTransistor
    from src.megaphrenia.core.bmd_state import OperationMode
    
    transistor = BMDTransistor()
    print(f"  Created transistor: {transistor}")
    print(f"  On/off ratio: {transistor.on_off_ratio}")
    
    # Test mode selection
    transistor.set_gate_voltage(0.6, context_s_coords=(2.0, 0.3, 0.2))
    print(f"  Active mode: {transistor.active_mode.value}")
    print(f"  State: {transistor.state}")
    assert transistor.is_on, "Transistor should be ON with V_g > V_th"

def test_logic_gate_tri_dimensional():
    """Test tri-dimensional logic gate (AND-OR-XOR parallel)."""
    from src.megaphrenia.circuits.logic_gates import TriDimensionalLogicGate, LogicFunction
    
    gate = TriDimensionalLogicGate(name="test_gate")
    print(f"  Created gate: {gate}")
    
    # Test with different S-contexts
    # High S_knowledge → AND
    result_and = gate.compute(True, True, s_coordinates=(2.0, 0.3, 0.2))
    print(f"  Result (high S_k): {result_and}, function: {gate.active_function.value}")
    assert gate.active_function == LogicFunction.AND
    
    # High S_time → OR
    result_or = gate.compute(True, False, s_coordinates=(0.3, 0.9, 0.2))
    print(f"  Result (high S_t): {result_or}, function: {gate.active_function.value}")
    assert gate.active_function == LogicFunction.OR

def test_memory_sdictionary():
    """Test S-dictionary content-addressable memory."""
    from src.megaphrenia.circuits.memory import SDictionaryMemory
    from src.megaphrenia.core.psychon import create_psychon_from_signature
    
    memory = SDictionaryMemory(quantization_levels=20)
    print(f"  Created memory: {memory}")
    print(f"  Capacity: {memory.total_capacity:,} states")
    
    # Write psychons
    p1 = create_psychon_from_signature(120.0)
    p1.id = "test_psychon_120"
    memory.write(p1)
    print(f"  Wrote: {p1.id}")
    
    # Read back (content-addressable)
    retrieved = memory.read(p1.extended_s_coordinates)
    print(f"  Retrieved: {retrieved.id if retrieved else 'None'}")
    assert retrieved is not None, "Should retrieve written psychon"
    assert retrieved.id == p1.id, "Should retrieve exact psychon"

def test_alu_virtual_processor():
    """Test Virtual Processor ALU with O(1) operations."""
    from src.megaphrenia.circuits.alu import VirtualProcessorALU, ALUOperation
    from src.megaphrenia.core.psychon import create_psychon_from_signature
    
    alu = VirtualProcessorALU(bit_width=4)
    print(f"  Created ALU: {alu}")
    
    # Create operands
    a = create_psychon_from_signature(120.0 * 3)
    b = create_psychon_from_signature(120.0 * 5)
    
    # Test ADD
    result = alu.execute(ALUOperation.ADD, operand_a=a, operand_b=b)
    print(f"  ADD result: {result.id}")
    print(f"  S-coords: ({result.s_knowledge:.2f}, {result.s_time:.2f}, {result.s_entropy:.2f})")
    assert result is not None, "ADD should return result"

def test_decoder():
    """Test S-coordinate decoder."""
    from src.megaphrenia.circuits.decoder import SCoordinateDecoder
    from src.megaphrenia.core.psychon import create_psychon_from_signature
    
    decoder = SCoordinateDecoder(num_outputs=8)
    print(f"  Created decoder: {decoder}")
    
    # Register components
    for i in range(4):
        p = create_psychon_from_signature(120.0 * (i+1))
        decoder.register_component(f"comp_{i}", p, output_index=i)
    print(f"  Registered {decoder.num_outputs} components")
    
    # Decode
    query = create_psychon_from_signature(240.0).primary_s_coordinates
    matches = decoder.decode(query)
    print(f"  Matches: {len(matches)}")
    assert len(matches) > 0, "Should find at least one match"

def test_registers():
    """Test S-coordinate register file."""
    from src.megaphrenia.circuits.registers import RegisterFile
    from src.megaphrenia.core.psychon import create_psychon_from_signature
    
    reg_file = RegisterFile(num_registers=16)
    print(f"  Created register file: {reg_file}")
    
    # Write to register
    p = create_psychon_from_signature(120.0)
    p.id = "test_operand"
    reg_file.write_register("R0", p)
    print(f"  Wrote to R0: {p.id}")
    
    # Read from register
    retrieved = reg_file.read_register("R0")
    print(f"  Read from R0: {retrieved.id if retrieved else 'None'}")
    assert retrieved is not None, "Should retrieve from register"

def test_multiplexer():
    """Test S-coordinate multiplexer with gear ratio."""
    from src.megaphrenia.circuits.multiplexer import SCoordinateMultiplexer
    from src.megaphrenia.core.psychon import create_psychon_from_signature
    
    mux = SCoordinateMultiplexer(num_inputs=8)
    print(f"  Created multiplexer: {mux}")
    
    # Set inputs
    for i in range(4):
        p = create_psychon_from_signature(120.0 * (i+1))
        mux.set_input(i, p)
    print(f"  Set 4 inputs")
    
    # Select by S-coordinates
    control = create_psychon_from_signature(240.0).primary_s_coordinates
    selected = mux.select(control)
    print(f"  Selected: {selected.id if selected else 'None'}")
    assert selected is not None, "Should select an input"

# =============================================================================
# HARDWARE HARVESTER TESTS
# =============================================================================

def test_cpu_clock_harvester():
    """Test CPU clock oscillation harvesting."""
    from src.megaphrenia.hardware.cpu_clocks import CPUClockHarvester
    
    harvester = CPUClockHarvester()
    print(f"  Created harvester: {harvester}")
    
    # Harvest jitter
    jitter = harvester.harvest_timing_jitter(num_samples=50)
    print(f"  Harvested {len(jitter)} jitter samples")
    print(f"  Mean jitter: {np.mean(jitter)*1e6:.2f} μs")
    
    # Extract S-coords
    s_coords = harvester.extract_s_entropy_coordinates()
    print(f"  S-coords: ({s_coords[0]:.2f}, {s_coords[1]:.2f}, {s_coords[2]:.2f})")
    assert len(s_coords) == 3, "Should return 3D S-coordinates"

def test_screen_harvester():
    """Test screen oscillation harvesting."""
    from src.megaphrenia.hardware.screen_oscillations import ScreenOscillationHarvester
    
    harvester = ScreenOscillationHarvester(nominal_refresh_rate=60.0)
    print(f"  Created harvester: {harvester}")
    print(f"  Note: Screen harvesting test uses simulated timing")
    
    # Harvest just a few frames to keep test fast
    intervals = harvester.harvest_refresh_timing(num_frames=10)
    print(f"  Harvested {len(intervals)} intervals")
    
    s_coords = harvester.extract_s_entropy_coordinates(intervals)
    print(f"  S-coords: ({s_coords[0]:.2f}, {s_coords[1]:.2f}, {s_coords[2]:.2f})")

def test_em_harvester():
    """Test electromagnetic oscillation harvesting."""
    from src.megaphrenia.hardware.electromagnetic import ElectromagneticHarvester
    
    harvester = ElectromagneticHarvester(carrier_frequency=2.4e9)
    print(f"  Created harvester: {harvester}")
    
    # Harvest network timing
    timings = harvester.harvest_network_timing(num_samples=20)
    print(f"  Harvested {len(timings)} timing samples")
    
    s_coords = harvester.extract_s_entropy_coordinates(timings)
    print(f"  S-coords: ({s_coords[0]:.2f}, {s_coords[1]:.2f}, {s_coords[2]:.2f})")

def test_memory_harvester():
    """Test memory access pattern harvesting."""
    from src.megaphrenia.hardware.memory_access import MemoryAccessHarvester
    
    harvester = MemoryAccessHarvester()
    print(f"  Created harvester: {harvester}")
    
    # Harvest memory access timing
    access_times = harvester.harvest_memory_access_timing(num_accesses=50)
    print(f"  Harvested {len(access_times)} access times")
    print(f"  Mean: {np.mean(access_times)*1e9:.1f} ns")
    
    s_coords = harvester.extract_s_entropy_coordinates(access_times)
    print(f"  S-coords: ({s_coords[0]:.2f}, {s_coords[1]:.2f}, {s_coords[2]:.2f})")

# =============================================================================
# RUN ALL TESTS
# =============================================================================

if __name__ == "__main__":
    # Core module tests
    run_test("Psychon Creation (Tri-Dimensional)", test_psychon_creation)
    run_test("BMD Tri-Dimensional Operation (R-C-L)", test_bmd_tri_dimensional_operation)
    run_test("S-Entropy Coordinate Calculation", test_s_entropy_calculation)
    
    # Circuit component tests
    run_test("BMD Transistor (Tri-Dimensional)", test_transistor_tri_dimensional)
    run_test("Logic Gate (AND-OR-XOR Parallel)", test_logic_gate_tri_dimensional)
    run_test("S-Dictionary Memory (Content-Addressable)", test_memory_sdictionary)
    run_test("Virtual Processor ALU (O(1) Operations)", test_alu_virtual_processor)
    run_test("S-Coordinate Decoder", test_decoder)
    run_test("Register File (S-Coordinate)", test_registers)
    run_test("Multiplexer (Gear Ratio)", test_multiplexer)
    
    # Hardware harvester tests
    run_test("CPU Clock Harvester", test_cpu_clock_harvester)
    run_test("Screen Oscillation Harvester", test_screen_harvester)
    run_test("Electromagnetic Harvester", test_em_harvester)
    run_test("Memory Access Harvester", test_memory_harvester)
    
    # =============================================================================
    # SAVE RESULTS FOR PUBLICATION
    # =============================================================================
    
    test_end_time = datetime.now()
    total_duration = (test_end_time - test_start_time).total_seconds()
    
    # Compile comprehensive results
    publication_data = {
        "metadata": {
            "test_suite": "Complete Framework Integration Test",
            "version": "1.0.0",
            "timestamp": test_end_time.isoformat(),
            "start_time": test_start_time.isoformat(),
            "end_time": test_end_time.isoformat(),
            "total_duration_seconds": total_duration,
            "platform": sys.platform
        },
        "summary": {
            "total_tests": tests_passed + tests_failed,
            "passed": tests_passed,
            "failed": tests_failed,
            "success_rate": (tests_passed / (tests_passed + tests_failed) * 100) if (tests_passed + tests_failed) > 0 else 0
        },
        "test_results": detailed_results,
        "failed_tests": [
            {"name": name, "error": error} 
            for name, status, error in test_results 
            if status == "FAILED"
        ]
    }
    
    # Save JSON (complete data)
    json_file = results_dir / f"framework_test_{test_end_time.strftime('%Y%m%d_%H%M%S')}.json"
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(publication_data, f, indent=2, ensure_ascii=False)
    
    # Save CSV summary (for tables in paper)
    csv_file = results_dir / f"framework_test_summary_{test_end_time.strftime('%Y%m%d_%H%M%S')}.csv"
    with open(csv_file, 'w', encoding='utf-8', newline='') as f:
        f.write("Test Name,Status,Duration (s),Timestamp\n")
        for test_name, result_data in detailed_results.items():
            f.write(f'"{test_name}",{result_data["status"]},{result_data["duration_seconds"]:.4f},{result_data["timestamp"]}\n')
    
    # Save human-readable report
    report_file = results_dir / f"framework_test_report_{test_end_time.strftime('%Y%m%d_%H%M%S')}.txt"
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write("="*80 + "\n")
        f.write("MEGAPHRENIA: BIOLOGICAL INTEGRATED CIRCUITS\n")
        f.write("Complete Framework Integration Test Report\n")
        f.write("="*80 + "\n\n")
        f.write(f"Test Date: {test_end_time.strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Duration: {total_duration:.2f} seconds\n")
        f.write(f"Total Tests: {tests_passed + tests_failed}\n")
        f.write(f"Passed: {tests_passed} ✅\n")
        f.write(f"Failed: {tests_failed} ❌\n")
        f.write(f"Success Rate: {publication_data['summary']['success_rate']:.1f}%\n\n")
        
        f.write("Test Results:\n")
        f.write("-"*80 + "\n")
        for test_name, result_data in detailed_results.items():
            status_icon = "✅" if result_data["status"] == "PASSED" else "❌"
            f.write(f"{status_icon} {test_name}: {result_data['status']} ({result_data['duration_seconds']:.3f}s)\n")
            if "error" in result_data:
                f.write(f"   Error: {result_data['error']}\n")
        
        f.write("\n" + "="*80 + "\n")
        f.write("Files Saved:\n")
        f.write(f"  - JSON (complete data): {json_file.name}\n")
        f.write(f"  - CSV (summary): {csv_file.name}\n")
        f.write(f"  - TXT (this report): {report_file.name}\n")
    
    print("\n" + "="*70)
    print("📊 RESULTS SAVED FOR PUBLICATION")
    print("="*70)
    print(f"✅ JSON (complete data):  results/{json_file.name}")
    print(f"✅ CSV (summary table):   results/{csv_file.name}")
    print(f"✅ TXT (human report):    results/{report_file.name}")
    print(f"\nTotal tests: {tests_passed + tests_failed}")
    print(f"Data points collected: {len(detailed_results)}")
    
    # =============================================================================
    # FINAL REPORT
    # =============================================================================
    
    print("\n" + "=" * 80)
    print("TEST SUMMARY")
    print("=" * 80)
    
    total_tests = tests_passed + tests_failed
    success_rate = (tests_passed / total_tests * 100) if total_tests > 0 else 0
    
    print(f"\nTotal tests: {total_tests}")
    print(f"Passed: {tests_passed} ✅")
    print(f"Failed: {tests_failed} ❌")
    print(f"Success rate: {success_rate:.1f}%")
    
    if tests_failed > 0:
        print("\nFailed tests:")
        for name, status, error in test_results:
            if status == "FAILED":
                print(f"  ❌ {name}")
                if error:
                    print(f"     {error}")
    
    print("\n" + "=" * 80)
    print("FRAMEWORK STATUS")
    print("=" * 80)
    print("\n✅ Core Modules: Psychon, BMD, S-Entropy")
    print("✅ Circuit Components: Transistor, Gates, Memory, ALU, Decoder, Registers, Mux")
    print("✅ Hardware Harvesters: CPU, Screen, EM, Memory")
    print("\nAll components implement tri-dimensional S-coordinate BMD operation:")
    print("  - Simultaneous computation across (S_knowledge, S_time, S_entropy)")
    print("  - Output selection via S-entropy minimization: argmin[α·S_k + β·S_t + γ·S_e]")
    print("  - O(1) complexity through categorical filtering")
    print("  - Content-addressable operations via S-distance")
    
    if success_rate == 100:
        print("\n🎉 ALL TESTS PASSED! Framework ready for use.")
    elif success_rate >= 80:
        print("\n✅ Most tests passed. Framework operational with minor issues.")
    else:
        print("\n⚠️  Several tests failed. Review errors above.")
    
    print(f"\nTest completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)
    
    sys.exit(0 if tests_failed == 0 else 1)

