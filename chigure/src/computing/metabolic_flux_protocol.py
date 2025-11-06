"""
Metabolic Flux Protocol Generator
Generates experimental protocols for validating hierarchical flux predictions.
Implements Prediction 2 from Kuramoto oscillator paper (Section 7.4.2).
"""

import numpy as np
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple
from dataclasses import dataclass, field


@dataclass
class ExperimentalProtocol:
    """Dataclass for experimental protocol."""
    protocol_name: str
    objective: str
    hypothesis: str
    methods: List[Dict]
    measurements: List[Dict]
    expected_results: Dict
    analysis_methods: List[str]
    timeline_hours: float
    required_equipment: List[str]
    required_reagents: List[str]
    sample_size: int
    control_conditions: List[str]
    experimental_conditions: List[str]


class MetabolicFluxProtocolGenerator:
    """Generate experimental protocols for metabolic flux validation."""
    
    def __init__(self):
        # Standard experimental parameters
        self.standard_culture_conditions = {
            'temperature_c': 37.0,
            'co2_percent': 5.0,
            'humidity_percent': 95.0,
            'culture_medium': 'DMEM + 10% FBS'
        }
        
        # Hierarchical metabolic levels
        self.metabolic_levels = [
            "Glucose_Transport",
            "Glycolysis",
            "TCA_Cycle",
            "Oxidative_Phosphorylation",
            "Gene_Expression"
        ]
    
    def generate_isotope_tracing_protocol(self, drug_name: str = 'metformin') -> ExperimentalProtocol:
        """
        Generate protocol for C13-glucose isotope tracing.
        Gold standard for measuring metabolic flux.
        """
        protocol = ExperimentalProtocol(
            protocol_name=f"Hierarchical Metabolic Flux via C13-Glucose Tracing: {drug_name.capitalize()} Intervention",
            
            objective="Measure metabolic flux through hierarchical levels (Glucose → Pyruvate → TCA → ATP → Gene Expression) and quantify drug-induced hierarchical restoration.",
            
            hypothesis=f"{drug_name.capitalize()} increases hierarchical metabolic depth from 0.4 (metabolic syndrome baseline) to 0.7-0.8 (therapeutic) by restoring multi-level signal propagation.",
            
            methods=[
                {
                    'step': 1,
                    'name': 'Cell Culture Preparation',
                    'description': 'Culture insulin-resistant hepatocytes (HepG2 or primary hepatocytes) in standard medium',
                    'duration_hours': 24,
                    'details': [
                        'Seed cells at 2×10^5 cells/well in 6-well plates',
                        'Allow 24h attachment',
                        'Verify insulin resistance via insulin-stimulated glucose uptake assay',
                        'Confirm HOMA-IR > 2.5 equivalent'
                    ]
                },
                {
                    'step': 2,
                    'name': 'Drug Pre-Treatment',
                    'description': f'Pre-treat with {drug_name} for 24 hours',
                    'duration_hours': 24,
                    'details': [
                        f'Add {drug_name} at therapeutic concentration (1-10 μM for metformin)',
                        'Control wells receive vehicle only',
                        'Maintain standard culture conditions',
                        'N=6 wells per condition'
                    ]
                },
                {
                    'step': 3,
                    'name': 'C13-Glucose Pulse',
                    'description': 'Replace medium with C13-glucose labeling medium',
                    'duration_hours': 0.25,
                    'details': [
                        'Remove standard medium',
                        'Add glucose-free DMEM + 10 mM [U-13C]-glucose',
                        'Maintain for 15 minutes (initial flux)',
                        '1 hour (steady-state), and 4 hours (downstream propagation)'
                    ]
                },
                {
                    'step': 4,
                    'name': 'Metabolite Extraction',
                    'description': 'Quench metabolism and extract metabolites',
                    'duration_hours': 0.5,
                    'details': [
                        'Aspirate medium rapidly',
                        'Quench with -80°C methanol/acetonitrile/water (40:40:20)',
                        'Scrape cells and collect lysate',
                        'Centrifuge 16,000g, 10 min, 4°C',
                        'Collect supernatant for LC-MS/MS',
                        'Pellet for protein normalization'
                    ]
                },
                {
                    'step': 5,
                    'name': 'LC-MS/MS Analysis',
                    'description': 'Quantify C13-labeled metabolites at each hierarchical level',
                    'duration_hours': 2,
                    'details': [
                        'Level 1: Glucose-6-phosphate (glucose transport)',
                        'Level 2: Pyruvate, lactate (glycolysis)',
                        'Level 3: Citrate, α-ketoglutarate, succinate, malate (TCA cycle)',
                        'Level 4: ATP, ADP (oxidative phosphorylation)',
                        'Level 5: Sample for RNA-seq (gene expression)',
                        'Calculate M+6 glucose → M+3 pyruvate → M+2 acetyl-CoA → TCA isotopomers'
                    ]
                },
                {
                    'step': 6,
                    'name': 'RNA Sequencing',
                    'description': 'Measure gene expression at hierarchical level 5',
                    'duration_hours': 48,
                    'details': [
                        'Extract RNA from cell pellet (RNeasy kit)',
                        'Prepare RNA-seq libraries',
                        'Sequence on Illumina platform (50M reads/sample)',
                        'Focus on metabolic gene signatures'
                    ]
                }
            ],
            
            measurements=[
                {
                    'level': 1,
                    'name': 'Glucose Transport',
                    'metabolites': ['Glucose', 'Glucose-6-phosphate'],
                    'metric': 'C13 enrichment in G6P',
                    'expected_change_with_drug': '+30-50% increase'
                },
                {
                    'level': 2,
                    'name': 'Glycolysis',
                    'metabolites': ['Pyruvate', 'Lactate', '3-phosphoglycerate'],
                    'metric': 'Pyruvate M+3 enrichment',
                    'expected_change_with_drug': '+40-60% increase'
                },
                {
                    'level': 3,
                    'name': 'TCA Cycle',
                    'metabolites': ['Citrate', 'α-ketoglutarate', 'Succinate', 'Fumarate', 'Malate'],
                    'metric': 'TCA intermediate enrichment',
                    'expected_change_with_drug': '+50-70% increase'
                },
                {
                    'level': 4,
                    'name': 'Oxidative Phosphorylation',
                    'metabolites': ['ATP', 'ADP', 'AMP'],
                    'metric': 'ATP/ADP ratio',
                    'expected_change_with_drug': '+20-40% increase'
                },
                {
                    'level': 5,
                    'name': 'Gene Expression',
                    'metabolites': ['mRNA transcripts'],
                    'metric': 'Metabolic gene expression',
                    'expected_change_with_drug': 'Upregulation of OxPhos genes'
                }
            ],
            
            expected_results={
                'control_insulin_resistant': {
                    'active_levels': '2/5',
                    'hierarchical_depth': 0.4,
                    'flux_glucose_to_atp': '20% of healthy',
                    'cascade_failure_at': 'Level 3 (TCA)',
                    'information_compression': '0.5 bits total'
                },
                f'treated_with_{drug_name}': {
                    'active_levels': '4-5/5',
                    'hierarchical_depth': '0.7-0.8',
                    'flux_glucose_to_atp': '60-80% of healthy',
                    'cascade_restoration': 'Level 3-4 reactivated',
                    'information_compression': '3-4 bits total'
                },
                'statistical_test': 'Two-way ANOVA (condition × hierarchical level)',
                'significance_threshold': 'p < 0.05, FDR < 0.1',
                'expected_effect_size': "Cohen's d > 0.8 for levels 3-4"
            },
            
            analysis_methods=[
                'Metabolic Flux Analysis (MFA) using INCA or C13Flux software',
                'Hierarchical depth calculation: active_levels / total_levels',
                'Information compression per level: log2(input_flux / output_flux)',
                'ATP cost-benefit analysis: bits compressed / ATP consumed',
                'Statistical comparison: Mixed-effects model with random patient effects',
                'Visualization: Flux cascade plots, hierarchical depth bar charts'
            ],
            
            timeline_hours=96.0,
            
            required_equipment=[
                'Cell culture incubator (37°C, 5% CO2)',
                '6-well cell culture plates',
                'LC-MS/MS system (high-resolution, Orbitrap or TOF)',
                'RNA extraction kit',
                'RNA-seq platform (Illumina)',
                'Centrifuge (16,000g, 4°C)',
                '-80°C freezer',
                'Liquid nitrogen'
            ],
            
            required_reagents=[
                '[U-13C]-glucose (Cambridge Isotope Labs)',
                'DMEM (glucose-free)',
                'Fetal bovine serum (FBS)',
                'Insulin',
                f'{drug_name} (therapeutic grade)',
                'Methanol, acetonitrile (LC-MS grade)',
                'RNA extraction kit (Qiagen RNeasy)',
                'RNA-seq library preparation kit'
            ],
            
            sample_size=6,  # N=6 per condition
            
            control_conditions=[
                'Healthy cells (no insulin resistance)',
                'Insulin-resistant cells + vehicle',
                'Insulin-resistant cells + insulin only (positive control)'
            ],
            
            experimental_conditions=[
                f'Insulin-resistant cells + {drug_name} (1 μM)',
                f'Insulin-resistant cells + {drug_name} (10 μM)',
                f'Insulin-resistant cells + {drug_name} (100 μM)'
            ]
        )
        
        return protocol
    
    def generate_seahorse_protocol(self, drug_name: str = 'metformin') -> ExperimentalProtocol:
        """
        Generate protocol for Seahorse XF Analyzer (real-time metabolic flux).
        Measures OCR (oxidative phosphorylation) and ECAR (glycolysis) simultaneously.
        """
        protocol = ExperimentalProtocol(
            protocol_name=f"Real-Time Metabolic Flux via Seahorse XF Analyzer: {drug_name.capitalize()}",
            
            objective="Measure oxygen consumption rate (OCR) and extracellular acidification rate (ECAR) to quantify hierarchical metabolic activity in real-time.",
            
            hypothesis=f"{drug_name.capitalize()} shifts metabolism from glycolysis-dominant to OxPhos-dominant, restoring hierarchical depth.",
            
            methods=[
                {
                    'step': 1,
                    'name': 'Cell Seeding',
                    'description': 'Seed cells in Seahorse XF96 microplate',
                    'duration_hours': 24,
                    'details': [
                        'Seed insulin-resistant hepatocytes at 2×10^4 cells/well',
                        'Seahorse XF96 plate (96 wells)',
                        'Allow 24h attachment',
                        'N=10 technical replicates per condition'
                    ]
                },
                {
                    'step': 2,
                    'name': 'Drug Treatment',
                    'description': f'Treat with {drug_name} for 24 hours',
                    'duration_hours': 24,
                    'details': [
                        f'Add {drug_name} to experimental wells',
                        'Vehicle control to control wells',
                        'Final volume 180 μL per well'
                    ]
                },
                {
                    'step': 3,
                    'name': 'Seahorse Assay',
                    'description': 'Run Mito Stress Test',
                    'duration_hours': 2,
                    'details': [
                        'Replace medium with Seahorse XF assay medium',
                        'Pre-incubate 1h at 37°C without CO2',
                        'Load compounds into injection ports:',
                        '  Port A: Oligomycin (1 μM) - ATP synthase inhibitor',
                        '  Port B: FCCP (0.5 μM) - uncoupler',
                        '  Port C: Rotenone/Antimycin A (0.5 μM) - ETC inhibitors',
                        'Run protocol: 3 baseline + 3 measurements per injection',
                        'Calculate: Basal OCR, ATP production, maximal respiration, spare capacity'
                    ]
                }
            ],
            
            measurements=[
                {
                    'parameter': 'Basal OCR',
                    'units': 'pmol O2/min/10^4 cells',
                    'hierarchical_level': 4,
                    'interpretation': 'Oxidative phosphorylation activity'
                },
                {
                    'parameter': 'ATP-linked OCR',
                    'units': 'pmol O2/min/10^4 cells',
                    'hierarchical_level': 4,
                    'interpretation': 'ATP synthesis via OxPhos'
                },
                {
                    'parameter': 'Maximal OCR',
                    'units': 'pmol O2/min/10^4 cells',
                    'hierarchical_level': 4,
                    'interpretation': 'Respiratory capacity'
                },
                {
                    'parameter': 'Spare Respiratory Capacity',
                    'units': '%',
                    'hierarchical_level': 4,
                    'interpretation': 'Metabolic flexibility'
                },
                {
                    'parameter': 'ECAR',
                    'units': 'mpH/min/10^4 cells',
                    'hierarchical_level': 2,
                    'interpretation': 'Glycolysis rate'
                },
                {
                    'parameter': 'OCR/ECAR ratio',
                    'units': 'dimensionless',
                    'hierarchical_level': 'integrated',
                    'interpretation': 'OxPhos vs glycolysis balance'
                }
            ],
            
            expected_results={
                'control_insulin_resistant': {
                    'basal_ocr': '50 pmol/min (↓50% vs healthy)',
                    'atp_linked_ocr': '30 pmol/min (↓60% vs healthy)',
                    'ecar': '40 mpH/min (↑100% vs healthy - Warburg-like)',
                    'ocr_ecar_ratio': '1.25 (↓60% vs healthy)',
                    'hierarchical_interpretation': 'Level 4 (OxPhos) impaired, Level 2 (glycolysis) compensatory upregulation'
                },
                f'treated_with_{drug_name}': {
                    'basal_ocr': '80 pmol/min (↑60% vs untreated)',
                    'atp_linked_ocr': '60 pmol/min (↑100% vs untreated)',
                    'ecar': '25 mpH/min (↓40% vs untreated)',
                    'ocr_ecar_ratio': '3.2 (↑150% vs untreated)',
                    'hierarchical_interpretation': 'Level 4 (OxPhos) restored, Level 2 (glycolysis) normalized'
                },
                'statistical_test': 'Two-way repeated measures ANOVA',
                'significance': 'p < 0.01 for OCR, p < 0.05 for ECAR'
            },
            
            analysis_methods=[
                'Wave Desktop software (Agilent)',
                'OCR normalization to cell number (CyQUANT assay post-Seahorse)',
                'Calculate metabolic phenotype (OCR vs ECAR)',
                'Calculate hierarchical depth from OCR/ECAR ratio',
                'Statistical analysis in GraphPad Prism or R'
            ],
            
            timeline_hours=50.0,
            
            required_equipment=[
                'Seahorse XF96 Analyzer (Agilent)',
                'Seahorse XF96 Cell Culture Microplates',
                'Seahorse XF96 Sensor Cartridges',
                'Cell culture incubator',
                'Non-CO2 incubator (for pre-assay incubation)'
            ],
            
            required_reagents=[
                'Seahorse XF Assay Medium',
                'Oligomycin',
                'FCCP',
                'Rotenone',
                'Antimycin A',
                'Glucose',
                'Pyruvate',
                'Glutamine',
                f'{drug_name}'
            ],
            
            sample_size=10,
            
            control_conditions=[
                'Healthy cells',
                'Insulin-resistant cells + vehicle'
            ],
            
            experimental_conditions=[
                f'Insulin-resistant cells + {drug_name} (1 μM)',
                f'Insulin-resistant cells + {drug_name} (10 μM)'
            ]
        )
        
        return protocol
    
    def save_protocol(self, protocol: ExperimentalProtocol, output_dir: Path):
        """Save protocol to JSON and formatted text."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Save JSON
        json_path = output_dir / f"protocol_{protocol.protocol_name.replace(' ', '_')}_{timestamp}.json"
        with open(json_path, 'w') as f:
            # Convert dataclass to dict
            protocol_dict = {
                'protocol_name': protocol.protocol_name,
                'objective': protocol.objective,
                'hypothesis': protocol.hypothesis,
                'methods': protocol.methods,
                'measurements': protocol.measurements,
                'expected_results': protocol.expected_results,
                'analysis_methods': protocol.analysis_methods,
                'timeline_hours': protocol.timeline_hours,
                'required_equipment': protocol.required_equipment,
                'required_reagents': protocol.required_reagents,
                'sample_size': protocol.sample_size,
                'control_conditions': protocol.control_conditions,
                'experimental_conditions': protocol.experimental_conditions
            }
            json.dump(protocol_dict, f, indent=2)
        
        return json_path


def main():
    """Main function for protocol generation."""
    print("=" * 80)
    print("Metabolic Flux Protocol Generator")
    print("Experimental Protocols for Hierarchical Flux Validation")
    print("=" * 80)
    
    generator = MetabolicFluxProtocolGenerator()
    
    # Generate protocols
    print("\n" + "="*60)
    print("Generating Protocol 1: C13-Glucose Isotope Tracing")
    print("="*60)
    protocol1 = generator.generate_isotope_tracing_protocol('metformin')
    
    print(f"\nProtocol: {protocol1.protocol_name}")
    print(f"Objective: {protocol1.objective}")
    print(f"Hypothesis: {protocol1.hypothesis}")
    print(f"\nMethods ({len(protocol1.methods)} steps):")
    for method in protocol1.methods:
        print(f"  Step {method['step']}: {method['name']} ({method['duration_hours']}h)")
    print(f"\nTimeline: {protocol1.timeline_hours} hours ({protocol1.timeline_hours/24:.1f} days)")
    print(f"Sample size: N={protocol1.sample_size} per condition")
    
    print("\n" + "="*60)
    print("Generating Protocol 2: Seahorse XF Real-Time Flux")
    print("="*60)
    protocol2 = generator.generate_seahorse_protocol('metformin')
    
    print(f"\nProtocol: {protocol2.protocol_name}")
    print(f"Objective: {protocol2.objective}")
    print(f"Hypothesis: {protocol2.hypothesis}")
    print(f"\nMethods ({len(protocol2.methods)} steps):")
    for method in protocol2.methods:
        print(f"  Step {method['step']}: {method['name']} ({method['duration_hours']}h)")
    print(f"\nTimeline: {protocol2.timeline_hours} hours ({protocol2.timeline_hours/24:.1f} days)")
    print(f"Sample size: N={protocol2.sample_size} per condition")
    
    # Save protocols
    output_dir = Path("chatelier/src/computing/results/protocols")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    json_path1 = generator.save_protocol(protocol1, output_dir)
    json_path2 = generator.save_protocol(protocol2, output_dir)
    
    print(f"\n{'='*60}")
    print(f"Protocols saved:")
    print(f"  1. {json_path1}")
    print(f"  2. {json_path2}")
    
    print("\n" + "="*80)
    print("PROTOCOL GENERATION COMPLETE")
    print("="*80)
    print("\nKey Predictions to Validate:")
    print("1. Metformin increases hierarchical depth from 0.4 → 0.7-0.8")
    print("2. Hierarchical reactivation occurs at Levels 3-4 (TCA + OxPhos)")
    print("3. ATP efficiency improves (bits/kATP increases)")
    print("4. Multi-scale signal propagation restored")
    print("\nFalsification Criteria:")
    print("- If metformin improves clinical outcomes WITHOUT hierarchical reactivation → framework incomplete")
    print("- If hierarchical depth does NOT correlate with therapeutic response → framework wrong")
    print("="*80)
    
    return [protocol1, protocol2]


if __name__ == "__main__":
    main()

