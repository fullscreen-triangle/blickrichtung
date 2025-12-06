Metabolic Flux Hierarchy Analyzer
Multi-Scale Information Cascades Through Metabolic Pathways
================================================================================

============================================================
Condition: BASELINE
============================================================
Active Levels:                 5/5
Hierarchical Depth:            1.00
End-to-End Flux Ratio:         0.298
Total Info Compression:        7.29 bits
Total ATP Cost:                1722.1 ATP
ATP Efficiency:                4.234 bits/kATP

Level-by-Level Breakdown:
  L1 Glucose_Transport         ✓  Flux:  100.0  Info: 8.00 bits  ATP:  100.0
  L2 Glycolysis                ✓  Flux:   80.0  Info: 5.12 bits  ATP:  160.0
  L3 TCA_Cycle                 ✓  Flux:   60.8  Info: 2.96 bits  ATP:    0.0
  L4 Oxidative_Phosphorylation ✓  Flux:   43.8  Info: 1.53 bits  ATP: -1313.3
  L5 Gene_Expression           ✓  Flux:   29.8  Info: 0.71 bits  ATP:  148.8

============================================================
Condition: METFORMIN
============================================================
Active Levels:                 5/5
Hierarchical Depth:            1.00
End-to-End Flux Ratio:         0.617
Total Info Compression:        4.95 bits
Total ATP Cost:                2870.0 ATP
ATP Efficiency:                1.725 bits/kATP

Level-by-Level Breakdown:
  L1 Glucose_Transport         ✓  Flux:  100.0  Info: 8.00 bits  ATP:  100.0
  L2 Glycolysis                ✓  Flux:   96.0  Info: 7.37 bits  ATP:  192.0
  L3 TCA_Cycle                 ✓  Flux:   87.6  Info: 6.13 bits  ATP:    0.0
  L4 Oxidative_Phosphorylation ✓  Flux:   75.6  Info: 4.58 bits  ATP: -2269.3
  L5 Gene_Expression           ✓  Flux:   61.7  Info: 3.05 bits  ATP:  308.6

============================================================
Condition: INSULIN_RESISTANCE
============================================================
Active Levels:                 5/5
Hierarchical Depth:            1.00
End-to-End Flux Ratio:         0.039
Total Info Compression:        7.99 bits
Total ATP Cost:                499.0 ATP
ATP Efficiency:                16.010 bits/kATP

Level-by-Level Breakdown:
  L1 Glucose_Transport         ✓  Flux:  100.0  Info: 8.00 bits  ATP:  100.0
  L2 Glycolysis                ✓  Flux:   48.0  Info: 1.84 bits  ATP:   96.0
  L3 TCA_Cycle                 ✓  Flux:   21.9  Info: 0.38 bits  ATP:    0.0
  L4 Oxidative_Phosphorylation ✓  Flux:    9.5  Info: 0.07 bits  ATP: -283.7
  L5 Gene_Expression           ✓  Flux:    3.9  Info: 0.01 bits  ATP:   19.3

============================================================
Condition: LITHIUM
============================================================
Active Levels:                 5/5
Hierarchical Depth:            1.00
End-to-End Flux Ratio:         0.298
Total Info Compression:        7.29 bits
Total ATP Cost:                1722.1 ATP
ATP Efficiency:                4.234 bits/kATP

Level-by-Level Breakdown:
  L1 Glucose_Transport         ✓  Flux:  100.0  Info: 8.00 bits  ATP:  100.0
  L2 Glycolysis                ✓  Flux:   80.0  Info: 5.12 bits  ATP:  160.0
  L3 TCA_Cycle                 ✓  Flux:   60.8  Info: 2.96 bits  ATP:    0.0
  L4 Oxidative_Phosphorylation ✓  Flux:   43.8  Info: 1.53 bits  ATP: -1313.3
  L5 Gene_Expression           ✓  Flux:   29.8  Info: 0.71 bits  ATP:  148.8

  ================================================================================
Metabolic Hierarchy Mapper
Clinical Mapping of Disease to Hierarchical Dysfunction
================================================================================

============================================================
Patient: PT001
============================================================
Age: 55, Sex: M, BMI: 32.5
Fasting Glucose:               145 mg/dL
HbA1c:                         7.2%
Insulin:                       18.5 μU/mL
HOMA-IR:                       6.62
Metabolic Syndrome Score:      5/5
Hierarchical Depth Estimate:   0.12
Disease State:                 type_2_diabetes (moderate)

Hierarchical Mapping:
Current Depth:                 0.12
Target Depth:                  0.80
Depth Deficit:                 0.68
Primary Pathway Affected:      Glucose_Transport

Dysfunction Pattern:
  L1 Glucose_Transport         ✗  Severity: 0.70
  L2 Glycolysis                ✗  Severity: 0.60
  L3 TCA_Cycle                 ✗  Severity: 0.50
  L4 Oxidative_Phosphorylation ✓  Severity: 0.20
  L5 Gene_Expression           ✓  Severity: 0.10

Therapeutic Recommendation:
Recommended Drug:              metformin
Expected Timeline:             12 weeks
Monitoring Frequency:          quarterly

============================================================
Patient: PT002
============================================================
Age: 48, Sex: F, BMI: 28.3
Fasting Glucose:               105 mg/dL
HbA1c:                         6.0%
Insulin:                       14.2 μU/mL
HOMA-IR:                       3.68
Metabolic Syndrome Score:      4/5
Hierarchical Depth Estimate:   0.30
Disease State:                 metabolic_syndrome (moderate)

Hierarchical Mapping:
Current Depth:                 0.30
Target Depth:                  0.70
Depth Deficit:                 0.40
Primary Pathway Affected:      Multiple

Dysfunction Pattern:
  L1 Glucose_Transport         ✗  Severity: 0.50
  L2 Glycolysis                ✗  Severity: 0.60
  L3 TCA_Cycle                 ✗  Severity: 0.70
  L4 Oxidative_Phosphorylation ✗  Severity: 0.50
  L5 Gene_Expression           ✓  Severity: 0.20

Therapeutic Recommendation:
Recommended Drug:              metformin
Expected Timeline:             24 weeks
Monitoring Frequency:          quarterly

============================================================
Patient: PT003
============================================================
Age: 35, Sex: M, BMI: 23.1
Fasting Glucose:               88 mg/dL
HbA1c:                         5.2%
Insulin:                       6.5 μU/mL
HOMA-IR:                       1.41
Metabolic Syndrome Score:      0/5
Hierarchical Depth Estimate:   1.00
Disease State:                 healthy (none)

Hierarchical Mapping:
Current Depth:                 1.00