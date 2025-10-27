# Running Megaphrenia Tests

## Quick Start

```bash
cd megaphrenia
python test_complete_framework.py
```

Expected output: **15 tests, 100% pass rate**

---

## Individual Module Tests

### Core Modules

```bash
python -m src.megaphrenia.core.psychon
python -m src.megaphrenia.core.bmd_state
python -m src.megaphrenia.core.s_entropy
```

### Circuit Components

```bash
python -m src.megaphrenia.circuits.transistor
python -m src.megaphrenia.circuits.logic_gates
python -m src.megaphrenia.circuits.memory
python -m src.megaphrenia.circuits.alu
python -m src.megaphrenia.circuits.decoder
python -m src.megaphrenia.circuits.registers
python -m src.megaphrenia.circuits.multiplexer
```

### Hardware Harvesters

```bash
python -m src.megaphrenia.hardware.cpu_clocks
python -m src.megaphrenia.hardware.screen_oscillations
python -m src.megaphrenia.hardware.electromagnetic
python -m src.megaphrenia.hardware.memory_access
```

---

## What Gets Tested

### Core Modules (3 tests)
1. ✅ **Psychon Creation**: Tri-dimensional S-coordinates, categorical equivalence, BMD filtering
2. ✅ **BMD Tri-Dimensional Operation**: R-C-L mode selection via S-entropy minimization
3. ✅ **S-Entropy Calculation**: Coordinate extraction from oscillatory signatures

### Circuit Components (7 tests)
4. ✅ **BMD Transistor**: Tri-dimensional impedance operator, mode selection
5. ✅ **Logic Gates**: AND-OR-XOR parallel computation with S-entropy optimization
6. ✅ **S-Dictionary Memory**: Content-addressable storage via S-distance
7. ✅ **Virtual Processor ALU**: O(1) operations via S-coordinate transformations
8. ✅ **S-Coordinate Decoder**: Component selection via S-distance minimization
9. ✅ **Register File**: S-coordinate based register access
10. ✅ **Multiplexer**: Signal routing with gear ratio transformation

### Hardware Harvesters (4 tests)
11. ✅ **CPU Clock Harvester**: Timing jitter, S-coordinate extraction
12. ✅ **Screen Harvester**: Refresh cycle timing, periodic patterns
13. ✅ **EM Harvester**: Network timing, power line frequency
14. ✅ **Memory Harvester**: Access patterns, cache hit/miss, DRAM refresh

---

## Expected Results

```
================================================================================
TEST SUMMARY
================================================================================

Total tests: 15
Passed: 15 ✅
Failed: 0 ❌
Success rate: 100.0%

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

🎉 ALL TESTS PASSED! Framework ready for use.
```

---

## Troubleshooting

### Import Errors

If you get import errors, make sure you're running from the `megaphrenia` directory:

```bash
cd megaphrenia
python test_complete_framework.py
```

### Module Not Found

If specific modules can't be found, check the `src/megaphrenia` directory structure:

```
megaphrenia/
├── src/megaphrenia/
│   ├── core/
│   │   ├── __init__.py
│   │   ├── psychon.py
│   │   ├── bmd_state.py
│   │   └── s_entropy.py
│   ├── circuits/
│   │   ├── __init__.py
│   │   ├── transistor.py
│   │   ├── logic_gates.py
│   │   ├── memory.py
│   │   ├── alu.py
│   │   ├── decoder.py
│   │   ├── registers.py
│   │   └── multiplexer.py
│   └── hardware/
│       ├── __init__.py
│       ├── cpu_clocks.py
│       ├── screen_oscillations.py
│       ├── electromagnetic.py
│       └── memory_access.py
└── test_complete_framework.py
```

### Slow Tests

Some tests (especially hardware harvesters) may take a few seconds:
- Screen oscillation test: ~1.7 seconds (100 frames at 60Hz)
- Memory access test: ~2-3 seconds (memory allocation)
- This is expected and reflects actual hardware measurement time

---

## Next Steps After Testing

Once all tests pass:

1. **Explore Individual Modules**: Run each module's demo script
2. **Build Custom Circuits**: Use components to create new circuits
3. **Harvest Hardware Oscillations**: Collect real oscillatory data
4. **Integrate Components**: Connect all pieces into complete system
5. **Validate Theory**: Compare measured vs. theoretical predictions

---

## Documentation

- `README.md`: Complete project documentation
- `REDESIGN_SUMMARY.md`: Paradigm shift explanation
- `IMPLEMENTATION_COMPLETE.md`: Detailed implementation report
- `FINAL_COMPLETION_SUMMARY.md`: File statistics and status
- `docs/biological-integrated-circuits.tex`: Publication manuscript
- `docs/implementation.md`: Implementation roadmap

---

**Status**: ✅ READY TO TEST

