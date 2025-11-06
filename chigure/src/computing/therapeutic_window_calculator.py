"""
Therapeutic Window Calculator
Calculates optimal dosing ranges for consciousness programming drugs.
Based on categorical state space reduction and phase-locking dynamics.
"""

import numpy as np
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from datetime import datetime
from pathlib import Path
from typing import Dict, Tuple, List
from dataclasses import dataclass


@dataclass
class TherapeuticWindow:
    """Dataclass for therapeutic window parameters."""
    drug_name: str
    min_effective_dose_mg: float
    max_safe_dose_mg: float
    therapeutic_index: float  # Max safe / Min effective
    optimal_dose_mg: float
    dosing_frequency_per_day: float
    
    # Consciousness programming metrics at optimal dose
    state_space_reduction: float  # 0-1
    phase_coherence_increase: float  # ΔR
    programming_specificity: float  # 0-1
    
    # Safety margins
    narrow_window: bool
    toxicity_risk: str  # 'low', 'moderate', 'high'
    individual_variability: float  # CV%


class TherapeuticWindowCalculator:
    """Calculate therapeutic windows based on consciousness programming framework."""
    
    def __init__(self):
        # Pharmacokinetic parameters
        self.volume_distribution_l = 42.0  # Average total body water (L)
        
        # Therapeutic targets from framework
        self.optimal_volume_reduction = (0.3, 0.7)  # 30-70% reduction
        self.optimal_phase_coherence = (0.4, 0.6)  # Order parameter R
        self.min_programming_specificity = 0.7
        
    def calculate_plasma_concentration(self, dose_mg: float, molecular_weight: float,
                                      bioavailability: float = 1.0) -> float:
        """
        Calculate plasma concentration from dose.
        C = (Dose × F) / (MW × Vd)
        """
        # Convert dose to moles
        dose_mol = (dose_mg / 1000.0) / molecular_weight
        
        # Plasma concentration (M)
        concentration = (dose_mol * bioavailability) / self.volume_distribution_l
        
        return concentration
    
    def dose_response_state_space(self, concentration: float, k_agg: float,
                                  baseline_constraint: float = 0.8) -> float:
        """
        Calculate state space reduction as function of drug concentration.
        From categorical reduction framework.
        """
        # Fraction of O2 bound to drug
        f_bound = (k_agg * concentration) / (1 + k_agg * concentration)
        
        # State space volume reduction
        # Higher f_bound → more constraint → smaller volume
        volume_reduction = baseline_constraint * (1 - np.exp(-10 * f_bound))
        
        return volume_reduction
    
    def dose_response_phase_coherence(self, concentration: float, k_agg: float,
                                     baseline_r: float = 0.3) -> float:
        """
        Calculate phase coherence increase as function of drug concentration.
        From Kuramoto network framework.
        """
        # Coupling strength modulation
        # K_modified = K_baseline × (1 + α × [Drug])
        alpha = k_agg / 1e5  # Scaling factor
        coupling_increase = 1 + alpha * concentration * 1e6  # Convert M to μM
        
        # Order parameter increase (saturates at high coupling)
        delta_r = (1 - baseline_r) * (1 - np.exp(-0.5 * coupling_increase))
        r_new = baseline_r + delta_r
        
        # Clip to physiological range
        r_new = np.clip(r_new, 0, 0.9)  # Never reach perfect sync (pathological)
        
        return r_new
    
    def calculate_programming_specificity(self, volume_reduction: float,
                                         phase_coherence: float) -> float:
        """
        Calculate programming specificity from state metrics.
        High specificity = targeted constraint without excessive reduction.
        """
        # Optimal volume reduction: 0.3-0.7
        if 0.3 <= volume_reduction <= 0.7:
            volume_score = 1.0
        elif volume_reduction < 0.3:
            volume_score = volume_reduction / 0.3
        else:  # > 0.7
            volume_score = (1.0 - volume_reduction) / 0.3
        
        # Optimal phase coherence: 0.4-0.6
        if 0.4 <= phase_coherence <= 0.6:
            coherence_score = 1.0
        elif phase_coherence < 0.4:
            coherence_score = phase_coherence / 0.4
        else:  # > 0.6
            coherence_score = (1.0 - phase_coherence) / 0.4
        
        # Combined specificity
        specificity = np.sqrt(volume_score * coherence_score)
        
        return specificity
    
    def calculate_toxicity_threshold(self, k_agg: float, bbb_penetration: float,
                                    narrow_window: bool) -> float:
        """
        Estimate toxicity threshold concentration.
        Higher K_agg + high BBB → lower toxicity threshold (more potent).
        """
        # Base toxicity threshold (M)
        base_threshold = 1e-3  # 1 mM
        
        # K_agg increases potency (lower threshold)
        potency_factor = np.sqrt(k_agg / 1e4)
        
        # BBB penetration increases CNS exposure
        cns_factor = 1 + bbb_penetration
        
        # Narrow window drugs have lower safety margin
        if narrow_window:
            safety_factor = 0.5
        else:
            safety_factor = 1.0
        
        # Toxicity threshold
        toxic_concentration = (base_threshold / (potency_factor * cns_factor)) * safety_factor
        
        return toxic_concentration
    
    def calculate_therapeutic_window(self, drug_name: str, molecular_weight: float,
                                    k_agg: float, bbb_penetration: float = 0.5,
                                    narrow_window: bool = False) -> TherapeuticWindow:
        """
        Calculate complete therapeutic window for a drug.
        """
        # Generate dose range (0.1 to 1000 mg)
        doses_mg = np.logspace(-1, 3, 1000)
        
        # Calculate responses for each dose
        concentrations = []
        state_reductions = []
        phase_coherences = []
        specificities = []
        
        for dose in doses_mg:
            conc = self.calculate_plasma_concentration(dose, molecular_weight)
            concentrations.append(conc)
            
            vol_red = self.dose_response_state_space(conc, k_agg)
            state_reductions.append(vol_red)
            
            phase_coh = self.dose_response_phase_coherence(conc, k_agg)
            phase_coherences.append(phase_coh)
            
            spec = self.calculate_programming_specificity(vol_red, phase_coh)
            specificities.append(spec)
        
        concentrations = np.array(concentrations)
        state_reductions = np.array(state_reductions)
        phase_coherences = np.array(phase_coherences)
        specificities = np.array(specificities)
        
        # Find minimum effective dose (specificity > 0.7)
        effective_indices = np.where(specificities > self.min_programming_specificity)[0]
        if len(effective_indices) == 0:
            min_effective_dose = doses_mg[-1]  # No effective dose found
            min_effective_idx = -1
        else:
            min_effective_idx = effective_indices[0]
            min_effective_dose = doses_mg[min_effective_idx]
        
        # Find maximum safe dose (below toxicity threshold)
        toxic_conc = self.calculate_toxicity_threshold(k_agg, bbb_penetration, narrow_window)
        safe_indices = np.where(concentrations < toxic_conc)[0]
        if len(safe_indices) == 0:
            max_safe_dose = doses_mg[0]  # Even lowest dose toxic
            max_safe_idx = 0
        else:
            max_safe_idx = safe_indices[-1]
            max_safe_dose = doses_mg[max_safe_idx]
        
        # Find optimal dose (maximum specificity within therapeutic window)
        if min_effective_idx >= 0 and max_safe_idx >= min_effective_idx:
            therapeutic_range = range(min_effective_idx, max_safe_idx + 1)
            optimal_idx = min_effective_idx + np.argmax(specificities[therapeutic_range])
            optimal_dose = doses_mg[optimal_idx]
            optimal_state_red = state_reductions[optimal_idx]
            optimal_phase_coh = phase_coherences[optimal_idx]
            optimal_spec = specificities[optimal_idx]
        else:
            # No therapeutic window
            optimal_dose = min_effective_dose
            optimal_state_red = 0.0
            optimal_phase_coh = 0.3
            optimal_spec = 0.0
        
        # Calculate therapeutic index
        if min_effective_dose > 0:
            therapeutic_index = max_safe_dose / min_effective_dose
        else:
            therapeutic_index = np.inf
        
        # Determine toxicity risk
        if therapeutic_index > 10:
            toxicity_risk = 'low'
        elif therapeutic_index > 3:
            toxicity_risk = 'moderate'
        else:
            toxicity_risk = 'high'
        
        # Estimate dosing frequency (based on half-life, approximate)
        # Shorter half-life → more frequent dosing
        # Assume 2-4 doses/day for most CNS drugs
        if narrow_window:
            dosing_frequency = 3.0  # TID for narrow window
        else:
            dosing_frequency = 2.0  # BID for wide window
        
        # Individual variability (CV%)
        # Narrow window drugs show higher variability in response
        if narrow_window:
            variability = 50.0  # 50% CV
        else:
            variability = 25.0  # 25% CV
        
        window = TherapeuticWindow(
            drug_name=drug_name,
            min_effective_dose_mg=min_effective_dose,
            max_safe_dose_mg=max_safe_dose,
            therapeutic_index=therapeutic_index,
            optimal_dose_mg=optimal_dose,
            dosing_frequency_per_day=dosing_frequency,
            state_space_reduction=optimal_state_red,
            phase_coherence_increase=optimal_phase_coh - 0.3,  # Δ from baseline
            programming_specificity=optimal_spec,
            narrow_window=narrow_window,
            toxicity_risk=toxicity_risk,
            individual_variability=variability
        )
        
        return window, doses_mg, concentrations, state_reductions, phase_coherences, specificities


def main():
    """Main function for therapeutic window analysis."""
    print("=" * 80)
    print("Therapeutic Window Calculator")
    print("Optimal Dosing for Consciousness Programming")
    print("=" * 80)
    
    calc = TherapeuticWindowCalculator()
    
    # Test drugs with properties
    drugs = {
        'lithium': {
            'molecular_weight': 6.94,
            'k_agg': 5e4,
            'bbb_penetration': 1.0,
            'narrow_window': True
        },
        'dopamine': {
            'molecular_weight': 153.18,
            'k_agg': 3e3,
            'bbb_penetration': 0.1,
            'narrow_window': False
        },
        'serotonin': {
            'molecular_weight': 176.22,
            'k_agg': 2e3,
            'bbb_penetration': 0.05,
            'narrow_window': False
        },
        'ssri_fluoxetine': {
            'molecular_weight': 309.33,
            'k_agg': 8e4,
            'bbb_penetration': 0.95,
            'narrow_window': False
        },
        'alprazolam': {
            'molecular_weight': 308.76,
            'k_agg': 1e5,
            'bbb_penetration': 0.98,
            'narrow_window': True
        }
    }
    
    all_results = []
    all_dose_responses = {}
    
    for drug_name, props in drugs.items():
        print(f"\n{'='*60}")
        print(f"Calculating: {drug_name.upper()}")
        print(f"{'='*60}")
        
        window, doses, concs, state_reds, phase_cohs, specs = calc.calculate_therapeutic_window(
            drug_name=drug_name,
            molecular_weight=props['molecular_weight'],
            k_agg=props['k_agg'],
            bbb_penetration=props['bbb_penetration'],
            narrow_window=props['narrow_window']
        )
        
        all_results.append(window.__dict__)
        all_dose_responses[drug_name] = {
            'doses': doses,
            'concentrations': concs,
            'state_reductions': state_reds,
            'phase_coherences': phase_cohs,
            'specificities': specs
        }
        
        # Print results
        print(f"Minimum Effective Dose:        {window.min_effective_dose_mg:.2f} mg")
        print(f"Maximum Safe Dose:             {window.max_safe_dose_mg:.2f} mg")
        print(f"Therapeutic Index:             {window.therapeutic_index:.2f}")
        print(f"Optimal Dose:                  {window.optimal_dose_mg:.2f} mg")
        print(f"Dosing Frequency:              {window.dosing_frequency_per_day:.1f} times/day")
        print(f"\nAt Optimal Dose:")
        print(f"State Space Reduction:         {window.state_space_reduction:.3f}")
        print(f"Phase Coherence Increase:      {window.phase_coherence_increase:.3f}")
        print(f"Programming Specificity:       {window.programming_specificity:.3f}")
        print(f"\nSafety Profile:")
        print(f"Narrow Therapeutic Window:     {window.narrow_window}")
        print(f"Toxicity Risk:                 {window.toxicity_risk}")
        print(f"Individual Variability:        {window.individual_variability:.1f}%")
    
    # Save results
    output_dir = Path("chatelier/src/computing/results")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Save JSON
    json_path = output_dir / f"therapeutic_window_results_{timestamp}.json"
    with open(json_path, 'w') as f:
        json.dump({
            'timestamp': timestamp,
            'description': 'Therapeutic windows for consciousness programming drugs',
            'results': all_results
        }, f, indent=2)
    
    print(f"\n{'='*60}")
    print(f"Results saved to: {json_path}")
    
    # Create visualizations
    fig, axes = plt.subplots(3, 2, figsize=(16, 14))
    fig.suptitle('Therapeutic Window Analysis', fontsize=16, fontweight='bold')
    
    colors = {
        'lithium': '#2ecc71',
        'dopamine': '#3498db',
        'serotonin': '#9b59b6',
        'ssri_fluoxetine': '#e74c3c',
        'alprazolam': '#f39c12'
    }
    
    # Plot 1: Dose-response (Programming Specificity)
    ax = axes[0, 0]
    for drug_name in drugs.keys():
        data = all_dose_responses[drug_name]
        ax.semilogx(data['doses'], data['specificities'], 
                   color=colors[drug_name], linewidth=2, label=drug_name)
    ax.axhline(0.7, color='red', linestyle='--', alpha=0.5, label='Min effective')
    ax.set_xlabel('Dose (mg)', fontweight='bold')
    ax.set_ylabel('Programming Specificity', fontweight='bold')
    ax.set_title('Dose-Response: Programming Specificity', fontweight='bold')
    ax.legend()
    ax.grid(alpha=0.3)
    
    # Plot 2: Dose-response (State Space Reduction)
    ax = axes[0, 1]
    for drug_name in drugs.keys():
        data = all_dose_responses[drug_name]
        ax.semilogx(data['doses'], data['state_reductions'],
                   color=colors[drug_name], linewidth=2, label=drug_name)
    ax.axhspan(0.3, 0.7, color='green', alpha=0.2, label='Therapeutic window')
    ax.set_xlabel('Dose (mg)', fontweight='bold')
    ax.set_ylabel('State Space Reduction', fontweight='bold')
    ax.set_title('Dose-Response: State Space Reduction', fontweight='bold')
    ax.legend()
    ax.grid(alpha=0.3)
    
    # Plot 3: Dose-response (Phase Coherence)
    ax = axes[1, 0]
    for drug_name in drugs.keys():
        data = all_dose_responses[drug_name]
        ax.semilogx(data['doses'], data['phase_coherences'],
                   color=colors[drug_name], linewidth=2, label=drug_name)
    ax.axhspan(0.4, 0.6, color='green', alpha=0.2, label='Therapeutic window')
    ax.set_xlabel('Dose (mg)', fontweight='bold')
    ax.set_ylabel('Phase Coherence (R)', fontweight='bold')
    ax.set_title('Dose-Response: Phase Coherence', fontweight='bold')
    ax.legend()
    ax.grid(alpha=0.3)
    
    # Plot 4: Therapeutic Index Comparison
    ax = axes[1, 1]
    ti_values = [r['therapeutic_index'] for r in all_results]
    drug_names = [r['drug_name'] for r in all_results]
    bars = ax.barh(drug_names, ti_values, color=[colors[d] for d in drug_names])
    ax.set_xlabel('Therapeutic Index', fontweight='bold')
    ax.set_title('Therapeutic Index Comparison', fontweight='bold')
    ax.axvline(3, color='orange', linestyle='--', label='Moderate risk')
    ax.axvline(10, color='green', linestyle='--', label='Low risk')
    ax.set_xscale('log')
    ax.legend()
    ax.grid(axis='x', alpha=0.3)
    
    # Plot 5: Optimal Dose Comparison
    ax = axes[2, 0]
    optimal_doses = [r['optimal_dose_mg'] for r in all_results]
    bars = ax.bar(drug_names, optimal_doses, color=[colors[d] for d in drug_names])
    ax.set_ylabel('Optimal Dose (mg)', fontweight='bold')
    ax.set_title('Optimal Dose Comparison', fontweight='bold')
    ax.set_yscale('log')
    ax.grid(axis='y', alpha=0.3)
    for i, bar in enumerate(bars):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{optimal_doses[i]:.1f}',
                ha='center', va='bottom', fontweight='bold', fontsize=9)
    plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha='right')
    
    # Plot 6: Programming Specificity at Optimal Dose
    ax = axes[2, 1]
    spec_values = [r['programming_specificity'] for r in all_results]
    bars = ax.bar(drug_names, spec_values, color=[colors[d] for d in drug_names])
    ax.set_ylabel('Programming Specificity', fontweight='bold')
    ax.set_title('Specificity at Optimal Dose', fontweight='bold')
    ax.set_ylim([0, 1])
    ax.axhline(0.7, color='red', linestyle='--', alpha=0.5, label='Min effective')
    ax.legend()
    ax.grid(axis='y', alpha=0.3)
    for i, bar in enumerate(bars):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{spec_values[i]:.3f}',
                ha='center', va='bottom', fontweight='bold')
    plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha='right')
    
    plt.tight_layout()
    
    # Save plot
    plot_path = output_dir / f"therapeutic_window_analysis_{timestamp}.png"
    plt.savefig(plot_path, dpi=300, bbox_inches='tight')
    print(f"Plot saved to: {plot_path}")
    
    plt.close()
    
    print("\n" + "="*80)
    print("ANALYSIS COMPLETE")
    print("="*80)
    
    return all_results


if __name__ == "__main__":
    main()

