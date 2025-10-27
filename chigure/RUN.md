# How to Run Chigure

## Quick Run (3 commands)

```bash
# 1. Go to chigure directory
cd chigure

# 2. Install (one time only)
pip install -e .

# 3. Run complete experiment
python run_experiment.py
```

Done! ✅

---

## Individual Scripts

After installing (`pip install -e .`), you can run any script:

```bash
# Hardware demo
python src/experimental/hardware_setup.py

# Oscillatory hole detection
python src/experimental/oscillatory_hole_detector.py

# Thought geometry
python src/experimental/thought_geometry.py

# Complete system
python src/experimental/complete_system.py
```

---

## From Python

```python
from experimental.complete_system import run_complete_experiment

results = run_complete_experiment()
```

---

## Command Line Tools

After installation:

```bash
chigure-experiment      # Run complete experiment
chigure-validate        # Run validation suite
```

---

That's it. No complicated setup. Just install and run.

