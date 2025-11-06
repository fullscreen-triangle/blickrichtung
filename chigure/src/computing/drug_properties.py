"""
Drug Properties Calculator
Calculates molecular properties of pharmaceutical agents for consciousness programming.
Extends electromagnetic resonance framework with detailed molecular structure analysis.
"""

import numpy as np
import json
from dataclasses import dataclass, asdict
from typing import Dict, List, Tuple
from pathlib import Path


@dataclass
class DrugProperties:
    """Dataclass for drug molecular properties."""
    name: str
    molecular_weight: float  # Da
    num_atoms: int
    num_electrons: int
    charge: int
    num_aromatic_rings: int
    num_h_bond_donors: int
    num_h_bond_acceptors: int
    num_rotatable_bonds: int
    polar_surface_area: float  # Ų
    log_p: float  # Octanol-water partition coefficient
    pka_acid: float  # Acidic pKa
    pka_base: float  # Basic pKa
    
    # Calculated oscillatory properties
    vibrational_frequency: float  # Hz
    o2_aggregation_constant: float  # M⁻¹
    em_coupling_strength: float  # dimensionless
    paramagnetic_moment: float  # Bohr magnetons
    
    # Therapeutic classification
    drug_class: str
    mechanism: str
    therapeutic_window_narrow: bool
    blood_brain_barrier_penetration: float  # 0-1 scale


class DrugPropertiesCalculator:
    """Calculate comprehensive drug properties for consciousness programming."""
    
    def __init__(self):
        # Physical constants
        self.h_planck = 6.62607015e-34  # J·s
        self.k_b = 1.380649e-23  # J/K
        self.T = 310.15  # Body temperature (K)
        self.mu_B = 9.274009994e-24  # Bohr magneton (J/T)
        
        # Molecular force constants
        self.k_spring_default = 500  # N/m for biomolecules
        
        # Database of known drugs (extensible)
        self.drug_database = self._initialize_drug_database()
    
    def _initialize_drug_database(self) -> Dict:
        """Initialize database with common psychoactive drugs."""
        return {
            'lithium': {
                'molecular_weight': 6.94,
                'num_atoms': 1,
                'num_electrons': 3,
                'charge': +1,
                'num_aromatic_rings': 0,
                'num_h_bond_donors': 0,
                'num_h_bond_acceptors': 0,
                'num_rotatable_bonds': 0,
                'polar_surface_area': 0.0,
                'log_p': 0.0,
                'pka_acid': 14.0,
                'pka_base': -1.0,
                'drug_class': 'mood_stabilizer',
                'mechanism': 'inositol_depletion_gsk3_inhibition',
                'therapeutic_window_narrow': True,
                'blood_brain_barrier_penetration': 1.0
            },
            'dopamine': {
                'molecular_weight': 153.18,
                'num_atoms': 23,
                'num_electrons': 86,
                'charge': 0,
                'num_aromatic_rings': 1,
                'num_h_bond_donors': 3,
                'num_h_bond_acceptors': 3,
                'num_rotatable_bonds': 3,
                'polar_surface_area': 66.5,
                'log_p': -0.98,
                'pka_acid': 13.0,
                'pka_base': 8.87,
                'drug_class': 'catecholamine_neurotransmitter',
                'mechanism': 'd1_d2_receptor_agonist',
                'therapeutic_window_narrow': False,
                'blood_brain_barrier_penetration': 0.1
            },
            'serotonin': {
                'molecular_weight': 176.22,
                'num_atoms': 25,
                'num_electrons': 98,
                'charge': 0,
                'num_aromatic_rings': 2,
                'num_h_bond_donors': 2,
                'num_h_bond_acceptors': 2,
                'num_rotatable_bonds': 2,
                'polar_surface_area': 45.8,
                'log_p': -0.06,
                'pka_acid': 14.0,
                'pka_base': 9.8,
                'drug_class': 'indolamine_neurotransmitter',
                'mechanism': '5ht_receptor_agonist',
                'therapeutic_window_narrow': False,
                'blood_brain_barrier_penetration': 0.05
            },
            'ssri_fluoxetine': {
                'molecular_weight': 309.33,
                'num_atoms': 39,
                'num_electrons': 174,
                'charge': 0,
                'num_aromatic_rings': 2,
                'num_h_bond_donors': 1,
                'num_h_bond_acceptors': 2,
                'num_rotatable_bonds': 6,
                'polar_surface_area': 21.3,
                'log_p': 4.09,
                'pka_acid': 14.0,
                'pka_base': 10.1,
                'drug_class': 'ssri_antidepressant',
                'mechanism': 'serotonin_reuptake_inhibitor',
                'therapeutic_window_narrow': False,
                'blood_brain_barrier_penetration': 0.95
            },
            'alprazolam': {
                'molecular_weight': 308.76,
                'num_atoms': 37,
                'num_electrons': 170,
                'charge': 0,
                'num_aromatic_rings': 3,
                'num_h_bond_donors': 0,
                'num_h_bond_acceptors': 3,
                'num_rotatable_bonds': 1,
                'polar_surface_area': 43.1,
                'log_p': 2.12,
                'pka_acid': 14.0,
                'pka_base': 2.4,
                'drug_class': 'benzodiazepine',
                'mechanism': 'gaba_a_receptor_positive_allosteric_modulator',
                'therapeutic_window_narrow': True,
                'blood_brain_barrier_penetration': 0.98
            },
            'metformin': {
                'molecular_weight': 129.16,
                'num_atoms': 21,
                'num_electrons': 70,
                'charge': +1,
                'num_aromatic_rings': 0,
                'num_h_bond_donors': 4,
                'num_h_bond_acceptors': 2,
                'num_rotatable_bonds': 1,
                'polar_surface_area': 91.5,
                'log_p': -2.64,
                'pka_acid': 14.0,
                'pka_base': 12.4,
                'drug_class': 'biguanide_antidiabetic',
                'mechanism': 'ampk_activation_mitochondrial_complex_i_inhibition',
                'therapeutic_window_narrow': False,
                'blood_brain_barrier_penetration': 0.3
            }
        }
    
    def calculate_vibrational_frequency(self, molecular_weight: float, num_atoms: int) -> float:
        """
        Calculate fundamental vibrational frequency from molecular structure.
        ω = √(k/m_eff) where m_eff accounts for all vibrational modes.
        """
        # Effective mass (kg)
        mass_kg = molecular_weight * 1.66054e-27
        
        # Spring constant (adjusted by molecular complexity)
        k_effective = self.k_spring_default * (1 + 0.1 * np.log(num_atoms))
        
        # Angular frequency
        omega = np.sqrt(k_effective / mass_kg)
        
        # Fundamental frequency (accounts for distributed modes)
        freq = omega / (2 * np.pi * np.sqrt(num_atoms))
        
        return freq
    
    def calculate_o2_aggregation_constant(self, log_p: float, polar_surface_area: float,
                                         num_aromatic_rings: int) -> float:
        """
        Calculate oxygen aggregation constant K_agg.
        Based on lipophilicity, polarity, and aromatic character.
        
        Higher K_agg → stronger drug-O2 coupling → better phase-lock programming.
        """
        # Base aggregation from lipophilicity
        # log_p > 0: lipophilic (aggregates better)
        # log_p < 0: hydrophilic (aggregates poorly)
        k_base = 10 ** (3 + log_p)  # M⁻¹
        
        # Polarity penalty (high PSA reduces aggregation)
        polarity_factor = np.exp(-polar_surface_area / 100.0)
        
        # Aromatic enhancement (π-π stacking with O2)
        aromatic_factor = 1 + 0.5 * num_aromatic_rings
        
        # Combined K_agg
        k_agg = k_base * polarity_factor * aromatic_factor
        
        # Physiological constraint: 10² to 10⁶ M⁻¹
        k_agg = np.clip(k_agg, 1e2, 1e6)
        
        return k_agg
    
    def calculate_em_coupling_strength(self, k_agg: float, num_electrons: int) -> float:
        """
        Calculate electromagnetic coupling strength.
        Depends on O2 aggregation and electron cloud size.
        """
        # Coupling strength increases with K_agg (more drug-O2 complexes)
        coupling_agg = np.log10(k_agg) / 6.0  # Normalize to 0-1
        
        # Coupling strength increases with electron cloud (polarizability)
        coupling_electron = np.tanh(num_electrons / 100.0)
        
        # Combined coupling (dimensionless, 0-1 scale)
        coupling = np.sqrt(coupling_agg * coupling_electron)
        
        return coupling
    
    def calculate_paramagnetic_moment(self, num_electrons: int, charge: int) -> float:
        """
        Estimate paramagnetic moment from unpaired electrons.
        Most drugs have paired electrons (diamagnetic), but transition metal
        complexes or radical species can have unpaired electrons.
        """
        # Count unpaired electrons (simplified)
        # Most organic drugs: fully paired → μ = 0
        # Transition metals: unpaired d-electrons → μ > 0
        
        total_electrons = num_electrons - charge
        unpaired = total_electrons % 2  # 0 or 1 for simple organics
        
        # Spin-only magnetic moment: μ = √(n(n+2)) μ_B
        if unpaired == 0:
            mu = 0.0
        else:
            mu = np.sqrt(unpaired * (unpaired + 2))
        
        return mu
    
    def calculate_consciousness_programming_score(self, k_agg: float, em_coupling: float,
                                                  bbb_penetration: float) -> float:
        """
        Overall consciousness programming effectiveness score (0-100).
        Integrates K_agg, EM coupling, and BBB penetration.
        """
        # Threshold for effective programming: K_agg > 10⁴ M⁻¹
        k_agg_score = 100 * (1 - np.exp(-k_agg / 1e4))
        
        # EM coupling score
        em_score = 100 * em_coupling
        
        # BBB penetration score
        bbb_score = 100 * bbb_penetration
        
        # Weighted combination (K_agg most important)
        score = 0.5 * k_agg_score + 0.3 * em_score + 0.2 * bbb_score
        
        return score
    
    def calculate_drug_properties(self, drug_name: str) -> DrugProperties:
        """
        Calculate complete drug properties from database or custom input.
        """
        if drug_name not in self.drug_database:
            raise ValueError(f"Drug '{drug_name}' not in database. Add it first.")
        
        # Get base properties
        props = self.drug_database[drug_name]
        
        # Calculate oscillatory properties
        freq = self.calculate_vibrational_frequency(
            props['molecular_weight'],
            props['num_atoms']
        )
        
        k_agg = self.calculate_o2_aggregation_constant(
            props['log_p'],
            props['polar_surface_area'],
            props['num_aromatic_rings']
        )
        
        em_coupling = self.calculate_em_coupling_strength(
            k_agg,
            props['num_electrons']
        )
        
        paramagnetic = self.calculate_paramagnetic_moment(
            props['num_electrons'],
            props['charge']
        )
        
        # Create DrugProperties object
        drug_props = DrugProperties(
            name=drug_name,
            molecular_weight=props['molecular_weight'],
            num_atoms=props['num_atoms'],
            num_electrons=props['num_electrons'],
            charge=props['charge'],
            num_aromatic_rings=props['num_aromatic_rings'],
            num_h_bond_donors=props['num_h_bond_donors'],
            num_h_bond_acceptors=props['num_h_bond_acceptors'],
            num_rotatable_bonds=props['num_rotatable_bonds'],
            polar_surface_area=props['polar_surface_area'],
            log_p=props['log_p'],
            pka_acid=props['pka_acid'],
            pka_base=props['pka_base'],
            vibrational_frequency=freq,
            o2_aggregation_constant=k_agg,
            em_coupling_strength=em_coupling,
            paramagnetic_moment=paramagnetic,
            drug_class=props['drug_class'],
            mechanism=props['mechanism'],
            therapeutic_window_narrow=props['therapeutic_window_narrow'],
            blood_brain_barrier_penetration=props['blood_brain_barrier_penetration']
        )
        
        return drug_props
    
    def add_drug_to_database(self, drug_name: str, properties: Dict):
        """Add new drug to database."""
        self.drug_database[drug_name] = properties
    
    def compare_drugs(self, drug_names: List[str]) -> Dict:
        """Compare multiple drugs across key properties."""
        results = {}
        
        for drug_name in drug_names:
            props = self.calculate_drug_properties(drug_name)
            results[drug_name] = asdict(props)
        
        return results
    
    def predict_therapeutic_class(self, k_agg: float, em_coupling: float, 
                                  bbb_penetration: float) -> str:
        """
        Predict likely therapeutic class from consciousness programming metrics.
        """
        if k_agg > 5e4 and em_coupling > 0.7 and bbb_penetration > 0.8:
            return "potent_cns_active"
        elif k_agg > 1e4 and bbb_penetration > 0.5:
            return "moderate_cns_active"
        elif k_agg < 1e3 or bbb_penetration < 0.1:
            return "peripheral_acting"
        else:
            return "mild_cns_active"


def main():
    """Main function for drug properties analysis."""
    print("=" * 80)
    print("Drug Properties Calculator")
    print("Molecular Structure Analysis for Consciousness Programming")
    print("=" * 80)
    
    calc = DrugPropertiesCalculator()
    
    # Test drugs
    drugs = ['lithium', 'dopamine', 'serotonin', 'ssri_fluoxetine', 
             'alprazolam', 'metformin']
    
    all_results = []
    
    for drug_name in drugs:
        print(f"\n{'='*60}")
        print(f"Analyzing: {drug_name.upper()}")
        print(f"{'='*60}")
        
        props = calc.calculate_drug_properties(drug_name)
        
        # Print key properties
        print(f"Molecular Weight:              {props.molecular_weight:.2f} Da")
        print(f"Number of Atoms:               {props.num_atoms}")
        print(f"Number of Electrons:           {props.num_electrons}")
        print(f"Charge:                        {props.charge:+d}")
        print(f"Aromatic Rings:                {props.num_aromatic_rings}")
        print(f"LogP (lipophilicity):          {props.log_p:.2f}")
        print(f"Polar Surface Area:            {props.polar_surface_area:.1f} ų")
        print(f"\nOscillatory Properties:")
        print(f"Vibrational Frequency:         {props.vibrational_frequency:.2e} Hz")
        print(f"O2 Aggregation Constant:       {props.o2_aggregation_constant:.2e} M⁻¹")
        print(f"EM Coupling Strength:          {props.em_coupling_strength:.4f}")
        print(f"Paramagnetic Moment:           {props.paramagnetic_moment:.2f} μ_B")
        print(f"\nTherapeutic Classification:")
        print(f"Drug Class:                    {props.drug_class}")
        print(f"Mechanism:                     {props.mechanism}")
        print(f"BBB Penetration:               {props.blood_brain_barrier_penetration:.2f}")
        print(f"Narrow Therapeutic Window:     {props.therapeutic_window_narrow}")
        
        # Calculate consciousness programming score
        score = calc.calculate_consciousness_programming_score(
            props.o2_aggregation_constant,
            props.em_coupling_strength,
            props.blood_brain_barrier_penetration
        )
        print(f"\nConsciousness Programming Score: {score:.1f}/100")
        
        all_results.append(asdict(props))
    
    # Save results
    output_dir = Path("chatelier/src/computing/results")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    from datetime import datetime
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    json_path = output_dir / f"drug_properties_{timestamp}.json"
    with open(json_path, 'w') as f:
        json.dump({
            'timestamp': timestamp,
            'description': 'Molecular properties for consciousness programming',
            'drugs': all_results
        }, f, indent=2)
    
    print(f"\n{'='*60}")
    print(f"Results saved to: {json_path}")
    print(f"{'='*60}")
    
    print("\n" + "="*80)
    print("ANALYSIS COMPLETE")
    print("="*80)
    
    return all_results


if __name__ == "__main__":
    main()

