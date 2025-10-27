"""
Data Visualization Tool for NPY/NPZ Files

Automatically loads and visualizes NumPy binary data with intelligent
detection of data structure and appropriate visualization methods.

Supports:
- .npy files (single array)
- .npz files (multiple arrays)
- Automatic visualization selection based on data shape
- Interactive and saved plots
"""

import numpy as np
import json
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# Set style
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")


class DataVisualizer:
    """Visualize NumPy binary data files."""
    
    def __init__(self, output_dir: str = "results/visualizations"):
        """
        Initialize visualizer.
        
        Args:
            output_dir: Directory to save visualization outputs
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        self.metadata = {}
    
    def load_npy(self, filepath: str) -> Tuple[np.ndarray, Dict]:
        """
        Load .npy file and associated metadata.
        
        Args:
            filepath: Path to .npy file
        
        Returns:
            (array, metadata_dict)
        """
        filepath = Path(filepath)
        
        # Load array
        array = np.load(filepath)
        
        # Try to load metadata JSON
        metadata_path = filepath.with_suffix('.json')
        metadata = {}
        
        if metadata_path.exists():
            with open(metadata_path, 'r') as f:
                metadata = json.load(f)
            print(f"✓ Loaded metadata from {metadata_path}")
        else:
            print(f"  No metadata found at {metadata_path}")
        
        return array, metadata
    
    def load_npz(self, filepath: str) -> Tuple[Dict[str, np.ndarray], Dict]:
        """
        Load .npz file.
        
        Args:
            filepath: Path to .npz file
        
        Returns:
            (dict of arrays, metadata_dict)
        """
        filepath = Path(filepath)
        
        # Load npz
        data = np.load(filepath)
        arrays = {key: data[key] for key in data.files}
        
        # Try to load metadata
        metadata_path = filepath.with_suffix('.json')
        metadata = {}
        
        if metadata_path.exists():
            with open(metadata_path, 'r') as f:
                metadata = json.load(f)
        
        return arrays, metadata
    
    def visualize_npy(self, filepath: str, show: bool = True, save: bool = True):
        """
        Visualize .npy file with automatic plot selection.
        
        Args:
            filepath: Path to .npy file
            show: Show interactive plot
            save: Save plot to file
        """
        print("\n" + "="*80)
        print(f"VISUALIZING: {filepath}")
        print("="*80 + "\n")
        
        # Load data
        array, metadata = self.load_npy(filepath)
        
        print(f"Array shape: {array.shape}")
        print(f"Array dtype: {array.dtype}")
        print(f"Array size: {array.size} elements")
        print(f"Memory: {array.nbytes / 1024:.2f} KB")
        
        if metadata:
            print(f"\nMetadata:")
            for key, value in metadata.items():
                if key != 'columns' and not isinstance(value, (list, dict)):
                    print(f"  {key}: {value}")
        
        # Select visualization based on shape
        if array.ndim == 1:
            self._visualize_1d(array, metadata, filepath, show, save)
        elif array.ndim == 2:
            self._visualize_2d(array, metadata, filepath, show, save)
        elif array.ndim == 3:
            self._visualize_3d(array, metadata, filepath, show, save)
        else:
            print(f"\n⚠ Cannot visualize {array.ndim}D array (too many dimensions)")
    
    def _visualize_1d(self, array: np.ndarray, metadata: Dict, 
                     filepath: Path, show: bool, save: bool):
        """Visualize 1D array."""
        print("\n" + "-"*80)
        print("1D ARRAY VISUALIZATION")
        print("-"*80)
        
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        fig.suptitle(f"1D Array: {filepath.name}", fontsize=16)
        
        # 1. Line plot
        ax = axes[0, 0]
        ax.plot(array, linewidth=1.5)
        ax.set_title("Line Plot")
        ax.set_xlabel("Index")
        ax.set_ylabel("Value")
        ax.grid(True, alpha=0.3)
        
        # 2. Histogram
        ax = axes[0, 1]
        ax.hist(array, bins=50, edgecolor='black', alpha=0.7)
        ax.set_title("Distribution")
        ax.set_xlabel("Value")
        ax.set_ylabel("Frequency")
        ax.grid(True, alpha=0.3)
        
        # 3. Statistics
        ax = axes[1, 0]
        ax.axis('off')
        stats_text = (
            f"Statistics:\n\n"
            f"Count: {len(array)}\n"
            f"Mean: {np.mean(array):.4e}\n"
            f"Std: {np.std(array):.4e}\n"
            f"Min: {np.min(array):.4e}\n"
            f"Max: {np.max(array):.4e}\n"
            f"Median: {np.median(array):.4e}\n"
            f"25th percentile: {np.percentile(array, 25):.4e}\n"
            f"75th percentile: {np.percentile(array, 75):.4e}\n"
        )
        ax.text(0.1, 0.5, stats_text, fontsize=12, family='monospace',
                verticalalignment='center')
        
        # 4. Box plot
        ax = axes[1, 1]
        ax.boxplot(array, vert=True)
        ax.set_title("Box Plot")
        ax.set_ylabel("Value")
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        if save:
            output_path = self.output_dir / f"{filepath.stem}_1d.png"
            plt.savefig(output_path, dpi=300, bbox_inches='tight')
            print(f"✓ Saved to {output_path}")
        
        if show:
            plt.show()
        else:
            plt.close()
    
    def _visualize_2d(self, array: np.ndarray, metadata: Dict,
                     filepath: Path, show: bool, save: bool):
        """Visualize 2D array."""
        print("\n" + "-"*80)
        print("2D ARRAY VISUALIZATION")
        print("-"*80)
        
        rows, cols = array.shape
        print(f"Shape: {rows} rows × {cols} columns")
        
        # Determine if this is a signature matrix or similarity matrix
        is_square = (rows == cols)
        is_symmetric = is_square and np.allclose(array, array.T)
        
        # Get column names if available
        col_names = metadata.get('columns', [f"Col {i}" for i in range(cols)])
        
        if is_symmetric:
            # Similarity/distance matrix
            self._visualize_similarity_matrix(array, metadata, filepath, show, save)
        elif cols <= 10:
            # Small number of columns - show as signature matrix
            self._visualize_signature_matrix(array, col_names, filepath, show, save)
        else:
            # Large matrix - show as heatmap
            self._visualize_heatmap(array, filepath, show, save)
    
    def _visualize_signature_matrix(self, array: np.ndarray, col_names: List[str],
                                   filepath: Path, show: bool, save: bool):
        """Visualize signature matrix (e.g., [n_samples, 5])."""
        rows, cols = array.shape
        
        fig, axes = plt.subplots(2, 3, figsize=(18, 10))
        fig.suptitle(f"Signature Matrix: {filepath.name} ({rows}×{cols})", fontsize=16)
        
        # Plot distribution of each column
        for i in range(min(cols, 5)):
            ax = axes[i // 3, i % 3]
            ax.hist(array[:, i], bins=50, edgecolor='black', alpha=0.7)
            ax.set_title(f"{col_names[i]} Distribution")
            ax.set_xlabel("Value")
            ax.set_ylabel("Frequency")
            ax.grid(True, alpha=0.3)
        
        # Correlation heatmap
        ax = axes[1, 2]
        if rows > 1:
            corr = np.corrcoef(array.T)
            im = ax.imshow(corr, cmap='coolwarm', aspect='auto', vmin=-1, vmax=1)
            ax.set_xticks(range(cols))
            ax.set_yticks(range(cols))
            ax.set_xticklabels(col_names, rotation=45, ha='right')
            ax.set_yticklabels(col_names)
            ax.set_title("Feature Correlations")
            plt.colorbar(im, ax=ax)
        else:
            ax.text(0.5, 0.5, "Need >1 sample\nfor correlations",
                   ha='center', va='center', transform=ax.transAxes)
            ax.axis('off')
        
        plt.tight_layout()
        
        if save:
            output_path = self.output_dir / f"{filepath.stem}_signatures.png"
            plt.savefig(output_path, dpi=300, bbox_inches='tight')
            print(f"✓ Saved to {output_path}")
        
        if show:
            plt.show()
        else:
            plt.close()
    
    def _visualize_similarity_matrix(self, array: np.ndarray, metadata: Dict,
                                    filepath: Path, show: bool, save: bool):
        """Visualize similarity/distance matrix."""
        n = array.shape[0]
        
        fig, axes = plt.subplots(1, 2, figsize=(16, 7))
        fig.suptitle(f"Similarity Matrix: {filepath.name} ({n}×{n})", fontsize=16)
        
        # 1. Heatmap
        ax = axes[0]
        im = ax.imshow(array, cmap='viridis', aspect='auto')
        ax.set_title("Pairwise Similarities")
        ax.set_xlabel("Sample Index")
        ax.set_ylabel("Sample Index")
        plt.colorbar(im, ax=ax, label="Similarity")
        
        # Add grid
        ax.set_xticks(np.arange(0, n, max(1, n//20)))
        ax.set_yticks(np.arange(0, n, max(1, n//20)))
        ax.grid(True, alpha=0.2, color='white', linewidth=0.5)
        
        # 2. Distribution of similarities
        ax = axes[1]
        
        # Get upper triangle (excluding diagonal)
        mask = np.triu(np.ones_like(array, dtype=bool), k=1)
        similarities = array[mask]
        
        ax.hist(similarities, bins=50, edgecolor='black', alpha=0.7)
        ax.set_title("Distribution of Pairwise Similarities")
        ax.set_xlabel("Similarity Value")
        ax.set_ylabel("Frequency")
        ax.grid(True, alpha=0.3)
        
        # Add statistics
        stats_text = (
            f"Statistics (excluding diagonal):\n"
            f"Mean: {np.mean(similarities):.4f}\n"
            f"Std: {np.std(similarities):.4f}\n"
            f"Min: {np.min(similarities):.4f}\n"
            f"Max: {np.max(similarities):.4f}"
        )
        ax.text(0.02, 0.98, stats_text, transform=ax.transAxes,
                fontsize=10, verticalalignment='top',
                bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
        
        plt.tight_layout()
        
        if save:
            output_path = self.output_dir / f"{filepath.stem}_similarity.png"
            plt.savefig(output_path, dpi=300, bbox_inches='tight')
            print(f"✓ Saved to {output_path}")
        
        if show:
            plt.show()
        else:
            plt.close()
    
    def _visualize_heatmap(self, array: np.ndarray, filepath: Path,
                          show: bool, save: bool):
        """Visualize large 2D array as heatmap."""
        rows, cols = array.shape
        
        fig, ax = plt.subplots(figsize=(12, 10))
        fig.suptitle(f"Heatmap: {filepath.name} ({rows}×{cols})", fontsize=16)
        
        im = ax.imshow(array, cmap='viridis', aspect='auto', interpolation='nearest')
        ax.set_xlabel("Column Index")
        ax.set_ylabel("Row Index")
        plt.colorbar(im, ax=ax, label="Value")
        
        plt.tight_layout()
        
        if save:
            output_path = self.output_dir / f"{filepath.stem}_heatmap.png"
            plt.savefig(output_path, dpi=300, bbox_inches='tight')
            print(f"✓ Saved to {output_path}")
        
        if show:
            plt.show()
        else:
            plt.close()
    
    def _visualize_3d(self, array: np.ndarray, metadata: Dict,
                     filepath: Path, show: bool, save: bool):
        """Visualize 3D array (show slices)."""
        print("\n" + "-"*80)
        print("3D ARRAY VISUALIZATION (Slices)")
        print("-"*80)
        
        d0, d1, d2 = array.shape
        print(f"Shape: {d0} × {d1} × {d2}")
        
        # Show slices along each dimension
        fig, axes = plt.subplots(2, 3, figsize=(18, 10))
        fig.suptitle(f"3D Array Slices: {filepath.name}", fontsize=16)
        
        # First dimension slices
        for i, idx in enumerate([0, d0//2, d0-1]):
            ax = axes[0, i]
            im = ax.imshow(array[idx], cmap='viridis', aspect='auto')
            ax.set_title(f"Slice at dim0={idx}")
            plt.colorbar(im, ax=ax)
        
        # Second dimension slices
        for i, idx in enumerate([0, d1//2, d1-1]):
            ax = axes[1, i]
            im = ax.imshow(array[:, idx, :], cmap='viridis', aspect='auto')
            ax.set_title(f"Slice at dim1={idx}")
            plt.colorbar(im, ax=ax)
        
        plt.tight_layout()
        
        if save:
            output_path = self.output_dir / f"{filepath.stem}_3d_slices.png"
            plt.savefig(output_path, dpi=300, bbox_inches='tight')
            print(f"✓ Saved to {output_path}")
        
        if show:
            plt.show()
        else:
            plt.close()
    
    def visualize_npz(self, filepath: str, show: bool = True, save: bool = True):
        """
        Visualize .npz file (multiple arrays).
        
        Args:
            filepath: Path to .npz file
            show: Show interactive plots
            save: Save plots to files
        """
        print("\n" + "="*80)
        print(f"VISUALIZING NPZ: {filepath}")
        print("="*80 + "\n")
        
        arrays, metadata = self.load_npz(filepath)
        
        print(f"Contains {len(arrays)} arrays:")
        for name, arr in arrays.items():
            print(f"  {name}: shape {arr.shape}, dtype {arr.dtype}")
        
        # Visualize each array
        for name, arr in arrays.items():
            print(f"\n{'='*80}")
            print(f"Array: {name}")
            print(f"{'='*80}")
            
            # Create temporary metadata for this array
            arr_metadata = metadata.get(name, {})
            
            # Create temporary path
            temp_path = Path(filepath).parent / f"{Path(filepath).stem}_{name}"
            
            if arr.ndim == 1:
                self._visualize_1d(arr, arr_metadata, temp_path, show, save)
            elif arr.ndim == 2:
                self._visualize_2d(arr, arr_metadata, temp_path, show, save)
            elif arr.ndim == 3:
                self._visualize_3d(arr, arr_metadata, temp_path, show, save)
    
    def auto_visualize_directory(self, directory: str, 
                                 show: bool = False, save: bool = True):
        """
        Auto-visualize all .npy and .npz files in directory.
        
        Args:
            directory: Directory to search
            show: Show interactive plots
            save: Save plots to files
        """
        directory = Path(directory)
        
        # Find all npy and npz files
        npy_files = list(directory.glob("**/*.npy"))
        npz_files = list(directory.glob("**/*.npz"))
        
        print("\n" + "="*80)
        print("AUTO-VISUALIZING DIRECTORY")
        print("="*80)
        print(f"Directory: {directory}")
        print(f"Found: {len(npy_files)} .npy files, {len(npz_files)} .npz files")
        print("="*80)
        
        # Visualize all npy files
        for filepath in npy_files:
            try:
                self.visualize_npy(str(filepath), show=show, save=save)
            except Exception as e:
                print(f"✗ Error visualizing {filepath}: {e}")
        
        # Visualize all npz files
        for filepath in npz_files:
            try:
                self.visualize_npz(str(filepath), show=show, save=save)
            except Exception as e:
                print(f"✗ Error visualizing {filepath}: {e}")
        
        print("\n" + "="*80)
        print("VISUALIZATION COMPLETE")
        print("="*80)
        print(f"Saved to: {self.output_dir}")


def main():
    """Main visualization interface."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Visualize NumPy binary data files")
    parser.add_argument('path', nargs='?', help='Path to .npy/.npz file or directory')
    parser.add_argument('--no-show', action='store_true', help='Do not show interactive plots')
    parser.add_argument('--no-save', action='store_true', help='Do not save plots')
    parser.add_argument('--output', default='results/visualizations', help='Output directory')
    
    args = parser.parse_args()
    
    visualizer = DataVisualizer(output_dir=args.output)
    
    if args.path is None:
        # Auto-visualize all results
        print("No path specified. Searching for data files in results/...")
        visualizer.auto_visualize_directory(
            'results',
            show=not args.no_show,
            save=not args.no_save
        )
    else:
        path = Path(args.path)
        
        if path.is_dir():
            # Visualize directory
            visualizer.auto_visualize_directory(
                str(path),
                show=not args.no_show,
                save=not args.no_save
            )
        elif path.suffix == '.npy':
            # Visualize single npy file
            visualizer.visualize_npy(
                str(path),
                show=not args.no_show,
                save=not args.no_save
            )
        elif path.suffix == '.npz':
            # Visualize npz file
            visualizer.visualize_npz(
                str(path),
                show=not args.no_show,
                save=not args.no_save
            )
        else:
            print(f"✗ Unknown file type: {path.suffix}")
            print("  Supported: .npy, .npz, or directory")


if __name__ == "__main__":
    main()

