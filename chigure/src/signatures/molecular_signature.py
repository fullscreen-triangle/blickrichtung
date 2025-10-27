"""
Molecular Oscillatory Signature Generation

Generates oscillatory signatures from molecular structures by combining:
- Structural features (from structure_encoder)
- Bond vibrational properties (from bond_analyzer)
- 3D geometry (from geometry_calculator)
- Mass properties (from mass_properties)

This is the core module that maps molecules to oscillatory space.
"""

import numpy as np
import json
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, List
from dataclasses import dataclass

try:
    # Import molecular analysis modules
    import sys
    
    # Try package imports first
    try:
        from molecular.structure_encoder import MolecularStructureEncoder, MolecularFeatures
        from molecular.bond_analyzer import BondAnalyzer
        from molecular.geometry_calculator import GeometryCalculator
        from molecular.mass_properties import MassPropertiesCalculator
    except ImportError:
        # Fallback for direct execution
        sys.path.insert(0, str(Path(__file__).parent.parent))
        from molecular.structure_encoder import MolecularStructureEncoder, MolecularFeatures
        from molecular.bond_analyzer import BondAnalyzer
        from molecular.geometry_calculator import GeometryCalculator
        from molecular.mass_properties import MassPropertiesCalculator
    
    MOLECULAR_AVAILABLE = True
except ImportError:
    MOLECULAR_AVAILABLE = False
    print("Warning: Molecular modules not available")

try:
    from rdkit import Chem
    from rdkit.Chem import AllChem
    RDKIT_AVAILABLE = True
except ImportError:
    RDKIT_AVAILABLE = False


@dataclass
class MolecularOscillatorySignature:
    """Complete oscillatory signature for a molecule."""
    frequency: float  # Dominant oscillatory frequency (Hz)
    amplitude: float  # Oscillation amplitude
    phase: float  # Phase (radians)
    damping: float  # Damping coefficient
    symmetry: float  # Symmetry factor
    
    # Source molecule info
    smiles: Optional[str] = None
    molecular_weight: Optional[float] = None
    
    def to_array(self) -> np.ndarray:
        """Convert to [5] numpy array."""
        return np.array([
            self.frequency,
            self.amplitude,
            self.phase,
            self.damping,
            self.symmetry
        ])
    
    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        return {
            'frequency': float(self.frequency),
            'amplitude': float(self.amplitude),
            'phase': float(self.phase),
            'damping': float(self.damping),
            'symmetry': float(self.symmetry),
            'smiles': self.smiles,
            'molecular_weight': float(self.molecular_weight) if self.molecular_weight else None
        }


class MolecularSignatureGenerator:
    """
    Generates oscillatory signatures from molecular structures.
    
    Combines multiple molecular properties:
    1. Bond vibrational frequencies → Primary frequency
    2. Molecular size/complexity → Amplitude
    3. Electronic structure → Phase
    4. Rigidity/flexibility → Damping
    5. Structural symmetry → Symmetry factor
    """
    
    def __init__(self, generate_3d: bool = True):
        """
        Args:
            generate_3d: Generate 3D coordinates for geometry calculations
        """
        if not MOLECULAR_AVAILABLE or not RDKIT_AVAILABLE:
            raise ImportError("Molecular modules and RDKit required")
        
        self.structure_encoder = MolecularStructureEncoder(generate_3d=generate_3d)
        self.bond_analyzer = BondAnalyzer()
        self.geometry_calculator = GeometryCalculator()
        self.mass_calculator = MassPropertiesCalculator()
        self.generate_3d = generate_3d
    
    def generate_from_smiles(self, smiles: str) -> MolecularOscillatorySignature:
        """
        Generate oscillatory signature from SMILES string.
        
        Args:
            smiles: SMILES string
            
        Returns:
            MolecularOscillatorySignature object
        """
        # Parse molecule
        mol = Chem.MolFromSmiles(smiles)
        if mol is None:
            raise ValueError(f"Invalid SMILES: {smiles}")
        
        mol = Chem.AddHs(mol)
        
        # Generate 3D if requested
        if self.generate_3d:
            try:
                AllChem.EmbedMolecule(mol, randomSeed=42)
                AllChem.MMFFOptimizeMolecule(mol)
            except:
                pass
        
        return self.generate_from_mol(mol, smiles=smiles)
    
    def generate_from_mol(self, 
                          mol: 'Chem.Mol', 
                          smiles: Optional[str] = None) -> MolecularOscillatorySignature:
        """
        Generate oscillatory signature from RDKit Mol object.
        
        Args:
            mol: RDKit Mol object (with 3D coordinates if available)
            smiles: Optional SMILES string for metadata
            
        Returns:
            MolecularOscillatorySignature object
        """
        # 1. Analyze bonds for vibrational frequencies
        bond_properties = self.bond_analyzer.analyze_molecule(mol)
        
        # 2. Calculate geometric properties
        geom_properties = None
        if mol.GetNumConformers() > 0:
            geom_properties = self.geometry_calculator.calculate_properties(mol)
        
        # 3. Calculate mass properties
        mass_properties = self.mass_calculator.calculate_properties(mol)
        
        # 4. Encode structural features
        features = self.structure_encoder.encode_mol(mol)
        
        # 5. Combine into oscillatory signature
        frequency = self._calculate_frequency(bond_properties, mass_properties)
        amplitude = self._calculate_amplitude(features, geom_properties)
        phase = self._calculate_phase(features, bond_properties)
        damping = self._calculate_damping(features, bond_properties, geom_properties)
        symmetry = self._calculate_symmetry(features, geom_properties)
        
        return MolecularOscillatorySignature(
            frequency=frequency,
            amplitude=amplitude,
            phase=phase,
            damping=damping,
            symmetry=symmetry,
            smiles=smiles,
            molecular_weight=mass_properties.molecular_weight
        )
    
    def _calculate_frequency(self, bond_properties, mass_properties) -> float:
        """
        Calculate dominant oscillatory frequency.
        
        Primary determinant: Bond vibrational frequencies
        Weighted by bond strength and occurrence
        """
        if not bond_properties:
            return 1e13  # Default molecular frequency
        
        # Weight by force constant (stronger bonds dominate)
        frequencies = [bp.vibrational_frequency for bp in bond_properties]
        weights = [bp.force_constant for bp in bond_properties]
        
        total_weight = sum(weights)
        if total_weight > 0:
            weighted_freq = sum(f*w for f, w in zip(frequencies, weights)) / total_weight
        else:
            weighted_freq = np.mean(frequencies)
        
        return float(weighted_freq)
    
    def _calculate_amplitude(self, features, geom_properties) -> float:
        """
        Calculate oscillation amplitude.
        
        Determined by:
        - Molecular size (more atoms → larger amplitude)
        - Number of vibrational modes (3N-6)
        - Spatial extent
        """
        # Base amplitude from number of vibrational modes
        n_modes = 3 * features.n_atoms - 6
        amplitude = np.sqrt(n_modes)
        
        # Scale by molecular volume if available
        if geom_properties and geom_properties.molecular_volume:
            volume_factor = np.log10(geom_properties.molecular_volume + 1)
            amplitude *= (1.0 + 0.1 * volume_factor)
        
        return float(amplitude)
    
    def _calculate_phase(self, features, bond_properties) -> float:
        """
        Calculate phase offset.
        
        Determined by:
        - Electronic structure (aromaticity, conjugation)
        - Bond type distribution
        """
        # Phase from aromatic character
        if features.n_rings > 0:
            aromatic_fraction = features.n_aromatic_rings / features.n_rings
        else:
            aromatic_fraction = 0.0
        
        phase_aromatic = aromatic_fraction * np.pi
        
        # Phase from bond alternation
        if bond_properties:
            n_conjugated = sum(1 for bp in bond_properties if bp.is_conjugated)
            conjugation_fraction = n_conjugated / len(bond_properties)
            phase_conjugation = conjugation_fraction * np.pi / 2
        else:
            phase_conjugation = 0.0
        
        # Combine
        phase = (phase_aromatic + phase_conjugation) % (2 * np.pi)
        
        return float(phase)
    
    def _calculate_damping(self, features, bond_properties, geom_properties) -> float:
        """
        Calculate damping coefficient.
        
        Determined by:
        - Molecular rigidity (rings → less damping)
        - Rotatable bonds (flexibility → more damping)
        - Molecular shape (compact → less damping)
        """
        # Rigidity from rings
        rigidity = features.n_rings + 1
        
        # Flexibility from rotatable bonds
        flexibility = features.n_rotatable_bonds + 1
        
        # Base damping: flexible/rigid
        damping = flexibility / (rigidity + flexibility)
        
        # Adjust by asphericity if available
        if geom_properties:
            # More spherical → less damping (uniform energy distribution)
            damping *= (1.0 + 0.2 * geom_properties.asphericity)
        
        # Normalize to [0, 1]
        damping = np.clip(damping, 0.0, 1.0)
        
        return float(damping)
    
    def _calculate_symmetry(self, features, geom_properties) -> float:
        """
        Calculate symmetry factor.
        
        Determined by:
        - Structural symmetry (from molecular structure)
        - Geometric symmetry (from 3D shape)
        """
        # Structural symmetry from atom type diversity
        if features.n_atoms > 0:
            # Lower diversity → higher symmetry
            n_types = len(set([features.n_carbon > 0, features.n_hydrogen > 0,
                              features.n_oxygen > 0, features.n_nitrogen > 0]))
            structural_symmetry = 1.0 - (n_types / 5.0)
        else:
            structural_symmetry = 0.0
        
        # Geometric symmetry from asphericity
        if geom_properties:
            # Lower asphericity → higher symmetry
            geometric_symmetry = 1.0 - geom_properties.asphericity
        else:
            geometric_symmetry = structural_symmetry
        
        # Average
        symmetry = 0.5 * (structural_symmetry + geometric_symmetry)
        
        return float(np.clip(symmetry, 0.0, 1.0))
    
    def save_signatures(self,
                       signatures: Dict[str, MolecularOscillatorySignature],
                       output_path: str,
                       metadata: Optional[Dict] = None) -> None:
        """
        Save molecular signatures to JSON file.
        
        Args:
            signatures: Dict[molecule_name] = MolecularOscillatorySignature
            output_path: Path to output JSON file
            metadata: Optional metadata to include
        """
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Convert signatures to dict
        signatures_dict = {
            name: sig.to_dict() 
            for name, sig in signatures.items()
        }
        
        # Build output data
        output_data = {
            'timestamp': datetime.now().isoformat(),
            'num_molecules': len(signatures),
            'signatures': signatures_dict
        }
        
        if metadata:
            output_data['metadata'] = metadata
        
        # Save to JSON
        with open(output_path, 'w') as f:
            json.dump(output_data, f, indent=2)
        
        print(f"✓ Saved molecular signatures to {output_path}")
    
    def save_similarity_matrix(self,
                              signatures: Dict[str, MolecularOscillatorySignature],
                              output_path: str,
                              metric: str = 'euclidean') -> None:
        """
        Save similarity matrix between molecules.
        
        Args:
            signatures: Dict of molecular signatures
            output_path: Path to output JSON file
            metric: Similarity metric ('euclidean', 'cosine')
        """
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        names = list(signatures.keys())
        n = len(names)
        
        # Compute pairwise distances
        similarity_matrix = {}
        for i, name1 in enumerate(names):
            similarity_matrix[name1] = {}
            sig1 = signatures[name1].to_array()
            
            for name2 in names:
                sig2 = signatures[name2].to_array()
                
                if metric == 'euclidean':
                    distance = float(np.linalg.norm(sig1 - sig2))
                elif metric == 'cosine':
                    # Cosine similarity
                    dot_product = np.dot(sig1, sig2)
                    norm_product = np.linalg.norm(sig1) * np.linalg.norm(sig2)
                    distance = 1.0 - (dot_product / norm_product if norm_product > 0 else 0.0)
                else:
                    distance = 0.0
                
                similarity_matrix[name1][name2] = distance
        
        output_data = {
            'timestamp': datetime.now().isoformat(),
            'metric': metric,
            'molecules': names,
            'similarity_matrix': similarity_matrix
        }
        
        with open(output_path, 'w') as f:
            json.dump(output_data, f, indent=2)
        
        print(f"✓ Saved similarity matrix to {output_path}")


def demonstrate_molecular_signatures():
    """Demonstrate molecular signature generation."""
    print("="*80)
    print("MOLECULAR OSCILLATORY SIGNATURE GENERATION")
    print("="*80 + "\n")
    
    if not MOLECULAR_AVAILABLE or not RDKIT_AVAILABLE:
        print("✗ Required modules not available")
        return
    
    generator = MolecularSignatureGenerator()
    
    # Example molecules
    molecules = {
        'Vanillin (vanilla)': 'COc1cc(C=O)ccc1O',
        'Ethyl Vanillin (vanilla)': 'CCOc1cc(C=O)ccc1O',
        'Benzene (aromatic)': 'c1ccccc1',
        'Indole (fecal)': 'c1ccc2c(c1)cc[nH]2',
        'Citral (lemon)': 'CC(C)=CCCC(C)=CC=O',
    }
    
    signatures = {}
    
    for name, smiles in molecules.items():
        print(f"Molecule: {name}")
        print(f"SMILES: {smiles}")
        
        sig = generator.generate_from_smiles(smiles)
        signatures[name] = sig
        
        print(f"  Frequency: {sig.frequency:.2e} Hz")
        print(f"  Amplitude: {sig.amplitude:.2f}")
        print(f"  Phase: {sig.phase:.3f} rad")
        print(f"  Damping: {sig.damping:.3f}")
        print(f"  Symmetry: {sig.symmetry:.3f}")
        print()
    
    # Compare similar molecules
    print("Similarity Comparison:")
    print("-" * 80)
    
    van_sig = signatures['Vanillin (vanilla)'].to_array()
    ethyl_van_sig = signatures['Ethyl Vanillin (vanilla)'].to_array()
    
    # Simple Euclidean distance
    distance = np.linalg.norm(van_sig - ethyl_van_sig)
    print(f"Vanillin vs Ethyl Vanillin distance: {distance:.3f}")
    print("(Both smell like vanilla - should be similar!)")
    print()
    
    # Save results
    print("Saving results...")
    print("-" * 80)
    
    # Create output directory
    output_dir = Path("results/molecular_signatures")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Save signatures
    generator.save_signatures(
        signatures,
        output_dir / "molecular_signatures.json",
        metadata={'description': 'Oscillatory signatures of odorant molecules'}
    )
    
    # Save similarity matrix
    generator.save_similarity_matrix(
        signatures,
        output_dir / "similarity_matrix.json",
        metric='euclidean'
    )
    
    print("✓ Molecular signature generation complete!")


if __name__ == "__main__":
    demonstrate_molecular_signatures()

