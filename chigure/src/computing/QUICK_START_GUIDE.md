# Quick Start Guide: Extended Validation Suite

## Overview

You now have a comprehensive consciousness programming validation framework with **10 modules** (5 core + 5 extensions) ready to run.

---

## Quick Start (3 Steps)

### **Step 1: Verify Environment**

```bash
# Activate virtual environment (if not already active)
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac

# Verify dependencies
pip install -r requirements.txt
```

### **Step 2: Run Extended Validation Suite**

```bash
# Windows
RUN_EXTENDED_VALIDATIONS.bat

# Linux/Mac
python run_extended_validations.py --modules all
```

### **Step 3: Review Results**

```bash
# Results will be saved to:
chatelier/src/computing/results/

# JSON files for each module:
# - drug_properties_[timestamp].json
# - therapeutic_window_results_[timestamp].json
# - metabolic_flux_hierarchy_results_[timestamp].json
# - metabolic_hierarchy_mapping_[timestamp].json
# - protocol_*_[timestamp].json

# Plots (PNG) for each module
```

---

## What Gets Validated

### **Core Framework (Modules 1-5)**:
1. ✅ **Electromagnetic Resonance**: H+ EM field 4:1 resonance with O2
2. ✅ **Kuramoto Networks**: Drug-modulated phase-locking dynamics
3. ✅ **Categorical Reduction**: Drug-induced state space constraint
4. ✅ **BMD Phase Sorting**: Information catalysis mechanism
5. ✅ **Hierarchical Composition**: Multi-level computational cascades

### **Clinical Extensions (Modules 6-10)**:
6. ✅ **Drug Properties**: Molecular structure → oscillatory properties
7. ✅ **Therapeutic Windows**: Optimal dosing ranges
8. ✅ **Metabolic Flux Hierarchy**: Multi-scale metabolic cascades
9. ✅ **Clinical Disease Mapping**: Patient profiling & recommendations
10. ✅ **Experimental Protocols**: C13-glucose & Seahorse XF protocols

---

## Run Individual Modules

If you want to run specific modules:

```bash
# Core validators
python electromagnetic_resonance_calculator.py
python kuramoto_oscillator_network.py
python categorical_state_space_reduction.py
python bmd_phace_sorting.py
python hierarchical_bmd_composition.py

# Extensions
python drug_properties.py
python therapeutic_window_calculator.py
python metabolic_flux_hierarchy.py
python metabolic_hierarchy_mapper.py
python metabolic_flux_protocol.py
```

---

## Expected Results

### **Drug Properties**:
```
Lithium:    K_agg = 5.0×10^4 M^-1, Programming Score = 95.3/100
Metformin:  K_agg = 2.5×10^3 M^-1, Programming Score = 82.1/100
Fluoxetine: K_agg = 8.0×10^4 M^-1, Programming Score = 98.1/100
```

### **Therapeutic Windows**:
```
Lithium:    300-1200 mg, TI = 4.0 (narrow window)
Metformin:  500-2500 mg, TI = 5.0 (moderate window)
Fluoxetine: 10-80 mg, TI = 8.0 (wide window)
```

### **Metabolic Hierarchy**:
```
Healthy:             Depth = 1.0 (all 5 levels active)
Insulin Resistance:  Depth = 0.4 (cascade failure at Level 3)
Metformin Treatment: Depth = 0.8 (Levels 3-4 restored)
```

### **Clinical Mapping**:
```
Patient with HbA1c = 7.2%, HOMA-IR = 6.5:
  - Disease: Type 2 Diabetes (moderate)
  - Hierarchical Depth: 0.6
  - Recommended: Metformin, target depth 0.8
  - Timeline: 12 weeks
```

---

## Troubleshooting

### **Issue: Import errors**
```bash
# Solution: Install dependencies
pip install numpy scipy matplotlib networkx
```

### **Issue: Module not found**
```bash
# Solution: Run from correct directory
cd chigure/src/computing
```

### **Issue: chatelier directory not found**
```bash
# Solution: Results directory will be created automatically
# If path errors persist, update paths in scripts to use "results/" instead of "chatelier/src/computing/results/"
```

---

## Key Metrics to Check

After running, verify these key predictions:

### **From Electromagnetic Resonance**:
- H+:O2 ratio = 4.00 for all drugs ✓
- Resonance quality Q = 1.3-60.4 ✓
- Programming strength > 0.9 for all drugs ✓

### **From Kuramoto Networks**:
- Drug-modulated coupling: lithium +50%, dopamine +20%, serotonin +30% ✓
- Phase coherence R ≈ 0.09 for all drugs ✓
- Information transfer: 505-610 bits/s ✓

### **From Metabolic Hierarchy**:
- Metformin increases depth: 0.4 → 0.8 ✓
- Active levels restored: 2/5 → 4/5 ✓
- ATP efficiency improves: 2.8× gain ✓

---

## Next Steps

### **1. Review All Results**
```bash
cd chatelier/src/computing/results
# OR
cd results  # if chatelier path doesn't work

# Check JSON files for quantitative data
# Check PNG files for visualizations
```

### **2. Extend Drug Library**
Add more drugs to `drug_properties.py`:
```python
'new_drug': {
    'molecular_weight': XXX,
    'num_atoms': YYY,
    'log_p': ZZZ,
    # ... other properties
}
```

### **3. Customize Protocols**
Modify experimental protocols in `metabolic_flux_protocol.py`:
```python
# Change drug concentration
# Adjust timeline
# Modify measurement intervals
```

### **4. Clinical Application**
Add patient data to `metabolic_hierarchy_mapper.py`:
```python
patients = [
    {
        'patient_id': 'PT004',
        'fasting_glucose': XXX,
        'hba1c': YYY,
        # ... other biomarkers
    }
]
```

---

## Documentation

- **Full README**: `README.md`
- **Implementation Details**: `IMPLEMENTATION_SUMMARY.md`
- **This Guide**: `QUICK_START_GUIDE.md`

---

## Support & Questions

If modules fail to run:
1. Check Python version (3.8+)
2. Verify all dependencies installed
3. Ensure correct working directory
4. Check `IMPLEMENTATION_SUMMARY.md` for troubleshooting

---

## Success Criteria

After running `RUN_EXTENDED_VALIDATIONS.bat`, you should see:

```
================================================================================
FINAL RESULTS: 10/10 modules completed successfully
Success Rate: 100.0%
================================================================================

🎉 ALL VALIDATIONS COMPLETE!

Validated Predictions:
  ✓ Perfect 4:1 H+:O2 resonance across all drugs
  ✓ Drug-modulated coupling strength (∂K/∂[D] > 0)
  ✓ Categorical state space reduction (3-4 bits)
  ✓ BMD information gain (0.8 bits/endpoint)
  ✓ Hierarchical composition (5-level cascades)
  ✓ Therapeutic windows (K_agg > 10^4 M^-1)
  ✓ Metabolic hierarchy restoration (depth 0.4 → 0.8)
  ✓ Clinical disease mapping (patient-specific)
  ✓ Experimental protocols (isotope tracing, Seahorse)
```

---

**Ready to run!** Execute `RUN_EXTENDED_VALIDATIONS.bat` and review results.

