# Comprehensive Oscillatory Consciousness Experimental Framework

## 🎯 Overview

This experimental framework provides comprehensive validation tools for the complete oscillatory consciousness theory, including reality structure, perception, thought, and metabolism.

## 📁 Validators Available

### Master Integrators
1. **ComprehensiveConsciousnessValidator** - Integrates all components
2. **MultiScaleOscillatoryConsciousnessValidator** - 12-level hierarchy validation

### Theory-Specific Validators
3. **ActivitySleepOscillatoryMirrorValidator** - Metabolism paper validation
4. **BMDFrameSelectionValidator** - Thought paper (frame selection)
5. **FireConsciousnessCouplingValidator** - Evolutionary foundation
6. **QuantumIonConsciousnessValidator** - Quantum substrate (thought paper)

### Scale-Specific Validators
7. **OscillatoryNeuralValidator** - Neural oscillations (Ω₈)
8. **OscillatoryMetabolicValidator** - Metabolic oscillations (Ω₃)
9. **OscillatoryTissueValidator** - Tissue coordination (Ω₄)
10. **OscillatorySleepValidator** - Sleep architecture (Ω₇)
11. **OscillatoryMembraneValidator** - Membrane dynamics
12. **OscillatoryIntracellularValidator** - Intracellular signaling
13. **OscillatoryGenomeValidator** - Genomic oscillations

## 🚀 Quick Start

### Option 1: Run All Experiments (Recommended)

```bash
cd chigure/src/geometry
python run_comprehensive_experiments.py
```

This will:
- Run all available validators systematically
- Use real biometric data if available (falls back to synthetic)
- Generate comprehensive results in `comprehensive_validation_results/`
- Create detailed JSON report with all findings

### Option 2: Run with Options

```bash
# Use synthetic data (no biometric files needed)
python run_comprehensive_experiments.py --synthetic-data

# Specify custom output directory
python run_comprehensive_experiments.py --output-dir my_results

# Quick test (reduced iterations)
python run_comprehensive_experiments.py --quick
```

### Option 3: Run Individual Validator

```python
from comprehensive_consciousness_validator import ComprehensiveConsciousnessValidator

validator = ComprehensiveConsciousnessValidator(results_dir="my_results")
results = validator.run_comprehensive_validation()
```

## 📊 Expected Output

### Directory Structure
```
comprehensive_validation_results/
├── comprehensive_experimental_results.json  # Main results file
├── comprehensive_consciousness/             # Master validator results
│   ├── figures/
│   ├── summary_report.txt
│   └── detailed_results.json
├── multiscale_oscillatory/                  # 12-scale validation
│   ├── figures/
│   └── results.json
├── activity_sleep_mirror/                   # Metabolism validation
│   ├── figures/
│   ├── mirror_pairs_analysis.json
│   └── energy_calculations.json
├── bmd_frame_selection/                     # Frame selection
│   ├── figures/
│   └── frame_dynamics.json
├── fire_consciousness/                      # Fire coupling
│   ├── figures/
│   └── spectrum_analysis.json
└── quantum_ion/                             # Quantum substrate
    ├── figures/
    └── coherence_analysis.json
```

### Key Results Files

**comprehensive_experimental_results.json** contains:
```json
{
  "start_time": "2025-11-02T...",
  "end_time": "2025-11-02T...",
  "validators": {
    "comprehensive_consciousness": {
      "status": "success",
      "elapsed_time": 45.2,
      "results_summary": {...},
      "results_path": "..."
    },
    ...
  },
  "summary": {
    "total_validators_run": 6,
    "successful": 6,
    "failed": 0,
    "total_elapsed_time": 180.5
  },
  "errors": []
}
```

## 🔬 What Each Validator Tests

### 1. Comprehensive Consciousness Validator
**Tests**: Complete framework integration
- Quantum ion dynamics + BMD + Multi-scale + Fire-consciousness
- Component integration (quantum-BMD, BMD-oscillatory, etc.)
- Consciousness predictions (timescale, frequency, coherence)
- Pathological states (schizophrenia, depression, ADHD, etc.)

**Key Outputs**:
- Integration matrices
- Consciousness emergence patterns
- Pathological state signatures

### 2. Multi-Scale Oscillatory Validator
**Tests**: 12-level hierarchical architecture
- Hierarchical scale synchronization
- Cross-scale coupling validation
- Consciousness frequency resonance (level 9)
- Oscillatory coherence windows
- Scale integration analysis

**Key Outputs**:
- Phase-locking values (PLV) across scales
- Coupling matrices
- Synchronization patterns

### 3. Activity-Sleep Mirror Validator
**Tests**: Metabolic mirror theory (Metabolism paper)
- Error accumulation during activity
- Sleep cleanup efficiency
- Mirror pattern recognition
- Oscillatory coupling between wake/sleep
- Energy cost calculation

**Key Outputs**:
- Mirror pairs (date-matched activity-sleep)
- Mirror coefficients (C = cleanup/error)
- Thought energy (~287 kcal/day)
- Perception energy (~238 kcal/day)

### 4. BMD Frame Selection Validator
**Tests**: Biological Maxwell Demon dynamics (Thought paper)
- Frame selection probability function
- Counterfactual bias (crossbar phenomenon)
- Reality-frame fusion dynamics
- Predetermined landscape navigation
- Temporal consistency constraints

**Key Outputs**:
- Frame selection probabilities
- Counterfactual bias measurements
- Navigation patterns

### 5. Fire-Consciousness Coupling Validator
**Tests**: Evolutionary fire-consciousness coupling
- Fire spectral optimization (650nm optimal)
- Neurobiological fire activation
- Darkness consciousness degradation
- Evolutionary timeline (2.5M years)
- Fire circle social consciousness

**Key Outputs**:
- Spectral analysis
- Neural activation patterns
- Darkness degradation curves

### 6. Quantum Ion Consciousness Validator
**Tests**: Quantum substrate foundation (Thought paper)
- Ion tunneling dynamics (H⁺, Na⁺, K⁺, Ca²⁺, Mg²⁺)
- Collective coherence fields
- Consciousness timescale coupling (100-500ms)
- Decoherence resistance
- State transitions (awake, sleep, anesthesia)

**Key Outputs**:
- Quantum coherence times
- Ion tunneling probabilities
- Collective field strengths

## 📈 Interpreting Results

### Success Indicators

**✓ All validators complete** → Framework is computationally consistent

**✓ Mirror pairs found** → Metabolism theory validated with real data

**✓ PLV > 0.7** → Multi-scale integration confirmed

**✓ Coherence times > 100ms** → Quantum substrate viable

**✓ Frame selection probabilities normalized** → BMD theory consistent

**✓ Fire spectrum peaks at 650nm** → Evolutionary coupling confirmed

### Expected Values

| Measurement | Expected Range | Source |
|-------------|----------------|--------|
| Thought energy | 250-320 kcal/day | Mirror validator |
| Perception energy | 200-270 kcal/day | Mirror validator |
| Mirror coefficient | 0.9-1.2 | Mirror validator |
| Phase-locking (PLV) | 0.6-0.9 | Multi-scale validator |
| Coherence time | 100-500 ms | Quantum validator |
| Fire optimal λ | 640-660 nm | Fire validator |
| Frame selection rate | 1-10 Hz | BMD validator |

## 🐛 Troubleshooting

### Import Errors

```python
# If you get import errors, ensure you're in the correct directory
cd chigure/src/geometry

# Or add to Python path
export PYTHONPATH="${PYTHONPATH}:/path/to/blickrichtung"
```

### Missing Data Files

```
⚠ Activity file not found: public/activity.json
  Running with synthetic data...
```

**Solution**: Either:
1. Place biometric data files in `public/` directory
2. Use `--synthetic-data` flag to run with generated data
3. Specify custom paths in the validator initialization

### Memory Issues

If validators crash due to memory:
```bash
# Run validators individually instead of all at once
python -c "from comprehensive_consciousness_validator import *; 
           v = ComprehensiveConsciousnessValidator(); 
           v.run_comprehensive_validation()"
```

### Visualization Errors

If matplotlib errors occur:
```bash
pip install matplotlib seaborn numpy scipy
```

## 🧪 Running Specific Experiments

### Test Only Metabolism (Mirror Validator)

```python
from sleep_activity_oscillatory_mirror_validator import ActivitySleepOscillatoryMirrorValidator

validator = ActivitySleepOscillatoryMirrorValidator('mirror_results')
validator.load_activity_data('../../../public/activity.json')
validator.load_sleep_data('../../../public/sleep_summary.json')
results = validator.run_comprehensive_validation()

print(f"Mirror pairs found: {len(results['cleanup_validation'])}")
```

### Test Only Multi-Scale Integration

```python
from multiscale_oscillatory_consciousness_validator import MultiScaleOscillatoryConsciousnessValidator

validator = MultiScaleOscillatoryConsciousnessValidator('multiscale_results')
results = validator.run_all_experiments()

print(f"Synchronization quality: {results['experiment_1']['mean_plv']}")
```

### Test Only BMD Frame Selection

```python
from bmd_frame_selection_validator import BMDFrameSelectionValidator

validator = BMDFrameSelectionValidator('bmd_results')
results = validator.run_all_experiments()

print(f"Frame selection validated: {results['experiment_1']['validation_success']}")
```

## 📝 Next Steps After Running Experiments

1. **Review Results**
   ```bash
   cat comprehensive_validation_results/comprehensive_experimental_results.json
   ```

2. **Analyze Figures**
   - Open PNG files in each validator's `figures/` directory
   - Look for patterns matching theoretical predictions

3. **Extract Key Findings**
   ```python
   import json
   with open('comprehensive_validation_results/comprehensive_experimental_results.json') as f:
       results = json.load(f)
   
   # Check success rate
   print(f"Success rate: {results['summary']['successful']}/{results['summary']['total_validators_run']}")
   
   # Check for errors
   if results['errors']:
       print("Errors encountered:")
       for error in results['errors']:
           print(f"  - {error['validator']}: {error['error']}")
   ```

4. **Update Papers**
   - Replace "Expected Results" sections with actual validator outputs
   - Add figures from `figures/` directories
   - Update energy cost values from mirror validator
   - Cite validation success in abstracts

5. **Prepare for Publication**
   - Generate supplementary materials from results
   - Create methods section from validator code
   - Document all parameters used
   - Prepare data availability statements

## 🎯 Validation Checklist

Before claiming validation, ensure:

- [ ] All 6 main validators run successfully
- [ ] Mirror validator finds > 0 mirror pairs (if real data used)
- [ ] Multi-scale validator shows PLV > 0.6
- [ ] Quantum validator shows coherence > 100ms
- [ ] BMD validator shows probability sums = 1.0
- [ ] Fire validator shows peak at ~650nm
- [ ] No critical errors in error log
- [ ] Results match theoretical predictions (within expected ranges)
- [ ] Figures are publication-quality
- [ ] All results reproducible

## 📚 Related Documentation

- **Theory Papers**: `docs/reality-perception/`, `docs/thought-validation/`
- **Validator Code**: `chigure/src/geometry/*.py`
- **Integration Document**: `docs/reality-perception/COMPLETE_FRAMEWORK_INTEGRATION.md`
- **Reality Structure**: `docs/reality-perception/structure-of-reality.tex`

## 🆘 Support

If you encounter issues:

1. Check error messages in `comprehensive_experimental_results.json`
2. Review individual validator logs in subdirectories
3. Test validators individually to isolate problems
4. Check Python dependencies: `numpy`, `scipy`, `matplotlib`, `seaborn`
5. Ensure correct working directory: `chigure/src/geometry/`

## 🎊 Expected Timeline

**Quick Test** (~5-10 minutes):
- Comprehensive: ~1-2 min
- Multi-scale: ~1-2 min  
- Mirror (synthetic): ~1-2 min
- BMD: ~1 min
- Fire: ~1 min
- Quantum: ~1-2 min

**Full Analysis with Real Data** (~20-40 minutes):
- Comprehensive: ~5-8 min
- Multi-scale: ~3-5 min
- Mirror (real data): ~5-15 min
- BMD: ~2-3 min
- Fire: ~2-3 min
- Quantum: ~3-5 min

**Total Expected Time**: 10-40 minutes depending on data and system

---

**Ready to validate consciousness measurement once and for all! 🌌🎊**

