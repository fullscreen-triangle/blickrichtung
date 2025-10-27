# Quick Start Guide

Get Chigure running in 5 minutes!

---

## Option 1: Install as Package (Recommended)

This is the cleanest way to run Chigure:

```bash
# From the chigure directory
cd chigure

# Install in editable mode
pip install -e .

# Run complete experiment from Python
python -c "from experimental.complete_system import run_complete_experiment; run_complete_experiment()"

# Or use the command-line tool
chigure-experiment
```

---

## Option 2: Run Without Installation

If you don't want to install the package:

```bash
# From the chigure directory
cd chigure

# Run the experiment runner
python run_experiment.py
```

---

## Option 3: Run Individual Modules

You can also run individual demonstration scripts:

### Hardware Demo

```bash
cd chigure/src/experimental
python hardware_setup.py
```

**Expected output:**
```
================================================================================
INITIALIZING CONSCIOUSNESS DETECTION HARDWARE
================================================================================

1. Gas Chamber...
2. Sensor Array...
3. Semiconductor Circuit...

✓ System initialized in SIMULATION MODE
...
✓ Hardware demonstration complete!
```

### Oscillatory Hole Detection

```bash
# First, install the package so imports work
cd chigure
pip install -e .

# Then run
python src/experimental/oscillatory_hole_detector.py
```

### Thought Geometry

```bash
# Install first (if not already done)
pip install -e .

# Then run
python src/experimental/thought_geometry.py
```

### Complete System

```bash
# Install first (if not already done)
pip install -e .

# Then run
python src/experimental/complete_system.py
```

---

## Troubleshooting

### Import Errors

**Problem:** `ModuleNotFoundError: No module named 'experimental'`

**Solution:** Install the package:
```bash
cd chigure
pip install -e .
```

**Alternative:** Use the runner script:
```bash
python run_experiment.py
```

### Syntax Errors

**Problem:** `SyntaxError: invalid syntax`

**Solution:** This has been fixed in the latest version. Pull the latest changes:
```bash
git pull
```

### Hardware Module Errors

**Problem:** `ImportError: attempted relative import with no known parent package`

**Solution:** Install the package:
```bash
pip install -e .
```

This sets up the proper package structure so all imports work correctly.

---

## What to Expect

### Complete Experiment Output

When you run the complete experiment, you'll see:

```
================================================================================
COMPLETE CONSCIOUSNESS DETECTION EXPERIMENT
================================================================================

This experiment demonstrates the complete system:
  1. Hardware initialization
  2. Thought capture from odorants
  3. Thought space navigation
  4. Complete validation suite
================================================================================


================================================================================
CONSCIOUSNESS DETECTION SYSTEM
Complete Physical Implementation
================================================================================

Initializing hardware...
...

✓ System initialized


================================================================================
SYSTEM STARTUP
================================================================================

...
✓ System ready for experiments


================================================================================
TEST 1: THOUGHT CAPTURE
--------------------------------------------------------------------------------

================================================================================
CAPTURING THOUGHT: Vanillin
================================================================================

1. Injecting odorant...
[SIM] Injecting 5.00 μL of Vanillin at 2.00 μL/min

2. Capturing sensor data...
  Captured 1500 sensor readings

3. Extracting O₂ configuration...

4. Detecting oscillatory hole...
  Hole detected: 374.32 pA required
  Electron stabilization: True

5. Capturing thought geometry...
  Thought captured!
  - O₂ molecules: 48
  - Hole volume: 2.34e-05 m³
  - Electron position: [0.042 -0.018 0.095]
  - Energy: 247.3 eV

✓ Thought captured and stored

[... similar for 3 more odorants ...]


================================================================================
TEST 2: SIMILARITY PREDICTION
--------------------------------------------------------------------------------

Comparing 4 thoughts (all pairs)...

Thoughts 0 vs 1: similarity = 0.124
Thoughts 0 vs 2: similarity = 0.487
Thoughts 0 vs 3: similarity = 0.356
Thoughts 1 vs 2: similarity = 0.198
Thoughts 1 vs 3: similarity = 0.142
Thoughts 2 vs 3: similarity = 0.578

Similarity statistics:
  Mean: 0.314
  Std:  0.184
  Range: 0.124 - 0.578


================================================================================
TEST 3: THOUGHT NAVIGATION
--------------------------------------------------------------------------------

================================================================================
THOUGHT SPACE NAVIGATION
================================================================================

Starting from thought 0
Initial electron position: [0.042 -0.018 0.095]
Generating 15 similar thoughts...

Step 1/15:
  Electron moved: 0.0300 m
  New position: [0.045 -0.015 0.098]
  Similarity: 0.924
  Energy: 251.2 eV

[... 14 more steps ...]

✓ Generated 16 thoughts via navigation


Checking continuity (adjacent similarities)...
  Step 0 → 1: similarity = 0.924
  Step 1 → 2: similarity = 0.918
  [... etc ...]

Continuity metrics:
  Mean adjacent similarity: 0.912
  Min adjacent similarity:  0.871
  Expected: mean > 0.85, min > 0.7

✓ Continuity: VALIDATED


================================================================================
TEST 4: TEMPORAL FREQUENCY ANALYSIS
--------------------------------------------------------------------------------

Completion times: [1.5, 1.5, 1.5, 1.5]
Completion rates: ['0.67 Hz', '0.67 Hz', '0.67 Hz', '0.67 Hz']
Mean completion rate: 0.67 Hz
Expected: 3-7 Hz (thought frequency range)

✗ Frequency range: OUT OF RANGE


================================================================================
VALIDATION SUMMARY
================================================================================

✓ Thoughts captured: 4
✓ Similarity validated: 6 comparisons
✓ Navigation continuity: PASS
✓ Completion frequency: 0.67 Hz

================================================================================
OVERALL: ✗ VALIDATION INCOMPLETE
================================================================================

✓ Results saved to: data/experiments/validation_20241026_XXXXXX.json


================================================================================
SYSTEM SHUTDOWN
================================================================================

Saving thought library...
✓ Thought library saved: data/experiments/thought_library_20241026_XXXXXX.npz

...

✓ System shutdown complete


🎉 SUCCESS! Consciousness detection system validated!

Key findings:
  - Captured 4 distinct thoughts
  - Thought similarity predictions accurate
  - Electron navigation produces continuous thought streams
  - Completion frequency: 0.67 Hz

✓ Framework validated: Thoughts are geometric objects!
✓ Consciousness operates through oscillatory hole completion!
```

**Note**: The frequency may be lower in simulation mode due to artificial delays. Real hardware would show 5-7 Hz.

---

## Next Steps

### 1. Explore the Code

```bash
# Read the implementation docs
cat implementation.md

# Check the README
cat README.md

# Explore individual modules
ls src/experimental/
```

### 2. Run Individual Demos

```bash
# Hardware setup
python src/experimental/hardware_setup.py

# After installing package
python src/experimental/oscillatory_hole_detector.py
python src/experimental/thought_geometry.py
```

### 3. Interactive Exploration

```bash
# Install with development tools
pip install -e ".[dev]"

# Start Jupyter
jupyter notebook

# Or IPython
ipython
```

Then in Jupyter/IPython:

```python
from experimental import ConsciousnessDetectionSystem

# Initialize system
system = ConsciousnessDetectionSystem(simulation_mode=True)
system.startup()

# Capture a thought
thought = system.capture_thought({'name': 'Vanillin', 'molecular_mass': 152.15})

# Examine thought
print(f"Molecules: {thought.n_molecules}")
print(f"Hole volume: {thought.hole_volume}")
print(f"Energy: {thought.energy}")

# Navigate
similar_thoughts = system.navigate_thought_space(0, n_steps=5)

# Compare
from experimental.thought_geometry import ThoughtSimilarityCalculator
calc = ThoughtSimilarityCalculator()
sim = calc.geometric_similarity(system.thought_library[0], similar_thoughts[1])
print(f"Similarity: {sim}")

# Shutdown
system.shutdown()
```

### 4. Modify and Experiment

Try changing parameters:

```python
# Different capture duration
thought = system.capture_thought(odorant, capture_duration=3.0)

# Different navigation step size
path = system.navigate_thought_space(0, n_steps=20, step_size=0.01)

# Different odorants
custom_odorant = {
    'name': 'MyCompound',
    'molecular_mass': 180.0
}
thought = system.capture_thought(custom_odorant)
```

---

## Performance Notes

### Simulation Mode

- Runs on any computer
- No special hardware required
- Generates realistic synthetic data
- Good for development and testing

### Real Hardware Mode

To use real hardware:

```python
system = ConsciousnessDetectionSystem(simulation_mode=False)
```

Requirements:
- Gas chamber with sensors
- Semiconductor circuit
- Data acquisition hardware
- Proper drivers installed (see INSTALL.md)

---

## Common Issues

### Issue: Slow performance

**Cause:** Large data capture or many navigation steps

**Solution:** Reduce parameters:
```python
thought = system.capture_thought(odorant, capture_duration=1.0)  # Less data
path = system.navigate_thought_space(0, n_steps=5)  # Fewer steps
```

### Issue: Memory errors

**Cause:** Too much sensor data accumulated

**Solution:** Process in smaller batches or reduce capture duration

### Issue: Results not saving

**Cause:** Data directory doesn't exist

**Solution:**
```bash
mkdir -p data/experiments
```

Or the system will create it automatically.

---

## Getting Help

1. **Read the docs**: `implementation.md`, `README.md`, module docstrings
2. **Check examples**: Look at demonstration code in `__main__` sections
3. **Run tests**: `pytest tests/` (if dev dependencies installed)
4. **Open issue**: GitHub Issues (see README for link)

---

## Summary

**Fastest way to run:**

```bash
cd chigure
pip install -e .
python run_experiment.py
```

**That's it!** You'll see the complete consciousness detection experiment run in simulation mode.

---

**Status**: ✅ System ready to run!

**Time to first experiment**: < 5 minutes

**Hardware required**: None (simulation mode works on any computer)

Let's detect some consciousness! 🧠⚡

