# Results Saving Functionality

All molecular and signature modules now save their results to JSON files instead of only printing to console.

## Updated Modules

### 1. Signatures Modules

#### `src/signatures/hardware_signature.py`
- **Added Methods:**
  - `HardwareOscillatorySignature.to_dict()` - Convert signature to JSON-serializable dict
  - `HardwareSignatureGenerator.save_signatures()` - Save individual hardware signatures
  - `HardwareSignatureGenerator.save_combined_signature()` - Save combined signature
  
- **Output Location:** `results/hardware_signatures/`
  - `hardware_signatures.json` - Individual source signatures (CPU, thermal, EM, etc.)
  - `combined_signature.json` - Weighted combination of all sources
  - `molecular_scale_signature.json` - Hardware signature mapped to molecular scale (10¹³ Hz)

#### `src/signatures/molecular_signature.py`
- **Added Methods:**
  - `MolecularOscillatorySignature.to_dict()` - Convert signature to JSON-serializable dict
  - `MolecularSignatureGenerator.save_signatures()` - Save molecular signatures
  - `MolecularSignatureGenerator.save_similarity_matrix()` - Save pairwise similarity matrix
  
- **Output Location:** `results/molecular_signatures/`
  - `molecular_signatures.json` - Oscillatory signatures for all molecules
  - `similarity_matrix.json` - Pairwise distance matrix (Euclidean/Cosine)

### 2. Molecular Analysis Modules

#### `src/molecular/bond_analyzer.py`
- **Added Methods:**
  - `BondProperties.to_dict()` - Convert bond properties to JSON-serializable dict
  - `BondAnalyzer.save_bond_analysis()` - Save complete bond analysis with summary statistics
  
- **Output Location:** `results/bond_analysis/`
  - `{molecule_name}_bonds.json` - All bonds with:
    - Individual bond properties (type, length, frequency, force constant)
    - Summary statistics (average frequency, conjugated bonds, dominant modes)

#### `src/molecular/mass_properties.py`
- **Fixed:** Dataclass field ordering issue (fields with defaults must come after fields without defaults)
- **Added Methods:**
  - `MassProperties.to_dict()` - Convert mass properties to JSON-serializable dict
  - `MassPropertiesCalculator.save_mass_properties()` - Save mass properties
  - `MassPropertiesCalculator.save_isotope_comparison()` - Save H/D isotope comparison
  
- **Output Location:** `results/mass_properties/`
  - `{molecule_name}_mass.json` - Mass properties (MW, exact mass, reduced mass, etc.)
  - `isotope_comparison.json` - Critical test comparing H vs D versions

#### `src/molecular/structure_encoder.py`
- **Added Methods:**
  - `MolecularFeatures.to_dict()` - Convert features to JSON-serializable dict
  - `MolecularStructureEncoder.save_features()` - Save single molecule features
  - `MolecularStructureEncoder.save_batch_features()` - Save batch of molecule features
  
- **Output Location:** `results/structure_encoding/`
  - `molecular_features.json` - Structural features for all molecules:
    - Atom/bond counts
    - Ring statistics
    - 3D geometry (volume, asphericity, eccentricity)

#### `src/molecular/geometry_calculator.py`
- **Added Methods:**
  - `GeometricProperties.to_dict()` - Convert geometry to JSON-serializable dict
  - `GeometryCalculator.save_geometry()` - Save single molecule geometry
  - `GeometryCalculator.save_batch_geometries()` - Save batch of geometries
  
- **Output Location:** `results/geometry/`
  - `molecular_geometries.json` - 3D geometric properties:
    - Center of mass
    - Principal moments of inertia
    - Shape descriptors (asphericity, eccentricity, radius of gyration)
    - Spatial extent (diameter, volume, surface area)

## Output Format

All JSON files follow this structure:

```json
{
  "timestamp": "2025-10-26T...",
  "smiles": "COc1cc(C=O)ccc1O",  // If applicable
  "num_molecules": 5,              // For batch operations
  "data_field": { ... },           // Main data
  "metadata": {                    // Optional
    "description": "...",
    "experiment_params": { ... }
  }
}
```

## Running Demonstrations

Each module can be run independently to generate results:

```bash
# Hardware signatures
python chigure/src/signatures/hardware_signature.py

# Molecular signatures
python chigure/src/signatures/molecular_signature.py

# Bond analysis
python chigure/src/molecular/bond_analyzer.py

# Mass properties (including isotope test)
python chigure/src/molecular/mass_properties.py

# Structure encoding
python chigure/src/molecular/structure_encoder.py

# Geometry calculation
python chigure/src/molecular/geometry_calculator.py
```

## Key Features

1. **Automatic Directory Creation:** Output directories are created automatically
2. **Timestamped Results:** Each file includes ISO timestamp
3. **Metadata Support:** All save functions accept optional metadata dict
4. **Type Conversion:** NumPy types (float64, int64, etc.) automatically converted to Python types for JSON compatibility
5. **Console + File:** Results are both displayed on console AND saved to files
6. **Organized Structure:** Results grouped by module type in `results/` directory

## Integration with Validation Engine

These save functions integrate seamlessly with the main validation pipeline:

```python
from signatures.molecular_signature import MolecularSignatureGenerator
from molecular.bond_analyzer import BondAnalyzer

# Generate signatures
generator = MolecularSignatureGenerator()
signatures = generator.generate_from_smiles("COc1cc(C=O)ccc1O")

# Save results
generator.save_signatures(
    {'vanillin': signatures},
    'results/validation_run_1/signatures.json',
    metadata={'experiment': 'scent_prediction', 'version': '1.0'}
)
```

## Benefits

- **Reproducibility:** All experimental results saved for later analysis
- **Traceability:** Timestamps and metadata track experimental conditions
- **Integration:** JSON format easy to load in Python, R, Julia, web apps
- **Validation:** Saved results can be compared against experimental data
- **Publication:** Results ready for supplementary materials

