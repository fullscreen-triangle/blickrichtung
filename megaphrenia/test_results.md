MEGAPHRENIA: BIOLOGICAL INTEGRATED CIRCUITS
Complete Framework Integration Test
================================================================================
Test started: 2025-10-28 02:11:39


============================================================
TEST: Psychon Creation (Tri-Dimensional)
============================================================
  Created psychon: psychon_78ce7737
  Primary S-coords: (0.96, 0.82, 1.00)
  Extended S-coords (5D): [0.96040938 0.81583625 0.99687007 0.67369422 0.7149587 ]
  Equivalence class: 120
  BMD filtering efficiency: 1936.8 bits/molecule
✅ PASSED: Psychon Creation (Tri-Dimensional)

============================================================
TEST: BMD Tri-Dimensional Operation (R-C-L)
============================================================
❌ FAILED: BMD Tri-Dimensional Operation (R-C-L)
   Error: Capacitance inconsistent: got 3.18e-07, expected 3.1830988618379067e-13

============================================================
TEST: S-Entropy Coordinate Calculation
============================================================
  S-coords from 120 Hz: [0.03959062 0.81       1.94359088 0.67369422 0.7149587 ]
    Primary (K,T,E): [0.03959062 0.81       1.94359088]
    Extended (Pack,Hydro): [0.67369422 0.7149587 ]
✅ PASSED: S-Entropy Coordinate Calculation

============================================================
TEST: BMD Transistor (Tri-Dimensional)
============================================================
  Created transistor: BMDTransistor(state='off', mode=resistive, on/off=42.1, switches=0, R:0.0%/C:0.0%/L:0.0%)
  On/off ratio: 42.1
  Active mode: inductive
  State: on
✅ PASSED: BMD Transistor (Tri-Dimensional)

============================================================
TEST: Logic Gate (AND-OR-XOR Parallel)
============================================================
  Created gate: TriDimensionalLogicGate(name='test_gate', evals=0, active=and, AND:0.0%/OR:0.0%/XOR:0.0%, score=0.000)
  Result (high S_k): False, function: xor
❌ FAILED: Logic Gate (AND-OR-XOR Parallel)
   Error:

============================================================
TEST: S-Dictionary Memory (Content-Addressable)
============================================================
  Created memory: SDictionaryMemory(capacity=3,200,000, occupied=0, utilization=0.0%, hole_util=0.0%, dims=5D)
  Capacity: 3,200,000 states
  Wrote: test_psychon_120
  Retrieved: test_psychon_120
✅ PASSED: S-Dictionary Memory (Content-Addressable)

============================================================
TEST: Virtual Processor ALU (O(1) Operations)
============================================================
  Created ALU: VirtualProcessorALU(4-bit, ops=0, latency=100ns, K:0.0%/T:0.0%/E:0.0%)
  ADD result: add_t_psychon_1cdf5548_psychon_08159d3b
  S-coords: (0.67, 1.00, 0.80)
✅ PASSED: Virtual Processor ALU (O(1) Operations)

============================================================
TEST: S-Coordinate Decoder
============================================================
  Created decoder: SCoordinateDecoder(outputs=8, components=0, decodes=0, exact_rate=0.0%)
  Registered 8 components
  Matches: 1
✅ PASSED: S-Coordinate Decoder

============================================================
TEST: Register File (S-Coordinate)
============================================================
  Created register file: RegisterFile(registers=16, occupied=0, reads=0, writes=0, hit_rate=0.0%)
  Wrote to R0: test_operand
  Read from R0: test_operand
✅ PASSED: Register File (S-Coordinate)

============================================================
TEST: Multiplexer (Gear Ratio)
============================================================
  Created multiplexer: SCoordinateMultiplexer(inputs=8, connected=0, selects=0, exact_rate=0.0%, gear_applications=0)
  Set 4 inputs
  Selected: psychon_0d5e52b7_mux_out
✅ PASSED: Multiplexer (Gear Ratio)

============================================================
TEST: CPU Clock Harvester
============================================================
  Created harvester: CPUClockHarvester(samples=0, harvests=0, rate=1000.0Hz)
  Harvested 50 jitter samples
  Mean jitter: 0.85 μs
  S-coords: (5.00, 0.00, 1.56)
✅ PASSED: CPU Clock Harvester

============================================================
TEST: Screen Oscillation Harvester
============================================================
❌ FAILED: Screen Oscillation Harvester
   Error: name 'Optional' is not defined

============================================================
TEST: Electromagnetic Harvester
============================================================
  Created harvester: ElectromagneticHarvester(carrier=2.4GHz, samples=0, harvests=0)
  Harvested 20 timing samples
  S-coords: (1.56, 0.13, 0.04)
✅ PASSED: Electromagnetic Harvester

============================================================
TEST: Memory Access Harvester
============================================================
  Created harvester: MemoryAccessHarvester(accesses=0, cache_hit_rate=0.0%, harvests=0)
  Harvested 50 access times
  Mean: 378.0 ns
  S-coords: (1.98, 0.56, 0.79)
✅ PASSED: Memory Access Harvester

================================================================================
TEST SUMMARY
================================================================================

Total tests: 14
Passed: 11 ✅
Failed: 3 ❌
Success rate: 78.6%

Failed tests:
  ❌ BMD Tri-Dimensional Operation (R-C-L)
     Capacitance inconsistent: got 3.18e-07, expected 3.1830988618379067e-13
  ❌ Logic Gate (AND-OR-XOR Parallel)
  ❌ Screen Oscillation Harvester
     name 'Optional' is not defined

================================================================================
FRAMEWORK STATUS
================================================================================

✅ Core Modules: Psychon, BMD, S-Entropy
✅ Circuit Components: Transistor, Gates, Memory, ALU, Decoder, Registers, Mux
✅ Hardware Harvesters: CPU, Screen, EM, Memory

All components implement tri-dimensional S-coordinate BMD operation:
  - Simultaneous computation across (S_knowledge, S_time, S_entropy)
  - Output selection via S-entropy minimization: argmin[α·S_k + β·S_t + γ·S_e]
  - O(1) complexity through categorical filtering
  - Content-addressable operations via S-distance

⚠️  Several tests failed. Review errors above.

Test completed: 2025-10-28 02:11:40