"""
Metabolic Hierarchy Mapper
Maps disease states to hierarchical dysfunction patterns.
Clinical application of metabolic flux hierarchy for diagnosis and treatment.
"""

import numpy as np
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple
from dataclasses import dataclass, field


@dataclass
class DiseaseState:
    """Dataclass for disease-specific hierarchical dysfunction."""
    disease_name: str
    affected_levels: List[int]  # Which hierarchical levels are impaired
    dysfunction_severity: List[float]  # 0-1 scale per level
    baseline_depth: float
    symptomatic_depth: float
    primary_pathway_affected: str
    biomarkers: List[str]
    
    # Therapeutic intervention
    recommended_drug: str
    target_depth_restoration: float
    expected_timeline_weeks: float


@dataclass
class PatientProfile:
    """Dataclass for patient metabolic profile."""
    patient_id: str
    age: int
    sex: str
    bmi: float
    
    # Metabolic biomarkers
    fasting_glucose: float  # mg/dL
    hba1c: float  # %
    insulin: float  # μU/mL
    triglycerides: float  # mg/dL
    hdl_cholesterol: float  # mg/dL
    ldl_cholesterol: float  # mg/dL
    
    # Calculated metrics
    homa_ir: float  # Insulin resistance index
    metabolic_syndrome_score: float  # 0-5
    hierarchical_depth_estimate: float  # 0-1
    
    # Disease classification
    disease_state: str
    severity: str  # 'mild', 'moderate', 'severe'


class MetabolicHierarchyMapper:
    """Map metabolic diseases to hierarchical dysfunction patterns."""
    
    def __init__(self):
        # Define disease-specific dysfunction patterns
        self.disease_database = self._initialize_disease_database()
        
        # Hierarchical level names
        self.level_names = [
            "Glucose_Transport",
            "Glycolysis",
            "TCA_Cycle",
            "Oxidative_Phosphorylation",
            "Gene_Expression"
        ]
    
    def _initialize_disease_database(self) -> Dict:
        """Initialize database of disease-hierarchical dysfunction mappings."""
        return {
            'type_2_diabetes': DiseaseState(
                disease_name="Type 2 Diabetes",
                affected_levels=[1, 2, 3],  # Glucose transport + glycolysis + TCA
                dysfunction_severity=[0.7, 0.6, 0.5, 0.2, 0.1],
                baseline_depth=1.0,
                symptomatic_depth=0.6,
                primary_pathway_affected="Glucose_Transport",
                biomarkers=['glucose', 'HbA1c', 'insulin', 'HOMA-IR'],
                recommended_drug='metformin',
                target_depth_restoration=0.8,
                expected_timeline_weeks=12
            ),
            'metabolic_syndrome': DiseaseState(
                disease_name="Metabolic Syndrome",
                affected_levels=[1, 2, 3, 4],  # All metabolic levels
                dysfunction_severity=[0.5, 0.6, 0.7, 0.5, 0.2],
                baseline_depth=1.0,
                symptomatic_depth=0.4,
                primary_pathway_affected="Multiple",
                biomarkers=['glucose', 'triglycerides', 'HDL', 'blood_pressure', 'waist_circumference'],
                recommended_drug='metformin',
                target_depth_restoration=0.7,
                expected_timeline_weeks=24
            ),
            'mitochondrial_dysfunction': DiseaseState(
                disease_name="Mitochondrial Dysfunction",
                affected_levels=[3, 4],  # TCA + OxPhos
                dysfunction_severity=[0.2, 0.3, 0.8, 0.9, 0.3],
                baseline_depth=1.0,
                symptomatic_depth=0.4,
                primary_pathway_affected="Oxidative_Phosphorylation",
                biomarkers=['lactate', 'pyruvate', 'ATP', 'mitochondrial_DNA'],
                recommended_drug='coenzyme_q10',
                target_depth_restoration=0.7,
                expected_timeline_weeks=8
            ),
            'cancer_warburg': DiseaseState(
                disease_name="Cancer (Warburg Effect)",
                affected_levels=[2, 3, 4],  # Glycolysis upregulated, OxPhos downregulated
                dysfunction_severity=[0.1, -0.5, 0.6, 0.8, 0.3],  # Negative = upregulation
                baseline_depth=1.0,
                symptomatic_depth=0.5,
                primary_pathway_affected="Glycolysis",
                biomarkers=['lactate', 'glucose_uptake', 'FDG-PET'],
                recommended_drug='dichloroacetate',
                target_depth_restoration=0.8,
                expected_timeline_weeks=16
            ),
            'neurodegenerative': DiseaseState(
                disease_name="Neurodegenerative Disease",
                affected_levels=[3, 4, 5],  # Energy + gene expression
                dysfunction_severity=[0.1, 0.2, 0.5, 0.7, 0.6],
                baseline_depth=1.0,
                symptomatic_depth=0.5,
                primary_pathway_affected="Oxidative_Phosphorylation",
                biomarkers=['ATP', 'oxidative_stress', 'protein_aggregates'],
                recommended_drug='nad_precursors',
                target_depth_restoration=0.7,
                expected_timeline_weeks=52
            )
        }
    
    def calculate_homa_ir(self, fasting_glucose: float, fasting_insulin: float) -> float:
        """
        Calculate HOMA-IR (Homeostatic Model Assessment of Insulin Resistance).
        HOMA-IR = (Glucose × Insulin) / 405
        """
        homa_ir = (fasting_glucose * fasting_insulin) / 405.0
        return homa_ir
    
    def calculate_metabolic_syndrome_score(self, patient: Dict) -> float:
        """
        Calculate metabolic syndrome score (0-5 criteria).
        ATP III criteria: ≥3 = metabolic syndrome
        """
        score = 0
        
        # 1. Elevated waist circumference (use BMI as proxy)
        if patient['bmi'] > 30:
            score += 1
        
        # 2. Elevated triglycerides (≥150 mg/dL)
        if patient['triglycerides'] >= 150:
            score += 1
        
        # 3. Reduced HDL cholesterol (<40 mg/dL men, <50 mg/dL women)
        hdl_threshold = 50 if patient['sex'] == 'F' else 40
        if patient['hdl_cholesterol'] < hdl_threshold:
            score += 1
        
        # 4. Elevated blood pressure (use glucose as proxy)
        if patient['fasting_glucose'] >= 100:
            score += 1
        
        # 5. Elevated fasting glucose (≥100 mg/dL)
        if patient['hba1c'] >= 5.7:
            score += 1
        
        return score
    
    def estimate_hierarchical_depth_from_biomarkers(self, patient: Dict) -> float:
        """
        Estimate hierarchical depth from patient biomarkers.
        Lower glucose control + higher insulin resistance → lower depth.
        """
        # Glucose control (HbA1c)
        # Normal: <5.7%, Prediabetes: 5.7-6.4%, Diabetes: ≥6.5%
        if patient['hba1c'] < 5.7:
            glucose_factor = 1.0
        elif patient['hba1c'] < 6.5:
            glucose_factor = 0.7
        else:
            glucose_factor = 0.4
        
        # Insulin resistance (HOMA-IR)
        # Normal: <2.0, Insulin resistant: >2.5
        homa_ir = patient['homa_ir']
        if homa_ir < 2.0:
            insulin_factor = 1.0
        elif homa_ir < 3.0:
            insulin_factor = 0.8
        elif homa_ir < 5.0:
            insulin_factor = 0.6
        else:
            insulin_factor = 0.4
        
        # Lipid profile
        triglyceride_factor = 1.0 if patient['triglycerides'] < 150 else 0.8
        hdl_threshold = 50 if patient['sex'] == 'F' else 40
        hdl_factor = 1.0 if patient['hdl_cholesterol'] >= hdl_threshold else 0.9
        
        # Combined depth estimate
        depth = glucose_factor * insulin_factor * triglyceride_factor * hdl_factor
        
        return depth
    
    def classify_disease_state(self, patient: Dict) -> Tuple[str, str]:
        """
        Classify patient disease state from biomarkers.
        Returns: (disease_name, severity)
        """
        met_syn_score = patient['metabolic_syndrome_score']
        hba1c = patient['hba1c']
        homa_ir = patient['homa_ir']
        
        # Type 2 Diabetes
        if hba1c >= 6.5:
            severity = 'severe' if hba1c >= 8.0 else 'moderate' if hba1c >= 7.0 else 'mild'
            return 'type_2_diabetes', severity
        
        # Metabolic Syndrome
        elif met_syn_score >= 3:
            severity = 'severe' if met_syn_score == 5 else 'moderate' if met_syn_score == 4 else 'mild'
            return 'metabolic_syndrome', severity
        
        # Prediabetes / Insulin Resistance
        elif hba1c >= 5.7 or homa_ir >= 2.5:
            severity = 'mild'
            return 'metabolic_syndrome', severity
        
        # Healthy
        else:
            return 'healthy', 'none'
    
    def create_patient_profile(self, patient_data: Dict) -> PatientProfile:
        """Create complete patient profile with calculated metrics."""
        
        # Calculate HOMA-IR
        homa_ir = self.calculate_homa_ir(
            patient_data['fasting_glucose'],
            patient_data['insulin']
        )
        patient_data['homa_ir'] = homa_ir
        
        # Calculate metabolic syndrome score
        met_syn_score = self.calculate_metabolic_syndrome_score(patient_data)
        patient_data['metabolic_syndrome_score'] = met_syn_score
        
        # Estimate hierarchical depth
        depth = self.estimate_hierarchical_depth_from_biomarkers(patient_data)
        patient_data['hierarchical_depth_estimate'] = depth
        
        # Classify disease state
        disease_state, severity = self.classify_disease_state(patient_data)
        patient_data['disease_state'] = disease_state
        patient_data['severity'] = severity
        
        # Create profile
        profile = PatientProfile(**patient_data)
        
        return profile
    
    def map_patient_to_hierarchy(self, profile: PatientProfile) -> Dict:
        """
        Map patient profile to hierarchical dysfunction pattern.
        Returns therapeutic recommendations.
        """
        if profile.disease_state == 'healthy':
            return {
                'patient_id': profile.patient_id,
                'disease': 'healthy',
                'current_depth': profile.hierarchical_depth_estimate,
                'dysfunction_levels': [],
                'recommended_intervention': 'lifestyle_maintenance',
                'expected_outcome': 'maintain health'
            }
        
        # Get disease pattern
        disease = self.disease_database.get(profile.disease_state)
        
        if disease is None:
            return {
                'patient_id': profile.patient_id,
                'disease': profile.disease_state,
                'error': 'Disease pattern not in database'
            }
        
        # Map to hierarchy
        dysfunction_map = []
        for level_idx in range(5):
            dysfunction_map.append({
                'level': level_idx + 1,
                'name': self.level_names[level_idx],
                'dysfunction_severity': disease.dysfunction_severity[level_idx],
                'affected': level_idx in [l-1 for l in disease.affected_levels]
            })
        
        # Therapeutic recommendation
        result = {
            'patient_id': profile.patient_id,
            'disease': disease.disease_name,
            'severity': profile.severity,
            'current_depth': profile.hierarchical_depth_estimate,
            'target_depth': disease.target_depth_restoration,
            'depth_deficit': disease.target_depth_restoration - profile.hierarchical_depth_estimate,
            'dysfunction_levels': dysfunction_map,
            'primary_pathway': disease.primary_pathway_affected,
            'biomarkers': disease.biomarkers,
            'recommended_drug': disease.recommended_drug,
            'expected_timeline_weeks': disease.expected_timeline_weeks,
            'monitoring_frequency': 'monthly' if profile.severity == 'severe' else 'quarterly'
        }
        
        return result


def main():
    """Main function for metabolic hierarchy mapping."""
    print("=" * 80)
    print("Metabolic Hierarchy Mapper")
    print("Clinical Mapping of Disease to Hierarchical Dysfunction")
    print("=" * 80)
    
    mapper = MetabolicHierarchyMapper()
    
    # Test patient cohort
    patients = [
        {
            'patient_id': 'PT001',
            'age': 55,
            'sex': 'M',
            'bmi': 32.5,
            'fasting_glucose': 145,
            'hba1c': 7.2,
            'insulin': 18.5,
            'triglycerides': 220,
            'hdl_cholesterol': 35,
            'ldl_cholesterol': 145
        },
        {
            'patient_id': 'PT002',
            'age': 48,
            'sex': 'F',
            'bmi': 28.3,
            'fasting_glucose': 105,
            'hba1c': 6.0,
            'insulin': 14.2,
            'triglycerides': 165,
            'hdl_cholesterol': 45,
            'ldl_cholesterol': 120
        },
        {
            'patient_id': 'PT003',
            'age': 35,
            'sex': 'M',
            'bmi': 23.1,
            'fasting_glucose': 88,
            'hba1c': 5.2,
            'insulin': 6.5,
            'triglycerides': 95,
            'hdl_cholesterol': 55,
            'ldl_cholesterol': 105
        }
    ]
    
    all_profiles = []
    all_mappings = []
    
    for patient_data in patients:
        print(f"\n{'='*60}")
        print(f"Patient: {patient_data['patient_id']}")
        print(f"{'='*60}")
        
        # Create profile
        profile = mapper.create_patient_profile(patient_data)
        all_profiles.append(profile.__dict__)
        
        # Print profile
        print(f"Age: {profile.age}, Sex: {profile.sex}, BMI: {profile.bmi:.1f}")
        print(f"Fasting Glucose:               {profile.fasting_glucose} mg/dL")
        print(f"HbA1c:                         {profile.hba1c:.1f}%")
        print(f"Insulin:                       {profile.insulin:.1f} μU/mL")
        print(f"HOMA-IR:                       {profile.homa_ir:.2f}")
        print(f"Metabolic Syndrome Score:      {profile.metabolic_syndrome_score}/5")
        print(f"Hierarchical Depth Estimate:   {profile.hierarchical_depth_estimate:.2f}")
        print(f"Disease State:                 {profile.disease_state} ({profile.severity})")
        
        # Map to hierarchy
        mapping = mapper.map_patient_to_hierarchy(profile)
        all_mappings.append(mapping)
        
        if mapping.get('error'):
            print(f"ERROR: {mapping['error']}")
            continue
        
        print(f"\nHierarchical Mapping:")
        print(f"Current Depth:                 {mapping['current_depth']:.2f}")
        print(f"Target Depth:                  {mapping['target_depth']:.2f}")
        print(f"Depth Deficit:                 {mapping['depth_deficit']:.2f}")
        print(f"Primary Pathway Affected:      {mapping['primary_pathway']}")
        print(f"\nDysfunction Pattern:")
        for dm in mapping['dysfunction_levels']:
            status = "✗" if dm['affected'] else "✓"
            severity = dm['dysfunction_severity']
            severity_str = f"{severity:.2f}" if severity >= 0 else f"+{abs(severity):.2f}"
            print(f"  L{dm['level']} {dm['name']:25s} {status}  Severity: {severity_str}")
        
        print(f"\nTherapeutic Recommendation:")
        print(f"Recommended Drug:              {mapping['recommended_drug']}")
        print(f"Expected Timeline:             {mapping['expected_timeline_weeks']} weeks")
        print(f"Monitoring Frequency:          {mapping['monitoring_frequency']}")
    
    # Save results
    output_dir = Path("chatelier/src/computing/results")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Save JSON
    json_path = output_dir / f"metabolic_hierarchy_mapping_{timestamp}.json"
    with open(json_path, 'w') as f:
        json.dump({
            'timestamp': timestamp,
            'description': 'Patient metabolic hierarchy mapping',
            'profiles': all_profiles,
            'mappings': all_mappings
        }, f, indent=2)
    
    print(f"\n{'='*60}")
    print(f"Results saved to: {json_path}")
    
    # Create visualization
    fig, axes = plt.subplots(2, 2, figsize=(14, 12))
    fig.suptitle('Metabolic Hierarchy Clinical Mapping', fontsize=16, fontweight='bold')
    
    # Plot 1: Hierarchical depth by patient
    ax = axes[0, 0]
    patient_ids = [p['patient_id'] for p in all_profiles]
    depths = [p['hierarchical_depth_estimate'] for p in all_profiles]
    colors_patients = ['#e74c3c' if d < 0.7 else '#f39c12' if d < 0.9 else '#2ecc71' for d in depths]
    bars = ax.bar(patient_ids, depths, color=colors_patients)
    ax.set_ylabel('Hierarchical Depth', fontweight='bold')
    ax.set_title('Patient Hierarchical Depth Estimates', fontweight='bold')
    ax.set_ylim([0, 1])
    ax.axhline(0.7, color='orange', linestyle='--', alpha=0.5, label='Intervention threshold')
    ax.axhline(0.9, color='green', linestyle='--', alpha=0.5, label='Healthy threshold')
    ax.legend()
    ax.grid(axis='y', alpha=0.3)
    for i, bar in enumerate(bars):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{depths[i]:.2f}',
                ha='center', va='bottom', fontweight='bold')
    
    # Plot 2: Metabolic syndrome scores
    ax = axes[0, 1]
    met_scores = [p['metabolic_syndrome_score'] for p in all_profiles]
    colors_met = ['#2ecc71' if s < 3 else '#e74c3c' for s in met_scores]
    bars = ax.bar(patient_ids, met_scores, color=colors_met)
    ax.set_ylabel('Metabolic Syndrome Score', fontweight='bold')
    ax.set_title('Metabolic Syndrome Criteria (≥3 = Syndrome)', fontweight='bold')
    ax.set_ylim([0, 5])
    ax.axhline(3, color='red', linestyle='--', alpha=0.5, label='Syndrome threshold')
    ax.legend()
    ax.grid(axis='y', alpha=0.3)
    for i, bar in enumerate(bars):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(met_scores[i])}',
                ha='center', va='bottom', fontweight='bold')
    
    # Plot 3: Dysfunction heatmap (first patient with disease)
    ax = axes[1, 0]
    diseased_mappings = [m for m in all_mappings if m.get('dysfunction_levels')]
    if diseased_mappings:
        mapping = diseased_mappings[0]
        levels = [dm['name'] for dm in mapping['dysfunction_levels']]
        severities = [dm['dysfunction_severity'] for dm in mapping['dysfunction_levels']]
        
        colors_heatmap = ['#27ae60' if s < 0 else '#e74c3c' if s > 0.5 else '#f39c12' if s > 0.2 else '#95a5a6' 
                         for s in severities]
        bars = ax.barh(levels, severities, color=colors_heatmap)
        ax.set_xlabel('Dysfunction Severity', fontweight='bold')
        ax.set_title(f'Hierarchical Dysfunction Pattern\n{mapping["patient_id"]}: {mapping["disease"]}', 
                    fontweight='bold')
        ax.axvline(0.5, color='red', linestyle='--', alpha=0.5, label='Severe')
        ax.legend()
        ax.grid(axis='x', alpha=0.3)
    
    # Plot 4: Treatment timeline
    ax = axes[1, 1]
    diseased_profiles = [p for p in all_profiles if p['disease_state'] != 'healthy']
    if diseased_profiles:
        diseased_patient_ids = [p['patient_id'] for p in diseased_profiles]
        diseased_mappings_filtered = [m for m in all_mappings if m['patient_id'] in diseased_patient_ids]
        
        timelines = [m['expected_timeline_weeks'] for m in diseased_mappings_filtered]
        depth_deficits = [m['depth_deficit'] for m in diseased_mappings_filtered]
        
        scatter = ax.scatter(depth_deficits, timelines, s=200, c=range(len(timelines)),
                            cmap='viridis', edgecolors='black', linewidths=2, alpha=0.7)
        for i, pid in enumerate(diseased_patient_ids):
            ax.annotate(pid, (depth_deficits[i], timelines[i]),
                       ha='center', va='center', fontweight='bold', color='white')
        
        ax.set_xlabel('Hierarchical Depth Deficit', fontweight='bold')
        ax.set_ylabel('Expected Treatment Timeline (weeks)', fontweight='bold')
        ax.set_title('Treatment Timeline vs. Dysfunction Severity', fontweight='bold')
        ax.grid(alpha=0.3)
    
    plt.tight_layout()
    
    # Save plot
    plot_path = output_dir / f"metabolic_hierarchy_mapping_{timestamp}.png"
    plt.savefig(plot_path, dpi=300, bbox_inches='tight')
    print(f"Plot saved to: {plot_path}")
    
    plt.close()
    
    print("\n" + "="*80)
    print("ANALYSIS COMPLETE")
    print("="*80)
    print("\nClinical Summary:")
    healthy_count = sum([1 for p in all_profiles if p['disease_state'] == 'healthy'])
    diseased_count = len(all_profiles) - healthy_count
    print(f"- Total Patients: {len(all_profiles)}")
    print(f"- Healthy: {healthy_count}")
    print(f"- Metabolic Dysfunction: {diseased_count}")
    print("- Hierarchical mapping enables precision medicine")
    print("- Therapeutic interventions target specific dysfunctional levels")
    print("="*80)
    
    return all_mappings


if __name__ == "__main__":
    main()

