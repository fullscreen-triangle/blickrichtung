# Data Visualization Guide

## Quick Start

Visualize all NPY/NPZ files in results directory:

```bash
cd chigure
python visualize_data.py
```

This will:
- Search `results/` for all `.npy` and `.npz` files
- Automatically create appropriate visualizations
- Save plots to `results/visualizations/`

## Usage Examples

### 1. Visualize Specific File

```bash
# Single NPY file
python visualize_data.py results/oxygen_clock/o2_signatures.npy

# NPZ file (multiple arrays)
python visualize_data.py results/experimental/thought_library.npz

# Show interactive plots (pop-up windows)
python visualize_data.py results/oxygen_clock/o2_signatures.npy --no-save
```

### 2. Visualize Entire Directory

```bash
# Visualize all data in a directory
python visualize_data.py results/oxygen_clock/

# Visualize without showing interactive plots (save only)
python visualize_data.py results/oxygen_clock/ --no-show
```

### 3. Custom Output Directory

```bash
python visualize_data.py --output my_visualizations/
```

## Automatic Plot Selection

The tool intelligently selects visualizations based on data structure:

### 1D Arrays (Vectors)
- **Line plot**: Trend over indices
- **Histogram**: Distribution of values
- **Box plot**: Quartiles and outliers
- **Statistics table**: Mean, std, min, max, percentiles

**Example files:**
- Time series data
- Single feature vectors
- State sequences

### 2D Arrays (Matrices)

#### Signature Matrices (n × 5, n × small)
- **Feature distributions**: Histogram for each column
- **Correlation heatmap**: Inter-feature correlations

**Example files:**
- `o2_signatures.npy` - [1452, 5] O₂ state signatures
- `molecular_signatures.npy` - [n_molecules, 5] signatures

#### Similarity Matrices (n × n, symmetric)
- **Similarity heatmap**: Full matrix visualization
- **Distribution**: Histogram of pairwise similarities
- **Statistics**: Mean, std, min, max of similarities

**Example files:**
- `similarity_matrix.npy` - Pairwise distances
- Correlation matrices
- Distance matrices

#### General Matrices
- **Heatmap**: Color-coded visualization
- **Color bar**: Value scale

### 3D Arrays (Tensors)
- **Slice visualization**: Representative slices along each dimension

**Example files:**
- 3D thought geometries
- Multi-channel data

## Output Files

All visualizations saved to `results/visualizations/` by default:

```
results/visualizations/
├── o2_signatures_signatures.png      # Signature matrix plots
├── similarity_matrix_similarity.png  # Similarity matrix plots
├── timeseries_1d.png                 # 1D array plots
└── tensor_3d_slices.png              # 3D array slices
```

High resolution (300 DPI) PNG format, suitable for publications.

## Metadata Integration

If a `.json` file exists with the same name as the `.npy` file, it will be loaded automatically:

```
results/oxygen_clock/
├── o2_signatures.npy       # Binary data
└── o2_signatures.json      # Metadata (shape, columns, description)
```

Metadata provides:
- Column names for signature matrices
- Data descriptions
- Units and scales
- Creation timestamps

## Command-Line Options

```
python visualize_data.py [path] [options]

Arguments:
  path              Path to .npy/.npz file or directory (optional)
                    If not provided, searches results/ directory

Options:
  --no-show         Do not show interactive plots (save only)
  --no-save         Do not save plots (show only)
  --output DIR      Custom output directory (default: results/visualizations)
  -h, --help        Show help message
```

## Python API

Use programmatically in your own scripts:

```python
from visualize_data import DataVisualizer

# Initialize
viz = DataVisualizer(output_dir="my_plots/")

# Visualize single file
viz.visualize_npy("results/oxygen_clock/o2_signatures.npy", 
                  show=True, save=True)

# Visualize NPZ file
viz.visualize_npz("results/experimental/thought_library.npz",
                  show=False, save=True)

# Visualize entire directory
viz.auto_visualize_directory("results/", show=False, save=True)

# Load data manually
array, metadata = viz.load_npy("data.npy")
print(f"Loaded array with shape: {array.shape}")
```

## Data Types Handled

### From Core Modules

**Oxygen Clock:**
- `o2_signatures.npy` - [n_states, 5] signature matrix
- Each row: [frequency, amplitude, phase, damping, symmetry]

**S-Entropy:**
- `sentropy_coordinates.json` - Coordinates (JSON, not NPY)
- `similarity_matrix.npy` - [n, n] distance matrix

**BMDs:**
- `bmd_geometries.npz` - Multiple arrays:
  - `o2_positions` - [n_molecules, 3]
  - `hole_centers` - [n_bmds, 3]
  - etc.

**Signatures:**
- `oscillatory_signatures.json` - Signatures (JSON)
- `similarity_matrix.npy` - [n, n] resonance matrix

### From Molecular Modules

- `molecular_features.json` - Features (JSON)
- `bond_analysis.json` - Bond properties (JSON)
- Geometry data typically in JSON format

### From Experimental Modules

- `thought_library.npz` - Multiple arrays:
  - `o2_positions` - 3D arrays
  - `signatures` - 2D arrays
  - etc.

## Troubleshooting

### No plots appear
- Use `--no-show` to save without displaying
- Check that matplotlib backend is configured correctly

### "File not found" error
- Verify path is correct
- Use relative path from `chigure/` directory
- Check file extension (.npy vs .npz)

### Memory errors with large files
- The tool loads entire arrays into memory
- For very large files (>1GB), consider subsampling first

### Matplotlib backend issues
```python
# Add to top of script if needed
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend
```

## Best Practices

1. **Always save metadata JSON** with your NPY files:
   ```python
   np.save("data.npy", array)
   
   metadata = {
       'shape': list(array.shape),
       'dtype': str(array.dtype),
       'description': 'O₂ state signatures',
       'columns': ['frequency', 'amplitude', 'phase', 'damping', 'symmetry']
   }
   
   with open("data.json", 'w') as f:
       json.dump(metadata, f, indent=2)
   ```

2. **Use descriptive filenames**:
   - Good: `o2_signatures_310K.npy`
   - Bad: `data.npy`

3. **Organize by module**:
   ```
   results/
   ├── oxygen_clock/
   ├── sentropy/
   ├── bmds/
   └── signatures/
   ```

4. **Keep visualizations separate**:
   - Data: `results/*/`
   - Plots: `results/visualizations/`

## Examples

### Visualize O₂ Signatures

```bash
cd chigure

# Run oxygen clock demo (generates o2_signatures.npy)
python src/core/oxygen_categorical_clock.py

# Visualize the signatures
python visualize_data.py results/oxygen_clock/o2_signatures.npy
```

Creates:
- Histogram for each signature component
- Correlation heatmap between components
- Saved to `results/visualizations/o2_signatures_signatures.png`

### Visualize Similarity Matrix

```bash
# Run molecular signature demo
python src/signatures/molecular_signature.py

# Visualize similarity matrix
python visualize_data.py results/molecular_signatures/
```

Creates:
- Heatmap of pairwise similarities
- Distribution of similarity values
- Statistics overlay

### Batch Visualize Everything

```bash
# Run all demonstrations
python run_core_demonstrations.py

# Visualize all results
python visualize_data.py
```

Searches entire `results/` tree and visualizes everything found.

---

**Tip**: Start with `python visualize_data.py --no-show` to generate all plots without pop-ups, then review saved images in `results/visualizations/`.

