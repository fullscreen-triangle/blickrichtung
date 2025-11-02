"""
Thought Metabolism Analysis: Calculating the Energy Cost of Conscious Thought

Based on Activity-Sleep Oscillatory Mirror Theory and multi-scale biological oscillations.

The approach:
1. Identify mirror regions between activity and sleep patterns
2. Calculate total energy expenditure during awake periods
3. Subtract locomotion energy (from MET data)
4. Subtract dream metabolism (REM sleep energy)
5. Subtract baseline metabolism
6. Result = Energy cost of coherent conscious thought

Theoretical Foundation:
- Activity-Sleep Mirror Theory (error accumulation & cleanup)
- Cognitive-Neuromuscular Oscillatory Coupling
- Atmospheric-Biological Oscillations (O2 information density)
- Allometric Scaling (metabolic rate scaling)
"""

import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from scipy import signal, stats
from typing import Dict, List, Tuple
import seaborn as sns

class ThoughtMetabolismAnalyzer:
    """
    Analyzes the metabolic cost of conscious thought by comparing
    activity and sleep patterns across oscillatory mirror regions.
    """
    
    def __init__(self, sleep_data_path: str, activity_data_path: str):
        """Load sleep and activity data."""
        with open(sleep_data_path, 'r') as f:
            self.sleep_data = json.load(f)
        with open(activity_data_path, 'r') as f:
            self.activity_data = json.load(f)
        
        # Constants from theoretical framework
        self.BASELINE_MET = 0.9  # Resting metabolic rate
        self.ERROR_ACCUMULATION_COEFF = 0.1  # error units per MET-minute
        self.DEEP_CLEANUP_COEFF = 2.5  # cleanup efficiency
        self.REM_CLEANUP_COEFF = 2.0  # cleanup efficiency
        self.LIGHT_CLEANUP_COEFF = 1.2  # estimated
        
        # Oxygen information density (from atmospheric-biological paper)
        self.O2_INFO_DENSITY = 3.2e15  # bits/molecule/s
        
        # Allometric constants
        self.UNIVERSAL_OSC_CONSTANT = 2.3  # Ω from allometric paper
        
        # Results storage
        self.results = {}
        
    def convert_timestamp(self, ts_ms: int) -> datetime:
        """Convert millisecond timestamp to datetime."""
        return datetime.fromtimestamp(ts_ms / 1000)
    
    def calculate_baseline_metabolism(self, body_weight_kg: float = 70) -> Dict:
        """
        Calculate baseline metabolic rate using allometric scaling.
        
        From paper: B = B₀ * M^(3/4)
        Typical human: ~1500-1800 kcal/day baseline
        """
        # Harris-Benedict equation adjusted for oscillatory framework
        BMR_kcal_day = 88.362 + (13.397 * body_weight_kg) * (body_weight_kg ** 0.75) / body_weight_kg
        BMR_kcal_hr = BMR_kcal_day / 24
        BMR_watts = BMR_kcal_hr * 1.163  # Convert to watts
        
        return {
            'kcal_per_day': BMR_kcal_day,
            'kcal_per_hour': BMR_kcal_hr,
            'watts': BMR_watts,
            'met_equivalent': self.BASELINE_MET
        }
    
    def extract_hypnogram_data(self, sleep_record: Dict) -> pd.DataFrame:
        """
        Extract and parse hypnogram data (5-minute sleep stages).
        
        Stages: '1' = Deep, '2' = Light, '3' = REM, '4' = Awake
        """
        hypnogram = sleep_record.get('hypnogram_5min', '')
        if not hypnogram:
            return pd.DataFrame()
        
        stages = [int(s) for s in hypnogram]
        duration_hrs = sleep_record.get('duration_in_hrs', len(stages) * 5 / 60)
        
        # Create time series
        start_time = self.convert_timestamp(sleep_record['bedtime_start_dt_adjusted'])
        times = [start_time + timedelta(minutes=i*5) for i in range(len(stages))]
        
        df = pd.DataFrame({
            'time': times,
            'stage': stages,
            'stage_name': ['Deep' if s == 1 else 'Light' if s == 2 else 'REM' if s == 3 else 'Awake' 
                          for s in stages]
        })
        
        return df
    
    def extract_activity_met_data(self, activity_record: Dict) -> pd.DataFrame:
        """
        Extract and parse MET (Metabolic Equivalent of Task) data.
        
        MET values indicate intensity: 
        - 0.9 = Rest
        - 1.0-1.5 = Sedentary
        - 1.5-3.0 = Light activity
        - 3.0-6.0 = Moderate activity
        - 6.0+ = Vigorous activity
        """
        met_1min = activity_record.get('met_1min', '')
        if not met_1min:
            # Fallback to 5-minute class data
            return self._extract_activity_class_data(activity_record)
        
        # Parse MET string (comma or space separated)
        if isinstance(met_1min, str):
            met_values = [float(m) for m in met_1min.replace(',', ' ').split() if m]
        else:
            met_values = met_1min
        
        start_time = self.convert_timestamp(activity_record['day_start_dt_adjusted'])
        times = [start_time + timedelta(minutes=i) for i in range(len(met_values))]
        
        df = pd.DataFrame({
            'time': times,
            'met': met_values
        })
        
        return df
    
    def _extract_activity_class_data(self, activity_record: Dict) -> pd.DataFrame:
        """Fallback: extract 5-minute activity classification."""
        class_5min = activity_record.get('class_5min', '')
        if not class_5min:
            return pd.DataFrame()
        
        # Class: '0'=non-wear, '1'=rest, '2'=inactive, '3'=low, '4'=medium, '5'=high
        classes = [int(c) for c in class_5min]
        
        # Map to approximate MET values
        met_mapping = {0: 0, 1: 0.9, 2: 1.0, 3: 1.8, 4: 3.0, 5: 6.0}
        met_values = [met_mapping.get(c, 1.0) for c in classes]
        
        start_time = self.convert_timestamp(activity_record['day_start_dt_adjusted'])
        times = [start_time + timedelta(minutes=i*5) for i in range(len(classes))]
        
        df = pd.DataFrame({
            'time': times,
            'met': met_values,
            'activity_class': classes
        })
        
        return df
    
    def calculate_sleep_metabolism(self, sleep_record: Dict, body_weight_kg: float = 70) -> Dict:
        """
        Calculate energy expenditure during different sleep stages.
        
        Stages have different metabolic rates:
        - Deep sleep: 0.85 * BMR (lowest metabolism, max cleanup)
        - Light sleep: 0.90 * BMR (moderate cleanup)
        - REM sleep: 0.95 * BMR (dream thought metabolism)
        - Awake in bed: 1.0 * BMR
        """
        baseline = self.calculate_baseline_metabolism(body_weight_kg)
        BMR_kcal_hr = baseline['kcal_per_hour']
        
        # Extract durations
        deep_hrs = sleep_record.get('deep_in_hrs', 0)
        light_hrs = sleep_record.get('light_in_hrs', 0)
        rem_hrs = sleep_record.get('rem_in_hrs', 0)
        awake_hrs = sleep_record.get('awake_in_hrs', 0)
        
        # Calculate energy for each stage
        deep_energy = deep_hrs * BMR_kcal_hr * 0.85
        light_energy = light_hrs * BMR_kcal_hr * 0.90
        rem_energy = rem_hrs * BMR_kcal_hr * 0.95  # REM includes dream thought
        awake_energy = awake_hrs * BMR_kcal_hr * 1.0
        
        total_energy = deep_energy + light_energy + rem_energy + awake_energy
        
        # Calculate cleanup capacity (from mirror theory)
        cleanup_deep = self.DEEP_CLEANUP_COEFF * deep_hrs * (sleep_record.get('efficiency', 85) / 100)
        cleanup_rem = self.REM_CLEANUP_COEFF * rem_hrs * (sleep_record.get('efficiency', 85) / 100)
        total_cleanup = cleanup_deep + cleanup_rem
        
        return {
            'total_energy_kcal': total_energy,
            'deep_energy_kcal': deep_energy,
            'light_energy_kcal': light_energy,
            'rem_energy_kcal': rem_energy,
            'awake_energy_kcal': awake_energy,
            'cleanup_capacity': total_cleanup,
            'deep_hrs': deep_hrs,
            'light_hrs': light_hrs,
            'rem_hrs': rem_hrs,
            'awake_hrs': awake_hrs,
            'total_sleep_hrs': deep_hrs + light_hrs + rem_hrs,
            'efficiency': sleep_record.get('efficiency', 0)
        }
    
    def calculate_activity_metabolism(self, activity_record: Dict, body_weight_kg: float = 70) -> Dict:
        """
        Calculate energy expenditure during awake activity.
        
        Total energy = Baseline + (MET - Baseline_MET) * time * weight_factor
        """
        baseline = self.calculate_baseline_metabolism(body_weight_kg)
        
        # Get MET data
        met_df = self.extract_activity_met_data(activity_record)
        if met_df.empty:
            return {
                'total_energy_kcal': activity_record.get('cal_total', 0),
                'active_energy_kcal': activity_record.get('cal_active', 0),
                'locomotion_energy_kcal': 0,
                'error_accumulation': 0
            }
        
        # Calculate energy for each minute/period
        met_df['energy_kcal'] = met_df['met'] * body_weight_kg * (1/60)  # kcal per minute
        met_df['baseline_kcal'] = self.BASELINE_MET * body_weight_kg * (1/60)
        met_df['active_kcal'] = met_df['energy_kcal'] - met_df['baseline_kcal']
        
        # Separate locomotion from baseline activity
        met_df['is_locomotion'] = met_df['met'] > 1.5  # Threshold for physical movement
        locomotion_energy = met_df[met_df['is_locomotion']]['active_kcal'].sum()
        
        # Calculate error accumulation (from mirror theory)
        met_df['error_rate'] = self.ERROR_ACCUMULATION_COEFF * np.maximum(0, met_df['met'] - self.BASELINE_MET)
        total_error = met_df['error_rate'].sum()
        
        total_energy = met_df['energy_kcal'].sum()
        active_energy = met_df['active_kcal'].sum()
        
        return {
            'total_energy_kcal': total_energy,
            'active_energy_kcal': active_energy,
            'locomotion_energy_kcal': locomotion_energy,
            'non_locomotion_active_kcal': active_energy - locomotion_energy,
            'error_accumulation': total_error,
            'average_met': met_df['met'].mean(),
            'peak_met': met_df['met'].max(),
            'active_minutes': (met_df['met'] > self.BASELINE_MET).sum()
        }
    
    def find_mirror_regions(self) -> List[Tuple[Dict, Dict]]:
        """
        Identify activity-sleep mirror pairs where cleanup matches error accumulation.
        
        Mirror coefficient: C_total / E_total ≈ 1 (from paper)
        """
        mirror_pairs = []
        
        for sleep_rec in self.sleep_data:
            sleep_start = self.convert_timestamp(sleep_rec['bedtime_start_dt_adjusted'])
            
            # Find activity record from same day or previous day
            for activity_rec in self.activity_data:
                activity_start = self.convert_timestamp(activity_rec['day_start_dt_adjusted'])
                
                # Check if activity is within 24 hours before sleep
                time_diff = (sleep_start - activity_start).total_seconds() / 3600
                if 0 <= time_diff <= 24:
                    # Calculate mirror coefficient
                    sleep_meta = self.calculate_sleep_metabolism(sleep_rec)
                    activity_meta = self.calculate_activity_metabolism(activity_rec)
                    
                    if activity_meta['error_accumulation'] > 0:
                        mirror_coeff = sleep_meta['cleanup_capacity'] / activity_meta['error_accumulation']
                        
                        # Good mirror: 0.8 < coefficient < 1.2
                        if 0.8 < mirror_coeff < 1.2:
                            mirror_pairs.append({
                                'activity': activity_rec,
                                'sleep': sleep_rec,
                                'activity_meta': activity_meta,
                                'sleep_meta': sleep_meta,
                                'mirror_coefficient': mirror_coeff,
                                'time_diff_hrs': time_diff
                            })
        
        return mirror_pairs
    
    def calculate_thought_metabolism(self, mirror_pairs: List[Dict], body_weight_kg: float = 70) -> Dict:
        """
        Calculate the metabolic cost of coherent conscious thought.
        
        Approach:
        1. Total awake energy = Baseline + Locomotion + Thought
        2. Total sleep energy = Baseline + Dream + Cleanup
        3. REM energy = Baseline + Dream (incoherent thought)
        4. Thought energy = (Awake - Baseline - Locomotion)
        5. Coherent thought = Thought - (REM - Baseline) * (Awake_hrs / REM_hrs)
        """
        results = []
        
        for pair in mirror_pairs:
            activity_meta = pair['activity_meta']
            sleep_meta = pair['sleep_meta']
            
            # Calculate baseline for awake period (assume 16 hours awake)
            awake_hrs = 16  # Typical waking hours
            baseline = self.calculate_baseline_metabolism(body_weight_kg)
            baseline_awake_kcal = baseline['kcal_per_hour'] * awake_hrs
            
            # Total awake energy
            total_awake_kcal = activity_meta['total_energy_kcal']
            
            # Locomotion energy
            locomotion_kcal = activity_meta['locomotion_energy_kcal']
            
            # REM (dream) metabolism above baseline
            rem_baseline_kcal = baseline['kcal_per_hour'] * sleep_meta['rem_hrs'] * 0.85
            rem_total_kcal = sleep_meta['rem_energy_kcal']
            dream_metabolism_kcal = rem_total_kcal - rem_baseline_kcal
            
            # Scale dream metabolism to awake hours (since REM is shorter)
            if sleep_meta['rem_hrs'] > 0:
                dream_metabolism_awake_scaled = dream_metabolism_kcal * (awake_hrs / sleep_meta['rem_hrs'])
            else:
                dream_metabolism_awake_scaled = 0
            
            # Coherent thought metabolism
            # = Total awake - Baseline - Locomotion - (Dream scaled to awake time)
            coherent_thought_kcal = (total_awake_kcal - baseline_awake_kcal - 
                                     locomotion_kcal - dream_metabolism_awake_scaled)
            
            # Thought power (watts)
            coherent_thought_watts = coherent_thought_kcal * 1.163 / awake_hrs
            
            # Thought energy per hour
            thought_kcal_per_hr = coherent_thought_kcal / awake_hrs
            
            # Information processing rate (from O2 coupling)
            # Assuming thought utilizes oxygen information density
            thought_info_rate = coherent_thought_watts * self.O2_INFO_DENSITY / 1e12  # Tbits/s
            
            results.append({
                'mirror_coefficient': pair['mirror_coefficient'],
                'total_awake_kcal': total_awake_kcal,
                'baseline_awake_kcal': baseline_awake_kcal,
                'locomotion_kcal': locomotion_kcal,
                'dream_metabolism_kcal': dream_metabolism_kcal,
                'dream_scaled_kcal': dream_metabolism_awake_scaled,
                'coherent_thought_kcal': coherent_thought_kcal,
                'coherent_thought_watts': coherent_thought_watts,
                'thought_kcal_per_hr': thought_kcal_per_hr,
                'thought_info_rate_Tbits_s': thought_info_rate,
                'awake_hrs': awake_hrs,
                'rem_hrs': sleep_meta['rem_hrs'],
                'error_accumulation': activity_meta['error_accumulation'],
                'cleanup_capacity': sleep_meta['cleanup_capacity']
            })
        
        # Aggregate statistics
        thought_kcal_values = [r['coherent_thought_kcal'] for r in results]
        thought_watts_values = [r['coherent_thought_watts'] for r in results]
        thought_hr_values = [r['thought_kcal_per_hr'] for r in results]
        
        return {
            'n_mirror_pairs': len(results),
            'mean_thought_kcal_per_day': np.mean(thought_kcal_values) if thought_kcal_values else 0,
            'std_thought_kcal_per_day': np.std(thought_kcal_values) if thought_kcal_values else 0,
            'mean_thought_watts': np.mean(thought_watts_values) if thought_watts_values else 0,
            'std_thought_watts': np.std(thought_watts_values) if thought_watts_values else 0,
            'mean_thought_kcal_per_hr': np.mean(thought_hr_values) if thought_hr_values else 0,
            'std_thought_kcal_per_hr': np.std(thought_hr_values) if thought_hr_values else 0,
            'median_thought_kcal_per_day': np.median(thought_kcal_values) if thought_kcal_values else 0,
            'details': results
        }
    
    def analyze(self, body_weight_kg: float = 70) -> Dict:
        """
        Perform complete thought metabolism analysis.
        """
        print("=" * 80)
        print("THOUGHT METABOLISM ANALYSIS")
        print("=" * 80)
        
        # Step 1: Find mirror regions
        print("\n[1] Finding activity-sleep mirror regions...")
        mirror_pairs = self.find_mirror_regions()
        print(f"    Found {len(mirror_pairs)} mirror pairs")
        if mirror_pairs:
            coeffs = [p['mirror_coefficient'] for p in mirror_pairs[:5]]
            print(f"    Mirror coefficients: {[f'{c:.2f}' for c in coeffs]}...")
        
        # Step 2: Calculate thought metabolism
        print("\n[2] Calculating thought metabolism...")
        thought_results = self.calculate_thought_metabolism(mirror_pairs, body_weight_kg)
        
        print(f"\n{'='*80}")
        print("RESULTS: METABOLIC COST OF COHERENT CONSCIOUS THOUGHT")
        print(f"{'='*80}")
        print(f"  Mirror pairs analyzed: {thought_results['n_mirror_pairs']}")
        print(f"\n  Coherent Thought Energy:")
        print(f"    {thought_results['mean_thought_kcal_per_day']:.1f} ± {thought_results['std_thought_kcal_per_day']:.1f} kcal/day")
        print(f"    {thought_results['mean_thought_kcal_per_hr']:.1f} ± {thought_results['std_thought_kcal_per_hr']:.1f} kcal/hr")
        print(f"    {thought_results['mean_thought_watts']:.1f} ± {thought_results['std_thought_watts']:.1f} watts")
        print(f"\n  Median: {thought_results['median_thought_kcal_per_day']:.1f} kcal/day")
        print(f"{'='*80}\n")
        
        self.results = {
            'mirror_pairs': mirror_pairs,
            'thought_metabolism': thought_results,
            'body_weight_kg': body_weight_kg
        }
        
        return self.results
    
    def save_results(self, output_path: str = 'thought_metabolism_results.json'):
        """Save analysis results to JSON."""
        if not self.results:
            print("No results to save. Run analyze() first.")
            return
        
        # Prepare serializable results
        serializable_results = {
            'n_mirror_pairs': self.results['thought_metabolism']['n_mirror_pairs'],
            'mean_thought_kcal_per_day': float(self.results['thought_metabolism']['mean_thought_kcal_per_day']),
            'std_thought_kcal_per_day': float(self.results['thought_metabolism']['std_thought_kcal_per_day']),
            'mean_thought_watts': float(self.results['thought_metabolism']['mean_thought_watts']),
            'std_thought_watts': float(self.results['thought_metabolism']['std_thought_watts']),
            'mean_thought_kcal_per_hr': float(self.results['thought_metabolism']['mean_thought_kcal_per_hr']),
            'std_thought_kcal_per_hr': float(self.results['thought_metabolism']['std_thought_kcal_per_hr']),
            'median_thought_kcal_per_day': float(self.results['thought_metabolism']['median_thought_kcal_per_day']),
            'body_weight_kg': self.results['body_weight_kg'],
            'theoretical_constants': {
                'baseline_met': self.BASELINE_MET,
                'error_accumulation_coeff': self.ERROR_ACCUMULATION_COEFF,
                'deep_cleanup_coeff': self.DEEP_CLEANUP_COEFF,
                'rem_cleanup_coeff': self.REM_CLEANUP_COEFF,
                'o2_info_density': self.O2_INFO_DENSITY,
                'universal_osc_constant': self.UNIVERSAL_OSC_CONSTANT
            },
            'details': [
                {k: float(v) if isinstance(v, (np.floating, np.integer)) else v 
                 for k, v in detail.items()}
                for detail in self.results['thought_metabolism']['details']
            ]
        }
        
        with open(output_path, 'w') as f:
            json.dump(serializable_results, f, indent=2)
        
        print(f"Results saved to: {output_path}")
    
    def visualize(self, output_dir: str = 'thought_metabolism_figures'):
        """Generate comprehensive visualizations."""
        import os
        os.makedirs(output_dir, exist_ok=True)
        
        if not self.results:
            print("No results to visualize. Run analyze() first.")
            return
        
        details = self.results['thought_metabolism']['details']
        if not details:
            print("No detailed results available.")
            return
        
        # Create comprehensive figure
        fig = plt.figure(figsize=(20, 12))
        gs = fig.add_gridspec(3, 4, hspace=0.3, wspace=0.3)
        
        # 1. Thought energy distribution
        ax1 = fig.add_subplot(gs[0, 0])
        thought_kcal = [d['coherent_thought_kcal'] for d in details]
        ax1.hist(thought_kcal, bins=20, color='steelblue', alpha=0.7, edgecolor='black')
        ax1.axvline(np.mean(thought_kcal), color='red', linestyle='--', linewidth=2, label=f'Mean: {np.mean(thought_kcal):.1f}')
        ax1.axvline(np.median(thought_kcal), color='orange', linestyle='--', linewidth=2, label=f'Median: {np.median(thought_kcal):.1f}')
        ax1.set_xlabel('Coherent Thought Energy (kcal/day)', fontsize=11, fontweight='bold')
        ax1.set_ylabel('Frequency', fontsize=11, fontweight='bold')
        ax1.set_title('Distribution of Thought Metabolism', fontsize=12, fontweight='bold')
        ax1.legend()
        ax1.grid(alpha=0.3)
        
        # 2. Thought power (watts)
        ax2 = fig.add_subplot(gs[0, 1])
        thought_watts = [d['coherent_thought_watts'] for d in details]
        ax2.hist(thought_watts, bins=20, color='coral', alpha=0.7, edgecolor='black')
        ax2.axvline(np.mean(thought_watts), color='red', linestyle='--', linewidth=2, label=f'Mean: {np.mean(thought_watts):.1f} W')
        ax2.set_xlabel('Coherent Thought Power (watts)', fontsize=11, fontweight='bold')
        ax2.set_ylabel('Frequency', fontsize=11, fontweight='bold')
        ax2.set_title('Thought Power Distribution', fontsize=12, fontweight='bold')
        ax2.legend()
        ax2.grid(alpha=0.3)
        
        # 3. Energy breakdown (stacked bar)
        ax3 = fig.add_subplot(gs[0, 2])
        mean_baseline = np.mean([d['baseline_awake_kcal'] for d in details])
        mean_locomotion = np.mean([d['locomotion_kcal'] for d in details])
        mean_dream = np.mean([d['dream_scaled_kcal'] for d in details])
        mean_thought = np.mean([d['coherent_thought_kcal'] for d in details])
        
        categories = ['Baseline', 'Locomotion', 'Dream\n(scaled)', 'Coherent\nThought']
        values = [mean_baseline, mean_locomotion, mean_dream, mean_thought]
        colors = ['lightgray', 'lightgreen', 'plum', 'steelblue']
        
        bars = ax3.bar(categories, values, color=colors, edgecolor='black', linewidth=1.5)
        for bar, val in zip(bars, values):
            height = bar.get_height()
            ax3.text(bar.get_x() + bar.get_width()/2., height,
                    f'{val:.0f}',
                    ha='center', va='bottom', fontsize=10, fontweight='bold')
        
        ax3.set_ylabel('Energy (kcal/day)', fontsize=11, fontweight='bold')
        ax3.set_title('Mean Energy Breakdown', fontsize=12, fontweight='bold')
        ax3.grid(axis='y', alpha=0.3)
        
        # 4. Mirror coefficient vs thought energy
        ax4 = fig.add_subplot(gs[0, 3])
        mirror_coeffs = [d['mirror_coefficient'] for d in details]
        ax4.scatter(mirror_coeffs, thought_kcal, alpha=0.6, s=50, color='purple', edgecolor='black')
        ax4.set_xlabel('Mirror Coefficient', fontsize=11, fontweight='bold')
        ax4.set_ylabel('Thought Energy (kcal/day)', fontsize=11, fontweight='bold')
        ax4.set_title('Mirror Quality vs Thought Energy', fontsize=12, fontweight='bold')
        ax4.axvline(1.0, color='red', linestyle='--', linewidth=1.5, label='Perfect Mirror')
        ax4.legend()
        ax4.grid(alpha=0.3)
        
        # 5. Error accumulation vs cleanup capacity
        ax5 = fig.add_subplot(gs[1, 0])
        error_acc = [d['error_accumulation'] for d in details]
        cleanup_cap = [d['cleanup_capacity'] for d in details]
        ax5.scatter(error_acc, cleanup_cap, alpha=0.6, s=50, color='teal', edgecolor='black')
        ax5.plot([min(error_acc), max(error_acc)], [min(error_acc), max(error_acc)], 
                'r--', linewidth=2, label='Perfect Mirror (y=x)')
        ax5.set_xlabel('Error Accumulation (units)', fontsize=11, fontweight='bold')
        ax5.set_ylabel('Cleanup Capacity (units)', fontsize=11, fontweight='bold')
        ax5.set_title('Activity-Sleep Mirror Validation', fontsize=12, fontweight='bold')
        ax5.legend()
        ax5.grid(alpha=0.3)
        
        # 6. Thought energy per hour
        ax6 = fig.add_subplot(gs[1, 1])
        thought_per_hr = [d['thought_kcal_per_hr'] for d in details]
        ax6.hist(thought_per_hr, bins=20, color='gold', alpha=0.7, edgecolor='black')
        ax6.axvline(np.mean(thought_per_hr), color='red', linestyle='--', linewidth=2, 
                   label=f'Mean: {np.mean(thought_per_hr):.1f} kcal/hr')
        ax6.set_xlabel('Thought Energy per Hour (kcal/hr)', fontsize=11, fontweight='bold')
        ax6.set_ylabel('Frequency', fontsize=11, fontweight='bold')
        ax6.set_title('Hourly Thought Metabolism', fontsize=12, fontweight='bold')
        ax6.legend()
        ax6.grid(alpha=0.3)
        
        # 7. Cumulative energy over mirror pairs
        ax7 = fig.add_subplot(gs[1, 2:])
        sorted_idx = np.argsort(thought_kcal)
        cumulative_thought = np.cumsum(np.array(thought_kcal)[sorted_idx])
        cumulative_baseline = np.cumsum(np.array([d['baseline_awake_kcal'] for d in details])[sorted_idx])
        cumulative_locomotion = np.cumsum(np.array([d['locomotion_kcal'] for d in details])[sorted_idx])
        
        ax7.fill_between(range(len(cumulative_thought)), 0, cumulative_baseline, 
                         alpha=0.3, color='lightgray', label='Baseline')
        ax7.fill_between(range(len(cumulative_thought)), cumulative_baseline, 
                         cumulative_baseline + cumulative_locomotion, 
                         alpha=0.3, color='lightgreen', label='Locomotion')
        ax7.fill_between(range(len(cumulative_thought)), 
                         cumulative_baseline + cumulative_locomotion, 
                         cumulative_baseline + cumulative_locomotion + cumulative_thought, 
                         alpha=0.3, color='steelblue', label='Thought')
        
        ax7.plot(cumulative_thought, color='steelblue', linewidth=2, label='Thought (cumulative)')
        ax7.set_xlabel('Mirror Pair (sorted by thought energy)', fontsize=11, fontweight='bold')
        ax7.set_ylabel('Cumulative Energy (kcal)', fontsize=11, fontweight='bold')
        ax7.set_title('Cumulative Energy Across Mirror Pairs', fontsize=12, fontweight='bold')
        ax7.legend()
        ax7.grid(alpha=0.3)
        
        # 8. Violin plot: Energy components
        ax8 = fig.add_subplot(gs[2, 0])
        data_for_violin = [
            [d['baseline_awake_kcal'] for d in details],
            [d['locomotion_kcal'] for d in details],
            [d['dream_scaled_kcal'] for d in details],
            [d['coherent_thought_kcal'] for d in details]
        ]
        parts = ax8.violinplot(data_for_violin, positions=[1, 2, 3, 4], showmeans=True, showmedians=True)
        ax8.set_xticks([1, 2, 3, 4])
        ax8.set_xticklabels(['Baseline', 'Locomotion', 'Dream', 'Thought'], rotation=15)
        ax8.set_ylabel('Energy (kcal/day)', fontsize=11, fontweight='bold')
        ax8.set_title('Energy Component Distributions', fontsize=12, fontweight='bold')
        ax8.grid(axis='y', alpha=0.3)
        
        # 9. Box plot: Thought watts by mirror quality bins
        ax9 = fig.add_subplot(gs[2, 1])
        mirror_bins = pd.cut(mirror_coeffs, bins=[0.8, 0.95, 1.05, 1.2], labels=['Low', 'Optimal', 'High'])
        df_mirror = pd.DataFrame({'mirror_quality': mirror_bins, 'thought_watts': thought_watts})
        df_mirror.boxplot(column='thought_watts', by='mirror_quality', ax=ax9)
        ax9.set_xlabel('Mirror Quality', fontsize=11, fontweight='bold')
        ax9.set_ylabel('Thought Power (watts)', fontsize=11, fontweight='bold')
        ax9.set_title('Thought Power by Mirror Quality', fontsize=12, fontweight='bold')
        plt.sca(ax9)
        plt.xticks(rotation=0)
        ax9.get_figure().suptitle('')  # Remove auto-generated title
        ax9.grid(alpha=0.3)
        
        # 10. Scatter matrix (mini version)
        ax10 = fig.add_subplot(gs[2, 2:])
        scatter_data = pd.DataFrame({
            'Thought (kcal/day)': thought_kcal,
            'Mirror Coeff.': mirror_coeffs,
            'Error Accum.': error_acc,
            'Cleanup Cap.': cleanup_cap
        })
        pd.plotting.scatter_matrix(scatter_data, ax=ax10, alpha=0.5, diagonal='hist', 
                                   grid=True, figsize=(8, 6))
        ax10.set_title('Correlation Matrix', fontsize=12, fontweight='bold')
        
        plt.suptitle('THOUGHT METABOLISM ANALYSIS: Metabolic Cost of Coherent Conscious Thought', 
                    fontsize=16, fontweight='bold', y=0.995)
        
        output_path = os.path.join(output_dir, 'thought_metabolism_comprehensive.png')
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        print(f"Visualization saved to: {output_path}")
        plt.close()
        
        # Generate summary text report
        self._generate_text_report(output_dir)
    
    def _generate_text_report(self, output_dir: str):
        """Generate detailed text report."""
        report_path = os.path.join(output_dir, 'thought_metabolism_report.txt')
        
        results = self.results['thought_metabolism']
        details = results['details']
        
        with open(report_path, 'w') as f:
            f.write("="*80 + "\n")
            f.write("THOUGHT METABOLISM ANALYSIS: COMPREHENSIVE REPORT\n")
            f.write("="*80 + "\n\n")
            
            f.write("THEORETICAL FOUNDATION:\n")
            f.write("-" * 80 + "\n")
            f.write("1. Activity-Sleep Oscillatory Mirror Theory\n")
            f.write("   - Error accumulation coefficient: {:.2f} units per MET-minute\n".format(self.ERROR_ACCUMULATION_COEFF))
            f.write("   - Deep sleep cleanup coefficient: {:.2f}\n".format(self.DEEP_CLEANUP_COEFF))
            f.write("   - REM sleep cleanup coefficient: {:.2f}\n\n".format(self.REM_CLEANUP_COEFF))
            
            f.write("2. Atmospheric-Biological Oscillations\n")
            f.write("   - O₂ information density: {:.2e} bits/molecule/s\n".format(self.O2_INFO_DENSITY))
            f.write("   - Universal oscillatory constant Ω: {:.2f}\n\n".format(self.UNIVERSAL_OSC_CONSTANT))
            
            f.write("\nEXPERIMENTAL RESULTS:\n")
            f.write("-" * 80 + "\n")
            f.write(f"Mirror pairs analyzed: {results['n_mirror_pairs']}\n\n")
            
            f.write("COHERENT CONSCIOUS THOUGHT METABOLISM:\n")
            f.write(f"  Mean: {results['mean_thought_kcal_per_day']:.1f} ± {results['std_thought_kcal_per_day']:.1f} kcal/day\n")
            f.write(f"  Median: {results['median_thought_kcal_per_day']:.1f} kcal/day\n")
            f.write(f"  Mean: {results['mean_thought_kcal_per_hr']:.1f} ± {results['std_thought_kcal_per_hr']:.1f} kcal/hr\n")
            f.write(f"  Mean: {results['mean_thought_watts']:.1f} ± {results['std_thought_watts']:.1f} watts\n\n")
            
            f.write("COMPARISON TO KNOWN VALUES:\n")
            f.write("  Brain baseline metabolism: ~20W (20% of BMR)\n")
            f.write(f"  Our calculated thought metabolism: {results['mean_thought_watts']:.1f}W\n")
            f.write("  Interpretation: Coherent conscious thought represents additional\n")
            f.write("                  metabolic cost beyond baseline brain function\n\n")
            
            f.write("MIRROR QUALITY STATISTICS:\n")
            mirror_coeffs = [d['mirror_coefficient'] for d in details]
            f.write(f"  Mean mirror coefficient: {np.mean(mirror_coeffs):.3f}\n")
            f.write(f"  Std mirror coefficient: {np.std(mirror_coeffs):.3f}\n")
            f.write(f"  Near-perfect mirrors (0.95-1.05): {sum(0.95 < c < 1.05 for c in mirror_coeffs)}/{len(mirror_coeffs)}\n\n")
            
            f.write("ENERGY BREAKDOWN (Mean values):\n")
            f.write(f"  Baseline metabolism: {np.mean([d['baseline_awake_kcal'] for d in details]):.1f} kcal/day\n")
            f.write(f"  Locomotion: {np.mean([d['locomotion_kcal'] for d in details]):.1f} kcal/day\n")
            f.write(f"  Dream (scaled): {np.mean([d['dream_scaled_kcal'] for d in details]):.1f} kcal/day\n")
            f.write(f"  Coherent thought: {results['mean_thought_kcal_per_day']:.1f} kcal/day\n\n")
            
            f.write("="*80 + "\n")
            f.write("END OF REPORT\n")
            f.write("="*80 + "\n")
        
        print(f"Text report saved to: {report_path}")


def main():
    """Run thought metabolism analysis."""
    # Initialize analyzer
    analyzer = ThoughtMetabolismAnalyzer(
        sleep_data_path='public/sleep_summary.json',
        activity_data_path='public/activity.json'
    )
    
    # Run analysis
    results = analyzer.analyze(body_weight_kg=70)  # Adjust weight as needed
    
    # Save results
    analyzer.save_results('thought_metabolism_results.json')
    
    # Generate visualizations
    analyzer.visualize('thought_metabolism_figures')
    
    print("\nAnalysis complete!")
    print("Check 'thought_metabolism_results.json' for detailed results")
    print("Check 'thought_metabolism_figures/' for visualizations")


if __name__ == '__main__':
    main()

